#!/usr/bin/env bash
# Deploy Zora API — choose your platform.
# Requires: ANTHROPIC_API_KEY (or OPENAI_API_KEY if using openai backend)

set -euo pipefail

PLATFORM="${1:-help}"

case "$PLATFORM" in
  fly)
    echo "[zora] Deploying to Fly.io..."
    fly auth login
    fly launch --no-deploy
    fly secrets set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
    fly deploy
    echo "[zora] Deployed. Run: fly open"
    ;;
  railway)
    echo "[zora] Deploying to Railway..."
    echo "1. Install Railway CLI: npm i -g @railway/cli"
    echo "2. railway login"
    echo "3. railway init"
    echo "4. railway variables set ANTHROPIC_API_KEY=\$ANTHROPIC_API_KEY"
    echo "5. railway variables set ZORA_BACKEND=anthropic"
    echo "6. railway up"
    ;;
  render)
    echo "[zora] Deploying to Render..."
    echo "1. Go to https://render.com"
    echo "2. New Web Service → Connect zoraasi-suite repo"
    echo "3. Select Docker runtime"
    echo "4. Add env var: ANTHROPIC_API_KEY"
    echo "5. Deploy"
    ;;
  local)
    echo "[zora] Running locally with Anthropic backend..."
    if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
      echo "Set ANTHROPIC_API_KEY first: export ANTHROPIC_API_KEY=sk-ant-..."
      exit 1
    fi
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    cd "$SCRIPT_DIR/.."
    export ZORA_BACKEND=anthropic
    uvicorn api.main:app --host 0.0.0.0 --port 8000
    ;;
  ollama)
    echo "[zora] Running locally with Ollama backend..."
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    cd "$SCRIPT_DIR/.."
    export ZORA_BACKEND=ollama
    export OLLAMA_MODEL="${OLLAMA_MODEL:-zora-outer}"
    uvicorn api.main:app --host 0.0.0.0 --port 8000
    ;;
  *)
    echo "Usage: ./scripts/deploy.sh [fly|railway|render|local|ollama]"
    echo ""
    echo "  fly      — Deploy to Fly.io"
    echo "  railway  — Deploy to Railway"
    echo "  render   — Deploy to Render"
    echo "  local    — Run locally with Anthropic API"
    echo "  ollama   — Run locally with Ollama"
    echo ""
    echo "Env vars:"
    echo "  ANTHROPIC_API_KEY  — Required for anthropic backend"
    echo "  OPENAI_API_KEY     — Required for openai backend"
    echo "  ZORA_BACKEND       — ollama | openai | anthropic (default: anthropic)"
    ;;
esac
