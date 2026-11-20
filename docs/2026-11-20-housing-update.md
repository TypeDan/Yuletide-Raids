# Version 2026.11.20.1

Custom population limits now set the maximum without granting housing. The previous OnPlay fixed-cap override made a 250 limit immediately usable without houses. The code clears that override and retains the maximum-population modifier. Team population transfers also preserve housing. Restore callbacks clear the override without applying the maximum modifier twice. Mongols retain their civilization's housing exception, and an explicit minimum-population setting still applies.

Validation on 20 November 2026:

- Automated checks passed for all eight lobby slots in reversed internal player order, independent housing and ceiling values, global and individual limits, house gains/losses, maximum clamping, Mongols, repeated initialization/restore callbacks and team population transfers.
- Player settings and bonus-HUD regression checks passed in both repositories.
- A native Yuletide match used Knights Templar in host slot 1, Abbasids in slot 2 and HRE in slot 3, each configured for 250. All started with 10 housing capacity and a reported maximum of 250.
- A temporary diagnostic gave sufficient housing to all three players: usable capacity stopped at 250. Removing it restored their natural housing (10 for the idle host, 20 for the AIs which had built houses).
- Building a normal house as the host raised the native display from 7/10 to 7/20 while the maximum remained 250.
- The diagnostic overlay, temporary housing and test tokens are excluded from the production archive.

The native match validates the shared population code used in both mods. It is not a full multiplayer or saved-game compatibility test; start a new match with the updated mod.

The shop uses a compact button template with centered labels, equal-width Goods/Raids/Buffs tabs, a narrower panel and one aligned numeric cost column. All three tabs were inspected in the native game; text fit without clipping. The shop sits below the objective icons. The Festive Cheer purchase/timer regression passed with the generated XAML parsed successfully.

Both final native Content Editor builds completed with zero errors and warnings. Archive inspection confirmed production source matches, mod metadata and all expected files; no housing diagnostic remains.

A second match with the clean production archive confirmed the compact menu clears the objective icons, the wallet starts at zero, no test overlay appears, and the host starts at 7/10 with the configured maximum shown as Pop 250.

Published through the native AoE IV publisher as [Yuletide Raids 593849](https://www.ageofempires.com/mods/details/593849/). A fresh subscription download matched the tested production archive byte-for-byte: SHA256 `37b6a3ea99aa5e4186149f59357e4061eb082d979303d27aa33c11a9c6f86be0`. The superseded listing 593827 was deleted after that verification. Previous subscribers need the new listing; select Yuletide as both Game Mode and Tuning Pack.
