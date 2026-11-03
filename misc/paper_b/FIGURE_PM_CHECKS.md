# PM checks during the reader-pass seat pause

This is an incremental check, not manuscript or online-build acceptance.

## Scientific-code baseline

Main code checkout: `/Users/bonorinoa/Desktop/Github_Repositories/SCA2_PofW`.

Command: `HF_TOKEN= env -u PYTHONPATH .venv/bin/python -m pytest paper_b -q`.

Result: exit 0; **613 passed in 182.68s**. The first foreground attempt timed out at 180 seconds; the completed background run is authoritative. Output: `/Users/bonorinoa/.hermes/cache/scratch/paper-b-reader-pass/pm_baseline_pytest.log`.

## Independent aggregate-to-plot check

Input: unchanged `NUMBERS_TABLE.csv`, sha256 `71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4`.

The PM independently read the manifest and checked all **285 data/label records** against their exact CSV cell, rounded labels using Decimal half-up, and checked horizontal positions against each panel's declared affine map. Result: **zero mismatches**, exit 0. No raw human data were opened. Generator `--verify` also returned `verify: ok`, exit 0.

This does not substitute for checking that the plotted statistical targets are correctly described, nor for a final visual read.

## Parent-owned adversarial tests and an actual defect

New file: `tools/test_build_figures.py`.

Checks cover frozen table hash/count, deterministic source/manifest regeneration, exact data and coordinates, full surface/cohort coverage, differing bootstrap units, direct paired screen contrasts, undefined constant-base ranking, and deliberate corruption of a plotted point, interval endpoint, printed label, and manifest value.

The first run returned **1 failed, 12 passed**. It caught a genuine semantic metadata error: the screen's quantity was described as agreement with GPS. The retrospective screen compares assigned item directions with **WVS-7 human country differences**. A one-string correction was made in `tools/build_figures.py`; it changes no plotted value, interval, estimator or decision rule.

After that correction:

```
HF_TOKEN= PYTHONDONTWRITEBYTECODE=1 \
TMPDIR=/Users/bonorinoa/.hermes/cache/scratch/paper-b-reader-pass \
env -u PYTHONPATH /Users/bonorinoa/Desktop/Github_Repositories/SCA2_PofW/.venv/bin/python \
-m pytest misc/paper_b/tools/test_build_figures.py \
          misc/paper_b/tools/test_audit_numbers.py \
          misc/paper_b/tools/test_render_supplement.py \
          misc/paper_b/tools/test_anonymize_prereg.py -q
```

Result: exit 0; **36 passed in 0.40s** at that stage.

Two further RED→GREEN mutation tests exposed verification gaps: reversing the generated TeX coordinate transform could still pass the cell audit, and dropping a whole figure from the manifest could pass because the verifier only iterated surviving entries. The verifier now also compares the saved TeX and complete manifest with fresh generator output. Both deliberate corruptions first failed their rejection tests, then passed after the minimal regeneration-comparison guards were added. This strengthens the gate; it does not change the rendered data or any scientific statistic.

Final rerun of the combined figure/audit/render/anonymization tool suite: exit 0; **38 passed in 0.35s**. Final generator `--verify`: `verify: ok`, exit 0.

`python3 misc/paper_b/tools/build_figures.py --no-compile` regenerated four sources and the manifest after the metadata correction. The correction and verification guards do not change the generated visual content. Visual corrections requested in figure card comment 184 are still outstanding, so regenerated previews and a new final read remain required.

## Attribution and independent review

The core figure generator is Claude-produced. This test module, the semantic metadata correction, and the small source/manifest regeneration guards are PM-authored. The Codex verifier was told to record the narrow same-family limit for those PM contributions and to inspect the generator/table linkage independently; the later Claude PM acceptance was told to inspect those contributions too. Do not describe all bytes as independently Claude-produced or accept the tests alone as an independent scientific verdict.

## Remaining gates

Figure visual polish and final build report → writer revision → independent manuscript/figure gate → standalone archive closure → exact canonical Overleaf upload and fresh main/supplement builds. The online project has not been replaced with this candidate. No git commit or push was made.
