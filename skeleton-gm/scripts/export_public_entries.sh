#!/usr/bin/env bash
set -euo pipefail

PUBLIC_REPO_PATH="${PUBLIC_REPO_PATH:-../__PUBLIC_REPO_NAME__}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITEMS_DIR="$ROOT_DIR/items"
OUT_DIR="$PUBLIC_REPO_PATH/content"

if [[ ! -d "$PUBLIC_REPO_PATH" ]]; then
  echo "ERROR: PUBLIC_REPO_PATH does not exist: $PUBLIC_REPO_PATH" >&2
  exit 1
fi

if [[ ! -d "$PUBLIC_REPO_PATH/.git" ]]; then
  echo "ERROR: PUBLIC_REPO_PATH is not a git repo (missing .git): $PUBLIC_REPO_PATH" >&2
  echo "Hint: cd into the public repo and run: git init" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

validate_markers() {
  local file="$1"
  python3 - <<PY
from pathlib import Path
import re, sys

text = Path("$file").read_text(encoding="utf-8")

def count(tag):
    return len(re.findall(rf"<!--\s*{tag}\s*-->", text))

for start, end in [("PUBLIC_START","PUBLIC_END"), ("PRIVATE_START","PRIVATE_END")]:
    cs, ce = count(start), count(end)
    if cs != ce:
        print(f"ERROR: Unbalanced markers in {Path('$file').name}: {start}={cs}, {end}={ce}", file=sys.stderr)
        sys.exit(2)
PY
}

render_export() {
  local file="$1"
  python3 - <<PY
from pathlib import Path
import re

p = Path("$file")
text = p.read_text(encoding="utf-8")

fm = ""
body = text
m = re.match(r"^---\\s*\\n(.*?)\\n---\\s*\\n(.*)$", text, re.S)
if m:
    fm = m.group(1).strip()
    body = m.group(2)

pub_lines = []
in_pub = False
for line in body.splitlines():
    if re.search(r"<!--\\s*PUBLIC_START\\s*-->", line):
        in_pub = True
        continue
    if re.search(r"<!--\\s*PUBLIC_END\\s*-->", line):
        in_pub = False
        continue
    if in_pub:
        pub_lines.append(line)

pub = "\\n".join(pub_lines).strip()

out = ""
if fm:
    out += "---\\n" + fm + "\\n---\\n\\n"
out += pub + ("\\n" if pub else "")

print(out)
PY
}

while IFS= read -r -d '' file; do
  rel="${file#$ITEMS_DIR/}"
  out_file="$OUT_DIR/$rel"
  mkdir -p "$(dirname "$out_file")"

  validate_markers "$file"

  content="$(render_export "$file")"
  if [[ -z "${content//[[:space:]]/}" ]]; then
    rm -f "$out_file"
    continue
  fi
  printf "%s\n" "$content" > "$out_file"
done < <(find "$ITEMS_DIR" -type f -name "*.md" -print0 | sort -z)

echo "Export complete -> $OUT_DIR"
echo
echo "Public repo status:"
( cd "$PUBLIC_REPO_PATH" && git status --porcelain && echo "OK" )
