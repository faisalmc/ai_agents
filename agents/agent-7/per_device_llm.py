# agents/agent-7/per_device_llm.py
from __future__ import annotations
import os, json, glob, time
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------
# Plain bootstrap imports (no dynamic loaders)
# ---------------------------
from bootstrap import Agent7Config, Agent7Paths, load_config, resolve_paths, ensure_dirs

# ---------------------------
# LLM wrapper (graceful fallback if missing)
# ---------------------------
try:
    from shared.llm_api import call_llm  # type: ignore
except Exception:
    call_llm = None  # degrade gracefully

# ---------------------------
# Validators (centralized gating & safety)
# ---------------------------
try:
    from validators import validate_per_device_output  # type: ignore
except Exception:
    # Fallback: no-op validator (keeps compatibility if file missing)
    def validate_per_device_output(obj: Dict[str, Any], facts: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        return obj, []

# ---------------------------
# Debug
# ---------------------------
def _dbg(msg: str) -> None:
    print(f"[agent7][per-device] {msg}", flush=True)

# ---------------------------
# IO helpers
# ---------------------------
def _read_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)

def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)

def _list_facts(paths: Agent7Paths) -> List[str]:
    """
    Reads facts from the configured facts directory.
    Your bootstrap should resolve this to agent7/3-analyze/2-facts/*.json.
    """
    return sorted(glob.glob(os.path.join(paths.facts_dir, "*.json")))

def _read_agent1_row(agent1_row_path: Optional[str], host: str) -> Optional[Dict[str, Any]]:
    if not agent1_row_path:
        return None
    arr = _read_json(agent1_row_path)
    if isinstance(arr, list):
        for row in arr:
            if isinstance(row, dict) and row.get("hostname") == host:
                return row
    return None

def _read_adk_snippets(adk_cache_path: Optional[str],
                       signals: List[str],
                       platform_hint: str) -> List[Dict[str, str]]:
    """
    Best-effort: read ADK cache (if present) and return a few relevant snippets.
    Expected format (array of objects with at least title/url/snippet and optional tags).
    """
    if not adk_cache_path:
        return []
    arr = _read_json(adk_cache_path) or []
    if not isinstance(arr, list):
        return []
    sigset = {str(s).lower() for s in (signals or [])}
    plat = (platform_hint or "unknown").lower()
    out: List[Dict[str, str]] = []
    for row in arr:
        if not isinstance(row, dict):
            continue
        tags = {str(t).lower() for t in (row.get("tags") or [])}
        # light matching: prefer platform/tag overlap or vendor tag
        if plat in " ".join(tags) or "cisco" in tags or (sigset & tags):
            out.append({
                "title": row.get("title", ""),
                "url": row.get("url", ""),
                "snippet": row.get("snippet", ""),
            })
        if len(out) >= 6:
            break
    return out

def _compact_facts_for_prompt(facts: Dict[str, Any], soft_limit_chars: int = 45000) -> str:
    s = json.dumps(facts, ensure_ascii=False)
    return s[:soft_limit_chars]

# ---------------------------
# Prompt builders (LLM-first)
# ---------------------------
_SYS = """You are a senior Cisco SP NOC engineer.
You will analyze structured FACTS produced from parsed CLI (pyATS Genie or LLM). You MUST:
- Use only the provided facts as evidence; do NOT invent information.
- Return STRICT JSON only (no prose) with this schema:
{
  "hostname": "<string>",
  "platform": "ios-xr" | "ios" | "unknown",
  "signals_seen": ["bgp","isis","mpls","evpn","l2vpn","sr","srv6","intf","ip","bfd", ...],
  "status": "healthy" | "degraded" | "error" | "unknown",
  "status_reason": "<short explanation tied to evidence, not to parsing availability>",
  "ok": [
    {
      "summary": "<what looks healthy (1 line)>",
      "evidence_ref": { "command_key": "<cmd_key>", "path": "commands.<cmd_key>.<...>" }
    }
  ],
  "suspect": [
    {
      "summary": "<what looks off (1 line)>",
      "evidence_ref": { "command_key": "<cmd_key>", "path": "commands.<cmd_key>.<...>" }
    }
  ],
  "findings": [
    {
      "signal": "<one of signals_seen>",
      "severity": "info" | "warn" | "error",
      "summary": "<short, evidence-backed>",
      "evidence_ref": {
        "command_key": "<cmd_key from facts.commands>",
        "path": "commands.<cmd_key>.<...>"  // MUST point to a real path in facts
      }
    }
  ],
  "recommended_show_cmds": ["show ..."],
  "optional_active_cmds": ["ping ..."]
}
Rules:
- Evidence must reference REAL paths in the provided facts (start with commands.<cmd_key>.).
- Do NOT mark status as degraded/error just because a parser is unavailable or parser_ok=false.
  If tables/metrics/evidence_text exist and clearly show healthy behavior, treat that as valid evidence.
- Prefer listing both positives (ok[]) and negatives (suspect[]) so the operator sees what's working and what's not.
- status_reason must reflect network state (e.g., "some BGP neighbors Idle while others Established"), NOT "parser not found".
- Be conservative: if unclear, use severity "info".
- Never propose config/debug/clear/reload commands.
"""

def _available_command_keys(facts: Dict[str, Any]) -> List[str]:
    cmds = (facts or {}).get("commands") or {}
    if isinstance(cmds, dict):
        return sorted([k for k in cmds.keys() if isinstance(k, str)])
    return []

def _build_messages(host: str,
                    facts: Dict[str, Any],
                    agent1_row: Optional[Dict[str, Any]],
                    adk_snips: List[Dict[str,str]]) -> List[Dict[str,str]]:
    ctx = {
        "hostname": host,
        "platform_hint": facts.get("platform_hint", "unknown"),
        "signals_seen": facts.get("signals_seen", []),
        "available_command_keys": _available_command_keys(facts),
        "agent1_summary": agent1_row or {},
        "adk_snippets": adk_snips,
        "facts_json": _compact_facts_for_prompt(facts),
    }
    user = "### Context\n```json\n" + json.dumps(ctx, indent=2) + "\n```"
    return [
        {"role": "system", "content": _SYS},
        {"role": "user", "content": user},
    ]

# ---------------------------
# Status fallback (only if LLM is empty/unknown)
# ---------------------------
def _status_from_findings(findings: List[Dict[str, Any]], has_evidence: bool) -> str:
    if not findings:
        return "healthy" if has_evidence else "unknown"
    sev_rank = {"error": 3, "warn": 2, "info": 1}
    top = 0
    for f in findings:
        top = max(top, sev_rank.get(str(f.get("severity", "info")).lower(), 1))
    if top >= 3:
        return "error"
    if top == 2:
        return "degraded"
    return "healthy"

# ---------------------------
# Public API (stable names)
# ---------------------------
def analyze_host(*,
                 hostname: str,
                 facts: Dict[str, Any],
                 agent1_row_path: Optional[str] = None,
                 adk_cache_path: Optional[str] = None,
                 out_prompt_path: Optional[str] = None,
                 out_raw_path: Optional[str] = None) -> Dict[str, Any]:
    host = hostname or facts.get("hostname") or "unknown"
    agent1 = _read_agent1_row(agent1_row_path, host)
    adk   = _read_adk_snippets(adk_cache_path, facts.get("signals_seen") or [], facts.get("platform_hint","unknown"))

    msgs = _build_messages(host, facts, agent1, adk)

    if out_prompt_path:
        _write_text(out_prompt_path, f"--- SYSTEM ---\n{_SYS}\n\n--- USER ---\n{msgs[1]['content']}\n")

    # ---- call LLM ----
    if call_llm is None:
        raw = ""
    else:
        try:
            raw = call_llm(msgs, temperature=0.0) or ""
        except Exception as e:
            _dbg(f"[llm] call failed: {e}")
            raw = ""

    if out_raw_path:
        _write_text(out_raw_path, raw if isinstance(raw, str) else json.dumps(raw, indent=2))

    # ---- parse LLM output (dict OR JSON string; also handle ```json fences) ----
    obj: Dict[str, Any]
    try:
        if isinstance(raw, dict):
            obj = raw
        else:
            txt = (raw or "")
            # strip triple backtick fences if present
            t = txt.strip()
            if t.startswith("```"):
                lines = t.splitlines()
                # drop first line (``` or ```json) and any trailing ``` line
                if lines:
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                t = "\n".join(lines).strip()
            obj = json.loads(t)  # may raise
            if not isinstance(obj, dict):
                raise ValueError("non-dict")
    except Exception:
        obj = {
            "hostname": host,
            "platform": facts.get("platform_hint", "unknown"),
            "signals_seen": facts.get("signals_seen", []),
            "status": "unknown",
            "status_reason": "LLM output unavailable or not JSON",
            "ok": [],
            "suspect": [],
            "findings": [{"signal": "meta", "severity": "info", "summary": "LLM output unavailable or not JSON"}],
            "recommended_show_cmds": [],
            "optional_active_cmds": []
        }

    # ---- centralized validation ----
    cleaned, _errs = validate_per_device_output(obj, facts)

    # ---- preserve LLM status when present; otherwise roll up from findings ----
    cov = facts.get("coverage") or {}
    has_evidence = bool(cov.get("total_cmds")) or bool(facts.get("commands"))
    llm_status = (cleaned.get("status") or "").strip().lower()
    if not llm_status or llm_status == "unknown":
        cleaned["status"] = _status_from_findings(cleaned.get("findings") or [], has_evidence)

    # ensure platform/signals/hostname
    if not cleaned.get("platform"):
        cleaned["platform"] = facts.get("platform_hint", "unknown")
    if not cleaned.get("signals_seen"):
        cleaned["signals_seen"] = facts.get("signals_seen", [])
    cleaned["hostname"] = cleaned.get("hostname") or host

    return cleaned

# ------------------------------------------------------
# A) agents/agent-7/per_device_llm.py — ADD a host-scoped runner
# ------------------------------------------------------

def _list_facts_for_hosts(paths: Agent7Paths, hosts: List[str]) -> List[str]:
    hostset = {h.strip() for h in hosts or [] if isinstance(h, str) and h.strip()}
    out = []
    for fp in _list_facts(paths):
        base = os.path.basename(fp)
        host = base[:-5] if base.endswith(".json") else os.path.splitext(base)[0]
        if host in hostset:
            out.append(fp)
    return sorted(out)


def run_hosts(config_dir: str, task_dir: str, hosts: List[str]) -> Dict[str, Any]:
    """
    Host-scoped per-device analysis.
    - Reads facts only for `hosts`.
    - Writes a separate scoped per_device JSON (does NOT merge with the global file).
    - Returns the same shape as run(), but with 'path' pointing to the scoped file.
    """
    cfg: Agent7Config = load_config()
    paths: Agent7Paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    facts_paths = _list_facts_for_hosts(paths, hosts)
    results: List[Dict[str, Any]] = []
    for fp in facts_paths:
        try:
            res = _analyze_one_host(paths, fp)
            results.append(res)
            _dbg(f"[host] {res.get('hostname','?')} status={res.get('status','?')} findings={len(res.get('findings') or [])}")
        except Exception as e:
            _dbg(f"[error] analyzing {os.path.basename(fp)}: {e}")

    # Write to a scoped file to avoid contaminating the global per_device.json
    import hashlib, json as _json
    id_src = "|".join(sorted([r.get("hostname","") for r in results])) or "|".join(sorted(hosts or []))
    short_id = hashlib.sha1(id_src.encode("utf-8", errors="ignore")).hexdigest()[:8]
    out_p = os.path.join(paths.analyze_dir, f"per_device__scoped__{short_id}.json")

    _write_json(out_p, results)
    _dbg(f"[done] wrote {out_p} (hosts={len(results)})")
    return {"hosts": len(results), "path": out_p, "generated_at": int(time.time())}

# ---------------------------
# Internal: iterate facts dir and write per_device.json
# ---------------------------
def _analyze_one_host(paths: Agent7Paths, facts_path: str) -> Dict[str, Any]:
    facts = _read_json(facts_path) or {}
    host = facts.get("hostname") or os.path.splitext(os.path.basename(facts_path))[0]

    # default locations for optional inputs/audits
    agent1_row_path = os.path.join(paths.task_root, "agent1_summary.json")
    adk_cache_path  = os.path.join(paths.audit_dir, "adk_cache.json")
    out_prompt_path = os.path.join(paths.audit_dir, f"{host}__per_device_prompt.txt")
    out_raw_path    = os.path.join(paths.audit_dir, f"{host}__per_device_raw.json")

    return analyze_host(
        hostname=host,
        facts=facts,
        agent1_row_path=agent1_row_path,
        adk_cache_path=adk_cache_path,
        out_prompt_path=out_prompt_path,
        out_raw_path=out_raw_path,
    )

def run(config_dir: str, task_dir: str) -> Dict[str, Any]:
    """
    Reads facts (paths.facts_dir), analyzes each host, and writes:
      - paths.per_device_json
      - agent7/audit/<host>__per_device_prompt.txt
      - agent7/audit/<host>__per_device_raw.json
    """
    cfg: Agent7Config = load_config()
    paths: Agent7Paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    results: List[Dict[str, Any]] = []
    for fp in _list_facts(paths):
        try:
            res = _analyze_one_host(paths, fp)
            results.append(res)
            _dbg(f"[host] {res.get('hostname','?')} status={res.get('status','?')} findings={len(res.get('findings') or [])}")
        except Exception as e:
            _dbg(f"[error] analyzing {os.path.basename(fp)}: {e}")

    # merge/update per-device rollup (stable location via bootstrap)
    out_p = paths.per_device_json
    prev = _read_json(out_p)
    if isinstance(prev, list):
        prev_by_host = {d.get("hostname"): d for d in prev if isinstance(d, dict)}
        for r in results:
            prev_by_host[r.get("hostname")] = r
        merged = list(prev_by_host.values())
    else:
        merged = results

    _write_json(out_p, merged)
    _dbg(f"[done] wrote {out_p} (hosts={len(merged)})")
    return {"hosts": len(merged), "path": out_p, "generated_at": int(time.time())}

# ---------------------------
# CLI
# ---------------------------
def _main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/per_device_llm.py <config_dir> <task_dir>")
        raise SystemExit(2)
    run(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    _main()