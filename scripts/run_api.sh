#!/usr/bin/env bash
# Run Zora API (FastAPI) locally.

set -euo pipefail

SUITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PATH="$SUITE_ROOT/.venv"
LOCAL_SITE_PACKAGES="$SUITE_ROOT/.python_packages"
REQUIREMENTS_PATH="$SUITE_ROOT/api/requirements.txt"
INSTALL_STAMP="$VENV_PATH/.zora_requirements_installed"
LOCAL_INSTALL_STAMP="$LOCAL_SITE_PACKAGES/.zora_requirements_installed"

use_venv=true

if [[ ! -d "$VENV_PATH" ]]; then
  if ! python3 -m venv "$VENV_PATH"; then
    use_venv=false
    rm -rf "$VENV_PATH"
  fi
fi

if [[ "$use_venv" == true && -f "$VENV_PATH/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$VENV_PATH/bin/activate"

  if [[ ! -f "$INSTALL_STAMP" || "$REQUIREMENTS_PATH" -nt "$INSTALL_STAMP" ]]; then
    python -m pip install --upgrade pip
    python -m pip install -r "$REQUIREMENTS_PATH"
    touch "$INSTALL_STAMP"
  fi
else
  mkdir -p "$LOCAL_SITE_PACKAGES"
  if [[ ! -f "$LOCAL_INSTALL_STAMP" || "$REQUIREMENTS_PATH" -nt "$LOCAL_INSTALL_STAMP" ]]; then
    python3 -m pip install --target "$LOCAL_SITE_PACKAGES" -r "$REQUIREMENTS_PATH"
    touch "$LOCAL_INSTALL_STAMP"
  fi
  export PYTHONPATH="$LOCAL_SITE_PACKAGES${PYTHONPATH:+:$PYTHONPATH}"
fi

cd "$SUITE_ROOT/api"
exec python3 -m uvicorn main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}"
