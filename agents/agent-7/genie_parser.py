# ai_agents/agents/agent-7/genie_parser.py
from __future__ import annotations
import os, re, json, glob, time
from typing import Any, Dict, List, Optional

# Simple logger
def _dbg(msg: str) -> None:
    print(f"[agent7][genie] {msg}", flush=True)

# Static bootstrap import (no dynamic loaders)
from bootstrap import (
    Agent7Paths,
    load_config,
    resolve_paths,
    ensure_dirs,
)

# Optional shared helpers (with safe fallbacks)
try:
    from agent5_shared import sanitize_show, normalize_platform  # type: ignore
except Exception:
    def sanitize_show(cmd: str, platform_hint: str) -> str:
        c = (cmd or "").strip()
        return c if c.lower().startswith("show ") else ""
    def normalize_platform(p: str) -> str:
        p = (p or "").strip().lower()
        if "xr" in p: return "cisco-ios-xr"
        if "xe" in p or p == "ios": return "cisco-ios"
        return "unknown"

# ---------------------------
# Genie offline device factory
# ---------------------------
_OS_MAP = {
    "cisco-ios-xr": "iosxr",
    "cisco-ios": "iosxe",
    "unknown": "iosxe",
}

def _make_offline_device(os_name: str):
    """
    Create a dummy pyATS device; Genie parsers can run with output=... (no connect()).
    """
    from genie.testbed import load as tb_load  # raises if genie not installed
    tb_yaml = f"""
devices:
  dummy:
    os: {os_name}
    type: router
    connections:
      defaults:
        class: unicon.Unicon
      cli:
        protocol: unknown
"""
    tb = tb_load(tb_yaml)
    return tb.devices["dummy"]

def _read(path: str) -> str:
    try:
        return open(path, "r", encoding="utf-8").read()
    except Exception:
        return ""

def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)

def _safe_cmd_key(s: str) -> str:
    # Fallback if md index didn’t provide cmd_key
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_:\-\.]", "", s)
    return s[:160] or "cmd"

def _genie_os(platform_hint: str) -> str:
    return _OS_MAP.get(normalize_platform(platform_hint), "iosxe")

# ---------------------------
# Inputs: per-host blocks index
# ---------------------------
def _load_blocks_for_host(paths: Agent7Paths, host: str) -> List[Dict[str, Any]]:
    """
    Preferred:  agent7/3-analyze/0-md-index/<host>__blocks.json (array)
    Fallback:   agent7/md_split/<host>/blocks.ndjson (line-delimited JSON)
    Each block should ideally include:
      "sanitized_command", "text_path", "platform_hint", optionally "cmd_key"
    """
    rows: List[Dict[str, Any]] = []

    # Preferred JSON array
    new_idx = os.path.join(paths.md_index_dir, f"{host}__blocks.json")
    try:
        arr = json.loads(open(new_idx, "r", encoding="utf-8").read())
        if isinstance(arr, list):
            for obj in arr:
                if isinstance(obj, dict):
                    rows.append(obj)
    except Exception:
        pass

    if rows:
        return rows

    # Fallback NDJSON under legacy md_split
    legacy_nd = os.path.join(paths.agent7_root, "md_split", host, "blocks.ndjson")
    try:
        with open(legacy_nd, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        rows.append(obj)
                except Exception:
                    continue
    except Exception:
        pass

    return rows

def _list_hosts_with_blocks(paths: Agent7Paths) -> List[str]:
    """Discover hosts from preferred index dir, else from legacy md_split."""
    hosts: List[str] = []

    # Preferred: json files named <host>__blocks.json
    try:
        for p in sorted(glob.glob(os.path.join(paths.md_index_dir, "*__blocks.json"))):
            base = os.path.basename(p)
            host = base[:-len("__blocks.json")]
            if host:
                hosts.append(host)
    except Exception:
        pass

    if hosts:
        return hosts

    # Fallback: subdirs in md_split that contain blocks.ndjson
    legacy_root = os.path.join(paths.agent7_root, "md_split")
    try:
        for name in sorted(os.listdir(legacy_root)):
            nd = os.path.join(legacy_root, name, "blocks.ndjson")
            if os.path.isfile(nd):
                hosts.append(name)
    except Exception:
        pass

    return hosts

# ---------------------------
# Core parse loop
# ---------------------------
def _parse_one(dev, command: str, text: str) -> Dict[str, Any]:
    try:
        out = dev.parse(command, output=text)
        return {"ok": True, "data": out}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def _output_path(paths: Agent7Paths, host: str, platform_hint: str, cmd_key: str) -> str:
    plat = normalize_platform(platform_hint) or "unknown"
    host_dir = os.path.join(paths.parsed_dir, host)
    os.makedirs(host_dir, exist_ok=True)
    return os.path.join(host_dir, f"{plat}__{cmd_key}.json")

# ---------------------------
# Public: run genie parsing
# ---------------------------
def run(config_dir: str, task_dir: str) -> Dict[str, Any]:
    """
    Reads md-index for each host and produces:
      • agent7/3-analyze/1-parsed/<host>/<platform>__<cmd_key>.json  (only on success)
      • agent7/audit/coverage.json                                   (hit/miss stats)
    """
    cfg = load_config()
    paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    hosts = _list_hosts_with_blocks(paths)
    if not hosts:
        _dbg("[inputs] no md-index found; did you run md_splitter.split_task() ?")
        summary = {"hosts": 0, "blocks": 0, "ok": 0, "err": 0}
        _write_json(os.path.join(paths.audit_dir, "coverage.json"), {
            "generated_at": int(time.time()),
            "summary": summary,
            "per_platform": {},
            "errors": [],
        })
        return summary

    per_platform: Dict[str, Dict[str, Any]] = {}
    errors: List[Dict[str, Any]] = []
    total_blocks = ok = err = 0

    for host in hosts:
        blocks = _load_blocks_for_host(paths, host)
        if not blocks:
            continue

        # Choose platform from first block; fallback to unknown
        plat_hint = blocks[0].get("platform_hint", "unknown")
        os_name = _genie_os(plat_hint)

        # Create device once per host/platform
        try:
            dev = _make_offline_device(os_name)
        except Exception as e:
            _dbg(f"[init] host={host} failed to init genie device: {e}")
            for b in blocks:
                total_blocks += 1
                err += 1
                errors.append({"host": host, "command": b.get("sanitized_command"), "error": f"init: {str(e)}"})
                pp = per_platform.setdefault(normalize_platform(plat_hint), {"ok": 0, "err": 0})
                pp["err"] += 1
            continue

        for b in blocks:
            cmd = b.get("sanitized_command") or ""
            txt_path = b.get("text_path") or ""
            cmd_key = b.get("cmd_key") or _safe_cmd_key(cmd)  # tolerate missing
            total_blocks += 1

            if not cmd or not txt_path or not os.path.exists(txt_path):
                err += 1
                errors.append({"host": host, "command": cmd, "error": "skip: missing command/text_path"})
                per_platform.setdefault(normalize_platform(plat_hint), {"ok": 0, "err": 0})["err"] += 1
                continue

            text = _read(txt_path)
            if not text.strip():
                err += 1
                errors.append({"host": host, "command": cmd, "error": "skip: empty output"})
                per_platform.setdefault(normalize_platform(plat_hint), {"ok": 0, "err": 0})["err"] += 1
                continue

            res = _parse_one(dev, cmd, text)
            if res.get("ok"):
                out_path = _output_path(paths, host, plat_hint, cmd_key)
                _write_json(out_path, res.get("data"))
                ok += 1
                per_platform.setdefault(normalize_platform(plat_hint), {"ok": 0, "err": 0})["ok"] += 1
            else:
                err += 1
                errors.append({"host": host, "command": cmd, "error": res.get("error", "unknown")})
                per_platform.setdefault(normalize_platform(plat_hint), {"ok": 0, "err": 0})["err"] += 1

    summary = {"hosts": len(hosts), "blocks": total_blocks, "ok": ok, "err": err}
    cov = {
        "config_dir": config_dir,
        "task_dir": task_dir,
        "generated_at": int(time.time()),
        "summary": summary,
        "per_platform": per_platform,
        "errors": errors[:200],  # cap to keep file small
    }
    _write_json(os.path.join(paths.audit_dir, "coverage.json"), cov)
    _dbg(f"[done] ok={ok} err={err} → {os.path.join(paths.audit_dir, 'coverage.json')}")
    return cov

# ---------------------------
# CLI
# ---------------------------
def _main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/genie_parser.py <config_dir> <task_dir>")
        raise SystemExit(2)
    run(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    _main()