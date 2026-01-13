---
id: reference-ingest-log
title: Reference Ingest Log
type: meta
status: draft
---

<!-- PRIVATE_START -->
Purpose: Track extraction work from `references/` conversation records into canonical `items/` content.

Rules:
- Treat reference material as canon by default, but do not publish it automatically.
- If an existing `status: published` item is touched, set it to `status: draft`.
- When merging extracted material into an existing item, add an explicit `## Extracted From References` section (PRIVATE).
- If new material contradicts existing lore, keep both and add a `## Contradictions / Tensions` section (PRIVATE) pointing to the conflicting item(s).

Log format (one entry per reference file processed):

### YYYY-MM-DD — `references/parsed/<file>.md`
- Created: `items/...`
- Updated: `items/...`
- Idea box: `items/meta/idea-box/<slug>.md`
- Contradictions: (links)

### 2026-01-13 — `references/qualihut-magical-blight-investigation.md`
- Updated: `items/quests/q-magic-blight-monastery.md`

### 2026-01-13 — `references/qualihut-proxy-insurgency-dynamics.md`
- Updated: `items/quests/q-magic-blight-monastery.md`

### 2026-01-13 — `references/qualihut-magic-as-currency.md`
- Updated: `items/quests/q-the-calderon-job.md`

### 2026-01-13 — `references/qualihut-merovingian-symbolism-in-matrix.md`
- Updated: `items/quests/q-the-calderon-job.md`

### 2026-01-13 — `references/qualihut-fey-court-midsummer-revel.md`
- Created: `items/quests/q-fey-court-midsummer-revel.md`

### 2026-01-13 — `references/qualihut-magic-as-currency.md`
- Updated: `items/locations/hochsilvar.md`
- Updated: `items/locations/niederstadt.md`

### 2026-01-13 — `references/qualihut-border-city-of-intrigue.md`
- Updated: `items/locations/valdengratz.md`

### 2026-01-13 — `references/qualihut-magical-blight-investigation.md`
- Created: `items/locations/central-wilds.md`

### 2026-01-13 — `references/qualihut-cave-octopus-monster-guide.md`
- Created: `items/locations/earth-wound.md`

### 2026-01-13 — `references/qualihut-magic-as-currency.md`
- Updated: `items/institutions/banco-valdieri.md`
- Updated: `items/institutions/city-watch.md`
- Updated: `items/institutions/thieves-guilds.md`
- Idea box: `items/meta/idea-box/glass-vault-of-aurelion.md`

### 2026-01-13 — `references/qualihut-game-mastering-highlights.md`
- Updated: `items/institutions/intelligence-bureaus.md`
- Updated: `items/institutions/der-weitblick.md`
- Updated: `items/institutions/der-kronenschild.md`

### 2026-01-13 — `references/qualihut-fey-court-midsummer-revel.md`
- Updated: `items/institutions/thieves-guilds.md`

### 2026-01-13 — `references/qualihut-cult-of-ink-assassins.md`
- Created: `items/institutions/cult-of-ink.md`

### 2026-01-13 — `references/qualihut-medieval-football-culture.md`
- Created: `items/institutions/royal-games.md`

### 2026-01-13 — `references/qualihut-proxy-insurgency-dynamics.md`
- Created: `items/institutions/order-of-transcendent-light.md`

### 2026-01-13 — `references/qualihut-dnd-campaign-idea.md`
- Created: `items/institutions/solar-church.md`

### 2026-01-13 — `references/qualihut-elvish-prophecies-and-power.md`
- Created: `items/institutions/solar-church.md`

### 2026-01-13 — `references/qualihut-border-city-of-intrigue.md`
- Created: `items/institutions/cult-of-ink.md`

### 2026-01-13 — `references/qualihut-lonely-planet-elven-empire.md`
- Updated: `items/institutions/solar-church.md`

### 2026-01-13 — `references/qualihut-magical-blight-investigation.md`
- Created: `items/institutions/imperial-monasteries.md`

### 2026-01-13 — `references/qualihut-proxy-insurgency-dynamics.md`
- Created: `items/institutions/imperial-monasteries.md`

### 2026-01-13 — `references/qualihut-dnd-campaign-idea.md`
- Created: `items/institutions/imperial-monasteries.md`
- Created: `items/institutions/sacrament-administration.md`
- Created: `items/institutions/caretakers-of-sacred-lineage.md`
- Idea box: `items/meta/idea-box/sun-blood.md`

### 2026-01-13 — `references/qualihut-border-city-of-intrigue.md`
- Created: `items/institutions/church-caravans.md`
- Updated: `items/institutions/sacrament-administration.md`
- Idea box: `items/meta/idea-box/border-basilica.md`

### 2026-01-13 — `references/qualihut-elvish-stewardship-of-bloodlines.md`
- Created: `items/institutions/lineage-stewardship.md`

### 2026-01-13 — `references/qualihut-banking-guild-names.md`
- Created: `items/institutions/hochkathedrale-der-ewigen-flamme.md`
- Created: `items/institutions/der-sonnenmarsch.md`

### 2026-01-13 — `references/qualihut-yellow-grass-cultivation.md`
- Updated: `items/institutions/sacrament-administration.md`

### 2026-01-13 — `references/qualihut-magic-as-currency.md`
- Updated: `items/factions/banking-guild.md`
- Updated: `items/factions/ponte-nero.md`

### 2026-01-13 — `references/qualihut-npc-name-generation.md`
- Updated: `items/factions/ventresca-associati.md`

### 2026-01-13 — `references/qualihut-game-mastering-highlights.md`
- Updated: `items/factions/white-stag.md`

### 2026-01-13 — `references/qualihut-proxy-insurgency-dynamics.md`
- Created: `items/factions/southern-union.md`
- Created: `items/factions/tribal-proxies.md`

### 2026-01-13 — `references/qualihut-banking-guild-names.md`
- Created: `items/factions/covenant-of-the-long-road.md`

### 2026-01-13 — `references/qualihut-dnd-campaign-idea.md`
- Created: `items/factions/travelers.md`

### 2026-01-13 — `references/qualihut-tears-of-the-moon.md`
- Idea box: `items/meta/idea-box/techno-barbarians.md`
- Idea box: `items/meta/idea-box/union-tears-of-the-moon-access.md`

### 2026-01-13 — `references/qualihut-npc-name-generation.md`
- Updated: `items/people/npcs/alarich-von-silberhain.md`
- Updated: `items/people/npcs/luciano-ferri.md`
- Updated: `items/people/npcs/aurelian-vaelk.md`
- Updated: `items/people/npcs/edeltraud-isenwald.md`
- Updated: `items/people/npcs/arnhold-vaelric.md`

### 2026-01-13 — `references/qualihut-banking-guild-names.md`
- Updated: `items/people/npcs/guy-roman.md`
- Updated: `items/people/npcs/ensio-silbermark.md`
- Updated: `items/people/npcs/giovanni-valdieri.md`
- Created: `items/people/npcs/althric-von-eichenwald.md`
- Created: `items/people/npcs/berengar-von-dornfels.md`
- Created: `items/people/npcs/lorenzo-di-monteluce.md`
- Created: `items/people/npcs/anselm-von-sonnenfels.md`
- Created: `items/people/npcs/saheera-al-zahret.md`

### 2026-01-13 — `references/qualihut-merovingian-symbolism-in-matrix.md`
- Created: `items/people/npcs/albrika-vael.md`

### 2026-01-13 — `references/qualihut-game-mastering-highlights.md`
- Updated: `items/people/npcs/guy-roman.md`

### 2026-01-13 — `references/qualihut-magic-as-currency.md`
- Updated: `items/magic/refined-magic.md`

### 2026-01-13 — `references/qualihut-fey-road-thresholds.md`
- Updated: `items/magic/refined-magic.md`
- Created: `items/magic/fey-roads.md`

### 2026-01-13 — `references/qualihut-liminal-dimensions-and-madness.md`
- Created: `items/magic/fey-roads.md`

### 2026-01-13 — `references/qualihut-dream-magic-and-astral-travel.md`
- Created: `items/magic/fey-roads.md`

### 2026-01-13 — `references/qualihut-animal-omen-spell.md`
- Created: `items/magic/animal-omen.md`

### 2026-01-13 — `references/qualihut-magical-tattoo-ink.md`
- Created: `items/magic/magical-tattoo-ink.md`

### 2026-01-13 — `references/qualihut-tears-of-the-moon.md`
- Created: `items/magic/tears-of-the-moon.md`

### 2026-01-13 — `references/qualihut-cult-of-the-red-sun.md`
- Created: `items/magic/red-sun-rites.md`

### 2026-01-13 — `references/qualihut-migratory-elvish-tree.md`
- Created: `items/magic/leyline-convergences.md`

### 2026-01-13 — `references/qualihut-yellow-grass-cultivation.md`
- Created: `items/economy/yellow-grass.md`

### 2026-01-13 — `references/qualihut-salt-pork-world-building.md`
- Created: `items/economy/salt-pork.md`

### 2026-01-13 — `references/qualihut-peasant-leather-plant.md`
- Created: `items/economy/hideleaf.md`

### 2026-01-13 — `references/qualihut-salt-pork-world-building.md`
- Created: `items/economy/pottery-and-seals.md`

### 2026-01-13 — `references/qualihut-yellow-grass-cultivation.md`
- Created: `items/economy/insect-spice.md`
- Created: `items/economy/fish-farming.md`

### 2026-01-13 — `references/qualihut-treacherous-sea-navigation.md`
- Created: `items/economy/sea-trade-routes.md`

### 2026-01-13 — `references/qualihut-project-summary-overview.md`
- Created: `items/meta/tooling/_index.md`
- Created: `items/meta/tooling/templates.md`
- Created: `items/meta/tooling/export-pipeline.md`

### 2026-01-13 — `references/qualihut-exporting-chatgpt-projects.md`
- Created: `items/meta/tooling/reference-ingest.md`

### 2026-01-13 — `references/qualihut-dungeon-master-tooling-ideas.md`
- Created: `items/meta/tooling/dm-table-app-ideas.md`
<!-- PRIVATE_END -->
