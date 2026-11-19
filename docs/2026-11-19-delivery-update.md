# Version 2026.11.19.2 — delivery spacing

The first Father Christmas visit is due at 5:00. Subsequent visits retain their 5–8 minute interval from the previous visit's start, and each visit still delivers 8–12 presents.

Previously, a cart that stopped could repeatedly drop presents in one small area. Collection removed the only record of an earlier drop, so immediately collecting gifts could also allow the same location to be reused. Delivery now remembers every successful site for the entire visit and checks the final position returned by the engine. Drops are at least 6–9 seconds apart and separated by a distance scaled to the map, bounded to 24–80 world units. Existing unopened presents count towards spacing too.

If a native route makes no delivery progress for 20 seconds, the convoy relocates to randomly sampled clear land and resumes its route with the same remaining gift budget. The old convoy is removed first. There remains exactly one Santa and nine reindeer, all neutral, invulnerable and unselectable. Crowded or unsuitable terrain uses bounded retries.

The existing per-player military, economy and population fixes are unchanged. Their settings use native lobby slots and military settings are loaded independently from economy settings. See the [previous validation record](2026-11-19-update.md) for the live host/population and Player 2 boost checks. More Advanced Game Settings remains at 2026.11.19.1.

## Verification

- All ten Yuletide test scripts and both shared More Advanced Game Settings tests passed.
- The new Lua regression checks cover the 300-second first visit, a completely immobile convoy, immediate gift collection, twelve separated delivery sites, engine-adjusted positions, bounded recovery on blocked maps, neutral ownership through recovery, and one convoy at a time.
- Native Content Editor release build: zero errors and zero warnings. Archive SHA256: `cab9373b743f24fd9eb8e196abec7fd074e9678b59c424c7043edc57c27fbcf1`.

## Native match verification

AoE IV 17.0.12303, Large MegaRandom, normal unaccelerated game time: no gifts at 4:55; first successful drop exactly at 300 seconds. The visit selected eight gifts, delivered all eight, and had ended by 374 seconds. The nearest pair was over 81 world units apart against an 80-unit requirement. All ten convoy entities were world-owned on every sampled tick. No recovery relocation was needed on this route; its blocked-route behavior is covered by the regression tests.

The eight recorded sites (rounded down) were `(348,238)`, `(203,166)`, `(53,221)`, `(267,101)`, `(134,213)`, `(-22,312)`, `(-90,256)`, `(-37,91)`. The native cart and running reindeer rendered during the visit and despawned at completion. A temporary readout and map reveal were used to measure delivery; neither is in the release archive. The diagnostic was built with the official editor and differs from the production archive only by appended observation code in the main Christmas script.

This is not exhaustive multiplayer, save/load or every-map validation.

## Publication

Published through AoE IV on 19 November as [catalogue entry 593826](https://www.ageofempires.com/mods/details/593826/), by TypeEkcyall. The live description starts with `Version 2026.11.19.2`. After moving the publishing copy outside the game folders, a fresh in-game subscription downloaded `44e10f989d148a22633b0dc1c83a7d67680256b8f012b7a9161260fae81e3108.sga`; its SHA256 exactly matches the native production build above.

The publisher again created a new entry instead of associating the build with the existing entry. Superseded entry 593823 was deleted only after the replacement download was verified, as authorised by the owner. The remaining owned catalogue listings are Yuletide 593826, More Advanced Game Settings 593824, and the separate Empowered Queen 517774. Existing Yuletide subscribers need the new entry; selecting Yuletide as both Game Mode and Tuning Pack is still required.
