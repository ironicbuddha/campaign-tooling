#!/usr/bin/env bash
set -euo pipefail


# --- Push control -------------------------------------------------------------
PUSH_TO_GH="false"
if [[ "${1:-}" == "--push" ]]; then
  PUSH_TO_GH="true"
  shift
fi

NO_GIT="false"
if [[ "${1:-}" == "--no-git" ]]; then
  NO_GIT="true"
  shift
fi
# -----------------------------------------------------------------------------


TOOLING_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKELETON_GM="$TOOLING_ROOT/skeleton-gm"
SKELETON_PUBLIC="$TOOLING_ROOT/skeleton-public"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "ERROR: '$1' is required but not installed." >&2
    exit 1
  }
}

ensure_gh_auth() {
  if gh auth status >/dev/null 2>&1; then
    echo "GitHub CLI already authenticated."
    return 0
  fi
  echo "GitHub CLI is not authenticated."
  echo "Launching: gh auth login"
  gh auth login
  if ! gh auth status >/dev/null 2>&1; then
    echo "ERROR: GitHub authentication failed or was cancelled." >&2
    exit 1
  fi
  echo "GitHub CLI authenticated."
}

prompt() {
  local var="$1"
  local msg="$2"
  local def="${3:-}"
  local val=""
  if [[ -n "$def" ]]; then
    read -r -p "$msg [$def]: " val
    val="${val:-$def}"
  else
    read -r -p "$msg: " val
  fi
  printf -v "$var" "%s" "$val"
}

wire_public_repo_name() {
  local gm_path="$1"
  local public_repo="$2"

  python3 - "$gm_path" "$public_repo" <<'PY'
import sys
from pathlib import Path

gm_path = Path(sys.argv[1])
public_repo = sys.argv[2]

for p in gm_path.rglob("*"):
    if p.is_file() and p.suffix in {".sh", ".md"}:
        txt = p.read_text(encoding="utf-8")
        txt = txt.replace("__PUBLIC_REPO_NAME__", public_repo)
        p.write_text(txt, encoding="utf-8")
PY
}

main() {
  require_cmd git
  require_cmd python3
  require_cmd gh

  ensure_gh_auth

  local gh_user
  gh_user="$(gh api user -q .login 2>/dev/null || true)"
  if [[ -z "$gh_user" ]]; then
    echo "ERROR: Could not determine GitHub username via gh." >&2
    exit 1
  fi

  local campaign owner base_dir
  prompt campaign "Campaign name (kebab-case recommended, e.g. fey-roads)" ""
  [[ -z "$campaign" ]] && { echo "ERROR: campaign name cannot be empty." >&2; exit 1; }

  prompt owner "GitHub owner (user or org)" "$gh_user"
  prompt base_dir "Local parent directory to create repos in" "$(pwd)"

  local gm_repo="${campaign}-gm"
  local public_repo="${campaign}-public"

  local gm_path="$base_dir/$gm_repo"
  local public_path="$base_dir/$public_repo"

  if [[ -e "$gm_path" || -e "$public_path" ]]; then
    echo "ERROR: Target folder already exists:" >&2
    [[ -e "$gm_path" ]] && echo " - $gm_path" >&2
    [[ -e "$public_path" ]] && echo " - $public_path" >&2
    exit 1
  fi

  echo
  echo "== Creating local repos =="
  mkdir -p "$gm_path" "$public_path"
  cp -R "$SKELETON_GM/." "$gm_path/"
  cp -R "$SKELETON_PUBLIC/." "$public_path/"

  echo "Wiring defaults (public repo name) into GM repo..."
  wire_public_repo_name "$gm_path" "$public_repo"

  echo
  if [[ "$NO_GIT" == "true" ]]; then
    echo "== --no-git: Skipping git init/commit =="
  else
    echo "== Initializing git repos =="
    (
      cd "$gm_path"
      git init
      git config core.hooksPath .githooks
      git add .
      SKIP_MD_LINT=1 git commit -m "Bootstrap GM campaign repo"
    )
    (
      cd "$public_path"
      git init
      git config core.hooksPath .githooks
      git add .
      SKIP_MD_LINT=1 git commit -m "Bootstrap public player repo"
    )
  fi

  echo
  echo "== Creating GitHub repos and pushing =="
  echo "GM (private):    $owner/$gm_repo"
  echo "Public (public): $owner/$public_repo"
  echo

  
if [[ "$PUSH_TO_GH" == "true" ]]; then
  if [[ "$NO_GIT" == "true" ]]; then
    echo "ERROR: --push requires git repos. Remove --no-git." >&2
    exit 1
  fi
  echo "== Creating GitHub repos and pushing =="
  ( cd "$gm_path" && gh repo create "$owner/$gm_repo" --private --source . --remote origin --push )
  ( cd "$public_path" && gh repo create "$owner/$public_repo" --public --source . --remote origin --push )
else
  echo "== DRY RUN: GitHub push skipped =="
  echo "To publish later, run:"
  echo "  gh repo create \"$owner/$gm_repo\" --private --source \"$gm_path\" --remote origin --push"
  echo "  gh repo create \"$owner/$public_repo\" --public --source \"$public_path\" --remote origin --push"
fi


  echo
  echo "== Done =="
  echo "Local GM repo:      $gm_path"
  echo "Local Public repo:  $public_path"
  echo
  echo "Next: from the GM repo, export + compile in one go:"
  echo "  cd \"$gm_path\""
  echo "  PUBLIC_REPO_PATH=\"../$public_repo\" ./scripts/release.sh"
}

main "$@"
