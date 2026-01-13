---
id: tooling-dm-table-app-ideas
title: DM Table Tooling Ideas (Future)
type: meta
status: draft
---

<!-- PRIVATE_START -->
Source material: extracted and normalized from:
- `references/qualihut-dungeon-master-tooling-ideas.md`

This file is intentionally “future tooling” and is not implemented in this repo.

## Table-side modes (device roles)
Suggested view separation:
- Laptop: DM dashboard (full control).
- iPad (DM remote): touch-friendly controls (big buttons, no typing).
- iPad (player display): player-safe visuals and revealed information only.

Suggested modes:
- Oracle mode (omens, random events, prophecy fragments).
- War room mode (factions, clocks, off-screen moves).
- Diegetic display mode (player-facing images/handouts only).
- Black box mode (private DM notes, consequences, reminders).

## Minimal architecture sketch
Run a local web app on the laptop:
- Serves three routes: `/dm`, `/remote`, `/display`.
- Uses WebSockets for real-time state updates to iPads.
- Stores state in SQLite or a JSON file.
- Enforces simple auth (DM token vs public token).

## “Single state object” sync model
Keep campaign state as a single object that can be broadcast/diffed:
- scene (title, text, display image)
- map (fog mask, pings)
- encounter (active, posture, participants)
- clocks (threat/alert tracks)

Design rule from references: agents/tools propose changes; the DM applies them (no autonomous mutation).
<!-- PRIVATE_END -->

