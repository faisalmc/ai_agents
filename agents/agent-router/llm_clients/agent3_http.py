# agents/agent-router/llm_clients/agent_3_http.py
# FastAPI shim for Agent-3 (per-host analysis)
# Exposes POST /analyze-host and calls existing agent_c_analyze_log.analyze_log_entry

import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import the existing analyzer (does LLM + Slack posting)
# from agent_c_analyze_log import analyze_log_entry
from agent_c_analyze_log import analyze_log_entry, analyze_log_core, save_agent3_json
# ADD:
import os
import json

app = FastAPI(title="Agent-3 HTTP API", version="1.0.0")


class AnalyzeHostReq(BaseModel):
    config_dir: str
    task_id: str
    hostname: str
    channel: str                 # Slack channel ID to post results into
    thread_ts: str | None = None # Currently unused by agent_c_analyze_log.py
    requested_by: str | None = None

# ADD: JSON-returning endpoint schema (no Slack args)
class AnalyzeHostJSONReq(BaseModel):
    config_dir: str
    task_id: str
    hostname: str

@app.post("/analyze-host")
def analyze_host(req: AnalyzeHostReq):
    """
    Fire-and-return endpoint: start analysis in a background thread,
    immediately return {"status":"accepted"} (mirrors Agent-2 style).
    """

    def _runner():
        try:
            # Existing signature: analyze_log_entry(task_path, task_name, hostname, channel_id)
            analyze_log_entry(req.config_dir, req.task_id, req.hostname, req.channel)
        except Exception as e:
            print(f"[agent-3:/analyze-host] ERROR: {e}", flush=True)

    try:
        threading.Thread(target=_runner, daemon=True).start()
        return {"status": "accepted"}
    except Exception as e:
        print(f"[agent-3:/analyze-host] FAILED to start thread: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


# ADD: synchronous JSON-returning endpoint
@app.post("/analyze-host-json")
def analyze_host_json(req: AnalyzeHostJSONReq):
    """
    Synchronous per-host analysis:
    - Reads log
    - Runs LLM
    - Saves /app/doo/<config_dir>/<task_id>/agent3_<HOST>-analysis.json
    - Returns the JSON body
    """
    try:
        summary = analyze_log_core(req.config_dir, req.task_id, req.hostname)
        # persist with agreed name
        save_agent3_json(req.config_dir, req.task_id, req.hostname, summary)
        return summary
    except Exception as e:
        print(f"[agent-3:/analyze-host-json] ERROR: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))
    