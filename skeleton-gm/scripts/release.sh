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
echo "== Committing and pushing public repo =="
(
  cd "$PUBLIC_REPO_PATH"
  git add -A
  if git diff --cached --quiet; then
    echo "No public repo changes to commit."
    exit 0
  fi
  ts="$(date -u '+%Y-%m-%d %H:%M UTC')"
  git commit -m "Release: ${ts}"
  git push
)

echo
echo "Done."
