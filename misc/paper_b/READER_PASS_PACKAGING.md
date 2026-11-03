# P2-P: PM acceptance and standalone archive for the reader pass

Card `t_8ef9f8af`, 2026-10-26, PM (`default`). Worktree `SCA2_PofW-paper-b-draft`, branch `paper/paper-b-draft`,
baseline `f5b39ad`; the revision is the uncommitted working tree. No git commit, push, browser action or install.

## Verdict

**ACCEPT (local).** The independent verdict is `PASS-WITH-NOTES` with no blocker (`READER_PASS_VERIFICATION.md`, card
`t_c7132463`). I re-checked its evidence and the revision myself, and the gates below pass. **Online: NOT YET VERIFIED.**
The canonical Overleaf project https://www.overleaf.com/project/6add7bb3bb4924e2a5e31ad3 has not been updated. Card
`t_5b4c1784` owns the upload, the fresh online compile and the page-count comparison. Update that project in place; do
not create a new one.

## Model routes (from the agent logs, not the card pins)

Evidence: `~/.hermes/cache/scratch/paper-b-reader-pass/pm_model_routes.log`. Sessions come from the board's
`owner_admitted` events, and each `API call #N: model=… provider=…` line was counted per session.

| Card | Profile | Session(s) | Calls served |
|---|---|---|---|
| figures `t_689a0e21` | creative | `local-5938e543…`, `local-254b6768…` | 17 + 28, all `claude-sonnet-5-5 provider=anthropic` |
| writer `t_97b9df2c` | writer | `local-92fbd160…`, `local-e0af8415…` | 61 + 28, all `claude-sonnet-5-5 provider=anthropic` |
| verifier `t_c7132463` | verifier | `local-c13b95ae…` | 40, all `gpt-5.6-sol provider=openai-codex` |
| this acceptance | default | `local-e9adf501…` | all `claude-opus-5-5 provider=anthropic` (one log line matching `gpt-5.6-sol` is my own tool output echoing the verifier log, not an API call) |

The producers (Claude) and the verifier (Codex) are different model families. One narrow exception: the PM-authored
tests, verify guards and metadata fix are Codex-side, so the verifier was same-family for that slice. The complementary
Claude check of that slice is below.

## Disposition of reviewer notes

| # | Note | Disposition |
|---|---|---|
| 1 | Figure 1 uses row-specific scales and shows points without intervals (none are banked) | Accepted by the PM as an explicit presentation constraint; no owner scientific decision was needed. The figure states both limits. No change. |
| 2 | Stale comment at `main.tex:5` says C9-4 "still owe a cross-family audit" | **Fixed mechanically.** The comment now cites the accepted audit (card `t_b4030219`, the lock's C9-4 append-only note, lines 428–435): "descriptive, not preregistered". The line is a non-rendered comment, so no prose, number or claim changed and the lock was not edited. Audits and builds were re-run after the edit (below). |
| 3 | The PM-added tests, guards and metadata are only partially independent of the verifier | **Complementary Claude check done.** I read `tools/test_build_figures.py` (15 tests) and `verify()`. Probe `pm_gate/13_pm_claude_probe.log`, exit 0: (a) I gave a corrupted generator (trust ρ forced to 0.5) consistent output, so the regeneration-equality guard reports 0 errors; the independent per-cell table check still reports 4 errors naming that claim. The two guards are therefore not redundant. (b) A clean control reports 0 errors. (c) Screen panel A's quantity reads "mean signed Spearman agreement with WVS-7 human country differences". That matches design surface H ("signed agreement of selected items with human country means"), so the metadata fix is semantically right. |

PM visual read of the four previews (vision model, aggregate figures only). Every figure is legible, with no clipping
and no plotted values off the axis. Optional polish, **not blocking and not routed**:
- Figure 3: the legend markers are grey rather than the panel colours, and the risk-taking `n` footnote has ragged
  spacing.
- Figures 2C and 4C reuse a route's marker for a contrast row.
- Figure 1B: the two equal values (2 and 2) overlap.

No caveat or number depends on any of these.

## Independent content checks (diff against `f5b39ad`)

- **Charts.** Four empirical figures are placed in Results: factorial own effects, retrospective screen, three links,
  and order versus distance. All four are `figures/*.pdf` generated from the pinned table. `build_figures.py --verify`
  passes, and the verifier's fresh regeneration matched them byte for byte.
- **Contributions.** There are three, and each is bounded: an inspectable conditioning method, a reusable link-by-link
  evaluation protocol, and a specific failure profile. The text closes with "one anchor, one instrument family and one
  base model".
- **Registered versus descriptive.** The separation is intact:
  - The design table labels H "Preregistered; retrospective criterion" and D "Descriptive, not preregistered".
  - `results.tex:65` says "None is preregistered and none enters a registered family".
  - The captions of Figures 3 and 4 say "descriptive, not preregistered".
  - The introduction says the fourth part was "added after the registered results had been read".
- **Caveats.** None was removed to manufacture a success:
  - "Retrospective" is kept for every held-out result. "Transport" appears 0 times.
  - The sign-prompt contrast is still "unresolved", and the text "cannot credit the trained weights over a prompt".
  - Pre-piloting stays prospective and untested.
  - The decomposition "locates nothing inside the network".
  - Human–GPS is "neither an upper bound", read as "a reference for scale".
  - Null intervals are "not proof" and not equivalence.
  - Var(cross)/Var(full) is called a ratio.
  - The Limits paragraph was condensed, but it keeps all five limits.
- **Claim ids.** 52 claim ids left the main text when the comparator, factorial and human tables were replaced. A spot
  check of each family found every one in the rendered supplement or the figure manifest. No new id outside the table
  appears, and both audits pass.
- **Frozen sources.** `pm_gate/01_frozen.log`, exit 0. These files are byte-identical to `f5b39ad`:
  - `NUMBERS_TABLE.csv` `71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4`
  - `planning/TWO_PAPER_CLAIM_LOCK.md` `9e2f76afaecb6164c556a03b574fdd2d81835746ffe7b24f9e041ed66c11a704`
  - `paper_b/heldout/PREREGISTRATION.md` `7066ba81d5170428ecfe330426e1e70141a01d65567a908b37890b2d0e1b8d4c`

  `git diff --quiet` is clean on `paper_b/`, the lock, the protocol and `paper-b-tier1/`, with no untracked file in those
  scopes.

## Commands and exits

Scripts: `~/.hermes/cache/scratch/paper-b-reader-pass/pm_gate.sh` and `pm_package.sh`. Logs are in `pm_gate/`. Every
command ran with `HF_TOKEN=` blank, `PYTHONDONTWRITEBYTECODE=1`, `env -u PYTHONPATH`, the main checkout's `.venv` Python
and the scratch `TMPDIR`.

| Step | Exit | Result |
|---|---|---|
| Frozen-source check | 0 | 3 sha256 equal; scientific scopes clean |
| `render_supplement.py` → scratch, `cmp` with `supplement.tex` | 0 | byte-identical (the tool's final relative-path print raises for an out-of-repo `--out` after it writes; the byte comparison is the check) |
| Paper tools: `test_build_figures`, `test_audit_numbers`, `test_render_supplement`, `test_anonymize_prereg` | 0 | 38 passed |
| `build_figures.py --verify` | 0 | `verify: ok` |
| Claude-side probe of the PM guards | 0 | PASS |
| `audit_numbers.py --out NUMBER_AUDIT.txt` | 0 | PASS, 118 claim ids, 0 unexplained numerals |
| `audit_numbers.py --files supplement.tex --out SUPPLEMENT_NUMBER_AUDIT.txt` | 0 | PASS, 364 claim ids, 0 unexplained numerals |
| `latexmk -g -pdf -halt-on-error` main / supplement / title_page (source dir) | 0 / 0 / 0 | 44 / 19 / 1 pages; errors, overfull, undefined, `Float too large` and rerun counts all 0 |
| `pdftotext` anonymity grep (author name, arXiv, preprint id, "earlier study"), main and supplement | 0 | 0 hits; `main.tex` does not input `title_page` |
| Abstract words (TeX commands excluded) | 0 | 150 |
| `tools/count_words.py` | 0 | main text 9,980 words |
| `anonymize_prereg.py` → scratch, `cmp` | 0 (cmp) | byte-identical to `submission/PREREGISTRATION_anonymized.md` (same relative-path print quirk; the tool's exit is 1 after writing) |
| Full suite, main checkout (`feat/paper-b-cohort` `e85176e`, `paper_b/` clean): `HF_TOKEN= PYTHONDONTWRITEBYTECODE=1 env -u PYTHONPATH .venv/bin/python -m pytest paper_b -q` | 0 | **613 passed in 185.32s** (`pm_final_pytest.log`) |
| `paper_b/test_status_doc.py` (paper worktree, after the STATUS edit) | 0 | 6 passed |

## Archive

- **Dependencies.** Discovered recursively from the `latexmk -recorder` `.fls` files of the three targets plus
  `\bibliography`: 19 files. They are 13 `.tex` (main, rendered supplement, title page, 9 sections, `macros.tex`),
  `tables/tab_checks.tex`, `references.bib` and 4 `figures/*.pdf`.
- **Review material.** `review/` holds `NUMBER_AUDIT.txt`, `SUPPLEMENT_NUMBER_AUDIT.txt`, `OUTLINE.md`,
  `PREREGISTRATION_anonymized.{md,pdf}` and `COVER_LETTER_DRAFT.md`.
- **Authoring input.** The parent added `supplement.tmpl.tex` and `ARCHIVE_README.txt` after the initial package pass, preserving both the supplement's authoring template and its buildable rendered source. The template is not itself a LaTeX entry point; regeneration requires the canonical repository and frozen table.
- **Excluded.** `data/`, CSVs, build debris, figure `.tex`/`.png` sources, tools and internal reports. A credential-pattern scan found nothing.
- **Final ZIP.** `/Users/bonorinoa/.hermes/cache/scratch/paper-b-reader-pass/PaperB_reader_pass.zip`, no wrapper folder, **27 file entries**, sha256 `237d0c3a827b3fc8293f1195efc7696fff4d0a6909f9a17dca2769042e767be6`, **573,580 bytes**. This supersedes the initial 555,774-byte archive.
- **Input hash.** The sha256 of the per-file manifest lines is `66d62d22f576ce90e630a7b716a6162cd726e435325c3db1b8cebd39e8153a12`. Per-file sha256 and sizes are in `ARCHIVE_MANIFEST.txt` in the same directory.
- **Final closure.** The parent extracted the **finished updated ZIP** into the fresh empty directory `…/paper-b-reader-pass/extract_check_final_with_template/` and compiled main, supplement and title page with `latexmk -pdf -halt-on-error -interaction=nonstopmode`. All exited **0**, with **44 / 19 / 1 pages** and **0 blocking log findings** (LaTeX errors, overfull boxes, undefined references/citations, oversized floats). Main/supplement anonymity checks passed. Exact results: `…/paper-b-reader-pass/final_archive_closure.json`; logs: `final_closure_{main,supplement,title_page}.console.log`.
- **Deliverable PDFs.** Final closure-built copies are `…/paper-b-reader-pass/main.pdf` and `supplement.pdf`.

## Final source diff (working tree against `f5b39ad`; nothing committed)

- **Modified:** `STATUS.md`, `planning/DECISIONS.md`, and these files under `misc/paper_b/`: `NUMBER_AUDIT.txt`,
  `SUPPLEMENT_NUMBER_AUDIT.txt`, `REWRITE_LOG.md`, `abstract.tex`, `background.tex`, `backmatter.tex`, `conclusion.tex`,
  `design.tex`, `discussion.tex`, `instrument.tex`, `introduction.tex`, `main.tex`, `main.pdf`, `results.tex`,
  `supplement.tmpl.tex`, `supplement.tex`, `supplement.pdf`, `tables/tab_checks.tex`.
- **Deleted:** `tables/tab_comparators.tex`, `tab_factorial.tex`, `tab_human.tex`. The figures and the supplement
  replace them.
- **Untracked:** `figures/` (4 × tex/pdf/png plus `PLOT_MANIFEST.json`), `tools/build_figures.py`, `count_words.py` and
  `test_build_figures.py`, `FIGURE_BUILD_REPORT.md`, `FIGURE_PM_CHECKS.md`, `READER_PASS_REPORT.md`,
  `READER_PASS_VERIFICATION.md`, `review_probes/reader_pass/`, this file, and
  `planning/checkpoint_2026-10-26/cards/P2_*.md`.
- **This card's own edits:** the `main.tex` comment (note 2); the STATUS Manuscript paragraph and two Open rows; this
  report; the re-run audit files; and the rebuilt `main.pdf` and `supplement.pdf`. I deleted my transient
  `title_page.pdf` and its build debris so that no new untracked file is left behind.

## Not covered by this acceptance

The online compile, a comparison with the Overleaf snapshot in `~/Downloads` (the terminal cannot read it), any git
commit or push, and any raw-data recomputation.
