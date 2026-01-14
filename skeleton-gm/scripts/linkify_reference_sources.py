#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


REF_CODE_RE = re.compile(r"(?<!\[)`(?P<path>references/[^`]+)`")


def _rel_link(from_file: Path, target: Path) -> str:
    rel = os.path.relpath(target.as_posix(), start=from_file.parent.as_posix())
    return rel.replace(os.sep, "/")


def _linkify(from_file: Path, ref_text: str) -> str | None:
    target = Path(ref_text)
    if not target.exists():
        return None
    href = _rel_link(from_file, target)
    return f"[`{ref_text}`]({href})"


def linkify_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    in_front_matter = False
    front_matter_done = False
    in_fence = False
    in_private_block = False

    out: list[str] = []

    def repl(m: re.Match[str]) -> str:
        ref_text = m.group("path")
        replacement = _linkify(from_file=path, ref_text=ref_text)
        return replacement or m.group(0)

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

        if stripped == "<!-- PRIVATE_START -->":
            in_private_block = True
            out.append(line)
            continue

        if stripped == "<!-- PRIVATE_END -->":
            in_private_block = False
            out.append(line)
            continue

        if not in_private_block:
            out.append(line)
            continue

        out.append(REF_CODE_RE.sub(repl, line))

    updated = "".join(out)
    if updated == original:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert backticked `references/...` paths in items/*.md into relative markdown links."
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
        if args.dry_run:
            original = md.read_text(encoding="utf-8")
            would_change = REF_CODE_RE.search(original) is not None
            if would_change:
                # Cheap filter; verify by running full transform in-memory
                temp = md.read_text(encoding="utf-8")
                before = temp
                # Reuse linkify_file logic by simulating write
                # (duplicated minimal work to keep dry-run cheap and safe)
                lines = before.splitlines(keepends=True)
                in_front_matter = False
                front_matter_done = False
                in_fence = False
                in_private_block = False
                out: list[str] = []

                def repl(m: re.Match[str]) -> str:
                    ref_text = m.group("path")
                    replacement = _linkify(from_file=md, ref_text=ref_text)
                    return replacement or m.group(0)

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
                    if stripped == "<!-- PRIVATE_START -->":
                        in_private_block = True
                        out.append(line)
                        continue
                    if stripped == "<!-- PRIVATE_END -->":
                        in_private_block = False
                        out.append(line)
                        continue
                    if not in_private_block:
                        out.append(line)
                        continue
                    out.append(REF_CODE_RE.sub(repl, line))

                if "".join(out) != before:
                    changed.append(md)
            continue

        if linkify_file(md):
            changed.append(md)

    for p in changed:
        print(p.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
