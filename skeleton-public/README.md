# Player-Facing Campaign Notes (Public)

This repository contains **player-safe** materials only.

## Build guides
```bash
./scripts/compile_guides.sh
```
If `pandoc` is installed, PDFs will also be generated.

## Markdown lint on commit
- Hooks live in `.githooks`; installer wires `core.hooksPath`.
- Install the linter once: `npm install -g markdownlint-cli`
- To lint staged Markdown manually: `./scripts/lint_markdown.sh`

## CI build (GitHub Actions)
A workflow builds the guides on push and uploads `docs/*.md` and `docs/*.pdf` as workflow artifacts.

## Shell compatibility
Scripts are compatible with macOS default bash (3.2).
