# ai_agents/agents/agent-7/signal_harvester.py
# LLM-only signal harvesting. No static keyword lists, no regex heuristics.

from __future__ import annotations
import os
import json
import glob
from typing import Dict, Any

from bootstrap import load_config, resolve_paths

# Prefer shared.llm_api; fall back to local llm_api; else graceful degrade.
try:
    from shared.llm_api import call_llm  # type: ignore
except Exception:
    try:
        from llm_api import call_llm  # type: ignore
    except Exception:
        call_llm = None  # degrade: we will return empty signals

def _dbg(msg: str) -> None:
    print(f"[agent7][signals] {msg}", flush=True)

_SYSTEM = """You extract high-level network 'signals' (protocols/features) from raw CLI logs.
Strict rules:
- Read ONLY the provided CLI markdown text.
- Output signals as short, lowercase tokens (single words if possible).
- Do NOT invent signals; include none if evidence is insufficient.
- Also guess a platform hint if possible (e.g., ios-xr, ios, nx-os, junos, unknown).

Output ONLY JSON with this schema:
{
  "hostname": "<string>",
  "platform_hint": "<string>",
  "signals": ["<string>", "..."],
  "confidence": 0.0,
  "evidence": { "<signal>": ["<verbatim evidence line>", "..."] },
  "notes": "<one or two sentences on how you decided>"
}
Be conservative; it’s OK to return an empty 'signals' list if the log is too sparse.
"""

def _read_dir(md_dir: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not os.path.isdir(md_dir):
        return out
    for p in sorted(glob.glob(os.path.join(md_dir, "*.md"))):
        try:
            host = os.path.basename(p).removesuffix(".md")
            out[host] = open(p, "r", encoding="utf-8").read()
        except Exception as e:
            _dbg(f"[signals] failed reading {p}: {e}")
    return out

def _read_md_logs(task_root: str) -> Dict[str, str]:
    """
    Merge CLI markdown from:
      • <task_root>/grading_logs/*.md        (baseline/original)
      • <task_root>/agent7/show_logs/*.md    (Agent-7 capture outputs)
    Later source simply concatenates after the first (no parsing/heuristics).
    """
    orig = _read_dir(os.path.join(task_root, "grading_logs"))
    a7   = _read_dir(os.path.join(task_root, "agent7", "show_logs"))

    all_hosts = set(orig) | set(a7)
    merged: Dict[str, str] = {}
    for h in sorted(all_hosts):
        a = orig.get(h, "")
        b = a7.get(h, "")
        merged[h] = a + ("\n\n" if a and b else "") + b
    _dbg(f"[signals] loaded md logs: {len(merged)} (grading_logs + agent7/show_logs)")
    return merged

def _fallback_empty(host: str) -> Dict[str, Any]:
    return {
        "hostname": host,
        "platform_hint": "unknown",
        "signals": [],
        "confidence": 0.0,
        "evidence": {},
        "notes": "fallback: LLM unavailable or returned non-JSON",
    }

def _ask_llm_for_signals(host: str, md_text: str) -> Dict[str, Any]:
    """Call the LLM with the host's markdown only (no local parsing)."""
    if not call_llm:
        return _fallback_empty(host)

    snippet = md_text[:15000] if md_text else ""
    user = (
        f"### Hostname\n{host}\n\n"
        f"### CLI Markdown (truncated)\n```md\n{snippet}\n```"
    )
    obj: Dict[str, Any] = {}
    try:
        raw = call_llm(
            messages=[{"role": "system", "content": _SYSTEM},
                      {"role": "user", "content": user}],
            temperature=0.0,
        ) or ""
        try:
            obj = json.loads(raw)
        except Exception:
            import re
            m = re.search(r"```json\s*(.+?)\s*```", str(raw), flags=re.DOTALL | re.IGNORECASE)
            if m:
                obj = json.loads(m.group(1))
    except Exception as e:
        _dbg(f"[signals][{host}] LLM call failed: {e}")
        obj = {}

    # Minimal, conservative fallback (no heuristics)
    if not isinstance(obj, dict):
        obj = _fallback_empty(host)

    # Normalize and dedupe signals (lowercase only)
    sigs = obj.get("signals")
    if isinstance(sigs, list):
        seen = set()
        norm = []
        for s in sigs:
            if isinstance(s, str):
                ls = s.strip().lower()
                if ls and ls not in seen:
                    seen.add(ls); norm.append(ls)
        obj["signals"] = norm
    else:
        obj["signals"] = []

    obj.setdefault("hostname", host)
    obj.setdefault("platform_hint", "unknown")
    obj.setdefault("confidence", 0.0)
    obj.setdefault("evidence", {})
    obj.setdefault("notes", obj.get("notes", ""))
    return obj

def harvest_signals(config_dir: str, task_dir: str) -> Dict[str, Dict[str, object]]:
    """
    LLM-only signal discovery.
    Writes:
      • agent7/meta/<host>__signal_set.json
      • agent7/meta/signal_set.json
    Returns {hostname: {...}} for all hosts with logs.
    """
    cfg = load_config()
    paths = resolve_paths(cfg, config_dir, task_dir)
    os.makedirs(paths.meta_dir, exist_ok=True)

    md_map = _read_md_logs(paths.task_root)
    results: Dict[str, Dict[str, object]] = {}

    for host, text in md_map.items():
        obj = _ask_llm_for_signals(host, text)
        results[host] = obj

        per_host_path = os.path.join(paths.meta_dir, f"{host}__signal_set.json")
        try:
            with open(per_host_path, "w", encoding="utf-8") as fh:
                json.dump(obj, fh, indent=2)
        except Exception as e:
            _dbg(f"[signals] failed to write {per_host_path}: {e}")

    bundle_path = os.path.join(paths.meta_dir, "signal_set.json")
    try:
        with open(bundle_path, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2)
        _dbg(f"[signals] wrote {bundle_path} and {len(results)} per-host files")
    except Exception as e:
        _dbg(f"[signals] failed to write {bundle_path}: {e}")

    return results

# CLI (optional)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/signal_harvester.py <config_dir> <task_dir>")
        raise SystemExit(2)
    config_dir, task_dir = sys.argv[1], sys.argv[2]
    obj = harvest_signals(config_dir, task_dir)
    print(json.dumps(obj, indent=2))