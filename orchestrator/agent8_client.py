# orchestrator/agent8_client.py
from __future__ import annotations
import os
import httpx
from typing import Any, Dict, List, Optional

AGENT_8_URL = os.getenv("AGENT_8_URL", "http://agent-8:8008")

def _post(path: str, payload: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
    url = f"{AGENT_8_URL}{path}"
    with httpx.Client(timeout=timeout) as cli:
        r = cli.post(url, json=payload)
    r.raise_for_status()
    return r.json() if r.content else {}

def start_triage(config_dir: str, task_dir: str, host: str,
                 channel: Optional[str] = None, thread_ts: Optional[str] = None,
                 user_id: Optional[str] = None) -> Dict[str, Any]:
    return _post("/triage/start", {
        "config_dir": config_dir,
        "task_dir": task_dir,
        "host": host,
        "channel": channel,
        "thread_ts": thread_ts,
        "user_id": user_id,
    })

def ingest(session_id: str, user_text: str) -> Dict[str, Any]:
    return _post("/triage/ingest", {
        "session_id": session_id,
        "user_text": user_text,
    })

def run_shows(session_id: str, host: str, commands: List[str]) -> Dict[str, Any]:
    return _post("/triage/run_shows", {
        "session_id": session_id,
        "host": host,
        "commands": commands,
    })

def reanalyze(session_id: str, host: str) -> Dict[str, Any]:
    return _post("/triage/reanalyze", {
        "session_id": session_id,
        "host": host,
    })

# --- agent-8 triage client --- #

def analyze_command(session_id: str, host: str, command: str) -> Dict[str, Any]:
    return _post("/triage/analyze_command", {
        "session_id": session_id,
        "host": host,
        "command": command,
        # "output": output,
    })

# --- NEW: save triage session to memory (Close Issue) --- #
def save_memory(session_id: str,
                root_cause_text: str = "",
                fix_steps_text: str = "",
                user_feedback: str = "") -> Dict[str, Any]:
    """
    Calls Agent-8 /memory/save to persist the triage session data
    into /app/shared/_agent_knowledge/triage_memory.jsonl

    The optional text fields can later be filled by user input (future UI).
    For now, they can be left blank.
    """
    payload = {
        "session_id": session_id,
        "root_cause_text": root_cause_text,
        "fix_steps_text": fix_steps_text,
        "user_feedback": user_feedback,
    }

    try:
        return _post("/memory/save", payload, timeout=30.0)
    except Exception as e:
        return {"ok": False, "error": f"Agent-8 /memory/save failed: {e}"}