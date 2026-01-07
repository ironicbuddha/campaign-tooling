# AGENTS.md — GM Campaign Repo (Source of Truth)

This repository is the **authoritative master source** for a D&D campaign.
It contains canon, drafts, contradictions, secrets, and future intent.

The public/player repo is a **derived artifact** built from this repo.
Nothing here is player-facing unless it is explicitly marked.

## One rule above all others
**If it is not inside a PUBLIC block, it is NOT public.**

Assume everything else is GM-only.

---

## What this repo is
- A **toolchain-backed authoring system**
- Optimized for rapid iteration, revision, and contradiction
- Designed to safely export player-facing material without spoilers

This is not a wiki.  
This is not a lore dump.  
This is **source code**.

---

## Structure (do not fight it)
- `items/` — all world content (one concept per file)
  - races, factions, institutions, locations, environments
  - monsters, magic, economy, trade, materials
  - quests live in `items/quests/`
  - campaign intent lives in `items/meta/`
  - `_world_state.md` is the canonical snapshot
- `templates/` — approved starting points for new content
- `scripts/` — authoring + publishing tools (do not bypass)

Prefer **many small files** over god-docs.  
Single responsibility applies to lore too.

---

## PUBLIC vs PRIVATE (non-negotiable)

Player-safe text **must** live inside:

<!-- PUBLIC_START -->
player-facing content
<!-- PUBLIC_END -->

GM-only truth **must** live inside:

<!-- PRIVATE_START -->
spoilers, secrets, timelines, mechanics
<!-- PRIVATE_END -->

### Enforcement
- Export scripts **only extract PUBLIC blocks**
- Unbalanced markers are errors
- If you are unsure whether players should know something, it goes PRIVATE

When in doubt, **withhold**.

---

## Metaphysical constants (do not violate)
These are load-bearing assumptions of the setting.

- Time is **not universal**. Consensus time exists; Fey time does not.
- Magic is **finite, refinable, and corruptible**. It has economic consequences.
- Gods are **not omnipotent** and may be constrained, absent, or unreliable.
- Resurrection is **rare, conditional, or impossible** depending on context.
- Travel is dangerous:
  - the sea is unstable (three moons, monsters)
  - the central wilds are ungovernable
  - the Fey Roads distort causality
- Power always creates second-order effects.

Any content that contradicts these must do so **intentionally** and be flagged in PRIVATE.

---

## Things that do NOT exist (blacklist)
Do not introduce these unless explicitly instructed:

- benevolent, omnipresent gods who solve problems
- cheap or consequence-free resurrection
- universal literacy or perfect record keeping
- safe, fast, routine long-distance travel
- absolute moral clarity
- stable borders with total control
- magic that scales infinitely without cost
- prophecy that is clear, reliable, or comforting

If it removes tension, it probably doesn’t belong.

---

## Authoring rules (humans and AI)
1. Never leak PRIVATE content into PUBLIC.
2. Never edit generated files in the public repo.
3. Keep each file focused on one idea.
4. Frontmatter discipline:
   - `id` = filename slug
   - `title` = human-readable
   - `type` = faction / quest / location / etc.
   - `status` = draft | canon
5. Contradictions are allowed here. Resolve them later.
6. Ambiguity is a feature, not a bug.

---

## Quests (pay attention)
Quests are **situations**, not stories.

- PUBLIC:
  - briefing
  - known facts
  - rumors
  - stated objective
  - things the party can reasonably discover
- PRIVATE:
  - what is actually happening
  - antagonistic forces
  - timelines if ignored
  - secrets and false assumptions
  - branching consequences

If a quest can be “solved” by reading the PUBLIC section, it is badly written.

---

## Publishing pipeline (do not improvise)
From this repo:

PUBLIC_REPO_PATH="../<campaign>-public" ./scripts/release.sh

This:
- exports PUBLIC blocks into the public repo
- triggers compilation into player guides (Markdown + optional PDF)

The public repo is **output**.  
This repo is **truth**.

---

## How AI agents should behave here
- Treat this repo as **source code**
- Be conservative with PUBLIC knowledge
- Default to PRIVATE when uncertain
- Preserve tone, metaphysics, and constraints
- Optimize for playability, not completeness
- Introduce pressure, trade-offs, and consequences

Your job is not to finish the world.  
Your job is to make it **dangerous to misunderstand**.

---

## Intent
This toolchain exists to:
- think faster than typing allows
- separate knowledge safely
- evolve a campaign without retcon chaos
- let players discover truth at the table, not in a document

If something feels neat, clean, or resolved — look again.
