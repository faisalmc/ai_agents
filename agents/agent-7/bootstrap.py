# agents/agent-7/bootstrap.py
from __future__ import annotations
import os, json
from dataclasses import dataclass, asdict
from typing import Optional

# -------- helpers --------

def _as_bool(val: Optional[str], default: bool = False) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "y", "on")

def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default

# -------- config & paths --------

@dataclass(frozen=True)
class Agent7Config:
    repo_root: str
    cache_ttl_min: int
    agent4_capture_entry: Optional[str]
    adk_enabled: bool

def load_config() -> Agent7Config:
    """
    Reads only environment variables (no hardcoding):
      - REPO_ROOT: base repo dir (default: /app/doo)
      - AGENT7_CACHE_TTL_MIN: TTL for local *parsing/analysis* reuse (default: 15)
      - AGENT4_CAPTURE_ENTRY: path/command to Agent-4 capture entrypoint (optional)
      - AGENT7_ADK_ENABLED: toggle ADK lookups (default: true)
    """
    return Agent7Config(
        repo_root=os.getenv("REPO_ROOT", "/app/doo").rstrip("/"),
        cache_ttl_min=_int_env("AGENT7_CACHE_TTL_MIN", 15),
        agent4_capture_entry=os.getenv("AGENT4_CAPTURE_ENTRY", None),
        adk_enabled=_as_bool(os.getenv("AGENT7_ADK_ENABLED", "true"), True),
    )

@dataclass(frozen=True)
class Agent7Paths:
    # resolved, absolute paths
    repo_root: str
    task_root: str            # <repo_root>/<config_dir>/<task_dir>
    agent7_root: str          # <task_root>/agent7

    # --- New canonical layout (execution order) ---
    plan_dir: str             # agent7/1-plan
    capture_dir: str          # agent7/2-capture
    show_logs_dir: str        # agent7/2-capture/show_logs
    analyze_dir: str          # agent7/3-analyze
    md_index_dir: str         # agent7/3-analyze/0-md-index
    parsed_dir: str           # agent7/3-analyze/1-parsed
    facts_dir: str            # agent7/3-analyze/2-facts

    # Trace / tiny operational data
    audit_dir: str            # agent7/audit
    meta_dir: str             # agent7/meta

    # Rollups
    per_device_json: str      # agent7/3-analyze/per_device.json
    cross_device_json: str    # agent7/3-analyze/cross_device.json

def resolve_paths(config: Agent7Config, config_dir: str, task_dir: str) -> Agent7Paths:
    """
    Creates no IO; just computes canonical locations under <task>/agent7.
    """
    task_root = os.path.join(config.repo_root, config_dir, task_dir)
    agent7_root = os.path.join(task_root, "agent7")

    plan_dir = os.path.join(agent7_root, "1-plan")
    capture_dir = os.path.join(agent7_root, "2-capture")
    show_logs_dir = os.path.join(capture_dir, "show_logs")

    analyze_dir = os.path.join(agent7_root, "3-analyze")
    md_index_dir = os.path.join(analyze_dir, "0-md-index")
    parsed_dir = os.path.join(analyze_dir, "1-parsed")
    facts_dir = os.path.join(analyze_dir, "2-facts")

    audit_dir = os.path.join(agent7_root, "audit")
    meta_dir = os.path.join(agent7_root, "meta")

    per_device_json = os.path.join(analyze_dir, "per_device.json")
    cross_device_json = os.path.join(analyze_dir, "cross_device.json")

    return Agent7Paths(
        repo_root=config.repo_root,
        task_root=task_root,
        agent7_root=agent7_root,
        plan_dir=plan_dir,
        capture_dir=capture_dir,
        show_logs_dir=show_logs_dir,
        analyze_dir=analyze_dir,
        md_index_dir=md_index_dir,
        parsed_dir=parsed_dir,
        facts_dir=facts_dir,
        audit_dir=audit_dir,
        meta_dir=meta_dir,
        per_device_json=per_device_json,
        cross_device_json=cross_device_json,
    )

# -------- filesystem setup --------

def ensure_dirs(paths: Agent7Paths) -> None:
    """
    Idempotently creates the Agent-7 directory tree.
    """
    for d in (
        paths.agent7_root,
        paths.plan_dir,
        paths.capture_dir,
        paths.show_logs_dir,
        paths.analyze_dir,
        paths.md_index_dir,
        paths.parsed_dir,
        paths.facts_dir,
        paths.audit_dir,
        paths.meta_dir,
    ):
        os.makedirs(d, exist_ok=True)

def write_boot_snapshot(cfg: Agent7Config, paths: Agent7Paths) -> None:
    """
    Writes a tiny audit snapshot for traceability.
    """
    try:
        ensure_dirs(paths)
        snap = {
            "config": asdict(cfg),
            "paths": asdict(paths),
            "env_subset": {
                "REPO_ROOT": os.getenv("REPO_ROOT", ""),
                "AGENT7_CACHE_TTL_MIN": os.getenv("AGENT7_CACHE_TTL_MIN", ""),
                "AGENT4_CAPTURE_ENTRY": os.getenv("AGENT4_CAPTURE_ENTRY", ""),
                "AGENT7_ADK_ENABLED": os.getenv("AGENT7_ADK_ENABLED", ""),
            },
        }
        with open(os.path.join(paths.audit_dir, "_boot.json"), "w", encoding="utf-8") as f:
            json.dump(snap, f, indent=2)
    except Exception:
        # Never raise from audit
        pass

# -------- convenience: common file helpers --------

def host_signal_set_path(paths: Agent7Paths, hostname: str) -> str:
    # tiny operational file; meta is fine
    return os.path.join(paths.meta_dir, f"{hostname}__signal_set.json")

def capture_plan_path(paths: Agent7Paths) -> str:
    # canonical capture plan JSON produced in planning phase
    return os.path.join(paths.plan_dir, "capture_plan.json")

def overlay_ini_path(paths: Agent7Paths) -> str:
    """
    Back-compat helper name used by older code.
    Points to the canonical plan INI file in the new layout.
    """
    return os.path.join(paths.plan_dir, "ShowCommandsPlan.ini")

def command_plan_ini_path(paths: Agent7Paths) -> str:
    # Preferred explicit name for new code.
    return os.path.join(paths.plan_dir, "ShowCommandsPlan.ini")

def host_blocks_index_path(paths: Agent7Paths, hostname: str) -> str:
    """
    Canonical per-host blocks index (produced during analysis indexing).
    """
    return os.path.join(paths.md_index_dir, f"{hostname}__blocks.json")

def parsed_command_path(paths: Agent7Paths, hostname: str, platform_key: str, cmd_key: str) -> str:
    host_dir = os.path.join(paths.parsed_dir, hostname)
    return os.path.join(host_dir, f"{platform_key}__{cmd_key}.json")

def host_facts_path(paths: Agent7Paths, hostname: str) -> str:
    return os.path.join(paths.facts_dir, f"{hostname}.json")

def write_audit(path: str, text: str) -> None:
    """
    Small helper used by analysis steps to write human-readable traces.
    Never raises.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text if isinstance(text, str) else str(text))
    except Exception:
        pass

# -------- optional CLI bootstrap --------

def _main():
    """
    Usage:
      python -m agents.agent-7.bootstrap <config_dir> <task_dir>
    Creates the dir tree + writes audit/_boot.json
    """
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m agents.agent-7.bootstrap <config_dir> <task_dir>")
        sys.exit(2)
    config_dir, task_dir = sys.argv[1], sys.argv[2]
    cfg = load_config()
    paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)
    write_boot_snapshot(cfg, paths)
    print(f"[agent7] ready at {paths.agent7_root}")

if __name__ == "__main__":
    _main()