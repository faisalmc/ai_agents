# agents/agent-router/llm_clients/agent2_api.py
import sys
sys.path.append("/app/agents/agent-router/llm_clients")

# Re-export the FastAPI app already defined in agent_b_push_configs.py
# That file already wires /deploy and posts to Slack using WebClient.
from agent_b_push_configs import api as app


# import os, sys
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# # # existing shared push logic
# # sys.path.append("/app/shared")
# # from push_core import push_configs

# ## import the *existing* Slack posting logic from agent_b (no duplication)
# sys.path.append("/app/agents/agent-router/llm_clients")
# # from agent_b_push_configs import post_summary_to_slack, slack_client  # reuses your code
# # from agents.agent-router.llm_clients.agent_b_push_configs import api as app
# from agent_b_push_configs import api as app

# app = FastAPI()

# class DeployReq(BaseModel):
#     config_dir: str
#     task_dir: str
#     device_filter: str | None = None
#     dry_run: bool = False
#     # Slack context from orchestrator_bot:
#     slack_channel: str | None = None
#     slack_thread_ts: str | None = None

# @app.post("/deploy")
# def deploy(req: DeployReq):
#     try:
#         # IMPORTANT: push_configs() does NOT accept task_id → don't pass it.
#         result = push_configs(
#             config_dir=req.config_dir,
#             task_dir=req.task_dir,
#             dry_run=req.dry_run
#         )

#         # If orchestrator_bot provided Slack context, post the same summary + upload file
#         if req.slack_channel:
#             try:
#                 post_summary_to_slack(
#                     slack_client=slack_client,
#                     channel=req.slack_channel,
#                     thread_ts=req.slack_thread_ts,
#                     result=result,
#                     config_dir=req.config_dir,
#                     task_dir=req.task_dir,
#                 )
#             except Exception as e:
#                 print(f"[agent-2:/deploy] Slack post failed: {e}")

#         return result

#     except Exception as e:
#         print(f"[agent-2:/deploy] ERROR: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# ##### below worked as part of 2.working.central_orchestrator
# # import os
# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # import sys
# # sys.path.append("/app/shared")
# # from push_core import push_configs

# # app = FastAPI()

# # class DeployReq(BaseModel):
# #     config_dir: str
# #     task_dir: str
# #     device_filter: str | None = None
# #     dry_run: bool = False

# # @app.post("/deploy")
# # def deploy(req: DeployReq):
# #     try:
# #         # Call push_configs with accepted params only
# #         result = push_configs(
# #             config_dir=req.config_dir,
# #             task_dir=req.task_dir,
# #             dry_run=req.dry_run
# #         )
# #         return result
# #     except Exception as e:
# #         print(f"[agent-2:/deploy] ERROR: {e}")
# #         raise HTTPException(status_code=500, detail=str(e))