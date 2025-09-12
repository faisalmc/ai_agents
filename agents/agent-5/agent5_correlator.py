# agent5_correlator.py
import os, json
from agent5_shared import dbg, write_audit, safe_json_loads

CORR_SYSTEM = """You are a network service lead.
You will receive an array of per-device analyses produced by another agent. Each item typically contains:
  - hostname
  - platform
  - status
  - findings
  - trusted_commands         (per-device vetted shows; safe to subset)
  - unvalidated_cmds         (per-device ideas; DO NOT run unless promoted later)
  - optional_active_cmds     (ping/traceroute)

Strict rules:
- Do NOT invent device names. Only reference hostnames that appear in the input array.
- 'trusted_followup_cmds' must be a subset of the union of devices' trusted_commands.
- If you include 'unvalidated_followup_cmds', they must be a subset of the union of devices' unvalidated_cmds.
- Active probes must be limited to ping/traceroute (read-only impact). No config/clear/debug.
- Keep output concise and actionable.

Task:
- Correlate incidents across devices (patterns, shared symptoms).
- Summarize key themes and propose SAFE follow-up shows (subset of per-device trusted_commands).
- Optionally surface unvalidated follow-up ideas (subset of per-device unvalidated_cmds) for human review.
- Optionally propose active probes (ping/traceroute) that help disambiguate.

Return ONLY valid JSON:
{
  "task_status": "healthy" | "mixed" | "degraded" | "error" | "unknown",
  "top_incidents": [ {"scope":"pair|site|global","summary":"...","impact":"...","devices":["..."]} ],
  "remediation_themes": [ "..." ],
  "trusted_followup_cmds": [ "show ..." ],
  "unvalidated_followup_cmds": [ "show ..." ],
  "optional_active_probes": [ "ping ...","traceroute ..." ]
}
Be conservative and reference patterns evident in inputs. No config commands and no historical leakage.
"""

def build_corr_messages(per_device_objs: list[dict]):
    user = "### Correlate this array\n```json\n" + json.dumps(per_device_objs, indent=2) + "\n```"
    return [{"role":"system","content":CORR_SYSTEM},
            {"role":"user","content":user}]

def _worst_status(statuses: list[str]) -> str:
    # order from best to worst
    order = ["healthy", "mixed", "degraded", "error", "unknown"]
    # map for quick rank; unknown treated as worst unless nothing else present
    rank = {s:i for i,s in enumerate(order)}
    if not statuses:
        return "unknown"
    # if any 'error', return error; else degraded; else mixed; else healthy; else unknown
    # rely on rank min across mapped statuses (unseen -> unknown)
    best = None
    for s in statuses:
        s2 = s if s in rank else "unknown"
        if best is None or rank[s2] > rank[best]:
            best = s2
    return best or "unknown"

def correlate(per_device_objs: list[dict], call_llm_fn, audit_dir: str) -> dict:
    msgs = build_corr_messages(per_device_objs)
    write_audit(os.path.join(audit_dir, "_correlator_prompt.txt"), json.dumps(msgs, indent=2))
    raw = call_llm_fn(msgs, temperature=0.0) or ""
    write_audit(os.path.join(audit_dir, "_correlator_raw.json"), raw)
    parsed = safe_json_loads(raw)
    if not isinstance(parsed, dict):
        parsed = {}

    # --------- Post-parse safety & hygiene ---------
    known_devices = { (d.get("hostname") or "").strip() for d in per_device_objs if d.get("hostname") }

    # Build allowed sets (prefer new keys; fall back to legacy)
    allowed_trusted = set()
    allowed_unvalidated = set()
    for d in per_device_objs:
        # trusted per-device
        for c in (d.get("trusted_commands") or d.get("recommended_show_cmds") or []):
            if isinstance(c, str) and c.strip():
                allowed_trusted.add(c.strip())

        # unvalidated per-device (ideas)
        for c in (d.get("unvalidated_cmds") or []):
            if isinstance(c, str) and c.strip():
                allowed_unvalidated.add(c.strip())
                
    # 1) task_status: if missing or odd, derive a conservative one from device statuses
    if parsed.get("task_status") not in {"healthy","mixed","degraded","error","unknown"}:
        dev_statuses = [(d.get("status") or "unknown") for d in per_device_objs]
        parsed["task_status"] = _worst_status(dev_statuses)

    # 2) top_incidents: filter device names to known; drop empty device lists only if the incident listed non-empty devices
    clean_incidents = []
    for inc in (parsed.get("top_incidents") or []):
        if not isinstance(inc, dict):
            continue
        devs = inc.get("devices")
        if isinstance(devs, list):
            devs = [d for d in devs if isinstance(d, str) and d in known_devices]
            inc["devices"] = devs
        # normalize scope
        scope = (inc.get("scope") or "").lower()
        if scope not in {"pair","site","global"}:
            inc["scope"] = "global"  # default
        # keep if devices were not specified OR after filtering there are still devices
        if inc.get("devices") is None or inc["devices"]:
            clean_incidents.append(inc)
    parsed["top_incidents"] = clean_incidents

    # 3) remediation_themes: ensure list[str], dedup, cap
    themes = [t for t in (parsed.get("remediation_themes") or []) if isinstance(t, str) and t.strip()]
    seen = set()
    themes = [t for t in themes if not (t in seen or seen.add(t))]
    parsed["remediation_themes"] = themes[:8]

    # 4) trusted_followup_cmds: must be subset of allowed_trusted
    tshows = [s for s in (parsed.get("trusted_followup_cmds") or []) if isinstance(s, str) and s.strip()]
    tshows = [s for s in tshows if s in allowed_trusted]
    seen = set()
    tshows = [s for s in tshows if not (s in seen or seen.add(s))]
    parsed["trusted_followup_cmds"] = tshows[:10]

    # 4b) unvalidated_followup_cmds: must be subset of allowed_unvalidated, and not duplicate trusted
    ushows = [s for s in (parsed.get("unvalidated_followup_cmds") or []) if isinstance(s, str) and s.strip()]
    ushows = [s for s in ushows if s in allowed_unvalidated and s not in parsed["trusted_followup_cmds"]]
    seen = set()
    ushows = [s for s in ushows if not (s in seen or seen.add(s))]
    parsed["unvalidated_followup_cmds"] = ushows[:10]

    # 5) optional_active_probes: only ping/traceroute, dedup, cap
    probes = [p for p in (parsed.get("optional_active_probes") or []) if isinstance(p, str)]
    probes = [p.strip() for p in probes if p.strip().lower().startswith(("ping", "traceroute"))]
    seen = set()
    probes = [p for p in probes if not (p in seen or seen.add(p))]
    parsed["optional_active_probes"] = probes[:5]

    # 6) Final audit of cleaned output
    write_audit(os.path.join(audit_dir, "_correlator_clean.json"), json.dumps(parsed, indent=2))

    # Fallback if something still off
    if isinstance(parsed, dict):
        return parsed
    return {
    "task_status": "unknown",
    "top_incidents": [],
    "remediation_themes": [],
    "trusted_followup_cmds": [],
    "unvalidated_followup_cmds": [],
    "optional_active_probes": []
}