# agent-d-oper-check.py
# Author: Faisal Chaudhry
# Purpose: Capture and report operational status (show command logs) for devices

import os
import json
import subprocess
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from llm_api import call_llm

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "all-sp")
REPO_ROOT = "/app/doo"

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

# --- Shared local memory for shows (observed) ---
AGENT_KNOWLEDGE_ROOT = os.getenv("AGENT_KNOWLEDGE_ROOT", "/app/doo/_agent_knowledge").rstrip("/")
OBSERVED_ROOT = os.path.join(AGENT_KNOWLEDGE_ROOT, "observed")  # /_agent_knowledge/observed/<config>/<task>/commands.txt

def _append_unique_lines(path: str, lines: list[str]):
    """Append new lines to a text file if they are not already present."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            existing = set(l.strip() for l in fh if l.strip())
    new = [l.strip() for l in lines if l.strip() and l.strip() not in existing]
    if new:
        with open(path, "a", encoding="utf-8") as fh:
            for l in new:
                fh.write(l + "\n")

def debug(msg):
    print(f"[agent-d] {msg}", flush=True)

def list_devices_with_txt(task_path):
    full_path = os.path.join(REPO_ROOT, task_path)
    return sorted([f[:-4] for f in os.listdir(full_path) if f.endswith(".txt")])

def list_devices_with_logs(task_path):
    log_path = os.path.join(REPO_ROOT, task_path, "grading_logs")
    return sorted([f[:-3] for f in os.listdir(log_path) if f.endswith(".md")])

def extract_show_cmds_description(config_dir, task_name):
    """
    Read show_cmds.ini from /app/doo/<config_dir>/<task_name>/show_cmds.ini,
    ask the LLM to summarize (intent, command, protocol). If LLM returns
    non-JSON or empty, fall back to naive parsing of 'show ...' lines.

    Side-effect (Phase-1): persist the raw 'show ...' lines into
      /app/doo/_agent_knowledge/observed/<config_dir>/<task_name>/commands.txt
    so Agent-5 can treat them as trusted observed commands.
    """
    import re
    ini_path = os.path.join(REPO_ROOT, config_dir, task_name, "show_cmds.ini")

    if not os.path.exists(ini_path):
        debug(f"show_cmds.ini not found at per-task path: {ini_path}")
        return []

    try:
        with open(ini_path, "r", encoding="utf-8") as f:
            ini_text = f.read()
    except Exception as e:
        debug(f"[ERROR] Failed reading show_cmds.ini at {ini_path}: {e}")
        return []

    def _fallback_parse_commands(ini_text_local):
        """
        Very simple extractor: returns [{'command': 'show ...'}] for each unique show line found.
        Ignores commented lines (# or ;).
        """
        cmds, seen = [], set()
        for raw in ini_text_local.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            # capture "command = show ..." or plain "show ..."
            m = re.search(r'(?:^|=)\s*(show\s+.+)$', line, flags=re.IGNORECASE)
            if m:
                cmd = m.group(1).strip()
                if cmd.lower().startswith("show ") and cmd not in seen:
                    seen.add(cmd)
                    cmds.append({"command": cmd})
        debug(f"[fallback] extracted {len(cmds)} show commands from INI")
        return cmds

    # -------- NEW: persist observed commands (raw) for Agent-5 ----------
    try:
        raw_shows = []
        for raw in ini_text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            m = re.search(r'(?:^|=)\s*(show\s+.+)$', line, flags=re.IGNORECASE)
            if m:
                cmd = m.group(1).strip()
                if cmd.lower().startswith("show "):
                    raw_shows.append(cmd)
        if raw_shows:
            observed_path = os.path.join(OBSERVED_ROOT, config_dir, task_name, "commands.txt")
            _append_unique_lines(observed_path, sorted(set(raw_shows)))
            debug(f"[observed] appended {len(set(raw_shows))} shows → {observed_path}")
    except Exception as e:
        debug(f"[observed] failed to persist observed shows: {e}")
    # --------------------------------------------------------------------

    # --- LLM path (for Slack explanation only) ---
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Cisco operations assistant. Analyze the content of show_cmds.ini. "
                "For each show command, explain the operational intent in 1 line, and extract the associated protocol "
                "(e.g., BGP, ISIS, MPLS). Respond in JSON format as a list of {intent, command, protocol} objects."
            )
        },
        {"role": "user", "content": f"```ini\n{ini_text}\n```"}
    ]

    try:
        raw = call_llm(messages)
        if not raw or not str(raw).strip():
            debug("[LLM] Empty response; using fallback parser.")
            return _fallback_parse_commands(ini_text)

        # Try direct JSON parse
        try:
            out = json.loads(raw)
            if isinstance(out, dict):
                out = [out]
            if isinstance(out, list):
                debug(f"[LLM] Parsed JSON with {len(out)} items.")
                return out
        except json.JSONDecodeError:
            # Try to recover JSON from a fenced code block (```json ... ```)
            block = None
            m = re.search(r"```json\s*(.+?)\s*```", raw, flags=re.DOTALL | re.IGNORECASE)
            if m:
                block = m.group(1)
            else:
                # As a last resort, grab the first [ ... ] or { ... } blob
                m2 = re.search(r"(\[.*\]|\{.*\})", raw, flags=re.DOTALL)
                if m2:
                    block = m2.group(1)
            if block:
                try:
                    out = json.loads(block)
                    if isinstance(out, dict):
                        out = [out]
                    if isinstance(out, list):
                        debug(f"[LLM] Recovered JSON from code block with {len(out)} items.")
                        return out
                except json.JSONDecodeError as je:
                    debug(f"[LLM] JSON recovery failed: {je}")

        # If we reach here, LLM didn’t give valid JSON
        debug("[LLM] Response not JSON; using fallback parser.")
        return _fallback_parse_commands(ini_text)

    except Exception as e:
        debug(f"[ERROR] Failed to parse show_cmds.ini via LLM: {e}")
        return _fallback_parse_commands(ini_text)



def run_show_capture(config_dir, task_name):
    script_path = os.path.join(REPO_ROOT, config_dir, "run_show_commands.py")
    debug(f"Executing: python3 {script_path} --task {task_name}")
    try:
        output = subprocess.check_output(
            ["python3", script_path, "--task", task_name],
            stderr=subprocess.STDOUT,
            text=True
        )
        debug("run_show_commands.py output:\n" + output)
        return True
    except subprocess.CalledProcessError as e:
        debug(f"[ERROR] Script failed: {e.output}")
        return False

# def post_operational_summary(task_name, config_dir, channel_id):
#     task_path = os.path.join(config_dir, task_name)
#     devices_with_txt = list_devices_with_txt(task_path)
#     devices_with_logs = list_devices_with_logs(task_path)

#     total = len(devices_with_txt)
#     with_cmds = len(devices_with_logs)
#     no_cmds = total - with_cmds

#     timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

#     result_msg = f"""
# :white_check_mark: Operational Check Summary

# *Task:* `{task_name}`
# *Config Dir:* `{config_dir}`
# *Timestamp:* `{timestamp}`

# • Total devices listed (with .txt configs): {total}
# • Devices with configs and matching show commands: {with_cmds}
# • Devices with configs but **no show commands defined**: {no_cmds}
# • Validation status:  Not performed (raw .md logs only)
# """

#     try:
#         client.chat_postMessage(channel=channel_id, text=result_msg)
#     except SlackApiError as e:
#         debug(f"[SlackError] {e.response['error']}\nMessage attempted: {result_msg}")

def post_operational_summary(task_name, config_dir, channel_id):
    task_path = os.path.join(config_dir, task_name)
    devices_with_txt = list_devices_with_txt(task_path)
    devices_with_logs = list_devices_with_logs(task_path)

    total = len(devices_with_txt)
    with_cmds = len(devices_with_logs)
    no_cmds = total - with_cmds

    # Pull command list (safe to ignore errors)
    cmd_meta = extract_show_cmds_description(config_dir, task_name)  # returns [{intent, command, protocol}, ...] or []
    commands = [item.get("command", "").strip() for item in cmd_meta if item.get("command")]
    if not commands:
        commands = ["(could not read show_cmds.ini)"]

    # Compose strings
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    grading_path = os.path.join(REPO_ROOT, config_dir, task_name, "grading_logs")
    devices_csv = ", ".join(devices_with_txt) if devices_with_txt else "(none)"
    analyze_cmd = f"/operational-analyze {config_dir} {task_name}"

    persist_note = f"\n_Persisted {len(commands)} commands to observed memory for Agent-5._"

    # Block Kit message (clean, no emojis/icons)
    blocks = [
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Operational Check Summary*\n\n"
                          f"*Task:* `{task_name}`\n"
                          f"*Config Dir:* `{config_dir}`\n"
                          f"*Timestamp:* `{timestamp}`"}},
        {"type": "section",
        "text": {"type": "mrkdwn",
                "text": "*What I ran*\n"
                        "• Show commands loaded from `show_cmds.ini`:\n"
                        + "\n".join([f"  - `{c}`" for c in commands[:8]])
                        + ("\n  - …" if len(commands) > 8 else "")
                        + persist_note}},
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Where I ran it*\n"
                          f"• Devices targeted ({total}): {devices_csv}"}},
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*What I captured*\n"
                          f"• Per-device Markdown logs: `{grading_path}/*.md`\n"
                          f"• Devices with logs: {with_cmds}\n"
                          f"• Devices with configs in this task but no captured output from operational commands: {no_cmds}"}},
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Next step*\n"
                          "• To analyze these logs and get device-level health:\n"
                          f"  `{analyze_cmd}`"}},
        # Optional: Add a button to trigger analysis if you wire up a block action
        # {"type": "actions",
        #  "elements": [
        #      {"type": "button", "text": {"type": "plain_text", "text": "Run Analysis"},
        #       "action_id": "oper_analyze",
        #       "value": json.dumps({"config_dir": config_dir, "task_name": task_name})}
        #  ]}
    ]

    try:
        client.chat_postMessage(channel=channel_id, blocks=blocks, text="Operational Check Summary")
    except SlackApiError as e:
        # Fallback to plain text if blocks fail
        debug(f"[SlackError] {e.response['error']} — falling back to text")
        result_msg = (
            "Operational Check Summary\n\n"
            f"Task: `{task_name}`\n"
            f"Config Dir: `{config_dir}`\n"
            f"Timestamp: `{timestamp}`\n\n"
            "What I ran\n"
            "• Show commands loaded from `show_cmds.ini`:\n" +
            "\n".join([f"  - {c}" for c in commands]) + "\n\n" +
            "Where I ran it\n"
            f"• Devices targeted ({total}): {devices_csv}\n\n"
            "What I captured\n"
            f"• Per-device Markdown logs: `{grading_path}/*.md`\n"
            f"• Devices with logs: {with_cmds}\n"
            f"• Devices missing logs: {no_cmds}\n\n"
            "Next step\n"
            f"• To analyze these logs and get device-level health:\n  `{analyze_cmd}`"
        )
        client.chat_postMessage(channel=channel_id, text=result_msg)

@app.command("/operational-check")
def handle_oper_check(ack, respond, command):
    try:
        ack({"response_type": "ephemeral", "text": "Starting operational check ⏳"})
    except Exception as e:
        debug(f"[ERROR] Failed to ack: {e}")
        return

    try:
        args = command.get("text", "").strip().split()
        if len(args) != 2:
            respond("Usage: /operational-check <config_dir> <task>")
            return

        config_dir, task_name = args
        channel_id = command["channel_id"]

        def work():
            debug(f"[INFO] Slack request received: {args}")
            # success = run_show_capture(task_name)
            success = run_show_capture(config_dir, task_name)


            if success:
                post_operational_summary(task_name, config_dir, channel_id)
            else:
                client.chat_postMessage(channel=channel_id, text=":x: Error running operational check script")

        import threading
        threading.Thread(target=work).start()

    except Exception as e:
        debug(f"[ERROR] handle_oper_check: {e}")
        try:
            respond(f"Exception occurred: {e}")
        except:
            pass

if __name__ == "__main__":
    print("[DEBUG] Agent-D is running...", flush=True)
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
