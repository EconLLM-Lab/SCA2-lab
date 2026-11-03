#!/usr/bin/env python3
"""Read-only verifier probe for Paper B voice pass c6c16e7."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

BASELINE = "3613d82"
REVIEWED = "c6c16e7"
HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
PAPER = REPO / "misc/paper_b"
TABLE = REPO / "planning/sprint_2026-10-11/paper-b-tier1/NUMBERS_TABLE.csv"
SECTIONS = [
    "abstract.tex", "introduction.tex", "background.tex", "instrument.tex",
    "design.tex", "results.tex", "discussion.tex", "conclusion.tex",
]
EXPECTED_SHA = "71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4"

CL_RE = re.compile(r"\\clh?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*)\}")
CI_RE = re.compile(r"\\ci\{([^{}]*)\}\{([^{}]*)\}\{([^{}]*)\}")
DC_RE = re.compile(r"\\dc\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*)\}")
FIELDS = {"v", "lo", "hi", "n", "pct", "abs"}


def git_show(rev: str, rel: str) -> str:
    p = subprocess.run(
        ["git", "show", f"{rev}:{rel}"], cwd=REPO, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if p.returncode:
        raise RuntimeError(f"git show failed ({p.returncode}): {rev}:{rel}: {p.stderr}")
    return p.stdout


def clean_printed(s: str) -> str:
    return (s.replace("$", "").replace("{,}", ",").replace("\\,", "")
             .replace("~", "").replace("−", "-").replace("--", "-").strip())


def split_ref(ref: str, table: dict[str, dict[str, str]]) -> tuple[str, str]:
    if ref in table:
        return ref, "v"
    cid, sep, field = ref.rpartition(":")
    if sep and field in FIELDS:
        return cid, field
    return ref, "v"


def macro_counter(tex: str) -> Counter:
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    found: list[tuple[str, ...]] = []
    for lo, hi, ref in CI_RE.findall(tex):
        found.append(("ci", clean_printed(lo), clean_printed(hi), ref))
    tex_no_ci = CI_RE.sub(" ", tex)
    for shown, ref in CL_RE.findall(tex_no_ci):
        found.append(("cl", clean_printed(shown), ref))
    for shown, key in DC_RE.findall(tex_no_ci):
        found.append(("dc", clean_printed(shown), key))
    return Counter(found)


def check_stat(shown: str, ref: str, table: dict[str, dict[str, str]]) -> str | None:
    cid, field = split_ref(ref, table)
    row = table.get(cid)
    if row is None:
        return f"missing claim id {cid}"
    source = {"v": "value", "lo": "ci_low", "hi": "ci_high", "n": "n",
              "pct": "value", "abs": "value"}[field]
    raw = row.get(source, "")
    if raw == "":
        return f"empty {source} for {cid}"
    try:
        value = Decimal(raw)
    except InvalidOperation:
        prefix = shown.rstrip(".").replace("\\ldots", "").replace("…", "")
        if len(prefix) < 8 or not raw.startswith(prefix):
            return f"string mismatch {shown} vs {raw} for {cid}"
        return None
    if field == "pct":
        value *= 100
    elif field == "abs":
        value = abs(value)
    if shown.startswith("<"):
        if not value < Decimal(shown[1:].replace(",", "")):
            return f"bound mismatch {shown} vs {raw} for {cid}"
        return None
    try:
        observed = Decimal(shown.replace(",", ""))
    except InvalidOperation:
        return f"unparseable {shown} for {cid}"
    places = len(shown.split(".", 1)[1]) if "." in shown else 0
    expected = value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    if observed != expected:
        return f"rounding mismatch {shown} vs {raw}->{expected} for {cid}:{field}"
    return None


def raw_prose_numerals(tex: str) -> Counter:
    """Count numeral tokens after removing statistic/design macros and TeX metadata."""
    text = re.sub(r"(?<!\\)%.*", "", tex)
    text = CI_RE.sub(" ", CL_RE.sub(" ", DC_RE.sub(" ", text)))
    text = re.sub(r"\\begin\{(?:equation|align|tikzpicture)[^}]*\}.*?\\end\{[^}]+\}", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\(?:cite[tp]?|citet|citep|ref|label|input|includegraphics)\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", text)
    # These are identifiers rather than quantitative prose.
    text = re.sub(r"\bQ\d+\b|\bWVS-?~?\d+\b|\bWave~?\d+\b|\bS[12]\b|\bV5\b|\bjev-\d+(?:\.\d+)+\b|Llama~?\d+(?:\.\d+)?\s*\d+B", " ", text)
    return Counter(m.group(0) for m in re.finditer(r"(?<![A-Za-z_\\])\d+(?:[.,]\d+)*", text))


def main() -> int:
    table_rows = list(csv.DictReader(TABLE.open(newline="")))
    table = {r["claim_id"]: r for r in table_rows}
    table_sha = hashlib.sha256(TABLE.read_bytes()).hexdigest()

    old_all = Counter()
    new_all = Counter()
    old_raw_numerals = Counter()
    new_raw_numerals = Counter()
    stat_errors: list[str] = []
    for name in SECTIONS:
        rel = f"misc/paper_b/{name}"
        old = git_show(BASELINE, rel)
        new = (PAPER / name).read_text()
        old_all.update(macro_counter(old))
        new_all.update(macro_counter(new))
        old_raw_numerals.update(raw_prose_numerals(old))
        new_raw_numerals.update(raw_prose_numerals(new))
        current = macro_counter(new)
        for macro, *parts in current:
            if macro == "cl":
                err = check_stat(parts[0], parts[1], table)
                if err:
                    stat_errors.append(f"{name}: {err}")
            elif macro == "ci":
                lo, hi, ref = parts
                for shown, suffix in ((lo, "lo"), (hi, "hi")):
                    cid, field = split_ref(ref, table)
                    target_ref = ref if field in {"lo", "hi"} else f"{cid}:{suffix}"
                    err = check_stat(shown, target_ref, table)
                    if err:
                        stat_errors.append(f"{name}: {err}")

    bib = (PAPER / "references.bib").read_text()
    sections_text = "\n".join((PAPER / f).read_text() for f in SECTIONS)
    supplement = (PAPER / "supplement.tex").read_text()
    main_tex = (PAPER / "main.tex").read_text()
    main_review = (PAPER / "main_review.tex").read_text()

    bib_checks = {
        "kirman1992": all(x in bib for x in (
            "@article{kirman1992", "Journal of Economic Perspectives", "volume  = {6}",
            "number  = {2}", "pages   = {117--136}", "doi     = {10.1257/jep.6.2.117}",
        )),
        "robinson1950": all(x in bib for x in (
            "@article{robinson1950", "American Sociological Review", "volume  = {15}",
            "number  = {3}", "pages   = {351--357}", "doi     = {10.2307/2087176}",
        )),
        "zhao2023gpo": all(x in bib for x in (
            "@misc{zhao2023gpo", "Zhao, Siyan and Dang, John and Grover, Aditya",
            "eprint        = {2310.11523}",
        )),
    }
    preprint_hits = re.findall(r"gonzalezbonorino2026|arXiv|2610\.06562|earlier study", sections_text, re.I)
    review_gate = (
        "\\ifdefined\\showauthors" in main_tex
        and "\\else\n\\author{}\n\\fi" in main_tex
        and main_review.strip().endswith("\\input{main}")
        and "\\def\\showauthors{1}" in main_review
    )
    supplement_carry = {
        "C7_by_dimension_TVD": "\\label{tab:s-tvd-dim}" in supplement,
        "C9_recovery_definitions": all(x in supplement for x in (
            "Recovery (adapter margin above base margin)",
            "Accuracy (adapter prefers its own chosen completion)",
            "Base accuracy", "Mean margin shift (nats)",
        )),
    }

    report = {
        "reviewed_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "table_sha256": table_sha,
        "table_rows": len(table_rows),
        "macro_occurrences_baseline": sum(old_all.values()),
        "macro_occurrences_reviewed": sum(new_all.values()),
        "macro_multiset_added": list((new_all - old_all).elements()),
        "macro_multiset_removed": list((old_all - new_all).elements()),
        "stat_errors": stat_errors,
        "added_raw_prose_numerals": list((new_raw_numerals - old_raw_numerals).elements()),
        "bib_checks": bib_checks,
        "section_preprint_hits": preprint_hits,
        "main_review_showauthors_gate": review_gate,
        "supplement_carry": supplement_carry,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    ok = (
        report["reviewed_head"].startswith(REVIEWED)
        and table_sha == EXPECTED_SHA
        and len(table_rows) == 562
        and not (new_all - old_all) and not (old_all - new_all)
        and not stat_errors and not report["added_raw_prose_numerals"]
        and all(bib_checks.values()) and not preprint_hits and review_gate
        and all(supplement_carry.values())
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
