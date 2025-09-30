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

def norm_tech(t: Union[str, List[str], None]) -> str:
    if isinstance(t, list) and t:
        t = t[0]
    t = (t or "misc")
    t = str(t).strip().lower()
    return t or "misc"


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
    """
    v = norm_vendor(vendor)
    p = norm_platform(platform)
    t = norm_tech(tech)
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