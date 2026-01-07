#!/usr/bin/env bash
set -euo pipefail

# Create a new content item from templates.
#
# Usage:
#   ./scripts/new_item.sh <type> <slug> "<Title>"
#
# Examples:
#   ./scripts/new_item.sh factions banking-guild "Banking Guild"
#   ./scripts/new_item.sh quests q-magic-blight-monastery "The Blighted Monastery"
#   ./scripts/new_item.sh locations sunkeep "Sunkeep"
#
# Notes:
# - For quests, this will use templates/quest_item.template.md
# - For everything else, it uses templates/content_item.template.md
# - Writes to: items/<type>/<slug>.md  (creates folders if needed)

TYPE="${1:-}"
SLUG="${2:-}"
TITLE="${3:-}"

if [[ -z "$TYPE" || -z "$SLUG" || -z "$TITLE" ]]; then
  echo "ERROR: Missing args." >&2
  echo "Usage: $0 <type> <slug> \"<Title>\"" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITEM_DIR="$ROOT_DIR/items/$TYPE"
OUT_FILE="$ITEM_DIR/$SLUG.md"

if [[ "$TYPE" == "quests" || "$TYPE" == "quest" ]]; then
  TEMPLATE="$ROOT_DIR/templates/quest_item.template.md"
else
  TEMPLATE="$ROOT_DIR/templates/content_item.template.md"
fi

if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: Template not found: $TEMPLATE" >&2
  exit 1
fi

mkdir -p "$ITEM_DIR"

if [[ -f "$OUT_FILE" ]]; then
  echo "ERROR: File already exists: $OUT_FILE" >&2
  exit 1
fi

python3 - "$TEMPLATE" "$OUT_FILE" "$SLUG" "$TITLE" "$TYPE" <<'PY'
import sys, re
from pathlib import Path

template = Path(sys.argv[1]).read_text(encoding="utf-8")
out_path = Path(sys.argv[2])
slug = sys.argv[3]
title = sys.argv[4]
type_ = sys.argv[5]

# Normalize type if user used "quest"
if type_ == "quest":
    type_ = "quests"

# Patch frontmatter keys if present
def patch_frontmatter(md: str) -> str:
    # Update id/title/type where possible
    def repl(key, value, s):
        return re.sub(rf"^({key}:\s*).*$", rf"\1{value}", s, flags=re.M)
    md = repl("id", slug, md)
    md = repl("title", title, md)
    # for quest template, type: quest is correct; for content template, we set to folder name singular-ish
    # keep it simple: set type to 'quest' if quests else type_ without trailing 's'
    if type_ == "quests":
        t = "quest"
    else:
        t = type_.rstrip("s")
    md = repl("type", t, md)
    return md

patched = patch_frontmatter(template).strip() + "\n"
out_path.write_text(patched, encoding="utf-8")
PY

echo "Created: $OUT_FILE"
