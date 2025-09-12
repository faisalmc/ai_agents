# agent5_shared.py
import os, json, re
from datetime import datetime

def dbg(msg: str):
    print(f"[agent-5] {msg}", flush=True)

def write_audit(path: str, data: str | bytes) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
        with open(path, mode) as f:
            f.write(data)
    except Exception as e:
        dbg(f"[audit] failed to write {path}: {e}")

def safe_json_loads(raw: str):
    raw = (raw or "").strip()
    if not raw:
        return None
    # try strict
    try:
        return json.loads(raw)
    except Exception:
        pass
    # try fenced ```json blocks
    m = re.search(r"```json\s*(.+?)\s*```", raw, flags=re.DOTALL|re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            return None
    # last resort: first {...} or [...]
    m2 = re.search(r"(\{.*\}|\[.*\])", raw, flags=re.DOTALL)
    if m2:
        try:
            return json.loads(m2.group(1))
        except Exception:
            return None
    return None
