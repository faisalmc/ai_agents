# agent5_facts.py
import os, re, json
from typing import Dict, Any
#from agent5_shared import dbg, write_audit, safe_json_loads
from agent5_shared import (
    dbg,
    write_audit,
    safe_json_loads,
    normalize_platform,
    sanitize_show,
    load_observed_commands,
    load_lexicon_candidates,
)
# Very light regex anchors (optional, extend over time)
_RE_BGP_NEI = re.compile(r"Neighbor\s+(\S+).*(Established|Idle|Active|Connect|OpenSent|OpenConfirm)", re.IGNORECASE)
_RE_PING = re.compile(r"Success rate is\s+(\d+)\s+percent", re.IGNORECASE)
_RE_XC_DOWN = re.compile(r"Group .*?, XC .*?, state is (down|up)", re.IGNORECASE)

FACTS_SYSTEM = """You extract structured, low-level FACTS from network CLI logs (IOS/IOS-XR).
Output ONLY JSON with this schema:
{
  "hostname": "<string>",
  "platform_guess": "ios-xr" | "ios" | "unknown",
  "signals_seen": ["bgp","evpn","isis","mpls","sr","l2vpn","intf","ip", ...],
  "facts": {
    "bgp_neighbors": [ {"peer":"<ip|id>","state":"Established|Idle|Active|...","evidence":"<verbatim line>"} ],
    "evpn_xconnects": [ {"name":"<xc>","state":"up|down|...","evidence":"<line>"} ],
    "lacp_bundles":   [ {"bundle":"BExx","state":"up|down|...","evidence":"<line>"} ],
    "reachability":   [ {"probe":"ping|traceroute","target":"<str>","result":"success|fail|mixed","success_rate":<0-100>,"evidence":"<line>"} ]
  }
}
Be conservative: only include items you can point to an evidence line for. Do NOT diagnose or recommend here.
"""

def _regex_prefill(md_text: str) -> Dict[str, Any]:
    facts = {
        "bgp_neighbors": [],
        "evpn_xconnects": [],
        "lacp_bundles": [],
        "reachability": []
    }

    # BGP neighbors
    for m in _RE_BGP_NEI.finditer(md_text):
        peer, state = m.group(1), m.group(2)
        facts["bgp_neighbors"].append({"peer": peer, "state": state, "evidence": m.group(0).strip()})

    # EVPN xconnect states
    for line in md_text.splitlines():
        m = _RE_XC_DOWN.search(line)
        if m:
            facts["evpn_xconnects"].append({"name": "unknown", "state": m.group(1), "evidence": line.strip()})

    # Ping success
    for m in _RE_PING.finditer(md_text):
        rate = int(m.group(1))
        facts["reachability"].append({
            "probe": "ping",
            "target": "unknown",
            "result": "success" if rate > 0 else "fail",
            "success_rate": rate,
            "evidence": m.group(0).strip()
        })

    return facts

def build_facts_messages(hostname: str, md_text: str, platform_hint: str, focus_signals: list[str], fewshots_text: str | None = None):
    context = {
        "hostname": hostname,
        "platform_hint": platform_hint,
        "focus_signals": focus_signals
    }
    user_payload = (
        "### Context\n"
        f"```json\n{json.dumps(context, indent=2)}\n```\n\n"
        "### Device Log (.md)\n"
        f"```md\n{md_text[:15000]}\n```"
    )
    msgs = [{"role": "system", "content": FACTS_SYSTEM}]
    if fewshots_text:  # optional dynamic examples
        msgs.append({"role": "user", "content": fewshots_text})
    msgs.append({"role": "user", "content": user_payload})
    return msgs

# def extract_facts_for_device(hostname: str, md_text: str, platform_hint: str, focus_signals: list[str],
#                              call_llm_fn, audit_dir: str) -> Dict[str, Any]:
#     # prefill via regex
#     prefilled = _regex_prefill(md_text)

#     # build messages (few-shots optional; leave None for now)
#     msgs = build_facts_messages(hostname, md_text, platform_hint, focus_signals, fewshots_text=None)

#     # audit prompt
#     write_audit(os.path.join(audit_dir, f"{hostname}__facts_prompt.txt"), json.dumps(msgs, indent=2))

#     raw = call_llm_fn(msgs, temperature=0.0) or ""
#     write_audit(os.path.join(audit_dir, f"{hostname}__facts_raw.json"), raw)

#     parsed = safe_json_loads(raw) or {}
#     # merge: prefer LLM structure; fall back to regex prefill
#     facts = {
#         "hostname": parsed.get("hostname", hostname),
#         "platform_guess": parsed.get("platform_guess", platform_hint or "unknown"),
#         "signals_seen": parsed.get("signals_seen", focus_signals),
#         "facts": parsed.get("facts", prefilled) or prefilled
#     }
#     return facts

## v5 ##
def extract_facts_for_device(
    hostname: str,
    md_text: str,
    platform_hint: str,
    focus_signals: list[str] | set[str],
    call_llm_fn=None,          # kept for future use, not used in Phase-1
    audit_dir: str | None = None,
    agent1_obj: dict | None = None,
    observed_cmds: list[str] | None = None,
    lexicon_candidates: list[str] | None = None,
) -> dict:
    """
    Build the single source of truth for this host in Phase-1.
    Returns a dict; optionally writes JSON to {audit_dir}/{host}__facts.json
    """
    
    # add this near the top of extract_facts_for_device(...)
    prefilled = _regex_prefill(md_text or "")

    plat = normalize_platform(platform_hint)
    focus = sorted(list(focus_signals or []))

    # 1) Observed (trusted for this task)
    trusted_from_observed = []
    for c in (observed_cmds or []):
        sc = sanitize_show(c, plat)
        if sc:
            trusted_from_observed.append(sc)

    # 2) Agent-1 ideas for THIS host (ALL unvalidated; none promoted to trusted)
    trusted_from_agent1 = []            # keep defined, but we won't use it
    candidates_from_agent1 = []         # this will hold BOTH suggested & candidate shows

    if isinstance(agent1_obj, dict):
        for est in (agent1_obj.get("expected_state") or []):
            for bucket in ("suggested_show", "candidate_show"):
                for item in (est.get(bucket) or []):
                    if isinstance(item, dict):
                        cmd = sanitize_show(item.get("cmd", ""), plat)
                    else:
                        cmd = sanitize_show(str(item), plat)
                    if cmd:
                        candidates_from_agent1.append(cmd)
                        

    # 3) Global lexicon candidates for this platform (ideas only)
    ideas_from_lexicon = []
    for c in (lexicon_candidates or []):
        sc = sanitize_show(c, plat)
        if sc:
            ideas_from_lexicon.append(sc)

    # 4) Signals seen from the .md (very light)
    signals_seen = []
    if md_text:
        low = md_text.lower()
        for s in ["bgp","isis","ospf","mpls","evpn","l2vpn","sr","srv6","intf","ip","bfd","lacp","ldp"]:
            if s in low:
                signals_seen.append(s)
    signals_seen = sorted(set(signals_seen) | set(focus))

    # 5) Dedup priority: observed > agent1 > lexicon
    def _dedup_keep_order(items: list[str]) -> list[str]:
        out, seen = [], set()
        for x in items:
            if x not in seen:
                out.append(x); seen.add(x)
        return out

    # observed-only trust (no promotion from Agent-1 in Phase-1)
    trusted_all = _dedup_keep_order(trusted_from_observed)
    # NEW: exclude any trusted commands from the candidate pool
    trusted_set = set(trusted_all)
    candidate_all = _dedup_keep_order(
        [c for c in (candidates_from_agent1 + ideas_from_lexicon) if c not in trusted_set]
    )

    facts = {
        "hostname": hostname,
        "platform_hint": plat,
        "signals_seen": signals_seen,
        "trusted_from_observed": trusted_from_observed,
        "trusted_from_agent1": trusted_from_agent1,
        "trusted_all": trusted_all,
        "candidates_from_agent1": candidates_from_agent1,
        "ideas_from_lexicon": ideas_from_lexicon,
        "candidates_all": candidate_all,
        "source_counts": {
            "observed": len(trusted_from_observed),
            "agent1_suggested": len(trusted_from_agent1),
            "agent1_candidates": len(candidates_from_agent1),
            "lexicon_candidates": len(ideas_from_lexicon),
            "trusted_total": len(trusted_all),
            "candidates_total": len(candidate_all),
        },
        "md_len": len(md_text or ""),
        "facts": prefilled,   # contains bgp_neighbors / reachability / evpn_xconnects with evidence lines
    }

    # audit (optional)
    if audit_dir:
        os.makedirs(audit_dir, exist_ok=True)
        write_audit(os.path.join(audit_dir, f"{hostname}__facts.json"), json.dumps(facts, indent=2))
    return facts