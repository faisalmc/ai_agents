# agent5_correlator.py
import os, json
from agent5_shared import dbg, write_audit, safe_json_loads

CORR_SYSTEM = """You are a network service lead.
Input: per-device analyses (status+findings).
Task: correlate incidents across devices, summarize themes, propose safe follow-up shows and optional probes.
Return ONLY:
{
  "task_status": "healthy" | "mixed" | "degraded" | "error" | "unknown",
  "top_incidents": [ {"scope":"pair|site|global","summary":"...","impact":"...","devices":["..."]} ],
  "remediation_themes": [ "..." ],
  "safe_followup_show_cmds": [ "show ..." ],
  "optional_active_probes": [ "ping ...","traceroute ..." ]
}
Be conservative and reference patterns evident in inputs. No config commands, no historical leakage.
"""

def build_corr_messages(per_device_objs: list[dict]):
    user = "### Correlate this array\n```json\n" + json.dumps(per_device_objs, indent=2) + "\n```"
    return [{"role":"system","content":CORR_SYSTEM},
            {"role":"user","content":user}]

def correlate(per_device_objs: list[dict], call_llm_fn, audit_dir: str) -> dict:
    msgs = build_corr_messages(per_device_objs)
    write_audit(os.path.join(audit_dir, "_correlator_prompt.txt"), json.dumps(msgs, indent=2))
    raw = call_llm_fn(msgs, temperature=0.0) or ""
    write_audit(os.path.join(audit_dir, "_correlator_raw.json"), raw)
    parsed = safe_json_loads(raw)
    if isinstance(parsed, dict):
        return parsed
    return {
        "task_status":"unknown",
        "top_incidents":[],
        "remediation_themes":[],
        "safe_followup_show_cmds":[],
        "optional_active_probes":[]
    }
