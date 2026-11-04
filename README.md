# SCA2_PofW — Synthetic Cultural Agents from Aggregate Anchors

**EconLLM Lab** · [econllm-lab.com](https://www.econllm-lab.com/) · [github.com/EconLLM-Lab/SCA2_PofW](https://github.com/EconLLM-Lab/SCA2_PofW)

We build language-model instruments from declared aggregate anchors. Country signs from the Global Preferences
Survey (GPS) label one shared bank of synthetic preference pairs. Each sign profile is then written into a small DPO
adapter, which reads World Values Survey (WVS) Wave 7 items with no country named in the prompt.

This repository is the methods archive for that program. It is not a packaged product or a one-click trainer.

---

## Papers

| Paper | Question | Read | Source of record |
|---|---|---|---|
| **A**: *Synthetic Cultural Agents from Aggregate Anchors* (Gonzalez-Bonorino, Biriukova, Capra) | How to build the instrument (16 countries) | [arXiv:2610.06562](https://arxiv.org/abs/2610.06562) (v1, 2026-10-05) | Sealed upload package [`misc/arxiv-submission-2026-10-05/`](./misc/arxiv-submission-2026-10-05/) and tag `arxiv-2610.06562-v1` |
| **B**: the journal version of A | A preregistered evaluation of the instrument, from anchor to respondents (42 countries, two scenario banks) | In preparation. The current build is [`misc/paper_b/main.pdf`](./misc/paper_b/main.pdf) with [`supplement.pdf`](./misc/paper_b/supplement.pdf) | [`STATUS.md`](./STATUS.md), [`planning/TWO_PAPER_CLAIM_LOCK.md`](./planning/TWO_PAPER_CLAIM_LOCK.md) |
| **C** | What training adds once the anchor is stated | Preliminary, not yet registered | Branch `feat/paper-c-magnitude` |

Paper A's headline, on sixteen countries and twenty-three WVS items: the trust adapter–GPS Spearman correlation is
**0.74** [0.44, 0.88]. That is coarse sign transfer, not recovery of magnitudes within a sign.

Earlier drafts of Paper A (`misc/position_paper/`, `planning/rewrite_pre_*`) were removed in the 2026-11-03 hygiene
pass. They are identical to, or older than, the sealed package, and git history keeps them.

---

## Start here

| If you need… | Go to |
|---|---|
| Where every workstream stands | [`STATUS.md`](./STATUS.md), then [`planning/DECISIONS.md`](./planning/DECISIONS.md) |
| Reproduce Paper A's committed tables (no GPU) | [`replication/README.md`](./replication/README.md) |
| Obtain the survey data (not shipped) and our Hugging Face artifacts | [`DATA.md`](./DATA.md) |
| Set the project up with an AI agent | [`REPLICATE_WITH_AN_AGENT.md`](./REPLICATE_WITH_AN_AGENT.md) |
| The Paper B cohort runner and readout | [`paper_b/README.md`](./paper_b/README.md) |
| Protocol and sign-labelling CLI | [`sca2/README.md`](./sca2/README.md), [`protocols/`](./protocols/) |
| Synthetic pair generation | [`synthetic_generation/README.md`](./synthetic_generation/README.md) |
| Historical phase-1 notebooks | [`DPO_train_test/`](./DPO_train_test/), [`DPO_eval_WVS/`](./DPO_eval_WVS/). Not the papers' result tables |
| Manuscripts and talks | [`misc/README.md`](./misc/README.md) |

The `sca2` CLI audits a frozen protocol. `train`, `eval` and `generate --materialize` refuse execution by design.

## Branches

```
main ─► feat/paper-b-cohort ─► paper/paper-b-draft      Paper B code, then manuscript
                     └──────► feat/paper-c-magnitude     Paper C (preliminary)
main ─► Adapter-Brain-Vizualization                      the visualization workbench (independent stream)
```

The workbench reads Paper B artifacts one way. Paper B claims never depend on workbench results.

---

## What is public vs local

| Object | Where | Public? |
|---|---|---|
| Code, protocol, committed analysis tables and figures | this repository | Yes (MIT) |
| Paper A adapter weights | Hugging Face [`Bonorinoa/SCA2-phase2-adapters`](https://huggingface.co/Bonorinoa/SCA2-phase2-adapters), commit `03c43dfd27c9535283feb78ffa727da3bfa1b966` | Released behind a gate (Hugging Face account and acceptance required) |
| Paper B adapters and artifacts | Hugging Face, private datasets | Not yet |
| Sixteen-country option probabilities | [Drive download](https://drive.google.com/uc?export=download&id=1lIAx0ueSpgaZPmAzNbFSD31ddGQH7Nqo) | Model outputs only. Not the source of the 0.74 headline |
| GPS country and individual files | briq / Falk et al. (2018) | Obtain from the source. Not redistributed |
| WVS Wave 7 microdata | World Values Survey Association | Obtain from the source. Derived respondent extracts are not shipped; rebuild with `data/wvs_eval_full/_build_wvs_eval_full.py` |

`analysis/phase2/reproduce_tables.py` reprints Paper A's headline from
`analysis/phase2/outputs/paper_a/country_item_scores.csv`. Do not use the file marked `SUPERSEDED` in that folder.

## Design in one paragraph

Country information enters only as GPS `sign(z)` labels on a **shared** scenario bank, so magnitudes inside a profile
do not change the labels. Evaluation prompts omit country names. That closes a prompting channel, not pretrained
associations. Pairwise DPO identifies an ordering, not population marginals. The instrument reads the group directly
and never simulates individual respondents, so it carries no spread within a country.

## Scope

Reliable uses, when the tests support them: scoring new item text against a declared anchor, mapping where two
batteries share a construct, and fixed-policy proximity to survey distributions.

Unreliable uses: speaking for individuals, recovering the shape of response distributions, causal or policy
counterfactuals, and treating adapters as national cultures.

---

The study had no funding. No author has a competing interest.

## License

- **Code**: MIT. See [`LICENSE`](./LICENSE).
- **Manuscripts, figures and text**: CC BY 4.0 unless the publisher's terms say otherwise. Paper A's arXiv license
  governs its arXiv version (see the [arXiv listing](https://arxiv.org/abs/2610.06562); it currently shows arXiv's
  non-exclusive distribution license).
- **Third-party survey data** (WVS, GPS, LAPOP and others): under their distributors' terms, not redistributed here.
  See [`DATA.md`](./DATA.md).

To cite, use [`CITATION.cff`](./CITATION.cff) (Paper A).
