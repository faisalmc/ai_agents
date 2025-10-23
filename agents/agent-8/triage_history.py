# agents/agent-8/triage_history.py
# This file manages the triage history during a troubleshooting session.
# Each triage step (what command was run, what the analysis said, etc.)
# is written to a JSONL (JSON per line) file.
# Solved cases can be written to a separate file.
# This helps build memory of what happened in each triage session.

import os
import json
from datetime import datetime

# Base directory for history files (shared across all agents)
DEFAULT_DIR = "/app/shared/_agent_knowledge/triage_history"

def _ensure_dir(path: str) -> None:
    """Make sure the folder exists (treat path as a directory)."""
    os.makedirs(path, exist_ok=True)


def append_step(session_id: str, host: str, cmds: list,
                analysis: str, direction: str,
                trusted: list, unvalidated: list,
                base_dir: str = DEFAULT_DIR) -> None:
    """
    Save one step of the triage into a JSONL file.

    Example of one step:
    {
      "ts": "2025-09-20T12:30:00",
      "host": "B-ASBR-1",
      "commands": ["show ip bgp summary"],
      "analysis": "BGP neighbors are down",
      "direction": "Check interface states",
      "trusted": ["show interfaces"],
      "unvalidated": ["show logging"]
    }
    """
    _ensure_dir(base_dir)
    record = {
        "ts": datetime.utcnow().isoformat(),
        "host": host,
        "commands": cmds,
        "analysis": analysis,
        "direction": direction,
        "trusted": trusted,
        "unvalidated": unvalidated,
    }
    path = os.path.join(base_dir, f"{session_id}.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def append_solved_case(session_id: str, summary: dict,
                       base_dir: str = DEFAULT_DIR) -> None:
    """
    Mark a session as solved.
    Writes a short summary of the session to solved_cases.jsonl.

    Example summary:
    {
      "session_id": "abc12345",
      "ts": "2025-09-20T12:45:00",
      "host": "B-ASBR-1",
      "root_cause": "Interface down",
      "resolution": "Interface was re-enabled"
    }
    """
    _ensure_dir(base_dir)
    summary["session_id"] = session_id
    summary["ts"] = datetime.utcnow().isoformat()
    path = os.path.join(base_dir, "solved_cases.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(summary) + "\n")


def collect_recent_steps(session_id: str, limit: int = 5,
                         base_dir: str = DEFAULT_DIR) -> list:
    """
    Read back the last N steps of a session.
    Used when we want to escalate to L3 or review what happened.

    Returns a list of dicts (each step).
    """
    path = os.path.join(base_dir, f"{session_id}.jsonl")
    if not os.path.exists(path):
        return []

    steps = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                steps.append(json.loads(line))
            except Exception:
                continue

    return steps[-limit:]


# --- Debug logging helpers (safe, optional) ---
def _ensure_dir_for_file(file_path: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def debug_write_text(session_id: str, filename: str, content: str,
                     base_dir: str = DEFAULT_DIR) -> None:
    """
    Writes a text blob for debugging under:
      <DEFAULT_DIR>/debug/<session_id>/<filename>
    """
    debug_dir = os.path.join(base_dir, "debug", session_id)
    os.makedirs(debug_dir, exist_ok=True)
    path = os.path.join(debug_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def debug_write_json(session_id: str, filename: str, obj: dict,
                     base_dir: str = DEFAULT_DIR) -> None:
    from json import dumps
    debug_write_text(session_id, filename, dumps(obj, indent=2), base_dir)