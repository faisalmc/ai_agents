from slack_sdk import WebClient

def reply_in_thread(client: WebClient, channel: str, thread_ts: str, text: str):
    client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)

def reply_ephemeral_safe(client: WebClient, channel: str, user: str, text: str):
    try:
        client.chat_postEphemeral(channel=channel, user=user, text=text)
    except Exception:
        # Fallback if ephemeral fails (e.g., not in channel)
        client.chat_postMessage(channel=channel, text=text)

def get_user_mention(user_id: str) -> str:
    return f"<@{user_id}>"