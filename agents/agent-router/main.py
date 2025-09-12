import os
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import hmac, hashlib
from git import Repo
import openai
from slack_sdk import WebClient

app = FastAPI()

# Load env vars
GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_DIR = os.getenv("REPO_CLONE_DIR", "/opt/tasks")

openai.api_key = OPENAI_API_KEY
slack = WebClient(token=SLACK_TOKEN)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    # 1) Validate signature
    body = await request.body()
    mac = hmac.new(GITHUB_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
    if not hmac.compare_digest(f"sha256={mac.hexdigest()}", x_hub_signature_256):
        raise HTTPException(401, "Invalid signature")

    payload = await request.json()
    # 2) Detect changes in tasks/
    changed = []
    for c in payload.get('commits', []):
        changed += [f for f in c.get('added', []) + c.get('modified', []) if f.startswith('tasks/')]
    if not changed:
        return JSONResponse({"msg": "no relevant changes"})

    # 3) Clone or pull repo
    if not os.path.isdir(REPO_DIR):
        Repo.clone_from(payload['repository']['clone_url'], REPO_DIR)
    else:
        Repo(REPO_DIR).git.pull()

    # 4) Parse files and call LLM (omitted for brevity)
    summary = "<LLM-generated summary goes here>"

    # 5) Post to Slack
    slack.chat_postMessage(
        channel="#network-ops",
        text=f":robot_face: *New Task Briefing*\n{summary}",
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": summary}},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": " Approve & Push"}, "action_id": "approve_push"},
                {"type": "button", "text": {"type": "plain_text", "text": " Abort"}, "action_id": "abort_task"}
            ]}
        ]
    )

    return JSONResponse({"msg": "summary posted"})

