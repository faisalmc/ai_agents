# agents/agent-7/command_plan_builder.py
# Planning phase for Agent-7 (AI-driven, no static rules).
# Emits:
#   • agent7/1-plan/show_cmds.plan.ini
#   • agent7/1-plan/capture_plan.json
from __future__ import annotations

import os, re, json, glob, time
from typing import Any, Dict, List, Set, Optional

# ---- bootstrap (pure imports) ----
from bootstrap import (
    Agent7Config,
    Agent7Paths,
    load_config,
    resolve_paths,
    ensure_dirs,
)

# ---- optional helpers (safe fallbacks; NO hardcoded signal lists) ----
try:
    from agent5_shared import (
        sanitize_show,
        normalize_platform,
        load_lexicon_candidates,
        dbg as _dbg,
    )  # type: ignore
except Exception:  # pragma: no cover
    def _dbg(msg: str) -> None:
        print(f"[agent7][plan] {msg}", flush=True)

    def sanitize_show(cmd: str, platform_hint: str) -> str:
        c = (cmd or "").strip()
        return c if c.lower().startswith("show ") else ""

    def normalize_platform(p: str) -> str:
        p = (p or "").strip().lower()
        if "xr" in p:
            return "cisco-ios-xr"
        if "xe" in p or p == "ios":
            return "cisco-ios"
        return "unknown"

    def load_lexicon_candidates(platform_norm: str) -> List[str]:
        # Lexicon is optional; fallback returns empty
        return []

# ---- assistants (optional) ----
try:
    from signal_harvester import harvest_signals  # type: ignore
except Exception:  # pragma: no cover
    def harvest_signals(config_dir: str, task_dir: str) -> Dict[str, Any]:
        return {}

try:
    from adk_client import ADKClient  # type: ignore
except Exception:  # pragma: no cover
    ADKClient = None  # type: ignore


# ---------------------------
# Canonical plan locations
# ---------------------------
def _plan_dir(paths: Agent7Paths) -> str:
    return os.path.join(paths.agent7_root, "1-plan")

def _plan_ini_path(paths: Agent7Paths) -> str:
    # canonical filename
    return os.path.join(_plan_dir(paths), "show_cmds.plan.ini")

def _plan_json_path(paths: Agent7Paths) -> str:
    return os.path.join(_plan_dir(paths), "capture_plan.json")


# ---------------------------
# Inputs (discovery, no hardcoding)
# ---------------------------
_SHOW_LINE = re.compile(r'(?:^|=)\s*(show\s+.+)$', re.IGNORECASE)

def _load_show_cmds_ini(paths: Agent7Paths) -> List[str]:
    """Read taREMOVEDscoped baseline show_cmds.ini if present."""
    ini_path = os.path.join(paths.task_root, "show_cmds.ini")
    cmds: List[str] = []
    if not os.path.exists(ini_path):
        _dbg(f"[inputs] no show_cmds.ini at {ini_path}")
        return cmds
    seen = set()
    with open(ini_path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            m = _SHOW_LINE.search(line)
            if not m:
                continue
            c = m.group(1).strip()
            if c.lower().startswith("show ") and c.lower() not in seen:
                cmds.append(c)
                seen.add(c.lower())
    _dbg(f"[inputs] show_cmds.ini commands: {len(cmds)}")
    return cmds

def _read_md(paths: Agent7Paths) -> Dict[str, str]:
    """Load original grading logs (observed CLI)."""
    log_dir = os.path.join(paths.task_root, "grading_logs")
    host_to_md: Dict[str, str] = {}
    if not os.path.isdir(log_dir):
        _dbg(f"[inputs] grading_logs not found: {log_dir}")
        return host_to_md
    for p in sorted(glob.glob(os.path.join(log_dir, "*.md"))):
        try:
            txt = open(p, "r", encoding="utf-8").read()
            host = os.path.basename(p).removesuffix(".md")
            host_to_md[host] = txt
        except Exception:
            continue
    _dbg(f"[inputs] loaded md logs: {len(host_to_md)}")
    return host_to_md

def _extract_observed_successful(md_text: str, platform_hint: str) -> List[str]:
    """
    Very light heading/fence parse: keep echoed 'show ...' if code block has non-error output.
    No regex heuristics for signals; strictly structural.
    """
    if not md_text:
        return []
    plat = normalize_platform(platform_hint)
    lines = md_text.splitlines()
    ok: List[str] = []
    i = 0
    while i < len(lines):
        hdr = lines[i].strip()
        if re.match(r"^##\s+show\s+", hdr, re.IGNORECASE):
            # find ``` opening
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                j += 1
            if j >= len(lines):
                i += 1
                continue
            j += 1  # enter block
            block = []
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                block.append(lines[j])
                j += 1
            # echoed command is first non-empty
            k = 0
            while k < len(block) and not block[k].strip():
                k += 1
            if k >= len(block):
                i = j + 1
                continue
            echoed = block[k].strip()
            clean = sanitize_show(echoed, plat)
            if not clean:
                i = j + 1
                continue
            body = "\n".join(block[k + 1 :])
            # simple error guards (no vendor-specific lists)
            if re.search(
                r"%(?:\s*Invalid input detected|\s*Incomplete command|\s*Ambiguous command|\s*Error)",
                body,
                re.IGNORECASE,
            ):
                i = j + 1
                continue
            if re.search(
                r"(?:Unknown|Unrecognized)\s+command|syntax error|Command not supported",
                body,
                re.IGNORECASE,
            ):
                i = j + 1
                continue
            if re.search(r"\S", body):
                ok.append(clean)
        i += 1
    return ok

def _load_facts(paths: Agent7Paths) -> Dict[str, dict]:
    """
    Optional bootstrap from Agent-5 style artifacts when present.
    Never required; planner works without them.
    """
    out: Dict[str, dict] = {}
    audit_facts_dir = os.path.join(paths.task_root, "agent5_audit", "facts")
    if os.path.isdir(audit_facts_dir):
        for p in glob.glob(os.path.join(audit_facts_dir, "*__facts.json")):
            try:
                obj = json.load(open(p, "r", encoding="utf-8"))
                host = obj.get("hostname") or os.path.basename(p).split("__facts.json")[0]
                if host:
                    out[host] = obj
            except Exception:
                pass
    if not out:
        bundle_path = os.path.join(paths.task_root, "agent5_facts.json")
        try:
            arr = json.load(open(bundle_path, "r", encoding="utf-8"))
            if isinstance(arr, list):
                for obj in arr:
                    if isinstance(obj, dict) and obj.get("hostname"):
                        out[obj["hostname"]] = obj
        except Exception:
            pass
    _dbg(f"[inputs] facts hosts: {len(out)}")
    return out

def _infer_platform(md_text: str) -> str:
    if not md_text:
        return "unknown"
    if "RP/" in md_text or "IOS XR" in md_text or "config-bgp" in md_text:
        return "cisco-ios-xr"
    if "Building configuration" in md_text or "IOS Software" in md_text:
        return "cisco-ios"
    return "unknown"

# ---------------------------
# Per-host synthesis (no static signals)
# ---------------------------
def _signals_for_host(host: str, harvested: Dict[str, Any], fallback_md: str, facts: dict) -> List[str]:
    sigs = harvested.get(host, {}).get("signals") if isinstance(harvested, dict) else None
    if isinstance(sigs, list) and sigs:
        # lower, dedupe, stable order
        seen, out = set(), []
        for s in sigs:
            if isinstance(s, str):
                ls = s.strip().lower()
                if ls and ls not in seen:
                    seen.add(ls); out.append(ls)
        return out

    fs = (facts or {}).get("signals_seen") or []
    if isinstance(fs, list) and fs:
        seen, out = set(), []
        for s in fs:
            if isinstance(s, str):
                ls = s.strip().lower()
                if ls and ls not in seen:
                    seen.add(ls); out.append(ls)
        return out

    # last-resort: ultra-light guess from raw text (bootstrap only; still no hardcoded semantics)
    low = (fallback_md or "").lower()
    guesses = []
    for w in ("bgp", "isis", "ospf", "mpls", "evpn", "l2vpn", "sr", "srv6", "bfd", "ip", "intf"):
        if w in low:
            guesses.append(w)
    # dedupe while preserving order
    seen, out = set(), []
    for s in guesses:
        if s not in seen:
            seen.add(s); out.append(s)
    return out

def _platform_for_host(facts: dict, md_text: str) -> str:
    plat = (facts or {}).get("platform_hint") or _infer_platform(md_text)
    return normalize_platform(plat)

def _present_trusted_pool(md_text: str, facts: dict, ini_cmds: List[str]) -> Set[str]:
    pool: Set[str] = set()
    plat = (facts or {}).get("platform_hint", "unknown")
    for c in _extract_observed_successful(md_text or "", plat):
        pool.add(c.lower())
    for c in ((facts or {}).get("trusted_all") or []):
        cc = sanitize_show(c, plat)
        if cc:
            pool.add(cc.lower())
    for c in ini_cmds or []:
        pool.add(c.strip().lower())
    return pool

def _limit(lst: List[str], n: int) -> List[str]:
    if n <= 0:
        return []
    out: List[str] = []
    seen: Set[str] = set()
    for x in lst:
        lx = x.lower()
        if lx not in seen:
            seen.add(lx)
            out.append(x)
        if len(out) >= n:
            break
    return out

# ---------------------------
# Public API
# ---------------------------
def plan_commands(
    *,
    config_dir: str,
    task_dir: str,
    hosts: Optional[List[str]] = None,
    per_signal_limit: int = 3,
    use_adk: bool = True,
    include_lexicon: bool = True,
) -> Dict[str, Any]:
    """
    Main entrypoint. Returns a plan dict and writes:
      • agent7/1-plan/show_cmds.plan.ini
      • agent7/1-plan/capture_plan.json
    """
    cfg: Agent7Config = load_config()
    paths: Agent7Paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)
    os.makedirs(_plan_dir(paths), exist_ok=True)

    ini_cmds = _load_show_cmds_ini(paths)
    md_map = _read_md(paths)
    facts_by = _load_facts(paths)

    # host discovery
    discovered_hosts = sorted(md_map.keys())
    target_hosts = [h for h in (hosts or discovered_hosts) if h]  # explicit beats discovery
    _dbg(f"[plan] target_hosts={len(target_hosts)} (explicit={bool(hosts)})")

    # optional assistants
    harvested = harvest_signals(config_dir, task_dir) if md_map else {}
    adk_client = ADKClient(config_dir, task_dir) if (use_adk and ADKClient is not None) else None

    plan: Dict[str, Any] = {
        "config_dir": config_dir,
        "task_dir": task_dir,
        "generated_at": int(time.time()),
        "per_signal_limit": int(per_signal_limit),
        "hosts": {},
    }

    # per-host synthesis
    for host in target_hosts:
        md_text = md_map.get(host, "")
        fx = facts_by.get(host, {})
        plat = _platform_for_host(fx, md_text)
        signals = _signals_for_host(host, harvested, md_text, fx)
        trusted_pool = _present_trusted_pool(md_text, fx, ini_cmds)

        proposed: Dict[str, List[str]] = {}
        reasons: Dict[str, List[str]] = {}

        # optional lexicon extras
        if include_lexicon:
            try:
                lex_cmds = load_lexicon_candidates(plat)
            except Exception:
                lex_cmds = []
            for c in lex_cmds:
                clean = sanitize_show(c, plat)
                if not clean:
                    continue
                if clean.lower() in trusted_pool:
                    continue
                proposed.setdefault("lexicon", []).append(clean)

        # ADK suggestions per signal (if enabled)
        if adk_client:
            for sig in signals:
                try:
                    cand = adk_client.suggest_canonical_commands(signal=sig, platform=plat) or []
                except Exception:
                    cand = []
                kept: List[str] = []
                for cc in cand:
                    cl = sanitize_show(cc, plat)
                    if not cl:
                        continue
                    if cl.lower() in trusted_pool:
                        continue
                    kept.append(cl)
                if kept:
                    proposed.setdefault(sig, []).extend(_limit(kept, per_signal_limit))
                    reasons.setdefault(sig, []).append("adk_suggest")

        # flatten & dedupe against trusted/baseline
        final_cmds: List[str] = []
        for sig in signals:
            if sig in proposed:
                final_cmds.extend(proposed[sig])
        if "lexicon" in proposed:
            final_cmds.extend(_limit(proposed["lexicon"], per_signal_limit))

        uniq: List[str] = []
        seen: Set[str] = set([c.lower() for c in ini_cmds])
        for c in final_cmds:
            lc = c.lower()
            if lc not in seen and lc not in trusted_pool:
                uniq.append(c)
                seen.add(lc)

        plan["hosts"][host] = {
            "platform": plat,
            "signals": signals,
            "added": uniq,
            "present_count": len(trusted_pool),
            "reasons": reasons,
        }

    # write INI
    ini_lines: List[str] = []
    ini_lines.append("# --- GENERATED by Agent-7 command_plan_builder ---")
    ini_lines.append("# Read-only overlay for Agent-4 capture, grouped by host/signal (comments only).")
    for host in target_hosts:
        info = plan["hosts"].get(host, {})
        sigs = ", ".join(info.get("signals") or []) or "(none)"
        ini_lines.append(f"\n# host: {host}  platform: {info.get('platform','unknown')}  signals: {sigs}")
        for cmd in info.get("added") or []:
            ini_lines.append(cmd)

    ini_path = _plan_ini_path(paths)
    with open(ini_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(ini_lines) + "\n")

    # write plan JSON (capture driver uses this)
    json_path = _plan_json_path(paths)
    out = {
        **plan,
        "ini_path": os.path.abspath(ini_path),
        "selected_hosts": target_hosts,
    }
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    _dbg(f"[write] ini={ini_path} json={json_path} hosts={len(target_hosts)}")
    return out

# ---------------------------
# CLI
# ---------------------------
def _main():
    """
    Usage:
      python agents/agent-7/command_plan_builder.py <config_dir> <task_dir> [host1,host2,...]
    """
    import sys
    if len(sys.argv) < 3:
        print("Usage: python agents/agent-7/command_plan_builder.py <config_dir> <task_dir> [host_csv]")
        raise SystemExit(2)
    config_dir, task_dir = sys.argv[1], sys.argv[2]
    hosts = []
    if len(sys.argv) >= 4 and sys.argv[3].strip():
        hosts = [h.strip() for h in sys.argv[3].split(",") if h.strip()]

    # env toggles (all optional)
    per_signal_limit = int(os.getenv("AGENT7_PLAN_PER_SIGNAL_LIMIT", "3"))
    use_adk = os.getenv("AGENT7_USE_ADK", "1").lower() not in ("0", "false", "no")
    include_lexicon = os.getenv("AGENT7_INCLUDE_LEXICON", "1").lower() not in ("0", "false", "no")

    obj = plan_commands(
        config_dir=config_dir,
        task_dir=task_dir,
        hosts=hosts or None,
        per_signal_limit=per_signal_limit,
        use_adk=use_adk,
        include_lexicon=include_lexicon,
    )
    print(json.dumps(obj, indent=2))

if __name__ == "__main__":
    _main()