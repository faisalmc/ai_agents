# ai_agents/agents/agent-7/cache.py
from __future__ import annotations
import os, glob, time
from typing import Iterable, List, Tuple

# TTL (minutes) controls *local* recompute avoidance only.
# Capture via Agent-4 is explicitly excluded from TTL reuse.
DEFAULT_TTL_MIN = int(os.getenv("AGENT7_CACHE_TTL_MIN", "15"))

# ---------------------------
# Generic helpers
# ---------------------------
def _mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except Exception:
        return 0.0

def _newest(paths: Iterable[str]) -> float:
    newest = 0.0
    for p in paths:
        ts = _mtime(p)
        if ts > newest:
            newest = ts
    return newest

def _glob_files(root: str, pattern: str) -> List[str]:
    """Return only files (no dirs) matching pattern under root."""
    out: List[str] = []
    for p in glob.glob(os.path.join(root, pattern), recursive=True):
        if os.path.isfile(p):
            out.append(p)
    return out

def _newest_glob(root: str, pattern: str) -> float:
    return _newest(_glob_files(root, pattern))

def ttl_seconds(ttl_min: int | None = None) -> int:
    return int(60 * (ttl_min if ttl_min is not None else DEFAULT_TTL_MIN))

def is_fresh(output_path: str, inputs: Iterable[str], ttl_min: int | None = None) -> Tuple[bool, str]:
    """
    True when:
      1) output exists
      2) output.mtime >= max(inputs.mtime)
      3) now - output.mtime <= TTL
    Returns (fresh, reason_if_stale)
    """
    now = time.time()
    out_m = _mtime(output_path)
    if out_m == 0.0:
        return False, "missing output"

    max_in = _newest(inputs)
    if max_in > out_m:
        return False, "inputs newer than output"

    if now - out_m > ttl_seconds(ttl_min):
        return False, "ttl expired"

    return True, ""

def touch_stamp(stamp_path: str) -> None:
    os.makedirs(os.path.dirname(stamp_path), exist_ok=True)
    with open(stamp_path, "a", encoding="utf-8"):
        pass
    os.utime(stamp_path, None)

# ---------------------------
# Artifact-specific checks
# ---------------------------
def md_index_fresh(md_path: str, index_path: str, ttl_min: int | None = None) -> Tuple[bool, str]:
    """
    Is the per-host markdown index fresh?
    Typical inputs/outputs now are:
      - input:  agent7/show_logs/<host>.md   (or merged source)
      - output: agent7/md_split/<host>/blocks.ndjson
    """
    return is_fresh(index_path, [md_path], ttl_min)

def genie_parsed_fresh(blocks_index_path: str, parsed_dir_for_host: str, ttl_min: int | None = None) -> Tuple[bool, str]:
    """
    Parsed outputs are fresh if there is at least one parsed JSON in parsed/<host>/
    and the newest parsed JSON is newer than the blocks index (within TTL).
    (No stamp file required; genie_parser.py does not write one.)
    """
    parsed_files = _glob_files(parsed_dir_for_host, "*.json")
    if not parsed_files:
        return False, "no parsed json"
    # Use the newest parsed json as 'output' representative
    newest_parsed = max(parsed_files, key=_mtime)
    return is_fresh(newest_parsed, [blocks_index_path], ttl_min)

def facts_fresh(facts_path: str, parsed_dir_for_host: str, ttl_min: int | None = None) -> Tuple[bool, str]:
    """
    Facts are fresh if facts/<host>.json exists and is newer than the newest parsed/* for that host.
    """
    parsed_files = _glob_files(parsed_dir_for_host, "*.json")
    if not parsed_files:
        return False, "no parsed json"
    return is_fresh(facts_path, parsed_files, ttl_min)

def per_device_fresh(
    per_device_path: str,
    host_facts_paths: List[str],
    adk_cache_path: str | None,
    agent1_summary_path: str | None,
    ttl_min: int | None = None,
) -> Tuple[bool, str]:
    """
    Per-device JSON fresh vs facts/*, optional ADK cache, optional Agent-1 summary.
    """
    inputs: List[str] = list(host_facts_paths)
    if adk_cache_path:
        inputs.append(adk_cache_path)
    if agent1_summary_path:
        inputs.append(agent1_summary_path)
    return is_fresh(per_device_path, inputs, ttl_min)

def cross_device_fresh(
    cross_path: str,
    per_device_path: str,
    facts_dir: str,
    ttl_min: int | None = None,
) -> Tuple[bool, str]:
    """
    Cross-device JSON fresh vs per_device.json and the newest facts/* (to catch late changes).
    """
    fact_files = _glob_files(facts_dir, "*.json")
    inputs = [per_device_path] + fact_files
    return is_fresh(cross_path, inputs, ttl_min)

# ---------------------------
# Convenience: decide-then-skip
# ---------------------------
def should_skip_build(output_path: str, inputs: Iterable[str], ttl_min: int | None = None) -> bool:
    ok, _ = is_fresh(output_path, inputs, ttl_min)
    return ok

def stale_reason(output_path: str, inputs: Iterable[str], ttl_min: int | None = None) -> str:
    ok, why = is_fresh(output_path, inputs, ttl_min)
    return "" if ok else why