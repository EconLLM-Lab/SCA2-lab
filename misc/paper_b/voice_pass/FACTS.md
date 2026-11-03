# Paper B voice pass: fact sheet (PM-owned)

Written by the PM (`default`) on 2026-11-02 for the writer's voice pass on `misc/paper_b/`. The thinking is done
here; the writer tells the story. Every number below comes from `planning/sprint_2026-10-11/paper-b-tier1/NUMBERS_TABLE.csv`
(562 rows, sha256 `71ee7c8c…86a4`) by claim id, rounded to three decimals. In the `.tex` files a number is only ever
written through its existing `\cl`/`\ci`/`\dc` macro. **No number, interval, claim status or table changes in this
pass.**

## 0. Purpose and reader

The reader is an SMR referee: a survey methodologist or quantitative sociologist who knows silicon sampling, has
reviewed papers on synthetic respondents, and is sceptical of them. They need to see three things in the first two
pages. What the instrument is for. Why it is built at the level of the group. What it does and does not do when
checked against people.

## 1. Thesis (locked by Augusto, 2026-11-02)

> **Ask a language model only about the group, and it can order countries the way a cross-national survey does
> while answering unlike the people in them.**

Scope that keeps it true (the writer may reword, never widen):
- "Order countries the way a survey does" means the GPS order on **trust**, on the 42 countries, kept on a second
  scenario bank. It does not hold on the other six surfaces.
- "Answering unlike the people" means two separate facts: the adapters' order does not detectably agree with the
  WVS-7 respondents' order, and their answer distributions are farther from the survey than the base model's.
- "Ask only about the group" covers both routes that carry the order: trained adapters **and** a prompt that states
  the same six signs. The thesis is about group-level conditioning on declared signs, not about weights.

## 2. The design argument: why model the group directly (new in this pass)

This is a design rationale, not a result. No new number supports it and none may be invented for it.

**The estimand, in plain words.** Cross-national survey research usually wants a country-level quantity, such as how
countries rank on generalized trust. Silicon sampling reaches it bottom-up: it simulates many individuals from
persona descriptions, then averages them into a country figure. That route needs two things a language model does
poorly. It needs a model of each simulated person, and the errors of those simulated people are correlated (one
model, one set of assumptions), so averaging more of them does not cancel the bias. It also needs a sampling frame:
someone must decide which people to simulate and in what proportions.

**What this instrument does instead.** It never models individuals. A probability survey (the GPS) has already done
the aggregation over people, with sampling weights, which is the job surveys are designed for. The instrument takes
the resulting country-level moments as declared inputs and is asked only for a group-level reading of new item text.
Short version for the writer: *the survey aggregates people; the language model reads items at the level of the group.*

**Why the order can survive without a "representative person".** An ordering of countries only requires the
instrument's score to rise with the group's latent preference. It does not require that a single "representative"
respondent exists whose answers equal the population's.

**The price, stated in the same breath.** A single choice policy per country has no spread within the country built
in. So it can carry an order, but it has no reason to match the distribution of respondents' answers. This is the
representative-agent problem (Kirman 1992). The design therefore *predicts* the paper's order-versus-distribution split.
Use it to frame Section 5.7 and the discussion paragraph "Order and distribution", which currently offers the signs
explanation as an untested aside. Keep that aside's hedge ("we offer one reading without testing it"): the prediction
is an argument, not a test.

**Two boundaries the writer must keep.**
- Country-level agreement says nothing about individuals (ecological inference; Robinson 1950). Keep the existing
  sentences on invariance and individual-level validity (`background.tex` "Cross-national comparability", Limits).
  Move them from hedge to design: we chose the group as the unit, and claims stay at that unit.
- Modelling the group directly is not new on its own. SubPOP (`suh2025`) and Group Preference Optimization (Zhao et
  al. 2023) predict group-level responses without simulating individuals, but they train on human response
  distributions and name the group. What is specific here is the combination: a group-level ordinal reading,
  conditioned only on declared aggregate moments, with the group unnamed at evaluation. Never write "first" or
  "novel".

**Where it goes.** One paragraph in the introduction, after the paragraph on the three features of the construction
or merged into it, and one paragraph in the discussion that frames "Order and distribution". Optionally, one sentence
in the abstract if the 150-word cap allows. The background paragraph "Cross-national comparability" may absorb the
Robinson sentence.

**New bibliography entries** (metadata verified on Crossref and arXiv by the PM, 2026-11-02; add to `references.bib`):
- `kirman1992`: Kirman, A. P. (1992). Whom or what does the representative individual represent? *Journal of
  Economic Perspectives*, 6(2), 117–136. doi:10.1257/jep.6.2.117
- `robinson1950`: Robinson, W. S. (1950). Ecological correlations and the behavior of individuals. *American
  Sociological Review*, 15(3), 351–357. doi:10.2307/2087176
- `zhao2023gpo`: Zhao, S., Dang, J., & Grover, A. (2023). Group preference optimization: Few-shot alignment of large
  language models. arXiv:2310.11523. (The writer confirms the author list on the arXiv page before adding it.)

## 3. Findings, link by link, with the PM's readings

### Link 1: anchor to instrument (what training installs)

| Fact | Value | Claim id |
|---|---|---|
| Label recovery on unseen training-scenario pairs | 0.940 [0.926, 0.952] | `C9_label_recovery_recovery_profile_block` |
| Adapter prefers its own label outright | 0.816 [0.771, 0.856] | `C9_label_recovery_accuracy_profile_block` |
| Base model before training | 0.489 [0.471, 0.506] | `C9_label_recovery_base_accuracy_profile_block` |

**Reading:** training does what it was built to do: it installs each country's synthetic labels on scenarios the
adapter never saw. This is a construction check. It says nothing about GPS order or about people.

### Link 1, continued: the trust order

| Fact | Value | Claim id |
|---|---|---|
| Trust adapter–GPS, cohort-1 adapters | 0.744 [0.500, 0.865] | `B2_cohort1_trust_rho` |
| Same, adapters trained on a second scenario bank | 0.803 [0.615, 0.876] | `B2_bank2_trust_rho` |
| Bank-to-bank agreement, 26 sign cells | 0.907 [0.774, 0.957] | `B2_bank_to_bank_trust_spearman` |
| Prompt stating the same six signs, no adapter | 0.773 [0.584, 0.844] | `PX_signprompt_trust_rho` |
| Prompt naming the country, no adapter | 0.028 [−0.339, 0.381] | `PX_persona_trust_rho` |
| Adapters minus country-named prompt | 0.716 [0.191, 1.154] | `PX_D_cohort1_trust` |
| Adapter minus sign prompt on own items (unresolved) | 0.033 [−0.083, 0.143] | `SP_D_own` |

**Reading:** on trust, conditioning on declared group signs reproduces the GPS order of countries. It does so on a
second bank and whether the signs enter through weights or through a prompt. Naming the country does not. So the
signs carry the order, and the weights get no separate credit. This is the clearest support for the thesis: a
group-level reading built from declared aggregates keeps a cross-national order. **Can say:** declared signs keep the
trust order; a country name does not. **Cannot say:** weights beat prompts; the order holds on other dimensions.

### Entanglement

| Fact | Value | Claim id |
|---|---|---|
| Own effects pointing the wrong way, 64-cell factorial | 0 of 7 | `FX_adapter64_own_effects_wrong_signed` |
| Main-effects prediction vs GPS, trust | 0.834 | `C9_W1_trust_spearman_full_vs_gps` |
| Largest shift from one unseeded retrain | 0.11 profile SDs | `RP_max_abs_surface_diff_sd` |

**Reading:** each sign pushes its own surface the intended way but also pushes the others, often harder. Trust is
the one surface where its own sign dominates. This is a behavioural decomposition: it locates nothing inside the
network, and it does not explain why the other dimensions fail.

### Link 2: the retrospective held-out screen

| Fact | Value | Claim id |
|---|---|---|
| Screen statistic A, 56 adapter-selected items | 0.061 [−0.007, 0.126] | `SCR_A_primary` |
| Permutation p against randomly chosen items | 0.0097 | `SCR_p_perm` |
| A as a share of the wave-6/7 test–retest agreement | 0.081 | `SCR_A_over_ceiling` |
| Sign-prompt arm, same probe | 0.028 [−0.109, 0.158] | `SP_A_primary` |
| Adapter minus Jev, shared items | −0.002 [−0.064, 0.061] | `CMP_jev_D_common` |
| Adapter minus face-valid reader, shared items | 0.020 [−0.181, 0.215] | `CMP_face_valid_D_common` |

**Reading:** the items the adapters pick separate countries a little better than random items with the same labels,
but the signal is weak, and the registered contrasts cannot tell the adapters from careful questionnaire readers.
Always say "retrospective" first: WVS-7 existed before the study and is the only human source. Never "transport".
The 0.081 is a share of survey reliability, not "8% of the maximum".

### Link 3: instrument to respondents

| Fact | Value | Claim id |
|---|---|---|
| Trust adapter–respondents (WVS-7 composite) | 0.295 [−0.044, 0.547] | `C9_a_adapter_human_trust_spearman_rho` |
| Trust GPS–respondents (humans against humans) | 0.351 [0.088, 0.564] | `C9_a_human_gps_trust_spearman_rho` |
| Mean distance to survey answer distributions (TVD): base / adapters / country-named prompt | 0.470 / 0.515 / 0.365 | `C9_TVD_base_mean_tvd_country_equal`, `C9_TVD_adapter_mean_tvd_country_equal`, `C9_TVD_persona_mean_tvd_country_equal` |
| Adapters minus base | 0.045 [0.006, 0.093] | `C9_TVD_adapter_minus_base_profile_block` |
| Country-named prompt minus base | −0.105 [−0.122, −0.086] | `C9_TVD_persona_minus_base_profile_block` |

**Reading:** agreement with respondents is not detected, and the two cross-national sources only loosely agree with
each other even among humans. That loose link is a fact about the anchor and the survey, but it is **not** an upper
bound for the instrument and not "the bottleneck". On distributions the ranking reverses: the adapters move away
from the survey and the country-named prompt moves toward it while carrying no trust order. Section 2 gives the
design reason this is expected. **Can say:** order and distribution are different targets, and here they cross.
**Cannot say:** the country-named prompt matches respondents; the anchor limits the instrument.

### What counts as noise

Profile-block intervals over 26 sign profiles. One unseeded retrain is a narrow comparison for one unit. The human
grouping test is underpowered (`C9_c_human_trust_between_share_multi_member` 0.384, inconclusive). The adapter-minus-
sign-prompt contrast covers zero, so the signs-not-weights reading stands but is not a test of equivalence.

## 4. Intended use (keep its bounds)

The instrument is an inspectable, group-level reading of candidate survey items that a researcher may use beside
human pretesting, as a complement and never in its place. Pre-piloting is untested. The prospective test that would
license more (probe-selected items fielded to people, after the selection and a human-only rule are both declared)
stays in the discussion as written.

## 5. Voice (measured, so it can be checked)

Calibrated targets come from `augusto-academic-voice` (fitted to his published SCA1). The baseline was measured on
this tree with `voice_audit.py` and a comma count on the detexed sections, 2026-11-02:

| Feature | Target (SCA1) | Paper B now |
|---|---|---|
| "we" per 1,000 words | about 17 | 0.8 (discussion) to 5.9 (abstract) |
| Connectors per 1,000 ("That is,", "In other words,", "Notably,", "Therefore,") | about 3 | 0 to 0.8 |
| Mean sentence length | about 20 words | 21.5 to 28.1 |
| 90th-percentile sentence | about 37 words | 34 to 50 (results) |
| Sentences with more than two commas | none (Augusto's rule, 2026-10-31) | 61 of 400 (15%) |

Failure patterns found on a paragraph read (first and last sentence of every paragraph):
- **Late point:** paragraphs open with signposts. "The question has practical weight." "The evaluation has four
  parts." "The evaluation returns a specific profile." "At the second link the evidence changes character."
- **Maxim closers and semicolon antitheses:** "The decomposition describes behavior and locates nothing inside the
  network." "A result at that level would license the use; a result at the level reported here does not." "…the
  present evidence adds a case in which the two cross." Conclusion opener: "Preserving an external benchmark is
  evidence about the link between benchmark and method."
- **Opaque key phrase:** "what a retained benchmark warrants" is the paper's organizing question three times
  (introduction twice, discussion once). Augusto could not parse it. Replace it everywhere with the thesis in §1 and
  plain words ("ranking countries like the GPS", "agreeing with the people who answered the survey").

## 6. Decisions and constraints

- Thesis (a) and the voice samples: Augusto, 2026-11-02, this session.
- Group-level framing in Paper B as design rationale only: PM recommendation, 2026-11-02, accepted with the thesis.
- Magnitude labels, steering and interpretability are Paper C (`planning/DECISIONS.md`, 2026-11-02). Do not mention them.
- Paper B is the journal version of the preprint: never cite it, never write "earlier study".
- Word target 9,000–10,000 on `tools/count_words.py` (now 9,980). This round may run to about 10,300; the writer
  reports a cut list against the excess and does not cut silently.
