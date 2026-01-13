#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _strip_frontmatter(md: str) -> tuple[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", md, re.S)
    if not m:
        return "", md
    return m.group(1), m.group(2)


def _extract_title(frontmatter: str, body: str, fallback: str) -> str:
    m_title = re.search(r"^title:\s*(.+)\s*$", frontmatter, re.M)
    if m_title:
        return m_title.group(1).strip()
    m_h1 = re.search(r"^#\s+(.+)$", body, re.M)
    if m_h1:
        return m_h1.group(1).strip()
    return fallback


def _strip_first_h1(body: str) -> str:
    return re.sub(r"^#\s+.*\n", "", body, count=1).strip()


def _render_gm_body(body: str) -> str:
    lines: list[str] = []
    for line in body.splitlines():
        if re.search(r"<!--\s*PUBLIC_START\s*-->", line):
            lines.append("## Player-Safe (PUBLIC)")
            lines.append("")
            continue
        if re.search(r"<!--\s*PUBLIC_END\s*-->", line):
            lines.append("")
            continue
        if re.search(r"<!--\s*PRIVATE_START\s*-->", line):
            lines.append("## GM-Only (PRIVATE)")
            lines.append("")
            continue
        if re.search(r"<!--\s*PRIVATE_END\s*-->", line):
            lines.append("")
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def _humanize_section(section: str) -> str:
    return section.replace("-", " ").replace("_", " ").title()


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate an mdBook source tree for the GM repo.")
    ap.add_argument("--root", required=True, help="Repo root directory.")
    ap.add_argument("--items-dir", required=True, help="Items directory (e.g., ./items).")
    ap.add_argument("--out-src", required=True, help="Output directory for mdBook sources.")
    ap.add_argument("--title", required=True, help="Book title.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    items_dir = Path(args.items_dir).resolve()
    out_src = Path(args.out_src).resolve()
    src_dir = out_src / "src"

    if out_src.exists():
        shutil.rmtree(out_src)
    src_dir.mkdir(parents=True, exist_ok=True)

    book_toml = "\n".join(
        [
            "[book]",
            f'title = "{args.title}"',
            "authors = []",
            "language = \"en\"",
            "",
            "[output.html]",
            "default-theme = \"navy\"",
            "",
        ]
    )
    _write_text(out_src / "book.toml", book_toml)

    files = sorted(items_dir.rglob("*.md"))

    pages: list[tuple[str, str, str]] = []
    for f in files:
        rel = f.relative_to(root).as_posix()
        dest = src_dir / rel

        raw = _read_text(f)
        front, body = _strip_frontmatter(raw)
        title = _extract_title(front, body, fallback=f.stem)
        body = _strip_first_h1(body)
        body = _render_gm_body(body)

        page = "\n".join(
            [
                f"# {title}",
                "",
                f"_Source: `{rel}`_",
                "",
                body,
                "",
            ]
        ).rstrip() + "\n"

        _write_text(dest, page)

        parts = rel.split("/")
        section = "Misc"
        if len(parts) >= 2 and parts[0] == "items":
            section = parts[1]
        pages.append((section, rel, title))

    _write_text(
        src_dir / "index.md",
        "\n".join(
            [
                f"# {args.title}",
                "",
                "This site is generated from the GM source repo.",
                "",
                "Visibility markers are rendered as explicit PUBLIC/PRIVATE sections.",
                "",
            ]
        ),
    )

    summary_lines: list[str] = ["# Summary", "", "- [Home](index.md)"]

    by_section: dict[str, list[tuple[str, str]]] = {}
    for section, rel, title in pages:
        by_section.setdefault(section, []).append((rel, title))

    sections_dir = src_dir / "sections"
    for section in sorted(by_section.keys()):
        section_title = _humanize_section(section)
        section_page = f"sections/{section}.md"
        summary_lines.append(f"- [{section_title}]({section_page})")

        items = sorted(by_section[section], key=lambda t: t[1].lower())
        for rel, title in items:
            summary_lines.append(f"  - [{title}]({rel})")

        section_md = "\n".join(
            [f"# {section_title}", "", "## Pages", ""]
            + [f"- [{title}](../{rel})" for rel, title in items]
            + [""]
        )
        _write_text(sections_dir / f"{section}.md", section_md)

    _write_text(src_dir / "SUMMARY.md", "\n".join(summary_lines).rstrip() + "\n")

    print(f"Wrote mdBook sources: {out_src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

