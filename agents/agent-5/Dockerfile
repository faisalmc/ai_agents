FROM python:3.11-slim

# Optional debugging tools; drop if you want smaller images
RUN apt-get update \
  && apt-get install -y --no-install-recommends git net-tools curl \
  && rm -rf /var/lib/apt/lists/*

# We'll mount the repo at /app in compose; keep /app as base
WORKDIR /app

# Install only Agent-5 deps (build context is agents/agent-5)
COPY requirements.txt /app/requirements-agent5.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements-agent5.txt

# Make shared imports work if you later move utils to /app/shared
ENV PYTHONPATH=/app:/app/shared

EXPOSE 8004

# We’ll override CMD in docker-compose; leaving a harmless default here:
CMD ["uvicorn", "agent5_api:app", "--host", "0.0.0.0", "--port", "8004"]

# ## version-1
# FROM python:3.11-slim

# # install git, net-tools, curl for diagnostics
# RUN apt-get update \
#   && apt-get install -y --no-install-recommends \
#        git net-tools curl \
#   && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # copy only dependencies and install them
# COPY requirements.txt .
# RUN python -m pip install --upgrade pip \
#  && pip install --no-cache-dir -r requirements.txt

# COPY orchestrator.py utils.py ./
# COPY orchestrator/agent2_client.py orchestrator/agent3_client.py ./ 
# CMD ["python", "orchestrator.py"]

# # # expose health port
# # EXPOSE 8000

# # # no entrypoint – this is just your dependency layer