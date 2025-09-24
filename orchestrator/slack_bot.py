# orchestrator/slack_bot.py
import os, json, importlib.util, re
from typing import Dict, Optional, List
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from agent2_client import run_deploy              # Agent-2 (/deploy)
from agent3_client import run_analyze_host        # Agent-3 (/analyze-host)
from agent4_client import run_operational_check   # Agent-4 (/operational-check)
from agent5_client import run_operational_analyze # Agent-5 (/operational-analyze)
from agent7_client import (
    run_plan as run_a7_plan,
    run_capture as run_a7_capture,
    run_analyze as run_a7_analyze,
    run_analyze_host as run_a7_analyze_host,   # NEW
)

# --- New: minimal HTTP helper (no external client file) ---
import requests

# --- agent-8 triage (analyze 1 command)
from agent8_client import analyze_command

# shared/helpers.py
from shared.helpers import extract_cmd_output   

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
BOT_NAME = os.getenv("ORCHESTRATOR_BOT_NAME", "agent")

# Where the repo data lives (to locate artifacts to attach)
REPO_ROOT = os.getenv("REPO_ROOT", "/app/doo")

# Agent-7 Slack UI helper (file path)
A7_SLACK_UI_PATH = os.getenv("A7_SLACK_UI_PATH", "/app/agents/agent-7/slack_ui.py")

# New: Agent-8 base URL
AGENT_8_URL = os.getenv("AGENT_8_URL", "http://agent-8:8008")

app = App(token=SLACK_BOT_TOKEN)

print(f"[DEBUG] slack_bot.py: A7_SLACK_UI_PATH={A7_SLACK_UI_PATH} REPO_ROOT={REPO_ROOT} AGENT_8_URL={AGENT_8_URL}", flush=True)

# --- Simple per-thread memory of the last picked triage host ---
_SELECTED_TRIAGE_HOST: Dict[str, str] = {}  # key = thread_ts, value = host

# NEW: remember Agent-8 session per thread
_A8_SESSION_BY_THREAD: Dict[str, str] = {}  # key = thread_ts, value = session_id

_A8_SESSION_LAST_BY_CHANNEL: Dict[str, str] = {}  # NEW: fallback when thread mapping isn’t available
# Remember config/task/host for this thread so we can watch for output and auto-analyze
_A8_CTX_BY_THREAD: Dict[str, Dict[str, str]] = {}

_A8_CTX_BY_SESSION: Dict[str, Dict[str, str]] = {}   # key = session_id, value = {config_dir, task_id, host, thread_ts, channel}

# --- Core watch-and-analyze flow ---
def _watch_and_analyze(say, pchan: str, pthr: str,
                       session_id: str, hst: str,
                       commands: List[str], chosen: str):
    """
    After run_shows has dispatched commands, wait for the .md log file,
    then call Agent-8 /triage/analyze_command for each command and format results into Slack.
    """
    try:
        import os, time

        # 1) Get config/task from the orchestrator's own session context
        ctx = _A8_CTX_BY_SESSION.get(session_id, {})  # <- orchestrator-owned, not Agent-8
        cfg = ctx.get("config_dir")
        tsk = ctx.get("task_id")

        # Fallback: derive cfg/tsk from the INI path if context is missing
        if (not cfg or not tsk) and chosen:
            try:
                rel = os.path.relpath(chosen, REPO_ROOT)  # e.g. configs.5/task-18.bfd/agent7/1-plan/triage_...
                parts = rel.split(os.sep)
                if len(parts) >= 2:
                    cfg = cfg or parts[0]
                    tsk = tsk or parts[1]
            except Exception:
                pass

        if not cfg or not tsk:
            say(channel=pchan, thread_ts=pthr,
                text="⚠️ Cannot locate capture path for analysis (missing session context). "
                     "Please click *Start triage* again.")
            return

        # 2) Path where Agent-4 writes the show log
        md_path = os.path.join(
            REPO_ROOT, cfg, tsk, "agent7", "2-capture", "show_logs", f"{hst}.md"
        )

        # 3) Wait (poll) up to 90s for the .md to appear
        waited = 0
        while not os.path.isfile(md_path) and waited < 90:
            time.sleep(2)
            waited += 2

        if not os.path.isfile(md_path):
            say(channel=pchan, thread_ts=pthr,
                text=f"⚠️ No show_log found for `{hst}` at:\n`{md_path}`")
            return

        # 4) Ask Agent-8 to analyze each command (Agent-8 reads the file locally)
        for cmd in commands:
            try:
                res = analyze_command(session_id=session_id, host=hst, command=cmd)

                # Raw fenced output (always first)
                # Use the same snippet extraction as _post_show_snippets but inline
                import re
                body = _read_text(md_path)
                preview = extract_cmd_output(body, cmd)
                # preview = ""
                # if body:
                #     pat = rf"(?mis)^##\s*{re.escape(cmd)}\s*\n+```(.*?)```"
                #     m = re.search(pat, body)
                #     if m:
                #         preview = m.group(1).strip()
                #     else:
                #         blocks = re.findall(r"(?s)```(.*?)```", body)
                #         if blocks:
                #             preview = blocks[-1].strip()
                if not preview:
                    preview = f"(no captured output for `{cmd}` in log)"

                # Analyses
                analysis1 = res.get("analysis_pass1") or "(no analysis)"
                analysis2 = res.get("analysis_pass2") or None   # Optional

                direction = res.get("direction") or ""
                trusted = res.get("trusted_commands") or []
                unvalidated = res.get("unvalidated_commands") or []

                # Build Slack text
                out = []
                out.append(f"*📄 Output for `{cmd}` on `{hst}`:*\n```{preview}```")
                out.append(f"*🟢 Pass-1 (single-step):*\n{analysis1}")
                # comment this block to disable Pass-2 entirely
                if analysis2:   
                    out.append(f"*🔵 Pass-2 (with history):*\n{analysis2}")
                    # # comment above block to disable Pass-2 entirely
                if direction:
                    out.append(f"*Direction:* {direction}")
                if trusted:
                    out.append(f"*Trusted commands:* " + ", ".join(f"`{c}`" for c in trusted))
                if unvalidated:
                    out.append(f"*Unvalidated commands:* " + ", ".join(f"`{c}`" for c in unvalidated))

                say(channel=pchan, thread_ts=pthr, text="\n\n".join(out))

            except Exception as e:
                say(channel=pchan, thread_ts=pthr,
                    text=f"⚠️ Analysis failed for `{cmd}`: `{e}`")

    except Exception as e:
        say(channel=pchan, thread_ts=pthr, text=f"⚠️ Analysis failed: `{e}`")
    
                
def _post_json(url: str, payload: dict, timeout: int = 30) -> dict:
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"ok": True, "raw": r.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# -------- small helpers --------
def _help_text() -> str:
    return (
        f"Commands:\n"
        f"• Deploy configs — Agent-2:\n   `@{BOT_NAME} deploy <config_dir> <task>`\n"
        f"• Analyze a single host — Agent-3:\n   `@{BOT_NAME} analyze-host <config_dir> <task> <hostname>`\n"
        f"• NetOps capture — Agent-4:\n   `@{BOT_NAME} operational-check <config_dir> <task>`\n"
        f"• NetOps analysis — Agent-5:\n   `@{BOT_NAME} operational-analyze <config_dir> <task>`\n"
        f"• Agent-7 PLAN (AI-built command plan):\n   `@{BOT_NAME} a7-plan <config_dir> <task> [host1,host2,...]`\n"
        f"• Agent-7 CAPTURE (run plan via Agent-4):\n   `@{BOT_NAME} a7-capture <config_dir> <task> [host1,host2,...]`\n"
        f"• Agent-7 ANALYZE (md→parsed→facts→per-device→cross):\n   `@{BOT_NAME} a7-analyze <config_dir> <task>`\n"
        f"• Agent-7 END-TO-END (plan→capture→analyze):\n   `@{BOT_NAME} a7-run <config_dir> <task> [host1,host2,...]`\n"
        f"• `@{BOT_NAME} help`\n"
    )

def _read_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def _post_show_snippets(say, channel: str, thread_ts: str, md_path: str, commands: list[str], host: str):
    """
    Reads the host's show_log markdown and posts only the sections matching the commands.
    If no sections match (e.g., error file), post a concise raw/error preview instead.
    Sections in show logs are formatted as '## <command>' ... fenced block.
    """
    import re
    body = _read_text(md_path)
    if not body:
        try:
            say(channel=channel, thread_ts=thread_ts,
                text=f"⚠️ Could not read captured log for `{host}` at `{md_path}`.")
        except Exception:
            pass
        return

    # Try to collect matching command snippets
    snippets = []
    for cmd in commands or []:
        # Match header '## <cmd>' then the FIRST fenced code block under it.
        pat = rf"(?mis)^##\s*{re.escape(cmd)}\s*\n+```(.*?)```"
        m = re.search(pat, body)
        if not m:
            # Fallback: header up to next header (no fenced block)
            pat2 = rf"(?mis)^##\s*{re.escape(cmd)}\s*\n(.*?)(?=^##\s|\Z)"
            m = re.search(pat2, body)
        if m:
            raw = m.group(1).strip() if m.groups() else m.group(0).strip()
            preview = raw if len(raw) <= 1800 else (raw[:1750] + "\n…(truncated)…")
            snippets.append((cmd, preview))

    if snippets:
        parts = [f"*📄 Output — {host}*"]
        for cmd, txt in snippets:
            parts.append(f"*{cmd}*\n```{txt}```")
        try:
            say(channel=channel, thread_ts=thread_ts, text="\n\n".join(parts))
        except Exception:
            pass
        return

    # ---- No matching sections: provide a useful fallback (error/first block/raw) ----
    # 1) If it's an error file, post the first fenced block as the device error details.
    if body.lstrip().startswith("# ERROR for"):
        m_err = re.search(r"(?s)```(.*?)```", body)
        err_txt = (m_err.group(1).strip() if m_err else body.strip())
        preview = err_txt if len(err_txt) <= 1800 else (err_txt[:1750] + "\n…(truncated)…")
        try:
            say(channel=channel, thread_ts=thread_ts,
                text=f"⚠️ *Capture error on `{host}`* — posting device error details:\n```{preview}```")
        except Exception:
            pass
        return

    # 2) Otherwise, post the first fenced block; if none, a short raw preview of the file.
    m_block = re.search(r"(?s)```(.*?)```", body)
    if m_block:
        blob = m_block.group(1).strip()
    else:
        blob = body.strip()
    preview = blob if len(blob) <= 1800 else (blob[:1750] + "\n…(truncated)…")
    try:
        say(channel=channel, thread_ts=thread_ts,
            text=f"*📄 Output — {host}*\n```{preview}```")
    except Exception:
        pass


def _post_a7_llm_overview_if_available(say, channel: str, thread_ts: str, slack_overview_path: str | None) -> bool:
    """
    If agent-7 produced agent7/3-analyze/slack_overview.json with Slack-ready blocks/text,
    post it and return True. Otherwise return False (caller will fallback).
    """
    if not slack_overview_path:
        print("[DEBUG] LLM overview: no path provided", flush=True)
        return False
    obj = _read_json(slack_overview_path)
    if not isinstance(obj, dict):
        print(f"[DEBUG] LLM overview: not a dict at {slack_overview_path}", flush=True)
        return False

    blocks = obj.get("blocks")
    if isinstance(blocks, list) and blocks:
        try:
            say(channel=channel, thread_ts=thread_ts, text="Agent-7 Analysis", blocks=blocks)
            print(f"[DEBUG] LLM overview: posted blocks from {slack_overview_path}", flush=True)
            return True
        except Exception as e:
            print(f"[DEBUG] LLM overview: posting blocks failed: {e}", flush=True)

    for key in ("text", "overview_text"):
        txt = obj.get(key)
        if isinstance(txt, str) and txt.strip():
            say(channel=channel, thread_ts=thread_ts, text=txt.strip())
            print(f"[DEBUG] LLM overview: posted text via '{key}'", flush=True)
            return True

    print("[DEBUG] LLM overview: no usable content", flush=True)
    return False

def _load_a7_slack_ui():
    """
    Dynamically import agents/agent-7/slack_ui.py even though the parent
    folder has a hyphen and isn't a valid package name.
    """
    try:
        print(f"[DEBUG] _load_a7_slack_ui: trying {A7_SLACK_UI_PATH}", flush=True)
        spec = importlib.util.spec_from_file_location("a7_slack_ui", A7_SLACK_UI_PATH)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore
            has_blocks = hasattr(mod, "build_overview_blocks")
            print(f"[DEBUG] _load_a7_slack_ui: loaded ok, build_overview_blocks={has_blocks}", flush=True)
            if not has_blocks:
                return None
            return mod
        print("[DEBUG] _load_a7_slack_ui: spec/loader missing", flush=True)
    except Exception as e:
        print(f"[DEBUG] _load_a7_slack_ui: import failed: {e}", flush=True)
    return None

def _post_a7_overview(say, channel: str, thread_ts: str, config_dir: str, task_id: str,
                      per_device_path: str | None, cross_device_path: str | None):
    print(f"[DEBUG] _post_a7_overview: per_device_path={per_device_path} cross_device_path={cross_device_path}", flush=True)

    ui = _load_a7_slack_ui()

    per_device = _read_json(per_device_path) if per_device_path else None
    cross = _read_json(cross_device_path) if cross_device_path else None

    ## ------------------------
    ##  agent-8 fix attempt
    is_scoped = per_device_path and 'scoped' in per_device_path

    if is_scoped:
        print("[DEBUG] Scoped mode detected — suppressing cross-device analysis")
        cross = {}  # Clear stale cross-device summary if present
    #------------------------##
    try:
        pd_count = len(per_device) if isinstance(per_device, list) else "n/a"
        cross_keys = list(cross.keys()) if isinstance(cross, dict) else []
        print(f"[DEBUG] _post_a7_overview: per_device_rows={pd_count} cross_keys={cross_keys}", flush=True)
    except Exception:
        print("[DEBUG] _post_a7_overview: debug-counts failed", flush=True)

    # Fallback if UI missing
    if not ui:
        status = (cross or {}).get("task_status", "unknown") if isinstance(cross, dict) else "unknown"
        hosts = len(per_device or []) if isinstance(per_device, list) else 0
        say(
            channel=channel,
            thread_ts=thread_ts,
            text=(f"*Agent-7 Overview*\n"
                  f"Config: `{config_dir}` • Task: `{task_id}` • Status: *{status}*\n"
                  f"(Install slack_ui.py or set A7_SLACK_UI_PATH to enable rich blocks)")
        )
        print("[DEBUG] _post_a7_overview: posted fallback (no UI)", flush=True)
        return

    # Try to build blocks
    try:
        blocks = ui.build_overview_blocks(
            config_dir=config_dir,
            task_dir=task_id,
            cross=cross if isinstance(cross, dict) else {},
            per_device=per_device if isinstance(per_device, list) else [],
            include_attach_button=True,
            include_triage_button=True,      # <<< NEW: show Start triage + host picker
            triage_picker_limit=8,           # <<< NEW: optional cap
        )
        # last-resort sanity
        if not isinstance(blocks, list) or not blocks:
            raise RuntimeError("build_overview_blocks returned empty/invalid")
        # Post with blocks
        try:
            say(channel=channel, thread_ts=thread_ts, text="Agent-7 Analysis", blocks=blocks)
            print("[DEBUG] _post_a7_overview: posted rich blocks ok", flush=True)
        except Exception as e:
            print(f"[DEBUG] _post_a7_overview: say(blocks=...) failed: {e}", flush=True)
            # safe degrade to text
            status = (cross or {}).get("task_status", "unknown") if isinstance(cross, dict) else "unknown"
            hosts = len(per_device or []) if isinstance(per_device, list) else 0
            say(channel=channel, thread_ts=thread_ts,
                text=(f"*Agent-7 Overview*\n"
                      f"Config: `{config_dir}` • Task: `{task_id}` • Status: *{status}* • Per-device rows: {hosts}\n"
                      f"(blocks post failed)"))
    except Exception as e:
        print(f"[DEBUG] _post_a7_overview: build blocks failed: {e}", flush=True)
        # One more fallback
        status = (cross or {}).get("task_status", "unknown") if isinstance(cross, dict) else "unknown"
        hosts = len(per_device or []) if isinstance(per_device, list) else 0
        say(channel=channel, thread_ts=thread_ts,
            text=(f"*Agent-7 Overview*\n"
                  f"Config: `{config_dir}` • Task: `{task_id}` • Status: *{status}* • Per-device rows: {hosts}\n"
                  f"(UI build failed: {e})"))

# -------- Slack events --------
@app.event("app_mention")
def handle_app_mention(body, say, logger):
    ev = body.get("event", {})
    text = (ev.get("text") or "").strip()
    channel = ev.get("channel")
    thread_ts = ev.get("thread_ts") or ev.get("ts")
    user = ev.get("user")

    parts = text.split(maxsplit=2)
    if len(parts) < 2:
        say(channel=channel, thread_ts=thread_ts, text=_help_text())
        return

    cmd = parts[1].lower()

    # Aliases
    if cmd in ("a3", "analyse-host", "host"):
        cmd = "analyze-host"
    if cmd in ("a4", "ops-capture", "ops-check", "operational-capture"):
        cmd = "operational-check"
    if cmd in ("a5", "ops-analyze", "operational-analyze", "ops-analysis"):
        cmd = "operational-analyze"
    if cmd in ("a7", "agent7", "ops7", "ops"):
        cmd = "a7-run"

    print(f"[DEBUG] app_mention parsed cmd={cmd} raw_text={text}", flush=True)

    # --- NEW: Agent-8 free-text triage ---
    if cmd == "triage" and len(parts) == 3:
        user_text = parts[2]

        # Prefer the most-recent channel session; if the thread has an older one, override it.
        sess_thread = _A8_SESSION_BY_THREAD.get(thread_ts) if thread_ts else None
        sess_chan   = _A8_SESSION_LAST_BY_CHANNEL.get(channel) if channel else None

        session_id = None
        if sess_chan:  # newest for the channel wins
            session_id = sess_chan
            if thread_ts:
                _A8_SESSION_BY_THREAD[thread_ts] = sess_chan  # refresh thread mapping to latest
        elif sess_thread:
            session_id = sess_thread
        else:
            say(channel=channel, thread_ts=thread_ts,
                text="⚠️ No active triage session here. Click *Start triage* first.")
            return

        print(f"[DEBUG] triage using session={session_id} "
            f"sess_thread={sess_thread} sess_chan={sess_chan} "
            f"thread={thread_ts} channel={channel}", flush=True)

        # # Prefer session bound to this thread; otherwise fall back to channel's last session
        # session_id = None
        # if thread_ts and thread_ts in _A8_SESSION_BY_THREAD:
        #     session_id = _A8_SESSION_BY_THREAD[thread_ts]
        # elif channel and channel in _A8_SESSION_LAST_BY_CHANNEL:
        #     session_id = _A8_SESSION_LAST_BY_CHANNEL[channel]
        #     if thread_ts:
        #         _A8_SESSION_BY_THREAD[thread_ts] = session_id
        # else:
        #     say(channel=channel, thread_ts=thread_ts,
        #         text="⚠️ No active triage session here. Click *Start triage* first.")
        #     return

        print(f"[DEBUG] triage using session={session_id} thread={thread_ts} channel={channel}", flush=True)

        # ---- Mini parser: support "run ..." to dispatch immediately ----
        low = user_text.strip().lower()
        if low.startswith("run ") or low.startswith("run:"):
            # Commands can be separated by | ; or newline. If none, treat remainder as a single command.
            remainder = user_text.split(" ", 1)[1] if " " in user_text else ""
            raw_cmds = [remainder] if ("|" not in remainder and ";" not in remainder and "\n" not in remainder) \
                       else [c for c in re.split(r"[|;\n]", remainder) if c.strip()]
            commands = [c.strip() for c in raw_cmds if c.strip()]
            if not commands:
                say(channel=channel, thread_ts=thread_ts,
                    text="⚠️ No commands to run. Example: `@{BOT_NAME} triage run show ip bgp summary | show bgp neighbors`".format(BOT_NAME=BOT_NAME))
                return

            # Use the context that belongs to THIS session (original thread/channel/host)
            ctx = _A8_CTX_BY_SESSION.get(session_id, {})
            post_thread  = ctx.get("thread_ts") or thread_ts
            post_channel = ctx.get("channel")  or channel
            cfg = ctx.get("config_dir", "")
            tsk = ctx.get("task_id", "")
            host_hint = ctx.get("host") or _SELECTED_TRIAGE_HOST.get(post_thread or "", "selected host")

            # NEW: capture the moment we dispatch, to detect fresh file writes
            import time as _time
            dispatch_ts = _time.time()

            run_url = f"{AGENT_8_URL}/triage/run_shows"
            payload = {"session_id": session_id, "host": host_hint, "commands": commands}
            resp = _post_json(run_url, payload, timeout=90)

            if not resp or resp.get("ok") is False:
                say(channel=post_channel, thread_ts=post_thread,
                    text=f"❌ Dispatch failed: `{resp.get('error','unknown')}`")
                return

            ini_path = resp.get("plan_ini_path", "(unknown)")
            dispatched = resp.get("dispatched", False)

            # Confirm dispatch + tell user we’ll bring results back and analyze
            say(
                channel=post_channel,
                thread_ts=post_thread,
                text=(
                    f"📤 Dispatched {len(commands)} command(s) on `{host_hint}`.\n"
                    f"• Plan INI: `{ini_path}`\n"
                    f"• Capture: *{'queued with Agent-4' if dispatched else 'saved (not dispatched)'}*\n\n"
                    "I’ll post the command output here when it lands, then analyze it."
                )
            )

            # # FIX: launch watcher thread with proper args
            # import threading
            # threading.Thread(
            #     target=_watch_and_analyze,
            #     args=(say, post_channel, post_thread, session_id, host_hint, commands, ini_path),
            #     daemon=True
            # ).start()
            return
            
        # ---- Default path: send free-text to Agent-8 /triage/ingest ----
        ingest_url = f"{AGENT_8_URL}/triage/ingest"
        payload = {"session_id": session_id, "user_text": user_text}
        resp = _post_json(ingest_url, payload, timeout=60)

        if not resp or resp.get("ok") is False:
            err = (resp or {}).get("error", "unknown")
            hint = ""
            # If Agent-8 was restarted, in-memory sessions are gone; 404 is expected.
            if "404" in str(err) or "Not Found" in str(err):
                hint = " (session likely expired—click *Start triage* again in this thread)"
            say(channel=channel, thread_ts=thread_ts,
                text=f"❌ Triage ingest failed: `{err}`{hint}")
            return

        guidance = (resp.get("guidance_text") or "").strip()
        cmds = resp.get("proposed_commands") or []
        lines = []
        for c in cmds[:12]:
            cmd_txt = c.get("command", "")
            src = c.get("source", "llm")
            trust = c.get("trust_hint", "low")
            if cmd_txt:
                lines.append(f"• `{cmd_txt}`  _(src: {src}, trust: {trust})_")

        hint = f"_To run now:_ `@{BOT_NAME} triage run <cmd1> | <cmd2>`"
        out = []
        if guidance:
            out.append(f"*Guidance:*\n{guidance}")
        if lines:
            out.append("*Proposed commands:*\n" + "\n".join(lines))
        out.append(hint)

        say(channel=channel, thread_ts=thread_ts, text="\n\n".join(out))
        return

    if cmd == "help":
        say(channel=channel, thread_ts=thread_ts, text=_help_text())
        return

    # Agent-3
    if cmd == "analyze-host" and len(parts) == 3:
        args = parts[2].split()
        if len(args) != 3:
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} analyze-host <config_dir> <task_id> <hostname>`")
            return
        config_dir, task_id, hostname = args
        say(channel=channel, thread_ts=thread_ts,
            text=f"🔬 Routing to Agent-3: `{config_dir}` `{task_id}` host=`{hostname}` …")
        result = run_analyze_host(config_dir, task_id, hostname, channel, thread_ts, user)
        say(channel=channel, thread_ts=thread_ts, text=f"✅ Agent-3 request accepted.\n`{result}`")
        return

    # Agent-4
    if cmd == "operational-check" and len(parts) == 3:
        args = parts[2].split()
        if len(args) != 2:
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} operational-check <config_dir> <task_id>`")
            return
        config_dir, task_id = args
        say(channel=channel, thread_ts=thread_ts,
            text=f"📟 Routing to Agent-4: `{config_dir}` `{task_id}` …")
        result = run_operational_check(config_dir, task_id, channel, thread_ts, user)
        say(channel=channel, thread_ts=thread_ts, text=f"✅ Agent-4 request accepted.\n`{result}`")
        return

    # Agent-5
    if cmd == "operational-analyze" and len(parts) == 3:
        args = parts[2].split()
        if len(args) != 2:
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} ops-analyze <config_dir> <task_id>`")
            return
        config_dir, task_id = args
        say(channel=channel, thread_ts=thread_ts,
            text=f"🧠 Routing to Agent-5: `{config_dir}` `{task_id}` …")
        result = run_operational_analyze(config_dir, task_id, channel, thread_ts, user)
        say(channel=channel, thread_ts=thread_ts, text=f"✅ Agent-5 request accepted.\n`{result}`")
        return

    # Agent-7 PLAN
    if cmd == "a7-plan" and len(parts) == 3:
        args = parts[2].split()
        if len(args) not in (2, 3):
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} a7-plan <config_dir> <task_id> [host1,host2,...]`")
            return
        config_dir, task_id = args[0], args[1]
        hosts = args[2].split(",") if len(args) == 3 else None
        say(channel=channel, thread_ts=thread_ts,
            text=f"📝 Routing to Agent-7 /plan: `{config_dir}` `{task_id}` hosts=`{','.join(hosts) if hosts else '(auto)'}` …")
        res = run_a7_plan(config_dir, task_id, hosts=hosts)
        say(channel=channel, thread_ts=thread_ts,
            text=(f"✅ Plan ready.\n"
                  f"• INI: `{res.get('overlay_ini','')}`\n"
                  f"• Plan JSON: `{res.get('capture_plan','')}`\n"
                  f"• Hosts: `{', '.join(res.get('hosts') or [])}`"))
        return

    # Agent-7 CAPTURE
    if cmd == "a7-capture" and len(parts) == 3:
        args = parts[2].split()
        if len(args) not in (2, 3):
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} a7-capture <config_dir> <task_id> [host1,host2,...]`")
            return
        config_dir, task_id = args[0], args[1]
        hosts_override = args[2].split(",") if len(args) == 3 else None
        say(channel=channel, thread_ts=thread_ts,
            text=f"📟 Routing to Agent-7 /capture: `{config_dir}` `{task_id}` hosts_override=`{','.join(hosts_override) if hosts_override else '(plan)'}` …")
        res = run_a7_capture(config_dir, task_id, plan_path=None, hosts_override=hosts_override)
        say(channel=channel, thread_ts=thread_ts,
            text=f"✅ Capture summary: `{res.get('summary_path','')}`")
        return

    # Agent-7 ANALYZE
    if cmd == "a7-analyze" and len(parts) == 3:
        args = parts[2].split()
        if len(args) != 2:
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} a7-analyze <config_dir> <task_id>`")
            return
        config_dir, task_id = args
        say(channel=channel, thread_ts=thread_ts,
            text=f"🔎 Routing to Agent-7 /analyze: `{config_dir}` `{task_id}` …")
        
        try:
            res = run_a7_analyze(config_dir, task_id)
            print(f"[DEBUG] a7-analyze: run_a7_analyze returned keys={list((res or {}).keys())}", flush=True)

            # Post concise pointer (kept for continuity)
            say(channel=channel, thread_ts=thread_ts,
                text=(f"✅ Analyze summary: `{res.get('facts_summary_path','')}` • hosts={res.get('hosts_processed',0)}"))

            # 1) Prefer LLM-made slack_overview.json (blocks/text) if present
            if _post_a7_llm_overview_if_available(
                say, channel, thread_ts, res.get("slack_overview_path")
            ):
                return

            # 2) Fallback to local renderer → per_device + cross (with attach button + triage)
            _post_a7_overview(
                say=say,
                channel=channel,
                thread_ts=thread_ts,
                config_dir=config_dir,
                task_id=task_id,
                per_device_path=res.get("per_device_json_path"),
                cross_device_path=res.get("cross_device_json_path"),
            )
        except Exception as e:
            print(f"[DEBUG] a7-analyze: run_a7_analyze failed: {e}", flush=True)
            say(channel=channel, thread_ts=thread_ts,
                text=f"❌ Agent-7 analyze failed: `{e}`")

        return

    # Agent-7 END-TO-END
    if cmd == "a7-run" and len(parts) == 3:
        args = parts[2].split()
        if len(args) not in (2, 3):
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} a7-run <config_dir> <task_id> [host1,host2,...]`")
            return
        config_dir, task_id = args[0], args[1]
        hosts = args[2].split(",") if len(args) == 3 else None

        say(channel=channel, thread_ts=thread_ts,
            text=f"🚀 Agent-7 run starting: `{config_dir}` `{task_id}` • hosts=`{','.join(hosts) if hosts else '(auto)'}`")
        try:
            plan_res = run_a7_plan(config_dir, task_id, hosts=hosts)
            say(channel=channel, thread_ts=thread_ts,
                text=f"📝 Plan ok → INI=`{plan_res.get('overlay_ini','')}`")

            cap_res = run_a7_capture(config_dir, task_id, plan_path=None, hosts_override=hosts)
            say(channel=channel, thread_ts=thread_ts,
                text=f"📟 Capture ok → summary=`{cap_res.get('summary_path','')}`")

            ana_res = run_a7_analyze(config_dir, task_id)
            say(channel=channel, thread_ts=thread_ts,
                text=(f"🔎 Analyze ok → facts_summary=`{ana_res.get('facts_summary_path','')}` "
                      f"• hosts={ana_res.get('hosts_processed',0)}"))

            # Prefer prebuilt blocks; fallback if missing (with triage controls)
            if _post_a7_llm_overview_if_available(
                say, channel, thread_ts, ana_res.get("slack_overview_path")
            ):
                pass
            else:
                _post_a7_overview(
                    say=say,
                    channel=channel,
                    thread_ts=thread_ts,
                    config_dir=config_dir,
                    task_id=task_id,
                    per_device_path=ana_res.get("per_device_json_path"),
                    cross_device_path=ana_res.get("cross_device_json_path"),
                )

            say(channel=channel, thread_ts=thread_ts, text=f"✅ Agent-7 run COMPLETE.")
        except Exception as e:
            say(channel=channel, thread_ts=thread_ts, text=f"❌ Agent-7 run failed: `{e}`")
        return

    # Shorthand → Agent-2
    if len(parts) == 3 and cmd not in (
        "help", "deploy",
        "analyze-host", "analyse-host", "host", "a3",
        "operational-analyze", "ops-analyze", "ops-analysis", "a5",
    ):
        maybe_config = parts[1]
        maybe_task = parts[2].strip()
        args = maybe_task.split()
        if len(args) == 1:
            config_dir, task_id = maybe_config, args[0]
            say(channel=channel, thread_ts=thread_ts,
                text=f"**Routing** request to **Agent-2**: `{config_dir}` `{task_id}` …\n Hang tight! agent will update you shortly")
            result = run_deploy(config_dir, task_id, channel, thread_ts, user)
            return
        else:
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} deploy <config_dir> <task_id>`")
            return

    # Explicit Agent-2 deploy
    if cmd == "deploy" and len(parts) == 3:
        args = parts[2].split()
        if len(args) != 2:
            say(channel=channel, thread_ts=thread_ts,
                text=f"Usage: `@{BOT_NAME} deploy <config_dir> <task_id>`")
            return
        config_dir, task_id = args
        say(channel=channel, thread_ts=thread_ts,
            text=f"🧭 Routing to Agent-2: `{config_dir}` `{task_id}` …\n Hang tight! agent will update you shortly")
        result = run_deploy(config_dir, task_id, channel, thread_ts, user)
        return

    say(channel=channel, thread_ts=thread_ts, text=f"Unknown command `{cmd}`.\n{_help_text()}")


# -------- Button handler: “Attach artifacts” --------
@app.action("agent7_attach_artifacts")
def handle_attach_artifacts(ack, body, client, say, logger):
    """
    Uploads agent7/3-analyze/{per_device.json,cross_device.json,slack_overview.json} into the same thread.
    The button's value contains: {"config_dir":"...","task_dir":"..."}
    """
    ack()

    # Extract channel + thread
    channel = None
    thread_ts = None
    try:
        channel = body.get("container", {}).get("channel_id") or body.get("channel", {}).get("id")
        thread_ts = body.get("container", {}).get("message_ts") or body.get("message", {}).get("ts")
    except Exception:
        pass

    if not channel or not thread_ts:
        say(text="⚠️ Couldn't locate channel/thread to attach files.", thread_ts=None)
        return

    # Parse button payload (value)
    payload = {}
    try:
        val = (body.get("actions") or [{}])[0].get("value") or "{}"
        payload = json.loads(val)
    except Exception:
        pass

    config_dir = payload.get("config_dir", "")
    task_id    = payload.get("task_dir", "")
    base = os.path.join(REPO_ROOT, config_dir, task_id, "agent7", "3-analyze")
    per_path   = os.path.join(base, "per_device.json")
    cross_path = os.path.join(base, "cross_device.json")
    slack_overview_path = os.path.join(base, "slack_overview.json")

    uploaded_any = False
    for fp in (per_path, cross_path, slack_overview_path):
        try:
            if os.path.exists(fp):
                client.files_upload_v2(
                    channel=channel,
                    thread_ts=thread_ts,
                    file=fp,
                    filename=os.path.basename(fp),
                    title=os.path.basename(fp),
                    initial_comment=f"📎 {os.path.basename(fp)}"
                )
                uploaded_any = True
        except Exception as e:
            logger.error(f"files_upload_v2 failed for {fp}: {e}")
            # Fallback preview
            try:
                with open(fp, "r", encoding="utf-8") as fh:
                    content = fh.read()
                preview = content[:1800]
                say(
                    channel=channel,
                    thread_ts=thread_ts,
                    text=f"📎 _Upload failed for `{os.path.basename(fp)}` — preview:_\n```json\n{preview}\n```"
                )
                uploaded_any = True
            except Exception as e2:
                logger.error(f"fallback preview failed for {fp}: {e2}")

    if not uploaded_any:
        say(channel=channel, thread_ts=thread_ts,
            text=f"⚠️ Artifacts not found to attach for `{config_dir}` `{task_id}`.")

# -------- NEW: Triage host picker (static_select) --------
@app.action("agent8_host_select")
def handle_triage_host_select(ack, body, say, logger):
    """
    Remember the last selected host for this thread.
    """
    ack()
    try:
        # Find thread_ts
        thread_ts = body.get("container", {}).get("message_ts") or body.get("message", {}).get("ts")
        action = (body.get("actions") or [{}])[0]
        sel = action.get("selected_option") or {}
        host = sel.get("value") or sel.get("text", {}).get("text")
        if thread_ts and host and host != "__none__":
            _SELECTED_TRIAGE_HOST[thread_ts] = host
            print(f"[DEBUG] triage host selected: thread={thread_ts} host={host}", flush=True)
    except Exception as e:
        logger.error(f"agent8_host_select error: {e}")

# -------- NEW: Start triage button --------
@app.action("agent8_start_triage")
def handle_start_triage(ack, body, say, logger):
    """
    Start Agent-8 triage for the chosen host (or default).
    - Reads config_dir/task_dir from button value JSON.
    - Uses the last selected host in this thread, or falls back to the first option shown.
    - Calls Agent-8 /triage/start and stores session_id for this thread.
    """
    ack()

    # Channel/thread
    channel = body.get("container", {}).get("channel_id") or body.get("channel", {}).get("id")
    thread_ts = body.get("container", {}).get("message_ts") or body.get("message", {}).get("ts")

    # Parse button payload (value)
    payload = {}
    try:
        val = (body.get("actions") or [{}])[0].get("value") or "{}"
        payload = json.loads(val)
    except Exception:
        pass

    config_dir = payload.get("config_dir", "")
    task_id    = payload.get("task_dir", "")

    # Determine host: prefer remembered selection in this thread
    host: Optional[str] = _SELECTED_TRIAGE_HOST.get(thread_ts)

    # Fallback: derive first option from the message blocks (if present)
    if not host:
        try:
            blocks = (body.get("message") or {}).get("blocks") or []
            for blk in blocks:
                if blk.get("type") == "actions":
                    for el in blk.get("elements", []):
                        if el.get("type") == "static_select" and el.get("action_id") == "agent8_host_select":
                            opts = el.get("options") or []
                            if opts:
                                host = opts[0].get("value") or opts[0].get("text", {}).get("text")
                                break
                if host:
                    break
        except Exception:
            pass

    if not host or host == "__none__":
        say(channel=channel, thread_ts=thread_ts, text="⚠️ No host selected for triage.")
        return

    # Call Agent-8
    start_payload = {
        "config_dir": config_dir,
        "task_dir": task_id,
        "host": host,              # send single host (Agent-8 also accepts hosts[0])
        "thread_ts": thread_ts,
        "channel": channel
    }
    url = f"{AGENT_8_URL}/triage/start"
    res = _post_json(url, start_payload, timeout=60)
    print(f"[DEBUG] agent8_start_triage response: {res}", flush=True)

    sess = res.get("session_id")
    if not isinstance(sess, str) or not sess:
        # Do NOT proceed silently; tell the user and stop.
        err = res.get("error") or res.get("raw") or "no session_id returned"
        say(channel=channel, thread_ts=thread_ts,
            text=f"❌ Triage start failed for `{host}`: `{err}`")
        return

    # Remember session for this Slack thread (primary) and channel (fallback)
    if thread_ts:
        _A8_SESSION_BY_THREAD[thread_ts] = sess
    if channel:
        _A8_SESSION_LAST_BY_CHANNEL[channel] = sess  # NEW: channel-level fallback
    print(f"[DEBUG] stored triage session: thread={thread_ts} channel={channel} session={sess}", flush=True)

    # Save context for this thread (used by run-path watcher)
    if thread_ts:
        _A8_CTX_BY_THREAD[thread_ts] = {
            "config_dir": config_dir,
            "task_id": task_id,
            "host": host,
        }
    # ALSO save by session (so later messages can find the original thread/channel)
    _A8_CTX_BY_SESSION[sess] = {
        "config_dir": config_dir,
        "task_id": task_id,
        "host": host,
        "thread_ts": thread_ts or "",
        "channel": channel or "",
    }

    say(channel=channel, thread_ts=thread_ts,
        text=f"🧭 Starting triage on `{host}` (config `{config_dir}`, task `{task_id}`)…\n"
             f"_Tip:_ reply in this thread: `@{BOT_NAME} triage <what you’re seeing>`")
    

# -------- NEW: Escalate button --------
@app.action("agent8_escalate")
def handle_escalate(ack, body, say, logger):
    """
    Handle Escalate button → posts a mailto: link into the thread.
    This does not send email directly; it opens the user's local mail client.
    """
    ack()

    try:
        import urllib.parse

        # Extract channel + thread
        channel = body.get("container", {}).get("channel_id") or body.get("channel", {}).get("id")
        thread_ts = body.get("container", {}).get("message_ts") or body.get("message", {}).get("ts")

        # Parse button payload (value JSON)
        payload = {}
        try:
            val = (body.get("actions") or [{}])[0].get("value") or "{}"
            payload = json.loads(val)
        except Exception:
            pass

        config_dir = payload.get("config_dir", "")
        task_id    = payload.get("task_dir", "")
        host       = payload.get("host", "")
        session_id = payload.get("session_id", "")

        # --- Build email subject + body (URL-encoded) ---
        subject = f"Escalation - {task_id} - {host}"
        body_lines = [
            "Escalation Report",
            "",
            f"Config: {config_dir}",
            f"Task: {task_id}",
            f"Host: {host}",
            f"Session: {session_id}",
            "",
            f"Slack thread: https://slack.com/app_redirect?channel={channel}&message_ts={thread_ts}",
            "",
            "Summary: Triage session requires L3 investigation.",
            "Full CLI outputs are available in the attached Slack thread."
        ]
        body_txt = "\n".join(body_lines)

        subject_enc = urllib.parse.quote(subject)
        body_enc = urllib.parse.quote(body_txt)

        mailto_url = f"mailto:?subject={subject_enc}&body={body_enc}"

        # --- Post back to Slack thread with clickable link ---
        say(
            channel=channel,
            thread_ts=thread_ts,
            text=f"📧 Click to escalate via email:\n<{mailto_url}|Open mail draft>"
        )

    except Exception as e:
        logger.error(f"agent8_escalate error: {e}")
        say(channel=channel, thread_ts=thread_ts,
            text=f"⚠️ Escalation failed: {e}")


# Optional: silence generic "message" events
@app.event("message")
def ignore_plain_messages(body, logger):
    pass

if __name__ == "__main__":
    print("[DEBUG] Orchestrator Slack bot starting...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()