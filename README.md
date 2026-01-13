# Campaign Tooling (3-repo bootstrap)

This repo bootstraps a campaign into **two new GitHub repos**:
- `<campaign>-gm` (private): GM-only authoring + secrets
- `<campaign>-public` (public): player-facing content + compiled guides

## Requirements
- `git`
- `python3`
- GitHub CLI: `gh`
  - macOS: `brew install gh`
- GitHub auth (the installer will prompt if needed):
  - `gh auth login`

## Use
```bash
chmod +x install.sh
./install.sh
```

## Nice wiki site (mdBook)
The generated repos include scripts to produce a nice-looking HTML “wiki/book”:
- Public repo: `./scripts/build_mdbook.sh` (uses a manifest to select content)
- GM repo: `./scripts/build_mdbook.sh` (renders PUBLIC/PRIVATE as explicit sections)

To enable GitHub Pages in the public repo, copy `workflows/pages.yml.template` to `.github/workflows/pages.yml` and push.


## Reference ingest
The generated GM repo includes a lightweight pipeline for importing conversation records into canon:
- Parse PDFs to PRIVATE Markdown: `python3 scripts/parse_references.py` (writes to `references/parsed/` by default).
- Tooling docs and conventions: `items/meta/tooling/`
- Ingest audit trail: `items/meta/_reference_ingest_log.md`
- Idea inbox (one file per fragment): `items/meta/idea-box/`

## After install
From the GM repo:
```bash
PUBLIC_REPO_PATH="../<campaign>-public" ./scripts/release.sh
```

### Dry-run mode (default)
By default, the installer **does not** create or push GitHub repos.

To publish the repos once you're happy:

```bash
./install.sh --push
```

### Pure scaffold mode
Generate folders/files without initializing git:
```bash
./install.sh --no-git
```
