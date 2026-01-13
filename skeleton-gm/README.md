# Campaign GM Repo (Private)

Authoring repo with secrets.

## Export + compile (one command)
```bash
PUBLIC_REPO_PATH="../__PUBLIC_REPO_NAME__" ./scripts/release.sh
```

## Markdown lint on commit
- Hooks live in `.githooks`; installer wires `core.hooksPath`.
- Install the linter once: `npm install -g markdownlint-cli`
- To lint staged Markdown manually: `./scripts/lint_markdown.sh`

## Create new items quickly
```bash
./scripts/new_item.sh <type> <slug> "<Title>"
```

## Tooling docs
- Repo conventions, templates, export pipeline, and reference ingest live in `items/meta/tooling/`.
- Reference ingest audit trail: `items/meta/_reference_ingest_log.md`.
- Idea inbox for unallocated fragments: `items/meta/idea-box/`.
