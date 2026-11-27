# Yuletide Raids

**Prepared version: 2026.11.27.1; publication pending.** This label also appears at the start of the mod description.

![Yuletide Raids](assets/mod.png)

Father Christmas drops presents across the map. Spend golden presents on elf raids, villagers or resources, with options for each age.

**Select Yuletide Raids as BOTH the game mode and tuning pack.** The game mode runs the events and shop; the tuning pack supplies the custom unit and present definitions. Both are supplied by this one extension archive. Start a new match after updating.

**Version 2026.11.26.1** fixes enemy gifts for unequal teams: one shared enemy reward and one shared collecting-team deduction, both based on the collector's age. See [shared-gold validation](docs/2026-11-26-shared-gold.md).

**Version 2026.11.25.1** adds configurable starting tokens, gift counts and outcome weights, guaranteed tokens plus bonus rolls, earlier regular deliveries, individual enemy-gift payments/deductions and blocked-convoy recovery. Validation: [delivery update](docs/2026-11-25-delivery-draft.md).

**Version 2026.11.20.3** reconnects presents to Santa: gifts appear beside his actual cart position as he follows his random route. Spacing checks prevent clustered drops, including after earlier gifts are collected. See [delivery validation](docs/2026-11-20-santa-delivery.md).

**Version 2026.11.20.2** explicitly removes Festive Cheer's movement and gathering bonuses at the end of its 30-second timer. Repeat purchases refresh the timer without stacking. See [expiry fix and validation](docs/2026-11-20-cheer-expiry.md).

The population and compact shop fixes from **2026.11.20.1** remain included: a configured maximum of 250 preserves normal house requirements, and the shop has centered equal-width tabs and aligned numeric costs. See [housing validation](docs/2026-11-20-housing-update.md).

**Version 2026.11.26.2** replaces the pre-arrival notification sound with the game's bell sound (`taunt_007`). See [audio validation](docs/2026-11-26-bells.md).

**Version 2026.11.26.3** extends the warning to five seconds with four bell bursts and brings compact Yuletide settings ahead of the inherited advanced controls.

**Version 2026.11.26.4** changes default pickup outcomes to 60% shared team gold, 20% enemy gift, 10% gold ore and 10% stone ore. Existing custom lobby presets keep their selected weights.

**Version 2026.11.27.1** fixes 72 inherited text references that still pointed to another mod, so English objectives and notices resolve from Yuletide alone. Adds **Visit gap (min)** to the lobby: 1�20 minutes, default 5. First arrival remains 1:00; existing presets without this option use 5 minutes.

## Presents and convoy

- One Father Christmas trade cart per visit, with nine named reindeer. All ten remain neutral throughout the visit, invulnerable and unselectable, with zero sight and population. No player owns or tracks the convoy. Native movement orders are queued before ownership is relinquished in the same simulation callback. The convoy cannot collect its own gifts.
- First arrival at **1:00**, then every **five minutes** by default (lobby **Visit gap (min)**, 1�20 minutes), with four native bell bursts starting five seconds before arrival. A visit chooses **8–12 gifts** by default; lobby minimum and maximum can each be set to 1–20. Capacity is 80 unopened gifts; each expires after ten minutes. If capacity or safe land is unavailable, arrival retries. Visits continue until the selected gift count is delivered.
- Santa follows random land destinations. Every gift appears within six world units of the actual cart, separated from earlier sites by a map-scaled 24–80 units. If the convoy stalls or cannot find a valid delivery site for 15 seconds, all ten units phase to a clear location and resume native movement. This is obstruction recovery, not continuous flight through buildings.
- Every pickup gives the collector **one private golden token**, plus one independently rolled outcome. Default bonus chances: **60% shared team gold, 20% enemy gift, 10% gold ore, 10% stone ore**. Lobby weights are normalized by their total; zero disables an outcome, and all zero means tokens only.
- Team gold is a **100/150/200/300** pot by the collector's age, split between the collector and living teammates. Enemy gifts split one **100/150/200/300** gold pot among all living enemies and split one equal deduction among the collector and living teammates, both using the **collector's age**. Each deduction stops at zero; unpaid shares are not redistributed to teammates. Whole-gold remainders follow lobby-slot order. Neither pot increases with team size. No eligible enemies means no payment or deduction.
- Deposits appear on nearby clear ground, away from units. If no safe site is available, the bonus becomes shared team gold.
- The lobby puts Santa settings first, followed by compact starting-token groups for players 1-4 and 5-8. Default tokens sets the common starting amount; each player can override it. Default follows the common amount, which starts at zero. Existing wallets are not reset on resume.

## Golden-present shop

Only choices for your **current age** appear. Server checks reject purchases from other ages. Raid units have their age's configured health, armour and weapon upgrades; they are smaller than normal units, with a 20% health and 10% base weapon-damage bonus above those age-specific values. Waves use neutral ownership and do not reveal the enemy base to the buyer. There are no automatic elf raids.

| Option | Age I | Age II | Age III | Age IV |
|---|---:|---:|---:|---:|
| Resources per golden present | 100 | 150 | 200 | 300 |
| Villagers per golden present | 2 | 3 | 4 | 5 |
| Archer wave size | 3 | 4 | 5 | 6 |
| Spearman wave size | 4 | 6 | 8 | 10 |
| Armoured wave size | 2 | 3 | 4 | 5 |
| Golden-present cost per wave | 1 | 2 | 3 | 4 |

All purchased resources, including gold, go entirely to the buyer. The team-gold pickup outcome is shared with living teammates. Villagers match the buyer's civilization and respect population limits. Failed wave deployments refund their purchase.

The **Buffs** tab includes **Festive Cheer**, costing **1 golden present** in any age. For **30 game seconds**, the buyer's villagers move **30% faster** and gather food, wood, gold and stone **50% faster**. Existing and newly trained villagers benefit; other players and non-villager units do not. The tab shows the remaining time. Buying again resets the timer to 30 seconds without stacking the effect. The buff multiplies existing economy bonuses, and those bonuses remain after it expires. A failed activation refunds the purchase.

The enemy selector shows player names, cycling in lobby-slot order. Duplicate names include a small slot suffix; long names are shortened visually, with the full name available on hover. Purchases still use stable lobby-slot IDs, so renamed players and empty slots do not redirect raids.

Small text with no background or border just above the bottom-left resource box shows your applied economy/military boosts and the game's population limit on separate rows: Eco, Military, then Pop. It is hidden when you have no custom bonuses. Pending boosts or a population mismatch appear in amber; `Pop 200 / 250`, for example, means the game currently reports 200 while the configured limit is 250. This display is also included in More Advanced Game Settings.

## Installation and source build

[Subscribe through the Age of Empires IV mod catalogue](https://www.ageofempires.com/mods/details/604232/), or search for **Yuletide Raids** by **TypeEkcyall** in the game. Check for version **2026.11.26.4** in the description and start a new match after updating. The publisher created a replacement listing; subscribers to the older listing need this new link.

Download `Yuletide_Raids.sga` from [Releases](https://github.com/TypeDan/Yuletide-Raids/releases). Put it in a `Yuletide Raids` folder inside your AoE IV user-data `mods/extension/local` directory. Select it in **both** lobby selectors: Game Mode and Tuning Pack.

To build from source, open `Yuletide Raids.aoe4mod` in the AoE IV Content Editor and choose **Build Mod (F7)**. The archive is written under `archives/`. Close the editor before launching the game on the Xbox/Store installation.

### Updating the published mod

1. Edit this existing project and keep its project ID unchanged. Back up or commit the changes.
2. With AoE IV closed, build in Content Editor with **F7** and check for build errors. Copy the resulting `archives/Yuletide_Raids.sga` into `Documents/My Games/Age of Empires IV/mods/extension/local/Yuletide Raids/` if the build has not deployed it there. Include the thumbnail alongside it.
3. Close Content Editor, launch AoE IV and test a new match with Yuletide selected as both Game Mode and Tuning Pack.
4. Open **Mods → My Mods → Mod Publisher**. Select the existing local project and publish its update. Confirm completion and check the existing catalogue entry's version and downloaded archive.
5. Keep the source and release on GitHub in sync. After checking the subscribed archive, enable only the published copy of Yuletide. Keep any local publishing copy disabled, and retain the source project and build archives outside the game's mod folders.

Keep this project's GUID unchanged for updates; a genuinely separate mod needs a different GUID. The [official publishing guide](https://support.ageofempires.com/hc/en-us/articles/4416968609044-Publishing-and-Using-Mods) describes updating the existing local project. The game failed to associate the rebuilt archive with the existing listing on 20 November and created a fresh listing. Deletion is not a routine update step. If the publisher shows Unknown or Publish Mod unexpectedly, check the existing listing before proceeding; the website's separate version counter is not this release label.

## Experimental status

All 13 automated test scripts pass, including the current shared-gold correction for unequal teams and all ages. The preceding release's native 2v2 skirmish verified the engine's gold transactions, host starting-token override, reduced resource purchase, golden-token pickup plus bonus, two Santa visits and neutral convoy recovery. Every tested drop stayed beside the cart. Earlier live tests showed Age I melee and ranged attacks and reindeer running. Scots and Vikings blueprint support is included. Current build and publication evidence is recorded in the shared-gold validation document above.

A complete natural golden-present pickup → purchase → enemy attack sequence, all higher-age animations, deposit mining, multiplayer and save/load still need full in-game validation. The bell warning's audio was verified by matching a native-match speaker capture to the installed bell waveform. Available gift sites and convoy route access can vary by map, and the cart horse's animation has not been separately confirmed close up.

The current build uses a native trade cart, reindeer, smaller human soldiers and native present models. Custom sleigh/Santa models, reliable red/green recolours, imported voices/sleigh bells and turkey replacements are **not implemented**. Golden presents are larger and labelled, without a gold repaint. The cover is promotional illustration, not a screenshot of custom assets.

## Credits

Uses the match setup, settings, victory-condition, diplomacy and civilization helper code from More Advanced Game Settings, based on [Woprok's original Advanced Game Settings](https://github.com/Woprok/AOE4-AdvancedGameSettings) and [Joshua Sachtleben's continuation](https://github.com/joshuasachtleben/AOE4-AdvancedGameSettings). The Christmas convoy, present rewards, golden-present shop and elf raids were added for Yuletide Raids. See [CREDITS.md](CREDITS.md) and the retained [GPL-3.0 license](LICENSE.md).

## Release numbering

Use `YYYY.MM.DD.N` in `VERSION`, the description entries (IDs 2 and 3) in `assets/locdb/*.csv`, and the GitHub release. Increase `N` for each further release that day. Set the label before the native F7 build, publish through the existing local project, then verify the store description and downloaded archive. The site's own version counter is separate from this release label. Keep project GUIDs and existing store listings when updating; deleting listings is not a normal update step.
