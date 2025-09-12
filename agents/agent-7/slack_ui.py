# agents/agent-7/slack_ui.py
from __future__ import annotations
import json
from typing import Any, Dict, List, Tuple

# ---- Limits to keep Slack modal size sane ----
MAX_HOSTS_IN_MODAL = 8
MAX_CMDS_PER_HOST  = 12

# ---- Block/action ids (stable so the orchestrator can read submissions) ----
HOSTS_MULTI_ID         = ("hosts_block", "hosts_select")
INCLUDE_SHOW_RUN_ID    = ("opts_block", "include_show_run")
ATTACH_BTN_ACTION_ID   = "agent7_attach_artifacts"  # orchestrator listens for this

# Per-host command picks are dynamic: block_id = f"cmds_{host}", action_id = "trusted_cmds"/"unval_cmds"

def _per_device_status_counts(rows):
    c = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
    for r in rows or []:
        s = (r.get("status") or "unknown").lower()
        c[s] = c.get(s, 0) + 1
    return c

def _mk_section(text: str) -> Dict[str, Any]:
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

def _mk_divider() -> Dict[str, Any]:
    return {"type": "divider"}

def _mk_code_block(label: str, content: str, limit: int = 1400) -> Dict[str, Any]:
    txt = content if len(content) <= limit else (content[:limit] + "\n…")
    return _mk_section(f"*{label}:*\n```{txt}```")

# Helper for slack UI display
def _per_device_status_counts(rows: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
    for r in rows or []:
        s = str(r.get("status", "unknown")).lower()
        if s not in counts:
            s = "unknown"
        counts[s] += 1
    return counts

# ------------------------------------------------------------------------------------
# Overview message blocks (feed to your orchestrator to post)
# ------------------------------------------------------------------------------------
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

    blocks: List[Dict[str, Any]] = []
    blocks.append(_mk_section(f"*Agent-7 Overview*\n*Config:* `{config_dir}` • *Task:* `{task_dir}`"))

    # (1) Network summary (if present)
    net_sum = (cross.get("network_summary") or "").strip()
    if net_sum:
        blocks.append(_mk_section(f"*Summary:* {net_sum}"))

    # (2) Status rollup: prefer cross.status_rollup; else derive
    roll = cross.get("status_rollup") if isinstance(cross, dict) else None
    need_derive = (
        not isinstance(roll, dict)
        or not roll
        or not all(k in roll for k in ("healthy", "degraded", "error", "unknown"))
    )
    if need_derive:
        cnt = {"healthy": 0, "degraded": 0, "error": 0, "unknown": 0}
        for row in per_device:
            s = (row.get("status") or "unknown").lower()
            cnt[s] = cnt.get(s, 0) + 1
        roll = cnt
    blocks.append(_mk_section(
        f"*Status rollup:* healthy `{roll.get('healthy',0)}` • "
        f"degraded `{roll.get('degraded',0)}` • error `{roll.get('error',0)}` • "
        f"unknown `{roll.get('unknown',0)}`"
    ))

    # Visual separator after rollup
    blocks.append(_mk_divider())

    # (3) Notable devices (from cross)
    notable = cross.get("notable_devices") or []
    if isinstance(notable, list) and notable:
        lines = []
        for nd in notable[:5]:
            lines.append(f"• `{nd.get('host','?')}` — *{nd.get('status','unknown')}*: {nd.get('note','')}")
        blocks.append(_mk_section("*Notable devices:*\n" + "\n".join(lines)))
        blocks.append(_mk_divider())

    # (4) Per-device mini cards (ok/suspect; fallback to findings)
    if per_device:
        upto = min(len(per_device), 5)
        for i, row in enumerate(per_device[:upto]):
            host   = row.get("hostname", "?")
            status = row.get("status", "unknown")
            plat   = row.get("platform") or row.get("platform_hint") or "unknown"
            sigs   = ", ".join((row.get("signals_seen") or [])[:8]) or "—"

            ok_list       = row.get("ok") or []
            suspect_list  = row.get("suspect") or []
            findings      = row.get("findings") or []
            status_reason = (row.get("status_reason") or "").strip()

            lines: List[str] = []
            for o in ok_list[:2]:
                lines.append(f"• ✅ {o.get('summary','')}")
            for s in suspect_list[:2]:
                lines.append(f"• ⚠️ {s.get('summary','')}")
            if not lines and findings:
                for f in findings[:2]:
                    sev  = f.get("severity", "info")
                    sig  = f.get("signal", "meta")
                    summ = f.get("summary", "")
                    lines.append(f"• [{sev}] *{sig}* — {summ}")

            # Show Reason only if non-healthy OR nothing else to show
            show_reason = status_reason and (status.lower() != "healthy" or not lines)
            if show_reason:
                lines.append(f"_Reason:_ {status_reason}")
            if not lines:
                lines.append("_No key notes._")

            text = (
                f"*Device:* `{host}`  •  *Platform:* `{plat}`  •  *Status:* *{status}*\n"
                f"*Signals:* {sigs}\n" + "\n".join(lines)
            )
            blocks.append(_mk_section(text))

            # divider between device cards (not after the last one)
            if i < upto - 1:
                blocks.append(_mk_divider())
    else:
        blocks.append(_mk_section("_No per-device analysis available._"))

    blocks.append(_mk_divider())

    # (5) Cross-device summary
    task_status = cross.get("task_status", "unknown")
    blocks.append(_mk_section(f"*Network status:* *{task_status}*"))

    incidents = cross.get("top_incidents") or []
    if incidents:
        lines = []
        for inc in incidents[:6]:
            scope   = inc.get("scope", "scope")
            summary = inc.get("summary", "")
            devs    = ", ".join((inc.get("devices") or [])[:6])
            lines.append(f"• *[{scope}]* {summary} — _{devs}_")
        blocks.append(_mk_section("*Top incidents:*\n" + "\n".join(lines)))
    else:
        blocks.append(_mk_section("_No cross-device incidents detected._"))

    themes = cross.get("remediation_themes") or []
    if themes:
        blocks.append(_mk_section("*Remediation themes:*\n" + "\n".join([f"• {t}" for t in themes[:8]])))

    t_trust = cross.get("trusted_followup_cmds") or []
    t_unval = cross.get("unvalidated_followup_cmds") or []
    probes  = cross.get("optional_active_probes") or []
    if t_trust or t_unval or probes:
        if t_trust:
            blocks.append(_mk_section("*Trusted follow-ups:*\n" + "\n".join([f"• `{c}`" for c in t_trust[:10]])))
        if t_unval:
            blocks.append(_mk_section("*Unvalidated ideas:*\n" + "\n".join([f"• `{c}`" for c in t_unval[:10]])))
        if probes:
            blocks.append(_mk_section("*Optional probes:*\n" + "\n".join([f"• `{c}`" for c in probes[:6]])))

    # (6) Optional action
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
# ------------------------------------------------------------------------------------
# “Run selected” modal (multi-host, per-host trusted/unvalidated command picks)
# ------------------------------------------------------------------------------------
def _opt(text: str, value: str) -> Dict[str, Any]:
    return {"text": {"type": "plain_text", "text": text, "emoji": True}, "value": value}

def _host_options(per_device: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out, seen = [], set()
    for row in per_device:
        h = (row.get("hostname") or "").strip()
        if h and h not in seen:
            seen.add(h)
            out.append(_opt(h, h))
        if len(out) >= MAX_HOSTS_IN_MODAL:
            break
    return out

def _commands_for_host(row: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """
    Map to our agreed per-device schema:
      trusted     <- recommended_show_cmds   (fallback: trusted_commands)
      unvalidated <- optional_active_cmds    (fallback: unvalidated_cmds)
    """
    trusted = (row.get("recommended_show_cmds") or row.get("trusted_commands") or [])[:MAX_CMDS_PER_HOST]
    unval   = (row.get("optional_active_cmds") or row.get("unvalidated_cmds") or [])[:MAX_CMDS_PER_HOST]
    return trusted, unval

def build_run_selected_modal_from_per_device(
    per_device: List[Dict[str, Any]],
    title: str = "Agent-7: Run selected",
    submit_text: str = "Run",
) -> Dict[str, Any]:
    host_opts = _host_options(per_device)

    blocks: List[Dict[str, Any]] = []
    blocks.append(_mk_section("Select hosts and the commands you want to capture now. "
                              "_Trusted_ are safe/known; _Unvalidated_ are ideas (review before running)."))

    # Hosts multi-select
    blocks.append({
        "type": "input",
        "block_id": HOSTS_MULTI_ID[0],
        "label": {"type": "plain_text", "text": "Hosts", "emoji": True},
        "element": {
            "type": "multi_static_select",
            "action_id": HOSTS_MULTI_ID[1],
            "placeholder": {"type": "plain_text", "text": "Pick up to 8 hosts"},
            "options": host_opts
        },
        "optional": False
    })

    # Global options
    blocks.append({
        "type": "section",
        "block_id": INCLUDE_SHOW_RUN_ID[0],
        "text": {"type": "mrkdwn", "text": "*Options*"},
        "accessory": {
            "type": "checkboxes",
            "action_id": INCLUDE_SHOW_RUN_ID[1],
            "options": [
                {
                    "text": {"type": "plain_text", "text": "Include 'show running-config'"},
                    "value": "include_show_run"
                }
            ]
        }
    })

    # Per-host trusted/unvalidated selectors (limited to MAX_HOSTS_IN_MODAL)
    for row in per_device[:MAX_HOSTS_IN_MODAL]:
        host = (row.get("hostname") or "").strip()
        if not host:
            continue
        trusted, unval = _commands_for_host(row)
        if not (trusted or unval):
            continue

        if trusted:
            blocks.append({
                "type": "input",
                "block_id": f"cmds_{host}__trusted",
                "label": {"type": "plain_text", "text": f"{host} — Trusted commands", "emoji": True},
                "optional": True,
                "element": {
                    "type": "multi_static_select",
                    "action_id": "trusted_cmds",
                    "placeholder": {"type": "plain_text", "text": "Select trusted commands"},
                    "options": [_opt(c, c) for c in trusted]
                }
            })
        if unval:
            blocks.append({
                "type": "input",
                "block_id": f"cmds_{host}__unval",
                "label": {"type": "plain_text", "text": f"{host} — Unvalidated commands", "emoji": True},
                "optional": True,
                "element": {
                    "type": "multi_static_select",
                    "action_id": "unval_cmds",
                    "placeholder": {"type": "plain_text", "text": "Select unvalidated commands"},
                    "options": [_opt(c, c) for c in unval]
                }
            })

    modal = {
        "type": "modal",
        "title": {"type": "plain_text", "text": title},
        "submit": {"type": "plain_text", "text": submit_text},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": blocks,
        "callback_id": "agent7_run_selected_modal"
    }
    return modal

# ------------------------------------------------------------------------------------
# Parse modal submission → normalized selection for capture_wrapper/command_plan_builder
# ------------------------------------------------------------------------------------
def _read_selected_host_ids(view_state: Dict[str, Any]) -> List[str]:
    try:
        blk = view_state["values"][HOSTS_MULTI_ID[0]][HOSTS_MULTI_ID[1]]
        return [o["value"] for o in blk.get("selected_options") or []]
    except Exception:
        return []

def _read_include_show_run(view_state: Dict[str, Any]) -> bool:
    try:
        blk = view_state["values"][INCLUDE_SHOW_RUN_ID[0]][INCLUDE_SHOW_RUN_ID[1]]
        sel = blk.get("selected_options") or []
        return any(o.get("value") == "include_show_run" for o in sel)
    except Exception:
        return False

def _read_per_host_cmds(view_state: Dict[str, Any]) -> Dict[str, Dict[str, List[str]]]:
    out: Dict[str, Dict[str, List[str]]] = {}
    try:
        for block_id, sub in (view_state.get("values") or {}).items():
            if not isinstance(block_id, str):
                continue
            if block_id.startswith("cmds_") and ("__trusted" in block_id or "__unval" in block_id):
                _, rest = block_id.split("cmds_", 1)
                host, kind = rest.split("__", 1)
                action = "trusted_cmds" if kind == "trusted" else "unval_cmds"
                sel = sub.get(action, {}).get("selected_options") or []
                cmds = [o.get("value") for o in sel if o.get("value")]
                d = out.setdefault(host, {"trusted": [], "unvalidated": []})
                if kind == "trusted":
                    d["trusted"].extend(cmds)
                else:
                    d["unvalidated"].extend(cmds)
    except Exception:
        pass
    return out

def parse_run_selected_submission(view_payload: Dict[str, Any]) -> Dict[str, Any]:
    view = (view_payload or {}).get("view") or {}
    state = view.get("state") or {}
    hosts = _read_selected_host_ids(state)
    include_show_run = _read_include_show_run(state)
    per_host_cmds = _read_per_host_cmds(state)
    return {
        "hosts": hosts,
        "include_show_run": include_show_run,
        "per_host_cmds": per_host_cmds
    }

# ------------------------------------------------------------------------------------
# Capture result blocks (brief success/fail summary)
# ------------------------------------------------------------------------------------
def build_capture_result_blocks(
    task_dir: str,
    results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    blocks.append(_mk_section(f"*Agent-7 capture completed* — Task `{task_dir}`"))

    # Shape A: new summary with harvest
    harvest = results.get("harvest") if isinstance(results, dict) else None
    if isinstance(harvest, dict) and ("copied" in harvest or "missing" in harvest):
        copied = harvest.get("copied") or []
        missing = harvest.get("missing") or []
        if copied:
            blocks.append(_mk_section("*Copied show logs:* " + ", ".join([f"`{h}`" for h in copied[:20]])))
        if missing:
            lines = [f"• `{h}` — no show log found" for h in missing[:20]]
            blocks.append(_mk_section("*Missing:* \n" + "\n".join(lines)))
        return blocks

    # Shape B: legacy per-host map
    hosts = (results.get("hosts") or {})
    if isinstance(hosts, dict):
        oks, fails = [], []
        for h, r in hosts.items():
            (oks if r.get("ok") else fails).append(h)
        if oks:
            blocks.append(_mk_section("*Success:* " + ", ".join([f"`{h}`" for h in oks[:20]])))
        if fails:
            lines = [f"• `{h}` — {hosts[h].get('error','error')}" for h in fails[:20]]
            blocks.append(_mk_section("*Failed:*\n" + "\n".join(lines)))

    return blocks