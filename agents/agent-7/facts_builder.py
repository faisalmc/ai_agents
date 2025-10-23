# agents/agent-7/facts_builder.py
from __future__ import annotations
import os, re, json, glob, time
from typing import Any, Dict, List, Optional, Tuple

# ------- simple logging -------
def _dbg(msg: str) -> None:
    print(f"[agent7][facts] {msg}", flush=True)

# ------- plain bootstrap imports (no dynamic loaders) -------
from bootstrap import (
    Agent7Paths,
    load_config,
    resolve_paths,
    ensure_dirs,
)

# ------- optional shared helpers (static import with safe fallback) -------
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

# ------- optional LLM wrapper (graceful fallback) -------
try:
    from shared.llm_api import call_llm  # type: ignore
except Exception:
    call_llm = None  # degrade gracefully

# --- feature flag: allow legacy audit backfill (default: OFF) ---
# Set A7_ALLOW_AUDIT_BACKFILL=1 to re-enable reading agent7/audit/<host>__blocks.json
ALLOW_AUDIT_BACKFILL = (os.getenv("A7_ALLOW_AUDIT_BACKFILL", "0").strip() == "1")

# ------- tiny io helpers -------
def _read_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""

def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)


# ------- light topic tag (for UX grouping only; not used for decisions) -------
def _topic_from_command(cmd: str) -> str:
    toks = re.split(r"\s+", (cmd or "").strip().lower())
    drop = {"show", "ip", "ipv4", "ipv6"}
    toks = [t for t in toks if t and t not in drop]
    return toks[0] if toks else ""

# ------- discover hosts by parsed outputs (new location) -------
def _hosts_from_parsed(paths: Agent7Paths) -> List[str]:
    """
    Hostnames are the subfolders under agent7/3-analyze/1-parsed/
    """
    pat = os.path.join(paths.parsed_dir, "*")
    out: List[str] = []
    for p in sorted(glob.glob(pat)):
        if os.path.isdir(p):
            out.append(os.path.basename(p))
    return out

# ------- helper to extract hosts list even if no genie parser -------

def _hosts_from_md_index(paths: Agent7Paths) -> List[str]:
    """
    Hostnames inferred from md-index files:
    agent7/3-analyze/0-md-index/<HOST>__blocks.json
    """
    pat = os.path.join(paths.md_index_dir, "*__blocks.json")
    out: List[str] = []
    for p in sorted(glob.glob(pat)):
        base = os.path.basename(p)
        if base.endswith("__blocks.json"):
            host = base[: -len("__blocks.json")]
            if host:
                out.append(host)
    return out

# ------- optional signal set per host (written during planning) -------
def _signal_set(paths: Agent7Paths, host: str) -> List[str]:
    # Preferred (new): agent7/1-plan/<host>__signals.json
    plan_sig = getattr(paths, "plan_dir", None)
    if plan_sig:
        p1 = os.path.join(paths.plan_dir, f"{host}__signals.json")
        obj = _read_json(p1)
        if isinstance(obj, dict) and isinstance(obj.get("signals"), list):
            return sorted({str(s).strip().lower() for s in obj["signals"] if str(s).strip()})
    # Legacy fallback: agent7/meta/<host>__signal_set.json
    p2 = os.path.join(paths.meta_dir, f"{host}__signal_set.json")
    obj2 = _read_json(p2) or {}
    sigs = obj2.get("signals") if isinstance(obj2, dict) else None
    if isinstance(sigs, list):
        return sorted({str(s).strip().lower() for s in sigs if str(s).strip()})
    return []

# ------- blocks index lookup (new path first, then legacy audit) -------
# def _load_blocks_index(paths: Agent7Paths, host: str) -> Dict[str, Dict[str, Any]]:
#     """
#     Returns cmd_key -> block dict (if any):
#       { "sanitized_command", "text_path", "platform_hint", "cmd_key" }
#     Tries:
#       1) agent7/3-analyze/0-md-index/<host>__blocks.json   (preferred)
#       2) agent7/audit/<host>__blocks.json                  (legacy mirror)
#     """
#     out: Dict[str, Dict[str, Any]] = {}

#     idx_new = os.path.join(paths.md_index_dir, f"{host}__blocks.json")
#     arr = _read_json(idx_new)
#     if isinstance(arr, list):
#         for b in arr:
#             if isinstance(b, dict) and b.get("cmd_key"):
#                 out[b["cmd_key"]] = b
#     if out:
#         return out

#     idx_legacy = os.path.join(paths.audit_dir, f"{host}__blocks.json")
#     arr2 = _read_json(idx_legacy)
#     if isinstance(arr2, list):
#         for b in arr2:
#             if isinstance(b, dict) and b.get("cmd_key"):
#                 out[b["cmd_key"]] = b

#     return out

def _load_blocks_index(paths: Agent7Paths, host: str) -> Dict[str, Dict[str, Any]]:
    """
    Returns cmd_key -> block dict (if any):
      { "sanitized_command", "text_path", "platform_hint", "cmd_key" }

    Preferred (authoritative): agent7/3-analyze/0-md-index/<host>__blocks.json
    Optional (legacy only if A7_ALLOW_AUDIT_BACKFILL=1): agent7/audit/<host>__blocks.json
    """
    out: Dict[str, Dict[str, Any]] = {}

    # --- preferred index ---
    idx_new = os.path.join(paths.md_index_dir, f"{host}__blocks.json")
    arr = _read_json(idx_new)
    if isinstance(arr, list):
        for b in arr:
            if isinstance(b, dict) and b.get("cmd_key"):
                out[b["cmd_key"]] = b

    if out:
        # Fresh md-index found → authoritative
        return out

    # --- legacy audit (disabled by default) ---
    if not ALLOW_AUDIT_BACKFILL:
        _dbg(f"[blocks] {host}: no md-index; legacy audit backfill is disabled")
        return {}

    idx_legacy = os.path.join(paths.audit_dir, f"{host}__blocks.json")
    arr2 = _read_json(idx_legacy)
    if isinstance(arr2, list):
        for b in arr2:
            if isinstance(b, dict) and b.get("cmd_key"):
                out[b["cmd_key"]] = b
        if out:
            _dbg(f"[blocks] {host}: using legacy audit backfill (A7_ALLOW_AUDIT_BACKFILL=1)")
    return out


# ------- collect parsed files for a host (new location) -------
def _collect_parsed_for_host(paths: Agent7Paths, host: str) -> Dict[str, Dict[str, Any]]:
    """
    agent7/3-analyze/1-parsed/<host>/<platform_key>__<cmd_key>.json
    Returns map: cmd_key -> {path, platform_hint}
    """
    pat = os.path.join(paths.parsed_dir, host, "*.json")
    rows: Dict[str, Dict[str, Any]] = {}
    for p in sorted(glob.glob(pat)):
        base = os.path.basename(p)
        if "__" not in base:
            continue
        plat_part, cmd_file = base.split("__", 1)
        cmd_key = cmd_file[:-5] if cmd_file.endswith(".json") else cmd_file
        rows[cmd_key] = {"path": p, "platform_hint": plat_part}
    return rows

# ------- helpers for provider chain -------
def _is_empty_data(data: Any) -> bool:
    if data is None:
        return True
    if isinstance(data, (list, dict)) and len(data) == 0:
        return True
    return False

# ---- MCP (stub for future wiring) ----
def _try_mcp_extract(*, cmd: str, text: str, platform_hint: str) -> Optional[Dict[str, Any]]:
    """
    Placeholder for MCP-based extractor. Return an object that fits LLM schema (below),
    or None if not available. Wire your MCP client here later.
    """
    return None

# ---- Hygiene: rotate stale 1-parsed/<other-host>/ to _prev/ when md-index exists ----

def _rotate_stale_parsed(paths: Agent7Paths, keep_hosts: List[str]) -> None:
    """
    Hygiene for triage: if md-index exists (keep_hosts non-empty),
    move parsed outputs for other hosts under 1-parsed/_prev/<ts>/<host>.
    No-op if nothing to rotate.
    """
    if not keep_hosts:
        return
    try:
        import shutil
        ts = time.strftime("%Y%m%d-%H%M%S")
        prev_root = os.path.join(paths.parsed_dir, "_prev", ts)
        os.makedirs(prev_root, exist_ok=True)

        for p in sorted(glob.glob(os.path.join(paths.parsed_dir, "*"))):
            if not os.path.isdir(p):
                continue
            name = os.path.basename(p)
            if name.startswith("_"):
                continue  # skip our own rotations
            if name not in keep_hosts:
                dst = os.path.join(prev_root, name)
                try:
                    shutil.move(p, dst)
                    _dbg(f"[hygiene] rotated parsed/{name} -> {dst}")
                except Exception as e:
                    _dbg(f"[hygiene] rotate failed for {name}: {e}")
    except Exception as e:
        _dbg(f"[hygiene] rotate wrapper failed: {e}")

def _rotate_stale_facts(paths: Agent7Paths, keep_hosts: List[str]) -> None:
    """
    Hygiene for triage: if md-index exists (keep_hosts non-empty),
    move facts for other hosts under 2-facts/_prev/<ts>/<file>.
    """
    if not keep_hosts:
        return
    try:
        import shutil
        ts = time.strftime("%Y%m%d-%H%M%S")
        prev_root = os.path.join(paths.facts_dir, "_prev", ts)
        os.makedirs(prev_root, exist_ok=True)

        for p in sorted(glob.glob(os.path.join(paths.facts_dir, "*.json"))):
            base = os.path.basename(p)
            if base == "facts_summary.json":
                continue
            if base.startswith("_"):  # skip _audit etc.
                continue
            host = base[:-5] if base.endswith(".json") else base
            if host not in keep_hosts:
                dst = os.path.join(prev_root, base)
                try:
                    shutil.move(p, dst)
                    _dbg(f"[hygiene] rotated facts/{base} -> {dst}")
                except Exception as e:
                    _dbg(f"[hygiene] rotate facts failed for {base}: {e}")
    except Exception as e:
        _dbg(f"[hygiene] rotate facts wrapper failed: {e}")

        
# ---- LLM fallback extractor ----
_LLM_SYS = """You extract *structured facts* from a single CLI command output.
Return STRICT JSON only, with this schema:
{
  "summary": "<one sentence, factual>",
  "status": {
    "name": "<short key e.g., bgp_neighbors|bgp_table_state|ospf_neighbors|ospf_database|isis_adjacencies|ldp_neighbors|interfaces|bfd_session|...>",
    "value": "<up|down|established|idle|active|init|full|mixed|degraded|unknown>",
    "confidence": "high" | "medium" | "low",
    "confidence_reason": "<why>"
  },
  "metrics": { "<k>": <number|string|boolean> },
  "tables": { "<name>": [ { "<col>": "<val>", ... } ] },
  "evidence": ["<L##: verbatim evidence line>", "..."]
}

Global rules:
- Use only the provided output; never invent values.
- **Do NOT drop rows.** Preserve every row present (IPv4+IPv6, all VRFs/instances).
- Keep row order as it appears in the CLI.
- If unsure about overall status, set "unknown" with low confidence.
- Keep 1–6 short evidence lines; when possible prefix with a line number (e.g., "L23: ...").

Command intent & allowed outputs (vendor-agnostic):
- First, infer INTENT from the command string and headers:
  • BGP neighbor/summary/neighbor brief  → INTENT=adjacency.neighbors
  • BGP table/IPv4/IPv6/(labeled-)unicast/routes → INTENT=rib.table
  • OSPF neighbor/adjacency               → INTENT=adjacency.neighbors
  • OSPF database/show ospf database      → INTENT=database
  • IS-IS adjacency                       → INTENT=adjacency.neighbors
  • IS-IS database/LSP/RIB                → INTENT=database
  • LDP neighbors/peers                   → INTENT=adjacency.neighbors
  • BFD session/detail                    → INTENT=single_session
  • Interface brief/status                → INTENT=interfaces
- Then choose fields consistent with INTENT:
  • INTENT=adjacency.neighbors:
      - status.name MUST be one of: "bgp_neighbors", "ospf_neighbors", "isis_adjacencies", "ldp_neighbors"
      - table name SHOULD be one of: tables.bgp_neighbors | tables.ospf_neighbors | tables.isis_adjacencies | tables.ldp_neighbors
      - produce per-row state and rollups: metrics.<table>_total, metrics.<table>_by_state
  • INTENT=rib.table (routing table / RIB views like "show bgp ipv4 ..."):
      - status.name MUST be "bgp_table_state" (or "bgp_rib_state")
      - DO NOT emit tables.bgp_neighbors and DO NOT infer neighbor states from routes
      - prefer tables.routes or tables.prefixes; include columns as seen (Network, Next Hop, Best, etc.)
      - metrics can include prefixes_total, paths_total, best_paths, rib_state, etc.
      - status.value may mirror header state (e.g., "active") if present; otherwise "unknown"
  • INTENT=database (OSPF/ISIS DB):
      - status.name one of: "ospf_database", "isis_database"
      - tables: tables.lsas / tables.lsps / tables.database
      - no neighbor-state rollups unless explicitly present
  • INTENT=single_session (BFD detail):
      - status.name: "bfd_session"
      - include timers/intervals; state is typically UP/DOWN
  • INTENT=interfaces:
      - status.name: "interfaces"
      - include Admin/Oper state columns and rollups by oper state when present

Row detection & reconstruction:
- A line **starts a new row** if it begins with: an IPv4 address, an IPv6 address, an interface name, or another obvious key column; otherwise treat it as a **continuation** of the previous row.
- Reconstruct wrapped rows (e.g., IPv6 neighbors wrapping onto a second indented line) into a single row.

Tabular outputs:
- Include contextual fields when present (VRF, AddressFamily, Instance/Process, Node/Slot/RP).
- Determine the **state column** deterministically using the first present in:
  NBRState, State, Status, OperState, LineP/Proto, AdminState.
  Store the chosen column name in `metrics.<table>_state_column`.
- Emit rollups **only when a real state column exists**:
  • `"<table>_total": <int>` (must equal the number of rows)
  • `"<table>_by_state": { "<state-lowercased>": <count>, ... }`
- Derive overall `status.value` from the table when applicable:
  • all rows up/established → "up" or "established"
  • all rows down/idle      → "down" or "idle"
  • mixture of states       → "mixed"
  • no rows / no state      → "unknown"
  Set `confidence_reason` accordingly.

Non-tabular outputs:
- Put key-value sections into a plural table (e.g., tables.timers, tables.parameters).
- Mirror important timed values as numbers in metrics (e.g., durations_to_seconds) while keeping the original strings in tables.

Normalization & typing:
- When values include units ("2d19h", "500 ms"), keep the string in tables and add numeric mirrors in `metrics` (e.g., `*_seconds`, `*_ms`).
- Use lowercase keys for `*_by_state`. Do not invent states.

Quality/truncation checks:
- If the input appears truncated, set `metrics.input_truncated=true`.
- **Row accounting must reconcile** when a state column exists:
  `metrics.<table>_total == len(tables.<table>)` and
  `sum(metrics.<table>_by_state.values()) == metrics.<table>_total`.
  If reconciliation fails, set `metrics.validation_error=true` and still return all rows.

Always return valid JSON with: summary, status, metrics, tables, evidence.
"""

def _llm_extract_from_text(*, cmd: str, text: str, platform_hint: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Calls LLM to extract structured facts from CLI text.
    Returns (parsed_obj_or_none, raw_response_text_or_none).
    """
    if not call_llm:
        return None, None

    snippet = text[:45000]
    payload = {
        "command": cmd,
        "platform_hint": platform_hint,
        "output": snippet,
    }
    msgs = [
        {"role": "system", "content": _LLM_SYS},
        {"role": "user",   "content": "```json\n" + json.dumps(payload, indent=2) + "\n```"},
    ]

    raw_text: Optional[str] = None
    try:
        raw = call_llm(msgs, temperature=0.0) or ""
        # Normalize raw → string for auditing
        if isinstance(raw, str):
            raw_text = raw
        elif isinstance(raw, dict):
            raw_text = json.dumps(raw)
        else:
            raw_text = str(raw)

        # Robust parse: permit code-fence
        t = raw_text.strip()
        if t.startswith("```"):
            lines = t.splitlines()
            if lines:
                lines = lines[1:]  # drop ``` or ```json
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]  # drop closing ```
            t = "\n".join(lines).strip()

        obj = json.loads(t)
        if isinstance(obj, dict) and "status" in obj and "summary" in obj:
            return obj, raw_text

        # Parsed but not the expected shape → still return raw for audit
        return None, raw_text

    except Exception as e:
        _dbg(f"[llm] extract failed for '{cmd}': {e}")
        return None, raw_text

# ------- core facts build for a single host -------
def _build_facts_for_host(paths: Agent7Paths, host: str) -> Dict[str, Any]:
    blocks_by_key = _load_blocks_index(paths, host)
    parsed_map = _collect_parsed_for_host(paths, host)

    # Step-local audit directory for raw LLM replies
    audit_dir = os.path.join(paths.facts_dir, "_audit")
    os.makedirs(audit_dir, exist_ok=True)

    # ---- Option A gating: NEVER revive old parsed JSON when md-index has 0 blocks ----
    # (e.g., TCP error capture produced no "## show ..." sections)
    md_index_fp = os.path.join(paths.md_index_dir, f"{host}__blocks.json")
    md_arr = _read_json(md_index_fp)
    md_block_count = len(md_arr) if isinstance(md_arr, list) else 0
    _dbg(f"[blocks] {host}: md_blocks={md_block_count} parsed_cmds={len(parsed_map)}")

    if os.path.isfile(md_index_fp) and md_block_count == 0:
        # Explicitly ignore any leftover 1-parsed data for safety
        parsed_map = {}
        blocks_by_key = {}
        _dbg(f"[blocks] {host}: 0 md-index blocks → suppressing parsed backfill")

    # Consider ONLY commands present in md-index; parsed_map enriches those same commands
    all_cmd_keys: List[str] = sorted(list(blocks_by_key.keys()))
    _dbg(f"[select] {host}: cmd_keys={all_cmd_keys}")

    commands: Dict[str, Any] = {}
    platforms_seen: List[str] = []
    genie_ok = genie_err = llm_ok = 0
    gap_fill_used = False

    for cmd_key in all_cmd_keys:
        b = blocks_by_key.get(cmd_key, {})  # may be {}
        sanitized_cmd = b.get("sanitized_command") or cmd_key.replace("_", " ")
        text_path = b.get("text_path") or ""
        plat_hint = normalize_platform(b.get("platform_hint") or "")

        # Try Genie first if a parsed file exists (for THIS cmd_key only)
        genie_row = parsed_map.get(cmd_key)
        genie_data = None
        if genie_row:
            data = _read_json(genie_row["path"])
            if _is_empty_data(data):
                genie_err += 1
            else:
                genie_data = data
                platforms_seen.append(normalize_platform(genie_row["platform_hint"]))
                genie_ok += 1

        # If Genie failed/empty, try MCP (stub), then LLM fallback using the md-index text
        llm_data: Optional[Dict[str, Any]] = None
        if genie_data is None:
            # MCP (stub)
            if text_path:
                mcp_obj = _try_mcp_extract(cmd=sanitized_cmd, text=_read_text(text_path), platform_hint=plat_hint)
            else:
                mcp_obj = None

            if isinstance(mcp_obj, dict):
                llm_data = mcp_obj  # MCP conforms to same shape
                llm_ok += 1
                gap_fill_used = True
            elif text_path:
                llm_obj, raw_text = _llm_extract_from_text(
                    cmd=sanitized_cmd,
                    text=_read_text(text_path),
                    platform_hint=plat_hint
                )
                # Always write the raw response if we got one (even if parsing failed)
                if raw_text:
                    audit_fp = os.path.join(audit_dir, f"{host}__{cmd_key}__llm_extract.raw")
                    try:
                        with open(audit_fp, "w", encoding="utf-8") as fh:
                            fh.write(raw_text)
                        _dbg(f"[audit] wrote {audit_fp}")
                    except Exception as e:
                        _dbg(f"[audit] write failed for {audit_fp}: {e}")

                if isinstance(llm_obj, dict):
                    llm_data = llm_obj
                    llm_ok += 1
                    gap_fill_used = True

        # Decide what to write for this command
        if genie_data is not None:
            commands[cmd_key] = {
                "command": sanitized_cmd or "(unknown)",
                "topic": _topic_from_command(sanitized_cmd),
                "platform_hint": plat_hint or (platforms_seen[0] if platforms_seen else "unknown"),
                "source": "genie",
                "parsed_path": genie_row["path"] if genie_row else "",
                "evidence_text_path": text_path,
                "parser_ok": True,
                "data": genie_data,
                "genie_data": genie_data,
            }
        elif llm_data is not None:
            commands[cmd_key] = {
                "command": sanitized_cmd or "(unknown)",
                "topic": _topic_from_command(sanitized_cmd),
                "platform_hint": plat_hint or "unknown",
                "source": "llm",
                "parsed_path": "",  # no Genie JSON
                "evidence_text_path": text_path,
                "parser_ok": False,  # honest: this is LLM, not deterministic parser
                "data": llm_data,    # effective object used by analyzers
                "llm_data": llm_data
            }
        else:
            # Nothing usable → skip creating an entry for this cmd_key
            continue

    # platform roll-up
    plat = "unknown"
    if platforms_seen:
        from collections import Counter
        plat = Counter(platforms_seen).most_common(1)[0][0]

    facts = {
        "hostname": host,
        "platform_hint": plat,
        "signals_seen": _signal_set(paths, host),  # optional, may be empty
        "generated_at": int(time.time()),
        "facts_version": 1,
        "coverage": {
            "genie_ok": genie_ok,
            "genie_err": genie_err,
            "llm_ok": llm_ok,
            "total_cmds": len(all_cmd_keys),
            "total_enriched": genie_ok + llm_ok,
        },
        "commands": commands,
        "notes": {
            "gap_fill_permitted": True,
            "gap_fill_used": gap_fill_used,
            "providers": ["mcp(if-wired)", "genie", "llm"],
        },
    }
    return facts

# ------- public: build all hosts -------
def build_all(config_dir: str, task_dir: str) -> Dict[str, Any]:
    """
    Build per-host facts:
      - Prefer hosts discovered from md-index (authoritative when present).
      - Fall back to parsed/ only if md-index is entirely absent.
      - When md-index exists, rotate parsed and facts for non-indexed hosts.
    """
    cfg = load_config()
    paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    md_hosts = _hosts_from_md_index(paths)
    parsed_hosts = _hosts_from_parsed(paths)

    if md_hosts:
        hosts = sorted(md_hosts)
        _rotate_stale_parsed(paths, keep_hosts=hosts)  # already added earlier
        _rotate_stale_facts(paths,  keep_hosts=hosts)  # <<< NEW
    else:
        hosts = sorted(set(parsed_hosts))

    _dbg(f"[build] host_set={hosts} (md_index={len(md_hosts)}, parsed={len(parsed_hosts)})")

    written: List[str] = []
    for h in hosts:
        facts = _build_facts_for_host(paths, h)
        out_path = os.path.join(paths.facts_dir, f"{h}.json")
        _write_json(out_path, facts)
        written.append(out_path)
        _dbg(f"[write] {out_path} (cmds={len(facts.get('commands', {}))})")

    summary = {
        "config_dir": config_dir,
        "task_dir": task_dir,
        "hosts": len(hosts),
        "facts_written": written,
    }
    _write_json(os.path.join(paths.analyze_dir, "facts_summary.json"), summary)
    _dbg(f"[done] facts for {len(hosts)} host(s)")
    return summary

# ------- CLI -------
def _main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/facts_builder.py <config_dir> <task_dir>")
        raise SystemExit(2)
    build_all(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    _main()