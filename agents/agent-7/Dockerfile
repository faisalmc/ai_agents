FROM python:3.11-slim

# Optional but handy tools. Remove for smaller image.
RUN apt-get update \
  && apt-get install -y --no-install-recommends git curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Agent-7 deps
COPY requirements.txt /app/requirements-agent7.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements-agent7.txt

# Make repo imports work; we usually mount the repo at /app in compose
ENV PYTHONPATH=/app:/app/shared

# Env defaults (override in compose)
ENV REPO_ROOT=/app/doo \
    AGENT7_CACHE_TTL_MIN=15 \
    AGENT7_AUDIT_MAX_BYTES=1048576 \
    AGENT7_AUDIT_ROTATE_KEEP=3

# ---- Import path workaround for hyphenated package name ----
# Create a symlink so we can import agents.agent_7 when the folder is agents/agent-7
RUN mkdir -p /app/agents \
 && ln -s /app/agents/agent-7 /app/agents/agent_7 || true

EXPOSE 8007

# Default (safe) CMD. Override in docker-compose as needed.
# Example override:
#   uvicorn agents.agent_7.http_api:app --host 0.0.0.0 --port 8007
CMD ["uvicorn", "agents.agent_7.http_api:app", "--host", "0.0.0.0", "--port", "8007"]
