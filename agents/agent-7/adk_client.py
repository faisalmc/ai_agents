# ai_agents/agents/agent-7/adk_client.py
from __future__ import annotations
import os, json, time, hashlib, re
from typing import Any, Dict, List, Optional

from bootstrap import Agent7Config, Agent7Paths, load_config, resolve_paths, ensure_dirs

# ---------------------------
# Optional deps (graceful if missing)
# ---------------------------
try:
    from shared.llm_api import call_llm  # type: ignore
except Exception:
    call_llm = None

try:
    from agent5_shared import dbg as _dbg, sanitize_show, normalize_platform  # type: ignore
except Exception:
    def _dbg(msg: str) -> None:
        print(f"[agent7][adk] {msg}", flush=True)
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

# ---------------------------
# Cache helpers
# ---------------------------
def _cache_path(paths: Agent7Paths) -> str:
    # Keep it human-inspectable under meta/
    return os.path.join(paths.meta_dir, "adk_cache.json")

def _load_cache(paths: Agent7Paths) -> Dict[str, Any]:
    fn = _cache_path(paths)
    try:
        with open(fn, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_cache(paths: Agent7Paths, cache: Dict[str, Any]) -> None:
    fn = _cache_path(paths)
    try:
        os.makedirs(os.path.dirname(fn), exist_ok=True)
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass

def _hash_request(payload: Dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def _expired(ts: float, ttl_min: int) -> bool:
    return (time.time() - ts) > (ttl_min * 60)

# ---------------------------
# Seed (offline) provider
# ---------------------------
def _seed_dir(repo_root: str) -> str:
    # Optional curated snippets for offline/CI runs
    return os.path.join(repo_root, "_agent_knowledge", "adk_seed")

def _seed_lookup(repo_root: str, platform: str, signal: str) -> List[Dict[str, Any]]:
    """
    Reads seed JSON if present:
      _agent_knowledge/adk_seed/<platform>/<signal>.json
    File format: [{"title": "...", "url": "...", "source": "cisco", "excerpt": "..."}, ...]
    """
    plat = normalize_platform(platform)
    path = os.path.join(_seed_dir(repo_root), plat, f"{signal.lower()}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data[:10]
    except Exception:
        pass
    return []

# ---------------------------
# (Future) Google ADK provider stub
# ---------------------------
class _GoogleADKProvider:
    """
    Placeholder for a real Google ADK client.
    Implement the `.search(query, *, platform, version, signal, limit)` method
    to return a list of {title, url, source, excerpt}.
    """
    def __init__(self) -> None:
        # Wire real credentials/SDK here later.
        pass

    def search(self, query: str, *, platform: str, version: Optional[str],
               signal: str, limit: int = 6) -> List[Dict[str, Any]]:
        # Not implemented in Phase-1; return empty to fall back to seed.
        return []

def _pick_provider() -> Any:
    """
    Chooses a provider based on env. For Phase-1 we default to seed provider.
    Set AGENT7_ADK_PROVIDER=google to enable the stub (still returns empty).
    """
    prov = os.getenv("AGENT7_ADK_PROVIDER", "seed").strip().lower()
    if prov == "google":
        return _GoogleADKProvider()
    return None  # None means: use seed only

# ---------------------------
# Helpers: normalize snippet field
# ---------------------------
def _norm_row(r: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure downstream sees 'snippet'. Also mirror to 'excerpt' for backward readers.
    """
    if not isinstance(r, dict):
        return {}
    title = r.get("title", "")
    url = r.get("url", "")
    source = r.get("source", "")
    snippet = r.get("snippet") or r.get("excerpt") or r.get("summary") or ""
    if not isinstance(snippet, str):
        snippet = str(snippet)
    out = {"title": title, "url": url, "source": source, "snippet": snippet}
    # keep 'excerpt' as alias for compatibility
    out["excerpt"] = snippet
    return out

# ---------------------------
# LLM helpers
# ---------------------------
_CANON_SYSTEM = """You are validating whether a CLI 'show ...' command is CANONICAL for a given signal on a platform.
Return JSON only:
{
  "decision": "canonical" | "unknown",
  "confidence": "high" | "medium" | "low",
  "reasons": ["..."],
  "evidence_urls": ["..."]
}
Use the excerpts provided. Be conservative. If unclear, return "unknown".
"""

def _llm_judge_canonical(cmd: str, signal: str, platform: str,
                         snippets: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not call_llm:
        return {"decision": "unknown", "confidence": "low", "reasons": ["LLM unavailable"], "evidence_urls": []}
    payload = {
        "platform": platform,
        "signal": signal,
        "command": cmd,
        "snippets": [
            {"title": s.get("title"), "url": s.get("url"), "excerpt": s.get("snippet") or s.get("excerpt")}
            for s in snippets[:8]
        ],
    }
    try:
        msgs = [
            {"role": "system", "content": _CANON_SYSTEM},
            {"role": "user", "content": "```json\n" + json.dumps(payload, indent=2) + "\n```"}
        ]
        raw = call_llm(msgs, temperature=0.0)  # deterministic
        try:
            obj = json.loads(raw)
        except Exception:
            m = re.search(r"```json\s*(.+?)\s*```", raw or "", flags=re.DOTALL | re.IGNORECASE)
            obj = json.loads(m.group(1)) if m else {}
        if isinstance(obj, dict) and obj.get("decision"):
            return obj
    except Exception as e:
        _dbg(f"[llm] canonical judge failed: {e}")
    return {"decision": "unknown", "confidence": "low", "reasons": ["parse_error"], "evidence_urls": []}

# ---------------------------
# Public client
# ---------------------------
class ADKClient:
    """
    Phase-1: hybrid doc fetcher
      • Uses local seed snippets (optional) for offline determinism.
      • Optional provider hook for Google ADK (stub).
      • JSON cache with TTL under agent7/meta/adk_cache.json.
      • LLM-backed canonical validation (optional).
    """

    def __init__(self, config_dir: str, task_dir: str) -> None:
        cfg = load_config()
        self.cfg: Agent7Config = cfg
        self.paths: Agent7Paths = resolve_paths(cfg, config_dir, task_dir)
        ensure_dirs(self.paths)
        self.ttl_min = int(os.getenv("AGENT7_ADK_CACHE_TTL_MIN", str(cfg.cache_ttl_min or 15)))
        self.provider = _pick_provider()
        self.cache = _load_cache(self.paths)

    # ---- core search ----
    def query_docs(self, query: str, *, platform: str, signal: str,
                   version: Optional[str] = None, limit: int = 6,
                   force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Returns a list of normalized snippets: [{"title","url","source","snippet","excerpt"}, ...]
        Cache key includes query+platform+signal+version.
        """
        platform_n = normalize_platform(platform)
        req = {"q": query, "platform": platform_n, "signal": signal.lower(), "version": version, "limit": limit}
        key = _hash_request(req)

        # cache check
        entry = self.cache.get(key)
        if entry and not force_refresh and not _expired(entry.get("ts", 0), self.ttl_min):
            return entry.get("results", [])

        # provider first (if configured)
        results: List[Dict[str, Any]] = []
        try:
            if self.provider is not None:
                raw = self.provider.search(query, platform=platform_n, version=version, signal=signal, limit=limit) or []
                results = [_norm_row(r) for r in raw if isinstance(r, dict)]
        except Exception as e:
            _dbg(f"[provider] search failed: {e}")

        # fall back to seed
        if not results:
            seed = _seed_lookup(self.cfg.repo_root, platform_n, signal)
            results = [_norm_row(r) for r in seed if isinstance(r, dict)]

        # persist cache (normalized)
        self.cache[key] = {"ts": time.time(), "request": req, "results": results}
        _save_cache(self.paths, self.cache)
        return results

    # ---- judgment helpers ----
    def confirm_canonical(self, cmd: str, *, platform: str, signal: str,
                          version: Optional[str] = None) -> Dict[str, Any]:
        """
        Validates whether 'cmd' appears canonical for the signal on this platform.
        Uses LLM over fetched snippets when available; otherwise falls back to keyword checks.
        """
        clean = sanitize_show(cmd, platform)
        if not clean:
            return {"decision": "unknown", "confidence": "low", "reasons": ["not_a_show_cmd"], "evidence_urls": []}

        # Build a neutral query around the topic (no hardcoding of command semantics)
        topic_q = f"{signal} {platform} show command reference {version or ''}".strip()
        snippets = self.query_docs(topic_q, platform=platform, signal=signal, version=version, limit=8)

        # LLM route (preferred)
        if snippets and call_llm:
            return _llm_judge_canonical(clean, signal, platform, snippets)

        # Fallback: keyword-only, conservative
        urls = [s.get("url") for s in snippets if isinstance(s, dict)]
        text = " ".join((s.get("title", "") + " " + (s.get("snippet") or s.get("excerpt") or "")) for s in snippets)
        look = clean.lower().replace("  ", " ")
        decision = "canonical" if look in text.lower() else "unknown"
        conf = "medium" if decision == "canonical" else "low"
        return {
            "decision": decision,
            "confidence": conf,
            "reasons": ["keyword_match" if decision == "canonical" else "insufficient_evidence"],
            "evidence_urls": urls[:8],
        }

    def suggest_canonical_commands(self, *, signal: str, platform: str,
                                   version: Optional[str] = None, limit: int = 6) -> List[str]:
        """
        Suggest likely 'show ...' commands for a signal/platform from docs.
        Uses LLM to extract commands from snippets when available; otherwise returns empty.
        """
        snippets = self.query_docs(
            f"{signal} troubleshooting {platform} commands",
            platform=platform, signal=signal, version=version, limit=limit
        )
        if not snippets or not call_llm:
            return []
        payload = {
            "signal": signal, "platform": platform, "version": version,
            "snippets": [{"title": s.get("title"), "excerpt": (s.get("snippet") or s.get("excerpt") or "")} for s in snippets[:8]]
        }
        sys = ("Extract up to 8 CLI *read-only* commands from the excerpts that start with 'show '. "
               "Return JSON: {\"commands\": [\"show ...\", ...]}. Do not invent; be conservative.")
        try:
            msgs = [
                {"role": "system", "content": sys},
                {"role": "user", "content": "```json\n" + json.dumps(payload, indent=2) + "\n```"},
            ]
            raw = call_llm(msgs, temperature=0.0)
            obj = json.loads(raw)
            cmds = obj.get("commands", []) if isinstance(obj, dict) else []
            out = []
            for c in cmds:
                clean = sanitize_show(str(c), platform)
                if clean:
                    out.append(clean)
            # de-dup while preserving order
            seen = set()
            uniq = []
            for c in out:
                lc = c.lower()
                if lc not in seen:
                    seen.add(lc)
                    uniq.append(c)
            return uniq
        except Exception as e:
            _dbg(f"[llm] suggest_canonical_commands failed: {e}")
            return []

# ---------------------------
# CLI (simple debug)
# ---------------------------
def _main():
    """
    Debug usage:
      python agents/agent-7/adk_client.py <config_dir> <task_dir> <signal> <platform> [version]
    """
    import sys
    if len(sys.argv) < 5:
        print("Usage: python agents/agent-7/adk_client.py <config_dir> <task_dir> <signal> <platform> [version]")
        raise SystemExit(2)
    config_dir, task_dir, signal, platform = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    version = sys.argv[5] if len(sys.argv) > 5 else None

    client = ADKClient(config_dir, task_dir)
    print("== seed/provider docs ==")
    res = client.query_docs(f"{signal} {platform} command reference", platform=platform, signal=signal, version=version)
    print(json.dumps(res[:2], indent=2))

    if res:
        print("== canonical check (first guess) ==")
        guess = client.suggest_canonical_commands(signal=signal, platform=platform, version=version)[:1]
        if guess:
            print(json.dumps(client.confirm_canonical(guess[0], platform=platform, signal=signal, version=version), indent=2))
        else:
            print("(no suggestions)")

if __name__ == "__main__":
    _main()