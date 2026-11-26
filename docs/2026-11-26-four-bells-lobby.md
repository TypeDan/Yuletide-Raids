# Four bell bursts and compact lobby — 2026.11.26.3

Status: regression checks passed; native build and verification in progress.

Santa's warning now starts five seconds before arrival. The announcement plays the first native town-bell burst; three sound-only repeats follow at one-second intervals. There is still one banner per visit. First bursts are at 0:55, 0:56, 0:57 and 0:58, with arrival at 1:00 and the existing 180-second visit cadence.

The Yuletide controls move ahead of inherited advanced options. Shorter labels and a short lobby description reduce wrapping. Starting-token overrides are split into players 1-4 and 5-8 columns, with Default referring to the common Default tokens amount. All option keys, defaults and ranges are preserved; the settings parser accepts the previous single-section format as a fallback.

All 13 regression scripts pass, including exact four-burst timing across four visits and both old/new layouts for all eight wallet slots. Project identity is unchanged. Other gameplay rules are unchanged.

Native build: 43.7811456 seconds, zero errors and warnings. Archive verifier passed all 193 entries, exact Lua/source matching and no diagnostic markers. SHA-256: 0fbb54d2d52d39dd6242b1a78f8f255f15440cf5b84357a6af9525dbcc05e459.

