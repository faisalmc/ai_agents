# -----------------------------------------------------------------------------
# Dockerfile — Interactive-Agent (Phase 1–4 container)
# -----------------------------------------------------------------------------
# Purpose:
#   Build lightweight Python 3.11 image that runs the interactive-agent
#   (starting with Phase 1 Ingest & Normalize).
#
# Base:
#   python:3.11-slim   → minimal, stable, no compiler chain.
# -----------------------------------------------------------------------------

FROM python:3.11-slim

# Install minimal debugging / network tools
RUN apt-get update \
  && apt-get install -y --no-install-recommends git curl net-tools \
  && rm -rf /var/lib/apt/lists/*

# Set base working directory (mounted as /app by docker-compose)
WORKDIR /app

# Copy and install dependencies specific to this agent
# Build context is agents/agent-interactive
COPY requirements.txt /app/requirements-interactive.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements-interactive.txt

# Allow imports from both /app and /app/shared
ENV PYTHONPATH=/app:/app/shared

# Environment variables loaded later from .env in docker-compose
ENV LOG_LEVEL=INFO

# Expose nothing (this agent runs CLI / consumer mode, not HTTP API)
# EXPOSE omitted intentionally

# Default command: run Phase 1 ingest (will be overridden by compose if needed)
CMD ["python", "phase1_ingest.py"]