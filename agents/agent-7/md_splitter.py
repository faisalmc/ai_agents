# agents/agent-7/md_splitter.py
from __future__ import annotations
import os, re, json, glob, hashlib, time
from typing import Any, Dict, List

# ---------------------------
# Optional shared helpers (graceful fallback)
# ---------------------------
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

def _dbg(msg: str) -> None:
    print(f"[agent7][md_splitter] {msg}", flush=True)

# Canonical paths (no dynamic loaders)
from bootstrap import (
    Agent7Paths,
    load_config,
    resolve_paths,
    ensure_dirs,
)

# ---------------------------
# Inputs: .md from two locations (merge)
# ---------------------------
def _read_md_for_task(paths: Agent7Paths) -> Dict[str, str]:
    """
    Returns {hostname: merged_markdown_text}
    Merge order:
      1) <task>/grading_logs/*.md           (original logs, if present)
      2) <task>/agent7/2-capture/show_logs/*.md  (fresh capture copied by Agent-7)
    """
    def _read_dir(md_dir: str) -> Dict[str, str]:
        out: Dict[str, str] = {}
        if os.path.isdir(md_dir):
            for p in sorted(glob.glob(os.path.join(md_dir, "*.md"))):
                try:
                    host = os.path.basename(p)[:-3]  # strip ".md"
                    out[host] = open(p, "r", encoding="utf-8").read()
                except Exception:
                    pass
        return out

    orig = _read_dir(os.path.join(paths.task_root, "grading_logs"))
    fresh = _read_dir(paths.show_logs_dir)

    all_hosts = set(orig) | set(fresh)
    merged: Dict[str, str] = {}
    for h in sorted(all_hosts):
        a = orig.get(h, "")
        b = fresh.get(h, "")
        merged[h] = a + ("\n\n" if a and b else "") + b
    _dbg(f"[inputs] hosts with markdown: {len(merged)}")
    return merged

# ---------------------------
# Section & code-fence parsing
# ---------------------------
_HEADING = re.compile(r"^#{2,4}\s+(.+)$")  # ## ... or ### ...
_CODE_FENCE = re.compile(r"^```")          # triple backticks

def _infer_platform(md_text: str) -> str:
    if not md_text: return "unknown"
    if "RP/" in md_text or "IOS XR" in md_text or "config-bgp" in md_text:
        return "cisco-ios-xr"
    if "IOS Software" in md_text or "Building configuration" in md_text:
        return "cisco-ios"
    return "unknown"

def _slugify(s: str, max_len: int = 40) -> str:
    s = re.sub(r"[^a-zA-Z0-9._\-]+", "_", (s or "").strip().lower())
    return s[:max_len].strip("_") or "block"

def _sha1(txt: str) -> str:
    return hashlib.sha1((txt or "").encode("utf-8", errors="ignore")).hexdigest()

def _safe_cmd_key(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_:\-\.]", "", s)
    return s[:160] or "unknown"

def _extract_blocks(md_text: str) -> List[Dict[str, Any]]:
    """
    Splits the markdown into blocks keyed by headings that contain 'show'.
    Each block captures:
      - heading text
      - echoed command (first non-empty line in first code fence)
      - output_text (code fence body minus echoed line)
      - line numbers for traceability
    """
    blocks: List[Dict[str, Any]] = []
    if not md_text:
        return blocks

    lines = md_text.splitlines()
    n = len(lines)
    i = 0
    while i < n:
        m = _HEADING.match(lines[i])
        if not m:
            i += 1
            continue

        heading_text = m.group(1).strip()
        if "show " not in heading_text.lower():
            i += 1
            continue

        # find first code fence after heading
        j = i + 1
        while j < n and not _CODE_FENCE.match(lines[j]):
            j += 1
        if j >= n:
            i += 1
            continue

        # enter fence body
        j += 1
        body_lines: List[str] = []
        while j < n and not _CODE_FENCE.match(lines[j]):
            body_lines.append(lines[j])
            j += 1

        # first non-empty line is echoed command
        k = 0
        while k < len(body_lines) and not body_lines[k].strip():
            k += 1
        echoed = body_lines[k].strip() if k < len(body_lines) else ""
        output_lines = body_lines[k+1:] if k < len(body_lines) else body_lines
        output_text = "\n".join(output_lines).rstrip()

        blocks.append({
            "heading": heading_text,
            "echoed": echoed,
            "output_text": output_text,
            "start_line": i + 1,
            "end_line": min(j + 1, n),
        })
        i = j + 1 if j < n else j
    return blocks

# ---------------------------
# Writer
# ---------------------------
def _write_blocks_for_host(paths: Agent7Paths, host: str, md_text: str) -> List[Dict[str, Any]]:
    """
    Writes per-block files and a JSON index under:
      agent7/3-analyze/0-md-index/<host>__blocks.json
      agent7/3-analyze/0-md-index/<host>/*.txt   (raw outputs)
    Also mirrors the JSON index to:
      agent7/audit/<host>__blocks.json           (back-compat for downstream readers)
    """
    plat = normalize_platform(_infer_platform(md_text))
    blocks = _extract_blocks(md_text)

    host_dir = os.path.join(paths.md_index_dir, host)
    os.makedirs(host_dir, exist_ok=True)

    index_entries: List[Dict[str, Any]] = []
    for idx, blk in enumerate(blocks, start=1):
        echoed = blk.get("echoed", "")
        echoed_clean = sanitize_show(echoed, plat)
        # choose file stem from sanitized command if available, otherwise heading
        stem_src = echoed_clean or blk.get("heading", "block")
        stem = f"{idx:03d}__{_slugify(stem_src)}"
        body = blk.get("output_text", "")
        sha = _sha1(body)
        text_path = os.path.join(host_dir, f"{stem}.txt")

        # write body
        with open(text_path, "w", encoding="utf-8") as fh:
            fh.write(body + ("\n" if body and not body.endswith("\n") else ""))

        entry = {
            "host": host,
            "platform_hint": plat,
            "heading": blk.get("heading"),
            "echoed": echoed,
            "sanitized_command": echoed_clean,
            "cmd_key": _safe_cmd_key(echoed_clean or blk.get("heading", "")),
            "output_text_sha1": sha,
            "text_path": text_path,
            "start_line": blk.get("start_line"),
            "end_line": blk.get("end_line"),
        }
        index_entries.append(entry)

    # write per-host JSON index (list)
    json_index = os.path.join(paths.md_index_dir, f"{host}__blocks.json")
    with open(json_index, "w", encoding="utf-8") as fh:
        json.dump(index_entries, fh, indent=2)

    # mirror to audit for downstream readers that still look there
    audit_index = os.path.join(paths.audit_dir, f"{host}__blocks.json")
    try:
        with open(audit_index, "w", encoding="utf-8") as fh:
            json.dump(index_entries, fh, indent=2)
    except Exception:
        pass

    _dbg(f"[write] host={host} blocks={len(index_entries)} → {json_index}")
    return index_entries

# ---------------------------
# Orchestrate for task
# ---------------------------
def split_task(config_dir: str, task_dir: str) -> Dict[str, Any]:
    """
    Processes all host markdown and writes:
      - agent7/3-analyze/0-md-index/<host>__blocks.json
      - agent7/3-analyze/0-md-index/<host>/*.txt (raw outputs)
      - agent7/meta/md_index_summary.json (summary)
    Returns the summary dict.
    """
    cfg = load_config()
    paths = resolve_paths(cfg, config_dir, task_dir)
    ensure_dirs(paths)

    md_map = _read_md_for_task(paths)
    summary: Dict[str, Any] = {
        "config_dir": config_dir,
        "task_dir": task_dir,
        "generated_at": int(time.time()),
        "hosts": {},
    }

    total_blocks = 0
    for host, md_text in md_map.items():
        entries = _write_blocks_for_host(paths, host, md_text)
        total_blocks += len(entries)
        summary["hosts"][host] = {
            "platform_hint": entries[0]["platform_hint"] if entries else "unknown",
            "blocks": len(entries),
            "dir": os.path.join(paths.md_index_dir, host),
            "index_path": os.path.join(paths.md_index_dir, f"{host}__blocks.json"),
        }

    # write summary index
    idx_path = os.path.join(paths.meta_dir, "md_index_summary.json")
    os.makedirs(os.path.dirname(idx_path), exist_ok=True)
    with open(idx_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    _dbg(f"[summary] hosts={len(summary['hosts'])} total_blocks={total_blocks} → {idx_path}")
    return summary

# ---------------------------
# CLI
# ---------------------------
def _main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python agents/agent-7/md_splitter.py <config_dir> <task_dir>")
        raise SystemExit(2)
    config_dir, task_dir = sys.argv[1], sys.argv[2]
    split_task(config_dir, task_dir)

if __name__ == "__main__":
    _main()