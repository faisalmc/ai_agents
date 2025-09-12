# agent5_shared.py
import os, json, re
from datetime import datetime

AGENT_KNOWLEDGE_ROOT = os.getenv("AGENT_KNOWLEDGE_ROOT", "/app/doo/_agent_knowledge").rstrip("/")
LEXICON_ROOT = os.path.join(AGENT_KNOWLEDGE_ROOT, "lexicon")      # global, per-platform
OBSERVED_ROOT = os.path.join(AGENT_KNOWLEDGE_ROOT, "observed")    # per-task/task_dir

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

## v5

def _read_lines(path: str) -> list[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        return [l.strip() for l in fh if l.strip()]

def normalize_platform(p: str | None) -> str:
    p = (p or "").strip().lower()
    if not p:
        return "unknown"
    # keep simple + tolerant
    if "xr" in p:
        return "cisco-ios-xr"
    if "ios" in p and "xr" not in p:
        return "cisco-ios"
    return p

def sanitize_show(cmd: str, platform: str) -> str | None:
    """
    Conservative command sanitizer:
      - XR: drop IOS-style pipes; keep base command if meaningful.
      - IOS: allow pipes.
      - Always strip leading/trailing spaces.
    Returns cleaned command, or None if it collapses to empty/unsafe.
    """
    if not cmd:
        return None
    c = cmd.strip()
    plat = normalize_platform(platform)

    # absolutely forbid non-readonly starters here (paranoia)
    if re.match(r"^\s*(conf|configure|reload|clear|debug|monitor|copy|write)\b", c, re.I):
        return None

    # enforce 'show' only for this sanitizer
    if not re.match(r"^\s*show\b", c, re.I):
        return None 
           
    if plat == "cisco-ios-xr":
        # Split on pipe and keep the left-most. XR doesn't support IOS grep-style pipes.
        c = c.split("|", 1)[0].strip()
        # tiny XR normalizations (optional/safe)
        c = re.sub(r"^\s*show\s+(run|running[-\s]*config)\b", "show running-config", c, flags=re.I)

    # light dedupe of whitespace
    c = re.sub(r"\s+", " ", c).strip()
    return c or None

def load_observed_commands(config_dir: str, task_dir: str) -> list[str]:
    """
    Per-task observed list harvested from show_cmds.ini by Agent-1:
      /_agent_knowledge/observed/<config_dir>/<task_dir>/commands.txt
    """
    path = os.path.join(OBSERVED_ROOT, config_dir, task_dir, "commands.txt")
    return _read_lines(path)

def load_lexicon_candidates(platform: str) -> list[str]:
    """
    Agent-1 global 'ideas' bucket. Phase-1: treated as last-resort candidates only.
      /_agent_knowledge/lexicon/_candidates/<platform>.txt
    """
    plat = normalize_platform(platform)
    path = os.path.join(LEXICON_ROOT, "_candidates", f"{plat}.txt")
    return _read_lines(path)