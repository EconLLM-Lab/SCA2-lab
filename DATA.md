# DATA.md — how to obtain the data

This repository ships **code, synthetic data and model outputs only**. It does not ship survey microdata,
questionnaires, codebooks, or values computed from survey respondents. Each source has its own terms, and those terms
forbid redistribution, so you download each one yourself. All of them are free for academic use after registration.

Place every file at the path in the table. The code reads those paths, and `.gitignore` keeps them out of git.

## Third-party sources (you download)

| Source | What we use | Where to get it | Put it at |
|---|---|---|---|
| **Global Preferences Survey** (Falk, Becker, Dohmen, Enke, Huffman & Sunde 2018, *QJE*, [doi:10.1093/qje/qjy013](https://doi.org/10.1093/qje/qjy013)) | Country-level file (the anchor). The individual-level file is used only for robustness checks | briq Institute, [global-preferences](https://www.briq-institute.org/global-preferences/home) (registration form) | `data/GPS/GPS_dataset_country_level/country_gps.dta`; `data/GPS/GPS_dataset_individual_level/` |
| **World Values Survey, Wave 7** (2017–2022) | Respondent file, Stata format: the evaluation items and held-out human comparisons | WVS Association, [Wave 7 download](https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp) | `data/WVS/WVS_wave7.dta` |
| WVS Wave 6 and the WVS/EVS Time Series 1981–2022 | Second-wave and trend checks only | Same site, "Wave 6" and "Timeseries" | `data/WVS/wave6/`, `data/WVS/timeseries/WVS_Time_Series_1981-2022_stata_v5_0.dta` |
| WVS/EVS Joint 2017 and EVS 2017 (GESIS ZA7500) | Validity lane only | WVS site ("WVS/EVS Joint 2017"); [GESIS ZA7500](https://search.gesis.org/research_data/ZA7500) | `data/WVS/joint_evs_wvs/`, `data/EVS/ZA7500_v5-0-0.dta` |
| AmericasBarometer (LAPOP), USA and Mexico 2012–2019 | Out-of-sample checks in the validity lane only | Vanderbilt Center for Global Democracy, [data access](https://www.vanderbilt.edu/cgd/data-access/) | `data/Barometer/USA_Barometer/`, `data/Barometer/MEX_Barometer/` |
| World Development Indicators | GDP per capita (PPP), Gini, agricultural employment: the development controls in `analysis/phase2/10_development_restrictions.py` | World Bank, [WDI](https://databank.worldbank.org/source/world-development-indicators) | `data/phase2/aux/wdi.csv` with columns `iso3,year,gdp_pc_ppp,gini,agri_empl` |

To replicate Paper A's headline (trust adapter–GPS 0.74), you need only the GPS country file. Paper B also needs WVS
Wave 7.

## Derived files you rebuild locally

The following files are computed from respondents, so they are no longer tracked (since 2026-11-03). Rebuild them
after downloading the sources above:

| File | Built by |
|---|---|
| `data/wvs_eval_full/<ISO3>_WVS_wave7.parquet` | `data/wvs_eval_full/_build_wvs_eval_full.py` |
| `data/merged/*.parquet` | `data/merged/_build_merge.py` |
| `analysis/phase2/outputs/wvs_question_metrics_long.parquet`, `readout_option_panel.parquet`, `development_human_by_country.csv` | the `analysis/phase2/` pipeline (see [`analysis/phase2/README.md`](analysis/phase2/README.md)) |
| `data/validity/scores_*.csv`, `gradients_wvs*` | the validity lane |

Paper B reads held-out human data only through `paper_b/heldout/freeze.require_freeze()`. That guard refuses to read
before the preregistered item selection is frozen.

## Our artifacts (Hugging Face)

| Object | Where | Access |
|---|---|---|
| Paper A adapters (16 countries) | [`Bonorinoa/SCA2-phase2-adapters`](https://huggingface.co/Bonorinoa/SCA2-phase2-adapters), commit `03c43dfd27c9535283feb78ffa727da3bfa1b966` | Public behind a gate: log in and accept the conditions. Derived from Llama 3.1, so the Llama 3.1 Community License applies |
| Paper B adapters and run artifacts | `Bonorinoa/SCA2-paper-b-adapters`, `Bonorinoa/SCA2-paper-b-artifacts` | Private until Paper B is released |
| Paper A option probabilities (model outputs only) | [Drive zip](https://drive.google.com/uc?export=download&id=1lIAx0ueSpgaZPmAzNbFSD31ddGQH7Nqo) | Public |
| Base model | [`meta-llama/Llama-3.1-8B-Instruct`](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | Gated by Meta |

The synthetic scenario bank and its sign labels are in this repository
(`synthetic_generation/outputs/gps_sign_relabel_all/`). They contain no respondent data.
