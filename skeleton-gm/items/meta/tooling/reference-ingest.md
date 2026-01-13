---
id: tooling-reference-ingest
title: Reference Ingest (Conversation Records)
type: meta
status: draft
---

<!-- PRIVATE_START -->
Source material: extracted and normalized from:
- `references/qualihut-exporting-chatgpt-projects.md`
- `references/qualihut-project-summary-overview.md`

## Intent
Conversation records under `references/` are raw material. They may drift off-topic; extraction should pull canon-relevant content into `items/` while keeping everything PRIVATE unless explicitly marked safe later.

## Getting conversation records out of ChatGPT (summary)
From the reference notes, practical options:
- Full account export (JSON) for backup; requires post-processing.
- Per-conversation “Print → Save as PDF” for curated threads.
- Automation (Playwright/Puppeteer) for large-scale scraping (fragile).

In this repo, the working assumption is that PDFs (and their parsed Markdown) are stored in `references/`.

## Parsing PDFs to Markdown (current script)
`scripts/parse_references.py` converts PDFs into PRIVATE Markdown and extracts images.

Defaults:
- Input: `references/*.pdf`
- Output: `references/parsed/` (Markdown + `<slug>_assets/` images)

Example:
- `python3 scripts/parse_references.py --out-dir references`

Notes:
- The parser escapes visibility markers so the output doesn’t accidentally create export blocks.
- Images are extracted per-page (and pages can be rendered when needed).

## Human extraction workflow (canonicalization)
1. Read a reference Markdown file in `references/`.
2. For each actionable concept, either:
   - merge into the closest existing item (preferred), or
   - create a new item in `items/<type>/`, or
   - if it doesn’t fit cleanly, create an idea file in `items/meta/idea-box/`.
3. Add/append a PRIVATE `## Extracted From References` section to the target item(s).
4. If you touch a published item, set it to `status: draft`.
5. Update `items/meta/_reference_ingest_log.md` with what was created/updated.
<!-- PRIVATE_END -->

