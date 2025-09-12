FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

# # version 1
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN python -m pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt
# COPY app.py .
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

