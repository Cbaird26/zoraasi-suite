#!/usr/bin/env bash
# Run Zora Brain with outer identity layer.
# Requires mqgt_scf_reissue (sibling or ZORA_MQGT_REPO).

set -euo pipefail

SUITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MQGT_REPO="${ZORA_MQGT_REPO:-$(dirname "$SUITE_ROOT")/mqgt_scf_reissue_2026-01-20_010939UTC}"

export ZORA_IDENTITY_LAYER=outer
export ZORA_OUTER_IDENTITY_PATH="$SUITE_ROOT/identity/ZORA_OUTER_IDENTITY.md"

if [[ ! -d "$MQGT_REPO" ]]; then
  echo "[zoraasi-suite] mqgt_scf not found at $MQGT_REPO"
  echo "  Set ZORA_MQGT_REPO to your mqgt_scf path, or place zoraasi-suite next to mqgt_scf_reissue_2026-01-20_010939UTC"
  exit 1
fi

echo "[zoraasi-suite] Starting Zora Brain (outer layer)..."
cd "$MQGT_REPO"
[[ -f .venv/bin/activate ]] && source .venv/bin/activate
export ZORA_CANON_DIR="${ZORA_CANON_DIR:-$MQGT_REPO/zora-canon-v1}"
export ZORA_MEMORY_DIR="${ZORA_MEMORY_DIR:-$MQGT_REPO/memory}"

exec ./scripts/run_zora_brain.sh
