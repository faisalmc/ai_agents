# agent5_facts.py
import os, re, json
from typing import Dict, Any
from agent5_shared import dbg, write_audit, safe_json_loads

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

def extract_facts_for_device(hostname: str, md_text: str, platform_hint: str, focus_signals: list[str],
                             call_llm_fn, audit_dir: str) -> Dict[str, Any]:
    # prefill via regex
    prefilled = _regex_prefill(md_text)

    # build messages (few-shots optional; leave None for now)
    msgs = build_facts_messages(hostname, md_text, platform_hint, focus_signals, fewshots_text=None)

    # audit prompt
    write_audit(os.path.join(audit_dir, f"{hostname}__facts_prompt.txt"), json.dumps(msgs, indent=2))

    raw = call_llm_fn(msgs, temperature=0.0) or ""
    write_audit(os.path.join(audit_dir, f"{hostname}__facts_raw.json"), raw)

    parsed = safe_json_loads(raw) or {}
    # merge: prefer LLM structure; fall back to regex prefill
    facts = {
        "hostname": parsed.get("hostname", hostname),
        "platform_guess": parsed.get("platform_guess", platform_hint or "unknown"),
        "signals_seen": parsed.get("signals_seen", focus_signals),
        "facts": parsed.get("facts", prefilled) or prefilled
    }
    return facts
