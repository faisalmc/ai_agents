# agents/agent-router/llm_clients/agent5_http.py
# FastAPI shim for Agent-5 (operational analyze)
# Exposes POST /operational-analyze and delegates to the existing Slack handler.

import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import the existing Slack command handler (no duplication of logic)
from agent5_operational_analyze import handle_operational_analyze

app = FastAPI(title="Agent-5 HTTP API", version="1.0.0")


class OperAnalyzeReq(BaseModel):
    config_dir: str
    task_id: str
    channel: str                  # Slack channel ID to post results into
    thread_ts: str | None = None
    requested_by: str | None = None


@app.post("/operational-analyze")
def operational_analyze(req: OperAnalyzeReq):
    """
    Fire-and-return endpoint: invoke the existing Slack command handler directly.
    """
    def _runner():
        try:
            # minimal Slack-like call context
            ack = (lambda *_, **__: None)
            respond = (lambda *_, **__: None)

            class _NoopLogger:
                def info(self, *args, **kwargs): pass
                def error(self, *args, **kwargs): pass

            command = {
                "text": f"{req.config_dir} {req.task_id}",
                "channel_id": req.channel,
                "user_id": req.requested_by or "",
                "thread_ts": req.thread_ts or "",
            }

            # Call the existing Bolt handler
            handle_operational_analyze(ack, command, respond, _NoopLogger())

        except Exception as e:
            print(f"[agent-5:/operational-analyze] ERROR: {e}", flush=True)

    try:
        threading.Thread(target=_runner, daemon=True).start()
        return {"status": "accepted"}
    except Exception as e:
        print(f"[agent-5:/operational-analyze] FAILED to start thread: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))

# # agents/agent-router/llm_clients/agent5_http.py
# # FastAPI shim for Agent-5 (operational analyze)
# # Exposes POST /operational-analyze and calls existing agent5_operational_analyze helpers

# import threading
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# # Import existing function(s). These should already perform the Slack posting, JSON writes, etc.
# # IMPORTANT: We assume agent5_operational_analyze.py exposes run_operational_analyze(config_dir, task_dir, channel)
# from agent5_operational_analyze import handle_operational_analyze

# app = FastAPI(title="Agent-5 HTTP API", version="1.0.0")


# class OperAnalyzeReq(BaseModel):
#     config_dir: str
#     task_id: str
#     channel: str                  # Slack channel ID to post results into
#     thread_ts: str | None = None  # passthrough (not used by the legacy function if absent)
#     requested_by: str | None = None


# @app.post("/operational-analyze")
# def operational_analyze(req: OperAnalyzeReq):
#     """
#     Fire-and-return endpoint: call the existing Agent-5 analyze flow and let it post to Slack.
#     Mirrors Agent-4's shim style and behavior.
#     """
#     def _runner():
#         try:
#             # Delegate to existing Agent-5 function (no duplication of logic here)
#             handle_operational_analyze(_noop_ack, command, _noop_respond, _NoopLogger())
#         except Exception as e:
#             print(f"[agent-5:/operational-analyze] ERROR: {e}", flush=True)

#     try:
#         threading.Thread(target=_runner, daemon=True).start()
#         return {"status": "accepted"}
#     except Exception as e:
#         print(f"[agent-5:/operational-analyze] FAILED to start thread: {e}", flush=True)
#         raise HTTPException(status_code=500, detail=str(e))