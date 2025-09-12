# agent5_reasoner.py
import os, json
from typing import Dict, Any
from agent5_shared import dbg, write_audit, safe_json_loads, normalize_platform, sanitize_show

REASONER_SYSTEM = """You are a senior Cisco SP NOC engineer.
Inputs (from the user message):
  - 'context' → distilled fields (hostname, platform_hint, signals_seen)
  - 'trusted_show_only' → vetted read-only show commands (use these first)
  - 'candidate_show_ideas' → lower-confidence ideas (use only if trusted is insufficient)
  - optional 'intent' from Agent-1 (expected design at a high level)

Tasks:
  1) Determine device status: healthy | degraded | error | unknown
  2) Build findings array: [{signal, severity, detail, evidence?}]
  3) Recommend SAFE read-only show commands (no config/clear/debug). Prefer commands in 'trusted_show_only'.
     If you must include any from 'candidate_show_ideas', keep them minimal.
  4) Optionally suggest active probes (ping/traceroute) if helpful.

Platform handling:
  - Platform values are 'cisco-ios-xr' | 'cisco-ios' | 'unknown'. Do not mix syntaxes.
  - If platform is XR, avoid IOS-style pipes in recommendations.

Return ONLY JSON:
{
  "hostname": "<str>",
  "platform": "cisco-ios-xr" | "cisco-ios" | "unknown",
  "signals_seen": [...],
  "status": "healthy|degraded|error|unknown",
  "findings": [ {"signal":"bgp","severity":"error|warn|info","detail":"...","evidence":"<line>?"} ],
  "trusted_commands": ["show ..."],         # use these first (observed/.ini only)
  "unvalidated_cmds": ["show ..."],         # ideas only (DO NOT run unless promoted later)
  "optional_active_cmds": ["ping ...","traceroute ..."]
}
Be conservative; if in doubt, mark 'info' with explanation. Use evidence lines where possible.
"""

def build_reasoner_messages(hostname: str, facts: Dict[str, Any], agent1_for_host: Dict[str, Any] | None):
    # Distill what the model needs, rather than dumping the entire facts object
    context = {
        "hostname": hostname,
        "platform_hint": facts.get("platform_hint", "unknown"),
        "signals_seen": facts.get("signals_seen", []),
    }
    trusted_show_only = facts.get("trusted_all", [])          # vetted (.ini observed only in Phase-1)
    candidate_show_ideas = facts.get("candidates_all", [])    # ideas only (agent1 candidates + lexicon ideas)

    payload = {
        "context": context,
        "trusted_show_only": trusted_show_only,
        "candidate_show_ideas": candidate_show_ideas,
        "intent": agent1_for_host or {}
    }

    user = "### Device context\n```json\n" + json.dumps(payload, indent=2) + "\n```"
    return [
        {"role": "system", "content": REASONER_SYSTEM},
        {"role": "user", "content": user}
    ]


def reason_per_device(hostname: str, facts: Dict[str, Any], agent1_for_host: Dict[str, Any] | None,
                      call_llm_fn, audit_dir: str) -> Dict[str, Any]:
    msgs = build_reasoner_messages(hostname, facts, agent1_for_host)
    write_audit(os.path.join(audit_dir, f"{hostname}__reasoner_prompt.txt"), json.dumps(msgs, indent=2))
    raw = call_llm_fn(msgs, temperature=0.0) or ""
    write_audit(os.path.join(audit_dir, f"{hostname}__reasoner_raw.json"), raw)

    parsed = safe_json_loads(raw) or {}

    # Normalize platform using the Phase-1 hint (don’t let the model flip it)
    plat = normalize_platform(facts.get("platform_hint", "unknown"))
    parsed["platform"] = plat

    # Sanitize & hard-gate recommended_show_cmds to trusted only in Phase-1
    trusted = set(facts.get("trusted_all", []) or [])
    recs = parsed.get("recommended_show_cmds") or []
    clean_recs = []
    for c in recs:
        sc = sanitize_show(c, plat)
        if sc and ((not trusted) or (sc in trusted)):
            clean_recs.append(sc)

    # If model didn’t include enough, top up from trusted list (still sanitized)
    if trusted and len(clean_recs) < min(3, len(trusted)):
        for t in facts.get("trusted_all", []):
            sc = sanitize_show(t, plat)
            if sc and sc not in clean_recs:
                clean_recs.append(sc)
            if len(clean_recs) >= 5:
                break

    # Dedup while preserving order
    seen = set()
    clean_recs = [c for c in clean_recs if not (c in seen or seen.add(c))]

    # CHANGE 1: cap max number of shows
    MAX_TRUSTED = 8
    clean_recs = clean_recs[:MAX_TRUSTED]

    # NEW: expose Phase-1 names explicitly
    parsed["trusted_commands"] = clean_recs

    # Also surface unvalidated ideas (sanitized, not run). Do not include anything in trusted.
    MAX_UNVALIDATED = 6
    plat = parsed.get("platform", "unknown")
    cands = facts.get("candidates_all", []) or []
    seen_cmds = set(clean_recs)
    unval = []
    for c in cands:
        sc = sanitize_show(c, plat)
        if sc and sc not in seen_cmds:
            unval.append(sc)
            if len(unval) >= MAX_UNVALIDATED:
                break
    parsed["unvalidated_cmds"] = unval

    # Keep legacy key for downstream code that still expects it
    parsed["recommended_show_cmds"] = clean_recs

    # CHANGE 2: filter optional_active_cmds
    acts = parsed.get("optional_active_cmds") or []
    parsed["optional_active_cmds"] = [
        a for a in acts if isinstance(a, str) and a.strip().lower().startswith(("ping", "traceroute"))
    ]

    # Ensure required keys exist to avoid downstream KeyErrors
    parsed.setdefault("hostname", hostname)
    parsed.setdefault("signals_seen", facts.get("signals_seen", []))
    parsed.setdefault("status", "unknown")
    parsed.setdefault("findings", [])

    return parsed if isinstance(parsed, dict) else {
        "hostname": hostname,
        "platform": plat,
        "signals_seen": facts.get("signals_seen", []),
        "status": "unknown",
        "findings": [{"signal":"meta","severity":"info","detail":"LLM response not strictly JSON"}],
        "recommended_show_cmds": clean_recs,
        "optional_active_cmds": []
    }

