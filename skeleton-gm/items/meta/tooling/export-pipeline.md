---
id: tooling-export-pipeline
title: Export + Release Pipeline
type: meta
status: draft
---

<!-- PRIVATE_START -->
Source material: extracted and normalized from:
- `references/qualihut-project-summary-overview.md`

## What exists in this repo (today)
Scripts:
- `scripts/export_public_entries.sh` exports player-safe entries into the public repo (one file per item).
- `scripts/release.sh` runs export, runs the public repo compile step, then commits + pushes the public repo.
- `scripts/lint_markdown.sh` is a pre-commit helper (requires `markdownlint`).

Templates:
- `templates/content_item.template.md`
- `templates/quest_item.template.md`

## Export rules (as implemented)
`scripts/export_public_entries.sh`:
- Walks `items/**/*.md`.
- Validates that PUBLIC and PRIVATE markers are balanced.
- Only exports entries where frontmatter contains `status: published`.
- Output path mirrors the GM repo structure under the public repo `content/` directory.
- Exported output includes frontmatter (copied as-is) and only the content inside PUBLIC blocks.

## Public repo location
The public repo location is controlled by `PUBLIC_REPO_PATH` (defaults to `../qualihut-public`).

Manual export:
- `PUBLIC_REPO_PATH="../qualihut-public" ./scripts/export_public_entries.sh`

## Release script behavior (be deliberate)
`scripts/release.sh` will:
1. Export player-safe entries into the public repo.
2. Run `scripts/compile_guides.sh` inside the public repo.
3. `git add -A`, `git commit`, and `git push` in the public repo.

If you want to keep everything draft-only during ingest work, avoid running `scripts/release.sh`.
<!-- PRIVATE_END -->

