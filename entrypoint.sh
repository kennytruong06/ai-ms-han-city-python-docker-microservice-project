#!/bin/bash
set -e

echo "[START] Starting nsfw-ai-microservice project with Gunicorn..."

# Default value for ENV is "dev" if not set
ENV=${ENV:-dev}

# Construct gunicorn command
CMD="gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000"

# Add --reload in dev mode
if [ "$ENV" = "dev" ]; then
  echo "[INFO] Dev mode detected — enabling hot reload"

  CMD="$CMD --reload"
fi

echo "[INFO] Running: $CMD"
exec $CMD
