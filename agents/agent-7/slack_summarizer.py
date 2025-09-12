# agents/agent-7/slack_summarizer.py
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

# LLM wrapper (graceful fallback if missing)
try:
    from shared.llm_api import call_llm  # type: ignore
except Exception:
    call_llm = None  # degrade gracefully

# Slack action id (kept identical to orchestrator listener)
ATTACH_BTN_ACTION_ID = "agent7_attach_artifacts"

# ---- small Slack helpers -----------------------------------------------------
def _mk_section(text: str) -> Dict[str, Any]:
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

def _mk_divider() -> Dict[str, Any]:
    return {"type": "divider"}

def _opt(text: str, value: str) -> Dict[str, Any]:
    return {"text": {"type": "plain_text", "text": text, "emoji": True}, "value": value}

# ---- compact / rollup helpers ------------------------------------------------
def _compact_json(obj: Any, limit: int = 45000) -> str:
    try:
        s = json.dumps(obj, ensure_ascii=False)
    except Exception:
        s = "{}"
    return s if len(s) <= limit else s[:limit]

def _rollup_from_per_device(per_device: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
    for row in per_device or []:
        s = str(row.get("status", "unknown")).lower()
        counts[s] = counts.get(s, 0) + 1 if s in counts else counts["unknown"] + 1
    return counts

# ---- LLM prompt --------------------------------------------------------------
_SYS = """You are a NOC Slack summarizer.
Input:
  • per_device: list of device analyses (validated, evidence-backed; schema may evolve)
  • cross: cross-device correlation (schema may evolve)
Your task: produce a concise operator-ready summary for Slack that states BOTH
  (a) what is working and (b) what is broken/suspicious.

Hard rules:
- Use only devices present in the input; do NOT invent names.
- Keep it brief and scannable. Avoid redundancy.
- Output STRICT JSON only (no extra fields) with this schema:
{
  "network_summary": "<1–2 short lines; first line = overall counts; second line = one 'working' highlight and one 'issue' highlight when applicable>",
  "status_rollup": { "healthy": <int>, "degraded": <int>, "error": <int>, "unknown": <int> },

  "device_cards": [
    {
      "host": "<hostname>",
      "status": "healthy" | "degraded" | "error" | "unknown",
      "lines": ["<≤4 concise bullets about the device; include positives if present>"]
    }
  ],

  "cross_section": {
    "network_status": "<one line status like 'mixed/degraded/healthy' in plain language>",
    "incidents": ["<≤3 one-line incident summaries with device names>"],
    "themes": ["<≤5 remediation themes>"],
    "followups": {
      "trusted": ["show ..."],
      "unvalidated": ["show ..."],
      "probes": ["ping ...", "traceroute ..."]
    }
  }
}

Guidance:
- Derive status_rollup from per_device when present; otherwise infer from cross if possible.
- device_cards: pick up to 5 most informative devices (mix of good and bad).
- Use only read-only commands or safe probes in followups (show/ping/traceroute).
- No config/clear/reload/debug/copy/write/monitor suggestions.
"""

def _build_messages(per_device: List[Dict[str, Any]], cross: Dict[str, Any], rollup_hint: Dict[str, int]) -> List[Dict[str, str]]:
    ctx = {
        "per_device": per_device,
        "cross": cross or {},
        "rollup_hint": rollup_hint
    }
    user = "```json\n" + _compact_json(ctx) + "\n```"
    return [{"role": "system", "content": _SYS}, {"role": "user", "content": user}]

# ---- public API (plug-compatible with slack_ui.build_overview_blocks) --------
def build_overview_blocks(
    config_dir: str,
    task_dir: str,
    cross: Dict[str, Any] | None,
    per_device: List[Dict[str, Any]] | None,
    *,
    include_attach_button: bool = False,
) -> List[Dict[str, Any]]:
    cross = cross or {}
    per_device = per_device or []

    # Prepare rollup hint deterministically (LLM may reuse it)
    rollup_hint = _rollup_from_per_device(per_device)

    # Call LLM for summary JSON
    llm_obj: Dict[str, Any] = {}
    if call_llm is not None:
        try:
            msgs = _build_messages(per_device, cross, rollup_hint)
            raw = call_llm(msgs, temperature=0.0) or ""
            tmp = json.loads(raw) if isinstance(raw, str) else {}
            if isinstance(tmp, dict):
                llm_obj = tmp
        except Exception:
            llm_obj = {}

    # Fallback: minimal structure if LLM fails
    if not llm_obj:
        llm_obj = {
            "network_summary": f"{rollup_hint.get('healthy',0)} healthy • {rollup_hint.get('degraded',0)} degraded • {rollup_hint.get('error',0)} error • {rollup_hint.get('unknown',0)} unknown.",
            "status_rollup": rollup_hint,
            "device_cards": [
                {
                    "host": r.get("hostname","?"),
                    "status": r.get("status","unknown"),
                    "lines": [
                        f"Signals: {', '.join(r.get('signals_seen',[])[:8]) or '—'}",
                        *(f"• [{fnd.get('severity','info')}] {fnd.get('signal','meta')} — {fnd.get('summary','')}"
                          for fnd in (r.get("findings") or [])[:2])
                    ]
                } for r in per_device[:5]
            ],
            "cross_section": {
                "network_status": cross.get("task_status","unknown"),
                "incidents": [f"• {inc.get('summary','')}" for inc in (cross.get("top_incidents") or [])[:3]],
                "themes": (cross.get("remediation_themes") or [])[:5],
                "followups": {
                    "trusted": (cross.get("trusted_followup_cmds") or [])[:6],
                    "unvalidated": (cross.get("unvalidated_followup_cmds") or [])[:6],
                    "probes": (cross.get("optional_active_probes") or [])[:4],
                }
            }
        }

    # ---- Build Slack blocks from llm_obj (schema-safe, concise) ---------------
    blocks: List[Dict[str, Any]] = []
    blocks.append(_mk_section(f"*Agent-7 Overview*\n*Config:* `{config_dir}` • *Task:* `{task_dir}`"))

    net_sum = str(llm_obj.get("network_summary","")).strip()
    if net_sum:
        blocks.append(_mk_section(net_sum))

    # status rollup line
    sr = llm_obj.get("status_rollup") or {}
    if isinstance(sr, dict):
        line = (f"*Status:* healthy `{sr.get('healthy',0)}` • "
                f"degraded `{sr.get('degraded',0)}` • "
                f"error `{sr.get('error',0)}` • "
                f"unknown `{sr.get('unknown',0)}`")
        blocks.append(_mk_section(line))

    # device cards (top)
    dev_cards = llm_obj.get("device_cards") or []
    if dev_cards:
        for dc in dev_cards[:5]:
            host = dc.get("host","?")
            status = dc.get("status","unknown")
            lines = [str(x) for x in (dc.get("lines") or [])][:4]
            text = f"*Device:* `{host}` • *Status:* *{status}*"
            if lines:
                text += "\n" + "\n".join(lines)
            blocks.append(_mk_section(text))
    else:
        blocks.append(_mk_section("_No per-device analysis available._"))

    blocks.append(_mk_divider())

    # cross section
    cs = llm_obj.get("cross_section") or {}
    net_status = cs.get("network_status")
    if net_status:
        blocks.append(_mk_section(f"*Network status:* {net_status}"))

    incs = cs.get("incidents") or []
    if incs:
        blocks.append(_mk_section("*Top incidents:*\n" + "\n".join([str(x) for x in incs[:6]])))
    else:
        blocks.append(_mk_section("_No cross-device incidents detected._"))

    themes = cs.get("themes") or []
    if themes:
        blocks.append(_mk_section("*Remediation themes:*\n" + "\n".join([f"• {t}" for t in themes[:8]])))

    fu = cs.get("followups") or {}
    t_trust = fu.get("trusted") or []
    t_unval = fu.get("unvalidated") or []
    probes  = fu.get("probes") or []

    if t_trust or t_unval or probes:
        if t_trust:
            blocks.append(_mk_section("*Trusted follow-ups:*\n" + "\n".join([f"• `{c}`" for c in t_trust[:10]])))
        if t_unval:
            blocks.append(_mk_section("*Unvalidated ideas:*\n" + "\n".join([f"• `{c}`" for c in t_unval[:10]])))
        if probes:
            blocks.append(_mk_section("*Optional probes:*\n" + "\n".join([f"• `{c}`" for c in probes[:6]])))

    # Optional action button to attach raw artifacts
    if include_attach_button:
        payload = json.dumps({"config_dir": config_dir, "task_dir": task_dir})
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Attach artifacts"},
                    "action_id": ATTACH_BTN_ACTION_ID,
                    "value": payload
                }
            ]
        })

    return blocks