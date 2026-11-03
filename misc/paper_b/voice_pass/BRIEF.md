# Writer brief: Paper B voice pass ("Synthetic Cultural Agents as Measurement Instruments", SMR)

Written by the PM (`default`) on 2026-11-02. Owner: Augusto González-Bonorino. Run on Opus
(`-m claude-opus-5-5 --provider anthropic`, the ASU seat), because the earlier Sonnet passes drifted from his voice.

## Five-field handoff

**Root.** `/Users/bonorinoa/Desktop/Github_Repositories/SCA2_PofW-paper-b-draft` (branch `paper/paper-b-draft`),
manuscript in `misc/paper_b/`. Read in this order:
1. this file;
2. `misc/paper_b/voice_pass/FACTS.md`, the binding fact sheet: thesis, design argument, readings, can and cannot say,
   voice baseline;
3. the voice samples in `/Users/bonorinoa/Hermes/Projects/SCA2/voice_samples/` (README first; the Construct-Identified
   Inference post is the closest match). These are read-only and must never be copied into the repo;
4. the skill `augusto-academic-voice` (in your profile), and both `~/.hermes/skills/productivity/prose-coauthoring/references/prose-failure-modes.md`
   and `~/.hermes/skills/productivity/prose-coauthoring/references/research-prep-notes.md` ("Voice markers");
5. the manuscript files you edit, plus `misc/paper_b/OUTLINE.md` for the venue rubric.

**Acceptance.**
- **Thesis.** The abstract, introduction, discussion and conclusion land the thesis in FACTS §1. You may reword it,
  but you may not widen its meaning. The phrase "retained benchmark" and its variants ("what … warrants") are gone
  from every file.
- **Design argument.** FACTS §2 enters as one introduction paragraph and one discussion paragraph framing "Order and
  distribution", plus at most one abstract sentence if the 150-word cap allows. Add the three bib entries, after
  confirming the GPO author list on arXiv.
- **Scope of edits.**
  - Full voice rewrite: `abstract.tex`, `introduction.tex`, `discussion.tex`, `conclusion.tex`.
  - Light pass only: `background.tex` (it may absorb the Robinson sentence).
  - Sentence-level only: `instrument.tex`, `design.tex`, `results.tex`. Split long sentences, add one plain sentence
    of motivation before each method, and use the narrator "we". Do not reorder sections, figures or tables.
- **Voice.** The paper uses the multi-author "we". Write it as a story the authors tell, as in
  "we built…, we expected…, we found…". Take the following from the samples:
  - motivation before method, in one plain sentence;
  - his connectors ("That is,", "In other words,", "Therefore,", "Notably,");
  - candour about what a metric hides;
  - restraint stated as a choice ("we do not read this as…");
  - at most one framing question per major section.
  Leave out the essays' "I", asides and humour.
- **Voice targets** (FACTS §5), measured on each edited file:
  - "we" at 10 or more per 1,000 words in the abstract, introduction, discussion and conclusion;
  - connectors at 2 or more per 1,000 words;
  - mean sentence length at or under 22 words;
  - no sentence with more than two commas (split it). The only exceptions are sentences that list macros or
    interval pairs; list them.
- **Paragraph rules.** The first sentence of each paragraph states its point. No maxim closers and no semicolon
  antitheses. End a paragraph on what the finding means or on the open question. No contrastive kicker of the form
  "X, not Y": state the positive claim, and put the contrast in the next sentence.
- **Numbers and claims frozen.**
  - Every `\cl`, `\ci` and `\dc` macro keeps its value and claim id.
  - Do not add a new number to prose. Do not drop a claim id from the main text without listing it.
  - Hedges stay ("retrospective" first; "descriptive"; "we offer one reading without testing it"), as do the
    interval readings in FACTS §3 and the can/cannot lists.
  - Supplement, tables and figures are untouched.
- **Words.** The main text is now 9,980 by `python3 tools/count_words.py`. It may go to about 10,300 this round. Report
  per-file counts before and after, plus a proposed cut list for anything above 10,000. Do not cut silently. The
  abstract stays at or under 150 words.
- **Gates** (all from `misc/paper_b`, `HF_TOKEN=` blank, `env -u PYTHONPATH`):
  - `latexmk -pdf -halt-on-error main.tex`: exit 0, with 0 overfull boxes, 0 undefined references or citations, and 0
    `Float too large`.
  - `python3 tools/audit_numbers.py --out NUMBER_AUDIT.txt` reports `RESULT: PASS`. Run
    `tools/render_supplement.py`, then `tools/audit_numbers.py --files supplement.tex --out SUPPLEMENT_NUMBER_AUDIT.txt`,
    which also reports PASS (the supplement must be unchanged).
  - `pdftotext main.pdf - | grep -i -E "arxiv|2610\.06562|earlier study|gonzalez|bonorino"` is empty.
  - `grep -n -i -E "transport|bottleneck|earlier study|novel|first to|we introduce|histogram|stand-in|stereotype|causal|mechanis|retained benchmark|warrant" <edited .tex>`:
    explain every hit or remove it.
  - The `voice_audit.py` table before and after for each edited file, plus the comma count.

**Artifact.**
- The edited `.tex` files and `references.bib`, in place.
- `misc/paper_b/voice_pass/REPORT.md` containing:
  - the gate outputs with exit codes;
  - the voice before/after table and word counts;
  - a list of decisions for Augusto to confirm (any sentence where you guessed his judgement, marked `[A? …]` in
    the report, at most 6);
  - claim ids moved or dropped;
  - the proposed cut list;
  - title options that fit the thesis (propose; do not change `main.tex` or `title_page.tex`);
  - any premise in this brief you think is wrong;
  - the model route read from your agent log.
- `misc/paper_b/voice_pass/EDITS.md`: one row per changed paragraph in document order (file · old first sentence ·
  new first sentence · why), so Augusto can review by paragraph.

**Fence.**
- Write only:
  - the eight section files named above;
  - `references.bib`;
  - `NUMBER_AUDIT.txt` and `SUPPLEMENT_NUMBER_AUDIT.txt`;
  - build outputs (`main.pdf`, `supplement.pdf`, aux files);
  - `misc/paper_b/voice_pass/`.
- Do not touch:
  - `supplement.tmpl.tex`, `tables/`, `figures/`, `tools/`, `main.tex`, `title_page.tex`, `submission/`;
  - anything outside `misc/paper_b/`;
  - `data/` and any human-survey file;
  - Overleaf.
- **Do not commit, push or merge**: the PM audits and commits. Never print `HF_TOKEN`.

**Locks.**
- Claude only via the ASU seat.
- Paper B is the journal version of the preprint and never cites it.
- Terms come from `augusto-academic-voice`:
  - "response distributions" (never histograms);
  - "synthetic respondents";
  - "scoring instrument" or "choice policy";
  - "declared aggregate moments";
  - DPO read as a regularized Bradley–Terry choice model;
  - construct, measure and anchor kept apart.
- No mention of magnitude labels, steering or Paper C.
- If any part of FACTS or this brief looks wrong, say so in the report instead of complying silently.

## Thesis (locked)

> Ask a language model only about the group, and it can order countries the way a cross-national survey does while
> answering unlike the people in them.

## Arc for the introduction (about 1,500 words; a story map whose order is the argument)

| # | Paragraph carries | Notes |
|---|---|---|
| 1 | The problem: cross-national programs commit to items before they learn whether the items separate countries, and language models offer a cheap first reading | Motivation first, plain words |
| 2 | Why the usual route struggles: simulate individuals, then aggregate (FACTS §2) | Cite the existing silicon-sampling literature |
| 3 | Our route: the survey aggregates people, the model reads items at the level of the group; the three features of the construction | Design argument; SubPOP/GPO boundary in one sentence |
| 4 | How we evaluate it: three links, preregistered, 42 countries, a second bank | Keep the four-part design compressed |
| 5 | What we found, as the thesis: the order holds on trust and the signs carry it; answers move away from people | Readings from FACTS §3 |
| 6 | Contributions (numbered list allowed) and bounds | Keep "complement, never replacement" |
| 7 | Roadmap | One or two sentences |
