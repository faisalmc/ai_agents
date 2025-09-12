# agents/agent-router/llm_clients/agent3_api.py
import sys
sys.path.append("/app/agents/agent-router/llm_clients")

# Re-export the FastAPI app defined in agent3_http.py
from agent3_http import app as app