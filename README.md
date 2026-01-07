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
