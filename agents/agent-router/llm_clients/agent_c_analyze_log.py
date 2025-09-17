# agent_c_analyze_log.py
# Author: Faisal Chaudhry
# Purpose: Analyze device log and respond to Slack /analyze-log (via Socket Mode)

import os
import json
from datetime import datetime
import threading
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from llm_api import call_llm

# ADD:
from typing import Dict

# --- Config
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "general")  # Must be without '#'

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)


def analyze_log_with_llm(full_log_text):
    system_prompt = (
        "You are a Cisco-certified expert (CCIE-SP level). "
        "Analyze the provided router CLI logs (IOS, IOS-XR). "
        "If you see CLI or commit errors, describe them. "
        "If there are no errors, state clearly that the configuration applied successfully. "
        "Always respond with a JSON object containing:\n"
        "- issue: brief summary of problem or 'No errors detected'\n"
        "- explanation: why this issue happened or 'Configuration applied cleanly'\n"
        "- recommendation: suggested fix or 'No action needed'\n"
        "- confidence: low/medium/high\n"
        "- needs_more_context: true/false"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Analyze the following router log and return the JSON result:\n\n{full_log_text[:10000]}"
        }
    ]

    print("[DEBUG] Sending full log to LLM", flush=True)
    print("[DEBUG] Preview of full log:\n", full_log_text[:500], flush=True)

    response = call_llm(messages)
    print("[DEBUG] Raw LLM response:", response, flush=True)
    return response


def apply_confidence_threshold(summary):
    confidence = summary.get("confidence", "").lower()
    if confidence not in ["low", "medium", "high"]:
        summary["confidence"] = "unknown"
        summary["needs_more_context"] = True
        summary["explanation"] += " | Confidence not provided."
        print("[DEBUG] Confidence missing, marked as unknown", flush=True)
    elif confidence == "low":
        summary["needs_more_context"] = True
        summary["recommendation"] += " | Manual review recommended."
        print("[DEBUG] Low confidence detected", flush=True)
    return summary

# ADD: pure analysis used by HTTP endpoint (no Slack side effects)
def analyze_log_core(config_dir: str, task_id: str, hostname: str) -> Dict:
    """
    Read /app/doo/<config_dir>/<task_id>/logs/<hostname>.log,
    run LLM analysis, return the same JSON shape Agent-3 produces today.
    """
    log_path = os.path.join("/app/doo", config_dir, task_id, "logs", f"{hostname}.log")
    print(f"[DEBUG] (core) Looking for log at: {log_path}", flush=True)

    if not os.path.exists(log_path):
        return {
            "issue": "Log not found",
            "explanation": f"Expected at: {log_path}",
            "recommendation": "Verify push completed and logs are present.",
            "confidence": "unknown",
            "needs_more_context": True
        }

    with open(log_path, "r") as f:
        full_log = f.read()

    llm_result = analyze_log_with_llm(full_log)

    try:
        cleaned = llm_result.strip()
        # Remove Markdown fences if present
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")        # remove backticks
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()   # drop 'json' label

        summary = json.loads(cleaned)
        # summary = json.loads(llm_result)
        print("[DEBUG] (core) Parsed valid JSON from LLM.", flush=True)
    except json.JSONDecodeError as e:
        print(f"[ERROR] (core) Could not parse JSON from LLM: {e}", flush=True)
        summary = {
            "issue": "LLM output not in JSON format",
            "explanation": "",
            "recommendation": "",
            "confidence": "unknown",
            "needs_more_context": True,
            "raw_response": llm_result
        }

    summary = apply_confidence_threshold(summary)
    return summary

# ADD: persist file with agreed Agent-3 naming
def save_agent3_json(config_dir: str, task_id: str, hostname: str, summary: Dict) -> str:
    out_dir = os.path.join("/app/doo", config_dir, task_id)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"agent3_{hostname}-analysis.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[DEBUG] Wrote Agent-3 analysis: {out_path}", flush=True)
    return out_path


def post_to_slack(summary_json, task_path, task_name, hostname, channel_id):
    json_path = os.path.join("/tmp", f"{hostname}-analysis.json")
    with open(json_path, "w") as f:
        json.dump(summary_json, f, indent=2)

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    text_summary = f"""
*Log Analysis for* `{hostname}`
• Task: `{task_name}`
• Path: `{task_path}`
• Timestamp: `{timestamp}`
• Issue: `{summary_json.get("issue", "No issue reported")}`
• Explanation: `{summary_json.get("explanation", "N/A")}`
• Recommendation: `{summary_json.get("recommendation", "N/A")}`
• Confidence: `{summary_json.get("confidence", "unknown")}`
• Needs More Context: `{summary_json.get("needs_more_context", False)}`
"""

    try:
        print(f"[DEBUG] Posting summary for {hostname} to Slack", flush=True)
        client.chat_postMessage(channel=channel_id, text=text_summary)
        client.files_upload_v2(
            channel=channel_id,
            file=json_path,
            title=f"{hostname}-analysis.json",
            filename=f"{hostname}-analysis.json",
            initial_comment="Detailed JSON result attached."
        )
    except SlackApiError as e:
        print(f"[SlackError] {e.response['error']}", flush=True)


def analyze_log_entry(task_path, task_name, hostname, channel_id):
    log_path = os.path.join("/app/doo", task_path, task_name, "logs", f"{hostname}.log")
    print(f"[DEBUG] Looking for log at: {log_path}", flush=True)
    print(f"[DEBUG] File exists? {os.path.exists(log_path)}", flush=True)

    if not os.path.exists(log_path):
        print(f"[ERROR] Log not found: {log_path}", flush=True)
        return

    with open(log_path, "r") as f:
        full_log = f.read()

    print("[DEBUG] First 500 chars of log:\n", full_log[:500], flush=True)

    llm_result = analyze_log_with_llm(full_log)

    try:
        cleaned = llm_result.strip()

        # Remove Markdown fences if present
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")        # remove backticks
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()   # drop 'json' label

        summary = json.loads(cleaned)
        # summary = json.loads(llm_result)
        print("[DEBUG] Parsed valid JSON from LLM.", flush=True)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Could not parse JSON from LLM: {e}", flush=True)
        summary = {
            "issue": "LLM output not in JSON format",
            "explanation": "",
            "recommendation": "",
            "confidence": "unknown",
            "needs_more_context": True,
            "raw_response": llm_result
        }

    summary = apply_confidence_threshold(summary)
    post_to_slack(summary, task_path, task_name, hostname, channel_id)
    # Also persist using the agreed naming (agent3_<HOST>-analysis.json)
    try:
        save_agent3_json(task_path, task_name, hostname, summary)
    except Exception as e:
        print(f"[WARN] Could not save agent3 JSON in Slack path: {e}", flush=True)

@app.command("/analyze-log")
def handle_analyze_log(ack, command):
    try:
        ack({"response_type": "ephemeral", "text": "Analyzing log... Please wait ⏳"})
    except Exception as e:
        print(f"[ERROR] Failed to ack: {e}", flush=True)
        return

    def run_analysis():
        try:
            args = command.get("text", "").strip().split()
            print(f"[DEBUG] Received /analyze-log args: {args}", flush=True)

            if len(args) != 3:
                client.chat_postMessage(
                    channel=command["channel_id"],
                    text="Usage: `/analyze-log <hostname> <config_dir> <task_dir>`"
                )
                return

            hostname, config_dir, task_dir = args
            channel_id = command["channel_id"]

            print(f"[DEBUG] Background thread started for {hostname}", flush=True)
            analyze_log_entry(config_dir, task_dir, hostname, channel_id)
            print(f"[DEBUG] Analysis complete for {hostname}", flush=True)

        except Exception as thread_err:
            print(f"[ERROR] Exception in background thread: {thread_err}", flush=True)
            client.chat_postMessage(
                channel=command["channel_id"],
                text=f":x: Analysis failed for `{hostname}`. Error: {thread_err}"
            )

    threading.Thread(target=run_analysis).start()


if __name__ == "__main__":
    print("[DEBUG] Agent-C is running...", flush=True)
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
