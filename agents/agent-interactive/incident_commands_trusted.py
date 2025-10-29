"""
agents/agent-interactive/incident_commands_trusted.py
------------------------------------------------------
Copied and adapted from agents/agent-8/commands_trusted.py

Purpose:
Manages trusted read-only 'show' commands for the Incident-Agent (Phase-2).
Stores and retrieves trusted commands from an isolated YAML database under:
    /app/shared/_incident_knowledge/commands_trusted.yaml

This prevents any overlap with Agent-8’s _agent_knowledge data.

YAML schema:
vendor -> platform -> tech -> [commands]
"""

import os
import yaml
from typing import List, Optional, Union

# --------------------------------------------------------------------
# Use absolute path inside containers (isolated for Incident-Agent)
# --------------------------------------------------------------------
DEFAULT_PATH = os.getenv(
    "COMMANDS_TRUSTED_PATH",
    "/app/shared/_incident_knowledge/commands_trusted.yaml",
).strip()

# --------------------------------------------------------------------
# Canonical tech buckets (single source of truth)
# --------------------------------------------------------------------
TECH_BUCKETS = (
    "bgp",
    "ospf",
    "isis",
    "mpls",
    "interfaces",
    "routing",
    "misc",
)

# --------------------------------------------------------------------
# Basic normalization helpers
# --------------------------------------------------------------------
def normalize_command(cmd: str) -> str:
    """Lowercase and collapse spaces in a command string."""
    return " ".join((cmd or "").strip().lower().split())

def norm_vendor(v: Optional[str]) -> str:
    """Normalize vendor field."""
    v = (v or "").strip().lower()
    return "cisco" if v in ("cisco", "cisco-systems") else v

def norm_platform(p: Optional[str]) -> str:
    """Normalize platform field."""
    p = (p or "").strip().lower().replace("_", "").replace("-", "")
    if p in ("ios", "iosxe", "iosxenative"):
        return "iosxe"
    if p in ("iosxr", "iosxrv"):
        return "iosxr"
    if p in ("nxos",):
        return "nxos"
    return p

def norm_tech(t: Union[str, List[str], None]) -> str:
    """
    Normalize a hinted tech value into one of TECH_BUCKETS.
    If nothing matches, return 'misc'.
    NOTE: This does NOT inspect the command text (use choose_tech for that).
    """
    if isinstance(t, list) and t:
        t = t[0]
    t = (t or "misc")
    t = str(t).strip().lower()
    return t if t in TECH_BUCKETS else "misc"

# --------------------------------------------------------------------
# Light-weight command → tech classification
# --------------------------------------------------------------------
def classify_tech(cmd: str) -> str:
    """
    Given a CLI command string (e.g., 'show ip bgp summary'),
    return the best-fit bucket from TECH_BUCKETS.
    Simple substring checks; no regex.

    Inspect a CLI command and return which TECH_BUCKET it belongs to.
    Example:
        "show ip bgp summary"  → "bgp"
        "show ip interface brief"  → "interfaces"
        "show mpls ldp neighbor"  → "mpls"

    """
    c = " " + normalize_command(cmd) + " "  # pad to avoid partial-word confusion

    if " bgp " in c or " show bgp" in c or " show ip bgp" in c:
        return "bgp"
    if " ospf " in c or " show ip ospf" in c or " show ospf" in c:
        return "ospf"
    if " isis " in c or " show isis" in c:
        return "isis"
    if " mpls " in c or " ldp " in c or " show mpls" in c:
        return "mpls"
    if (
        " interface " in c
        or " interfaces " in c
        or " show ip interface brief" in c
        or " show interfaces" in c
    ):
        return "interfaces"
    if " route " in c or " show ip route" in c or " show route" in c:
        return "routing"
    return "misc"

def choose_tech(cmd: str, hinted_tech: Union[str, List[str], None] = None) -> str:
    """
    NOTE: choose_tech() acts only as a fallback if LLM doesn’t return a valid tech
    Decide the *final* tech category for a given command.

    Logic:
      1. If the LLM (or caller) provided a 'hinted_tech' value,
         and it is valid (exists in TECH_BUCKETS), use it directly.
      2. Otherwise, use classify_tech() to infer based on the command text.
      3. If still unknown, return 'misc'.
    This function ensures all results belong to TECH_BUCKETS.
    
    Resolve a final tech bucket for a command:
      1) If hinted_tech is valid (in TECH_BUCKETS), use it.
      2) Otherwise classify from the command string.
      3) Fallback to 'misc'.
    """
    # Step 1: normalize any provided hint
    hinted = norm_tech(hinted_tech)

    # Step 2: if hint is valid (and not misc), use it
    if hinted in TECH_BUCKETS and hinted != "misc":
        return hinted

    # Step 3: else classify automatically from the command string
    classified = classify_tech(cmd)

    # Step 4: sanity-check that result is within TECH_BUCKETS
    if classified not in TECH_BUCKETS:
        return "misc"

    return classified

# --------------------------------------------------------------------
# YAML I/O
# --------------------------------------------------------------------
def load_trusted(path: str = DEFAULT_PATH) -> dict:
    """Load trusted commands YAML into a Python dict."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}

def save_trusted(data: dict, path: str = DEFAULT_PATH) -> None:
    """Save trusted commands dict to YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=True, allow_unicode=True)

# --------------------------------------------------------------------
# Queries
# --------------------------------------------------------------------
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
    True if cmd exists under ANY tech for vendor/platform.
    False otherwise.
    """
    v = norm_vendor(vendor)
    p = norm_platform(platform)
    needle = normalize_command(cmd)
    data = load_trusted(path)
    buckets = data.get(v, {}).get(p, {}) or {}

    for cmds in buckets.values():
        for c in (cmds or []):
            if normalize_command(c) == needle:
                print(f"[DEBUG:is_trusted] vendor={v}, platform={p}, cmd={needle} → True", flush=True)
                return True
    
    print(f"[DEBUG:is_trusted] vendor={v}, platform={p}, cmd={needle} → False", flush=True)
    return False

# --------------------------------------------------------------------
# Mutations
# --------------------------------------------------------------------
def promote(cmd: str, vendor: str, platform: str, tech: Union[str, List[str], None],
            path: str = DEFAULT_PATH) -> None:
    """
    Add a command to the trusted list if not already present.
    Creates buckets if missing.
    Tech is resolved centrally via choose_tech() for consistency.

    Steps:
      1. Normalize vendor, platform, and tech fields.
      2. Ensure the command doesn’t already exist.
      3. Save updated YAML back to disk.

    """
    v = norm_vendor(vendor)
    p = norm_platform(platform)
    t = choose_tech(cmd, hinted_tech=tech)

    cmd_clean = cmd.strip()
    needle = normalize_command(cmd_clean)

    data = load_trusted(path)
    data.setdefault(v, {}).setdefault(p, {}).setdefault(t, [])

    existing = data[v][p][t] or []
    if not any(normalize_command(c) == needle for c in existing):
        existing.append(cmd_clean)
        data[v][p][t] = existing
        print(f"[DEBUG:promote] Added '{cmd_clean}' → {v}/{p}/{t}", flush=True)
    else:
        print(f"[DEBUG:promote] '{cmd_clean}' already exists → {v}/{p}/{t}", flush=True)

    save_trusted(data, path)
