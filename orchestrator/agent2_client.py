# orchestrator/agent2_client.py
import os
import asyncio
import httpx

ORCH_URL = os.getenv("ORCH_URL", "http://orchestrator:8080/deploy")

print(f"[DEBUG] ORCH_URL={ORCH_URL}", flush=True)

async def _post_deploy(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=1200) as c:
        r = await c.post(ORCH_URL, json=payload)
        r.raise_for_status()
        return r.json()

# def run_deploy(config_dir: str, task_id: str, channel: str, thread_ts: str, user: str) -> dict:
#     payload = {
#         "config_dir": config_dir,
#         "task_dir": task_id,
#         "device_filter": None,
#         "dry_run": False,
#         "channel": channel,
#         "thread_ts": thread_ts,
#         "user": user,
#     }
#     return asyncio.run(_post_deploy(payload))

def run_deploy(config_dir: str, task_id: str, channel: str, thread_ts: str, user: str) -> dict:
    payload = {
        "config_dir": config_dir,
        "task_id": task_id,         # agent_b_http expects task_id (or task_dir)
        "channel": channel,         # not slack_channel
        "thread_ts": thread_ts,     # not slack_thread_ts
        "requested_by": user,       # optional passthrough
    }
    return asyncio.run(_post_deploy(payload))