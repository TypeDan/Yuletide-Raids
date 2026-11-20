# Version 2026.11.20.3

Presents now appear beside Father Christmas as he travels his random route. Delivery uses his actual native squad position, not a separately sampled map location. Candidate points are three world units from the cart, and the engine-resolved spawn must remain within six world units. If nearby ground is blocked or too close to an earlier gift, the visit waits for Santa to reach a suitable location.

The existing map-scaled separation (24–80 world units) applies to unopened gifts and every earlier drop in the visit, including gifts already collected. The first visit remains at 5:00, with 8–12 successful deliveries per visit and a 6–9 second minimum delay after each delivery. A visit can take longer while Santa travels to sufficiently separated ground. Following Santa is possible; gifts are physically connected to his route.

Neutral ownership, native queued movement, one Santa and nine reindeer, invulnerability, the 40% golden-token chance, the housing fixes and explicit Festive Cheer expiry are preserved.

All eleven automated regression scripts passed. Delivery tests exercise the actual Lua functions with moving and stationary cart positions, collected-gift history, blocked ground, water, engine spawn relocation, all delivery targets from 8 through 12, the 24-gift capacity and neutral convoy ownership. A native spawn adjusted to a distant clear point is rejected. No extra convoy is created while delivery waits.

Native verification on AoE IV 17.0.12303 used a new Large MegaRandom skirmish, Knights Templar against an English AI. The visit randomly selected eleven gifts and delivered all eleven. Every gift was 2.54–3.58 world units from the actual cart position; the smallest separation between gifts was 80.21 units against the map's required 80. All ten convoy units remained neutral throughout, and Santa travelled approximately 2,005 world units before the visit ended normally.

The temporary diagnostic build brought the first visit forward to test second 15. Deliveries occurred at seconds 15, 23, 30, 38, 47, 53, 60, 69, 87, 95 and 104. The longer gap before the ninth gift is expected when suitable, sufficiently separated ground is unavailable beside Santa. The production first visit remains 300 seconds. Camera following, full-map reveal, measurement wrappers and the diagnostic overlay are excluded from the release.

This was a single-player native test. Multiplayer and save/load were not exercised.

The clean production archive was rebuilt with the native Content Editor in 44 seconds, with zero errors and zero warnings. All 192 archive entries were inspected; the delivery, buff, shop and population scripts match the production source and no diagnostic code remains.

Production SHA256: `6333b5fa5fa4d0c604ddf99cd7558c73021567a683f7cf9f6665e50a8aeaaef7`.

Published through AoE IV as [store listing 593852](https://www.ageofempires.com/mods/details/593852/), with version 2026.11.20.3 in its description and TypeEkcyall credited as author. The publisher again offered Publish Mod rather than updating the earlier listing. After clearing the installed upload copy, a fresh in-game subscription downloaded the archive with the same SHA256 as the clean build. The superseded listing 593851 was then removed. The local publishing copy is disabled for normal play.
