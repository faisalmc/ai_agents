# orchestrator/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import sys
sys.path.append("/app_mount/shared")
from push_core import push_configs

# create the FastAPI app BEFORE any decorators
app = FastAPI()

# add near the top (once)
def _sanitize(obj):
    if obj is ...:
        return None
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj

class DeployInput(BaseModel):
    config_dir: str
    task_dir: str
    device_filter: Optional[List[str]] = None
    dry_run: bool = False

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/deploy")
def deploy(inp: DeployInput):
    result = push_configs(
        config_dir=inp.config_dir,
        task_dir=inp.task_dir,
        device_filter=inp.device_filter,
        dry_run=inp.dry_run,
    )
    print("[DEBUG] deploy keys:", list(result.keys()), flush=True)
    print("[DEBUG] types:", {k: type(v).__name__ for k, v in result.items()}, flush=True)
    return result