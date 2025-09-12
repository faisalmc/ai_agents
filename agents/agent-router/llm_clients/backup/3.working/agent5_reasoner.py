# agent5_reasoner.py
import os, json
from typing import Dict, Any
from agent5_shared import dbg, write_audit, safe_json_loads

REASONER_SYSTEM = """You are a senior Cisco SP NOC engineer.
Input:
  - 'facts' (structured evidence with verbatim lines)
  - optional 'intent' from Agent-1 (expected design)
Task:
  - Determine device status: healthy | degraded | error | unknown
  - Build findings array: [{signal, severity, detail, evidence?}]
  - Suggest SAFE read-only show commands (no config/clear/debug)
  - Suggest OPTIONAL active probes (ping/traceroute) if helpful
Return ONLY JSON:
{
  "hostname": "<str>",
  "platform": "ios-xr" | "ios" | "unknown",
  "signals_seen": [...],
  "status": "healthy|degraded|error|unknown",
  "findings": [ {"signal":"bgp","severity":"error|warn|info","detail":"...","evidence":"<line>?"} ],
  "recommended_show_cmds": ["show ..."],
  "optional_active_cmds": ["ping ...","traceroute ..."]
}
Be conservative; if in doubt, mark info with explanation. Use evidence lines where possible.
"""

def build_reasoner_messages(hostname: str, facts: Dict[str, Any], agent1_for_host: Dict[str, Any] | None):
    payload = {
        "hostname": hostname,
        "facts": facts,
        "intent": agent1_for_host or {}
    }
    user = "### Reason over this device context\n```json\n" + json.dumps(payload, indent=2) + "\n```"
    return [{"role": "system", "content": REASONER_SYSTEM},
            {"role": "user", "content": user}]

def reason_per_device(hostname: str, facts: Dict[str, Any], agent1_for_host: Dict[str, Any] | None,
                      call_llm_fn, audit_dir: str) -> Dict[str, Any]:
    msgs = build_reasoner_messages(hostname, facts, agent1_for_host)
    write_audit(os.path.join(audit_dir, f"{hostname}__reasoner_prompt.txt"), json.dumps(msgs, indent=2))
    raw = call_llm_fn(msgs, temperature=0.0) or ""
    write_audit(os.path.join(audit_dir, f"{hostname}__reasoner_raw.json"), raw)
    parsed = safe_json_loads(raw)
    if isinstance(parsed, dict):
        return parsed
    # fallback minimal object
    return {
        "hostname": hostname,
        "platform": facts.get("platform_guess", "unknown"),
        "signals_seen": facts.get("signals_seen", []),
        "status": "unknown",
        "findings": [{"signal":"meta","severity":"info","detail":"LLM response not strictly JSON"}],
        "recommended_show_cmds": [],
        "optional_active_cmds": []
    }
