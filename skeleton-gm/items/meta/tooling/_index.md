---
id: tooling-index
title: Tooling & Templates
type: meta
status: draft
---

<!-- PRIVATE_START -->
Purpose: Collect repo tooling notes (templates, export pipeline, reference ingest) in one place.

Core rules (repo-specific):
- Nothing is player-facing unless it is inside a PUBLIC block.
- Exports only include PUBLIC blocks from entries with `status: published`.
- If a published item is edited, it must be set to `status: draft` (even for small edits).
- When moving material from `references/` into canonical `items/`, add a PRIVATE `## Extracted From References` section.
- If extracted material contradicts existing lore, keep both and add a PRIVATE `## Contradictions / Tensions` section.

Docs:
- Templates: `items/meta/tooling/templates.md`
- Content types: `items/meta/tooling/content-types.md`
- Export + release pipeline: `items/meta/tooling/export-pipeline.md`
- Reference ingest + parsing: `items/meta/tooling/reference-ingest.md`
- Future table tooling ideas (iPads / state sync): `items/meta/tooling/dm-table-app-ideas.md`
<!-- PRIVATE_END -->
