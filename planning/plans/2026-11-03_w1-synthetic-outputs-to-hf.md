# W1: move legacy phase-1 synthetic outputs to a private HF dataset (PLAN, not executed)

> **Record, not status.** Written 2026-11-03. The move was not run: the `hf` CLI was not logged in. Current status: [STATUS.md](../../STATUS.md).

Status: BLOCKED-AUTH. `hf auth whoami` returned "Not logged in"; no upload, no `git rm` done.

## Inventory (synthetic_generation/outputs, tracked files)
| folder | size | files | live references | class |
|---|---|---|---|---|
| gps_sign_relabel_all | 117 MB | 80 | paper_b/config.py, STATUS, DATA.md, tests, analysis | KEEP (frozen Paper B bank) |
| usa_mex_dpo_anchored_110_b6_c4_06232026 | 17 MB | 9 | protocols/gps_sign_dpo_wvs.toml, synthetic_generation/sca2_datagen/relabel.py (path strings; verify not a runtime read before removal) | MOVE |
| anchored_pilot_v2 | 11 MB | 7 | only synthetic_generation/Prompt_Improvements_Diffs.md, Sample_Triplets_600.md (prose) | MOVE |

Respondent check: no population_prob / weighted_count / human_mean columns. The word "respondent" appears only inside generated prompt text; confirm before upload.

## Steps once authed
1. Create private dataset `Bonorinoa/SCA2-phase1-synthetic-outputs` (new only).
2. Upload the two MOVE folders, relative paths preserved; record commit sha.
3. Verify remote file count and sha256 against local.
4. `git rm -r` the folders, add to .gitignore, document in synthetic_generation/README.md and DATA.md with
   `hf download Bonorinoa/SCA2-phase1-synthetic-outputs --repo-type dataset --revision <sha> --local-dir synthetic_generation/outputs`.
