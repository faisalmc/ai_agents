# agents/agent-7/http_api.py
from __future__ import annotations
import os
import time
import json
import glob
from typing import Any, Dict, List, Optional, Set

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Agent-7 HTTP API", version="1.1.0")

REPO_ROOT = os.getenv("REPO_ROOT", "/app/doo")

# -------- helpers --------
def _agent7_root(config_dir: str, task_dir: str) -> str:
    return os.path.join(REPO_ROOT, config_dir, task_dir, "agent7")

def _ensure_dirs(root: str) -> Dict[str, str]:
    """
    Create the agreed Plan → Capture → Analyze structure and return useful paths.
    """
    plan_dir = os.path.join(root, "1-plan")
    capture_dir = os.path.join(root, "2-capture")
    show_logs_dir = os.path.join(capture_dir, "show_logs")

    analyze_dir = os.path.join(root, "3-analyze")
    md_index_dir = os.path.join(analyze_dir, "0-md-index")
    parsed_dir = os.path.join(analyze_dir, "1-parsed")
    facts_dir = os.path.join(analyze_dir, "2-facts")

    audit_dir = os.path.join(root, "audit")
    meta_dir = os.path.join(root, "meta")

    for p in (
        root,
        plan_dir,
        capture_dir,
        show_logs_dir,
        analyze_dir,
        md_index_dir,
        parsed_dir,
        facts_dir,
        audit_dir,
        meta_dir,
    ):
        os.makedirs(p, exist_ok=True)

    return {
        "plan_dir": plan_dir,
        "capture_dir": capture_dir,
        "show_logs_dir": show_logs_dir,
        "analyze_dir": analyze_dir,
        "md_index_dir": md_index_dir,
        "parsed_dir": parsed_dir,
        "facts_dir": facts_dir,
        "audit_dir": audit_dir,
        "meta_dir": meta_dir,
    }

def _discover_hosts(show_logs_dir: str) -> List[str]:
    hosts: List[str] = []
    for p in sorted(glob.glob(os.path.join(show_logs_dir, "*.md"))):
        hosts.append(os.path.splitext(os.path.basename(p))[0])
    return hosts

def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)

def _read_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def _host_from_blocks_path(blocks_json_path: str) -> Optional[str]:
    """
    md_splitter writes 0-md-index/<HOST>__blocks.json
    """
    base = os.path.basename(blocks_json_path)
    if "__blocks.json" in base:
        return base.split("__blocks.json")[0]
    return None

def _prune_md_index_for_hosts(md_index_dir: str, allowed_hosts: Set[str]) -> None:
    """
    SAFE, non-destructive pruning of the generated md-index ONLY (never touch capture logs).
    Keeps only md-index artifacts for allowed hosts so downstream parsers process a subset.
    Non-allowed artifacts are *moved* under 0-md-index/_prev/<timestamp>/ for easy rollback.

    Structure we may see:
      • Current (v2):
          0-md-index/<HOST>/...            (raw block .txt files)
          0-md-index/<HOST>__blocks.json   (per-host block index at root)
      • Legacy (flat):
          0-md-index/00x__<HOST>__<cmd>.txt
    """
    if not allowed_hosts:
        return

    import time, shutil

    # Where we rotate non-allowed hosts
    ts = time.strftime("%Y%m%d-%H%M%S")
    prev_root = os.path.join(md_index_dir, "_prev", ts)
    try:
        os.makedirs(prev_root, exist_ok=True)
    except Exception:
        pass

    # --- 1) Move per-host DIRECTORIES (current layout) ---
    try:
        for name in os.listdir(md_index_dir):
            src = os.path.join(md_index_dir, name)
            if not os.path.isdir(src):
                continue
            # ignore our own _prev rotations
            if name.startswith("_"):
                continue
            if name not in allowed_hosts:
                dst = os.path.join(prev_root, name)
                try:
                    shutil.move(src, dst)
                except Exception:
                    # don't fail pruning on move errors
                    pass
    except Exception:
        pass

    # --- 2) Move per-host __blocks.json at root (current layout) ---
    try:
        for p in glob.glob(os.path.join(md_index_dir, "*__blocks.json")):
            h = _host_from_blocks_path(p)
            if h and h not in allowed_hosts:
                dst = os.path.join(prev_root, os.path.basename(p))
                try:
                    shutil.move(p, dst)
                except Exception:
                    # fallback to remove if move fails (file is regenerated anyway)
                    try:
                        os.remove(p)
                    except Exception:
                        pass
    except Exception:
        pass

    # --- 3) Move legacy flat block files at root (00x__<HOST>__*.txt) ---
    try:
        legacy_dst = os.path.join(prev_root, "legacy")
        os.makedirs(legacy_dst, exist_ok=True)
    except Exception:
        pass
    try:
        for p in glob.glob(os.path.join(md_index_dir, "*.txt")):
            base = os.path.basename(p)
            parts = base.split("__", 2)  # ["00x", "<HOST>", "<rest>.txt"]
            if len(parts) >= 2:
                host = parts[1]
                if host not in allowed_hosts:
                    dst = os.path.join(legacy_dst, base)
                    try:
                        shutil.move(p, dst)
                    except Exception:
                        # fallback to remove if move fails (legacy file is regenerated anyway)
                        try:
                            os.remove(p)
                        except Exception:
                            pass
    except Exception:
        pass
# -------- models --------
class PlanRequest(BaseModel):
    config_dir: str
    task_dir: str
    # optional explicit host list; planner can also infer from context
    hosts: Optional[List[str]] = None
    per_signal_limit: int = 3
    use_adk: bool = True
    include_lexicon: bool = True

class PlanResponse(BaseModel):
    # Field names kept for backward compatibility with callers.
    # We point them to the new canonical files under agent7/1-plan/.
    overlay_ini: str
    capture_plan: str
    hosts: List[str]
    signals_by_host: Dict[str, List[str]]

class CaptureRequest(BaseModel):
    config_dir: str
    task_dir: str
    plan_path: Optional[str] = None
    hosts_override: Optional[List[str]] = None

class CaptureResponse(BaseModel):
    summary_path: str

class AnalyzeRequest(BaseModel):
    config_dir: str
    task_dir: str
    # NEW: optional per-host filtering for a faster, scoped analyze
    hosts: Optional[List[str]] = None

class AnalyzeResponse(BaseModel):
    facts_summary_path: str
    hosts_processed: int
    per_device_json_path: str
    cross_device_json_path: str
    slack_overview_path: Optional[str] = None  # best-effort

# -------- endpoints --------
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest):
    """
    Planning stage (AI-driven).

    emits (canonical) →
      • agent7/1-plan/show_cmds.plan.ini
      • agent7/1-plan/capture_plan.json
    """
    # Try the new name first, fall back to legacy module name if needed.
    try:
        import command_plan_builder as _planner
        use_new_api = hasattr(_planner, "plan_commands")
    except ImportError:
        _planner = None
        use_new_api = False

    if not use_new_api:
        try:
            import overlay_planner as _planner  # legacy
        except ImportError as e:
            raise HTTPException(status_code=500, detail=f"No planner module available: {e}")

    root = _agent7_root(req.config_dir, req.task_dir)
    dirs = _ensure_dirs(root)
    plan_dir = dirs["plan_dir"]

    # Canonical targets
    plan_ini_path  = os.path.join(plan_dir, "show_cmds.plan.ini")
    plan_json_path = os.path.join(plan_dir, "capture_plan.json")

    # Call the planner (it may also write files itself)
    if use_new_api:
        plan_obj = _planner.plan_commands(
            config_dir=req.config_dir,
            task_dir=req.task_dir,
            hosts=req.hosts,
            per_signal_limit=req.per_signal_limit,
            use_adk=req.use_adk,
            include_lexicon=req.include_lexicon,
        )
    else:
        plan_obj = _planner.plan_overlay(
            req.config_dir,
            req.task_dir,
            per_signal_limit=req.per_signal_limit,
            use_adk=req.use_adk,
            include_lexicon=req.include_lexicon,
        )

        # Legacy outputs → normalize
        legacy_ini = os.path.join(root, "show_cmds.overlay.ini")
        legacy_json = os.path.join(root, "meta", "overlay_plan.json")
        try:
            if os.path.exists(legacy_ini):
                with open(legacy_ini, "r", encoding="utf-8") as fsrc, open(plan_ini_path, "w", encoding="utf-8") as fdst:
                    fdst.write(fsrc.read())
            if os.path.exists(legacy_json):
                data = _read_json(legacy_json) or {}
                _write_json(plan_json_path, data)
        except Exception:
            pass

    # Additional compat: if a prior version wrote into agent7/plan/*, copy into agent7/1-plan/*
    compat_old_plan_dir = os.path.join(root, "plan")
    compat_old_ini  = os.path.join(compat_old_plan_dir, "show_cmds.plan.ini")
    compat_old_json = os.path.join(compat_old_plan_dir, "capture_plan.json")
    try:
        if not os.path.exists(plan_ini_path) and os.path.exists(compat_old_ini):
            with open(compat_old_ini, "r", encoding="utf-8") as fsrc, open(plan_ini_path, "w", encoding="utf-8") as fdst:
                fdst.write(fsrc.read())
        if not os.path.exists(plan_json_path) and os.path.exists(compat_old_json):
            data = _read_json(compat_old_json) or {}
            _write_json(plan_json_path, data)
    except Exception:
        pass

    # Ensure capture_plan.json exists and contains the correct ini_path (canonical)
    plan_on_disk = _read_json(plan_json_path)
    if not isinstance(plan_on_disk, dict):
        plan_on_disk = plan_obj if isinstance(plan_obj, dict) else {}
    plan_on_disk["ini_path"] = plan_ini_path  # authoritative
    _write_json(plan_json_path, plan_on_disk)

    # Build response lists from the final plan JSON on disk
    hosts_map = plan_on_disk.get("hosts", {}) if isinstance(plan_on_disk, dict) else {}
    if isinstance(hosts_map, dict):
        hosts = sorted(list(hosts_map.keys()))
        signals_by_host = {
            h: list(hosts_map[h].get("signals", [])) if isinstance(hosts_map.get(h), dict) else []
            for h in hosts
        }
    else:
        hosts, signals_by_host = [], {}

    return PlanResponse(
        overlay_ini=plan_ini_path,
        capture_plan=plan_json_path,
        hosts=hosts,
        signals_by_host=signals_by_host,
    )

@app.post("/capture", response_model=CaptureResponse)
def capture(req: CaptureRequest):
    """
    Capture stage.

    emits →
      • agent7/2-capture/show_logs/<host>.md
      • agent7/meta/capture_summary.json (by wrapper)
      • agent7/meta/capture_http_summary.json (tiny roll-up from this API)
    """
    import capture_wrapper

    root = _agent7_root(req.config_dir, req.task_dir)
    dirs = _ensure_dirs(root)
    default_plan_path = os.path.join(dirs["plan_dir"], "capture_plan.json")

    summary = capture_wrapper.run_capture(
        req.config_dir,
        req.task_dir,
        plan_path=req.plan_path or default_plan_path,
        hosts_override=req.hosts_override,
    )

    out_path = os.path.join(dirs["meta_dir"], "capture_http_summary.json")
    _write_json(out_path, summary or {})
    return CaptureResponse(summary_path=out_path)

# @app.post("/analyze", response_model=AnalyzeResponse)
# def analyze(req: AnalyzeRequest):
#     """
#     Analysis stage.

#     executes →
#       1) md_splitter.split_task(config_dir, task_dir)  → agent7/3-analyze/0-md-index/...
#       2) (optional) prune md-index to selected hosts
#       3) genie_parser.run(config_dir, task_dir)        → agent7/3-analyze/1-parsed/...
#       4) facts_builder.build_all(config_dir, task_dir) → agent7/3-analyze/2-facts/*.json
#       5) per_device_llm.run(config_dir, task_dir)      → agent7/3-analyze/per_device.json
#       6) cross_device_llm.run(config_dir, task_dir)    → agent7/3-analyze/cross_device.json  (skipped if single host)
#       7) slack_summarizer.summarize(...)               → agent7/3-analyze/slack_overview.json  (best-effort)
#     emits →
#       • agent7/3-analyze/facts_summary.json
#     """
#     import md_splitter
#     import genie_parser
#     import facts_builder
#     import per_device_llm
#     import cross_device_llm

#     # DEBUG to check hosts
#     print(f"[agent7][analyze] req.hosts={req.hosts}", flush=True)

#     # Always split to regenerate md-index (safe)
#     md_splitter.split_task(req.config_dir, req.task_dir)

#     # If a host filter is provided, prune ONLY the generated md-index to those hosts.
#     # This avoids touching capture logs and speeds up downstream parsing.
#     if req.hosts:
#         root = _agent7_root(req.config_dir, req.task_dir)
#         dirs = _ensure_dirs(root)
#         allowed = {h.strip() for h in req.hosts if h and isinstance(h, str)}
#         _prune_md_index_for_hosts(dirs["md_index_dir"], allowed_hosts=allowed)

#     # DEBUG to check hosts #
#     root = _agent7_root(req.config_dir, req.task_dir); dirs = _ensure_dirs(root)
#     now_hosts = [n for n in os.listdir(dirs["md_index_dir"])
#                 if os.path.isfile(os.path.join(dirs["md_index_dir"], f"{n}__blocks.json"))]
#     print(f"[agent7][analyze] md_index hosts after prune={now_hosts}", flush=True)

#     # Parse facts from the (possibly pruned) md-index
#     genie_parser.run(req.config_dir, req.task_dir)
#     facts_summary = facts_builder.build_all(req.config_dir, req.task_dir)

#     # # Run LLM analyses (per-device, then cross-device if applicable)
#     # per_dev = per_device_llm.run(req.config_dir, req.task_dir) or {}

#     # run_cross = True
#     # if req.hosts and len(req.hosts) == 1:
#     #     # Fast path for triage: skip cross-device when only one host is requested
#     #     run_cross = False

#     # Run LLM analyses (per-device) — scoped if hosts provided
#     if req.hosts:
#         per_dev = per_device_llm.run_hosts(req.config_dir, req.task_dir, req.hosts) or {}
#     else:
#         per_dev = per_device_llm.run(req.config_dir, req.task_dir) or {}

#     run_cross = True
#     if req.hosts and len(req.hosts) == 1:
#         # Fast path for triage: skip cross-device when only one host is requested
#         run_cross = False


#     cross = {}
#     if run_cross:
#         cross = cross_device_llm.run(req.config_dir, req.task_dir) or {}

#     root = _agent7_root(req.config_dir, req.task_dir)
#     dirs = _ensure_dirs(root)

#     facts_summary_path     = os.path.join(dirs["analyze_dir"], "facts_summary.json")
#     per_device_json_path   = per_dev.get("path")   or os.path.join(dirs["analyze_dir"], "per_device.json")
#     cross_device_json_path = cross.get("path")     or os.path.join(dirs["analyze_dir"], "cross_device.json")

#     # -------- OPTIONAL: LLM Slack overview (best-effort) --------
#     slack_overview_path: Optional[str] = None
#     try:
#         import slack_summarizer  # local module in agents/agent-7/
#         # Load inputs
#         per_rows = _read_json(per_device_json_path) or []
#         cross_obj = _read_json(cross_device_json_path) or {}
#         # Load all facts for context (by host)
#         facts_by_host: Dict[str, Dict[str, Any]] = {}
#         for fp in glob.glob(os.path.join(dirs["facts_dir"], "*.json")):
#             fobj = _read_json(fp) or {}
#             h = fobj.get("hostname") or os.path.splitext(os.path.basename(fp))[0]
#             facts_by_host[h] = fobj
#         # Summarize to a file
#         slack_overview_path = os.path.join(dirs["analyze_dir"], "slack_overview.json")
#         slack_summarizer.summarize(
#             per_device_rows=per_rows,
#             cross_device=cross_obj,
#             facts_by_host=facts_by_host,
#             out_path=slack_overview_path
#         )
#     except Exception:
#         # Soft-fail: keep API stable even if summarizer is missing
#         slack_overview_path = None

#     hosts_processed = int(facts_summary.get("hosts", 0)) if isinstance(facts_summary, dict) else 0
#     return AnalyzeResponse(
#         facts_summary_path=facts_summary_path,
#         hosts_processed=hosts_processed,
#         per_device_json_path=per_device_json_path,
#         cross_device_json_path=cross_device_json_path,
#         slack_overview_path=slack_overview_path,
#     )

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    """
    Analysis stage.

    executes →
      1) md_splitter.split_task(config_dir, task_dir, allow_backfill=..., hosts_filter=...) → agent7/3-analyze/0-md-index/...
      2) (optional) prune md-index to selected hosts
      3) genie_parser.run(config_dir, task_dir)        → agent7/3-analyze/1-parsed/...
      4) facts_builder.build_all(config_dir, task_dir) → agent7/3-analyze/2-facts/*.json
      5) per_device_llm.run*(...)                      → agent7/3-analyze/per_device*.json
      6) cross_device_llm.run(config_dir, task_dir)    → agent7/3-analyze/cross_device.json  (skipped if single host)
      7) slack_summarizer.summarize(...)               → agent7/3-analyze/slack_overview.json  (best-effort)
    emits →
      • agent7/3-analyze/facts_summary.json
    """
    import md_splitter
    import genie_parser
    import facts_builder
    import per_device_llm
    import cross_device_llm

    # DEBUG: show incoming scope
    print(f"[agent7][analyze] req.hosts={req.hosts}", flush=True)
    print(f"[agent7]------------------------------", flush=True)
    print(f"[agent7] /analyze called with hosts: {req.hosts}")
    print(f"[agent7]------------------------------", flush=True)
    # Add this guard near the top
    

    # --- 1) Build md-index with correct semantics for triage vs full run ---
    # Full run (no host filter): allow grading backfill; index all hosts
    # Triage (hosts provided):   DO NOT backfill from grading; index only those hosts
    allow_backfill = not bool(req.hosts)
    hosts_filter   = list({h.strip() for h in (req.hosts or []) if h and isinstance(h, str)}) or None

    md_splitter.split_task(
        req.config_dir,
        req.task_dir,
        allow_backfill=allow_backfill,   # <-- corrected kwarg
        hosts_filter=hosts_filter        # <-- pass scope (or None)
    )

    # --- 2) Safe prune of md-index to selected hosts (defensive, non-destructive) ---
    if hosts_filter:
        root = _agent7_root(req.config_dir, req.task_dir)
        dirs = _ensure_dirs(root)
        _prune_md_index_for_hosts(dirs["md_index_dir"], allowed_hosts=set(hosts_filter))

        # DEBUG: list hosts present in md-index after prune
    root = _agent7_root(req.config_dir, req.task_dir)
    dirs = _ensure_dirs(root)
    now_hosts = [
        n for n in os.listdir(dirs["md_index_dir"])
        if os.path.isfile(os.path.join(dirs["md_index_dir"], f"{n}__blocks.json"))
    ]
    print(f"[agent7][analyze] md_index hosts after prune={now_hosts}", flush=True)

    # --- 3) Parser (Genie) over current md-index ---
    genie_parser.run(req.config_dir, req.task_dir)

    # --- 4) Facts builder (Option A semantics inside facts_builder) ---
    facts_summary = facts_builder.build_all(req.config_dir, req.task_dir)

    # --- 5) Per-device LLM: scoped vs full ---
    if hosts_filter:
        per_dev = per_device_llm.run_hosts(req.config_dir, req.task_dir, hosts_filter) or {}
    else:
        per_dev = per_device_llm.run(req.config_dir, req.task_dir) or {}

    # --- 6) Cross-device: skip if single-host triage ---
    run_cross = True
    if hosts_filter and len(hosts_filter) == 1:
        run_cross = False
    print(f"[DEBUG] run_cross={run_cross}")
    cross = {}
    if run_cross:
        cross = cross_device_llm.run(req.config_dir, req.task_dir) or {}
    else:
        print("[DEBUG] Skipping stale cross_device.json loading (triage mode)")
        cross_obj = {}

    # --- 7) Slack overview (best effort) ---
    facts_summary_path     = os.path.join(dirs["analyze_dir"], "facts_summary.json")
    per_device_json_path   = per_dev.get("path")   or os.path.join(dirs["analyze_dir"], "per_device.json")
    cross_device_json_path = cross.get("path")     or os.path.join(dirs["analyze_dir"], "cross_device.json")

    # Debug instrumentation (AFTER paths are known; no inner imports)
    def _dbg_file(p):
        try:
            st = os.stat(p)
            return {"exists": True, "size": st.st_size, "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime))}
        except Exception:
            return {"exists": False}
    print(f"[agent7][analyze][dbg] run_cross={run_cross}", flush=True)
    print(f"[agent7][analyze][dbg] per_device_json_path={per_device_json_path} meta={_dbg_file(per_device_json_path)}", flush=True)
    print(f"[agent7][analyze][dbg] cross_device_json_path={cross_device_json_path} meta={_dbg_file(cross_device_json_path)}", flush=True)

    slack_overview_path: Optional[str] = None
    try:
        import slack_summarizer  # local module in agents/agent-7/
        per_rows = _read_json(per_device_json_path) or []
        cross_obj = _read_json(cross_device_json_path) or {}
        # Load all facts for context (by host)
        facts_by_host: Dict[str, Dict[str, Any]] = {}
        for fp in glob.glob(os.path.join(dirs["facts_dir"], "*.json")):
            fobj = _read_json(fp) or {}
            h = fobj.get("hostname") or os.path.splitext(os.path.basename(fp))[0]
            facts_by_host[h] = fobj
        slack_overview_path = os.path.join(dirs["analyze_dir"], "slack_overview.json")
        # DEBUG for slack message loading
        print(f"[DEBUG] Calling build_overview_blocks with {len(per_rows)} per-device entries and cross keys: {list(cross_obj.keys())}")
        slack_summarizer.summarize(
            per_device_rows=per_rows,
            cross_device=cross_obj,
            facts_by_host=facts_by_host,
            out_path=slack_overview_path
        )
    except Exception:
        slack_overview_path = None  # keep API stable

    hosts_processed = int(facts_summary.get("hosts", 0)) if isinstance(facts_summary, dict) else 0
    return AnalyzeResponse(
        facts_summary_path=facts_summary_path,
        hosts_processed=hosts_processed,
        per_device_json_path=per_device_json_path,
        cross_device_json_path=cross_device_json_path,
        slack_overview_path=slack_overview_path,
    )
    
    
# -------- local dev entrypoint --------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("http_api:app", host="0.0.0.0", port=int(os.getenv("PORT", "8087")), reload=False)