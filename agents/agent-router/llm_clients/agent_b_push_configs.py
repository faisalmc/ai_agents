"""
Author: Faisal Chaudhry
Agent-B = Push Task specific configs by executing push_cli_configs.py
"""

import os
import glob
import subprocess
import re
from datetime import datetime

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

import threading

import sys
sys.path.append("/app/shared")
from push_core import push_configs

import logging
logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

# for agent-2 to invoke agent-3 and give LLM driven results
import json
import httpx
from typing import List, Dict
from llm_api import call_llm

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# for agent-2 to invoke agent-3 and give LLM driven results
AGENT3_URL = os.getenv("AGENT3_URL", "http://agent_3:8002/analyze-host-json")

app = App(token=SLACK_BOT_TOKEN)
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Flexible error patterns for both IOS and IOS-XR
GENERIC_ERROR_PATTERNS = [
    r"%\s*Invalid input.*",
    r"%\s*Incomplete command.*",
    r"%\s*Ambiguous command.*",
    r"%\s*Unrecognized command.*",
    r"commit.*failed",
    r"config apply failed",
    r"syntax error",
    r"\^.*%.*input.*",  # caret marker with error
    r"%\s*Error.*",
    r"error:.*",
    r"ERROR:.*",
    r"command rejected",
    r"unknown command",
]

def run_push_script(config_dir, task_dir):
    repo_dir = os.path.join("/app/doo", config_dir)
    script_name = "push_cli_configs.py"
    script_path = os.path.join(repo_dir, script_name)
    cmd = ["python3", script_path, "--task", task_dir]

    print(f"[DEBUG] Checking for script at: {script_path}", flush=True)
    print(f"[DEBUG] Task Dir: {task_dir}", flush=True)
    print(f"[DEBUG] Will run command: {' '.join(cmd)} in dir: {repo_dir}", flush=True)

    try:
        files = os.listdir(repo_dir)
        print(f"[DEBUG] Files in repo_dir ({repo_dir}): {files}", flush=True)
    except Exception as e:
        print(f"[ERROR] Could not list repo_dir: {e}", flush=True)
        return "", f"[ERROR] Could not list repo_dir: {e}", -1

    if not os.path.isfile(script_path):
        print(f"[ERROR] Script not found at: {script_path}", flush=True)
        return "", f"[ERROR] Script not found at: {script_path}", -1

    print(f"[INFO] Found script. Attempting to run it now...", flush=True)
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        stdout = result.stdout
        stderr = result.stderr
        rc = result.returncode

        print(f"[DEBUG] Subprocess return code: {rc}", flush=True)
        print(f"[DEBUG] STDOUT (first 500 chars):\n{stdout[:500]}", flush=True)
        print(f"[DEBUG] STDERR (first 500 chars):\n{stderr[:500]}", flush=True)

        # Check if all lines are [SKIP]
        skip_lines = [line for line in stdout.splitlines() if "[SKIP]" in line]
        if skip_lines and len(skip_lines) >= 3:
            print(f"[WARN] Script ran but skipped configs for all devices. Nothing was pushed.", flush=True)

        # Optional: Warn if script exited successfully but no logs were found
        if rc == 0:
            expected_log_dir = os.path.join("/app/doo", config_dir, task_dir, "logs")
            if not glob.glob(os.path.join(expected_log_dir, "*.log")):
                print(f"[WARN] Script exited with return code 0 but no log files were found in: {expected_log_dir}", flush=True)

        return stdout, stderr, rc

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Script timed out after 300 seconds", flush=True)
        return "", "[ERROR] Script timeout", -1
    except Exception as e:
        print(f"[ERROR] Exception running subprocess: {e}", flush=True)
        return "", f"[ERROR] Exception: {e}", -1


def basic_log_analysis(config_dir, task_dir):
    log_dir = os.path.join("/app/doo", config_dir, task_dir, "logs")
    results = []
    error_hosts = []
    found_logs = glob.glob(os.path.join(log_dir, "*.log"))
    print(f"[DEBUG] Searching for logs in: {log_dir}", flush=True)
    print(f"[DEBUG] Found log files: {found_logs}", flush=True)

    if not found_logs:
        results.append(("logs", "No .log files found. Check if push script ran correctly."))
        return results, error_hosts, log_dir

    for logfile in sorted(found_logs):
        hostname = os.path.basename(logfile).replace(".log", "")
        try:
            with open(logfile) as f:
                log = f.read()
        except Exception as e:
            results.append((hostname, f"Could not read log: {e}"))
            continue

        issues = []

        # Use the generic error patterns
        combined_patterns = GENERIC_ERROR_PATTERNS

        # Detect standard CLI errors
        for pattern in combined_patterns:
            if re.search(pattern, log, re.IGNORECASE | re.MULTILINE):
                issues.append(f"Matched: {pattern}")
                print(f"[DEBUG] Matched error in {hostname}: {pattern}", flush=True)

        # Detect caret + invalid input errors across multiple lines
        if re.search(r"\s*\^\s*\n.*% Invalid input", log, re.IGNORECASE):
            issues.append("Caret Invalid Input Detected")
            print(f"[DEBUG] Detected caret error pattern in {hostname}", flush=True)

        if issues:
            error_hosts.append(hostname)
        results.append((hostname, "; ".join(issues) if issues else "Success"))

    return results, error_hosts, log_dir



def generate_summary_md(log_dir, output_path):
    print(f"[DEBUG] Generating summary markdown at: {output_path}", flush=True)
    try:
        with open(output_path, 'w') as summary:
            for log_file in sorted(os.listdir(log_dir)):
                if log_file.endswith('.log'):
                    summary.write(f"## {log_file}\n\n")
                    with open(os.path.join(log_dir, log_file), 'r') as lf:
                        content = lf.read()
                        summary.write("```\n")
                        summary.write(content)
                        summary.write("\n```\n\n")
    except Exception as e:
        print(f"[ERROR] Failed to generate summary markdown: {e}", flush=True)

# for agent-2 to invoke agent-3
# === Agent-3 fan-out (sequential for minimal churn) ===
def fetch_agent3_analyses(hosts: List[str], config_dir: str, task_dir: str) -> Dict[str, dict]:
    """
    Calls Agent-3 /analyze-host-json once per host.
    Returns {host: analysis_json} where analysis_json matches Agent-3's schema.
    """
    results: Dict[str, dict] = {}
    for h in hosts:
        payload = {"hostname": h, "config_dir": config_dir, "task_id": task_dir}
        try:
            with httpx.Client(timeout=httpx.Timeout(10.0, connect=3.0)) as client:
                r = client.post(AGENT3_URL, json=payload)
                if r.headers.get("content-type", "").startswith("application/json"):
                    results[h] = r.json()
                else:
                    results[h] = {
                        "issue": "Bad content-type",
                        "explanation": f"Expected JSON, got: {r.headers.get('content-type')}",
                        "recommendation": "Check Agent-3 /analyze-host-json endpoint.",
                        "confidence": "unknown",
                        "needs_more_context": True
                    }
        except Exception as e:
            results[h] = {
                "issue": "Agent-3 unreachable",
                "explanation": str(e),
                "recommendation": "Verify Agent-3 is running and reachable at AGENT3_URL.",
                "confidence": "unknown",
                "needs_more_context": True
            }
    return results


# === LLM summary prompt (verbatim spec we agreed) ===
SYSTEM_PROMPT_SUMMARY = """
You are summarizing per-host configuration analyses produced by Agent-3.
For each host, the analysis object contains: issue, explanation, recommendation, confidence, needs_more_context.

Classify each host as:
- "success" if the analysis indicates there are no material errors (e.g., “No specific issue detected.” or explanation that configuration applied successfully).
- "failure" if any material error is present (e.g., SSH/transport errors, syntax/commit errors).
- "analysis_unavailable" if the analysis object is missing, invalid JSON, or not readable.

Compute totals across all hosts: devices (N), success (S), failed (F), analysis_unavailable (U).
Do NOT compute or report percentages.

Return ONE JSON object ONLY, with exactly these top-level fields:

{
  "slack_text": "<final concise Slack message, multi-line, suitable to post as-is>",
  "summary_json": {
    "task_id": "<as provided>",
    "config_dir": "<as provided>",
    "totals": { "devices": N, "success": S, "failed": F, "analysis_unavailable": U },
    "hosts": [
      {
        "host": "<hostname>",
        "status": "success|failure|analysis_unavailable",
        "issue": "<short issue or 'None'>",
        "recommendation": "<short action or 'None'>",
        "confidence": "<high|medium|low|unknown>"
      }
    ]
  }
}

Slack text constraints:
- Start with the line: "*Post-Deploy Overview*"
- Show Task and Config Dir each on their own line as: "*Task:* `<task_id>`", "*Config Dir:* `<config_dir>`"
- Show Totals on a single line immediately after those: "*Totals:* Devices=N | Success=S | Failed=F | Analysis Unavailable=U"
- If failures exist, add a blank line then "*Failures:*" followed by a bulleted list ("• <host> — <reason>")
- Use bold labels and backticks for IDs
- Keep the message compact and Slack-friendly. No emojis required.

Do not include any additional fields or text outside the JSON object.
""".strip()

# .. continuation of above > for agent-2 to invoke agent-3
def build_llm_messages_for_summary(task_id: str, config_dir: str, per_host_results: Dict[str, dict]):
    payload = {
        "task_id": task_id,
        "config_dir": config_dir,
        "per_host": [{"host": h, "analysis": per_host_results.get(h)} for h in sorted(per_host_results.keys())],
        "constraints": {"compute_percentages": False}
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT_SUMMARY},
        {"role": "user", "content": json.dumps(payload)}
    ]


def do_deploy(config_dir: str, task_dir: str, channel_id: str, thread_ts: str | None, requested_by: str | None) -> dict:
    """
    Runs the exact same push_configs flow and posts to Slack (channel/thread).
    Returns a small JSON summary for the HTTP caller (orchestrator).
    """
    # single source of truth
    result = push_configs(
        # task_id=task_dir,           # metadata only
        config_dir=config_dir,
        task_dir=task_dir,
        dry_run=False               # keep as-is for agent-2
    )

    per_device = result["per_device"]
    ok = [d["hostname"] for d in per_device if d["ok"]]
    err = {d["hostname"]: d["details"] for d in per_device if not d["ok"]}

    timestamp = result["meta"]["timestamp_utc"]
    summary_md = result["artifacts"]["summary_md"]
    summary_md_filename = os.path.basename(summary_md) if summary_md else "push_cli_configs-summary.md"

    lines = [
        "*Configuration Summary*",
        f"*Task:* `{task_dir}`",
        f"*Config Dir:* `{config_dir}`",
        f"*Timestamp:* {timestamp}",
        "",
        # f" *{len(ok)} devices successfully configured:* {', '.join(sorted(ok)) or 'None'}",
        # f" *{len(err)} devices failed:* {', '.join(sorted(err.keys())) or 'None'}",
        f"*Configuration attempt completed for {len(per_device)} device(s).*",
        f"_Final status (success/fail) will be posted below in **Post-Deploy Overview** after per-host analysis._",
        "",
        f"*A detailed log file (`{summary_md_filename}`) is attached below for review.*"
    ]
    # BEFORE:
    # slack_client.chat_postMessage(
    #     channel=channel_id,
    #     thread_ts=thread_ts if thread_ts else None,
    #     text="\n".join(lines)
    # )
    # AFTER (captures ts and ensures a thread exists)
    post_resp = slack_client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts if thread_ts else None,
        text="\n".join(lines)
    )
    # NEW: if no incoming thread_ts, start one anchored to the bot’s first message
    thread_ts = thread_ts or post_resp.get("ts")

    if summary_md and os.path.exists(summary_md):
        with open(summary_md, "rb") as f:
            slack_client.files_upload_v2(
                channel=channel_id,
                thread_ts=thread_ts if thread_ts else None,
                file=f,
                title="Configuration Logs",
                filename=summary_md_filename,
                initial_comment=f"Attached log file: `{summary_md_filename}`"
            )
    else:
        print("[WARN] Markdown summary file was not created.", flush=True)

    # === NEW: Post-deploy overview (Agent-3 analyses + LLM summary) ===
    try:
        # 1) Collect target hosts from push result
        per_device = result["per_device"]
        hosts = [d["hostname"] for d in per_device]

        # 2) Ask Agent-3 to analyze each host (writes agent3_<HOST>-analysis.json)
        agent3_map = fetch_agent3_analyses(hosts=hosts, config_dir=config_dir, task_dir=task_dir)

        # 3) Build LLM messages and call your existing LLM backend
        messages = build_llm_messages_for_summary(task_id=task_dir, config_dir=config_dir, per_host_results=agent3_map)
        llm_raw = call_llm(messages)

        # 4) Parse LLM output and persist artifacts
        try:
            llm_obj = json.loads(llm_raw)
        except json.JSONDecodeError:
            print("[ERROR] LLM summary is not valid JSON. Posting fallback note.", flush=True)
            slack_client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts if thread_ts else None,
                text="Post-Deploy Overview\n(LLM summary unavailable: invalid JSON response)"
            )
            # keep original return contract
            return {
                "status": "ok",
                "meta": {"timestamp": timestamp},
                "ok_devices": sorted([d["hostname"] for d in per_device if d["ok"]]),
                "error_devices": sorted([d["hostname"] for d in per_device if not d["ok"]]),
                "summary_md": summary_md_filename,
                "requested_by": requested_by
            }

        slack_text = llm_obj.get("slack_text", "Post-Deploy Overview\n(LLM summary missing)")
        summary_json = llm_obj.get("summary_json", {})

        # Save agent2_summary.json (+ optional .md mirror)
        out_dir = os.path.join("/app/doo", config_dir, task_dir)
        os.makedirs(out_dir, exist_ok=True)
        agent2_json_path = os.path.join(out_dir, "agent2_summary.json")
        with open(agent2_json_path, "w") as f:
            json.dump(summary_json, f, indent=2)

        agent2_md_path = os.path.join(out_dir, "agent2_summary.md")
        try:
            with open(agent2_md_path, "w") as f:
                f.write(slack_text + "\n")
        except Exception as e:
            print(f"[WARN] Could not write agent2_summary.md: {e}", flush=True)

        # 5) Post Slack summary to same thread + attach JSON
        slack_client.chat_postMessage(
            channel=channel_id,
            thread_ts=thread_ts if thread_ts else None,
            text=slack_text
        )
        try:
            with open(agent2_json_path, "rb") as f:
                slack_client.files_upload_v2(
                    channel=channel_id,
                    thread_ts=thread_ts if thread_ts else None,
                    file=f,
                    title="agent2_summary.json",
                    filename="agent2_summary.json",
                    initial_comment="Attached overall summary (JSON)."
                )
        except Exception as e:
            print(f"[WARN] Could not attach agent2_summary.json: {e}", flush=True)

    except Exception as e:
        print(f"[ERROR] Post-deploy overview failed: {e}", flush=True)
        slack_client.chat_postMessage(
            channel=channel_id,
            thread_ts=thread_ts if thread_ts else None,
            text=f"Post-Deploy Overview\n(Encountered error: {e})"
        )

    return {
        "status": "ok",
        "meta": {"timestamp": timestamp},
        "ok_devices": sorted(ok),
        "error_devices": sorted(err.keys()),
        "summary_md": summary_md_filename,
        "requested_by": requested_by
    }

@app.command("/push-configs")
def handle_push_configs(ack, command):
    print("[DEBUG] /push-configs received:", command, flush=True)  #
    try:
        # Immediate ephemeral acknowledgment (same as HND)
        ack({"response_type": "ephemeral", "text": "Starting configuration task !!"})
    except Exception as e:
        print(f"[ERROR] Failed to ack: {e}", flush=True)
        return

    def work():
        try:
            text = command.get("text", "").strip()
            if not text or len(text.split()) != 2:
                slack_client.chat_postMessage(
                    channel=command["channel_id"],
                    text="Usage: `/push-configs <config_dir> <task_dir>`"
                )
                return

            config_dir, task_dir = text.split()

            # single source of truth
            result = push_configs(
                # task_id=task_dir,           # metadata only
                config_dir=config_dir,
                task_dir=task_dir,
                dry_run=False               # keep as-is for agent-2
            )

            per_device = result["per_device"]
            ok = [d["hostname"] for d in per_device if d["ok"]]
            err = {d["hostname"]: d["details"] for d in per_device if not d["ok"]}

            timestamp = result["meta"]["timestamp_utc"]
            summary_md = result["artifacts"]["summary_md"]
            summary_md_filename = os.path.basename(summary_md) if summary_md else "push_cli_configs-summary.md"

            message_lines = [
                "*Configuration Summary*",
                f"*Task:* `{task_dir}`",
                f"*Config Dir:* `{config_dir}`",
                f"*Timestamp:* {timestamp}",
                "",
                # f" *{len(ok)} devices successfully configured:* {', '.join(sorted(ok)) or 'None'}",
                # f" *{len(err)} devices failed:* {', '.join(sorted(err.keys())) or 'None'}",
                f"*Configuration attempt completed for {len(per_device)} device(s).*",
                f"_Final status (success/fail) will be posted below in **Post-Deploy Overview** after per-host analysis._",
                "",
                f"*A detailed log file (`{summary_md_filename}`) is attached below for review.*"
            ]
            # NEW: capture ts to thread replies under this message
            post_resp = slack_client.chat_postMessage(channel=command["channel_id"], text="\n".join(message_lines))  # NEW
            parent_ts = post_resp.get("ts")  # NEW

            if summary_md and os.path.exists(summary_md):
                with open(summary_md, "rb") as f:
                    slack_client.files_upload_v2(
                        channel=command["channel_id"],
                        thread_ts=parent_ts,  # NEW (attach in the same thread)
                        file=f,
                        title="Configuration Logs",
                        filename=summary_md_filename,
                        initial_comment=f"Attached log file: `{summary_md_filename}`"
                    )
            else:
                print("[WARN] Markdown summary file was not created.", flush=True)

            # === NEW: Post-deploy overview (Agent-3 per-host + LLM summary) in same thread ===
            try:
                hosts = [d["hostname"] for d in per_device]
                agent3_map = fetch_agent3_analyses(hosts=hosts, config_dir=config_dir, task_dir=task_dir)

                messages = build_llm_messages_for_summary(task_id=task_dir, config_dir=config_dir, per_host_results=agent3_map)
                llm_raw = call_llm(messages)

                try:
                    llm_obj = json.loads(llm_raw)
                except json.JSONDecodeError:
                    slack_client.chat_postMessage(
                        channel=command["channel_id"],
                        thread_ts=parent_ts,  # keep in thread
                        text="Post-Deploy Overview\n(LLM summary unavailable: invalid JSON response)"
                    )
                    return

                slack_text = llm_obj.get("slack_text", "Post-Deploy Overview\n(LLM summary missing)")
                summary_json = llm_obj.get("summary_json", {})

                out_dir = os.path.join("/app/doo", config_dir, task_dir)
                os.makedirs(out_dir, exist_ok=True)
                agent2_json_path = os.path.join(out_dir, "agent2_summary.json")
                with open(agent2_json_path, "w") as f:
                    json.dump(summary_json, f, indent=2)

                # Optional mirror
                try:
                    with open(os.path.join(out_dir, "agent2_summary.md"), "w") as f:
                        f.write(slack_text + "\n")
                except Exception as e:
                    print(f"[WARN] Could not write agent2_summary.md: {e}", flush=True)

                # Post the LLM summary in same thread
                slack_client.chat_postMessage(
                    channel=command["channel_id"],
                    thread_ts=parent_ts,  # NEW
                    text=slack_text
                )
                # Attach the JSON artifact in same thread
                try:
                    with open(agent2_json_path, "rb") as f:
                        slack_client.files_upload_v2(
                            channel=command["channel_id"],
                            thread_ts=parent_ts,  # NEW
                            file=f,
                            title="agent2_summary.json",
                            filename="agent2_summary.json",
                            initial_comment="Attached overall summary (JSON)."
                        )
                except Exception as e:
                    print(f"[WARN] Could not attach agent2_summary.json: {e}", flush=True)

            except Exception as e:
                print(f"[ERROR] Post-deploy overview (command) failed: {e}", flush=True)
                slack_client.chat_postMessage(
                    channel=command["channel_id"],
                    thread_ts=parent_ts,  # keep errors in same thread
                    text=f"Post-Deploy Overview\n(Encountered error: {e})"
                )

        except Exception as e:
            print(f"[ERROR] Exception in /push-configs handler: {e}", flush=True)
            slack_client.chat_postMessage(channel=command["channel_id"], text=f"Exception occurred: {e}")

    # Run work in background thread (same as HND)
    threading.Thread(target=work).start()


api = FastAPI()

@api.post("/deploy")
async def http_deploy(req: Request):
    """
    JSON body:
    {
      "config_dir": "configs.5",
      "task_id": "task-1",
      "channel": "Cxxxxx",
      "thread_ts": "1712345678.901234",   # optional
      "requested_by": "Uxxxxx"            # optional
    }
    """
    try:
        body = await req.json()
        config_dir = body.get("config_dir")
        task_id = body.get("task_id") or body.get("task_dir")
        channel = body.get("channel")
        thread_ts = body.get("thread_ts")
        requested_by = body.get("requested_by")

        if not config_dir or not task_id or not channel:
            return JSONResponse(status_code=400, content={"status": "error", "error": "config_dir, task_id, and channel are required"})

        result = do_deploy(config_dir=config_dir, task_dir=task_id, channel_id=channel, thread_ts=thread_ts, requested_by=requested_by)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        print(f"[ERROR] /deploy failed: {e}", flush=True)
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})

# if __name__ == "__main__":
    # print("[DEBUG] Bolt app is starting...", flush=True)
    # SocketModeHandler(app, SLACK_APP_TOKEN).start()

if __name__ == "__main__":
    print("[DEBUG] Bolt app is starting...", flush=True)
    try:
        resp = slack_client.auth_test()
        print(f"[DEBUG] Slack auth_test ok: team={resp.get('team')} user={resp.get('user')}", flush=True)
    except Exception as e:
        print(f"[ERROR] slack_client.auth_test failed: {e}", flush=True)

    # Start FastAPI (HTTP) + Bolt (Socket Mode) side-by-side
    def start_bolt():
        SocketModeHandler(app, SLACK_APP_TOKEN).start()

    def start_http():
        # Bind to 0.0.0.0:8001 – matches your docker-compose service port
        uvicorn.run(api, host="0.0.0.0", port=8001, log_level="info")

    t1 = threading.Thread(target=start_bolt, daemon=True)
    t1.start()

    start_http()  # block here; Bolt runs in background thread