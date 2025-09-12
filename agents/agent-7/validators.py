# ai_agents/agents/agent-7/validators.py
from __future__ import annotations
import os, json
from typing import Any, Dict, List, Tuple

# ---------------------------
# tiny io helpers
# ---------------------------
def read_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)

# ---------------------------
# structural helpers
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

def is_safe_command(cmd: str, allow_active: bool = True) -> bool:
    c = (cmd or "").strip().lower()
    if not c:
        return False
    if c.startswith("show "):
        return True
    if allow_active and (c.startswith("ping ") or c.startswith("traceroute ")):
        return True
    # block config/clear/reload/debug/copy/monitor etc. by default
    for bad in ("configure", "conf t", "clear ", "reload", "debug", "copy ", "write ", "monitor "):
        if c.startswith(bad):
            return False
    return False

def validate_evidence_ref(facts: Dict[str, Any], evidence_ref: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Facts schema: commands.<cmd_key>.data...
    evidence_ref: { "command_key": "<cmd_key>", "path": "commands.<cmd_key>.data...." }
    """
    if not isinstance(evidence_ref, dict):
        return False, "evidence_ref:not_dict"
    cmd_key = (evidence_ref.get("command_key") or "").strip()
    path    = (evidence_ref.get("path") or "").strip()
    if not cmd_key or not path:
        return False, "evidence_ref:missing_fields"
    if not path.startswith(f"commands.{cmd_key}."):
        return False, "evidence_ref:bad_prefix"
    ok, _ = _dot_get(facts, path)
    if not ok:
        return False, "evidence_ref:no_such_path"
    return True, ""

# ---------------------------
# per-device validation
# ---------------------------
def validate_per_device_output(obj: Dict[str, Any], facts: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Drops findings with invalid evidence_ref and filters unsafe commands.
    Does not enforce any protocol rules; purely structural.
    """
    errors: List[str] = []
    cleaned = dict(obj or {})

    # Findings
    kept_findings: List[Dict[str, Any]] = []
    for f in (cleaned.get("findings") or []):
        ok, reason = validate_evidence_ref(facts, f.get("evidence_ref") or {})
        if ok:
            kept_findings.append(f)
        else:
            errors.append(f"drop_finding:{reason}")
    cleaned["findings"] = kept_findings

    # Commands
    recs  = [c for c in (cleaned.get("recommended_show_cmds") or []) if is_safe_command(c, allow_active=False)]
    probes = [c for c in (cleaned.get("optional_active_cmds") or []) if is_safe_command(c, allow_active=True)]
    cleaned["recommended_show_cmds"] = recs
    cleaned["optional_active_cmds"]  = probes

    # Basic fields
    if not isinstance(cleaned.get("signals_seen"), list):
        cleaned["signals_seen"] = []
    if not cleaned.get("platform"):
        cleaned["platform"] = facts.get("platform_hint", "unknown")
    if not cleaned.get("hostname"):
        cleaned["hostname"] = facts.get("hostname", "unknown")

    return cleaned, errors

# ---------------------------
# cross-device validation
# ---------------------------
def validate_cross_device_output(result: Dict[str, Any], facts_by_host: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Ensures incidents reference only known hosts and valid fact paths.
    Filters unsafe commands.
    """
    errors: List[str] = []
    cleaned = dict(result or {})
    known = set(facts_by_host.keys())

    # Guard simple fields
    cleaned["task_status"] = cleaned.get("task_status") or "unknown"
    cleaned["remediation_themes"] = cleaned.get("remediation_themes") or []

    def _guard_cmds(cmds: List[str], allow_active: bool = False) -> List[str]:
        return [c for c in (cmds or []) if is_safe_command(c, allow_active=allow_active)]

    cleaned["trusted_followup_cmds"]    = _guard_cmds(cleaned.get("trusted_followup_cmds") or [], allow_active=False)
    cleaned["unvalidated_followup_cmds"]= _guard_cmds(cleaned.get("unvalidated_followup_cmds") or [], allow_active=False)
    cleaned["optional_active_probes"]   = _guard_cmds(cleaned.get("optional_active_probes") or [], allow_active=True)

    # Incidents
    kept: List[Dict[str, Any]] = []
    for inc in (cleaned.get("top_incidents") or []):
        devs = [d for d in (inc.get("devices") or []) if d in known]
        if not devs and inc.get("devices"):
            errors.append("drop_incident:unknown_devices")
            continue

        ev_new: List[Dict[str, Any]] = []
        ev_ok = True
        for ev in (inc.get("evidence") or []):
            host = (ev.get("host") or "").strip()
            path = (ev.get("path") or "").strip()
            if not host or host not in known:
                ev_ok = False
                errors.append("drop_incident:bad_evidence_host")
                break
            ok, reason = validate_evidence_ref(facts_by_host.get(host) or {}, {"command_key": path.split(".")[1] if path.startswith("commands.") else "", "path": path})
            if not ok:
                ev_ok = False
                errors.append(f"drop_incident:{reason}")
                break
            ev_new.append({"host": host, "path": path})
        if ev_ok:
            if devs:
                inc["devices"] = devs
            if ev_new:
                inc["evidence"] = ev_new
            kept.append(inc)

    cleaned["top_incidents"] = kept
    return cleaned, errors

# ---------------------------
# simple CLI (optional)
# ---------------------------
def _main():
    import sys, glob
    if len(sys.argv) < 3:
        print("Usage:\n  python agents/agent-7/validators.py per <facts.json> <per_device.json>\n  python agents/agent-7/validators.py cross <facts_dir> <cross_device.json>")
        raise SystemExit(2)

    mode = sys.argv[1]
    if mode == "per":
        facts_p, per_p = sys.argv[2], sys.argv[3]
        facts = read_json(facts_p) or {}
        obj   = read_json(per_p) or {}
        cleaned, errs = validate_per_device_output(obj, facts)
        out_p = per_p.replace(".json", ".validated.json")
        write_json(out_p, cleaned)
        print(json.dumps({"out": out_p, "errors": errs}, indent=2))
    elif mode == "cross":
        facts_dir, cross_p = sys.argv[2], sys.argv[3]
        facts_by_host = {}
        for fp in glob.glob(os.path.join(facts_dir, "*.json")):
            f = read_json(fp) or {}
            h = f.get("hostname") or os.path.splitext(os.path.basename(fp))[0]
            facts_by_host[h] = f
        obj = read_json(cross_p) or {}
        cleaned, errs = validate_cross_device_output(obj, facts_by_host)
        out_p = cross_p.replace(".json", ".validated.json")
        write_json(out_p, cleaned)
        print(json.dumps({"out": out_p, "errors": errs}, indent=2))
    else:
        print("mode must be 'per' or 'cross'")
        raise SystemExit(2)

if __name__ == "__main__":
    _main()