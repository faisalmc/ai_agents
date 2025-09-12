# agent5_critic.py
import os, copy
from agent5_shared import dbg, write_audit

def _has_finding(analysis: dict, pred) -> bool:
    for f in (analysis.get("findings") or []):
        try:
            if pred(f):
                return True
        except Exception:
            continue
    return False

def critic_patch(analysis: dict, facts: dict, audit_dir: str) -> dict:
    """Inject synthetic findings if raw facts contradict a 'too-healthy' summary."""
    patched = copy.deepcopy(analysis)
    hostname = patched.get("hostname","unknown")
    changed = False
    findings = patched.setdefault("findings", [])

    # BGP neighbor not Established
    for nei in (facts.get("facts",{}).get("bgp_neighbors") or []):
        state = str(nei.get("state","")).lower()
        if state and state != "established":
            if not _has_finding(patched, lambda f: f.get("signal")=="bgp" and "neighbor" in f.get("detail","").lower()):
                findings.append({
                    "signal":"bgp",
                    "severity":"error",
                    "detail":f"BGP neighbor {nei.get('peer')} not Established ({nei.get('state')}) [synthetic-check]",
                    "evidence": nei.get("evidence","")
                })
                patched["status"] = "degraded" if patched.get("status")=="healthy" else patched.get("status","degraded")
                changed = True

    # Ping 0% success
    for pr in (facts.get("facts",{}).get("reachability") or []):
        if pr.get("probe")=="ping" and pr.get("success_rate",100)==0:
            if not _has_finding(patched, lambda f: f.get("signal") in ("ip","reachability")):
                findings.append({
                    "signal":"ip",
                    "severity":"warn",
                    "detail":"Ping success rate is 0% in captured logs [synthetic-check]",
                    "evidence": pr.get("evidence","")
                })
                if patched.get("status")=="healthy":
                    patched["status"]="degraded"
                changed = True

    # EVPN XC down
    for xc in (facts.get("facts",{}).get("evpn_xconnects") or []):
        if str(xc.get("state","")).lower()=="down":
            if not _has_finding(patched, lambda f: f.get("signal") in ("l2vpn","evpn")):
                findings.append({
                    "signal":"l2vpn",
                    "severity":"error",
                    "detail":"EVPN xconnect is down in logs [synthetic-check]",
                    "evidence": xc.get("evidence","")
                })
                if patched.get("status")=="healthy":
                    patched["status"]="degraded"
                changed = True

    if changed:
        write_audit(os.path.join(audit_dir, f"{hostname}__critic_note.txt"), "patched by critic\n")
    return patched
