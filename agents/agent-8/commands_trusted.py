# agents/agent-8/commands_trusted.py
# Simple helpers to manage trusted show commands
# YAML format: vendor -> platform -> tech -> [commands]

import os
import yaml
from typing import List, Optional, Union

# Use absolute path inside the containers (override with COMMANDS_TRUSTED_PATH if needed)
DEFAULT_PATH = os.getenv(
    "COMMANDS_TRUSTED_PATH",
    "/app/shared/_agent_knowledge/commands_trusted.yaml",
).strip()

# ---------------------------------------------------
# Canonical tech buckets (single source of truth)
# ---------------------------------------------------
TECH_BUCKETS = (
    "bgp",
    "ospf",
    "isis",
    "mpls",
    "interfaces",
    "routing",
    "misc",
)

# -------- basic normalization helpers --------
def normalize_command(cmd: str) -> str:
    """lowercase and collapse spaces"""
    return " ".join((cmd or "").strip().lower().split())

def norm_vendor(v: Optional[str]) -> str:
    v = (v or "").strip().lower()
    return "cisco" if v in ("cisco", "cisco-systems") else v

def norm_platform(p: Optional[str]) -> str:
    p = (p or "").strip().lower().replace("_", "").replace("-", "")
    if p in ("ios", "iosxe", "iosxenative"):
        return "iosxe"
    if p in ("iosxr", "iosxrv"):
        return "iosxr"
    if p in ("nxos",):
        return "nxos"
    return p

# def norm_tech(t: Union[str, List[str], None]) -> str:
#     if isinstance(t, list) and t:
#         t = t[0]
#     t = (t or "misc")
#     t = str(t).strip().lower()
#     return t or "misc"

def norm_tech(t: Union[str, List[str], None]) -> str:
    """
    Normalize a hinted tech value into one of TECH_BUCKETS, else 'misc'.
    NOTE: This does NOT inspect the command text (use choose_tech for that).
    """
    if isinstance(t, list) and t:
        t = t[0]
    t = (t or "misc")
    t = str(t).strip().lower()
    return t if t in TECH_BUCKETS else "misc"

# ---------------------------------------------------
# Light-weight command → tech classification
# (No regex; just a few obvious substrings)
# ---------------------------------------------------
def classify_tech(cmd: str) -> str:
    """
    Given a CLI command string (e.g., 'show ip bgp summary'),
    return the best-fit bucket from TECH_BUCKETS.
    Very simple substring checks; easy to maintain.
    """
    c = " " + normalize_command(cmd) + " "  # pad to avoid partial-word confusion

    # BGP
    if " bgp " in c or " show bgp" in c or " show ip bgp" in c:
        return "bgp"

    # OSPF
    if " ospf " in c or " show ip ospf" in c or " show ospf" in c:
        return "ospf"

    # ISIS
    if " isis " in c or " show isis" in c:
        return "isis"

    # MPLS / LDP
    if " mpls " in c or " ldp " in c or " show mpls" in c:
        return "mpls"

    # Interfaces
    if " interface " in c or " interfaces " in c or " show ip interface brief" in c or " show interfaces" in c:
        return "interfaces"

    # Routing / RIB
    if " route " in c or " show ip route" in c or " show route" in c:
        return "routing"

    return "misc"

def choose_tech(cmd: str, hinted_tech: Union[str, List[str], None] = None) -> str:
    """
    Resolve a final tech bucket for a command:
    1) if hinted_tech is valid (in TECH_BUCKETS), use it;
    2) otherwise classify from the command string;
    3) fallback to 'misc'.
    """
    hinted = norm_tech(hinted_tech)
    if hinted in TECH_BUCKETS and hinted != "misc":
        return hinted
    return classify_tech(cmd) or "misc"

# -------- YAML I/O --------
def load_trusted(path: str = DEFAULT_PATH) -> dict:
    """Load the trusted commands YAML into a Python dict."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}

def save_trusted(data: dict, path: str = DEFAULT_PATH) -> None:
    """Save the trusted commands dict back into the YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=True, allow_unicode=True)


# -------- queries --------
def get_trusted(vendor: str, platform: str, tech: Union[str, List[str]],
                path: str = DEFAULT_PATH) -> list:
    """Return list of trusted commands for vendor/platform/tech."""
    v = norm_vendor(vendor)
    p = norm_platform(platform)
    t = norm_tech(tech)
    data = load_trusted(path)
    return list(data.get(v, {}).get(p, {}).get(t, []) or [])

def is_trusted(cmd: str, vendor: str, platform: str,
               path: str = DEFAULT_PATH) -> bool:
    """
    True if cmd exists under ANY tech for vendor/platform. False otherwise.
    (Boolean return — safe in if-statements.)
    """
    v = norm_vendor(vendor)
    p = norm_platform(platform)
    needle = normalize_command(cmd)
    data = load_trusted(path)
    buckets = data.get(v, {}).get(p, {}) or {}
    for cmds in buckets.values():
        for c in (cmds or []):
            if normalize_command(c) == needle:
                print(f"[DEBUG:is_trusted] vendor={v}, platform={p}, cmd={needle} → returning True", flush=True)
                return True
    print(f"[DEBUG:is_trusted] vendor={v}, platform={p}, cmd={needle} → returning False", flush=True)
    return False

# -------- mutations --------
def promote(cmd: str, vendor: str, platform: str, tech: Union[str, List[str], None],
            path: str = DEFAULT_PATH) -> None:
    """
    Add a command to the trusted list if not already present.
    Accepts tech as str/list/None. Creates buckets if missing.
    Tech is resolved centrally via choose_tech() to keep consistency.
    """
    v = norm_vendor(vendor)
    p = norm_platform(platform)

    # resolve tech using our single source of truth
    t = choose_tech(cmd, hinted_tech=tech)

    cmd_clean = cmd.strip()
    needle = normalize_command(cmd_clean)

    data = load_trusted(path)
    data.setdefault(v, {}).setdefault(p, {}).setdefault(t, [])

    # Avoid duplicates
    existing = data[v][p][t] or []
    if not any(normalize_command(c) == needle for c in existing):
        existing.append(cmd_clean)
        data[v][p][t] = existing

    save_trusted(data, path)