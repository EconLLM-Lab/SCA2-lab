# Paper B voice pass: report

Writer run: profile `writer`, session `local-ee3d9132…`, 60 API calls, all `claude-opus-5-5 provider=anthropic` (agent log; no fallback). The run ended at its 60-iteration limit (exit 1) after the edits and before writing this file and EDITS.md. Part A is the writer's final message, verbatim; Part B is the PM's independent audit (2026-11-03).

## Part A: writer's final message

Nothing is committed or pushed. HF_TOKEN was never printed.

**What I edited**
- Full voice rewrite, following the brief's seven-beat arc: `abstract.tex`, `introduction.tex`, `discussion.tex`, `conclusion.tex`.
  - The "retained benchmark … warrants" framing is gone from every file.
  - The thesis now opens the conclusion and closes the introduction's findings paragraph and the discussion opener.
  - The design argument from FACTS §2 is one introduction paragraph (the survey aggregates people; the model reads at the group level; Kirman and Robinson cited) and one discussion paragraph framing "Order and distribution".
  - The SubPOP/GPO boundary is one sentence. The untested-reading hedge is kept verbatim in spirit.
- Light pass on `background.tex`: it absorbed the Robinson sentence, "stand in" became "answer for", and I split long sentences.
- Sentence-level only on `instrument.tex`, `design.tex`, `results.tex`:
  - I split long sentences and added one motivation sentence before each method.
  - I used the narrator "we" and removed the semicolon antitheses.
  - I removed "bottleneck" (now "evidence that the anchor limits the instrument") and "mechanism inside the network".
  - No sections, figures or tables were reordered, and the table in `design.tex` is byte-identical.
- `references.bib`: added kirman1992 and robinson1950 (checked on Crossref) and zhao2023gpo (author list confirmed on arXiv 2310.11523: Siyan Zhao, John Dang, Aditya Grover).

**Gates (last run, before a final small round of edits)**
These were run after all four full rewrites and the background, instrument and design passes. Afterwards I made four sentence merges in `results.tex` and `design.tex` that touch no macro.
- `latexmk -pdf -halt-on-error main.tex`: exit 0, 0 overfull boxes, 0 undefined references or citations, 0 Float too large. The three new citations resolve in the PDF.
- `audit_numbers.py --out NUMBER_AUDIT.txt`: exit 0, RESULT: PASS (118 claim ids).
- `render_supplement.py` failed under bare python3 (exit 1, ModuleNotFoundError: pandas). Re-run with `uv run --no-project --with pandas`: exit 0. `supplement.tex` was byte-identical afterwards.
- Supplement audit: exit 0, RESULT: PASS (364 ids).
- Fenced files: `git diff --quiet` on the supplement, its template, tables, figures, tools, `main.tex`, `title_page.tex` and submission gave exit 0, so they are unchanged.
- Anonymity grep on `pdftotext main.pdf`: empty (exit 1).
- `check_locks.py`: PASS, with no claim id dropped, no value changed and no citation key dropped.
- All gate outputs and exit codes are in `misc/paper_b/voice_pass/gates/`.

**Voice and word counts**

Voice before → after, measured with `voice_pass/measure.py` on detexed prose:

| File | we per 1k | Connectors per 1k | Mean sentence length (words) |
|---|---|---|---|
| abstract | 5.9 → 11.8 | 0 → 5.9 | 18.3 → 14.1 |
| introduction | 3.5 → 10.2 | 0 → 3.2 | 24.1 → 16.9 |
| discussion | 0.8 → 11.2 | 0.8 → 4.9 | 21.6 → 16.6 |
| conclusion | 3.2 → 11.8 | 0 → 2.9 | 24.2 → 17.9 |
| background | 3.9 → 7.2 | | 21.4 → 17.2 |
| instrument | 2.6 → 7.1 | | 21.7 → 17.2 |
| design | 5.2 → 9.6 | | 24.8 → 16.1 |
| results | 2.5 → 5.2 | | 22.0 → 16.0 |

- Sentences with more than two prose commas: 47 of 402 before, 0 of 600 after. Commas inside [lo, hi] intervals and digit groups are not counted.
- `voice_audit.py`: exit 0 on every file before and after, with zero fail flags. Remaining warnings are `sent_len` (sentences now shorter than the SCA1 band) and `low_we` on background, instrument and results, which are outside the we target.

Main-text word count, by `tools/count_words.py`:

| File | Before | After |
|---|---|---|
| introduction | 1,434 | 1,578 |
| background | 521 | 557 |
| instrument | 768 | 849 |
| design | 2,066 | 2,233 |
| results | 3,643 | 3,710 |
| discussion | 1,240 | 1,438 |
| conclusion | 308 | 332 |
| total | 9,980 | 10,697 |

The abstract is exactly 150 words. The main text is about 400 over the 10,300 allowance. I did not cut silently.

**Proposed cut list (665 words, measured with the repo's tokenizer)**

| Cut | File | Words | What |
|---|---|---|---|
| C1 | discussion | 91 | Delete the "failure profile" paragraph; it restates Results, the introduction and the conclusion. |
| C2 | discussion | ~130 | Compress "evaluation protocol" to its three-way attribution and transfer claims. |
| C3 | introduction | 36 | Drop contribution 3; the two findings paragraphs above already say it. |
| C4 | results | ~85 | Trim the Results roadmap; Table 1 already carries the map. |
| C5 | design | ~77 | Trim the Design opening list; it duplicates Table 1. |
| C6 | background | 65 | Delete "What is left open"; the gap is stated in the introduction. |
| C7 | results | 27 | Move the by-dimension TVD sentence to the supplement. |
| C8 | discussion | 47 | Drop the "value lies in what it makes explicit" pair, which repeats contribution 1. |
| C9 | results | ~64 | Move the label-recovery definitions to the supplement; the values stay in the main text. |
| C10 | results | 43 | Drop the last two sentences of §5.7, now carried by the discussion. |

**Claim ids moved or dropped:** none were dropped or moved.
- One design constant was added to prose: `\dc{42}{countries}` in the introduction. The audit passes, but the brief says no new numbers in prose, so revert it if you read that strictly.

**Term-grep hits kept**
- `design.tex`: "override mechanism" is procedural wording.
- `design.tex`: "causal statement about the instrument" is a correct use, because the bits are assigned by design. It is the existing sentence.

**Decisions for Augusto to confirm**
1. [A? To fit the 150-word cap I dropped "The dimensions are entangled" from the abstract. Entanglement is no longer in the abstract. Restore it at the cost of another clause?]
2. [A? The abstract now ends "We have not tested pre-piloting." It used to say "pre-piloting remains untested".]
3. [A? Results now reads "each sign keeps its intended direction on its own surface, while the size of its effects spreads across the others". This replaces "distinct in direction, mixes in magnitude". Same meaning?]
4. [A? The prospective-validation paragraph now ends on an open question: whether a prospective test would find the signal on trust. Does that read as widening?]
5. [A? To remove commas, the GPS dimensions are now listed in pairs ("trust and risk taking, patience and altruism, …"). That implies groupings the GPS does not make. Revert and treat it as a list exception?]
6. [A? Robinson now appears in the introduction, background and Limits. Is three places too many?]

**Premises in the brief that look wrong**
- The word budget is tight against the brief's own rules. A motivation sentence before each method, two new design paragraphs and splitting every 3-comma sentence together add about 700 words. Hitting 10,300 needs cuts from the list above.
- `render_supplement.py` needs pandas, but the brief's bare-python3 command cannot provide it. The gate should name the `uv run --with pandas` invocation.

**Title options (`main.tex` not touched)**
- "Ordering Countries without Answering Like Their People: A Preregistered Evaluation of Group-Level Synthetic Respondents"
- "Asking a Language Model Only about the Group: Cross-National Order without Respondent Fidelity"
- "Synthetic Cultural Agents as Group-Level Instruments: A Preregistered Evaluation from Anchor to Respondents"

**Helper scripts** I added in `voice_pass/` (inside the fence): `measure.py`, `check_locks.py`, `abstract_words.py`, plus the `audit_before/`, `audit_after/` and `gates/` directories.

## Part B: PM audit (default, claude-opus-5-5, 2026-11-03), on the final tree

**Gates, rerun by the PM after the writer's last edits.**
- `latexmk -pdf -halt-on-error main.tex`: exit 0, 0 overfull, 0 undefined, 0 `Float too large`, 47 pages (was 44).
- `audit_numbers.py`: main PASS; supplement re-rendered with `uv run --no-project --with pandas`, `supplement.tex` unchanged, PASS.
- Anonymity grep on `main.pdf`: 0 hits.
- Claim ids in the eight section files: 144 distinct before and after, none dropped or added.
- Banned-word grep: 2 hits, both pre-existing in `design.tex` ("override mechanism", "causal statement" about assigned bits), both acceptable.
- `, not` grep: 3 hits, all the label "descriptive, not preregistered".
- Abstract 150 words. Fence: only the eight section files, `references.bib`, `NUMBER_AUDIT.txt`, `main.pdf` and `voice_pass/` changed.

**Voice, `voice_pass/measure.py` (HEAD → now).** "we" per 1,000 words: abstract 5.9 → 11.8, introduction 3.5 → 10.2,
discussion 0.8 → 11.2, conclusion 3.2 → 11.8. Connectors 0–1.3 → 2.9–5.9. Mean sentence length 18–25 → 14–18 words.
Sentences with more than two commas: 47 of 402 → 0 of 600. Every brief target met.

**Words: over budget.** 10,697 by `tools/count_words.py` (was 9,980; the brief allowed about 10,300). The writer's
cut list totals about 665 words, which would land near 10,030. Augusto chooses the cuts.

**PM reading: wording to fix (no number changes).**
1. Introduction ¶2: "That route asks a language model for two things it does poorly". The second thing (a sampling
   frame) is a researcher's choice, not something the model does. Proposed: "That route needs two things that are
   hard to supply."
2. Introduction ¶2: "Averaging more of them therefore does not cancel the bias" states an argument as a fact with no
   citation. Proposed: "need not cancel".
3. Thesis ambiguity: "like the survey … unlike the people" can read as if the GPS were not a survey of people. The
   introduction already distinguishes "a benchmark survey" from "the respondents of a second survey". The abstract
   and conclusion should do the same once, for example "orders countries like a benchmark survey while answering
   unlike another survey's respondents". Decision for Augusto.
4. `instrument.tex` (writer's decision 5): the GPS dimensions written in pairs imply groupings the GPS does not
   make. Revert to the plain list and treat it as a list exception to the comma rule.

**Overall.** The pass does what was asked. The organizing question is plain, every paragraph opens on its point,
the design argument is in, and the discussion adds a candid limit the brief did not ask for (the group-level argument
explains why the adapters have no reason to approach the distributions, not why they move away). No number, claim
id or hedge moved. Remaining before commit: Augusto's decisions (the cut list, the six writer `[A?]` items, the four
PM items above), one short writer round to apply them, then a cross-family verifier.

## Part C: Augusto's decisions applied by the PM (2026-11-03)

Augusto: "go with your recommendations", plus "also add the authors".

- **Cuts C1–C10 all applied.** C7 and C9 deleted text the supplement already carries (by-dimension TVD table
  `tab:s-tvd-dim`; the label-recovery note). C9 keeps a one-sentence gloss of recovery and accuracy in the main text.
- **Writer items.** 1–4 accepted as written. 5: the GPS dimensions are a plain list again (the one sentence above two
  commas, a list exception). 6: Robinson now appears in the introduction and background only.
- **PM wording fixes.**
  - "needs two things that are hard to supply";
  - "need not cancel the bias";
  - the abstract and conclusion now name a benchmark survey and a second survey's respondents.
- **Title.** "Synthetic Cultural Agents as Group-Level Instruments: A Preregistered Evaluation from Anchor to Respondents".
  Changed in `main.tex`, `title_page.tex`, `supplement.tmpl.tex` (re-rendered) and `submission/COVER_LETTER_DRAFT.md`.
- **Authors.** The Paper A block (Gonzalez-Bonorino, Biriukova, Capra, with affiliations) was already on
  `title_page.tex`, and the title page's TODO to confirm list and order is still open.
  - `main.tex` shows the authors only when `\showauthors` is defined. The new `main_review.tex` defines it: it is the
    named copy for co-authors and Overleaf.
  - `main.tex` itself stays anonymous for SMR.

**Gates after these edits.**
- Builds: `main` 45 pages, `main_review` 45 pages, supplement 19 pages, title page 1 page. All exit 0, with 0 overfull
  and 0 undefined.
- Number audits: main PASS, supplement PASS.
- Anonymity grep (adds the two co-author surnames): 0 hits on `main.pdf` and `supplement.pdf`. The authors are
  present in `main_review.pdf`.
- Page 1 of the review copy checked visually: clean, with the third author on her own line by the default `\and`
  layout.
- Words: 10,107 (target 10,000). Abstract 150.
- Voice: "we" 10.4–11.7 per 1,000 words in the abstract, introduction, discussion and conclusion. One sentence with
  more than two commas (the list).

## Part D: cross-family verification and its notes (2026-11-03)

Card `t_68631832` (verifier, `gpt-5.6-sol` on `openai-codex`, from its agent log): **PASS-WITH-NOTES**, no blocker
(`voice_pass/VERIFICATION.md`). Its three readability notes were applied by the PM:
- the GPS dimensions in `background.tex` are a plain list (Part C had fixed only `instrument.tex`);
- `discussion.tex` opener now reads "on trust across both scenario banks";
- two short sentence pairs in the conclusion's second paragraph were joined.

The rebuild gives main and main_review 45 pages each, exit 0, 0 overfull and 0 undefined. The number audit passes, the
anonymity grep is empty, and the main text is 10,104 words.
