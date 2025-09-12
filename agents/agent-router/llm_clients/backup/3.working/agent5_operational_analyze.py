# ============================================================
# Agent-5 Operational Analyze
# Section 1: Imports, ENV variables, helpers
# ============================================================

import os
import re
import json
import glob
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from llm_api import call_llm  # same wrapper used in other agents

# v3 (.py.2.* worked but now v3 with modularity and new logic)
from agent5_shared import dbg, write_audit, safe_json_loads
from agent5_facts import extract_facts_for_device           # 5a
from agent5_reasoner import reason_per_device               # 5b
from agent5_critic import critic_patch                      # 5d
from agent5_correlator import correlate                     # 5c

# --- ENV / CONSTANTS ---
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "").strip()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN", "").strip()
REPO_ROOT       = os.getenv("REPO_ROOT", "/app/doo").strip()

# Limits to keep tokens in check
MAX_MD_CHARS_PER_DEVICE = 9000  # keep some headroom
MAX_FINDINGS_PER_DEVICE = 10

app    = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

# --- Debug / Audit helpers ---
DEBUG = os.getenv("DEBUG", "true").lower() in ("1", "true", "yes", "y")

# v3 - removed.  Now import from agent5_shared
# def dbg(msg: str):
#     if DEBUG:
#         print(f"[agent-5][DEBUG] {msg}", flush=True)

# v3 - removed.  Now import from agent5_shared
# def write_audit(path: str, content: str):
#     """Write debug/audit artifacts (prompts, raw LLM, inputs). Never raises."""
#     try:
#         os.makedirs(os.path.dirname(path), exist_ok=True)
#         with open(path, "w", encoding="utf-8") as f:
#             f.write(content if isinstance(content, str) else str(content))
#     except Exception as e:
#         dbg(f"[audit] failed to write {path}: {e}")

def audit_root(config_dir, task_dir):
    return os.path.join("/app/doo", config_dir, task_dir, "agent5_audit")

# ============================================================
# Section 2: Platform inference (IOS-XR vs IOS)
# ============================================================

IOSXR_HINTS = [
    r"\bRP/\d+/\w+\d+/CPU\d+:",          # RP/0/RP0/CPU0:...
    r"\b(config-bgp|config-ifs|config)#",# IOS-XR nested config prompts
    r"\bcommit\b",                        # XR commit model
    r"\bshow bgp l2vpn evpn\b",           # common on XR (also on NX-OS, but rare on IOS classic)
    r"\bBundle-Ether\d+\b",               # XR naming
    r"\bshow l2vpn xconnect\b",           # XR style
]

IOS_HINTS = [
    r"\bSwitch|Router>",                  # classic IOS prompts (exec)
    r"\bSwitch|Router\(config[^\)]*\)#",  # IOS config prompt
    r"\bBuilding configuration\.\.\.",    # IOS write mem outputs
    r"\binterface GigabitEthernet\d",     # common on IOS too (heuristic)
    r"\bshow ip route\b",                 # classic IOS command
]

def _count_matches(patterns: List[str], text: str) -> int:
    score = 0
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE | re.MULTILINE):
            score += 1
    return score

def infer_platform_from_md(md_text: str) -> str:
    """
    Heuristic platform detector using the captured .md log content.
    Returns one of: "ios-xr", "ios", or "unknown".
    """
    if not md_text:
        return "unknown"

    xr_score  = _count_matches(IOSXR_HINTS, md_text)
    ios_score = _count_matches(IOS_HINTS,  md_text)

    # Strong preference if one clearly wins
    if xr_score >= ios_score + 2 and xr_score >= 2:
        return "ios-xr"
    if ios_score >= xr_score + 2 and ios_score >= 2:
        return "ios"

    # Tie-breaker: some light-weight cues
    if "RP/" in md_text or "commit" in md_text:
        return "ios-xr"
    if "Building configuration" in md_text:
        return "ios"

    return "unknown"

# ============================================================
# Section 3: Read task inputs (agent1 summary, show_cmds.ini, .md logs)
# ============================================================

from typing import Dict, List, Tuple, Any

REPO_ROOT = "/app/doo"  # keep consistent with other agents

def task_root(config_dir: str, task_dir: str) -> str:
    return os.path.join(REPO_ROOT, config_dir, task_dir)

# ---------- 3A. Agent‑1 summary loader ----------
def load_agent1_summary(config_dir: str, task_dir: str) -> List[dict]:
    """
    Prefer agent1_summary.json. If missing, fall back to the latest agent1_summary_<sha>.json.
    Returns a Python list (parsed JSON array). On failure, returns [].
    """
    root = task_root(config_dir, task_dir)
    primary = os.path.join(root, "agent1_summary.json")

    candidates = []
    # if os.path.exists(primary):
    #     candidates.append(primary)

    # # collect per‑commit files and sort by mtime (desc)
    # try:
    #     for fn in os.listdir(root):
    #         if fn.startswith("agent1_summary_") and fn.endswith(".json"):
    #             candidates.append(os.path.join(root, fn))
    #     candidates = sorted(set(candidates), key=lambda p: os.path.getmtime(p), reverse=True)
    # except Exception:
    #     pass
    if os.path.exists(primary):
        dbg(f"[inputs] found agent1_summary.json at {primary}")
        candidates.append(primary)

    # collect per‑commit files and sort by mtime (desc)
    try:
        for fn in os.listdir(root):
            if fn.startswith("agent1_summary_") and fn.endswith(".json"):
                candidates.append(os.path.join(root, fn))
        candidates = sorted(set(candidates), key=lambda p: os.path.getmtime(p), reverse=True)
        dbg(f"[inputs] candidate Agent-1 JSON files (newest first): {candidates}")
    except Exception as e:
        dbg(f"[inputs] listing Agent-1 JSON candidates failed: {e}")

    for path in candidates:
        try:
            raw = open(path, "r", encoding="utf-8").read().strip()
            if not raw:
                continue
            # Agent‑1 returns a JSON array string
            data = json.loads(raw)
            if isinstance(data, list):
                dbg(f"[inputs] using Agent-1 summary file: {path} (items={len(data)})")
                return data
        except Exception as e:
            print(f"[agent-5][WARN] Could not parse {path}: {e}", flush=True)

    # print("[agent-5][INFO] No usable Agent‑1 summary found; continuing without it.", flush=True)
    dbg("[inputs] No usable Agent‑1 summary found; continuing without it.")
    return []

# ---------- 3B. show_cmds.ini loader ----------
_SHOW_LINE = re.compile(r'(?:^|=)\s*(show\s+.+)$', re.IGNORECASE)

def load_show_cmds_ini(config_dir: str, task_dir: str) -> List[str]:
    """
    Reads <task_root>/show_cmds.ini and extracts unique 'show ...' lines.
    Tolerates 'key = show ...' and comments.
    """
    root = task_root(config_dir, task_dir)
    ini_path = os.path.join(root, "show_cmds.ini")
    cmds: List[str] = []

    # if not os.path.exists(ini_path):
    #     print(f"[agent-5][INFO] show_cmds.ini not found at {ini_path}", flush=True)
    #     return cmds
    if not os.path.exists(ini_path):
        dbg(f"[inputs] show_cmds.ini not found at {ini_path}")
        return cmds

    seen = set()
    try:
        for raw in open(ini_path, "r", encoding="utf-8"):
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            m = _SHOW_LINE.search(line)
            if m:
                cmd = m.group(1).strip()
                if cmd.lower().startswith("show ") and cmd not in seen:
                    seen.add(cmd)
                    cmds.append(cmd)
                    dbg(f"[inputs] show-cmd detected: {cmd}")
    except Exception as e:
        print(f"[agent-5][WARN] Failed reading show_cmds.ini: {e}", flush=True)

    dbg(f"[inputs] total show_cmds.ini commands: {len(cmds)}")
    return cmds

# ---------- 3C. Per‑device .md log loader ----------
_MD_DEVICE = re.compile(r"\*\*Device:\*\*\s*([A-Za-z0-9._\-]+)", re.IGNORECASE)

def _infer_hostname_from_md_file(md_path: str, content: str) -> str:
    # Prefer explicit header in content
    m = _MD_DEVICE.search(content)
    if m:
        return m.group(1).strip()
    # Fallback: filename without extension
    return os.path.splitext(os.path.basename(md_path))[0]

def load_device_md_logs(config_dir: str, task_dir: str) -> Dict[str, str]:
    """
    Loads all Markdown logs from <task_root>/grading_logs/*.md
    Returns dict: hostname -> md_text
    """
    root = task_root(config_dir, task_dir)
    log_dir = os.path.join(root, "grading_logs")
    host_to_md: Dict[str, str] = {}

    # if not os.path.isdir(log_dir):
    #     print(f"[agent-5][INFO] grading_logs not found at {log_dir}", flush=True)
    #     return host_to_md
    if not os.path.isdir(log_dir):
        dbg(f"[inputs] grading_logs not found at {log_dir}")
        return host_to_md
    dbg(f"[inputs] scanning Markdown logs in {log_dir}")

    for fn in sorted(os.listdir(log_dir)):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(log_dir, fn)
        try:
            text = open(p, "r", encoding="utf-8").read()
            # host = _infer_hostname_from_md_file(p, text)
            # host_to_md[host] = text
            host = _infer_hostname_from_md_file(p, text)
            host_to_md[host] = text
            try:
                sz = os.path.getsize(p)
                dbg(f"[inputs] md: {os.path.basename(p)} → host={host} ({sz} bytes)")
            except Exception:
                dbg(f"[inputs] md: {os.path.basename(p)} → host={host} (size n/a)")
        except Exception as e:
            print(f"[agent-5][WARN] Could not read {p}: {e}", flush=True)

    return host_to_md

# ---------- 3D. Build device index ----------
def build_device_index(agent1_objs: List[dict], md_map: Dict[str, str]) -> List[str]:
    """
    Union of hostnames from Agent‑1 summary and .md logs.
    Keeps order: md_map first (observed logs), then any extra from Agent‑1.
    """
    names = list(md_map.keys())
    seen = set(names)
    for obj in agent1_objs:
        h = str(obj.get("hostname", "")).strip()
        if h and h not in seen:
            names.append(h)
            seen.add(h)
    return names

# ============================================================
# Section 4: Platform inference + dynamic signals + guardrails
# ============================================================

import re
from typing import Optional, Set, Tuple

# ---------- 4A. Infer platform (ios-xr vs ios) ----------
_PLAT_SIGS = {
    "ios-xr": [
        r"RP/\d+/\w+\d+/CPU\d+:",          # XR prompt style
        r"\(config-bgp[^\)]*\)#",          # XR submode prompt
        r"^Tue\s\w{3}\s",                  # XR timestamps in many sample logs
        r"BGP NSR",                        # XR-only features often present
        r"LC/|0/RP",                       # XR LC/RP tokens
    ],
    "ios": [
        r"^Router>", r"^Switch>",
        r"\(config\)#",                    # classic IOS config prompt
        r"^Codes:\s+L - local,",           # IOS 'show ip route' codes header
        r"Success rate is \d+ percent",    # IOS ping summary
    ],
}

def infer_platform_hint(md_text: str, agent1_obj: Optional[dict] = None) -> str:
    """
    Very light heuristic. Returns 'ios-xr', 'ios', or 'unknown'.
    Prefers .md evidence; falls back to Agent‑1 hostname/role tokens if helpful.
    """
    text = md_text or ""
    # 1) Heuristic over log text
    xr_hits = sum(bool(re.search(p, text, re.MULTILINE)) for p in _PLAT_SIGS["ios-xr"])
    ios_hits = sum(bool(re.search(p, text, re.MULTILINE)) for p in _PLAT_SIGS["ios"])
    if xr_hits > ios_hits and xr_hits >= 1:
        return "ios-xr"
    if ios_hits > xr_hits and ios_hits >= 1:
        return "ios"

    # 2) Gentle hint from Agent‑1 device name/role
    if agent1_obj:
        hn = str(agent1_obj.get("hostname", "")).upper()
        role = str(agent1_obj.get("role", "")).lower()
        # If hostname looks like C-PE-* or A-PE-* (your lab uses XR there), nudge XR
        if re.search(r"\b[ABC]-P(E|)\b|\bASBR\b|\bRR\b", hn) or any(k in role for k in ("provider", "asbr", "rr")):
            return "ios-xr"

    return "unknown"


# ---------- 4B. Dynamic protocol “signals” ----------
PROTO_WORDS = {
    "bgp":   [r"\bbgp\b", r"\bl2vpn evpn\b", r"route distinguisher", r"evpn\b"],
    "isis":  [r"\bisis\b", r"IS-IS"],
    "ospf":  [r"\bospf\b"],
    "mpls":  [r"\bmpls\b", r"label", r"ldp\b", r"te\b"],
    "sr":    [r"\bsegment\s*routing\b", r"\bsrv6\b", r"locator\b", r"sid\b"],
    "l2vpn": [r"\bxconnect\b", r"\bevpn\b", r"\bbundle-ether\b"],
    "ip":    [r"\bip route\b", r"\bprefex\b", r"\bpfx\b"],
    "intf":  [r"\binterface\b", r"\bGigabitEthernet\b", r"\bBundle-Ether\b"],
}

def derive_dynamic_signals(md_text: str, agent1_obj: Optional[dict] = None) -> Set[str]:
    """
    Build a set of protocols/features to focus on for a device.
    Sources:
      • What actually appears in the .md (primary)
      • Agent‑1 intents (secondary)
    """
    signals: Set[str] = set()
    text = (md_text or "")

    for proto, patterns in PROTO_WORDS.items():
        if any(re.search(p, text, re.IGNORECASE | re.MULTILINE) for p in patterns):
            signals.add(proto)

    # From Agent‑1 intents, add hints if present
    if agent1_obj:
        intents = agent1_obj.get("config_intents") or []
        joined = " ".join(intents).lower()
        for proto in PROTO_WORDS:
            if proto in joined:
                signals.add(proto)

    # Always include baseline network health signals
    if "bgp" in signals and "l2vpn" in signals:
        signals.add("evpn")

    return signals


# ---------- 4C. Guardrails / validation for candidate commands ----------
_FORBID_ALWAYS = [
    r"^\s*configure", r"^\s*conf t\b", r"^\s*reload\b", r"^\s*clear\b",
    r"^\s*write\b", r"^\s*copy\b", r"^\s*debug\b", r"^\s*monitor\b",
]

_ALLOW_ACTIVE_WHEN_TRUE = [
    r"^\s*ping\b", r"^\s*traceroute\b",
]

def validate_candidate_cmd(cmd: str, allow_active: bool = False, platform_hint: str = "unknown") -> Tuple[bool, str]:
    """
    Return (ok, reason). Only 'show' is always allowed.
    If allow_active=True, permit 'ping'/'traceroute' (read‑only active probes).
    Never allow config/clear/reload/debug etc.
    """
    c = (cmd or "").strip()
    if not c:
        return False, "empty command"

    # Absolute forbids
    for pat in _FORBID_ALWAYS:
        if re.search(pat, c, re.IGNORECASE):
            return False, f"blocked (dangerous): {c}"

    # Allow SHOW
    if re.match(r"^\s*show\b", c, re.IGNORECASE):
        return True, "ok"

    # Optional active probes
    if allow_active:
        for pat in _ALLOW_ACTIVE_WHEN_TRUE:
            if re.search(pat, c, re.IGNORECASE):
                return True, "ok (active probe permitted)"

    # Everything else is denied
    return False, f"unsupported command type for guardrails: {c}"

# ============================================================
# Section 5: LLM prompts + wrappers (per-device & cross-device)
# ============================================================

import json

# ----- 5A. Per-device system prompt -----
_PER_DEVICE_SYSTEM = """You are a senior Cisco SP NOC engineer.
You will receive:
  • Optional JSON from Agent‑1 summarizing intended configuration for this host
  • CLI show-output captured in a Markdown (.md) file for this host (IOS or IOS‑XR)
Your tasks:
  1) Determine platform ("ios-xr" or "ios") if possible from the log, else "unknown".
  2) From the log ONLY, assess health for protocols/features that appear (BGP, EVPN/L2VPN,
     ISIS/OSPF, SR/SRv6, MPLS, interface/port-channel, reachability).
  3) If intent JSON is provided, use it as context for *expected* state, but do NOT invent facts
     not visible in the log.
  4) Return a single JSON object with fields:
     {
       "hostname": "<string>",
       "platform": "ios-xr" | "ios" | "unknown",
       "signals_seen": ["bgp","evpn","isis","mpls","sr","l2vpn","intf","ip", ...],
       "status": "healthy" | "degraded" | "error" | "unknown",
       "findings": [ {"signal":"bgp","severity":"warn|error|info","detail":"..."} , ... ],
       "recommended_show_cmds": [ "show ...", ... ],   // safe, read-only
       "optional_active_cmds": [ "ping ...", "traceroute ..." ]  // optional probes only
     }
  5) NEVER include config/clear/reload/debug commands in either list.
  6) Be conservative: if signal is unclear, mark severity "info" and explain.
  7) Only report signals that are evidenced by the provided log text, agent‑1 intents, or show_cmds.ini. Do not infer protocols that are not visible.
Output ONLY the JSON object.
Prefer recommending follow-up 'show' commands that are already present in show_cmds.ini; add at most 3 new 'show' commands only if clearly warranted by the findings. Never suggest config/debug/clear.
Do not mention devices other than the current hostname. If a signal is not evidenced in the log/context, exclude it.
"""

# ----- 5B. Cross-device system prompt -----
_CROSS_DEVICE_SYSTEM = """You are a senior NOC service lead.
You will receive a JSON array of per-device analyses (from other calls).
Correlate across devices to identify fabric-wide issues (e.g., EVPN VPWS down on both PEs,
BGP session asymmetry, DF election pending, bundle down causing AC down, etc).
You MUST only reference devices that appear in the input array. If a device or link name is not present in the input data, do NOT invent it. 
If no cross‑device issue is clear, set top_incidents to an empty list.  
You must only report issues based upon information provided
Return ONLY one JSON object:
{
  "task_status": "healthy" | "mixed" | "degraded" | "error" | "unknown",
  "top_incidents": [ {"scope":"pair|site|global","summary":"...","impact":"...","devices":["...","..."]} ],
  "remediation_themes": [ "Check LACP on BE23 on C-PE-2/3", "Validate DF election for EVI 30020", ... ],
  "safe_followup_show_cmds": [ "show ..." ],
  "optional_active_probes": [ "ping ...", "traceroute ..." ]
}
Be conservative and avoid config changes; only suggest read-only checks and optional probes.
Prefer recommending follow-up 'show' commands that are already present in show_cmds.ini; add at most 3 new 'show' commands only if clearly warranted by the findings. Never suggest config/debug/clear.
Use only device names that appear in the provided per-device JSON array; do NOT invent devices or links. 
If no clear cross-device issue exists, return empty lists for top_incidents and remediation_themes.
Prefer recommending follow-up 'show' commands that are already present in show_cmds.ini across devices; add at most 3 new 'show' commands, read-only only.
"""

def _build_per_device_messages(
    hostname: str,
    md_text: str,
    agent1_obj: dict | None,
    platform_hint: str,
    signals: set[str],
    allow_active: bool,
    show_cmds: list[str] | None = None
) -> list[dict]:
    """Compose messages for per-device analysis."""
    # Pack context for the model (short + bounded)
    context = {
        "hostname": hostname,
        "platform_hint": platform_hint,
        "focus_signals": sorted(list(signals)),
        "allow_active_probes": bool(allow_active),
        "agent1_summary": agent1_obj or {},
        "show_cmds_ini": show_cmds or []   # <— include the ini list
    }

    dbg(f"[per-device] {hostname} context focus_signals={sorted(list(signals))} "
        f"platform_hint={platform_hint} show_cmds_ini={len(show_cmds or [])}")

    user_payload = (
        "### Context (JSON)\n"
        f"```json\n{json.dumps(context, indent=2)}\n```\n\n"
        "### Device Log (Markdown)\n"
        f"```md\n{md_text[:15000]}\n```"
    )
    # --- debug/audit: record the exact prompt we are sending ---
    try:
        md_preview = md_text[:600].replace("\n", "\\n")
        dbg(f"[per-device] host={hostname} platform_hint={platform_hint} signals={sorted(list(signals))} md_preview(600)={md_preview}")
        if AUDIT_ROOT:
            write_audit(os.path.join(AUDIT_ROOT, f"{hostname}__per_device_prompt.txt"),
                        f"--- SYSTEM ---\n{_PER_DEVICE_SYSTEM}\n\n--- USER ---\n{user_payload}\n")
    except Exception as e:
        dbg(f"[per-device] prompt logging failed for {hostname}: {e}")
    return [
        {"role": "system", "content": _PER_DEVICE_SYSTEM},
        {"role": "user", "content": user_payload}
    ]

def _build_cross_device_messages(per_device_jsons: list[dict]) -> list[dict]:
    """Compose messages for cross-device correlation."""
    arr = per_device_jsons[:]
    user_payload = f"```json\n{json.dumps(arr, indent=2)}\n```"
    # --- debug/audit: record cross-device prompt ---
    try:
        if AUDIT_ROOT:
            write_audit(os.path.join(AUDIT_ROOT, "cross_prompt.txt"),
                        f"--- SYSTEM ---\n{_CROSS_DEVICE_SYSTEM}\n\n--- USER ---\n{user_payload}\n")
        dbg(f"[cross] built cross-device prompt for {len(arr)} devices")
    except Exception as e:
        dbg(f"[cross] prompt logging failed: {e}")

    return [
        {"role": "system", "content": _CROSS_DEVICE_SYSTEM},
        {"role": "user", "content": user_payload}
    ]

def _call_llm(messages: list[dict], temperature: float = 0.0) -> str:
    """Thin wrapper around your existing llm_api.call_llm."""
    from llm_api import call_llm
    return call_llm(messages, temperature=temperature)

def per_device_analyze_with_llm(
    hostname: str,
    md_text: str,
    agent1_obj: dict | None,
    platform_hint: str,
    signals: set[str],
    allow_active: bool,
    show_cmds: list[str] | None = None
) -> dict:
    """Run the per-device LLM call and parse JSON with hardening."""
    msgs = _build_per_device_messages(
        hostname, md_text, agent1_obj, platform_hint, signals, allow_active,
        show_cmds=show_cmds
    )

    raw = _call_llm(msgs, temperature=0.0) or ""
    # --- debug/audit: raw LLM output ---
    try:
        dbg(f"[per-device] host={hostname} LLM raw (first 600): {str(raw)[:600]}")
        if AUDIT_ROOT:
            write_audit(os.path.join(AUDIT_ROOT, f"{hostname}__per_device_raw.json"), str(raw))
    except Exception as e:
        dbg(f"[per-device] raw logging failed for {hostname}: {e}")

    # Try strict JSON first
    try:
        obj = json.loads(raw)
        # if isinstance(obj, dict):
        #     return obj
        if isinstance(obj, dict):
            dbg(f"[per-device] host={hostname} JSON parse OK keys={list(obj.keys())}")
            return obj
    except json.JSONDecodeError:
        pass
    # Try to recover JSON from fenced blocks
    import re
    m = re.search(r"```json\s*(.+?)\s*```", raw, flags=re.DOTALL | re.IGNORECASE)
    if m:
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    # Last resort
    return {
        "hostname": hostname,
        "platform": platform_hint or "unknown",
        "signals_seen": sorted(list(signals)),
        "status": "unknown",
        "findings": [{"signal": "meta", "severity": "info", "detail": "LLM response not strictly JSON"}],
        "recommended_show_cmds": [],
        "optional_active_cmds": []
    }

def cross_device_analyze_with_llm(per_device_objs: list[dict]) -> dict:
    """Run the cross-device LLM call and parse JSON with hardening."""
    msgs = _build_cross_device_messages(per_device_objs)
    raw = _call_llm(msgs, temperature=0.0) or ""
    # --- debug/audit: raw LLM output ---
    try:
        dbg(f"[cross] LLM raw (first 800): {str(raw)[:800]}")
        if AUDIT_ROOT:
            write_audit(os.path.join(AUDIT_ROOT, "cross_raw.json"), str(raw))
    except Exception as e:
        dbg(f"[cross] raw logging failed: {e}")

    try:
        obj = json.loads(raw)
        # if isinstance(obj, dict):
        #     return obj
        if isinstance(obj, dict):
            dbg(f"[cross] JSON parse OK keys={list(obj.keys())}")
            return obj
    except json.JSONDecodeError:
        pass
    import re
    m = re.search(r"```json\s*(.+?)\s*```", raw, flags=re.DOTALL | re.IGNORECASE)
    if m:
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    return {
        "task_status": "unknown",
        "top_incidents": [],
        "remediation_themes": [],
        "safe_followup_show_cmds": [],
        "optional_active_probes": []
    }

# ============================================================
# Section 6: Orchestration + Slack formatting & command handler
# ============================================================

import os
import glob
import json
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Reuse config root from other agents
REPO_ROOT = os.getenv("REPO_ROOT", "/app/doo")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)
slack = WebClient(token=SLACK_BOT_TOKEN)

# ---------- helpers for Slack blocks ----------

def _fmt_kv(*pairs):
    # pairs: list of (key, value) tuples; renders in Slack mrkdwn
    lines = []
    for k, v in pairs:
        lines.append(f"*{k}:* {v}")
    return "\n".join(lines)

def _truncate_list(items, limit=8):
    items = items or []
    display = items[:limit]
    more = len(items) - len(display)
    if more > 0:
        return display + [f"... (+{more} more)"]
    return display

def _build_per_device_block(summary: dict) -> dict:
    host = summary.get("hostname", "(unknown)")
    status = summary.get("status", "unknown")
    platform = summary.get("platform", "unknown")
    signals = ", ".join(summary.get("signals_seen", [])) or "(none)"
    findings = summary.get("findings", [])
    rec_shows = _truncate_list(summary.get("recommended_show_cmds", []))
    probes = _truncate_list(summary.get("optional_active_cmds", []))

    # Flatten findings to bullet lines
    finding_lines = []
    for f in findings[:8]:
        sig = f.get("signal", "meta")
        sev = f.get("severity", "info")
        det = f.get("detail", "").strip()
        finding_lines.append(f"• [{sev}] {sig}: {det}" if det else f"• [{sev}] {sig}")
    if len(findings) > 8:
        finding_lines.append(f"... (+{len(findings)-8} more)")

    text = (
        f"*Device:* `{host}`\n"
        f"{_fmt_kv(('Status', status), ('Platform', platform), ('Signals', signals))}\n"
        f"*Key findings:*\n" + ("\n".join(finding_lines) if finding_lines else "• (none)") + "\n"
        f"*Suggested show commands:*\n" + ("\n".join([f"• `{c}`" for c in rec_shows]) if rec_shows else "• (none)") + "\n"
        f"*Optional probes:*\n" + ("\n".join([f"• `{p}`" for p in probes]) if probes else "• (none)")
    )
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

def _build_cross_device_block(agg: dict, config_dir: str, task_dir: str) -> list:
    status = agg.get("task_status", "unknown")
    incidents = agg.get("top_incidents", []) or []
    themes = agg.get("remediation_themes", []) or []
    shows = _truncate_list(agg.get("safe_followup_show_cmds", []))
    probes = _truncate_list(agg.get("optional_active_probes", []))

    lines_inc = []
    for inc in incidents[:6]:
        scope = inc.get("scope", "scope")
        summary = inc.get("summary", "")
        devs = ", ".join(inc.get("devices", [])[:6])
        impact = inc.get("impact", "")
        lines_inc.append(f"• [{scope}] {summary} — impact: {impact} — devices: {devs}")
    if len(incidents) > 6:
        lines_inc.append(f"... (+{len(incidents)-6} more)")

    blocks = [
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": f"*Operational Analysis Summary*\n\n"
                          f"*Task:* `{task_dir}`\n"
                          f"*Config Dir:* `{config_dir}`\n"
                          f"*Status:* {status}"}},
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Cross-device incidents:*\n" + ("\n".join(lines_inc) if lines_inc else "• (none)")}},

        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Remediation themes:*\n" + ("\n".join([f"• {t}" for t in themes[:8]]) if themes else "• (none)")}},
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Follow-up show commands:*\n" + ("\n".join([f"• `{c}`" for c in shows]) if shows else "• (none)")}},
        {"type": "section",
         "text": {"type": "mrkdwn",
                  "text": "*Optional probes:*\n" + ("\n".join([f"• `{p}`" for p in probes]) if probes else "• (none)")}},
    ]
    return blocks

# ---------- main run helpers ----------

def _load_agent1_latest(config_dir: str, task_dir: str) -> dict | None:
    path = os.path.join(REPO_ROOT, config_dir, task_dir, "agent1_summary.json")
    if os.path.exists(path):
        try:
            txt = open(path).read()
            return json.loads(txt)
        except Exception:
            return None
    return None

def _read_device_md_files(config_dir: str, task_dir: str) -> list[tuple[str, str]]:
    grade_dir = os.path.join(REPO_ROOT, config_dir, task_dir, "grading_logs")
    pairs = []
    for md in sorted(glob.glob(os.path.join(grade_dir, "*.md"))):
        host = os.path.basename(md).removesuffix(".md")
        try:
            txt = open(md, "r").read()
            pairs.append((host, txt))
        except Exception:
            # skip unreadable file
            continue
    return pairs

def _persist_json(obj: dict | list, path: str):
    try:
        with open(path, "w") as f:
            json.dump(obj, f, indent=2)
        return True
    except Exception:
        return False

def _infer_platform_hint_from_md(md_text: str) -> str:
    # quick heuristic; full platform decision is inside LLM too
    if "RP/0/" in md_text or "IOS XR" in md_text or "config-bgp" in md_text:
        return "ios-xr"
    if "#" in md_text and "IOS" in md_text and ">" not in md_text:
        return "ios"
    return "unknown"

def _default_signals():
    # start broad; LLM will prune
    return {"bgp", "evpn", "l2vpn", "isis", "ospf", "mpls", "sr", "srv6", "intf", "ip"}

def _post_files(channel_id: str, files: list[tuple[str, str]]):
    # files: list of (filepath, title)
    for path, title in files:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "rb") as f:
                slack.files_upload_v2(channel=channel_id, file=f, title=title,
                                      filename=os.path.basename(path))
        except SlackApiError:
            pass

# ---------- Slack command: /operational-analyze <config_dir> <task_dir> ----------
@app.command("/operational-analyze")
def handle_operational_analyze(ack, command, respond, logger):
    # Ack once, right away
    ack({"response_type": "ephemeral", "text": "Starting analysis !!"})

    # Log the raw payload first
    dbg(f"/operational-analyze received: {command}")
    dbg(f"[/operational-analyze] payload: {command}")

    # Parse args BEFORE logging them
    text = (command.get("text") or "").strip()
    args = text.split()
    dbg(f"[/operational-analyze] text='{text}' parsed args={args}")

    # Remove the second ack() block that caused confusion
    # try:
    #     ack({"response_type": "ephemeral", "text": "Analyzing operational logs…"})
    # except Exception:
    #     return

    if len(args) != 2:
        slack.chat_postMessage(
            channel=command["channel_id"],
            text="Usage: `/operational-analyze <config_dir> <task_dir>`"
        )
        return

    config_dir, task_dir = args
    channel_id = command["channel_id"]

    # v3
    #  Create common directories up-front
    out_dir = os.path.join(REPO_ROOT, config_dir, task_dir)
    os.makedirs(out_dir, exist_ok=True)

    global AUDIT_ROOT
    AUDIT_ROOT = os.path.join(out_dir, "agent5_audit")
    try:
        os.makedirs(AUDIT_ROOT, exist_ok=True)
    except Exception as e:
        dbg(f"[audit] could not create {AUDIT_ROOT}: {e}")


    # v3
    # --- load and log show_cmds.ini for this task ---
    show_cmds = load_show_cmds_ini(config_dir, task_dir)
    dbg(f"[inputs] total show_cmds.ini commands: {len(show_cmds)}")
    for c in show_cmds:
        dbg(f"[inputs] show-cmd detected: {c}")

    # Archive show_cmds.ini into audit (helps triage)
    try:
        sc_path = os.path.join(AUDIT_ROOT, "_show_cmds.ini.txt")
        with open(sc_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(show_cmds) + ("\n" if show_cmds else ""))
        dbg(f"[audit] wrote {sc_path}")
    except Exception as e:
        dbg(f"[audit] failed writing _show_cmds.ini.txt: {e}")

    # Load context + logs
    agent1 = _load_agent1_latest(config_dir, task_dir)  # JSON array from Agent‑1
    md_pairs = _read_device_md_files(config_dir, task_dir)
    if not md_pairs:
        slack.chat_postMessage(
            channel=channel_id,
            text=f"No Markdown logs found under `{config_dir}/{task_dir}/grading_logs`."
        )
        return

    # inputs snapshot for audit
    try:
        inputs_txt = [
            f"config_dir={config_dir}",
            f"task_dir={task_dir}",
            f"agent1_summary_present={isinstance(agent1, list)} items={len(agent1) if isinstance(agent1, list) else 0}",
            f"md_pairs_count={len(md_pairs)}",
            "md_files=" + ", ".join([h for h,_ in md_pairs])
        ]
        dbg(f"[inputs] " + " | ".join(inputs_txt))
        if AUDIT_ROOT:
            write_audit(os.path.join(AUDIT_ROOT, "_inputs.txt"), "\n".join(inputs_txt) + "\n")
    except Exception as e:
        dbg(f"[inputs] failed to write inputs snapshot: {e}")


    # v3
    facts_bundle = []           # collect per-device facts
    facts_dir = os.path.join(AUDIT_ROOT, "facts")
    os.makedirs(facts_dir, exist_ok=True)

    for host, md_text in md_pairs:
        platform_hint = _infer_platform_hint_from_md(md_text)
        signals = _default_signals()
        dbg(f"[facts] extracting facts for host={host}")
        facts_obj = extract_facts_for_device(
            hostname=host,
            md_text=md_text,
            platform_hint=platform_hint,
            focus_signals=sorted(list(signals)),
            call_llm_fn=call_llm,            # reuse your wrapper
            audit_dir=facts_dir
        )
        facts_bundle.append(facts_obj)

    # persist the facts as a single file (optional)
    facts_path = os.path.join(out_dir, "agent5_facts.json")
    _persist_json(facts_bundle, facts_path)
    dbg(f"[persist] facts JSON → {facts_path}")

    # Per-device loop
    per_device_objs = []
    for host, md_text in md_pairs:
        platform_hint = _infer_platform_hint_from_md(md_text)

        # --- dynamic signals derived from evidence (single calc only) ---
        sig_from_md = derive_dynamic_signals(md_text)
        sig_from_agent1 = derive_dynamic_signals(
            "", _find_agent1_for_host(agent1, host) if isinstance(agent1, list) else None
        )
        sig_from_ini = derive_dynamic_signals("\n".join(show_cmds))
        signals = set()
        signals |= sig_from_md
        signals |= sig_from_agent1
        signals |= sig_from_ini
        dbg(f"[per-device] {host} platform_hint={platform_hint} signals_dynamic={sorted(list(signals))}")

        # LLM call
        obj = per_device_analyze_with_llm(
            hostname=host,
            md_text=md_text,
            agent1_obj=_find_agent1_for_host(agent1, host) if isinstance(agent1, list) else None,
            platform_hint=platform_hint,
            signals=signals,
            allow_active=False,
            show_cmds=show_cmds  # <— you added this earlier; keep it
        )

        # Short result log (helps spot hallucinations quickly)
        dbg(f"[per-device][result] host={host} status={obj.get('status','?')} "
            f"platform={obj.get('platform','?')} "
            f"findings={len(obj.get('findings') or [])} "
            f"shows={len(obj.get('recommended_show_cmds') or [])}")

        per_device_objs.append(obj)

    # Persist per-device bundle
    per_device_path = os.path.join(out_dir, "agent5_per_device.json")
    _persist_json(per_device_objs, per_device_path)
    try:
        dbg(f"[persist] per-device JSON → {per_device_path} ({os.path.getsize(per_device_path)} bytes)")
    except Exception:
        dbg(f"[persist] per-device JSON → {per_device_path} (size n/a)")

    # Cross-device aggregation
    agg = cross_device_analyze_with_llm(per_device_objs)
    # --- sanitize cross-device incidents to known devices only ---
    known = {obj.get("hostname") for obj in per_device_objs}
    clean_incidents = []
    for inc in agg.get("top_incidents", []) or []:
        devs = [d for d in (inc.get("devices") or []) if d in known]
        if devs or not inc.get("devices"):
            inc["devices"] = devs
            clean_incidents.append(inc)
    agg["top_incidents"] = clean_incidents
    dbg(f"[cross-device] incidents_kept={len(clean_incidents)} (filtered to known devices)")

    cross_path = os.path.join(out_dir, "agent5_cross_device.json")
    _persist_json(agg, cross_path)
    try:
        dbg(f"[persist] cross-device JSON → {cross_path} ({os.path.getsize(cross_path)} bytes)")
    except Exception:
        dbg(f"[persist] cross-device JSON → {cross_path} (size n/a)")

    # Build Slack message
    blocks = _build_cross_device_block(agg, config_dir, task_dir)
    for obj in per_device_objs[:5]:
        blocks.append({"type": "divider"})
        blocks.append(_build_per_device_block(obj))
    if len(per_device_objs) > 5:
        blocks.append({"type": "context", "elements": [
            {"type": "mrkdwn", "text": f"... and {len(per_device_objs)-5} more devices. See JSON attachments."}
        ]})

    try:
        slack.chat_postMessage(channel=channel_id, blocks=blocks, text="Operational Analysis")
    except SlackApiError:
        slack.chat_postMessage(channel=channel_id, text="Operational analysis complete. See attachments.")

    # Attach JSON artifacts
    _post_files(channel_id, [
        (per_device_path, "Agent‑5 Per‑device Analysis (JSON)"),
        (cross_path, "Agent‑5 Cross‑device Analysis (JSON)"),
    ])


# ---------- helper: pick agent‑1 row for host ----------

def _find_agent1_for_host(agent1_obj_list, hostname: str):
    if not isinstance(agent1_obj_list, list):
        return None
    for row in agent1_obj_list:
        if isinstance(row, dict) and row.get("hostname") == hostname:
            return row
    return None

# ============================================================
# Section 7: Entrypoint
# ============================================================

if __name__ == "__main__":
    print("[DEBUG] Agent-5 is running...", flush=True)
    try:
        SocketModeHandler(app, SLACK_APP_TOKEN).start()
    except Exception as e:
        print(f"[FATAL] Failed to start SocketModeHandler: {e}", flush=True)
