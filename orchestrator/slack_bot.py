# orchestrator/slack_bot.py
import os, json, importlib.util
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from agent2_client import run_deploy              # Agent-2 (/deploy)
from agent3_client import run_analyze_host        # Agent-3 (/analyze-host)
from agent4_client import run_operational_check   # Agent-4 (/operational-check)
from agent5_client import run_operational_analyze # Agent-5 (/operational-analyze)
from agent7_client import run_plan as run_a7_plan, run_capture as run_a7_capture, run_analyze as run_a7_analyze

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
BOT_NAME = os.getenv("ORCHESTRATOR_BOT_NAME", "agent")

# Where the repo data lives (to locate artifacts to attach)
REPO_ROOT = os.getenv("REPO_ROOT", "/app/doo")
# Where to import Agent-7 Slack UI renderer from (file path).

# # Default now points inside REPO_ROOT so it exists in the Orchestrator container.
# A7_SLACK_UI_PATH = os.getenv("A7_SLACK_UI_PATH", os.path.join(REPO_ROOT, "agents", "agent-7", "slack_ui.py"))
A7_SLACK_UI_PATH = os.getenv("A7_SLACK_UI_PATH", "/app/agents/agent-7/slack_ui.py")

app = App(token=SLACK_BOT_TOKEN)

print(f"[DEBUG] slack_bot.py: A7_SLACK_UI_PATH={A7_SLACK_UI_PATH} REPO_ROOT={REPO_ROOT}", flush=True)

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

# commented out to add DEBUGs
# def _load_a7_slack_ui():
#     """
#     Dynamically import agents/agent-7/slack_ui.py even though the parent
#     folder has a hyphen and isn't a valid package name.
#     """
#     try:
#         spec = importlib.util.spec_from_file_location("a7_slack_ui", A7_SLACK_UI_PATH)
#         if spec and spec.loader:
#             mod = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(mod)  # type: ignore
#             return mod
#     except Exception:
#         pass
#     return None

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

# commented out to add DEBUGs
# def _post_a7_overview(say, channel: str, thread_ts: str, config_dir: str, task_id: str,
#                       per_device_path: str | None, cross_device_path: str | None):
#     """
#     Fallback renderer if run_a7_analyze didn't return prebuilt blocks.
#     """
#     ui = _load_a7_slack_ui()
#     per_device = _read_json(per_device_path) if per_device_path else None
#     cross = _read_json(cross_device_path) if cross_device_path else None

#     # Fallback: if import failed or malformed data, just print a compact text.
#     if not ui or not hasattr(ui, "build_overview_blocks"):
#         status = (cross or {}).get("task_status", "unknown") if isinstance(cross, dict) else "unknown"
#         hosts = len(per_device or []) if isinstance(per_device, list) else 0
#         say(
#             channel=channel,
#             thread_ts=thread_ts,
#             text=(f"*Agent-7 Overview*\n"
#                   f"Config `{config_dir}` Task `{task_id}` • Status: *{status}* • Per-device rows: {hosts}\n"
#                   f"(Install slack_ui or set A7_SLACK_UI_PATH for rich blocks)")
#         )
#         return

#     blocks = ui.build_overview_blocks(
#         config_dir=config_dir,
#         task_dir=task_id,
#         cross=cross if isinstance(cross, dict) else {},
#         per_device=per_device if isinstance(per_device, list) else [],
#         include_attach_button=True,
#     )
#     # Slack requires a fallback text string even with blocks
#     say(channel=channel, thread_ts=thread_ts, text="Agent-7 Analysis", blocks=blocks)

def _post_a7_overview(say, channel: str, thread_ts: str, config_dir: str, task_id: str,
                      per_device_path: str | None, cross_device_path: str | None):
    print(f"[DEBUG] _post_a7_overview: per_device_path={per_device_path} cross_device_path={cross_device_path}", flush=True)

    ui = _load_a7_slack_ui()

    per_device = _read_json(per_device_path) if per_device_path else None
    cross = _read_json(cross_device_path) if cross_device_path else None

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
    thread_ts = ev.get("ts")
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

    # # Agent-7 ANALYZE
    # if cmd == "a7-analyze" and len(parts) == 3:
    #     args = parts[2].split()
    #     if len(args) != 2:
    #         say(channel=channel, thread_ts=thread_ts,
    #             text=f"Usage: `@{BOT_NAME} a7-analyze <config_dir> <task_id>`")
    #         return
    #     config_dir, task_id = args
    #     say(channel=channel, thread_ts=thread_ts,
    #         text=f"🔎 Routing to Agent-7 /analyze: `{config_dir}` `{task_id}` …")
    #     res = run_a7_analyze(config_dir, task_id)

    #     # Post concise pointer (kept for continuity)
    #     say(channel=channel, thread_ts=thread_ts,
    #         text=(f"✅ Analyze summary: `{res.get('facts_summary_path','')}` • hosts={res.get('hosts_processed',0)}"))

    #     # Prefer prebuilt blocks from agent7_client; fallback to local renderer if missing.
    #     blocks = res.get("blocks")
    #     if isinstance(blocks, list) and blocks:
    #         say(channel=channel, thread_ts=thread_ts, text="Agent-7 Analysis", blocks=blocks)
    #     else:
    #         _post_a7_overview(
    #             say=say,
    #             channel=channel,
    #             thread_ts=thread_ts,
    #             config_dir=config_dir,
    #             task_id=task_id,
    #             per_device_path=res.get("per_device_json_path"),
    #             cross_device_path=res.get("cross_device_json_path"),
    #         )
    #     return

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

            # 2) Fallback to local renderer → per_device + cross (with attach button)
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

            # Prefer prebuilt blocks; fallback if missing
            # Prefer LLM-made slack_overview.json (blocks/text) if present
            if _post_a7_llm_overview_if_available(
                say, channel, thread_ts, ana_res.get("slack_overview_path")
            ):
                pass
            else:
                # Fallback to local renderer
                _post_a7_overview(
                    say=say,
                    channel=channel,
                    thread_ts=thread_ts,
                    config_dir=config_dir,
                    task_id=task_id,
                    per_device_path=ana_res.get("per_device_json_path"),
                    cross_device_path=ana_res.get("cross_device_json_path"),
                )
            # blocks = ana_res.get("blocks")
            # if isinstance(blocks, list) and blocks:
            #     say(channel=channel, thread_ts=thread_ts, text="Agent-7 Analysis", blocks=blocks)
            # else:
            #     _post_a7_overview(
            #         say=say,
            #         channel=channel,
            #         thread_ts=thread_ts,
            #         config_dir=config_dir,
            #         task_id=task_id,
            #         per_device_path=ana_res.get("per_device_json_path"),
            #         cross_device_path=ana_res.get("cross_device_json_path"),
            #     )

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
                
# Optional: silence generic "message" events
@app.event("message")
def ignore_plain_messages(body, logger):
    pass

if __name__ == "__main__":
    print("[DEBUG] Orchestrator Slack bot starting...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()