"""
agents/agent-interactive/incident_triage_history.py
----------------------------------------------------
Phase-2 adaptation of Agent-8's triage_history.py.

Purpose:
- Keep a persistent JSONL record of each triage/analysis step
- Write solved-case summaries for successful resolutions
- Maintain debug text/json under /app/shared/_incident_knowledge/triage_history/debug

All writes are isolated to /app/shared/_incident_knowledge/
so Agent-Interactive never overlaps with Agent-8's _agent_knowledge.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

# --------------------------------------------------------------------
# Step 1: Define base directory for Phase-2 triage history
# --------------------------------------------------------------------
DEFAULT_DIR = "/app/shared/_incident_knowledge/triage_history"


# --------------------------------------------------------------------
# Step 2: Ensure directory utilities
# --------------------------------------------------------------------
def _ensure_dir(path: str) -> None:
    """Make sure the folder exists (treat path as a directory)."""
    os.makedirs(path, exist_ok=True)


# --------------------------------------------------------------------
# Step 3: Append one triage step
# --------------------------------------------------------------------
def append_step(incident_id: str, host: str, cmds: List[str],
                analysis: str, direction: str,
                trusted: List[str], unvalidated: List[str],
                base_dir: str = DEFAULT_DIR) -> None:
    """
    Save one step of the triage into a JSONL (JSON per line) file.

    Example:
    {
      "ts": "2025-10-29T12:30:00",
      "host": "A-PE-1",
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
    path = os.path.join(base_dir, f"{incident_id}.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


# --------------------------------------------------------------------
# Step 4: Append a solved-case summary
# --------------------------------------------------------------------
def append_solved_case(incident_id: str, summary: Dict[str, Any],
                       base_dir: str = DEFAULT_DIR) -> None:
    """
    Mark an incident as solved.
    Writes a short summary into /app/shared/_incident_knowledge/solved_cases.jsonl.

    Example:
    {
      "incident_id": "evt-84432ef3",
      "ts": "2025-10-29T12:45:00",
      "host": "A-PE-1",
      "root_cause": "Interface down",
      "resolution": "Interface was re-enabled"
    }
    """
    _ensure_dir(base_dir)
    summary["incident_id"] = incident_id
    summary["ts"] = datetime.utcnow().isoformat()
    solved_path = "/app/shared/_incident_knowledge/solved_cases.jsonl"
    os.makedirs(os.path.dirname(solved_path), exist_ok=True)
    with open(solved_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(summary) + "\n")


# --------------------------------------------------------------------
# Step 5: Retrieve recent triage steps
# --------------------------------------------------------------------
def collect_recent_steps(incident_id: str, limit: int = 5,
                         base_dir: str = DEFAULT_DIR) -> List[Dict[str, Any]]:
    """
    Read back the last N steps of an incident.
    Used for context in LLM analysis or escalation review.
    """
    path = os.path.join(base_dir, f"{incident_id}.jsonl")
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


# --------------------------------------------------------------------
# Step 6: Debug logging utilities (optional)
# --------------------------------------------------------------------
def debug_write_text(incident_id: str, filename: str, content: str,
                     base_dir: str = DEFAULT_DIR) -> None:
    """
    Writes a plain text file for debugging under:
      /app/shared/_incident_knowledge/triage_history/debug/<incident_id>/<filename>
    """
    debug_dir = os.path.join(base_dir, "debug", incident_id)
    os.makedirs(debug_dir, exist_ok=True)
    path = os.path.join(debug_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def debug_write_json(incident_id: str, filename: str, obj: Dict[str, Any],
                     base_dir: str = DEFAULT_DIR) -> None:
    """
    Writes a JSON object for debugging under:
      /app/shared/_incident_knowledge/triage_history/debug/<incident_id>/<filename>
    """
    from json import dumps
    debug_write_text(incident_id, filename, dumps(obj, indent=2), base_dir)
