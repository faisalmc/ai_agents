import os, re, json, traceback
from typing import Dict, Optional, Tuple
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from agent2_client import run_deploy
from agent3_client import run_analyze
from utils import reply_ephemeral_safe, reply_in_thread, get_user_mention

BOT_NAME = os.getenv("ORCHESTRATOR_BOT_NAME", "orchestrator")

# Regexes for commands after the mention.
# Message will look like: "<@Uxxxx> deploy configs.5 task-1"
RE_DEPLOY = re.compile(r"\bdeploy\s+(\S+)\s+(\S+)\b", re.IGNORECASE)
RE_ANALYZE = re.compile(r"\banalyze\s+(\S+)\b", re.IGNORECASE)

app = App(token=os.environ["SLACK_BOT_TOKEN"])

def parse_command(text: str) -> Tuple[str, Tuple[str, ...]]:
    """
    Returns (cmd, args)
    cmd in {"deploy", "analyze", "help"}
    """
    t = text.strip()

    m = RE_DEPLOY.search(t)
    if m:
        config_dir, task_id = m.group(1), m.group(2)
        return ("deploy", (config_dir, task_id))

    m = RE_ANALYZE.search(t)
    if m:
        target = m.group(1)
        return ("analyze", (target,))

    return ("help", ())

def help_text() -> str:
    return (
        f"*Central Orchestrator (@{BOT_NAME})*\n"
        "Usage:\n"
        f"• `@{BOT_NAME} deploy <config_dir> <task_id>` – push configs via Agent-2\n"
        f"  e.g. `@{BOT_NAME} deploy configs.5 task-1`\n"
        f"• `@{BOT_NAME} analyze <target>` – analyze logs via Agent-3\n"
        f"  e.g. `@{BOT_NAME} analyze B-PE-3`\n"
        "_Tip:_ Mention me in a channel I’m a member of, or DM me."
    )

@app.event("app_mention")
def on_app_mention(body, say, logger):
    event = body.get("event", {})
    channel = event.get("channel")
    user = event.get("user")
    thread_ts = event.get("ts")
    text = event.get("text", "")

    try:
        cmd, args = parse_command(text)

        if cmd == "help":
            reply_in_thread(app.client, channel, thread_ts, help_text())
            return

        if cmd == "deploy":
            config_dir, task_id = args
            reply_in_thread(app.client, channel, thread_ts,
                            f"🧭 Routing to *Agent-2* (deploy): `{config_dir}` `{task_id}` …")
            # Route to Agent-2 (keep your existing logic intact)
            result = run_deploy(config_dir=config_dir, task_id=task_id, channel=channel, thread_ts=thread_ts, user=user)
            reply_in_thread(app.client, channel, thread_ts, f"✅ Deploy request accepted.\n{result}")
            return

        if cmd == "analyze":
            (target,) = args
            reply_in_thread(app.client, channel, thread_ts,
                            f"🧭 Routing to *Agent-3* (analyze): `{target}` …")
            result = run_analyze(target=target, channel=channel, thread_ts=thread_ts, user=user)
            reply_in_thread(app.client, channel, thread_ts, f"✅ Analyze request accepted.\n{result}")
            return

        reply_in_thread(app.client, channel, thread_ts, help_text())

    except SlackApiError as e:
        reply_in_thread(app.client, channel, thread_ts,
                        f"❌ Slack API error: `{e.response.get('error')}`")
        logger.exception("Slack API error")
    except Exception as e:
        reply_in_thread(app.client, channel, thread_ts,
                        f"❌ Internal error: `{e}`")
        logger.exception("Unhandled exception")

if __name__ == "__main__":
    app_token = os.environ["SLACK_APP_TOKEN"]
    SocketModeHandler(app, app_token).start()