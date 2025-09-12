# orchestrator/agent3_client.py
import os
import asyncio
import httpx

ORCH_A3_URL = os.getenv("ORCH_A3_URL", "http://orchestrator:8080/analyze-host")
print(f"[DEBUG] ORCH_A3_URL={ORCH_A3_URL}", flush=True)


async def _post_analyze(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=1200) as c:
        r = await c.post(ORCH_A3_URL, json=payload)
        r.raise_for_status()
        # Expecting {"status":"accepted"} from the shim
        return r.json()


def run_analyze_host(
    config_dir: str,
    task_id: str,
    hostname: str,
    channel: str,
    thread_ts: str | None,
    user: str | None,
) -> dict:
    payload = {
        "config_dir": config_dir,
        "task_id": task_id,
        "hostname": hostname,
        "channel": channel,
        "thread_ts": thread_ts,
        "requested_by": user,
    }
    return asyncio.run(_post_analyze(payload))