# orchestrator/run_orchestrator.py
import threading
import uvicorn
import os

# Import your Slack app (the same file you run today)
from slack_bot import app as slack_app
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Import the FastAPI app that will receive callbacks
from orch_api import app as http_app  # you'll create orch_api.py below

def start_slack():
    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

def start_http():
    uvicorn.run(http_app, host="0.0.0.0", port=int(os.getenv("ORCH_HTTP_PORT","8099")), log_level="info")

if __name__ == "__main__":
    # Run Slack in a background thread
    t = threading.Thread(target=start_slack, daemon=True)
    t.start()

    # Run FastAPI in the main thread
    start_http()