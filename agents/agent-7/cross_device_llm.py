# ai_agents/agents/agent-7/cross_device_llm.py
from __future__ import annotations
import os, json, glob, time
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------
# Simple logging
# ---------------------------
def _dbg(msg: str) -> None:
    print(f"[agent7][cross] {msg}", flush=True)

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
# Small IO helpers
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
    Read facts from the configured facts directory.
    Your bootstrap should resolve this to agent7/3-analyze/2-facts/*.json (per agreement).
    """
    return sorted(glob.glob(os.path.join(paths.facts_dir, "*.json")))

def _compact(s: str, limit: int) -> str:
    return s if len(s) <= limit else s[:limit]

# ---------------------------
# Evidence validation against facts
# ---------------------------
def _dot_get(obj: Any, dot_path: str) -> Tuple[bool, Any]:
    cur = obj
    if not dot_path:
        return True, cur
    for part in dot_path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False, None
    return True, cur

def _validate_incidents(
    incidents: List[Dict[str, Any]],
    facts_by_host: Dict[str, Dict[str, Any]],
    known_hosts: set,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Keep only incidents whose devices are known and whose evidence entries
    reference existing paths in corresponding facts.

    Evidence item schema (required):
      { "host": "<hostname>", "path": "commands.<cmd_key>.<...>" }
    """
    kept, errs = [], []
    for inc in (incidents or []):
        # devices: restrict to known hosts; drop incident if none left
        devs_in = inc.get("devices") or []
        devs = [d for d in devs_in if d in known_hosts]
        if devs_in and not devs:
            errs.append("drop_incident_unknown_devices")
            continue

        # evidence: each must point to an existing dot path under that host's facts
        ev_ok = True
        new_ev = []
        for ev in (inc.get("evidence") or []):
            host = (ev.get("host") or "").strip()
            path = (ev.get("path") or "").strip()
            if not host or not path or host not in known_hosts:
                ev_ok = False
                errs.append(f"bad_evidence_host({host})")
                break
            if not path.startswith("commands."):
                ev_ok = False
                errs.append(f"bad_evidence_path_prefix({path})")
                break
            facts = facts_by_host.get(host) or {}
            ok, _ = _dot_get(facts, path)
            if not ok:
                ev_ok = False
                errs.append(f"no_such_path({host}:{path})")
                break
            new_ev.append({"host": host, "path": path})

        if ev_ok:
            inc["devices"] = devs
            if new_ev:
                inc["evidence"] = new_ev
            kept.append(inc)

    return kept, errs

def _guard_followups(cmds: List[str]) -> List[str]:
    """
    Allow only safe read-only or active probe commands.
    """
    out = []
    for c in cmds or []:
        cc = (c or "").strip().lower()
        if cc.startswith("show ") or cc.startswith("ping ") or cc.startswith("traceroute "):
            out.append(c.strip())
    return out

# ---------------------------
# Helpers: available command keys (for evidence_ref accuracy)
# ---------------------------
def _available_keys_by_host(facts_by_host: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for h, f in (facts_by_host or {}).items():
        try:
            cmds = f.get("commands") or {}
            if isinstance(cmds, dict):
                out[h] = sorted([k for k in cmds.keys() if isinstance(k, str)])
        except Exception:
            pass
    return out

# ---------------------------
# Prompt builders
# ---------------------------
_SYS = """You are a senior NOC service lead.
Inputs:
  • per_device: list of per-device analyses (validated, evidence-backed)
  • facts_by_host: map host → FACTS (parsed CLI via Genie)
  • available_command_keys_by_host: map host → valid commands.<cmd_key> keys

Your job: correlate across devices and produce an operator-ready summary that clearly states BOTH:
  1) what is working, and
  2) what is broken or suspicious.

Hard rules:
- Use only devices present in the input; do NOT invent names.
- Every incident MUST include an "evidence" list; each item:
    { "host": "<hostname>", "path": "commands.<cmd_key>.<...>" }
  and MUST resolve to a real path in that host’s facts.
- Output STRICT JSON only (no extra fields, no prose outside fields) with this schema:

{
  "network_summary": "<1–2 short lines. Sentence 1: overall status using counts. Sentence 2: one working highlight and one issue highlight, if any.>",
  "status_rollup": { "healthy": <int>, "degraded": <int>, "error": <int>, "unknown": <int> },
  "top_incidents": [
    {
      "scope": "pair" | "site" | "global",
      "summary": "<short finding>",
      "impact": "<who/what is affected>",
      "devices": ["<host>", "..."],
      "evidence": [ { "host": "<host>", "path": "commands.<cmd_key>.<...>" }, ... ]
    }
  ],
  "notable_devices": [
    {
      "host": "<hostname>",
      "status": "healthy" | "degraded" | "error" | "unknown",
      "note": "<≤1 line: include both positives (e.g., 'some peers Established') and negatives (e.g., 'others Idle') when mixed.>",
      "evidence": { "host": "<hostname>", "path": "commands.<cmd_key>.<...>" }
    }
  ],
  "remediation_themes": ["..."],
  "trusted_followup_cmds": ["show ..."],        // safe, read-only
  "unvalidated_followup_cmds": ["show ..."],    // ideas, still read-only
  "optional_active_probes": ["ping ...", "traceroute ..."],
  "task_status": "healthy" | "mixed" | "degraded" | "error" | "unknown"
}

Guidance:
- Derive status_rollup by counting per_device[].status exactly.
- Set task_status from the rollup:
    • "healthy" if all healthy;
    • "error" if any error;
    • "degraded" if none error but any degraded;
    • "mixed" if a mix of healthy + unknown only, or mixed healthy/degraded without clear single label;
    • "unknown" if all unknown.
- network_summary MUST be balanced: one sentence on overall counts; one sentence that mentions at least one “working” example (if any healthy) AND at least one “issue” example (if any degraded/error). If nothing degraded/error, say so.
- Choose up to 5 notable_devices (mix of best and worst). Each must include exactly one evidence path that exists for that host.
- For incidents, prefer concise, high-signal patterns (0–3 items). If you cannot provide valid evidence paths, return an empty list rather than guessing.
- Only propose read-only follow-ups (show …) or safe probes (ping/traceroute). Never config/clear/reload/debug/copy/write/monitor.
- Keep all text brief and specific. Paths MUST start with commands.<cmd_key>. and use keys listed for that host when possible.
"""

def _build_messages(per_device_objs: List[Dict[str, Any]],
                    facts_for_prompt: Dict[str, str],
                    keys_by_host: Dict[str, List[str]]) -> List[Dict[str, str]]:
    ctx = {
        "per_device": per_device_objs,
        "facts_by_host": facts_for_prompt,  # each value is JSON string (may be truncated)
        "available_command_keys_by_host": keys_by_host
    }
    user = "```json\n" + json.dumps(ctx, indent=2) + "\n```"
    return [
        {"role": "system", "content": _SYS},
        {"role": "user", "content": user},
    ]

# ---------------------------
# Public API (stable): analyze_all
# ---------------------------
def analyze_all(
    *,
    per_device_rows: List[Dict[str, Any]],
    facts_by_host: Dict[str, Dict[str, Any]],
    out_prompt_path: Optional[str] = None,
    out_raw_path: Optional[str] = None,
    validation_log_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Correlates multiple per-device analyses + facts.
    - per_device_rows: list of per-device JSON objects
    - facts_by_host: {hostname: facts dict}
    - out_*_path: optional audit outputs
    Returns CLEANED dict ready to persist.
    """
    # Build prompt payload
    facts_for_prompt: Dict[str, str] = {}
    known_hosts: set = set(facts_by_host.keys())

    for h, fobj in facts_by_host.items():
        try:
            facts_for_prompt[h] = _compact(json.dumps(fobj, ensure_ascii=False), 45000)
        except Exception:
            facts_for_prompt[h] = "{}"

    # Include hosts from per-device rows (in case facts & per_device differ)
    for row in per_device_rows or []:
        if isinstance(row, dict):
            h = str(row.get("hostname", "")).strip()
            if h:
                known_hosts.add(h)

    keys_by_host = _available_keys_by_host(facts_by_host)
    msgs = _build_messages(per_device_rows or [], facts_for_prompt, keys_by_host)

    # Audit prompt if requested
    if out_prompt_path:
        _write_text(out_prompt_path, f"--- SYSTEM ---\n{_SYS}\n\n--- USER ---\n{msgs[1]['content']}\n")

    # Call LLM (graceful fallback)
    if call_llm is None:
        raw = ""
    else:
        try:
            raw = call_llm(msgs, temperature=0.0) or ""
        except Exception as e:
            _dbg(f"[llm] call failed: {e}")
            raw = ""

    if out_raw_path:
        _write_text(out_raw_path, raw if isinstance(raw, str) else json.dumps(raw))

    # # Parse JSON strictly; fallback skeleton
    # try:
    #     result = json.loads(raw)
    #     if not isinstance(result, dict):
    #         raise ValueError("non-dict")
    # except Exception:
    #     result = {
    #         "network_summary": "",
    #         "status_rollup": {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0},
    #         "top_incidents": [],
    #         "notable_devices": [],
    #         "remediation_themes": [],
    #         "trusted_followup_cmds": [],
    #         "unvalidated_followup_cmds": [],
    #         "optional_active_probes": [],
    #         "task_status": "unknown"
    #     }
    # ---- parse LLM output (dict OR JSON string; also handle ```json fences) ----
    try:
        if isinstance(raw, dict):
            result = raw
        else:
            t = (raw or "").strip()
            if t.startswith("```"):
                lines = t.splitlines()
                if lines:
                    lines = lines[1:]           # drop ``` or ```json
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]          # drop closing ```
                t = "\n".join(lines).strip()
            result = json.loads(t)
            if not isinstance(result, dict):
                raise ValueError("non-dict")
    except Exception:
        result = {
            "network_summary": "",
            "status_rollup": {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0},
            "top_incidents": [],
            "notable_devices": [],
            "remediation_themes": [],
            "trusted_followup_cmds": [],
            "unvalidated_followup_cmds": [],
            "optional_active_probes": [],
            "task_status": "unknown"
        }

    # Guard outputs we rely on downstream
    result["network_summary"] = result.get("network_summary") or ""
    # Leave status_rollup as-is if provided; otherwise keep default shape
    if not isinstance(result.get("status_rollup"), dict):
        result["status_rollup"] = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
    
    # ---- derive status_rollup from per_device if LLM omitted or malformed ----
    roll = result.get("status_rollup")
    if not isinstance(roll, dict) or not roll:
        cnt = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
        for row in (per_device_rows or []):
            s = str((row or {}).get("status") or "unknown").lower()
            cnt[s] = cnt.get(s, 0) + 1
        result["status_rollup"] = cnt

    result["remediation_themes"] = result.get("remediation_themes") or []
    result["trusted_followup_cmds"] = _guard_followups(result.get("trusted_followup_cmds") or [])
    result["unvalidated_followup_cmds"] = _guard_followups(result.get("unvalidated_followup_cmds") or [])
    result["optional_active_probes"] = _guard_followups(result.get("optional_active_probes") or [])
    result["task_status"] = result.get("task_status") or "unknown"

    # Validate incidents against facts
    incidents = result.get("top_incidents") or []
    kept, errs = _validate_incidents(incidents, facts_by_host, known_hosts)
    result["top_incidents"] = kept

    if errs and validation_log_path:
        _write_text(validation_log_path, "\n".join(errs))

    return result

# ---------------------------
# Orchestrator: run(config_dir, task_dir)
# ---------------------------
def run(config_dir: str, task_dir: str) -> Dict[str, Any]:
    """
    Loads per-device and facts from disk, runs analyze_all, writes:
      - paths.cross_device_json
      - agent7/audit/cross_prompt.txt
      - agent7/audit/cross_raw.json
      - agent7/audit/cross_validation.log (if any)
    """
    cfg: Agent7Config = load_config()
    paths: Agent7Paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    # Load per-device
    per_device_path = paths.per_device_json
    per_device_rows = _read_json(per_device_path) or []
    if not isinstance(per_device_rows, list):
        per_device_rows = []

    # Load all facts
    facts_by_host: Dict[str, Dict[str, Any]] = {}
    for fp in _list_facts(paths):
        fobj = _read_json(fp) or {}
        host = fobj.get("hostname") or os.path.splitext(os.path.basename(fp))[0]
        facts_by_host[host] = fobj

    # Audit paths
    prompt_p = os.path.join(paths.audit_dir, "cross_prompt.txt")
    raw_p    = os.path.join(paths.audit_dir, "cross_raw.json")
    v_log_p  = os.path.join(paths.audit_dir, "cross_validation.log")

    # Run correlation
    result = analyze_all(
        per_device_rows=per_device_rows,
        facts_by_host=facts_by_host,
        out_prompt_path=prompt_p,
        out_raw_path=raw_p,
        validation_log_path=v_log_p,
    )

    # Persist cleaned result
    out_p = paths.cross_device_json
    _write_json(out_p, result)
    _dbg(f"[done] wrote {out_p} (incidents={len(result.get('top_incidents') or [])})")

    return {
        "path": out_p,
        "incidents": len(result.get("top_incidents") or []),
        "generated_at": int(time.time())
    }

# ---------------------------
# CLI
# ---------------------------
def _main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/cross_device_llm.py <config_dir> <task_dir>")
        raise SystemExit(2)
    run(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    _main()