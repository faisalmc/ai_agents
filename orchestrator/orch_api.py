# orchestrator/orch_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

# We’ll reuse Slack client that slack_bolt already uses via the App
from slack_bolt import App
from slack_sdk import WebClient

# Import the existing Slack app instance so we can reuse its token/client
from slack_bot import app as slack_app

app = FastAPI(title="Orchestrator Callback API", version="0.1.0")

# Reuse the WebClient the same way Slack Bolt does (same bot token)
slack_client: WebClient = slack_app.client 

class Agent8AnalysisPayload(BaseModel):
    channel: str
    thread_ts: str
    session_id: str
    host: str
    command: str
    preview: Optional[str] = None
    analysis_pass1: Optional[str] = None
    analysis_pass2: Optional[str] = None
    direction: Optional[str] = None
    trusted_commands: Optional[List[str]] = None
    unvalidated_commands: Optional[List[str]] = None

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
        parts.append(f"*🟢 Pass-1 (single-command):*\n{body.analysis_pass1}")
    if body.analysis_pass2:
        parts.append(f"*🔵 Pass-2 (with history):*\n{body.analysis_pass2}")
    if body.direction:
        parts.append(f"*Direction:* {body.direction}")
    if body.trusted_commands:
        parts.append("*Trusted commands:* " + ", ".join(f"`{c}`" for c in body.trusted_commands))
    if body.unvalidated_commands:
        parts.append("*Unvalidated commands:* " + ", ".join(f"`{c}`" for c in body.unvalidated_commands))

    text = "\n\n".join(parts) if parts else f"Analysis for `{body.command}` on `{body.host}`"

    try:
            slack_client.chat_postMessage(
                channel=body.channel,
                thread_ts=body.thread_ts,
                text=text,  # still keep plain text for fallback -- adding blocks for Escalate & Close
                blocks=[
                    {"type": "section", "text": {"type": "mrkdwn", "text": text}},
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "📧 Escalate"},
                                "style": "primary",
                                "value": f"escalate|{body.session_id}|{body.host}|{body.command}",
                                "action_id": "escalate_action",
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "✔ Close issue"},
                                "style": "danger",
                                "value": f"close|{body.session_id}|{body.host}",
                                "action_id": "close_action",
                            },
                        ],
                    },
                ],
            )
            return {"ok": True}
        # slack_client.chat_postMessage(channel=body.channel, thread_ts=body.thread_ts, text=text)
        # return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Slack post failed: {e}")