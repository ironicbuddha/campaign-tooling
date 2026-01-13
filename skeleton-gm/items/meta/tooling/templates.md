---
id: tooling-templates
title: Templates (Authoring Model)
type: meta
status: draft
---

<!-- PRIVATE_START -->
Source material: extracted and normalized from:
- `references/qualihut-project-summary-overview.md`
- `references/qualihut-dungeon-master-tooling-ideas.md` (template/schema ideas for “cards”)

## Canon item format (GM repo)
Each canonical item is one Markdown file under `items/` with YAML frontmatter.

The visibility model is inline blocks:
- `&lt;!-- PUBLIC_START --&gt;` … `&lt;!-- PUBLIC_END --&gt;` for player-safe text.
- `&lt;!-- PRIVATE_START --&gt;` … `&lt;!-- PRIVATE_END --&gt;` for GM-only material.

If you accidentally include a visibility marker in normal prose, it will be treated as a real marker by scripts.

## Current repo templates
- Default content item: `templates/content_item.template.md`
- Quest item: `templates/quest_item.template.md`

Recommended workflow:
1. Create items via `scripts/new_item.sh` (pre-fills `id`, `title`, `type`).
2. Keep PUBLIC blocks short, “clean”, and spoiler-free (exporter will copy them verbatim).
3. Keep all extracted/reference-derived truth inside PRIVATE blocks until you explicitly promote to PUBLIC.

## Type variants (no new folders by default)
When you need a new “shape” (e.g., clue, rumour, hazard, encounter, clock), keep it as a `type:` variant in frontmatter rather than creating a new `items/<type>/` folder.
Place the file in the closest existing folder by subject, and use `type:` to declare the variant.
See: `items/meta/tooling/content-types.md`.

## Reference-derived merge convention
When adding material extracted from `references/` into an item:
- Add a PRIVATE section named: `## Extracted From References`
- Include at least one source pointer (file path and/or page numbers if relevant).
- Prefer integrating into the most relevant section, but keep the provenance section as an explicit audit trail.

## Draft vs published (export gating)
Only `status: published` entries are exported to the player repo.
During ingest work, keep new/updated items `status: draft` so nothing leaks by automation.

## Optional “card” schemas (future)
The reference material suggests “card” templates for table utility (NPC, Location, Encounter, Faction, Rumour).
If we decide to operationalize this, keep the schemas as checklists (not rigid structure) and treat them as PRIVATE tooling guidance.
<!-- PRIVATE_END -->
