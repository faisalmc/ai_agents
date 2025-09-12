FROM python:3.11-slim

# Optional debugging tools; drop if you want smaller images
RUN apt-get update \
  && apt-get install -y --no-install-recommends git net-tools curl \
  && rm -rf /var/lib/apt/lists/*

# We'll mount the repo at /app in compose; keep /app as base
WORKDIR /app

# Install only Agent-4 deps (build context is agents/agent-4)
# keeping per-agent requirements.txt in agents/agent-4/
COPY requirements.txt /app/requirements-agent4.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements-agent4.txt

# Make shared imports work if you later move utils to /app/shared
ENV PYTHONPATH=/app:/app/shared

EXPOSE 8003

# We’ll override CMD in docker-compose; leaving a harmless default here:
CMD ["uvicorn", "agent4_api:app", "--host", "0.0.0.0", "--port", "8003"]
