# agents/agent-8/commands_trusted.py
# Simple helpers to manage trusted show commands
# YAML format: vendor -> platform -> tech -> [commands]

import os
import yaml

DEFAULT_PATH = "shared/_agent_knowledge/commands_trusted.yaml"


def load_trusted(path: str = DEFAULT_PATH) -> dict:
    """Load the trusted commands YAML into a Python dict."""
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def save_trusted(data: dict, path: str = DEFAULT_PATH) -> None:
    """Save the trusted commands dict back into the YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=True)


def get_trusted(vendor: str, platform: str, tech: str,
                path: str = DEFAULT_PATH) -> list:
    """Return list of trusted commands for vendor/platform/tech."""
    data = load_trusted(path)
    return data.get(vendor, {}).get(platform, {}).get(tech, [])


def is_trusted(cmd: str, vendor: str, platform: str,
               path: str = DEFAULT_PATH) -> tuple:
    """
    Check if a command is trusted under any tech bucket.
    Returns (True, tech) if found, otherwise (False, None).
    """
    cmd_norm = normalize_command(cmd)
    data = load_trusted(path)
    for tech, cmds in data.get(vendor, {}).get(platform, {}).items():
        if cmd_norm in [normalize_command(c) for c in cmds]:
            return True, tech
    return False, None


def normalize_command(cmd: str) -> str:
    """Very basic normalization: lowercase and strip spaces."""
    return " ".join(cmd.lower().split())


def promote(cmd: str, vendor: str, platform: str, tech: str,
            path: str = DEFAULT_PATH) -> None:
    """
    Add a command to the trusted list if not already present.
    Creates vendor/platform/tech buckets if missing.
    """
    cmd_norm = normalize_command(cmd)
    data = load_trusted(path)

    if vendor not in data:
        data[vendor] = {}
    if platform not in data[vendor]:
        data[vendor][platform] = {}
    if tech not in data[vendor][platform]:
        data[vendor][platform][tech] = []

    # Avoid duplicates
    existing = [normalize_command(c) for c in data[vendor][platform][tech]]
    if cmd_norm not in existing:
        data[vendor][platform][tech].append(cmd_norm)

    save_trusted(data, path)