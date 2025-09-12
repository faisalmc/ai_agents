# agents/agent-7/overlay_planner.py
# Compatibility shim: delegate to command_plan_builder.plan_commands()
# and mirror artifacts to legacy filenames/locations so old callers keep working.

from __future__ import annotations
import os
import json
from typing import Any, Dict

from bootstrap import load_config, resolve_paths, ensure_dirs

# Prefer the new planner; if unavailable, raise (so we notice in dev).
try:
    import command_plan_builder as _planner
except Exception as e:  # pragma: no cover
    raise RuntimeError("command_plan_builder.py is required for overlay_planner shim") from e


def _read_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def plan_overlay(
    config_dir: str,
    task_dir: str,
    *,
    per_signal_limit: int = 3,
    use_adk: bool = True,
    include_lexicon: bool = True,
) -> Dict[str, Any]:
    """
    Legacy signature retained.
    Internally calls command_plan_builder.plan_commands(...) which writes:
      • agent7/plan/show_cmds.plan.ini
      • agent7/plan/capture_plan.json

    This shim additionally mirrors to the legacy paths so older tooling still finds:
      • agent7/show_cmds.overlay.ini
      • agent7/meta/overlay_plan.json
    """
    cfg = load_config()
    paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    # Run the new planner (canonical).
    plan_obj = _planner.plan_commands(
        config_dir=config_dir,
        task_dir=task_dir,
        hosts=None,  # allow the builder to decide/harvest
        per_signal_limit=per_signal_limit,
        use_adk=use_adk,
        include_lexicon=include_lexicon,
    )

    agent7_root = paths.agent7_root
    plan_dir = os.path.join(agent7_root, "plan")

    # Source (new) artifacts
    new_ini = os.path.join(plan_dir, "show_cmds.plan.ini")
    new_json = os.path.join(plan_dir, "capture_plan.json")

    # Legacy mirrors expected by some older entry points
    legacy_ini = os.path.join(agent7_root, "show_cmds.overlay.ini")
    legacy_json = os.path.join(agent7_root, "meta", "overlay_plan.json")

    # Mirror INI (best-effort)
    try:
        if os.path.exists(new_ini):
            with open(new_ini, "r", encoding="utf-8") as fsrc:
                _write_text(legacy_ini, fsrc.read())
    except Exception:
        pass

    # Mirror JSON (best-effort)
    try:
        cap = _read_json(new_json)
        if cap is None:
            cap = plan_obj if isinstance(plan_obj, dict) else {}
        _write_json(legacy_json, cap)
    except Exception:
        pass

    return plan_obj if isinstance(plan_obj, dict) else {"hosts": {}, "note": "shim-return"}


def _main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/overlay_planner.py <config_dir> <task_dir>")
        raise SystemExit(2)
    plan_overlay(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    _main()