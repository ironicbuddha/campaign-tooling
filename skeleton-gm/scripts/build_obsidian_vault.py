#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)
STATUS_RE = re.compile(r"^status:\s*(.+)\s*$", re.M)

PUBLIC_START_RE = re.compile(r"<!--\s*PUBLIC_START\s*-->")
PUBLIC_END_RE = re.compile(r"<!--\s*PUBLIC_END\s*-->")

PRIVATE_START_RE = re.compile(r"<!--\s*PRIVATE_START\s*-->")
PRIVATE_END_RE = re.compile(r"<!--\s*PRIVATE_END\s*-->")

LINK_RE = re.compile(r"\[[^\]]*\]\((?P<href>[^)]+)\)")


@dataclass(frozen=True)
class ParsedMarkdown:
    front_matter: str
    body: str


def parse_markdown(text: str) -> ParsedMarkdown:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return ParsedMarkdown(front_matter="", body=text)
    return ParsedMarkdown(front_matter=m.group(1).strip(), body=m.group(2))


def get_status(front_matter: str) -> str:
    m = STATUS_RE.search(front_matter)
    return (m.group(1).strip() if m else "").lower()


def validate_markers(path: Path, text: str) -> None:
    def count(pattern: re.Pattern[str]) -> int:
        return len(pattern.findall(text))

    for start, end in [
        (PUBLIC_START_RE, PUBLIC_END_RE),
        (PRIVATE_START_RE, PRIVATE_END_RE),
    ]:
        if count(start) != count(end):
            raise ValueError(
                f"Unbalanced visibility markers in {path.as_posix()}: {start.pattern} != {end.pattern}"
            )


def extract_public(text: str) -> str:
    parsed = parse_markdown(text)
    body = parsed.body

    in_pub = False
    out_lines: list[str] = []
    for line in body.splitlines():
        if PUBLIC_START_RE.search(line):
            in_pub = True
            continue
        if PUBLIC_END_RE.search(line):
            in_pub = False
            continue
        if in_pub:
            out_lines.append(line)

    public_body = "\n".join(out_lines).strip()

    out = ""
    if parsed.front_matter.strip():
        out += "---\n" + parsed.front_matter.strip() + "\n---\n\n"
    out += public_body + ("\n" if public_body else "")
    return out


def safe_clean_dir(out_dir: Path) -> None:
    if not out_dir.exists():
        return
    # Guardrail: only allow cleaning under dist/
    if "dist" not in out_dir.parts:
        raise SystemExit(f"Refusing to delete non-dist directory: {out_dir.as_posix()}")
    shutil.rmtree(out_dir)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_tree_filtered(src: Path, dst: Path, *, ignore_exts: set[str]) -> None:
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        if path.name in {".DS_Store", "Thumbs.db"}:
            continue
        if path.suffix.lower() in ignore_exts:
            continue
        rel = path.relative_to(src)
        out_path = dst / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, out_path)


def build_index(vault_root: Path, title: str, md_files: list[Path]) -> None:
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("Open this vault in Obsidian, then start here.")
    lines.append("")
    lines.append("## Files")
    lines.append("")

    for p in sorted(md_files):
        rel = p.relative_to(vault_root).as_posix()
        lines.append(f"- [[{rel}]]")

    write_text(vault_root / "_INDEX.md", "\n".join(lines) + "\n")


def find_markdown_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if p.is_file()]


def is_relative_md_link(href: str) -> bool:
    href = href.strip()
    if href.startswith(("http://", "https://", "mailto:")):
        return False
    if href.startswith("#"):
        return False
    return ".md" in href


def resolve_link(from_file: Path, href: str) -> Path:
    href = href.split("#", 1)[0].split("?", 1)[0]
    # Obsidian tolerates spaces; keep as-is.
    return (from_file.parent / href).resolve()


def write_missing_link_report(vault_root: Path) -> None:
    report: dict[str, set[str]] = {}
    for md in vault_root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            href = m.group("href").strip()
            if not is_relative_md_link(href):
                continue
            target = resolve_link(md, href)
            if not target.exists():
                rel_src = md.relative_to(vault_root).as_posix()
                report.setdefault(rel_src, set()).add(href)

    if not report:
        return

    lines: list[str] = []
    lines.append("# Missing Links Report")
    lines.append("")
    lines.append("Links below point to files that are not present in this vault.")
    lines.append("This is expected when previewing `status: published` only.")
    lines.append("")
    for src in sorted(report.keys()):
        lines.append(f"## {src}")
        lines.append("")
        for href in sorted(report[src]):
            lines.append(f"- `{href}`")
        lines.append("")

    write_text(vault_root / "_MISSING_LINKS.md", "\n".join(lines))


def build_gm_vault(*, out_dir: Path, clean: bool) -> None:
    if clean:
        safe_clean_dir(out_dir)
    (out_dir / "items").mkdir(parents=True, exist_ok=True)

    # Copy items verbatim
    copy_tree_filtered(Path("items"), out_dir / "items", ignore_exts=set())

    # Copy references (markdown + assets), but skip PDFs by default to keep it light.
    copy_tree_filtered(Path("references"), out_dir / "references", ignore_exts={".pdf"})

    md_files = find_markdown_files(out_dir)
    build_index(out_dir, "GM Vault", md_files)


def build_player_preview_vault(*, out_dir: Path, clean: bool, include_all_statuses: bool) -> None:
    if clean:
        safe_clean_dir(out_dir)
    (out_dir / "items").mkdir(parents=True, exist_ok=True)

    for src in Path("items").rglob("*.md"):
        text = src.read_text(encoding="utf-8")
        validate_markers(src, text)
        parsed = parse_markdown(text)
        status = get_status(parsed.front_matter)
        if not include_all_statuses and status != "published":
            continue

        rel = src.relative_to(Path("items"))
        out_path = out_dir / "items" / rel
        write_text(out_path, extract_public(text))

    md_files = find_markdown_files(out_dir)
    build_index(out_dir, "Player Preview (PUBLIC Blocks)", md_files)
    write_missing_link_report(out_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Obsidian vaults for GM browsing and player-safe preview.")
    parser.add_argument(
        "--out-root",
        default="dist",
        help="Output root directory (default: dist).",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not delete existing output dirs before writing.",
    )
    parser.add_argument(
        "--player-include-drafts",
        action="store_true",
        help="Include all item statuses in the player preview (still PUBLIC-only).",
    )

    args = parser.parse_args()
    out_root = Path(args.out_root)
    clean = not args.no_clean

    gm_out = out_root / "obsidian-gm"
    player_out = out_root / "obsidian-player-preview"

    build_gm_vault(out_dir=gm_out, clean=clean)
    build_player_preview_vault(
        out_dir=player_out,
        clean=clean,
        include_all_statuses=bool(args.player_include_drafts),
    )

    print(gm_out.as_posix())
    print(player_out.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
