# agents/agent-router/llm_clients/agent4_http.py
# FastAPI shim for Agent-4 (operational check)
# Exposes POST /operational-check and calls existing agent_d_operational_check helpers

import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import existing functions (these already post to Slack on success)
from agent_d_operational_check import run_show_capture, post_operational_summary

import os
import subprocess
import requests

AGENT_8_URL = os.getenv("AGENT_8_URL", "").rstrip("/")

app = FastAPI(title="Agent-4 HTTP API", version="1.0.0")


class OperCheckReq(BaseModel):
    config_dir: str
    task_id: str
    channel: str                 # Slack channel ID to post results into
    thread_ts: str | None = None
    requested_by: str | None = None

class CaptureOnlyReq(BaseModel):
    config_dir: str
    task_id: str
    overlay_ini_relpath: str | None = None   # e.g., "show_cmds.agent7.ini" relative to the task folder
    out_subdir: str = "agent8"
    devices: list[str] | None = None
    no_grading_logs: bool = True

@app.post("/operational-check")
def operational_check(req: OperCheckReq):
    """
    Fire-and-return endpoint: run capture then post summary via existing functions
    (mirrors Agent-3 style).
    """
    def _runner():
        try:
            # 1) run capture
            ok = run_show_capture(req.config_dir, req.task_id)
            # 2) on success, post the summary to Slack (existing function)
            if ok:
                post_operational_summary(req.task_id, req.config_dir, req.channel)
        except Exception as e:
            print(f"[agent-4:/operational-check] ERROR: {e}", flush=True)

    try:
        threading.Thread(target=_runner, daemon=True).start()
        return {"status": "accepted"}
    except Exception as e:
        print(f"[agent-4:/operational-check] FAILED to start thread: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/capture-only")
def capture_only(req: CaptureOnlyReq):
    """
    Fire-and-return endpoint that only runs the capture script with optional overlay INI
    and writes outputs under <task>/<out_subdir>/{show_logs, grading_logs}.
    It does NOT post to Slack (Agent-8 handle analysis + Slack).
    """
    def _runner():
        repo_root = os.getenv("REPO_ROOT", "/app/doo").rstrip("/")
        script_path = os.path.join(repo_root, req.config_dir, "run_show_commands.py")
        status = "done"
        error_msg = None

        try:
            if not os.path.isfile(script_path):
                raise FileNotFoundError(f"run_show_commands.py not found at {script_path}")

            cmd = ["python3", script_path, "--task", req.task_id, "--out-subdir", req.out_subdir]
            if req.overlay_ini_relpath:
                cmd += ["--ini", req.overlay_ini_relpath]
            if req.no_grading_logs:
                cmd += ["--no-grading-logs"]
            if req.devices:
                cmd += ["--devices", *req.devices]

            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            print(f"[agent-4:/capture-only] OK\n{out}", flush=True)

        except subprocess.CalledProcessError as e:
            status = "error"
            error_msg = f"capture failed: {e.output}"
            print(f"[agent-4:/capture-only] ERROR running capture: {e.output}", flush=True)
        except Exception as e:
            status = "error"
            error_msg = str(e)
            print(f"[agent-4:/capture-only] ERROR: {e}", flush=True)

        # -------- HTTP callback to Agent-8 --------
        try:
            payload = {
                "config_dir": req.config_dir,
                "task_id": req.task_id,
                "devices": req.devices,
                "out_subdir": req.out_subdir,
                "status": status,
            }
            if error_msg:
                payload["error"] = error_msg

            if AGENT_8_URL:
                requests.post(f"{AGENT_8_URL}/capture-done", json=payload, timeout=30)
                print(f"[agent-4:/capture-only] Callback sent to Agent-8 {AGENT_8_URL}/capture-done", flush=True)
            else:
                print("[agent-4:/capture-only] WARN: AGENT_8_URL not set, skipping callback", flush=True)

        except Exception as e:
            print(f"[agent-4:/capture-only] WARN could not notify agent-8: {e}", flush=True)

    try:
        threading.Thread(target=_runner, daemon=True).start()
        return {"status": "accepted"}
    except Exception as e:
        print(f"[agent-4:/capture-only] FAILED to start thread: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))