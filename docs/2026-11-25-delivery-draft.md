# Delivery update — 2026.11.25.1

Release 2026.11.25.1 built and passed native testing. AoE IV confirmed publication on 26 November at 00:21 UTC. The new [store listing 604183](https://www.ageofempires.com/mods/details/604183/) displays the correct version and description under TypeEkcyall. The game created a replacement listing despite the unchanged project GUID; superseded listing 593852 was removed after the new listing was verified. Previous subscribers need the new listing.

The [GitHub release](https://github.com/TypeDan/Yuletide-Raids/releases/tag/v2026.11.25.1) is available. Its fresh downloaded archive matches the clean production SHA-256 below.

Implemented in source:

- First visit at 60 game seconds, subsequent visits scheduled 180 seconds after the previous arrival.
- Native event-cue chime and announcement three seconds before each scheduled visit.
- Every pickup grants one private golden token and independently rolls one bonus outcome.
- Lobby outcome weights default to 40/40/10/10. Values are normalized by their total; zero disables an outcome, all zero gives tokens only.
- Lobby minimum/maximum gifts: 1–20, defaults 8–12. Reversed bounds are swapped.
- Common starting wallet plus individual overrides for all eight lobby slots. Defaults zero. Initialization never resets an existing wallet.
- Shop resource exchanges reduced to 100/150/200/300 by the buyer's current age.
- Found team gold and safe-deposit fallback reduced to a team pot of 100/150/200/300 by the collector's current age, shared among living teammates.
- Blocked convoy recovery phases all ten units to clear ground and resumes native orders. It does not implement continuous collision-free flight. Normal movement retains native animations. Recovery briefly assigns an issuer and returns squads to neutral ownership in the same callback; zero-sight definitions remain unchanged.
- Capacity raised to 80 unopened presents to accommodate four maximum-size visits before ten-minute gift expiry.

Enemy gifts pay every living enemy individually and charge each living collecting teammate individually: 100/150/200/300 according to each recipient's own age. Deductions are capped at available gold, preventing negative balances. The focused reward regression passed, including mixed-age recipients, eliminated-player exclusion and insufficient/zero balances.

The user explicitly confirmed both enemy payments and individual teammate deductions. No economy clarification remains outstanding.

All 13 current automated test scripts passed on 25 November, using `work/python-libs` on `PYTHONPATH`. Coverage includes lobby descriptor defaults/IDs, weights/zero-weight outcomes, stable slots, no wallet reset, warning and arrival schedule, single-consumption token-plus-outcome collection, reduced purchases, safe deposit placement, convoy recovery and inherited boost/population/buff/raid behavior. Timing tests use mocked native functions; they do not prove actual engine audio, menus or wall recovery.

The final native release build completed on 25 November in 47.1831 seconds, with 0 burn errors and 0 warnings. A separately built diagnostic copy completed just after midnight on 26 November. The production source and archive were restored after creating that copy.

The clean release archive is `archives/Yuletide_Raids.sga` (2,929,895 bytes), SHA-256 `a9458676e2b8778a8a50553bb88c55a91eda542d586459f17e18c5d515899f2a`. `tools/verify_archive.ps1` verified all 193 entries, mod metadata, the new settings script, exact source equality for every Lua script and absence of diagnostic markers. The previous production archive remains backed up in `work/yuletide-pre-nov25.sga`.

Native test completed: a new Large MegaRandom 2v2 skirmish on AoE IV 17.0.12303. Host English, Ottoman ally, Macedonian and Tughlaq enemies. The actual native reward function passed checks for both individual ally deductions and both enemy payments. Host starting override 2 appeared in the wallet, with common amount 3 selected in the lobby. A real shop purchase reduced the wallet from 2 to 1 and raised gold from 100 to 200. Santa arrived at the first scheduled minute. A diagnostic stop command at second 70 triggered recovery; all ten units were neutral afterward, and deliveries resumed. The first visit completed ten gifts. The scout collected a gift: the wallet increased from 1 to 2 and the enemy outcome deducted 100 gold from the host. At second 316 the second visit was active, with 18 total gifts, two recoveries and zero diagnostic failures. Every delivery was checked against the required six-unit cart distance. Audio, multiplayer networking and save/load were not independently tested. Recovery was exercised with a forced stop and a later natural stall, rather than a constructed wall.

The game was closed and its local diagnostic archive replaced with the verified clean release before publication.

After publication, the local publisher copy and old installed copy were moved outside the game's mod folders. The new uploaded copy was also backed up, then a fresh download was requested through the in-game public catalogue. The downloaded `subscriptions/604183/fe7ab5b9ddd28284cd136e7e25002219852c49d7768bab17b7e0bcaf0b5c901d.sga` matches the clean release and GitHub download exactly. No diagnostic archive remains in the active mod folders.
