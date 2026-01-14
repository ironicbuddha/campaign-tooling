#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


CODE_ITEM_REF_RE = re.compile(r"`(?P<path>items/[A-Za-z0-9_./-]+\.md)`")
BARE_ITEM_REF_RE = re.compile(
    r"(?<![`\\w/])(?P<path>items/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.md)(?![\\w/])"
)


def _rel_link(from_file: Path, target: Path) -> str:
    rel = os.path.relpath(target.as_posix(), start=from_file.parent.as_posix())
    return rel.replace(os.sep, "/")


def _linkify_path(from_file: Path, path_text: str) -> str | None:
    target = Path(path_text)
    if not target.exists():
        return None
    href = _rel_link(from_file, target)
    return f"[`{path_text}`]({href})"


def _process_line(from_file: Path, line: str) -> str:
    def replace_code(m: re.Match[str]) -> str:
        path_text = m.group("path")
        replacement = _linkify_path(from_file, path_text)
        return replacement or m.group(0)

    def replace_bare(m: re.Match[str]) -> str:
        path_text = m.group("path")
        replacement = _linkify_path(from_file, path_text)
        return replacement or path_text

    line = CODE_ITEM_REF_RE.sub(replace_code, line)
    line = BARE_ITEM_REF_RE.sub(replace_bare, line)
    return line


def linkify_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    in_front_matter = False
    front_matter_done = False
    in_fence = False

    out: list[str] = []
    for i, line in enumerate(lines):
        stripped = line.strip()

        if i == 0 and stripped == "---":
            in_front_matter = True
            out.append(line)
            continue

        if in_front_matter and stripped == "---":
            in_front_matter = False
            front_matter_done = True
            out.append(line)
            continue

        if not in_front_matter and front_matter_done and stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue

        if in_front_matter or in_fence:
            out.append(line)
            continue

        out.append(_process_line(from_file=path, line=line))

    updated = "".join(out)
    if updated == original:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert `items/...md` references in items/*.md into relative markdown links."
    )
    parser.add_argument(
        "--root",
        default="items",
        help="Directory containing content items (default: items).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would change, without writing.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"Root not found: {root.as_posix()}")

    changed: list[Path] = []
    for md in sorted(root.rglob("*.md")):
        original = md.read_text(encoding="utf-8")
        if args.dry_run:
            updated = []
            lines = original.splitlines(keepends=True)

            in_front_matter = False
            front_matter_done = False
            in_fence = False

            for i, line in enumerate(lines):
                stripped = line.strip()
                if i == 0 and stripped == "---":
                    in_front_matter = True
                    updated.append(line)
                    continue
                if in_front_matter and stripped == "---":
                    in_front_matter = False
                    front_matter_done = True
                    updated.append(line)
                    continue
                if not in_front_matter and front_matter_done and stripped.startswith("```"):
                    in_fence = not in_fence
                    updated.append(line)
                    continue
                if in_front_matter or in_fence:
                    updated.append(line)
                    continue
                updated.append(_process_line(from_file=md, line=line))

            if "".join(updated) != original:
                changed.append(md)
            continue

        if linkify_file(md):
            changed.append(md)

    for p in changed:
        print(p.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
