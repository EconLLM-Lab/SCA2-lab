#!/usr/bin/env python3
"""Voice measurements for the Paper B voice pass (writer, 2026-11-03).

For each section file, detex the prose (floats, captions and display equations removed; statistic macros
rendered as printed; citations dropped; \\citet rendered as "Author"), then report:
  - the calibrate.py feature set (we_per_1k, connect_per_1k, mean/p90 sentence words),
  - connectors4_per_1k: the brief's four connectors ("That is," "In other words," "Therefore," "Notably,"),
  - sentences with more than two prose commas. Commas inside a rendered [lo, hi] interval and digit-group
    commas (2,000) are not prose commas; they are counted separately so macro/interval lists are visible.

Usage (from misc/paper_b):
  python3 voice_pass/measure.py [--rev HEAD] [--list] [files...]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAL = Path.home() / ".hermes/profiles/writer/skills/research/augusto-academic-voice/scripts/calibrate.py"
spec = importlib.util.spec_from_file_location("calibrate", CAL)
assert spec is not None and spec.loader is not None
cal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cal)

FILES = ["abstract", "introduction", "background", "instrument", "design", "results", "discussion", "conclusion"]
CONN4 = re.compile(r"\b(That is|In other words|Therefore|Notably),", re.I)


def detex(t: str) -> str:
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\begin\{(figure|table)\}.*?\\end\{\1\}", " ", t, flags=re.S)
    t = re.sub(r"\\input\{tables/[^}]*\}", " ", t)
    t = re.sub(r"\\begin\{(equation|align)\*?\}.*?\\end\{\1\*?\}", " EQN ", t, flags=re.S)
    t = t.replace("{,}", "")
    t = re.sub(r"\\footnote\{((?:[^{}]|\{[^{}]*\})*)\}", r" \1 ", t)
    t = re.sub(r"\\ci\{([^}]*)\}\{([^}]*)\}\{[^}]*\}", r"[\1 ; \2]", t)  # interval: marked, not a prose comma
    t = re.sub(r"\\cl\{([^}]*)\}\{[^}]*\}", r"\1", t)
    t = re.sub(r"\\dc\{([^}]*)\}\{[^}]*\}", r"\1", t)
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)  # digit groups
    t = re.sub(r"\\citet\{[^}]*\}", "Author", t)
    t = re.sub(r"\s*\\citep(\[[^\]]*\])*\{[^}]*\}", "", t)
    t = re.sub(r"\\(ref|label)\{[^}]*\}", "1", t)
    t = re.sub(r"\\(section|subsection|paragraph)\*?\{([^}]*)\}", r"\n\n\2.\n\n", t)
    t = re.sub(r"\\item", "\n", t)
    t = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", " ", t)
    t = re.sub(r"\$[^$]*\$", " X ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}~]", " ", t)
    t = t.replace("``", '"').replace("''", '"').replace("--", "-")
    return t


def read(name: str, rev: str | None) -> str:
    if rev:
        return subprocess.run(["git", "show", f"{rev}:misc/paper_b/{name}.tex"], capture_output=True, text=True,
                              cwd=ROOT, check=True).stdout
    return (ROOT / f"{name}.tex").read_text()


def comma_sentences(prose: str):
    out = []
    for s in cal.split_sentences(prose):
        n = s.count(",")
        if n > 2:
            out.append((n, s.count(";") if "[" in s else 0, s))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    files = a.files or FILES
    print(f"{'file':13s} {'words':>6s} {'sents':>5s} {'we/1k':>6s} {'conn/1k':>7s} {'conn4/1k':>8s} "
          f"{'mean':>5s} {'p90':>4s} {'>2c':>4s}")
    tot_s = tot_c = 0
    for f in files:
        prose = detex(read(f, a.rev))
        feat = cal.features(prose)
        c4 = round(1000 * len(CONN4.findall(prose)) / feat["n_words"], 2)
        cs = comma_sentences(prose)
        tot_s += feat["n_sentences"]
        tot_c += len(cs)
        print(f"{f:13s} {feat['n_words']:6d} {feat['n_sentences']:5d} {feat['we_per_1k']:6.1f} "
              f"{feat['connect_per_1k']:7.1f} {c4:8.1f} {feat['mean_sent_words']:5.1f} {feat['p90_sent_words']:4d} "
              f"{len(cs):4d}")
        if a.list:
            for n, _, s in cs:
                print(f"    [{n} commas] {s[:220]}")
    print(f"sentences with >2 prose commas: {tot_c} of {tot_s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
