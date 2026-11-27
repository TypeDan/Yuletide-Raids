# Lobby layout - version 2026.11.27.2

Status: source, native builds and GitHub release are complete. AoE publication verification is in progress.

The main game-mode lobby now orders its advanced sections as Ages & diplomacy, Population & rules, Victory details, then Economy bonuses, Military bonuses and Player pop limits. Advanced rules and Player colours follow. Featured victory/team controls remain available. Yuletide keeps Santa/presents and both starting-token groups ahead of these shared controls.

Within Ages & diplomacy, age limits and starting resources come first, then map/team visibility, followed by tribute and diplomacy switches. Population & rules puts starting housing, the global ceiling and extra capacity per house together, followed by starting units/buildings, special map rules and score display.

Replaced ambiguous Min/Max Population Capacity with Starting housing and Global population limit. Tooltips explain that the former grants housing and the latter only sets the ceiling; individual player limits still require houses. The per-player tooltip names the exact global field and group. Player numbers, keys, values, defaults, ownership and project identities are unchanged. English labels were clarified; other languages retain their existing labels.

Validation: the descriptor was normalized before/after to prove that only section/option reference order changed. Every option object, key, enumeration order/default and ID is unchanged. Existing regression suites pass (4 scripts for MAGS, 14 for Yuletide), including real descriptor-derived selections, all eight player slots, normal housing growth/loss and localization completeness. No gameplay scripts changed.

Native verification: after restarting the PC, both mods built with zero errors and zero warnings. The game loaded version 2026.11.27.2. Inspected the shared three-column groups, all player bonus/cap columns, and Yuletide Santa/token settings. Shortened Teams & start, Resume sacred timer, Central sacred site and Reveal map on defeat after the initial visual pass; the final build renders these labels without truncation. Archive checks confirm production Lua and no injected diagnostic code. Fresh GitHub downloads match the final native build hashes.

Publication follow-up: the AoE text filter rejected the inherited French Wonder-loss tooltip (string 92). Version 2026.11.27.3 rephrases that tooltip with the same meaning. It includes all tested lobby changes from .2; no gameplay rules changed.
