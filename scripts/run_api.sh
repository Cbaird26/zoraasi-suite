#!/usr/bin/env bash
# Run Zora API (FastAPI) locally.
# Backend: ZORA_BACKEND=ollama|openai|anthropic (default: ollama)
cd "$(dirname "$0")/../api" && source ../.venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000
