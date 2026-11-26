# Shared gold correction — 2026.11.26.1

Enemy gifts now split one gold pot among living enemies and one equal deduction across the collector's living team. Both pots are 100/150/200/300 according to the collector's age. A 4v2 Age I pickup therefore charges 25 per ally and gives 50 per enemy, rather than multiplying either side's amount by player count.

Whole-gold remainders are assigned in stable lobby-slot order. Each player's deduction is capped at their available gold; an unpaid share is not redistributed. Eliminated players are excluded. With no living enemies, no gold is paid or deducted. Friendly gold remains one shared team pot; golden tokens and purchased resources remain private. Bonus probabilities are unchanged at 40/40/10/10 by default.

Regression coverage includes all four ages, mixed recipient ages, 4v2, 3v2 and 1v3 teams, deterministic rounding under reversed player iteration, insufficient funds, zero balances, eliminated players, no enemies and single-consumption pickups.

All 13 automated regression scripts passed on 26 November. These execute the shipped Lua functions with mocked engine calls. Native gold-resource API integration was exercised in the immediately preceding release; this arithmetic-only correction has not had a new multiplayer playtest.

Native Content Editor build completed in 42.1481 seconds with zero errors and warnings. Archive validation found all 193 entries, exact Lua-source equality and no diagnostic markers. SHA-256: `dfce04caeb1921bb4e9e94a08b5695e407fcf20a1326f12f1c202a4a27e7531f`. Publication is in progress.
