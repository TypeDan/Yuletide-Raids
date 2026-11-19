# Version 2026.11.19.3 — map-wide random presents

Presents now appear at independently sampled random land locations across the whole map. Santa's position and path do not determine those locations. This removes the trail that allowed a player following his convoy to collect a disproportionate number of presents.

The previous release increased spacing but still dropped gifts beside the cart. This release removes that connection, as well as the delivery-driven convoy relocation. Santa and his nine reindeer continue their neutral visual route while presents appear elsewhere. Random placement can still favour an area by chance; it does not reserve equal rewards for each player or team.

Candidate locations use the simulation's `World_GetRand`, reject water and nearby buildings, and preserve map-scaled spacing (24–80 world units) from unopened presents and every prior gift site in the visit, including collected gifts. The engine-resolved final position is checked too. Sampling is bounded and failed placement retries without spending the gift budget.

First arrival remains 5:00, with 8–12 successful gifts per visit and at least 6–9 seconds between gifts. Golden-token probability remains 40%; ordinary reward weights, team gold sharing, boosts and purchases are unchanged. More Advanced Game Settings remains 2026.11.19.1.

## Automated and build checks

- Delivery regression: the same RNG seed produces exactly the same twelve gift positions and times for an immobile cart and a cart taking an entirely different path. Neither scenario respawns the convoy.
- Pairwise gift spacing remains enforced after immediate collection; engine-adjusted invalid positions are rejected.
- Count/capacity regression: all targets from 8 through 12, bounded failed-placement retries and 40 golden outcomes out of 100 possible rolls pass.
- Route regression: player count/order do not bias map sampling; land sampling covers all four map quadrants and rejects water safely.
- Native Content Editor production build: zero errors and warnings. SHA256: `585728b0ef32b9e48315c35ec1b81b212fbac21c25a9f3d459671a78adb1434e`.

## Live-match verification

A normal-speed Large MegaRandom match produced its first gift at game second 300 and delivered all nine randomly selected gifts before ending the visit. The closest pair was 95 world units apart, above the required 80 on this map. Gifts appeared 84–512 world units from Santa at their respective drop times, across all four map quadrants. All ten convoy members remained neutral throughout, with no respawns.

The observation-only test archive added measurements to the main Christmas script without changing gameplay. Its evidence screenshot is retained outside the release. The arrival notification was subsequently corrected from “along his route” to “scattered across the map”; the final production archive was rebuilt without test code.

## Publication verification

The game published catalogue entry [593827](https://www.ageofempires.com/mods/details/593827/) under TypeEkcyall, with version 2026.11.19.3 in its description. A fresh server download matches the final production archive's SHA256 above. The superseded entry 593826 was removed after that verification. Existing subscribers must subscribe to the replacement entry. The latest local publisher copy is retained but disabled; only the published subscription is enabled for play.
