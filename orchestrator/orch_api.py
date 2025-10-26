# orchestrator/orch_api.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import os, json

# We’ll reuse Slack client that slack_bolt already uses via the App
from slack_bolt import App
from slack_sdk import WebClient

# Import the existing Slack app instance so we can reuse its token/client
from slack_bot import app as slack_app, build_triage_suggestion_blocks

app = FastAPI(title="Orchestrator Callback API", version="0.1.0")

# Reuse the WebClient the same way Slack Bolt does (same bot token)
slack_client: WebClient = slack_app.client 

class Agent8AnalysisPayload(BaseModel):
    channel: str
    thread_ts: str
    session_id: str
    host: str
    command: str
    config_dir: Optional[str] = None
    task_id: Optional[str] = None
    preview: Optional[str] = None
    analysis_pass1: Optional[str] = None
    analysis_pass2: Optional[str] = None
    direction: Optional[str] = None
    trusted_commands: Optional[List[str]] = None
    unvalidated_commands: Optional[List[str]] = None
    promoted: Optional[List[str]] = None   # <<< ADDED for trusted commands

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/agent8/callback")
def agent8_callback(body: Agent8AnalysisPayload):
    # composing the same message format that was already used in slack_bot.py
    parts = []
    if body.preview:
        parts.append(f"*📄 Output for `{body.command}` on `{body.host}`:*\n```{body.preview}```")
    if body.analysis_pass1:
        parts.append(f"*🔍 Analysis-1 (single-command):*\n{body.analysis_pass1}") # Pass-1
    if body.analysis_pass2:
        parts.append(f"*🔍 Analysis-2 (with history):*\n{body.analysis_pass2}") # Pass-2
    if body.direction:
        parts.append(f"*Direction:* {body.direction}")
    # if body.trusted_commands:
    #     parts.append("*Trusted commands:* " + ", ".join(f"`{c}`" for c in body.trusted_commands))
    # if body.unvalidated_commands:
    #     parts.append("*Unvalidated commands:* " + ", ".join(f"`{c}`" for c in body.unvalidated_commands))
    if hasattr(body, "promoted") and body.promoted:   # <<< added to indicate prompoted cmds
        parts.append("*Promoted to trusted (just ran ok):* " + ", ".join(f"`{c}`" for c in body.promoted))

    text = "\n\n".join(parts) if parts else f"Analysis for `{body.command}` on `{body.host}`"

    # Single JSON blob we’ll hand to Slack actions (Escalate / Close)
    btn_value = json.dumps({
        "config_dir": body.config_dir or "",
        "task_dir": body.task_id or "",
        "host": body.host or "",
        "session_id": body.session_id or "",
        "channel": body.channel,
        "thread_ts": body.thread_ts,
    })

    try:
        # Base section for analysis text
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ]

        # --- NEW: add quick-run suggestion buttons if Agent-8 proposed commands ---
        cmds = []
        if body.trusted_commands:
            cmds += [{"command": c, "trust_hint": "high"} for c in body.trusted_commands]
        if body.unvalidated_commands:
            cmds += [{"command": c, "trust_hint": "low"} for c in body.unvalidated_commands]

        if cmds:
            triage_blocks = build_triage_suggestion_blocks(
                guidance="Follow-up commands suggested by Agent-8:",
                cmds=cmds,
                bot_name="agent"
            )
            blocks.extend(triage_blocks)

        # --- Always include Escalate / Close buttons at bottom ---
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "📧 Escalate"},
                    "style": "primary",
                    "value": btn_value,
                    "action_id": "agent8_escalate",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "✔ Close issue"},
                    "style": "danger",
                    "value": btn_value,
                    "action_id": "agent8_close_issue",
                },
            ],
        })

        slack_client.chat_postMessage(
            channel=body.channel,
            thread_ts=body.thread_ts,
            text=text,
            blocks=blocks,
        )
        return {"ok": True}

    # try:
    #     slack_client.chat_postMessage(
    #         channel=body.channel,
    #         thread_ts=body.thread_ts,
    #         text=text,  # fallback text
    #         blocks=[
    #             {"type": "section", "text": {"type": "mrkdwn", "text": text}},
    #             {
    #                 "type": "actions",
    #                 "elements": [
    #                     {
    #                         "type": "button",
    #                         "text": {"type": "plain_text", "text": "📧 Escalate"},
    #                         "style": "primary",
    #                         "value": btn_value,
    #                         "action_id": "agent8_escalate",
    #                     },
    #                     {
    #                         "type": "button",
    #                         "text": {"type": "plain_text", "text": "✔ Close issue"},
    #                         "style": "danger",
    #                         "value": btn_value,
    #                         "action_id": "agent8_close_issue",
    #                     },
    #                 ],
    #             },
    #         ],
    #     )
    #     return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Slack post failed: {e}")

# ------------------------------------------------------------------------ #
# ---- interactive-agent callback to orchestrator when Kafka msg comes ---- #
# NOTE: async =  this function may pause (await) while waiting for data or network operations
#                — don’t block other requests in the meantime.

@app.post("/events/update")
async def events_update(req: Request):
    """
    Callback endpoint for any agent (e.g., interactive-agent Phase 1)
    that wants to post a Slack message via the orchestrator.

    Expected JSON:
    {
        "type": "incident_normalized",
        "data": {
            "incident_id": "evt-xxxx",
            "family": "interface",
            "confidence": 0.87,
            "hostname": "A-PE-1",
            "severity": "major",
            "symptom": "Link Gi0/0/0/1 down, CRC errors detected",
            "timestamp": "2025-10-26T09:43Z"
        }
    }
    """
    body = await req.json()
    event_type = body.get("type")
    data = body.get("data", {})

    # --- Build enriched Slack message ---
    text = (
        f"*Incident Normalized*\n"
        f"• ID: `{data.get('incident_id')}`\n"
        f"• Family: `{data.get('family')}`\n"
        f"• Confidence: {data.get('confidence')}\n"
        f"• Hostname: `{data.get('hostname')}`\n"
        f"• Severity: `{data.get('severity')}`\n"
        f"• Symptom: {data.get('symptom')}\n"
        f"• Timestamp: {data.get('timestamp')}"
    )

    try:
        slack_client.chat_postMessage(
            channel=os.getenv("SLACK_DEFAULT_CHANNEL", "#ai-agents"),
            text=text,
            blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": text}}],
        )
        logger.info(f"Slack message posted for incident {data.get('incident_id')}")
    except Exception as exc:
        logger.warning(f"Slack post failed: {exc}")

    return {"ok": True}

