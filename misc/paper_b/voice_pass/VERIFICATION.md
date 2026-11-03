PASS-WITH-NOTES

# VP-V — independent verification of the Paper B voice pass

**Artifact under review:** commit `c6c16e7` in `/Users/bonorinoa/Desktop/Github_Repositories/SCA2_PofW-paper-b-draft`, against baseline `3613d82`.

**Fence:** I read the manuscript and built an archived copy of `c6c16e7` under `$TMPDIR/vp-v/tree`. I did not edit any manuscript file. The only repository writes are this report and `voice_pass/verify_probes/`.

**Independent route:** `/Users/bonorinoa/.hermes/profiles/verifier/logs/agent.log`, line 19681, records `API call #26: model=gpt-5.6-sol provider=openai-codex`. The producer was Claude/Opus, so this is a cross-family check.

## Verdict

All seven acceptance checks pass. There is no claims, numbers, anonymity, build, or cut-preservation blocker. The three notes at the end concern one lingering list implication and two clipped sentences; under the card, readability observations are non-blocking.

## 1. Numbers frozen — PASS

- Both the baseline and reviewed numbers tables hash to the locked value:
  `71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4`.
  `git diff --quiet 3613d82 c6c16e7 -- .../NUMBERS_TABLE.csv` exited `0`.
- The independent probe compared the macro multiset in the eight section files at `3613d82` with the reviewed files. There are **226 macro invocations in each**, with no added or removed value/id tuple. It then resolved every current `\cl`, `\clh`, and `\ci` value against the 562-row table using Decimal half-up rounding: **0 mismatches**. The unchanged `\dc` tuples were also accepted by the official design-constant audit.
- The independent full-text comparison found **0 new raw prose numerals** after excluding statistics/design macros, references, citations, equations, and identifiers.
- The repository audit passed with **246 statistics, 0 failures; 240 design constants, 0 failures; 0 unexplained numeric literals**.
- The supplement renderer passed and left `supplement.tex` byte-identical (`37874dc71daae14882a912933962de1e1495a2ec22bdb364a7221aa0b2e17406` before and after). Its audit passed with **709 statistics, 0 failures; 547 design constants, 0 failures; 0 unexplained numeric literals**.

Commands and captured exits:

```text
HF_TOKEN= env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_numbers.py
  exit 0
  Statistics: 246 checked, 0 failures
  Design constants: 240 checked, 0 failures
  Unexplained numeric literals: 0

HF_TOKEN= env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pandas python tools/render_supplement.py
  exit 0
  supplement.tex written

HF_TOKEN= env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_numbers.py --files supplement.tex --out SUPPLEMENT_NUMBER_AUDIT.txt
  exit 0
  Statistics: 709 checked, 0 failures
  Design constants: 547 checked, 0 failures
  Unexplained numeric literals: 0

HF_TOKEN= env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 misc/paper_b/voice_pass/verify_probes/verify_voice_pass.py
  exit 0
```

The audit/render commands ran from `misc/paper_b` in the archived `c6c16e7` tree. The independent probe and its machine-readable result are in `voice_pass/verify_probes/verify_voice_pass.py` and `probe_output.json`.

## 2. Claims inside the lock — PASS

I read the abstract, introduction, discussion, and conclusion sentence by sentence against Amendments C7–C9.1 and `FACTS.md` §3.

- **Weights versus prompt:** the paper expressly says the contrast is unresolved and gives the trained weights no separate credit (`introduction.tex:13,23`; `discussion.tex:5`; `conclusion.tex:5`). It does not claim that weights beat the sign prompt.
- **Order scope:** every positive order claim is restricted to **trust** and the two scenario banks (`abstract.tex:2`; `introduction.tex:13`; `discussion.tex:3,5`; `conclusion.tex:5`). Nothing generalizes this result to the other dimensions.
- **Transport:** there is no transport claim. `introduction.tex:23`, `discussion.tex:15,17`, and `conclusion.tex:9` instead make prospective validation an unrun test.
- **Pre-piloting:** the introduction says it “remains untested”; the discussion calls it a prospective use; the conclusion again says it remains untested.
- **Anchor:** the revised prose calls the anchor loose and separates attribution across anchor, instrument, and respondent links. It does not call the anchor a bottleneck, upper bound, or ceiling.
- **`SCR_A_over_ceiling`:** the text describes a fraction of the *human-to-human ceiling*, not a fraction of a mathematical maximum. No “maximum” reading was introduced.
- **Hedges preserved:** the human screen remains “retrospective”; cross-country and response-shape findings remain “descriptive” or “descriptively” (`introduction.tex:15`; `discussion.tex:17`; `conclusion.tex:7`).
- **Group-level argument:** `discussion.tex:11` says the design “gives us reason to expect” the order/distribution split and closes with “This argument offers one reading of those findings; it does not test their cause.” It is clearly rationale, not a tested empirical result.

## 3. Citations — PASS

The bibliography entries exist and their metadata match the cited works:

- Kirman 1992, *Journal of Economic Perspectives* 6(2), 117–136, DOI `10.1257/jep.6.2.117` (`references.bib:362–371`).
- Robinson 1950, *American Sociological Review* 15(3), 351–357, DOI `10.2307/2087176` (`references.bib:373–382`).
- Zhao, Dang, and Grover 2023, GPO, arXiv `2310.11523` (`references.bib:384–392`).

The uses are substantively aligned with the sources:

- Kirman supports the warning that an aggregate ordering need not be represented by one representative individual.
- Robinson supports the warning against inferring within-group individual behavior from aggregate relations.
- SubPOP predicts population/group answer distributions from group identity and examples; its ACL paper explicitly evaluates human preference distributions.
- GPO learns group preference functions from human group-preference data and adapts with a small preference context; in its OpinionQA/GlobalOpinionQA applications the groups are named/identified and group metadata is supplied to the steered language model. Thus `introduction.tex:9` is correct for the cited survey applications. The sentence should not be read as claiming that a textual group name is a mathematical requirement of every possible GPO deployment.

Primary-source checks used:

- `https://aclanthology.org/2025.acl-long.1028/` and its PDF for SubPOP.
- `https://arxiv.org/html/2310.11523v2` for GPO, including the setup and group-metadata appendix.

## 4. Anonymity — PASS

The sources implement one author gate: `main.tex` shows the author block only when `\showauthors` is defined; otherwise it emits `\author{}`. `main_review.tex` contains only the review marker, `\def\showauthors{1}`, and `\input{main}`.

Fresh `pdftotext` checks found **0** occurrences in both `main.pdf` and `supplement.pdf` of:

- `arXiv`, `2610.06562`, or “earlier study”;
- `Augusto`, `Gonzalez-Bonorino`, `Biriukova`, or `Capra`.

The review and title-page PDFs do contain the expected author names. A source scan of all eight section files found **0** preprint/arXiv/earlier-study hits.

```text
pdftotext main.pdf ...                 exit 0
pdftotext supplement.pdf ...           exit 0
pdftotext main_review.pdf ...          exit 0
pdftotext title_page.pdf ...           exit 0
```

## 5. Builds — PASS

I built a clean `git archive` extraction of `c6c16e7`, not the working-tree PDFs.

```text
HF_TOKEN= env -u PYTHONPATH latexmk -pdf -halt-on-error main.tex
  exit 0 — 45 pages
HF_TOKEN= env -u PYTHONPATH latexmk -pdf -halt-on-error main_review.tex
  exit 0 — 45 pages
HF_TOKEN= env -u PYTHONPATH latexmk -pdf -halt-on-error title_page.tex
  exit 0 — 1 page
HF_TOKEN= env -u PYTHONPATH latexmk -pdf -halt-on-error supplement.tex
  exit 0 — 19 pages
```

A separate scan of all four final LaTeX logs exited `0` and found, for each build, **0 Overfull**, **0 occurrences of “undefined”**, **0 `Float too large`**, and **0 `LaTeX Error`**. The page counts exactly match REPORT Part C: main 45, review 45, supplement 19, title page 1.

## 6. Meaning preserved in cuts C1–C10 — PASS

| Cut | Independent check |
|---|---|
| C1 | The deleted discussion failure-profile paragraph was not the sole statement: the registered screen, failed comparisons, cross-country null, and response-shape result remain in `results.tex`, `introduction.tex:15`, `discussion.tex:3,9,13`, and `conclusion.tex:7`. |
| C2 | The shortened evaluation-protocol paragraph still preserves the three-link attribution and registered/descriptive distinction (`discussion.tex:9`); detailed checks and comparators remain in Results. |
| C3 | The removed contribution-list sentence was duplicative. The trust-order, prompt contrast, screen, and descriptive results remain in `introduction.tex:13–15`, Results, and Conclusion. |
| C4 | The deleted Results roadmap was navigational only; all result subsections and statements remain. |
| C5 | The deleted Design opening list was duplicated by the retained three-link prose and `tab:design-map`; no comparison or registered outcome disappeared. |
| C6 | The shortened background gap paragraph was duplicated by the introduction’s design rationale and limits. No result was removed. |
| C7 | By-dimension TVD evidence is carried by Supplement Table `tab:s-tvd-dim` and its interpretation (`supplement.tex:406–448`), including the four-of-six statement. |
| C8 | The removed contribution wording is restated by the introduction, the evaluation-protocol paragraph, and the intended-use paragraph. |
| C9 | The held-out label-recovery definitions and intervals are carried by `supplement.tex:455–491`; Results also retains the concise recovery/accuracy definitions. |
| C10 | The deleted interpretive close was not the sole order/distribution warning: `discussion.tex:11–13` now gives the full distinction and `discussion.tex:17` retains the limits on magnitudes and within-country variation. |

No cut removed the only statement of a registered result or limit.

## 7. Readability notes — non-blocking

1. `background.tex:5` still says “trust and risk taking, patience and altruism, and positive and negative reciprocity.” That paired syntax can imply three conceptual pairs. REPORT Part C says the dimensions are a plain list again, but only `instrument.tex` was fully unpaired. A plain six-item list would remove the small implication/report mismatch.
2. `discussion.tex:3` — “keeps the GPS order of countries on trust, also on a second scenario bank” is clipped. “...on trust and on a second scenario bank” or “...on trust across both scenario banks” would read more naturally without changing scope.
3. `conclusion.tex:5` contains six consecutive short declarative sentences. The content is accurate, but the paragraph is the closest remaining instance of the pass becoming staccato; joining either the country-name/sign-prompt pair or the final two sentences would smooth it.

These are notes only and do not require reopening the voice pass.

## Final command record

The controlling verifier command was:

```text
HF_TOKEN= env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 \
  python3 misc/paper_b/voice_pass/verify_probes/verify_voice_pass.py
```

Captured exit code: **0**.
