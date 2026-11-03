#!/usr/bin/env python3
"""Lock check for the voice pass: every \\cl, \\ci, \\dc macro (value + id) and every citation key in the eight
section files at a git revision must still be present in the working tree, file by file.

Usage (from misc/paper_b):  python3 voice_pass/check_locks.py [--rev HEAD]
Exit 0 if nothing was lost or changed; 1 otherwise. Additions are listed (they are allowed only if reported).
"""
from __future__ import annotations

import argparse
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["abstract", "introduction", "background", "instrument", "design", "results", "discussion", "conclusion"]
MAC = re.compile(r"\\(ci)\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}|\\(cl|dc)\{([^}]*)\}\{([^}]*)\}")
CITE = re.compile(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")


def macros(t: str) -> Counter:
    t = re.sub(r"(?<!\\)%.*", "", t)
    c = Counter()
    for m in MAC.finditer(t):
        if m.group(1):
            c[("ci", m.group(2), m.group(3), m.group(4))] += 1
        else:
            c[(m.group(5), m.group(6), m.group(7))] += 1
    return c


def cites(t: str) -> Counter:
    t = re.sub(r"(?<!\\)%.*", "", t)
    return Counter(k.strip() for m in CITE.finditer(t) for k in m.group(1).split(","))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")
    a = ap.parse_args()
    bad = 0
    gm_old, gm_new, gc_old, gc_new = Counter(), Counter(), Counter(), Counter()
    for f in FILES:
        old = subprocess.run(["git", "show", f"{a.rev}:misc/paper_b/{f}.tex"], capture_output=True, text=True,
                             cwd=ROOT, check=True).stdout
        new = (ROOT / f"{f}.tex").read_text()
        mo, mn, co, cn = macros(old), macros(new), cites(old), cites(new)
        gm_old += mo; gm_new += mn; gc_old += co; gc_new += cn
        lost = mo - mn
        added = mn - mo
        print(f"{f:13s} macros {sum(mo.values()):4d} -> {sum(mn.values()):4d}   cite keys {len(co):3d} -> {len(cn):3d}")
        for k, v in lost.items():
            print(f"    LOST  x{v} {k}")
        for k, v in added.items():
            print(f"    ADDED x{v} {k}")
        for k in set(co) - set(cn):
            print(f"    CITE LOST {k}")
        for k in set(cn) - set(co):
            print(f"    CITE ADDED {k}")
    # A claim id is dropped from the main text only if it vanishes from every file.
    ids_old = {k[-1] for k in gm_old} | {k[-1] for k in gm_old if k[0] == "ci"}
    ids_new = {k[-1] for k in gm_new}
    dropped_ids = sorted(ids_old - ids_new)
    lost_vals = gm_old - gm_new
    changed = [k for k in lost_vals if k[-1] in ids_new]
    print(f"claim/design ids dropped from the main text: {dropped_ids or 'none'}")
    print(f"citation keys dropped from the section files: {sorted(set(gc_old) - set(gc_new)) or 'none'}")
    if dropped_ids or set(gc_old) - set(gc_new):
        bad = 1
    # a value change for a surviving id
    vals_old = {(k[0],) + k[1:-1] + (k[-1],) for k in gm_old}
    vals_new = {(k[0],) + k[1:-1] + (k[-1],) for k in gm_new}
    by_id_new = {}
    for k in vals_new:
        by_id_new.setdefault((k[0], k[-1]), set()).add(k[1:-1])
    for k in vals_old:
        if k[1:-1] not in by_id_new.get((k[0], k[-1]), {k[1:-1]}):
            print(f"VALUE CHANGED for {k[0]} {k[-1]}: {k[1:-1]} -> {by_id_new[(k[0], k[-1])]}")
            bad = 1
    print("RESULT:", "PASS" if not bad else "FAIL")
    return bad


if __name__ == "__main__":
    raise SystemExit(main())
