# orchestrator/agent7_client.py
import os
import json
import asyncio
import httpx
import importlib.util
from typing import Any, Dict, List, Optional

# Use existing env var from .env
A7_BASE_URL   = os.getenv("AGENT_7_URL", "http://agent-7:8007")
A7_PLAN_URL    = f"{A7_BASE_URL}/plan"
A7_CAPTURE_URL = f"{A7_BASE_URL}/capture"
A7_ANALYZE_URL = f"{A7_BASE_URL}/analyze"

# For locating slack_ui.py if not provided explicitly
REPO_ROOT = os.getenv("REPO_ROOT", "/app/doo")
DEFAULT_SLACK_UI_PATH = os.path.join(REPO_ROOT, "agents", "agent-7", "slack_ui.py")
A7_SLACK_UI_PATH = os.getenv("A7_SLACK_UI_PATH", DEFAULT_SLACK_UI_PATH)

print(f"[DEBUG] AGENT_7_URL={A7_BASE_URL}", flush=True)


async def _post(url: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=1200) as c:
        r = await c.post(url, json=payload)
        r.raise_for_status()
        return r.json()


def _read_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _load_slack_ui_module() -> Optional[Any]:
    """
    Try to import the Slack UI builder from a direct file path.
    Returns the module or None on failure.
    """
    path = (A7_SLACK_UI_PATH or "").strip()
    if not path or not os.path.exists(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location("a7_slack_ui", path)
        if not spec or not spec.loader:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod
    except Exception as e:
        print(f"[DEBUG] failed to import slack_ui at {path}: {e}", flush=True)
        return None


def _compute_status_rollup(per_device: List[Dict[str, Any]]) -> str:
    counts = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
    for row in per_device or []:
        s = str(row.get("status", "unknown")).lower()
        if s not in counts:
            s = "unknown"
        counts[s] += 1
    # Show only the most relevant three buckets
    parts: List[str] = []
    for k in ("healthy", "degraded", "error"):
        if counts[k]:
            parts.append(f"*{k.capitalize()}:* {counts[k]}")
    if not parts:
        parts.append(f"*Unknown:* {counts['unknown']}")
    return " • ".join(parts)


def _build_blocks(
    config_dir: str,
    task_id: str,
    per_device_path: str,
    cross_device_path: str,
) -> List[Dict[str, Any]]:
    """
    Load per_device/cross JSON, call slack_ui.build_overview_blocks(...),
    and inject a small per-device status rollup near the top.
    """
    per_device_obj = _read_json(per_device_path) or []
    cross_obj = _read_json(cross_device_path) or {}
    if not isinstance(per_device_obj, list):
        per_device_obj = []
    if not isinstance(cross_obj, dict):
        cross_obj = {}

    ui = _load_slack_ui_module()

    # Fallback: minimal single-block message if UI module missing
    if ui is None or not hasattr(ui, "build_overview_blocks"):
        status = cross_obj.get("task_status", "unknown")
        text = (
            f"*Agent-7 Overview*\n"
            f"*Config:* `{config_dir}` • *Task:* `{task_id}` • *Status:* *{status}*\n"
            f"_(Install slack_ui.py or set A7_SLACK_UI_PATH to enable rich blocks)_"
        )
        return [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]

    # Build rich blocks
    blocks: List[Dict[str, Any]] = ui.build_overview_blocks(
        config_dir=config_dir,
        task_dir=task_id,
        cross=cross_obj,
        per_device=per_device_obj,
        include_attach_button=True,
    )

    # Inject a status rollup right after the header block (index 1)
    try:
        rollup = _compute_status_rollup(per_device_obj)
        rollup_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"*Per-device status:* {rollup}"}}
        # Only insert if we have at least 1 block (header)
        if blocks:
            blocks.insert(1, rollup_block)
        else:
            blocks = [rollup_block]
    except Exception:
        pass

    return blocks


def run_plan(
    config_dir: str,
    task_id: str,
    hosts: Optional[List[str]] = None,
    per_signal_limit: int = 3,
    use_adk: bool = True,
    include_lexicon: bool = True,
) -> dict:
    payload = {
        "config_dir": config_dir,
        "task_dir": task_id,
        "hosts": hosts,
        "per_signal_limit": per_signal_limit,
        "use_adk": use_adk,
        "include_lexicon": include_lexicon,
    }
    return asyncio.run(_post(A7_PLAN_URL, payload))


def run_capture(
    config_dir: str,
    task_id: str,
    plan_path: Optional[str] = None,
    hosts_override: Optional[List[str]] = None,
) -> dict:
    payload = {
        "config_dir": config_dir,
        "task_dir": task_id,
        "plan_path": plan_path,
        "hosts_override": hosts_override,
    }
    return asyncio.run(_post(A7_CAPTURE_URL, payload))


def run_analyze(
    config_dir: str,
    task_id: str,
) -> dict:
    """
    Calls Agent-7 /analyze, then prepares Slack blocks using the
    per-device and cross-device artifacts it wrote to disk.
    """
    payload = {"config_dir": config_dir, "task_dir": task_id}
    resp = asyncio.run(_post(A7_ANALYZE_URL, payload)) or {}

    per_p = resp.get("per_device_json_path")
    cross_p = resp.get("cross_device_json_path")

    blocks: List[Dict[str, Any]] = []
    if per_p and cross_p and os.path.exists(per_p) and os.path.exists(cross_p):
        try:
            blocks = _build_blocks(config_dir, task_id, per_p, cross_p)
        except Exception as e:
            # Safe fallback if anything goes wrong in block building
            status = "unknown"
            cx = _read_json(cross_p) or {}
            if isinstance(cx, dict):
                status = cx.get("task_status", "unknown")
            text = (
                f"*Agent-7 Overview*\n"
                f"*Config:* `{config_dir}` • *Task:* `{task_id}` • *Status:* *{status}*\n"
                f"_(Block build error: {e})_"
            )
            blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]
    else:
        # Very early fallback: we couldn’t find artifacts
        text = (
            f"*Agent-7 Overview*\n"
            f"*Config:* `{config_dir}` • *Task:* `{task_id}` • *Status:* *unknown*\n"
            f"_(Artifacts not found; check analyze run)_"
        )
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]

    # Return the API response plus Slack blocks for the bot to post
    resp["blocks"] = blocks
    return resp