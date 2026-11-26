# Four bell bursts and compact lobby — 2026.11.26.3

Status: native build, regression and in-game checks passed. Published as AoE listing 604203 and GitHub release v2026.11.26.3. Old listing 604200 was removed after the new store description was verified.

Santa's warning now starts five seconds before arrival. The announcement plays the first native town-bell burst; three sound-only repeats follow at one-second intervals. There is still one banner per visit. First bursts are at 0:55, 0:56, 0:57 and 0:58, with arrival at 1:00 and the existing 180-second visit cadence.

The Yuletide controls move ahead of inherited advanced options. Shorter labels and a short lobby description reduce wrapping. Starting-token overrides are split into players 1-4 and 5-8 columns, with Default referring to the common Default tokens amount. All option keys, defaults and ranges are preserved; the settings parser accepts the previous single-section format as a fallback.

All 13 regression scripts pass, including exact four-burst timing across four visits and both old/new layouts for all eight wallet slots. Project identity is unchanged. Other gameplay rules are unchanged.

Native build: 43.7811456 seconds, zero errors and warnings. Archive verifier passed all 193 entries, exact Lua/source matching and no diagnostic markers. SHA-256: 0fbb54d2d52d39dd6242b1a78f8f255f15440cf5b84357a6af9525dbcc05e459.


Native verification: the clean release archive was tested alone, with the older subscription temporarily moved out of the active mod directory. The lobby showed the three compact sections and shorter labels correctly. A fresh match loopback recording matched all four native bell bursts at 82.950, 83.826, 84.829 and 85.859 seconds into the capture, with correlations 0.573, 0.589, 0.586 and 0.797. The match log contained no SCAR runtime errors. No diagnostic code was used. The GitHub release download matches the tested archive hash.


The initial AoE publication was rejected because its text filter masked the GitHub URL. Replaced that URL with a plain GitHub repository credit in the five description localization tables. The metadata-only native rebuild completed in 48.6642652 seconds with zero errors/warnings; all 193 archive entries passed validation, with unchanged gameplay scripts. Final SHA256: 3ba53c65fccf70903114769ae4b502ee64f85caaa72c8387e5dc05a61704f390. The GitHub release asset was replaced with this final archive.

Archive-to-archive comparison confirmed that only four compiled localization tables changed for the publication retry; gameplay, UI descriptors, unit data and metadata are byte-identical to the live-tested archive. Final release source commit: 882ccf3efc9ee2d010f41fa46d2d888126650d49.

After removing the local publishing copy and temporary publisher subscription copy, a fresh in-game catalogue download from listing 604203 matched the final build and GitHub archive SHA256. Active mod folders contain exactly one Yuletide archive, under subscriptions/604203.
