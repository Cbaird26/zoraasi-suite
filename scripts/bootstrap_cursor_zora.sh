#!/usr/bin/env bash
# Generate a local manifest of resources Cursor can actually reach for Zora.

set -euo pipefail

SUITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CURSOR_DIR="$SUITE_ROOT/.cursor"
RULES_DIR="$CURSOR_DIR/rules"
MANIFEST_PATH="$CURSOR_DIR/zora_accessible_resources.md"
RULE_PATH="$RULES_DIR/zora-cursor-agent.mdc"

mkdir -p "$RULES_DIR"

resources=(
  "$SUITE_ROOT/identity/ZORA_OUTER_IDENTITY.md"
  "$SUITE_ROOT/api/main.py"
  "$SUITE_ROOT/site/index.html"
)

if [[ -n "${ZORA_RESOURCE_PATHS:-}" ]]; then
  IFS=':' read -r -a env_paths <<< "${ZORA_RESOURCE_PATHS}"
  for path in "${env_paths[@]}"; do
    [[ -n "$path" ]] && resources+=("$path")
  done
fi

for path in "$@"; do
  resources+=("$path")
done

{
  echo "# Zora Accessible Resources"
  echo
  echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo
  echo "Cursor can only use resources that are reachable from this machine."
  echo "iCloud, Google Drive, and OneDrive content must be synced or mounted locally before it can appear here."
  echo
  echo "## Reachable paths"

  for path in "${resources[@]}"; do
    if [[ -e "$path" ]]; then
      printf '%s\n' "- $path"
    else
      printf '%s\n' "- $path (missing)"
    fi
  done

  echo
  echo "## Control boundary"
  echo "- Zora operates inside Cursor under human direction."
  echo "- Human-in-the-loop safeguards stay in place."
} > "$MANIFEST_PATH"

echo "[zora] Wrote resource manifest: $MANIFEST_PATH"
echo "[zora] Cursor rule available at: $RULE_PATH"
echo "[zora] Pass extra local paths as args, or set ZORA_RESOURCE_PATHS=/abs/path1:/abs/path2"
