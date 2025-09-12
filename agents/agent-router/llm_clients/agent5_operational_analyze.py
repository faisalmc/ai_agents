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
from agent5_shared import load_observed_commands, load_lexicon_candidates, normalize_platform
from agent5_facts import extract_facts_for_device           # 5a
from agent5_reasoner import reason_per_device               # 5b
from agent5_critic import critic_patch                      # 5d
from agent5_correlator import correlate                     # 5c

# v7 
from agent5_shared import dbg, write_audit, safe_json_loads
from agent5_shared import load_observed_commands, load_lexicon_candidates, normalize_platform, sanitize_show

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

def _normalize_show_cmds_fields(obj: dict, show_cmds: list[str] | None) -> dict:
    """
    Split LLM 'recommended_show_cmds' into:
      - trusted_commands: only cmds present in show_cmds.ini
      - unvalidated_cmds: everything else
    Does not modify prompts; only normalizes the parsed JSON.
    """
    ini = { (c or "").strip().lower() for c in (show_cmds or []) }
    recs = obj.get("recommended_show_cmds") or []

    trusted = []
    unval = []
    for c in recs:
        c_norm = (c or "").strip().lower()
        if c_norm in ini:
            trusted.append(c)
        else:
            unval.append(c)

    # Only set if not already provided by the model/critic
    if not obj.get("trusted_commands"):
        obj["trusted_commands"] = trusted
    if not obj.get("unvalidated_cmds"):
        obj["unvalidated_cmds"] = unval

    return obj
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
  8) If `ground_evidence_facts` contains a condition (e.g., interface CLNS=Down, BGP neighbor=Idle/Active), you MUST surface a corresponding finding with the evidence reference.

Output ONLY the JSON object.
Prefer recommending follow-up 'show' commands that are already present in show_cmds.ini; add at most 3 new 'show' commands only if clearly warranted by the findings. Never suggest config/debug/clear.
Do not mention devices other than the current hostname. If a signal is not evidenced in the log/context, exclude it.
"""

# ----- 5B. Cross-device system prompt -----
_CROSS_DEVICE_SYSTEM = """You are a senior NOC service lead.
You will receive a JSON array of per-device analyses (from other calls).
Correlate across devices to identify network-wide issues (e.g., EVPN VPWS down on both PEs, BGP session asymmetry, DF election pending, bundle down causing AC down, etc).

Strict rules:
- Do NOT invent device names.  You MUST only reference devices that appear in the input array. If a device or link name is not present in the input data, do NOT invent it. 
- 'trusted_followup_cmds' must be a subset of the union of devices' trusted_commands.
- If you include 'unvalidated_followup_cmds', they must be a subset of the union of devices' unvalidated_cmds.
- You must only report issues based upon information provided
- Active probes limited to ping/traceroute. No config/clear/debug.
- Keep output concise and actionable.
- If no clear cross-device issue exists, return empty lists for "top_incidents" and "remediation_themes".  

Return ONLY one JSON object:
{
  "task_status": "healthy" | "mixed" | "degraded" | "error" | "unknown",
  "top_incidents": [ {"scope":"pair|site|global","summary":"...","impact":"...","devices":["...","..."]} ],
  "remediation_themes": [ "..." ],
  "trusted_followup_cmds": [ "show ..." ],
  "unvalidated_followup_cmds": [ "show ..." ],
  "optional_active_probes": [ "ping ...", "traceroute ..." ]
}

Be conservative and avoid config changes; only suggest read-only checks and optional probes.
"""
# Prefer recommending follow-up 'show' commands that are already present in show_cmds.ini; add at most 3 new 'show' commands only if clearly warranted by the findings. Never suggest config/debug/clear.

def _build_per_device_messages(
    hostname: str,
    md_text: str,
    agent1_obj: dict | None,
    platform_hint: str,
    signals: set[str],
    allow_active: bool,
    show_cmds: list[str] | None = None,
    host_facts: dict | None = None     # v4 .. agent5_fact.json
) -> list[dict]:
    """Compose messages for per-device analysis."""
    # Pack context for the model (short + bounded)
    context = {
        "hostname": hostname,
        "platform_hint": platform_hint,
        "focus_signals": sorted(list(signals)),
        "allow_active_probes": bool(allow_active),
        "agent1_summary": agent1_obj or {},
        "show_cmds_ini": show_cmds or [],   # <— include the ini list
        "ground_evidence_facts": host_facts or {}   # v4

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

# def _call_llm(messages: list[dict], temperature: float = 0.0) -> str:
#     """Thin wrapper around your existing llm_api.call_llm."""
#     from llm_api import call_llm
#     return call_llm(messages, temperature=temperature)

def per_device_analyze_with_llm(
    hostname: str,
    md_text: str,
    agent1_obj: dict | None,
    platform_hint: str,
    signals: set[str],
    allow_active: bool,
    show_cmds: list[str] | None = None,
    host_facts: dict | None = None           # v4 ... to make sure info from agent5_facts.json is used
) -> dict:
    """Run the per-device LLM call and parse JSON with hardening."""
    msgs = _build_per_device_messages(
        hostname, md_text, agent1_obj, platform_hint, signals, allow_active,
        show_cmds=show_cmds,
        host_facts=host_facts
    )
    
    raw = call_llm(msgs, temperature=0.0) or ""

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
        if isinstance(obj, dict):
            dbg(f"[per-device] host={hostname} JSON parse OK keys={list(obj.keys())}")
            return obj
        # if isinstance(obj, dict):
        #     dbg(f"[per-device] host={hostname} JSON parse OK keys={list(obj.keys())}")
        #     obj = _normalize_show_cmds_fields(obj, show_cmds)
        #     return obj
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
            # if isinstance(obj, dict):
            #     obj = _normalize_show_cmds_fields(obj, show_cmds)
            #     return obj
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
    # obj = {
    #     "hostname": hostname,
    #     "platform": platform_hint or "unknown",
    #     "signals_seen": sorted(list(signals)),
    #     "status": "unknown",
    #     "findings": [{"signal": "meta", "severity": "info", "detail": "LLM response not strictly JSON"}],
    #     "recommended_show_cmds": [],
    #     "optional_active_cmds": []
    # }
    # obj = _normalize_show_cmds_fields(obj, show_cmds)
    # return obj

def cross_device_analyze_with_llm(per_device_objs: list[dict]) -> dict:
    """Run the cross-device LLM call and parse JSON with hardening."""
    msgs = _build_cross_device_messages(per_device_objs)
    raw = call_llm(msgs, temperature=0.0) or ""
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
        "trusted_followup_cmds": [],
        "unvalidated_followup_cmds": [],
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
    trusted_cmds = _truncate_list(summary.get("trusted_commands", []))
    unval_cmds   = _truncate_list(summary.get("unvalidated_cmds", []))
    probes       = _truncate_list(summary.get("optional_active_cmds", []))

    # NEW: list which trust sources actually contributed for this device
    src_used = ", ".join(summary.get("trusted_sources_used", [])) or "none"

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
        f"*Trusted commands* _(sources: {src_used})_:\n"
        + ("\n".join([f"• `{c}`" for c in trusted_cmds]) if trusted_cmds else "• (none)") + "\n"
        f"*Unvalidated commands* _(LLM ideas — **do not run**)_:\n"
        + ("\n".join([f"• `{c}`" for c in unval_cmds]) if unval_cmds else "• (none)") + "\n"
        f"*Optional probes:*\n"
        + ("\n".join([f"• `{p}`" for p in probes]) if probes else "• (none)")
    )


    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

def _build_cross_device_block(agg: dict, config_dir: str, task_dir: str) -> list:
    status = agg.get("task_status", "unknown")
    incidents = agg.get("top_incidents", []) or []
    themes = agg.get("remediation_themes", []) or []

    trusted_shows = _truncate_list(agg.get("trusted_followup_cmds", []))
    unval_shows   = _truncate_list(agg.get("unvalidated_followup_cmds", []))
    probes        = _truncate_list(agg.get("optional_active_probes", []))

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
                "text": "*Follow-up (trusted) commands:*\n" +
                        ("\n".join([f"• `{c}`" for c in trusted_shows]) if trusted_shows else "• (none)")}},
        {"type": "section",
        "text": {"type": "mrkdwn",
                "text": "*Follow-up (unvalidated) commands:*\n" +
                        ("\n".join([f"• `{c}`" for c in unval_shows]) if unval_shows else "• (none)")}},
                        
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

# ---------- 
# v4
def _reconcile_findings_with_facts(obj: dict, host_facts: dict | None) -> dict:
    """
    Generic, schema-driven safety net:
    - If facts say an ISIS interface is down and the LLM forgot to report it,
      add a finding.
    - If facts say a BGP neighbor is not Established/Up and the LLM forgot,
      add a finding.
    No protocol-specific parsing of raw text here; we only use structured 'facts'.
    """
    if not host_facts or not isinstance(host_facts, dict):
        return obj

    findings = obj.get("findings") or []
    # Build a lowercase bag to avoid near-duplicate lines
    seen_blob = (json.dumps(findings) if findings else "").lower()

    # Facts are expected under host_facts["facts"]
    facts = host_facts.get("facts") or {}

    # 1) ISIS interface health evidence
    for iface in (facts.get("isis_interfaces") or []):
        clns = str(iface.get("clns", "")).lower()
        all_ok = str(iface.get("all_ok", "")).lower()
        if clns == "down" or all_ok == "no":
            detail = (
                f"ISIS interface {iface.get('interface','?')} shows "
                f"CLNS={iface.get('clns','?')} (all_ok={iface.get('all_ok','?')})."
            )
            if detail.lower() not in seen_blob:
                findings.append({"signal": "isis", "severity": "error", "detail": detail})

    # 2) BGP neighbor health evidence
    for n in (facts.get("bgp_neighbors") or []):
        state = str(n.get("state", "")).lower()
        if state and state not in ("established", "up"):
            detail = f"BGP neighbor {n.get('neighbor') or n.get('peer') or '?'} state={n.get('state','?')}."
            if detail.lower() not in seen_blob:
                findings.append({"signal": "bgp", "severity": "error", "detail": detail})

    if findings:
        obj["findings"] = findings
        # Upgrade status conservatively if we added an error and status looked too optimistic
        cur = (obj.get("status") or "unknown").lower()
        if any(f.get("severity") == "error" for f in findings) and cur in ("healthy", "unknown"):
            obj["status"] = "degraded"

    return obj

# v7 ---- use already trusted commands (based upon lexicon/observed: show_cmds.ini & .md )----

def _primary_keyword(cmd: str) -> str:
    """
    Extract a protocol/topic keyword from a 'show ...' command, skipping
    common qualifiers like ip/ipv4/ipv6. This avoids hard-coding command
    variants and works across XR/IOS flavors.
    """
    toks = re.split(r"\s+", (cmd or "").strip().lower())
    drop = {"show", "ip", "ipv4", "ipv6"}
    toks = [t for t in toks if t and t not in drop]
    return toks[0] if toks else ""

# def _split_trusted_unvalidated(
#     obj: dict,
#     host_facts: dict | None,
#     md_text: str,
#     show_cmds: list[str] | None,
# ) -> dict:
#     """
#     Promote trusted vs unvalidated:

#       • trusted = union of:
#           - facts['trusted_show_only']                (facts layer: observed/lexicon/INI)
#           - commands observed in the Markdown log     (Agent-5 log evidence)
#           - commands listed in show_cmds.ini          (task-scope allowlist)
#         PLUS topic-aware fallback: if the LLM show shares the same primary keyword
#         (e.g., 'bgp', 'bfd') with any trusted command, trust it.

#       • unvalidated = recommended_show_cmds minus trusted
#     """
#     if not isinstance(obj, dict):
#         return obj

#     recs = obj.get("recommended_show_cmds") or []
#     if not isinstance(recs, list) or not recs:
#         obj.setdefault("trusted_commands", [])
#         obj.setdefault("unvalidated_cmds", [])
#         return obj

#     # 1) exact-trusted baseline from facts/md/ini
#     trusted_norm: set[str] = set()

#     if isinstance(host_facts, dict):
#         fx = host_facts.get("facts") or {}
#         for c in (fx.get("trusted_show_only") or []):
#             cc = (c or "").strip().lower()
#             if cc:
#                 trusted_norm.add(cc)

#     observed_in_md: set[str] = set()
#     if md_text:
#         for line in md_text.splitlines():
#             ln = line.strip()
#             if ln.lower().startswith("show "):
#                 observed_in_md.add(ln.lower())
#     trusted_norm |= observed_in_md

#     for c in (show_cmds or []):
#         cc = (c or "").strip().lower()
#         if cc:
#             trusted_norm.add(cc)

#     # 2) topic keys derived from trusted sources (for fuzzy promotion)
#     trusted_topics: set[str] = set(_primary_keyword(c) for c in trusted_norm if c)

#     # 3) Partition the LLM list (preserve original order/case)
#     trusted_out: list[str] = []
#     unvalidated_out: list[str] = []
#     for c in recs:
#         cn = (c or "").strip()
#         if not cn:
#             continue
#         lc = cn.lower()

#         # Exact match wins
#         if lc in trusted_norm:
#             trusted_out.append(cn)
#             continue

#         # Topic-aware fallback: trust if primary keyword matches any trusted topic
#         if lc.startswith("show ") and _primary_keyword(lc) in trusted_topics:
#             trusted_out.append(cn)
#         else:
#             unvalidated_out.append(cn)

#     obj["trusted_commands"] = trusted_out
#     obj["unvalidated_cmds"] = unvalidated_out
#     obj.pop("recommended_show_cmds", None)
#     return obj

# def _split_trusted_unvalidated(
#     obj: dict,
#     host_facts: dict | None,
#     md_text: str,
#     show_cmds: list[str] | None,
# ) -> dict:
#     """
#     EXACT-MATCH ONLY:
#       trusted = union of
#         - facts['trusted_show_only']         (facts layer: observed/lexicon/INI if provided there)
#         - commands observed in the Markdown
#         - commands listed in show_cmds.ini
#         - facts['lexicon_show_only'] (if present)   # explicit lexicon, optional

#       unvalidated = every recommended_show_cmd not in trusted (exact, case-insensitive).
#     """
#     if not isinstance(obj, dict):
#         return obj

#     recs = obj.get("recommended_show_cmds") or []
#     if not isinstance(recs, list) or not recs:
#         obj.setdefault("trusted_commands", [])
#         obj.setdefault("unvalidated_cmds", [])
#         return obj

#     # Build exact-match allowlist (normalized to lowercase)
#     trusted_norm: set[str] = set()

#     fx = {}
#     if isinstance(host_facts, dict):
#         fx = host_facts.get("facts") or {}
#         for c in (fx.get("trusted_show_only") or []):
#             cc = (c or "").strip().lower()
#             if cc:
#                 trusted_norm.add(cc)
#         # Optional explicit lexicon if your facts writer exposes it
#         for c in (fx.get("lexicon_show_only") or []):
#             cc = (c or "").strip().lower()
#             if cc:
#                 trusted_norm.add(cc)

#     # Observed in the device Markdown (.md)
#     if md_text:
#         for line in md_text.splitlines():
#             ln = line.strip()
#             if ln.lower().startswith("show "):
#                 trusted_norm.add(ln.lower())

#     # From show_cmds.ini
#     for c in (show_cmds or []):
#         cc = (c or "").strip().lower()
#         if cc:
#             trusted_norm.add(cc)

#     # Partition LLM recommendations
#     trusted_out: list[str] = []
#     unvalidated_out: list[str] = []
#     for c in recs:
#         cn = (c or "").strip()
#         if not cn:
#             continue
#         (trusted_out if cn.lower() in trusted_norm else unvalidated_out).append(cn)

#     obj["trusted_commands"] = trusted_out
#     obj["unvalidated_cmds"] = unvalidated_out
#     obj.pop("recommended_show_cmds", None)
#     return obj


# def _split_trusted_unvalidated_debug(
#     obj: dict,
#     host_facts: dict | None,
#     md_text: str,
#     show_cmds: list[str] | None,
# ) -> dict:
#     """
#     (DEBUG ENABLED)
#     Partitions LLM-recommended commands into 'trusted' and 'unvalidated' lists.
#     This version includes extensive print statements to trace the inputs and logic.
#     """
#     hostname = obj.get("hostname", "Unknown Host")
#     print(f"\n--- DEBUG: Starting Trust Validation for [{hostname}] ---")

#     # --- Step 1: Print all inputs received by the function ---
#     recommended_cmds = obj.get("recommended_show_cmds") or []
#     print(f"[INPUT] LLM Recommended Commands: {recommended_cmds}")

#     trusted_all_from_facts = host_facts.get("trusted_all", []) if isinstance(host_facts, dict) else []
#     print(f"[INPUT] `trusted_all` from facts.json: {trusted_all_from_facts}")
    
#     print(f"[INPUT] `show_cmds` from show_cmds.ini: {show_cmds}")

#     # --- Step 2: Build the trusted set and show its construction step-by-step ---
#     trusted_command_set: set[str] = set()
#     print(f"[BUILD] Initial trusted set: {trusted_command_set}")

#     # Source 1: `trusted_all` from facts
#     if trusted_all_from_facts:
#         for cmd in trusted_all_from_facts:
#             if cmd and isinstance(cmd, str):
#                 trusted_command_set.add(cmd.strip().lower())
#     print(f"[BUILD] After adding `trusted_all`: {trusted_command_set}")

#     # Source 2: `show_cmds` from .ini
#     if show_cmds:
#         for cmd in show_cmds:
#             if cmd and isinstance(cmd, str):
#                 trusted_command_set.add(cmd.strip().lower())
#     print(f"[BUILD] After adding `show_cmds.ini`: {trusted_command_set}")

#     # Source 3: Commands from the markdown log
#     md_cmds_found = []
#     if md_text:
#         for line in md_text.splitlines():
#             cleaned_line = line.strip()
#             if cleaned_line.lower().startswith("show "):
#                 trusted_command_set.add(cleaned_line.lower())
#                 md_cmds_found.append(cleaned_line)
#     print(f"[INPUT] Commands found in .md log: {md_cmds_found}")
#     print(f"[BUILD] FINAL trusted command set for matching: {trusted_command_set}")

#     # --- Step 3: Iterate and decide on each command, printing the logic ---
#     print("\n[DECISION LOGIC] Checking each recommended command...")
#     trusted_output: list[str] = []
#     unvalidated_output: list[str] = []

#     for cmd in recommended_cmds:
#         cleaned_cmd = (cmd or "").strip()
#         if not cleaned_cmd:
#             continue
        
#         is_trusted = cleaned_cmd.lower() in trusted_command_set
#         print(f"  - Checking: '{cleaned_cmd.lower()}' -> In trusted set? {is_trusted}")
#         if is_trusted:
#             trusted_output.append(cleaned_cmd)
#         else:
#             unvalidated_output.append(cleaned_cmd)

#     # --- Step 4: Print the final result before returning ---
#     print("\n[RESULT] Final partitioned lists:")
#     print(f"  - Trusted Commands: {trusted_output}")
#     print(f"  - Unvalidated Commands: {unvalidated_output}")
#     print(f"--- DEBUG: Finished Trust Validation for [{hostname}] ---\n")

#     # Update the object with the final lists
#     obj["trusted_commands"] = trusted_output
#     obj["unvalidated_cmds"] = unvalidated_output
#     obj.pop("recommended_show_cmds", None)
    
#     return obj

# def _split_trusted_unvalidated_new_logic(
#     obj: dict,
#     host_facts: dict | None,
#     md_text: str,
#     show_cmds: list[str] | None,  # IGNORED per new requirements
# ) -> dict:
#     """
#     NEW LOGIC (per requirements):
#     * **Trusted = (observed-in-.md and output looks successful) ∪ (platform lexicon allow-list).**
#     * **Untrusted = everything else** (LLM/Agent-1 suggestions that don't match the above).
#     * **Ignore show_cmds.ini** and **ignore facts-based trust** for this decision.
#     """
#     hostname = obj.get("hostname", "Unknown Host")
#     print(f"\n--- DEBUG: NEW LOGIC Trust Validation for [{hostname}] ---")

#     recommended_cmds = obj.get("recommended_show_cmds") or []
#     print(f"[INPUT] LLM Recommended Commands: {recommended_cmds}")

#     # --- Step 1: Build trusted set from ONLY the allowed sources ---
#     trusted_command_set: set[str] = set()
#     print(f"[BUILD] Initial trusted set: {trusted_command_set}")

#     # Source 1: Commands observed in .md that look successful
#     observed_successful_cmds = []
#     if md_text:
#         lines = md_text.splitlines()
#         for i, line in enumerate(lines):
#             cleaned_line = line.strip()
#             if cleaned_line.lower().startswith("show "):
#                 # Check if this command appears to have executed successfully
#                 # Look for typical success indicators in following lines
#                 success_indicators = []
#                 error_indicators = []
                
#                 # Look ahead a few lines for success/error patterns
#                 for j in range(i+1, min(i+10, len(lines))):
#                     next_line = lines[j].strip().lower()
#                     if not next_line:
#                         continue
                    
#                     # Success indicators
#                     if any(pattern in next_line for pattern in [
#                         "neighbor", "established", "interface", "bgp", "isis", "ospf",
#                         "up", "active", "learned", "reachable", "state:", "status:"
#                     ]):
#                         success_indicators.append(next_line[:50])
                    
#                     # Error indicators
#                     if any(pattern in next_line for pattern in [
#                         "% invalid", "% incomplete", "% error", "% unknown", 
#                         "command not found", "syntax error"
#                     ]):
#                         error_indicators.append(next_line[:50])
                    
#                     # Stop looking if we hit another command
#                     if next_line.startswith("show ") or next_line.endswith("#"):
#                         break
                
#                 # Determine if successful (has output without errors)
#                 if success_indicators and not error_indicators:
#                     observed_successful_cmds.append(cleaned_line)
#                     trusted_command_set.add(cleaned_line.lower())
#                     print(f"[BUILD] Added observed successful: '{cleaned_line}' (indicators: {success_indicators[:2]})")
#                 elif not success_indicators and not error_indicators:
#                     # No clear indicators, assume successful if no errors
#                     observed_successful_cmds.append(cleaned_line)
#                     trusted_command_set.add(cleaned_line.lower())
#                     print(f"[BUILD] Added observed (no errors): '{cleaned_line}'")
#                 else:
#                     print(f"[BUILD] Skipped observed (errors found): '{cleaned_line}' (errors: {error_indicators[:1]})")

#     print(f"[INPUT] Observed successful commands in .md: {observed_successful_cmds}")
#     print(f"[BUILD] After adding observed successful: {trusted_command_set}")

#     # Source 2: Platform lexicon allow-list
#     platform_lexicon_cmds = []
#     if isinstance(host_facts, dict):
#         # Get platform hint to determine which lexicon to use
#         platform_hint = host_facts.get("platform_hint", "unknown")
        
#         # Load platform-specific lexicon (this would need to be implemented)
#         # For now, we'll use ideas_from_lexicon if available in host_facts
#         lexicon_cmds = host_facts.get("ideas_from_lexicon", [])
#         platform_lexicon_cmds = lexicon_cmds
        
#         for cmd in platform_lexicon_cmds:
#             if cmd and isinstance(cmd, str):
#                 trusted_command_set.add(cmd.strip().lower())
    
#     print(f"[INPUT] Platform lexicon commands: {platform_lexicon_cmds}")
#     print(f"[BUILD] After adding platform lexicon: {trusted_command_set}")

#     # EXPLICITLY IGNORE these sources per new requirements:
#     print(f"[IGNORED] show_cmds.ini (per new logic): {show_cmds}")
#     print(f"[IGNORED] facts-based trust like trusted_all (per new logic)")

#     print(f"[BUILD] FINAL trusted command set for matching: {trusted_command_set}")

#     # --- Step 3: Partition the LLM recommendations ---
#     print("\n[DECISION LOGIC] Checking each recommended command...")
#     trusted_output: list[str] = []
#     unvalidated_output: list[str] = []

#     for cmd in recommended_cmds:
#         cleaned_cmd = (cmd or "").strip()
#         if not cleaned_cmd:
#             continue
        
#         is_trusted = cleaned_cmd.lower() in trusted_command_set
#         print(f"  - Checking: '{cleaned_cmd}' -> In trusted set? {is_trusted}")
        
#         if is_trusted:
#             trusted_output.append(cleaned_cmd)
#             print(f"    -> TRUSTED: Added to trusted list")
#         else:
#             unvalidated_output.append(cleaned_cmd)
#             print(f"    -> UNVALIDATED: Added to unvalidated list")

#     # --- Step 4: Print summary and update object ---
#     print("\n[RESULT] Final partitioned lists:")
#     print(f"  - Trusted Commands: {trusted_output}")
#     print(f"  - Unvalidated Commands: {unvalidated_output}")
#     print(f"--- DEBUG: Finished NEW LOGIC Trust Validation for [{hostname}] ---\n")

#     # Update the object with the final lists
#     obj["trusted_commands"] = trusted_output
#     obj["unvalidated_cmds"] = unvalidated_output
#     obj.pop("recommended_show_cmds", None)
    
#     return obj


def _extract_observed_successful_commands(md_text: str, platform_hint: str) -> list[str]:
    if not md_text:
        return []
    plat = normalize_platform(platform_hint)
    lines = md_text.splitlines()
    ok: list[str] = []

    # simple fence scanning: look for code blocks after a "## show ..."
    i = 0
    while i < len(lines):
        hdr = lines[i].strip()
        if re.match(r"^##\s+show\s+", hdr, re.IGNORECASE):
            # find next code fence
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                j += 1
            if j >= len(lines):
                i += 1
                continue
            j += 1  # enter block
            block = []
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                block.append(lines[j])
                j += 1
            # analyze first non-empty line as echoed command
            k = 0
            while k < len(block) and not block[k].strip():
                k += 1
            if k >= len(block):
                i = j + 1
                continue

            echoed = block[k].strip()
            clean = sanitize_show(echoed, plat)
            if not clean:
                i = j + 1
                continue

            body = block[k+1:]
            block_text = "\n".join(body)

            # error markers
            if re.search(r"%(?:\s*Invalid input detected|\s*Incomplete command|\s*Ambiguous command|\s*Error)", block_text, re.IGNORECASE):
                i = j + 1
                continue
            if re.search(r"(?:Unknown|Unrecognized)\s+command|syntax error|Command not supported", block_text, re.IGNORECASE):
                i = j + 1
                continue

            # consider substantive if any non-prompt/non-timestamp non-empty line exists
            def _is_prompt(s: str) -> bool:
                s = s.strip()
                return bool(re.match(r"^(?:RP/\d+/\w+\d+/CPU\d+:|[A-Za-z0-9._-]+(?:\([^)]+\))?[#>])\s*$", s))
            def _is_ts(s: str) -> bool:
                return bool(re.match(r"^\w{3}\s\w{3}\s+\d{1,2}\s", s.strip()))

            meaningful = [l for l in body if l.strip() and not _is_prompt(l) and not _is_ts(l)]
            if meaningful:
                ok.append(clean)

        i += 1

    # audit
    try:
        if AUDIT_ROOT:
            os.makedirs(os.path.join(AUDIT_ROOT, "observed"), exist_ok=True)
            write_audit(os.path.join(AUDIT_ROOT, "observed", "trusted_from_md.txt"),
                        "\n".join(sorted(set(s.lower() for s in ok))))
    except Exception as e:
        dbg(f"[audit] failed writing trusted_from_md.txt: {e}")

    return ok


# def _load_platform_lexicon_allowlist(platform_hint: str) -> list[str]:
#     """
#     Load platform-specific lexicon allowlist.
#     This should load from your lexicon files based on platform.
#     For now, returns a basic set of common commands per platform.
#     """
#     platform = normalize_platform(platform_hint)
    
#     # You would replace this with actual file loading from your lexicon
#     if platform == "cisco-ios-xr":
#         return [
#             "show bgp summary",
#             "show bgp ipv4 unicast summary", 
#             "show bgp ipv6 unicast summary",
#             "show bgp neighbor",
#             "show bfd session",
#             "show bfd neighbors",
#             "show isis neighbors",
#             "show mpls ldp neighbors",
#             "show interface brief",
#             "show running-config router bgp"
#         ]
#     elif platform == "cisco-ios":
#         return [
#             "show ip bgp summary",
#             "show ip bgp neighbors", 
#             "show ip route",
#             "show interface brief",
#             "show running-config | section bgp"
#         ]
#     else:
#         return []


# Published per-platform allow-list:
#   /_agent_knowledge/lexicon/_allow/<platform>.txt
# Lines must be commands; each is sanitized per-platform and only 'show ...' survives.
def _load_platform_allowlist_from_disk(platform_hint: str) -> set[str]:
    from agent5_shared import LEXICON_ROOT  # already defined in agent5_shared
    plat = normalize_platform(platform_hint)
    allow_path = os.path.join(LEXICON_ROOT, "_allow", f"{plat}.txt")
    allowed: set[str] = set()
    raw = []

    try:
        if os.path.exists(allow_path):
            with open(allow_path, "r", encoding="utf-8") as fh:
                raw = [l.strip() for l in fh if l.strip() and not l.strip().startswith("#")]
    except Exception as e:
        dbg(f"[trust][lexicon] failed to read {allow_path}: {e}")

    for line in raw:
        clean = sanitize_show(line, plat)
        if clean:
            allowed.add(clean.lower())

    dbg(f"[trust][lexicon] platform={plat} path={allow_path} accepted={len(allowed)} raw={len(raw)}")

    # audit
    try:
        if AUDIT_ROOT:
            os.makedirs(os.path.join(AUDIT_ROOT, "trust"), exist_ok=True)
            write_audit(os.path.join(AUDIT_ROOT, "trust", "trusted_from_lexicon.txt"),
                        "\n".join(sorted(allowed)))
    except Exception as e:
        dbg(f"[audit] failed writing trusted_from_lexicon.txt: {e}")

    return allowed

# Alternative implementation that uses your existing lexicon loading
def _split_trusted_unvalidated_corrected(
    obj: dict,
    host_facts: dict | None,
    md_text: str,
    show_cmds: list[str] | None,  # ignored by design
) -> dict:
    hostname = obj.get("hostname", "Unknown Host")
    plat_hint = obj.get("platform") or (host_facts.get("platform_hint") if isinstance(host_facts, dict) else "unknown")

    # 1) Build sources
    observed_ok = set(s.lower() for s in _extract_observed_successful_commands(md_text, plat_hint))
    lex_ok      = _load_platform_allowlist_from_disk(plat_hint)

    pool = observed_ok | lex_ok
    src_map = {
        "md_success": observed_ok,
        "lexicon_published": lex_ok,
    }

    # 2) Partition with reasons
    recs = obj.get("recommended_show_cmds") or []
    trusted_out, unval_out = [], []
    used_sources = set()
    trace_lines = []

    for r in recs:
        raw = (r or "").strip()
        if not raw:
            continue
        clean = sanitize_show(raw, plat_hint)
        reasons = []
        if clean:
            cl = clean.lower()
            for label, s in src_map.items():
                if cl in s:
                    reasons.append(label)
                    used_sources.add(label)
        decision = "TRUSTED" if reasons else "UNVALIDATED"
        (trusted_out if decision == "TRUSTED" else unval_out).append(raw)
        trace_lines.append(json.dumps({
            "host": hostname,
            "platform": plat_hint,
            "input_cmd": raw,
            "sanitized": clean,
            "decision": decision,
            "reasons": reasons
        }))

    obj["trusted_commands"] = trusted_out
    obj["unvalidated_cmds"] = unval_out
    obj["trusted_sources_used"] = sorted(used_sources)
    obj.pop("recommended_show_cmds", None)

    dbg(f"[trust][{hostname}] md_ok={len(observed_ok)} lex_ok={len(lex_ok)} recs={len(recs)} → trusted={len(trusted_out)} unval={len(unval_out)} sources_used={obj['trusted_sources_used']}")

    # 3) Write per-host trace
    try:
        if AUDIT_ROOT:
            os.makedirs(os.path.join(AUDIT_ROOT, "trust"), exist_ok=True)
            write_audit(os.path.join(AUDIT_ROOT, "trust", f"trace_{hostname}.ndjson"), "\n".join(trace_lines))
    except Exception as e:
        dbg(f"[audit] failed to write trace for {hostname}: {e}")

    return obj

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

    # Load observed & lexicon once for the task
    observed_cmds_task = load_observed_commands(config_dir, task_dir)

    for host, md_text in md_pairs:
        platform_hint = _infer_platform_hint_from_md(md_text)
        signals = _default_signals()
        dbg(f"[facts] extracting facts for host={host}")

        # Phase-1: feed observed + lexicon candidates into facts
        plat_norm = normalize_platform(platform_hint)
        lex_cands = load_lexicon_candidates(plat_norm)

        facts_obj = extract_facts_for_device(
            hostname=host,
            md_text=md_text,
            platform_hint=platform_hint,
            focus_signals=sorted(list(signals)),
            # call_llm_fn=None,                 # Phase-1 facts are regex/aggregation only
            call_llm_fn=call_llm,
            audit_dir=facts_dir,
            agent1_obj=_find_agent1_for_host(agent1, host) if isinstance(agent1, list) else None,
            observed_cmds=observed_cmds_task,
            lexicon_candidates=lex_cands,
        )
        facts_bundle.append(facts_obj)

    #  v4 - Build quick lookup by hostname for reconciliation
    facts_index = {f.get("hostname"): f for f in facts_bundle if isinstance(f, dict)}

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

        # # Reasoner → Critic path
        # obj = reason_per_device(
        #     hostname=host,
        #     facts=facts_index.get(host) or {},
        #     agent1_for_host=_find_agent1_for_host(agent1, host) if isinstance(agent1, list) else None,
        #     call_llm_fn=call_llm,
        #     audit_dir=AUDIT_ROOT,
        # )

        # obj = per_device_analyze_with_llm(
        #     hostname=host,
        #     md_text=md_text,   # <— THIS is the critical piece: send the Markdown log
        #     agent1_obj=_find_agent1_for_host(agent1, host) if isinstance(agent1, list) else None,
        #     platform_hint=_infer_platform_hint_from_md(md_text),
        #     signals=signals,
        #     allow_active=False,
        #     show_cmds=show_cmds,
        #     host_facts=facts_index.get(host)
        # )
        # # Schema-driven safety patch
        # obj = critic_patch(obj, facts_index.get(host), AUDIT_ROOT)

        obj = per_device_analyze_with_llm(
            hostname=host,
            md_text=md_text,
            agent1_obj=_find_agent1_for_host(agent1, host) if isinstance(agent1, list) else None,
            platform_hint=_infer_platform_hint_from_md(md_text),
            signals=signals,
            allow_active=False,
            show_cmds=show_cmds,
            host_facts=facts_index.get(host)
        )

        # NEW: map recommended_show_cmds → trusted_commands vs unvalidated_cmds using *facts only*
        # obj = _split_trusted_unvalidated(obj, facts_index.get(host))
        # obj = _split_trusted_unvalidated(obj, facts_index.get(host), md_text, show_cmds)
        # DEBUG version
        # obj = _split_trusted_unvalidated_debug(obj, facts_index.get(host), md_text, show_cmds)

        obj = _split_trusted_unvalidated_corrected(obj, facts_index.get(host), md_text, show_cmds)

        # Schema-driven safety patch
        obj = critic_patch(obj, facts_index.get(host), AUDIT_ROOT)

        # # ---- Map LLM's 'recommended_show_cmds' to UI fields (trusted vs unvalidated)
        # recs = obj.get("recommended_show_cmds") or []
        # # trust = anything that appears in show_cmds.ini for this task
        # trust_set = set(show_cmds or [])
        # trusted_from_recs = [c for c in recs if c in trust_set]
        # unvalidated_from_recs = [c for c in recs if c not in trust_set]
        # # If the model already returned these fields, merge (de-dup) conservatively.
        # obj["trusted_commands"] = sorted(set((obj.get("trusted_commands") or []) + trusted_from_recs))
        # obj["unvalidated_cmds"] = sorted(set((obj.get("unvalidated_cmds") or []) + unvalidated_from_recs))

        dbg(f"[per-device][reconcile] host={host} -> findings={len(obj.get('findings') or [])} status={obj.get('status')}")

        # Short result log with new keys
        dbg(f"[per-device][result] host={host} status={obj.get('status','?')} "
            f"platform={obj.get('platform','?')} "
            f"findings={len(obj.get('findings') or [])} "
            f"trusted={len(obj.get('trusted_commands') or [])} "
            f"unvalidated={len(obj.get('unvalidated_cmds') or [])}")

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
