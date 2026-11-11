# Yuletide Raids

![Yuletide Raids](assets/mod.png)

Father Christmas drops presents across the map. Spend golden presents on elf raids, villagers or resources, with options for each age.

**Select Yuletide Raids as BOTH the game mode and tuning pack.** The game mode runs the events and shop; the tuning pack supplies the custom unit and present definitions. Both are supplied by this one extension archive. Start a new match after updating.

## Presents and convoy

- One Father Christmas trade cart per visit, with nine named reindeer. All ten are invulnerable, unselectable and controlled by the script, with zero sight and population. The convoy cannot collect its own gifts.
- The first visit is due after 60 seconds; later visits are due 5–8 minutes after the previous visit began. Each visit chooses a target of **5–10 presents** and normally lasts 36 seconds, with drops every 2–4 seconds. Santa searches nearby clear locations and retries blocked drops; he stays longer if needed to finish his target. A visit waits if fewer than five slots remain under the limit of 24 unopened presents, then starts once enough are collected or expire. Uncollected presents expire after ten minutes. Native pathfinding and movement animations are used.
- Each visit starts at a random land location and follows random destinations across the map, dropping presents along the way. Player bases, team sizes and lobby order do not determine the route. Drops avoid water, buildings and nearby presents; a safety margin keeps the convoy away from the map boundary.
- Bring an eligible unit near a present to open it. **Forty percent** are golden presents stored in your wallet.
- Ordinary presents give 300 gold to the opener (40%), 300 gold shared among living enemies (40%), a gold deposit (10%), or a stone deposit (10%). These chances apply to the remaining 60% of presents that are not golden shop tokens.

## Golden-present shop

Only choices for your **current age** appear. Server checks reject purchases from other ages. Raid units have their age's configured health, armour and weapon upgrades; they are smaller than normal units. Waves use neutral ownership and do not reveal the enemy base to the buyer. There are no automatic elf raids.

| Option | Age I | Age II | Age III | Age IV |
|---|---:|---:|---:|---:|
| Resources per golden present | 300 | 450 | 600 | 900 |
| Villagers per golden present | 2 | 3 | 4 | 5 |
| Archer wave size | 3 | 4 | 5 | 6 |
| Spearman wave size | 4 | 6 | 8 | 10 |
| Armoured wave size | 2 | 3 | 4 | 5 |
| Golden-present cost per wave | 1 | 2 | 3 | 4 |

Villagers match the buyer's civilization and respect population limits. Failed wave deployments refund their purchase.

The enemy selector uses the actual lobby slot number, in ascending order. Empty slots and eliminated players do not renumber the remaining targets.

## Installation and source build

[Subscribe through the Age of Empires IV mod catalogue](https://www.ageofempires.com/mods/details/583313/), or search for **Yuletide Raids** by **TypeEkcyall** in the game. This replaces the earlier listing; existing users must subscribe to this new entry.

Download `Yuletide_Raids.sga` from [Releases](https://github.com/TypeDan/Yuletide-Raids/releases). Put it in a `Yuletide Raids` folder inside your AoE IV user-data `mods/extension/local` directory. Select it in **both** lobby selectors: Game Mode and Tuning Pack.

To build from source, open `Yuletide Raids.aoe4mod` in the AoE IV Content Editor and choose **Build Mod (F7)**. The archive is written under `archives/`. Close the editor before launching the game on the Xbox/Store installation.

### Updating the published mod

1. Edit this existing project and keep its project ID unchanged. Back up or commit the changes.
2. With AoE IV closed, build in Content Editor with **F7** and check for build errors. Copy the resulting `archives/Yuletide_Raids.sga` into `Documents/My Games/Age of Empires IV/mods/extension/local/Yuletide Raids/` if the build has not deployed it there. Include the thumbnail alongside it.
3. Close Content Editor, launch AoE IV and test a new match with Yuletide selected as both Game Mode and Tuning Pack.
4. Open **Mods → My Mods → Mod Publisher**. Select Yuletide and choose **Update Mod**. Confirm completion and check that the existing catalogue entry has updated.
5. Keep the source and release on GitHub in sync. After checking the subscribed archive, enable only the published copy of Yuletide. Keep any local publishing copy disabled, and retain the source project and build archives outside the game's mod folders.

**If an existing mod shows “Publish Mod” instead of “Update Mod”, stop before uploading.** AoE IV can forget the publication association after restarting and create another listing. “By Unknown” can accompany this fault; it does not change the source project's authorship. Deleting and republishing is a last resort that resets the listing and requires subscribers to subscribe again. The current listing above was recreated on 11 November 2026 with the owner's approval because this fault blocked updates. Do not delete it as a routine update step.

## Experimental status

Built against game version **17.0.12260**. Automated checks cover age restrictions, rewards, refunds, neutral raid deployment, all twelve unit variants, convoy invulnerability/movement/cleanup and pickup exclusions. Live tests have shown Age I melee and ranged attacks, reindeer running, the shop panel and ordinary-present collection. Scots and Vikings blueprint support is included.

A complete natural golden-present pickup → purchase → enemy attack sequence, all higher-age animations, deposit mining, multiplayer and save/load still need full in-game validation. Convoy spacing and route access can vary by map, and the cart horse's animation has not been separately confirmed close up.

The current build uses a native trade cart, reindeer, smaller human soldiers and native present models. Custom sleigh/Santa models, reliable red/green recolours, festive voices/bells and turkey replacements are **not implemented**. Golden presents are larger and labelled, without a gold repaint. The cover is promotional illustration, not a screenshot of custom assets.

## Credits

Uses the match setup, settings, victory-condition, diplomacy and civilization helper code from More Advanced Game Settings, based on [Woprok's original Advanced Game Settings](https://github.com/Woprok/AOE4-AdvancedGameSettings) and [Joshua Sachtleben's continuation](https://github.com/joshuasachtleben/AOE4-AdvancedGameSettings). The Christmas convoy, present rewards, golden-present shop and elf raids were added for Yuletide Raids. See [CREDITS.md](CREDITS.md) and the retained [GPL-3.0 license](LICENSE.md).
