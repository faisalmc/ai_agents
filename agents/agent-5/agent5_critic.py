# agent5_critic.py
import os, copy
from agent5_shared import dbg, write_audit

MAX_SYNTHETIC_FINDINGS = 8  # keep output readable

def _has_finding(analysis: dict, pred) -> bool:
    for f in (analysis.get("findings") or []):
        try:
            if pred(f):
                return True
        except Exception:
            continue
    return False

def _dedup_findings(findings: list[dict]) -> list[dict]:
    """
    Deduplicate by (signal, detail) while preserving order.
    """
    seen = set()
    out = []
    for f in findings or []:
        sig = str(f.get("signal", "")).strip().lower()
        det = str(f.get("detail", "")).strip().lower()
        key = (sig, det)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out

def _promote_status(cur: str, injected_severity: str) -> str:
    """
    Conservative promotion: if we add an error/warn, ensure at least 'degraded'.
    """
    cur = (cur or "unknown").lower()
    sev = (injected_severity or "").lower()
    if cur in ("error", "degraded"):
        return cur
    if sev in ("error", "warn"):
        return "degraded"
    return cur or "unknown"

def critic_patch(analysis: dict, facts: dict, audit_dir: str) -> dict:
    """
    Inject synthetic findings if raw facts contradict a 'too-healthy' summary.
    Safe for Phase-1:
      - If facts['facts'] is missing, no synthetic checks run (graceful noop).
      - If present, we add a few high-signal booleans (bgp neighbor down, ping 0%, evpn xc down).
    """
    patched = copy.deepcopy(analysis)
    hostname = patched.get("hostname", "unknown")
    changed = False

    findings = patched.setdefault("findings", [])
    # Handle absent facts['facts'] (Phase-1 may not have LLM-parsed evidence yet)
    raw = (facts or {}).get("facts") or {}

    # --- Synthetic checks (only if we have evidence objects) ---
    # 1) BGP neighbor not Established
    for nei in (raw.get("bgp_neighbors") or []):
        state = str(nei.get("state", "")).lower()
        peer  = str(nei.get("peer", "")).strip()
        if state and state != "established":
            if not _has_finding(patched, lambda f: f.get("signal") == "bgp" and peer in (f.get("detail",""))):
                findings.append({
                    "signal": "bgp",
                    "severity": "error",
                    "detail": f"BGP neighbor {peer} not Established ({nei.get('state')}) [synthetic-check]",
                    "evidence": nei.get("evidence", "")
                })
                patched["status"] = _promote_status(patched.get("status"), "error")
                changed = True

    # 2) Ping 0% success
    for pr in (raw.get("reachability") or []):
        if pr.get("probe") == "ping" and pr.get("success_rate", 100) == 0:
            if not _has_finding(patched, lambda f: f.get("signal") in ("ip", "reachability")):
                findings.append({
                    "signal": "ip",
                    "severity": "warn",
                    "detail": "Ping success rate is 0% in captured logs [synthetic-check]",
                    "evidence": pr.get("evidence", "")
                })
                patched["status"] = _promote_status(patched.get("status"), "warn")
                changed = True

    # 3) EVPN XC down
    for xc in (raw.get("evpn_xconnects") or []):
        state = str(xc.get("state", "")).lower()
        if state == "down":
            if not _has_finding(patched, lambda f: f.get("signal") in ("l2vpn", "evpn")):
                findings.append({
                    "signal": "l2vpn",
                    "severity": "error",
                    "detail": "EVPN xconnect is down in logs [synthetic-check]",
                    "evidence": xc.get("evidence", "")
                })
                patched["status"] = _promote_status(patched.get("status"), "error")
                changed = True

    # --- Hygiene: dedupe & cap ---
    if findings:
        findings = _dedup_findings(findings)
        if len(findings) > MAX_SYNTHETIC_FINDINGS:
            findings = findings[:MAX_SYNTHETIC_FINDINGS]
        patched["findings"] = findings

    if changed and audit_dir:
        try:
            write_audit(os.path.join(audit_dir, f"{hostname}__critic_note.txt"),
                        "patched by critic: injected synthetic findings based on evidence\n")
        except Exception as e:
            dbg(f"[critic] failed to write audit note for {hostname}: {e}")
            
    return patched