# Lobby layout - prepared version 2026.11.27.2

Status: source updated and automated checks pass. Native build, visual layout verification and publication are pending. The published/downloadable version remains 2026.11.27.1. Do not label the old archive as this update.

The main game-mode lobby now orders its advanced sections as Ages & diplomacy, Population & rules, Victory details, then Economy bonuses, Military bonuses and Player pop limits. Advanced rules and Player colours follow. Featured victory/team controls remain available. Yuletide keeps Santa/presents and both starting-token groups ahead of these shared controls.

Within Ages & diplomacy, age limits and starting resources come first, then map/team visibility, followed by tribute and diplomacy switches. Population & rules puts starting housing, the global ceiling and extra capacity per house together, followed by starting units/buildings, special map rules and score display.

Replaced ambiguous Min/Max Population Capacity with Starting housing and Global population limit. Tooltips explain that the former grants housing and the latter only sets the ceiling; individual player limits still require houses. The per-player tooltip names the exact global field and group. Player numbers, keys, values, defaults, ownership and project identities are unchanged. English labels were clarified; other languages retain their existing labels.

Validation: the descriptor was normalized before/after to prove that only section/option reference order changed. Every option object, key, enumeration order/default and ID is unchanged. Existing regression suites pass (4 scripts for MAGS, 14 for Yuletide), including real descriptor-derived selections, all eight player slots, normal housing growth/loss and localization completeness. No gameplay scripts changed.

Native verification blocked: two attempts to capture the AoE window failed with D3D11CreateDevice / 0x887A0004 (device interface or feature level not supported), including recovery using a freshly selected window. No claim of visually verified fit or published menu update is made.
