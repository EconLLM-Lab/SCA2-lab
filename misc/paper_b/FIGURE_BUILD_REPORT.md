# Figure build report (P2-F, Paper B reader-facing empirical figures)

Checkout: `SCA2_PofW-paper-b-draft`, branch `paper/paper-b-draft`. Nothing committed. Model route for this run: claude-sonnet-5-5 (Anthropic), per the card; the parent PM wrote `tools/test_build_figures.py`, one metadata string, and the stricter `verify()` guards (see `FIGURE_PM_CHECKS.md`). I did the visual fixes and this report.

## Input

One file only: `planning/sprint_2026-10-11/paper-b-tier1/NUMBERS_TABLE.csv`, sha256 `71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4` (562 rows; the generator refuses any other hash). No `data/`, no human rows, no network, no installs. Every plotted point, interval endpoint, reference line and printed number is the exact CSV string of a named `claim_id` + column; TeX maps it to a position (x0 + (v - min) * scale) and prints it half-up with Decimal.

## Outputs (all in `misc/paper_b/figures/`)

| Figure | Files | Manifest entries | Claim ids |
|---|---|---|---|
| Three-link validity forest | `fig_three_links.{tex,pdf,png}` | 108 | 35: `C9_a_*` and `C9_b_*` for `adapter_gps` and `adapter_human`, `C9_a_human_gps_*`, seven surfaces each (`..._spearman_rho`) |
| Trust rank agreement vs distance | `fig_info_vs_route.{tex,pdf,png}` | 64 | 15: `B2_cohort1_trust_rho`, `B2_bank2_trust_rho`, `PX_persona_trust_rho`, `PX_signprompt_trust_rho`, `C9_TVD_adapter_persona_trust_gps_profile_block`, four `C9_TVD_*_mean_tvd_country_equal`, six `C9_TVD_*_profile_block` contrasts |
| Retrospective item screen | `fig_screen.{tex,pdf,png}` | 65 | 14: `SCR_A_primary`, `SCR_p_perm`, `SCR_null_q95`, `SCR_null_mean`, `SCR_one_third_ceiling`, `SP_A_primary`, `SP_p_perm`, `SP_null_q95`, `SP_D_own/common`, `CMP_face_valid_D_own/common`, `CMP_jev_D_own/common` |
| Own factorial effects | `fig_factorial_own.{tex,pdf,png}` | 48 | 24: `FX_{adapter64,signprompt64}_{surface}_own_beta` (7 each) and five summary statistics each (`V5_hits`, `own_effects_wrong_signed`, `surfaces_largest_mover_is_trust_bit`, `pc1_share`, `mean_abs_inter_surface_r`) |

`PLOT_MANIFEST.json`: each datum has figure, panel, claim_id, table column, exact value, role (`point`, `interval_low`, `interval_high`, `reference_line`, `null_95th_percentile`, `null_mean`, `printed_label`) and x position in cm; panels record the affine map, the quantity and the interval unit. 285 entries in total.

## What each plot means

1. **Three links.** Spearman correlation across countries, surface D, three panels (adapter-GPS, adapter-human, human-GPS), seven strict surfaces. Filled circle/solid = first-cohort adapters (primary, C9_a); open diamond/dashed = second-cohort adapters (robustness, C9_b); square = no adapter involved. The legend is neutral grey, since panel colour names the link. Heavy line is zero. Panels 1-2 use a **profile-block bootstrap (26 blocks)**; panel 3 uses a **country bootstrap (42 countries)**. Risk taking has n = 41 for the adapter-human and human-GPS estimates; this is stated in a note, not over the whiskers. Intervals covering zero are drawn, not hidden. C9 is descriptive, not preregistered.
2. **Information versus route.** Panel A: TRUST only, Spearman correlation with GPS trust (higher = stronger rank agreement), profile-block bootstrap. The base model's cell reads "undefined: constant composite" and is never drawn at zero. Panel B: FULL strict battery, mean total variation distance (TVD, country-equal; lower = closer), points only (the table banks no interval for the cell means); the sign-profile prompt and second-cohort adapters are marked "not scored". Panel C: six paired profile-block-bootstrap differences in mean TVD with a zero line and the interaction. The footer states the crossing is descriptive, not a causal fine-tuning effect or a weights-versus-prompts law.
3. **Retrospective screen.** Panel A: A for trained adapters and the sign-profile prompt with 95% **country-bootstrap** intervals; criterion is WVS-7 human country differences. Registered one-third-of-ceiling bar is a dashed reference line with no interval (the table banks none). Panel B: the same A against its **permutation** null (95th percentile bar; null mean for adapters only), one-sided p printed beside the points. Panel C: direct paired country-bootstrap contrasts (adapters minus sign-profile prompt, face-valid reader, typed decision model), on own and common items. n = 5 and 9 are printed. The footer says an interval covering zero is not equivalence, and that the interval and the permutation p answer different questions.
4. **Factorial.** The table banks only the seven own (diagonal) effects and five summary statistics, not the 7 x 6 matrix, so I did **not** build a heatmap (the brief allowed this fallback). Panel A: stems from zero, trained (circle) and prompt (square), raw composite units, each row on its own scale (stated), shaded half = against the intended direction, no uncertainty banked. Panel B: banked counts and shares on separate per-row scales. No mechanism language.

## Commands and exits (run from the checkout root)

All with `HF_TOKEN=` blank, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/Users/bonorinoa/.hermes/cache/scratch/paper-b-reader-pass`, `env -u PYTHONPATH`.

```
python3 misc/paper_b/tools/build_figures.py                 # exit 0; 4 x pdflatex exit 0, 4 x pdftoppm -r 200 exit 0
python3 misc/paper_b/tools/build_figures.py --verify        # "verify: ok", exit 0
python3 misc/paper_b/tools/build_figures.py --out <scratch> # regenerated copy; exit 0; the 4 PDFs, 4 PNGs and manifest are byte-identical (cmp) to the committed-in-place ones
.../SCA2_PofW/.venv/bin/python -m pytest misc/paper_b/tools/test_build_figures.py misc/paper_b/tools/test_audit_numbers.py \
    misc/paper_b/tools/test_render_supplement.py misc/paper_b/tools/test_anonymize_prereg.py -q   # 38 passed in 0.36s, exit 0
```

Tests include mutations of a plotted point, an interval endpoint, a printed label, the TeX coordinate transform, a manifest value and a dropped manifest figure, each rejected; plus pin, coverage, bootstrap-unit, direct-contrast and undefined-base checks. PDFs embed fonts (Latin Modern); vector throughout. I inspected all four rendered PNGs after the final build: no overlaps or clipping seen.

## Visual fixes applied (PM comment 184)

Three links: "Spearman correlation" axis label, neutral grey legend, n = 41 moved to a note. Info/route: "TRUST only" vs "FULL strict battery" titles, TVD spelled out, "higher = stronger rank agreement" / "lower = closer", darker subtitles, near-zero label moved off the zero line. Screen: A/B titles shortened and separated, p and CI labels moved off the zero lines, threshold text moved below the panel, null legend restated. Factorial: row spacing widened (ticks no longer touch the next row), shading note and legend moved clear of ticks, numeric columns headed by series, own/diagonal-only and no-uncertainty stated, row-specific scales stated. No value, coordinate source or scale was recomputed or standardized.

## Issues for the writer

- Natural page sizes (pt): three_links 430x355, info_vs_route 469x527, screen 455x419, factorial_own 435x568 (about 15.2 to 16.5 cm wide). Footnotes were wrapped so no long line sets the width. Include at `\textwidth` (about 0.9 to 1.0 scale for a ~15 cm text block) and keep the scale at or above 0.9 so `\footnotesize` text stays near 7 pt. Fig. 2 and Fig. 4 are tall (about 18.6 and 20 cm); give them their own float page. A final earlier width of 20 to 26 cm (from unwrapped footers) was fixed.
- Captions must restate: C9 descriptive, not preregistered; the three bootstrap units differ; the base-model trust correlation is undefined, not zero; trust is one dimension and TVD is the full strict battery; the screen is retrospective, pre-piloting untested, and interval and permutation p are different questions; coverage-matched readers have 5 and 9 items and do not establish equivalence.
- The one-third-of-ceiling value has no interval in the table, so none is drawn. The cross-wave mean has no interval and is not plotted.
- TVD cell means have no interval; only the paired contrasts do. Do not read overlap of the points as a test.
- The factorial figure shows own effects only; the text must not claim a full cross-effect structure.
- Edit figures only by changing `build_figures.py` and rerunning; `--verify` rejects hand-edited TeX/manifest.
- Pre-existing uncommitted `STATUS.md` and `planning/DECISIONS.md` changes, and untracked `planning/checkpoint_2026-10-26/`, were not touched by this run.
