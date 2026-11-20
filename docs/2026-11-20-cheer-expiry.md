# Version 2026.11.20.2

Festive Cheer now owns the lifetime of its modifiers. The previous code assumed the native duration had already removed them, skipped explicit cleanup at expiry, and discarded the stored IDs. The new code applies indefinite modifiers and explicitly removes its recorded IDs after 30 game seconds. The periodic simulation tick also checks expiry. Refreshing a purchase replaces the old modifier set and prevents the old timer from cancelling the new purchase. Existing economy bonuses are retained.

Automated validation covers both villager blueprint variants, player isolation, all four gathering resources, newly trained villagers, refresh without stacking, stale timer callbacks, partial-application refunds, expiry through both the timer and periodic tick, elimination and game-over cleanup. The modifier model deliberately does not expire effects automatically, so a disappearing countdown cannot hide a permanent effect. The generated shop XAML also parses successfully.

Native verification on AoE IV 17.0.12303 reproduced the reported speed bug in a fresh Knights Templar skirmish. A villager blueprint's modified speed was 4.5 before the effect and 5.85 (+30%) during it. The old native-duration call still returned 5.85 five seconds after its 30-second deadline; explicitly removing that modifier restored 4.5 immediately.

With the fixed purchase handler, purchases at test seconds 45 and 65 kept speed at 5.85 without stacking. The original deadline at second 75 did not cancel the refreshed purchase. At second 95, exactly 30 seconds after the refresh, speed returned to 4.5. The selected villager's game UI likewise changed from 1.46 to its normal 1.12. These UI values use the game's display scale and rounding.

A separate purchase at second 105 raised speed to 5.85 and returned it to 4.5 at second 135, remaining normal at second 140. The selected-unit UI confirmed normal speed after this second expiry too.

The test used temporary instrumentation to measure the native speed API and invoke the real purchase handler. The instrumentation is excluded from the production archive. Multiplayer and save/load were not exercised in this native test.

The production archive was rebuilt in the native Content Editor with zero errors and warnings. All 192 entries across its archive tables were checked; the changed gameplay scripts match the clean source and no diagnostic code remains.

Production SHA256: `14ab381ab72eb2745a58b2e62ca93501f38a8c20c18ce908076ec3b055efe9bb`.

Published through the game as [catalogue entry 593851](https://www.ageofempires.com/mods/details/593851/). Its description shows version 2026.11.20.2. After clearing the installed publishing copy, a fresh catalogue download matched the production SHA256 exactly. The project GUID is unchanged, but the publisher created a new listing instead of updating 593849.
