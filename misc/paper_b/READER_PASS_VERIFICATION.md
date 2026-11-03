PASS-WITH-NOTES

# P2-V — independent manuscript and visual-evidence gate

Artifact reviewed: `/Users/bonorinoa/Desktop/Github_Repositories/SCA2_PofW-paper-b-draft` on `paper/paper-b-draft`, working tree at `f5b39ad33ec10b5f6a0cf33f15e8120eeb483951` plus the disclosed uncommitted reader-pass revision.

This is the independent reader verdict. It does **not** verify an online compile or the exact Overleaf target; the PM still owns that check.

## Verdict

**PASS-WITH-NOTES. No blocking finding.** The revision makes a substantive, bounded contribution: it separates anchor retention, instrument behavior, and respondent agreement; differentiates itself from the cited synthetic-respondent and survey-simulation neighbors by its declared-sign construction and fixed-before-human-read screen; and reports an empirically informative failure profile without claiming transport, successful pre-piloting, equivalence, or a neural mechanism. Four empirical charts are integrated at useful points in the Results, reproduce the frozen aggregate table, and remain readable at manuscript print width.

The notes are presentation/provenance notes, not defects that halt packaging:

1. Figure 1 uses a different horizontal scale on each factorial row and has point estimates without uncertainty because no intervals are banked. The figure states both limitations directly and tells readers to compare trained versus prompt within a row, not across rows. This is readable but demands attentive reading.
2. `misc/paper_b/main.tex:5` has a stale source comment saying the C9-4 rows still owe a cross-family audit. The unchanged claim lock records the audit as accepted at `planning/TWO_PAPER_CLAIM_LOCK.md:428-435`. The stale comment does not enter the PDF or alter any claim, but the PM may correct it as mechanical source hygiene.
3. Partial-independence disclosure: the manuscript and core figures were produced on Claude-family routes. The PM-added adversarial tests, regeneration guards, and one metadata correction were Codex-side and therefore are not model-family-independent from this verifier. I did not rely on those tests alone: I inspected the generator/table/TeX linkage and ran a separate aggregate-only probe. A later Claude-family PM acceptance can independently inspect those narrow PM additions.

## 1. Route and fence

Actual serving route is proved by `/Users/bonorinoa/.hermes/profiles/verifier/logs/agent.log:9191` and the bounded capture `review_probes/reader_pass/31_model_route.log`: API call #1 and the latest captured call #35 both report `model=gpt-5.6-sol provider=openai-codex`. I did not open `data/`, `.replication_2026-10-25/`, credentials, raw human exports, model-human joins, the workbench, producer reasoning reports, or Overleaf. I wrote only this report and `misc/paper_b/review_probes/reader_pass/`.

## 2. Frozen scientific surface and baseline scope

Command/log: `misc/paper_b/review_probes/reader_pass/27_scientific_source_freeze.log` — exit 0.

Against baseline `f5b39ad`, `git diff --quiet` returns 0 for `paper_b/`, `planning/TWO_PAPER_CLAIM_LOCK.md`, `planning/PAPER_B_PROTOCOL_DRAFT.md`, and `planning/sprint_2026-10-11/paper-b-tier1/`; there are no untracked files in those scientific scopes. Exact baseline/current SHA-256 equality is recorded for:

- `NUMBERS_TABLE.csv`: `71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4`
- `planning/TWO_PAPER_CLAIM_LOCK.md`
- `paper_b/heldout/PREREGISTRATION.md`
- the accepted C9 and C9-4 verification records.

Thus the reader pass changes presentation/manuscript material, not the frozen numbers, lock, registration, or producing scientific code.

## 3. Figure provenance, exact mapping, coverage, and bounded calculations

Independent command: `HF_TOKEN= env -u PYTHONPATH /Users/bonorinoa/Desktop/Github_Repositories/SCA2_PofW/.venv/bin/python misc/paper_b/review_probes/reader_pass/independent_plot_probe.py`

Captured log: `misc/paper_b/review_probes/reader_pass/10_independent_plot_probe.log` — final exit 0, `RESULT: PASS`.

The independent probe reads only the frozen aggregate table, manifest, manuscript, and generated figure metadata. It does not import the producer generator. It establishes:

- 562 table rows at the locked SHA-256.
- Four empirical figures in the manifest.
- Every plotted point, interval endpoint, reference line, null marker, and printed numeric label maps to the exact named table cell; independent coordinate recomputation finds no mismatch or out-of-axis value.
- Figure 3’s three-link display contains the complete declared set: seven surfaces, two adapter cohorts in both adapter panels, and all seven human–GPS references (35 plotted interval claims). No silent favorable subset replaces the full set.
- Figure 2 retains all six direct screen/comparator contrasts; all six intervals cross zero.
- Figure 1 retains all fourteen trained/prompt own effects and all ten trained/prompt entanglement summaries (24 plotted claims), while explicitly stating that the unbanked full cross-effect matrix is not shown.
- All seven first-cohort adapter–human intervals cross zero; the text correctly says this is not proof of no association.
- The only second-bank interval above zero is trust; the only unadjusted per-dimension screen interval above zero is risk taking; their intersection is empty. The manuscript correctly says no dimension passes both checks.
- Aggregate-only spot arithmetic reproduces the registered one-third reference and all displayed TVD contrasts to floating representation tolerance (maximum absolute residual `1.8E-16`).
- The abstract is exactly 150 words under the document convention (TeX commands excluded).

Producer verification command: `HF_TOKEN= ... build_figures.py --verify` — exit 0, `verify: ok` (`11_build_figures_verify.log`). A second run generated all four TeX/PDF/PNG artifacts from the pinned table into `review_probes/reader_pass/fresh_figures/` with every `pdflatex -halt-on-error` and `pdftoppm` subcommand at exit 0 (`28_fresh_figure_generation.log`); fresh verification also exits 0 (`29_fresh_figure_verify.log`). `cmp -s` returns 0 for each of the four TeX files, four PDFs, four PNG previews, and the full manifest against the manuscript’s shipped artifacts (`30_fresh_figure_comparison.log`). Thus the inspected PDFs are the actual generator outputs, not stale presentation files.

Paper-tool suite: four focused test modules, 38 tests — exit 0, `38 passed` (`12_paper_tool_tests.log`).

Generator mutation command: `generator_mutation_probe.py` — exit 0 (`25_generator_mutation_probe.log`). A clean copied generator suite first exits 0; reversing the TeX coordinate transform in the copied generator makes the suite exit 1 at `test_mutating_coordinate_transform_is_caught`. The probe deletes copied bytecode before the mutant run so a same-size, same-timestamp edit cannot be hidden by stale `.pyc` reuse.

## 4. Number audits, builds, references, anonymity, and length

All builds ran in `misc/paper_b/review_probes/reader_pass/build_copy/`, not over the producer artifacts.

- Main number audit: exit 0 (`13_main_number_audit.txt`).
- Supplement number audit: exit 0 (`14_supp_number_audit.txt`).
- Main build: `latexmk -pdf -halt-on-error -interaction=nonstopmode main.tex`, exit 0 (`17_main_build.log`).
- Supplement build: same halt-on-error command for `supplement.tex`, exit 0 (`18_supp_build.log`).
- Independent log scan: exit 0 (`23_log_anonymity_check.log`): zero LaTeX errors, undefined citations, undefined references, overfull boxes, and `Float too large` warnings in both documents.
- `pdftotext` anonymity scan: exit 0; no author names, `arXiv`, preprint identifier, or “earlier study” in main or supplement.
- Reproducible main-text count: 9,980 words (`15_word_count.log`), within the requested roughly 9–10k target.
- Abstract: 150 words under the manuscript convention.

The captured exit ledger is `misc/paper_b/review_probes/reader_pass/01_command_exits.log`. It retains two superseded probe-development failures rather than hiding them: the first independent word-count check counted the TeX command `\\noindent` as a word (exit 1; corrected to the document convention, recheck exit 0), and the first same-size generator mutant reused copied bytecode (exit 1 of the harness, not a green mutant); deleting copied `__pycache__` before the mutant run produced the authoritative red mutant and final probe exit 0.

## 5. Skeptical visual read

Freshly built whole pages 24, 27, 31, and 33 were rendered at 150 dpi and inspected, not merely inferred from source. These contain the factorial, retrospective screen, three-link forest, and order-versus-distance figures respectively.

All four figures are legible at page width. Axes, directions, sample-size exceptions, interval units, cohort encodings, comparator overlap counts, and metric distinctions are visible. No plot, caption, legend, or note is clipped; no caption collides with the page number/footer. The earlier Figure 1/Figure 4 float overflow is absent from both the fresh log and the whole-page render.

The figures are used at useful locations: the factorial follows the factorial results; the screen follows the registered screen results; the three-link forest introduces the descriptive respondent-composite subsection; and the route/TVD comparison follows the order-versus-distance results.

## 6. Interpretation gates

Independent reading of `introduction.tex`, `results.tex`, `discussion.tex`, `conclusion.tex`, C9.1, and the registration finds the required distinctions intact:

- C9/descriptive analyses are labeled descriptive, retrospective, and not preregistered.
- The registered held-out screen is not described as transport or demonstrated pre-piloting; prospective validation remains untested.
- Separate permutation results are not used to infer a significant adapter–prompt difference; the direct contrast is shown and called unresolved.
- Comparator intervals crossing zero are not presented as equivalence; the manuscript explicitly warns against that reading and reports the small common-item counts.
- Cohort-1 adapter–human null intervals are not proof of absence.
- Trust retention is paired with the sign-prompt result and the unresolved direct screen contrast; trained weights are not credited over prompting.
- Trust-only anchor ranking and full-battery TVD are distinguished in both figure and prose.
- The base model’s undefined rank correlation is not plotted as zero and no base-country rho is invented.
- Human–GPS is a scale reference, not a ceiling or bottleneck.
- The own-sign ordering is labeled mechanical rather than an independent learning result.
- The factorial/decomposition is behavioral and explicitly says it locates nothing inside the network.
- `Var(cross)/Var(full)` is called a variance ratio, not percent explained; the above-one case is explained by covariance.

## 7. Contribution relative to cited neighbors

The introduction and background do not claim that synthetic respondents, distribution matching, country prompting, survey pretesting, or the general need for human validation are novel. They cite those neighboring literatures and make a narrower contribution: a declared-sign conditioning construction plus a reusable link-by-link validation protocol whose probe/selection is fixed before the human criterion is read, followed by a concrete empirical profile in which anchor order and respondent-distribution distance diverge. That contribution is substantive and accurately bounded to one anchor, instrument family, base model, and retrospective survey criterion.

## What remains outside this verdict

- No online/Overleaf compile or exact canonical-project inspection.
- No raw-data or model-human-join recomputation.
- No GPU re-scoring or repetition of the completed scientific experiments.
- No claim that the point-only factorial differences are statistically distinguishable where no interval is banked.
