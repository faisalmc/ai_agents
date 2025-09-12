# ai_agents/agents/agent-7/audit.py
from __future__ import annotations
import os, json, time, shutil
from typing import Any, Dict, Optional
from datetime import datetime

# Reuse shared writer if available (non-fatal fallback)
try:
    from agent5_shared import write_audit as _shared_write_audit  # type: ignore
except Exception:  # pragma: no cover
    _shared_write_audit = None  # noqa: N816

# Base path (kept consistent with the rest of Agent-7)
REPO_ROOT = os.getenv("REPO_ROOT", "/app/doo")

# Rotation/size caps (optional)
MAX_BYTES = int(os.getenv("AGENT7_AUDIT_MAX_BYTES", "1048576"))   # 1 MiB per file cap
ROTATE_KEEP = int(os.getenv("AGENT7_AUDIT_ROTATE_KEEP", "3"))     # how many rotated copies to retain

# ---------------------------
# Path helpers
# ---------------------------
def agent7_root(config_dir: str, task_dir: str) -> str:
    return os.path.join(REPO_ROOT, config_dir, task_dir, "agent7")

def audit_root(config_dir: str, task_dir: str) -> str:
    root = os.path.join(agent7_root(config_dir, task_dir), "audit")
    os.makedirs(root, exist_ok=True)
    return root

def _abs(path_or_rel: str, base: str) -> str:
    return path_or_rel if os.path.isabs(path_or_rel) else os.path.join(base, path_or_rel)

# ---------------------------
# Core writers
# ---------------------------
def _size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except Exception:
        return 0

def _rotate_if_needed(path: str) -> None:
    if MAX_BYTES <= 0 or not os.path.exists(path):
        return
    try:
        if _size(path) < MAX_BYTES:
            return
        # Rotate: file -> file.1, file.1 -> file.2, ...
        for i in range(ROTATE_KEEP, 0, -1):
            older = f"{path}.{i}"
            newer = f"{path}.{i-1}" if i > 1 else path
            if os.path.exists(older):
                try:
                    os.remove(older)
                except Exception:
                    pass
            if os.path.exists(newer):
                try:
                    shutil.copy2(newer, older)
                except Exception:
                    pass
        # Truncate current
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("")
        except Exception:
            pass
    except Exception:
        pass

def write_text(abs_path: str, content: str) -> None:
    """
    Write (or overwrite) a text file at an absolute path with rotation safety.
    """
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    _rotate_if_needed(abs_path)
    if _shared_write_audit:
        # shared helper is already safe & resilient
        _shared_write_audit(abs_path, content)
        return
    # local fallback
    try:
        with open(abs_path, "w", encoding="utf-8") as fh:
            fh.write(content if isinstance(content, str) else str(content))
    except Exception:
        # last-ditch best effort
        try:
            tmp = abs_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(content if isinstance(content, str) else str(content))
            os.replace(tmp, abs_path)
        except Exception:
            pass

# ---- Back-compat alias (used by some modules expecting write_audit) ----
def write_audit(abs_path: str, content: str) -> None:
    """
    Back-compat shim: identical to write_text(abs_path, content).
    """
    write_text(abs_path, content)

def write_json(abs_path: str, obj: Any) -> None:
    write_text(abs_path, json.dumps(obj, indent=2, ensure_ascii=False))

def append_jsonl(abs_path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    _rotate_if_needed(abs_path)
    try:
        with open(abs_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception:
        pass

# ---------------------------
# High-level helpers (used by other Agent-7 modules)
# ---------------------------
def set_run_context(config_dir: str, task_dir: str, extra: Optional[Dict[str, Any]] = None) -> str:
    """
    Record the run context for traceability (timestamps, env subset, dirs).
    """
    root = audit_root(config_dir, task_dir)
    ctx = {
        "ts_iso": datetime.utcnow().isoformat() + "Z",
        "config_dir": config_dir,
        "task_dir": task_dir,
        "repo_root": REPO_ROOT,
        "env": {
            "AGENT7_AUDIT_MAX_BYTES": MAX_BYTES,
            "AGENT7_AUDIT_ROTATE_KEEP": ROTATE_KEEP,
        },
    }
    if extra:
        ctx["extra"] = extra
    path = os.path.join(root, "_run_context.json")
    write_json(path, ctx)
    return path

def log_event(config_dir: str, task_dir: str, component: str, msg: str, meta: Optional[Dict[str, Any]] = None) -> None:
    """
    Append a small event row to audit/events.ndjson.
    """
    root = audit_root(config_dir, task_dir)
    rec = {
        "ts": time.time(),
        "ts_iso": datetime.utcnow().isoformat() + "Z",
        "component": component,
        "message": msg,
        "meta": meta or {},
    }
    append_jsonl(os.path.join(root, "events.ndjson"), rec)

def write_prompt(config_dir: str, task_dir: str, name: str, text: str) -> str:
    """
    Save any prompt text (LLM system/user) for traceability.
    name examples: 'B-PE-1__per_device_prompt.txt', 'cross_prompt.txt'
    """
    root = audit_root(config_dir, task_dir)
    path = os.path.join(root, name)
    write_text(path, text)
    return path

def write_raw(config_dir: str, task_dir: str, name: str, raw_text_or_obj: Any) -> str:
    """
    Save raw model output or any unprocessed payload.
    """
    root = audit_root(config_dir, task_dir)
    path = os.path.join(root, name)
    if isinstance(raw_text_or_obj, (dict, list)):
        write_json(path, raw_text_or_obj)
    else:
        write_text(path, str(raw_text_or_obj))
    return path

def write_trace(config_dir: str, task_dir: str, name: str, rows: list[dict]) -> str:
    """
    Save an ordered list of small trace rows as .ndjson (e.g., trust partitions).
    """
    root = audit_root(config_dir, task_dir)
    path = os.path.join(root, name if name.endswith(".ndjson") else f"{name}.ndjson")
    # rewrite (fresh) to preserve run order; each caller controls when to append
    try:
        with open(path, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return path

# Convenience shortcuts used by per_device_llm / cross_device_llm
def save_per_device_io(config_dir: str, task_dir: str, host: str, prompt_text: str, raw_text: str) -> None:
    write_prompt(config_dir, task_dir, f"{host}__per_device_prompt.txt", prompt_text)
    write_raw(config_dir, task_dir, f"{host}__per_device_raw.json", raw_text)

def save_cross_io(config_dir: str, task_dir: str, prompt_text: str, raw_text: str) -> None:
    write_prompt(config_dir, task_dir, "cross_prompt.txt", prompt_text)
    write_raw(config_dir, task_dir, "cross_raw.json", raw_text)