# agents/agent-8/http_api.py
from __future__ import annotations
import os, time, json, uuid
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import triage_llm, commands_trusted, command_history

app = FastAPI(title="Agent-8 Triage API", version="0.1.0")

# ---- Environment ----
REPO_ROOT   = os.getenv("REPO_ROOT", "/app/doo")
AGENT_4_URL = os.getenv("AGENT_4_URL")   # e.g. http://agent-4:8004
AGENT_7_URL = os.getenv("AGENT_7_URL")   # e.g. http://agent-7:8007
SESSION_TTL_MIN = int(os.getenv("A8_SESSION_TTL_MIN", "240"))  # default 4h

# ---- Minimal in-memory session store (TTL) ----
_SESS: Dict[str, Dict[str, Any]] = {}

def _now() -> float:
    return time.time()

def _cleanup_sessions() -> None:
    if not _SESS:
        return
    now = _now()
    dead = [sid for sid, s in _SESS.items() if s.get("expires_at", 0) <= now]
    for sid in dead:
        _SESS.pop(sid, None)

def _new_session_id() -> str:
    return uuid.uuid4().hex

def _require_session(session_id: str) -> Dict[str, Any]:
    _cleanup_sessions()
    s = _SESS.get(session_id)
    if not s:
        raise HTTPException(status_code=404, detail="session not found/expired")
    # refresh TTL on use
    s["expires_at"] = _now() + SESSION_TTL_MIN * 60
    return s

# ---- Models ----
class StartReq(BaseModel):
    config_dir: str
    task_dir: str
    host: Optional[str] = None            # accept either 'host' or 'hosts[0]'
    hosts: Optional[List[str]] = None
    channel: Optional[str] = None
    thread_ts: Optional[str] = None
    user_id: Optional[str] = None

class StartResp(BaseModel):
    session_id: str
    ttl_min: int
    host: str
    config_dir: str
    task_dir: str

class IngestReq(BaseModel):
    session_id: str
    user_text: str = Field(min_length=1)

class ProposedCmd(BaseModel):
    command: str
    source: str = Field(description="kb|docs|llm", default="llm")
    trust_hint: str = Field(description="high|medium|low", default="low")

class IngestResp(BaseModel):
    guidance_text: str
    proposed_commands: List[ProposedCmd]
    needs_confirmation: bool = True

class RunShowsReq(BaseModel):
    session_id: str
    host: str
    commands: List[str]

class RunShowsResp(BaseModel):
    plan_ini_path: str
    dispatched: bool
    agent4_response: Optional[Dict[str, Any]] = None

class ReAnalyzeReq(BaseModel):
    session_id: str
    host: str

class ReAnalyzeResp(BaseModel):
    accepted: bool
    agent7_response: Optional[Dict[str, Any]] = None

# --- New models for agent-8 triage --#
class AnalyzeCommandReq(BaseModel):
    session_id: str
    host: str
    command: str

class AnalyzeCommandResp(BaseModel):
    analysis_text: str
    direction: str
    trusted_commands: List[str]
    unvalidated_commands: List[str]
    promoted: List[str]

# ---- Agent-knowledge loaders & trial history (compatible) ----
from pathlib import Path
import yaml

AK_DIR = Path("/app/shared/_agent_knowledge")  # repo-level shared
TRIAL_DIR_NAME = "agent8"  # under /doo/<config>/<task>/

def _norm_vendor(v: Optional[str]) -> Optional[str]:
    if not v: return None
    v = v.strip().lower()
    if v in ("cisco", "cisco-systems"):
        return "cisco"
    return v

def _norm_platform(p: Optional[str]) -> Optional[str]:
    if not p: return None
    p = p.strip().lower().replace("_", "").replace("-", "")
    # accept common aliases
    if p in ("iosxe", "ios", "iosxenative"):
        return "iosxe"
    if p in ("iosxr", "iosxrv"):
        return "iosxr"
    if p in ("nxos",):
        return "nxos"
    return p

def _iter_from_tree(tree: dict) -> List[Dict[str, Any]]:
    """
    Convert hierarchical YAML shape:
      vendor -> platform -> tech -> [commands]
    into a flat list of dicts.
    """
    out: List[Dict[str, Any]] = []
    for vendor, v_body in (tree or {}).items():
        if not isinstance(v_body, dict):
            continue
        for platform, p_body in v_body.items():
            if not isinstance(p_body, dict):
                continue
            for tech, cmds in p_body.items():
                if not isinstance(cmds, list):
                    continue
                for cmd in cmds:
                    if not isinstance(cmd, str) or not cmd.strip():
                        continue
                    out.append({
                        "vendor": _norm_vendor(vendor),
                        "platform": _norm_platform(platform),
                        "tech": [str(tech).strip().lower()],
                        "command": cmd.strip(),
                        "parser": None,
                        "parser_support": None,
                        "trust": "trusted",
                        "aliases": [],
                    })
    return out

def _ak_trusted() -> List[Dict[str, Any]]:
    """
    Load commands_trusted from YAML in either:
     - hierarchical mapping (vendor->platform->tech->list[str]), or
     - list[dict] with fields (vendor, platform, tech[], command, aliases[], parser_support, trust).
    Always return a flat list of normalized dicts.
    """
    path = AK_DIR / "commands_trusted.yaml"
    try:
        if not path.exists():
            return []
        data = yaml.safe_load(path.read_text()) or {}
        if isinstance(data, list):
            out: List[Dict[str, Any]] = []
            for row in data:
                if not isinstance(row, dict):
                    continue
                cmd = str(row.get("command", "")).strip()
                if not cmd:
                    continue
                out.append({
                    "vendor": _norm_vendor(row.get("vendor")),
                    "platform": _norm_platform(row.get("platform")),
                    "tech": [t.strip().lower() for t in (row.get("tech") or []) if isinstance(t, str)],
                    "command": cmd,
                    "parser": row.get("parser"),
                    "parser_support": bool(row.get("parser_support")) if row.get("parser_support") is not None else None,
                    "trust": row.get("trust", "trusted"),
                    "aliases": [a for a in (row.get("aliases") or []) if isinstance(a, str)],
                })
            return out
        elif isinstance(data, dict):
            return _iter_from_tree(data)
        else:
            return []
    except Exception:
        return []

def _trial_path(config_dir: str, task_dir: str) -> str:
    base = Path(REPO_ROOT) / config_dir / task_dir / TRIAL_DIR_NAME
    base.mkdir(parents=True, exist_ok=True)
    return str(base / "trial_history.jsonl")

def _append_trial_event(config_dir: str, task_dir: str, event: Dict[str, Any]) -> None:
    try:
        path = _trial_path(config_dir, task_dir)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(event) + "\n")
    except Exception:
        pass

def _select_trusted_by_text(user_text: str,
                            vendor_hint: Optional[str] = None,
                            platform_hint: Optional[str] = None,
                            limit: int = 4) -> List[Dict[str, Any]]:
    """
    Simple scoring against the normalized list:
      +2 if alias token in text (when available)
      +1 if tech token in text
      +1 if parser_support is True
    Then filter by vendor/platform hints (if provided).
    """
    text = (user_text or "").lower()
    v_hint = _norm_vendor(vendor_hint)
    p_hint = _norm_platform(platform_hint)

    items: List[tuple[int, Dict[str, Any]]] = []
    rows = _ak_trusted()

    for row in rows:
        if v_hint and row.get("vendor") and row["vendor"] != v_hint:
            continue
        if p_hint and row.get("platform") and row["platform"] != p_hint:
            continue

        score = 0
        for a in (row.get("aliases") or []):
            if isinstance(a, str) and a.lower() in text:
                score += 2
        for t in (row.get("tech") or []):
            if isinstance(t, str) and t in text:
                score += 1
        if row.get("parser_support") is True:
            score += 1

        if score > 0:
            items.append((score, row))

    # fallback: if nothing matched, suggest 1–2 broadly safe starters
    if not items:
        for row in rows:
            if row.get("tech") and "interfaces" in row["tech"]:
                items.append((1, row))
                break
        for row in rows:
            if row.get("tech") and "bgp" in row["tech"]:
                items.append((1, row))
                break

    items.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in items[:limit]]


# ---- Helpers ----
def _agent7_plan_dir(config_dir: str, task_dir: str) -> str:
    # Reuse Agent-7 canonical layout so artifacts land in one place
    base = os.path.join(REPO_ROOT, config_dir, task_dir, "agent7")
    plan = os.path.join(base, "1-plan")
    os.makedirs(plan, exist_ok=True)
    return plan

def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

def _mk_host_ini(host: str, commands: List[str]) -> str:
    # Very small per-host INI that Agent-4 can consume (host section with commands)
    lines = [f"[{host}]"]
    for c in commands:
        c = (c or "").strip()
        if not c:
            continue
        # lines.append(f"show = {c}")
        lines.append(f"{c}")
    return "\n".join(lines) + "\n"

# ---- Endpoints ----
@app.get("/health")
def health():
    _cleanup_sessions()
    return {"ok": True, "sessions": len(_SESS)}

@app.post("/triage/start", response_model=StartResp)
def triage_start(req: StartReq):
    """
    Create a short-lived triage session bound to a host.
    """
    host = (req.host or (req.hosts[0] if req.hosts else "")).strip()
    if not host:
        raise HTTPException(status_code=400, detail="host required")

    sid = _new_session_id()
    _SESS[sid] = {
        "config_dir": req.config_dir,
        "task_dir": req.task_dir,
        "host": host,
        "channel": req.channel,
        "thread_ts": req.thread_ts,
        "user_id": req.user_id,
        "created_at": _now(),
        "expires_at": _now() + SESSION_TTL_MIN * 60,
        # place-holders for future context:
        "history": [],          # [{role, text, ts}]
        "last_proposals": [],   # [command strings]
    }
    return StartResp(
        session_id=sid,
        ttl_min=SESSION_TTL_MIN,
        host=host,
        config_dir=req.config_dir,
        task_dir=req.task_dir,
    )

@app.post("/triage/ingest", response_model=IngestResp)
def triage_ingest(req: IngestReq):
    """
    Accept free-text, return structured suggestions from trusted AK.
    """
    s = _require_session(req.session_id)
    s["history"].append({"role": "user", "text": req.user_text, "ts": _now()})

    # (Optional) you could attach vendor/platform hints later from facts
    vendor_hint = None
    platform_hint = None

    picks = _select_trusted_by_text(req.user_text, vendor_hint, platform_hint, limit=4)
    proposed: List[ProposedCmd] = [
        ProposedCmd(command=p["command"], source="kb", trust_hint="high") for p in picks
    ]

    guidance = "Here are safe commands based on what you described. You can run them or type a custom command."

    # Log proposal into trial history (no success/parse yet)
    _append_trial_event(
        s["config_dir"], s["task_dir"],
        {
            "ts": _now(),
            "session_id": req.session_id,
            "host": s["host"],
            "vendor": vendor_hint,
            "platform": platform_hint,
            "user_text": req.user_text,
            "proposed": [pc.command for pc in proposed],
            "source": "kb",
            "type": "proposal"
        }
    )
    s["last_proposals"] = [pc.command for pc in proposed]

    return IngestResp(
        guidance_text=guidance,
        proposed_commands=proposed,
        needs_confirmation=True
    )

@app.post("/triage/run_shows", response_model=RunShowsResp)
def triage_run_shows(req: RunShowsReq):
    """
    Persist a tiny per-host plan INI and dispatch to Agent-4 /capture-only for this host.
    Soft-correct the host to the session's host to avoid 400s when the UI omits or mismatches it.
    """
    s = _require_session(req.session_id)

    # ---- Minimal, safe normalization/fallback for host ----
    host_req = (req.host or "").strip()
    host_sess = (s.get("host") or "").strip()
    if not host_sess:
        raise HTTPException(status_code=400, detail="session host missing")

    # If caller didn't send a host, or it doesn't match, use the session host
    host_use = host_sess if (not host_req or host_req != host_sess) else host_req

    # Guard: avoid empty plan
    if not req.commands or not any((c or "").strip() for c in req.commands):
        raise HTTPException(status_code=400, detail="no commands provided")

    # 1) Write per-host INI under Agent-7 plan dir (shared tree)
    plan_dir = _agent7_plan_dir(s["config_dir"], s["task_dir"])
    ini_name = f"triage_{host_use}__{req.session_id[:8]}.ini"
    ini_path = os.path.join(plan_dir, ini_name)
    _write_text(ini_path, _mk_host_ini(host_use, req.commands or []))

    # 2) Dispatch to Agent-4 /capture-only (NOT /operational-check)
    dispatched = False
    a4_resp: Optional[Dict[str, Any]] = None
    if AGENT_4_URL:
        try:
            # overlay must be *relative to the task folder*
            task_root = os.path.join(REPO_ROOT, s["config_dir"], s["task_dir"])
            overlay_rel = os.path.relpath(ini_path, start=task_root)

            payload = {
                "config_dir": s["config_dir"],
                "task_id": s["task_dir"],
                "overlay_ini_relpath": overlay_rel,
                "out_subdir": "agent7/2-capture",
                "devices": [host_use],
                "no_grading_logs": True,
            }
            with httpx.Client(timeout=180.0) as cli:
                r = cli.post(f"{AGENT_4_URL}/capture-only", json=payload)
            r.raise_for_status()
            a4_resp = r.json() if r.content else {"ok": True}
            dispatched = True
        except Exception as e:
            a4_resp = {"error": f"agent-4 dispatch failed: {e}"}

    # 3) Log outcome stub (we only know dispatch result here)
    _append_trial_event(
        s["config_dir"], s["task_dir"],
        {
            "ts": _now(),
            "session_id": req.session_id,
            "host": host_use,
            "commands": req.commands,
            "source": "user",          # user confirmed via UI
            "dispatched": dispatched,
            "agent4_response": a4_resp,
            "type": "dispatch"
        }
    )

    return RunShowsResp(plan_ini_path=ini_path, dispatched=dispatched, agent4_response=a4_resp)

# ----- 
@app.post("/triage/reanalyze", response_model=ReAnalyzeResp)
def triage_reanalyze(req: ReAnalyzeReq):
    """
    Call Agent-7 analyze (host-scoped acceptable; will operate on available facts).
    """
    s = _require_session(req.session_id)
    accepted = False
    a7_resp: Optional[Dict[str, Any]] = None

    if not AGENT_7_URL:
        # Accept but no downstream call in this prototype
        return ReAnalyzeResp(accepted=False, agent7_response={"error": "AGENT_7_URL not set"})

    try:
        payload = {"config_dir": s["config_dir"], "task_dir": s["task_dir"]}
        with httpx.Client(timeout=120.0) as cli:
            r = cli.post(f"{AGENT_7_URL}/analyze", json=payload)
        r.raise_for_status()
        a7_resp = r.json() if r.content else {"ok": True}
        accepted = True
    except Exception as e:
        a7_resp = {"error": f"agent-7 analyze failed: {e}"}

    return ReAnalyzeResp(accepted=accepted, agent7_response=a7_resp)

# --- --- #
# --- --- #
# --- agent-8 triage functions --- #

@app.post("/triage/analyze_command", response_model=AnalyzeCommandResp)
def triage_analyze_command(req: AnalyzeCommandReq):
    """
    Read the captured show_log for a single command, run LLM analysis,
    decide trusted vs unvalidated follow-ups, and update history.
    """
    s = _require_session(req.session_id)

    # 1. Locate the show_log file
    md_path = os.path.join(
        REPO_ROOT, s["config_dir"], s["task_dir"],
        "agent7", "2-capture", "show_logs", f"{req.host}.md"
    )
    if not os.path.isfile(md_path):
        raise HTTPException(status_code=404, detail=f"show_log not found for {req.host}")

    body = Path(md_path).read_text(encoding="utf-8")

    # Extract section for this command
    import re
    pat = rf"(?mis)^##\s*{re.escape(req.command)}\s*\n+```(.*?)```"
    m = re.search(pat, body)
    if not m:
        raise HTTPException(status_code=400, detail=f"no output found for command {req.command}")
    cmd_output = m.group(1).strip()

    # 2. Call LLM for analysis
    history = command_history.load_steps(s["config_dir"], s["task_dir"], req.session_id)
    llm_result = triage_llm.triage_llm_analyze(
        host=req.host,
        commands=[req.command],
        outputs=[cmd_output],
        history=history
    )

    analysis_text = llm_result.get("analysis_text", "")
    direction = llm_result.get("direction", "")
    recommended = llm_result.get("recommended", [])
    execution_judgment = llm_result.get("execution_judgment", {})

    trusted_cmds, unvalidated_cmds, promoted = [], [], []

    # 3. Bucket recommended commands
    for rec in recommended:
        cmd = rec.get("command", "").strip()
        if not cmd:
            continue
        vendor = _norm_vendor("cisco")   # placeholder; later from facts
        platform = _norm_platform("iosxr")  # placeholder; later from facts
        tech = rec.get("tech", ["misc"])

        if commands_trusted.is_trusted(cmd, vendor, platform):
            trusted_cmds.append(cmd)
        else:
            unvalidated_cmds.append(cmd)

        # Promotion: if LLM judged the executed command as OK
        if execution_judgment.get(req.command) == "ok" and cmd.startswith("show "):
            commands_trusted.promote(cmd, vendor, platform, tech)
            promoted.append(cmd)

    # 4. Save in history
    command_history.append_step(
        config_dir=s["config_dir"],
        task_dir=s["task_dir"],
        session_id=req.session_id,
        host=req.host,
        commands=[req.command],
        analysis=analysis_text,
        direction=direction,
        trusted=trusted_cmds,
        unvalidated=unvalidated_cmds
    )

    return AnalyzeCommandResp(
        analysis_text=analysis_text,
        direction=direction,
        trusted_commands=trusted_cmds,
        unvalidated_commands=unvalidated_cmds,
        promoted=promoted
    )

# ---- Local dev ----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("http_api:app", host="0.0.0.0", port=int(os.getenv("PORT", "8008")), reload=False)