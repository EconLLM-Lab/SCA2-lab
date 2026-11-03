#!/usr/bin/env python3
"""Reproducible main-text word count for Paper B.

Counts the section files input by main.tex between \\doublespacing and \\input{backmatter}
(introduction ... conclusion), including table cells, table and figure captions and
footnotes; excludes the abstract, backmatter, bibliography and supplement.
Statistic macros print their number once: \\cl{v}{id} -> v, \\ci{a}{b}{id} -> "a b",
\\dc{v}{id} -> v. Display equations count as one token each, inline math as one token.

Usage (from misc/paper_b):  python tools/count_words.py [--per-file]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["introduction", "background", "instrument", "design", "results", "discussion", "conclusion"]


def inline_tables(text: str) -> str:
    return re.sub(r"\\input\{tables/([^}]+)\}", lambda m: (ROOT / "tables" / (m.group(1) + ".tex")).read_text(), text)


def detex(t: str) -> str:
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\begin\{(equation|align)\*?\}.*?\\end\{\1\*?\}", " EQN ", t, flags=re.S)
    t = re.sub(r"\\cl\{([^}]*)\}\{[^}]*\}", r"\1", t)
    t = re.sub(r"\\ci\{([^}]*)\}\{([^}]*)\}\{[^}]*\}", r"\1 \2", t)
    t = re.sub(r"\\dc\{([^}]*)\}\{[^}]*\}", r"\1", t)
    t = re.sub(r"\\(cite[a-z]*|citet|citep|ref|label|includegraphics|input|renewcommand|setlength)\*?(\[[^\]]*\])*\{[^}]*\}(\{[^}]*\})?", lambda m: " CITE " if m.group(1).startswith("cite") or m.group(1) == "ref" else " ", t)
    t = re.sub(r"\\begin\{tabularx\}\{[^}]*\}\{.*", " ", t)
    t = re.sub(r"\\begin\{[^}]*\}(\[[^\]]*\])?|\\end\{[^}]*\}", " ", t)
    t = re.sub(r"\$[^$]*\$", " MATH ", t)
    t = re.sub(r"\\(toprule|midrule|bottomrule|centering|small|footnotesize|clearpage|newpage|noindent)", " ", t)
    t = t.replace("&", " ").replace("\\\\", " ")
    t = re.sub(r"\\(section|subsection|subsubsection|paragraph|caption|footnote|emph|textbf|textit|textsc|operatorname|mathrm|citet|citep)\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}~]", " ", t)
    return t


def main() -> int:
    per_file = {}
    for name in FILES:
        text = inline_tables((ROOT / f"{name}.tex").read_text())
        words = [w for w in re.findall(r"[A-Za-z0-9$%.,;:'\-\u2013\u2014\u00c0-\u024f]+", detex(text)) if re.search(r"[A-Za-z0-9]", w)]
        per_file[name] = len(words)
    if "--per-file" in sys.argv:
        for k, v in per_file.items():
            print(f"{k:14s}{v:7,d}")
    print(f"total {sum(per_file.values()):,d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
