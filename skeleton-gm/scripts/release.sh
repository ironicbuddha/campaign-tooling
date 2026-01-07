#!/usr/bin/env bash
set -euo pipefail

PUBLIC_REPO_PATH="${PUBLIC_REPO_PATH:-../__PUBLIC_REPO_NAME__}"

GM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_SCRIPT="$GM_ROOT/scripts/export_public_entries.sh"

COMPILE_SCRIPT="$PUBLIC_REPO_PATH/scripts/compile_guides.sh"

echo "== Exporting player-safe entries =="
(
  cd "$GM_ROOT"
  PUBLIC_REPO_PATH="$PUBLIC_REPO_PATH" "$EXPORT_SCRIPT"
)

echo
echo "== Compiling guides in public repo =="
(
  cd "$PUBLIC_REPO_PATH"
  "$COMPILE_SCRIPT"
)

echo
echo "Done."
