#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-") or "document"


def _escape_visibility_markers(text: str) -> str:
    return (
        text.replace("<!-- PUBLIC_START -->", "&lt;!-- PUBLIC_START --&gt;")
        .replace("<!-- PUBLIC_END -->", "&lt;!-- PUBLIC_END --&gt;")
        .replace("<!-- PRIVATE_START -->", "&lt;!-- PRIVATE_START --&gt;")
        .replace("<!-- PRIVATE_END -->", "&lt;!-- PRIVATE_END --&gt;")
    )


@dataclass(frozen=True)
class ExtractedImage:
    xref: int
    filename: str
    page_number: int  # 1-based


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _extract_images_for_page(
    doc: fitz.Document,
    page: fitz.Page,
    assets_dir: Path,
    already_extracted: dict[int, str],
    image_counter: list[int],
    page_number: int,
) -> list[ExtractedImage]:
    extracted: list[ExtractedImage] = []
    for img in page.get_images(full=True):
        xref = int(img[0])
        if xref in already_extracted:
            extracted.append(
                ExtractedImage(xref=xref, filename=already_extracted[xref], page_number=page_number)
            )
            continue

        info = doc.extract_image(xref)
        ext = (info.get("ext") or "bin").lower()
        image_counter[0] += 1
        filename = f"img-{image_counter[0]:03d}.{ext}"
        out_path = assets_dir / filename
        _write_bytes(out_path, info["image"])

        already_extracted[xref] = filename
        extracted.append(ExtractedImage(xref=xref, filename=filename, page_number=page_number))
    return extracted


def _render_page_if_needed(page: fitz.Page, assets_dir: Path, page_number: int, dpi: int) -> str:
    pix = page.get_pixmap(dpi=dpi)
    filename = f"page-{page_number:03d}.png"
    out_path = assets_dir / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path.as_posix())
    return filename


def convert_pdf_to_markdown(pdf_path: Path, out_dir: Path, dpi: int, force_render_pages: bool) -> Path:
    doc = fitz.open(pdf_path.as_posix())
    title = pdf_path.stem
    slug = _slugify(title)

    md_path = out_dir / f"{slug}.md"
    assets_dir = out_dir / f"{slug}_assets"

    extracted_by_xref: dict[int, str] = {}
    image_counter = [0]

    converted_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    rel_pdf = pdf_path.as_posix()

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("<!-- PRIVATE_START -->")
    lines.append(f"Source: `{rel_pdf}`")
    lines.append(f"Pages: {doc.page_count}")
    lines.append(f"Converted (UTC): {converted_at}")
    lines.append("")

    for i in range(doc.page_count):
        page_number = i + 1
        page = doc.load_page(i)
        text = page.get_text("text") or ""
        text = text.strip()

        lines.append(f"## Page {page_number}")
        lines.append("")

        page_images = _extract_images_for_page(
            doc=doc,
            page=page,
            assets_dir=assets_dir,
            already_extracted=extracted_by_xref,
            image_counter=image_counter,
            page_number=page_number,
        )

        if text:
            lines.append(_escape_visibility_markers(text))
            lines.append("")
        else:
            lines.append("_No extractable text on this page._")
            lines.append("")

        if page_images:
            for extracted in page_images:
                lines.append(f"![Page {page_number} image](./{assets_dir.name}/{extracted.filename})")
            lines.append("")
        elif force_render_pages or not text:
            rendered = _render_page_if_needed(page, assets_dir=assets_dir, page_number=page_number, dpi=dpi)
            lines.append(f"![Rendered page {page_number}](./{assets_dir.name}/{rendered})")
            lines.append("")

    lines.append("<!-- PRIVATE_END -->")
    lines.append("")

    out_dir.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")

    if assets_dir.exists():
        try:
            next(assets_dir.iterdir())
        except StopIteration:
            assets_dir.rmdir()

    return md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert reference PDFs to PRIVATE markdown with extracted images.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="PDF(s) to convert (defaults to references/*.pdf).",
    )
    parser.add_argument(
        "--out-dir",
        default="references/parsed",
        help="Output directory for markdown + assets.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI when rendering pages (only used when needed).",
    )
    parser.add_argument(
        "--force-render-pages",
        action="store_true",
        help="Render every PDF page to a PNG (can be large).",
    )

    args = parser.parse_args()
    out_dir = Path(args.out_dir)

    if args.paths:
        pdf_paths = [Path(p) for p in args.paths]
    else:
        pdf_paths = sorted(Path("references").glob("*.pdf"))

    pdf_paths = [p for p in pdf_paths if p.exists() and p.suffix.lower() == ".pdf"]
    if not pdf_paths:
        raise SystemExit("No PDFs found. Pass paths or add PDFs under references/.")

    written: list[Path] = []
    for pdf in pdf_paths:
        if os.path.basename(pdf.as_posix()).startswith("~$"):
            continue
        written.append(
            convert_pdf_to_markdown(
                pdf_path=pdf,
                out_dir=out_dir,
                dpi=args.dpi,
                force_render_pages=args.force_render_pages,
            )
        )

    for p in written:
        print(p.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
