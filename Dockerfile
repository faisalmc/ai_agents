## version-1
FROM python:3.11-slim

# install git, net-tools, curl for diagnostics
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       git net-tools curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy only dependencies and install them
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY orchestrator.py utils.py ./
COPY orchestrator/agent2_client.py orchestrator/agent3_client.py ./ 
CMD ["python", "orchestrator.py"]

# # expose health port
# EXPOSE 8000

# # no entrypoint – this is just your dependency layer