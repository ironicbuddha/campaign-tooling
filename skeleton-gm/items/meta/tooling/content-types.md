---
id: tooling-content-types
title: Content Types (Type Variants)
type: meta
status: draft
---

<!-- PRIVATE_START -->
Decision: keep “new content types” as `type:` variants in frontmatter, not as new top-level folders under `items/`.

Source seed list: `references/qualihut-dungeon-master-tooling-ideas.md` (content-type enumeration).

## How to use `type:` variants
- Put the file in the closest existing folder by subject (e.g., lore about magic in `items/magic/`, an organization in `items/institutions/`).
- Use `type:` to declare the variant shape (e.g., `type: clue`, `type: encounter`, `type: hazard`).
- Keep everything PRIVATE by default; only add PUBLIC blocks when explicitly player-safe.

## Candidate variants to support
Geography granularity:
- `type: region` / `type: zone`
- `type: settlement` (location subtype)
- `type: dungeon` / `type: site`
- `type: room` / `type: area`
- `type: poi`

Play-moment objects:
- `type: scene`
- `type: encounter` (situation)
- `type: combat-setup`
- `type: negotiation` / `type: social-exchange`
- `type: chase` / `type: skill-challenge`

Mechanics/state tracking:
- `type: clock` / `type: front`
- `type: threat`
- `type: hazard`
- `type: condition`
- `type: resource-node`

Information objects:
- `type: clue`
- `type: rumour`
- `type: secret`
- `type: omen` / `type: vision` / `type: prophecy`
- `type: lore-entry`

Tangible things:
- `type: item`
- `type: artifact` / `type: relic`
- `type: consumable`
- `type: treasure-parcel`

Assets/handouts:
- `type: map-asset`
- `type: portrait-asset`
- `type: handout`
- `type: sigil` / `type: symbol`

Travel/downtime:
- `type: route`
- `type: travel-day`
- `type: downtime-activity`
- `type: service` / `type: vendor`

Campaign ops:
- `type: session-recap`
- `type: hook` / `type: quest-lead`
- `type: consequence`
- `type: player-myth`

## Practical mapping (recommended defaults)
Until we create dedicated folders, suggested “closest home” defaults:
- `clue` / `rumour` / `handout` → `items/briefings/` (or wherever you keep player-facing artifacts-in-waiting)
- `clock` / `front` / `consequence` / `player-myth` → `items/meta/` (campaign operations)
- `hazard` / `condition` → whichever domain owns it (often `items/magic/`, sometimes `items/locations/`)
- `item` / `artifact` → `items/items/` (create later) or `items/magic/` if it’s primarily magical

Open question for later: whether to introduce a small number of new folders (`items/encounters/`, `items/clues/`, `items/handouts/`) once volume justifies it.
<!-- PRIVATE_END -->

