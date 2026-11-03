#!/usr/bin/env python3
"""Build the Paper B empirical figures from the frozen NUMBERS_TABLE.csv.

Standard library only. Every plotted point and interval end is read from the table as the exact CSV
string and handed to TeX unchanged; TeX (pdflatex + TikZ) maps it to a position. No other input is read:
no human rows, no data/ directory, no network.

    python3 misc/paper_b/tools/build_figures.py            # TeX + manifest + PDFs + PNG previews
    python3 misc/paper_b/tools/build_figures.py --no-compile
    python3 misc/paper_b/tools/build_figures.py --verify   # re-check figures/ against the table

Outputs, all in misc/paper_b/figures/: fig_*.tex, fig_*.pdf, fig_*.png, PLOT_MANIFEST.json.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parent.parent
TABLE = REPO / "planning/sprint_2026-10-11/paper-b-tier1/NUMBERS_TABLE.csv"
FIGDIR = PAPER / "figures"
TABLE_SHA = "71ee7c8c68eb856bf7215165dd836aef7cc3f67993a6523790cee4b22ce186a4"  # claim lock C9.1
TABLE_ROWS = 562
MINUS = "$-$"

# ----------------------------------------------------------------------------- table access


def load_table(path=TABLE, pinned=True):
    raw = Path(path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if pinned and sha != TABLE_SHA:
        raise SystemExit(f"NUMBERS_TABLE.csv sha256 {sha} is not the pinned {TABLE_SHA}")
    with open(path, newline="", encoding="utf-8") as fh:
        rows = {r["claim_id"]: r for r in csv.DictReader(fh)}
    if pinned and len(rows) != TABLE_ROWS:
        raise SystemExit(f"expected {TABLE_ROWS} rows, found {len(rows)}")
    return rows, sha


FIELD = {"value": "value", "lo": "ci_low", "hi": "ci_high", "n": "n"}


def cell(rows, claim, field):
    s = rows[claim][FIELD[field]]
    if s == "":
        raise SystemExit(f"{claim}.{field} is empty in the table; nothing to plot")
    return s


def fmt(s, dp):
    """Exact decimal string -> printed string, half-up, TeX minus sign."""
    q = Decimal(s).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)
    t = f"{q:.{dp}f}"
    if t.startswith("-"):
        t = MINUS + t[1:]
    return t


def fmt_plain(s, dp):
    return fmt(s, dp).replace(MINUS, "-")


# ----------------------------------------------------------------------------- figure scaffolding

PREAMBLE = r"""\documentclass[border=3pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,xcolor}
\usepackage{tikz}
\pdftrailerid{}
\definecolor{cA}{HTML}{0072B2}% blue
\definecolor{cB}{HTML}{D55E00}% vermillion
\definecolor{cC}{HTML}{009E73}% green
\definecolor{cD}{HTML}{CC79A7}% purple
\definecolor{cG}{HTML}{6B6B6B}% grey
\definecolor{cS}{HTML}{3A3A3A}
\definecolor{zebra}{HTML}{F1F1F1}
\definecolor{gridc}{HTML}{C8C8C8}
\newcommand{\Px}{0}\newcommand{\Pmin}{0}\newcommand{\Psc}{1}
% \setpanel{x0 cm}{data value at x0}{cm per data unit}: every data x below is x0 + (v - vmin) * scale.
\newcommand{\setpanel}[3]{\renewcommand{\Px}{#1}\renewcommand{\Pmin}{#2}\renewcommand{\Psc}{#3}}
\newcommand{\XX}[1]{\fpeval{\Px+((#1)-(\Pmin))*\Psc}}
% markers: o filled circle, s filled square, d hollow diamond, t filled triangle, h hollow circle, q hollow square
\newcommand{\mk}[4]{% style colour x y
  \ifx#1o\fill[#2] (#3,#4) circle (0.095);\fi
  \ifx#1h\draw[#2,fill=white,line width=0.7pt] (#3,#4) circle (0.095);\fi
  \ifx#1s\fill[#2] (#3-0.088,#4-0.088) rectangle (#3+0.088,#4+0.088);\fi
  \ifx#1q\draw[#2,fill=white,line width=0.7pt] (#3-0.085,#4-0.085) rectangle (#3+0.085,#4+0.085);\fi
  \ifx#1d\draw[#2,fill=white,line width=0.7pt] (#3,#4+0.125)--(#3+0.125,#4)--(#3,#4-0.125)--(#3-0.125,#4)--cycle;\fi
  \ifx#1t\fill[#2] (#3,#4+0.115)--(#3+0.105,#4-0.085)--(#3-0.105,#4-0.085)--cycle;\fi}
% interval with point: claim, lo, value, hi, y, style, colour, dash(solid|dashed)
\newcommand{\ival}[8]{%
  \edef\xl{\XX{#2}}\edef\xv{\XX{#3}}\edef\xh{\XX{#4}}%
  \draw[#7,line width=0.8pt,#8] (\xl,#5)--(\xh,#5);
  \draw[#7,line width=0.8pt] (\xl,#5-0.055)--(\xl,#5+0.055);
  \draw[#7,line width=0.8pt] (\xh,#5-0.055)--(\xh,#5+0.055);
  \mk{#6}{#7}{\xv}{#5}}
% point only
\newcommand{\pval}[5]{\edef\xv{\XX{#2}}\mk{#4}{#5}{\xv}{#3}}
% stem from the panel zero to the value, with marker: claim, value, y, style, colour
\newcommand{\lval}[5]{\edef\xv{\XX{#2}}\edef\xz{\XX{0}}%
  \draw[#5,line width=0.8pt] (\xz,#3)--(\xv,#3);\mk{#4}{#5}{\xv}{#3}}
% vertical reference line at a data value: claim, value, y0, y1, colour
\newcommand{\vref}[5]{\edef\xv{\XX{#2}}\draw[#5,dashed,line width=0.8pt] (\xv,#3)--(\xv,#4);}
% a printed number tied to a table cell: claim, field, printed, prefix, suffix, x, y, anchor, background fill
\newcommand{\lbl}[9]{\node[anchor=#8,fill=#9,inner sep=1pt,font=\footnotesize] at (#6,#7) {#4#3#5};}
% a printed value with its interval: claim, printed value, printed lo, printed hi, x, y, anchor
\newcommand{\lblci}[7]{\node[anchor=#7,inner sep=0pt,font=\footnotesize] at (#5,#6) {#2\,[#3, #4]};}
% free text (no data)
\newcommand{\txt}[4]{\node[anchor=#3,inner sep=0pt,font=#4] at (#1) {#2};}
\begin{document}
\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={text=black}]
"""
POSTAMBLE = "\\end{tikzpicture}\n\\end{document}\n"

PANEL_COUNTER = [0]


class Panel:
    def __init__(self, fig, pid, x0, xmin, xmax, width, quantity, interval_unit):
        self.fig, self.id = fig, pid
        self.x0, self.xmin, self.xmax, self.width = Decimal(x0), Decimal(xmin), Decimal(xmax), Decimal(width)
        self.scale = (self.width / (self.xmax - self.xmin)).quantize(Decimal("0.000001"))
        self.meta = {"id": pid, "x0_cm": str(self.x0), "data_min": str(self.xmin), "data_max": str(self.xmax),
                     "cm_per_unit": str(self.scale), "quantity": quantity, "interval": interval_unit}
        fig.panels.append(self.meta)

    def x(self, v):  # python-side mapping, used for ticks, labels and the manifest
        return float(self.x0 + (Decimal(v) - self.xmin) * self.scale)

    def select(self):
        self.fig.tex(f"\\setpanel{{{self.x0}}}{{{self.xmin}}}{{{self.scale}}}")

    def record(self, claim, field, value, role, extra=None):
        d = {"figure": self.fig.name, "panel": self.id, "claim_id": claim, "field": FIELD[field],
             "value": value, "role": role, "x_cm": round(self.x(value), 4)}
        if extra:
            d.update(extra)
        self.fig.data.append(d)


class Fig:
    def __init__(self, name, rows, title):
        self.name, self.rows, self.title = name, rows, title
        self.lines, self.data, self.panels = [], [], []

    def tex(self, s):
        self.lines.append(s)

    # ---- data-bearing primitives (these are the only ways a number reaches the picture)
    def ival(self, p, claim, y, style, colour, dash="solid"):
        lo, v, hi = (cell(self.rows, claim, f) for f in ("lo", "value", "hi"))
        p.select()
        self.tex(f"\\ival{{{claim}}}{{{lo}}}{{{v}}}{{{hi}}}{{{y:.3f}}}{{{style}}}{{{colour}}}{{{dash}}}")
        for f, s, r in (("lo", lo, "interval_low"), ("value", v, "point"), ("hi", hi, "interval_high")):
            p.record(claim, f, s, r, {"y_cm": round(y, 3)})

    def pval(self, p, claim, y, style, colour):
        v = cell(self.rows, claim, "value")
        p.select()
        self.tex(f"\\pval{{{claim}}}{{{v}}}{{{y:.3f}}}{{{style}}}{{{colour}}}")
        p.record(claim, "value", v, "point", {"y_cm": round(y, 3)})

    def lval(self, p, claim, y, style, colour):
        v = cell(self.rows, claim, "value")
        p.select()
        self.tex(f"\\lval{{{claim}}}{{{v}}}{{{y:.3f}}}{{{style}}}{{{colour}}}")
        p.record(claim, "value", v, "point", {"y_cm": round(y, 3)})

    def vref(self, p, claim, y0, y1, colour):
        v = cell(self.rows, claim, "value")
        p.select()
        self.tex(f"\\vref{{{claim}}}{{{v}}}{{{y0:.3f}}}{{{y1:.3f}}}{{{colour}}}")
        p.record(claim, "value", v, "reference_line", {"y_cm": [round(y0, 3), round(y1, 3)]})

    def lbl(self, claim, field, dp, x, y, anchor="west", prefix="", suffix="", fill="none"):
        s = cell(self.rows, claim, field)
        printed = fmt(s, dp) if field != "n" else str(int(s))
        self.tex(f"\\lbl{{{claim}}}{{{field}}}{{{printed}}}{{{prefix}}}{{{suffix}}}{{{x:.3f}}}{{{y:.3f}}}{{{anchor}}}{{{fill}}}")
        self.data.append({"figure": self.fig_name(), "panel": "label", "claim_id": claim, "field": FIELD[field],
                          "value": s, "role": "printed_label", "printed": printed})

    def fig_name(self):
        return self.name

    def lblci(self, claim, dp, x, y, anchor="west"):
        v, lo, hi = (cell(self.rows, claim, f) for f in ("value", "lo", "hi"))
        self.tex(f"\\lblci{{{claim}}}{{{fmt(v, dp)}}}{{{fmt(lo, dp)}}}{{{fmt(hi, dp)}}}{{{x:.3f}}}{{{y:.3f}}}{{{anchor}}}")
        for f, s in (("value", v), ("lo", lo), ("hi", hi)):
            self.data.append({"figure": self.name, "panel": "label", "claim_id": claim, "field": FIELD[f],
                              "value": s, "role": "printed_label", "printed": fmt(s, dp)})

    def text(self, x, y, s, anchor="west", font="\\footnotesize"):
        self.tex(f"\\txt{{{x:.3f},{y:.3f}}}{{{s}}}{{{anchor}}}{{{font}}}")

    def notes(self, y, texts, width=84, step=0.4):
        """Italic footnote lines wrapped to the figure width; returns the y below the last line."""
        import textwrap
        for t in texts:
            for line in textwrap.wrap(t, width):
                self.text(0.0, y, line, "west", "\\footnotesize\\itshape")
                y -= step
        return y

    # ---- decoration (not data)
    def axis(self, p, ytop, ybot, ticks, dp=1, zero=True, title=None, sub=None, grid=True, tdy=0.50):
        p.select()
        for t in ticks:
            x = p.x(t)
            if grid:
                self.tex(f"\\draw[gridc,line width=0.4pt,dotted] ({x:.3f},{ytop:.3f})--({x:.3f},{ybot:.3f});")
            self.tex(f"\\draw[black,line width=0.5pt] ({x:.3f},{ybot:.3f})--({x:.3f},{ybot - 0.07:.3f});")
            self.tex(f"\\node[anchor=north,inner sep=1pt,font=\\footnotesize] at ({x:.3f},{ybot - 0.07:.3f}) {{{fmt(t, dp)}}};")
        x0, x1 = p.x(p.xmin), p.x(p.xmax)
        self.tex(f"\\draw[black,line width=0.5pt] ({x0:.3f},{ybot:.3f})--({x1:.3f},{ybot:.3f});")
        if zero and p.xmin < 0 < p.xmax:
            xz = p.x(0)
            self.tex(f"\\draw[black,line width=0.9pt] ({xz:.3f},{ytop:.3f})--({xz:.3f},{ybot:.3f});")
        if title:
            xm = (x0 + x1) / 2
            self.tex(f"\\node[anchor=south,inner sep=0pt,font=\\small\\bfseries,align=center] at ({xm:.3f},{ytop + tdy:.3f}) {{{title}}};")
        if sub:
            xm = (x0 + x1) / 2
            self.tex(f"\\node[anchor=south,inner sep=0pt,font=\\footnotesize,text=cS,align=center] at ({xm:.3f},{ytop + 0.05:.3f}) {{{sub}}};")

    def zebra(self, p, ys, dy):
        x0, x1 = p.x(p.xmin), p.x(p.xmax)
        for i, y in enumerate(ys):
            if i % 2 == 0:
                self.tex(f"\\fill[zebra] ({x0:.3f},{y - dy / 2:.3f}) rectangle ({x1:.3f},{y + dy / 2:.3f});")

    def render(self):
        head = f"% Generated by misc/paper_b/tools/build_figures.py from NUMBERS_TABLE.csv. Do not edit.\n% {self.title}\n"
        return head + PREAMBLE + "\n".join(self.lines) + "\n" + POSTAMBLE


# ----------------------------------------------------------------------------- Figure 1: three links

SURF = [("trust", "Trust"), ("risktaking", "Risk taking"), ("posrecip", "Positive reciprocity"),
        ("altruism", "Altruism"), ("negrecip", "Negative reciprocity"), ("patience_q43", "Patience (Q43)"),
        ("patience_q50", "Patience (Q50)")]


def fig1(rows):
    f = Fig("fig_three_links", rows, "Three-link validity forest (surface D; descriptive, not preregistered)")
    dy, top = 0.98, 0.0
    ys = [top - 0.55 - i * dy for i in range(7)]
    ybot = ys[-1] - 0.55
    specs = [("adapter_gps", "Adapter--GPS", "profile-block bootstrap\\\\(26 blocks)", "cA", "o", "d"),
             ("adapter_human", "Adapter--human", "profile-block bootstrap\\\\(26 blocks)", "cB", "o", "d"),
             ("human_gps", "Human--GPS", "country bootstrap\\\\(42 countries)", "cC", "s", None)]
    ticks = ["-0.5", "0", "0.5", "1"]
    panels = []
    for k, (key, title, unit, col, m1, m2) in enumerate(specs):
        x0 = 3.05 + k * 4.0
        p = Panel(f, f"p{k + 1}", x0, "-0.8", "1", 3.7, "Spearman correlation across countries", unit)
        panels.append(p)
        f.zebra(p, ys, dy)
        f.axis(p, top, ybot, ticks, dp=1, title=title, sub=unit, tdy=0.80)
        p.select()
        for (s, lab), y in zip(SURF, ys):
            if key == "human_gps":
                f.ival(p, f"C9_a_{key}_{s}_spearman_rho", y, m1, col)
            else:
                f.ival(p, f"C9_a_{key}_{s}_spearman_rho", y + 0.17, m1, col)
                f.ival(p, f"C9_b_{key}_{s}_spearman_rho", y - 0.17, m2, col, "dashed")
        xm = (p.x(p.xmin) + p.x(p.xmax)) / 2
        f.text(xm, ybot - 0.72, "Spearman correlation $\\rho$", "north", "\\footnotesize")
    for (s, lab), y in zip(SURF, ys):
        f.text(2.9, y, lab, "east")
    # legend (neutral grey: the shapes name the cohort, the panel colours name the link)
    ly = ybot - 1.55
    lx = 0.0
    f.tex(f"\\mk{{o}}{{cG}}{{{lx + 0.15}}}{{{ly}}}")
    f.text(lx + 0.35, ly, "first cohort (primary, solid)", "west")
    f.tex(f"\\draw[cG,dashed,line width=0.8pt] ({lx + 4.9:.2f},{ly})--({lx + 5.3:.2f},{ly});")
    f.tex(f"\\mk{{d}}{{cG}}{{{lx + 5.1}}}{{{ly}}}")
    f.text(lx + 5.45, ly, "second cohort (robustness, dashed)", "west")
    f.tex(f"\\mk{{s}}{{cG}}{{{lx + 11.2}}}{{{ly}}}")
    f.text(lx + 11.4, ly, "no adapter involved", "west")
    yn = f.notes(ly - 0.5, ["Higher = stronger rank agreement; the heavy line is zero (no rank association). 95\\% intervals. "
                            "Descriptive (surface D), not preregistered; retrospective against the WVS Wave 7 composite."])
    # estimates scored on fewer than the 42 countries are named here, not over the whiskers
    ex = [(c, lab) for c, lab in (("C9_a_adapter_human_risktaking_spearman_rho", "adapter--human, primary"),
                                  ("C9_b_adapter_human_risktaking_spearman_rho", "adapter--human, robustness"),
                                  ("C9_a_human_gps_risktaking_spearman_rho", "human--GPS"))
          if cell(rows, c, "n") != "42"]
    f.text(0.0, yn, "Risk taking is scored on fewer than 42 countries:", "west", "\\footnotesize\\itshape")
    f.text(0.0, yn - 0.4, "adapter--human:", "west", "\\footnotesize\\itshape")
    nx = 2.6
    for c, lab in ex:
        if lab == "human--GPS":
            f.lbl(c, "n", 0, 0.0, yn - 0.8, "west", prefix="human--GPS ($n=$", suffix=")")
        else:
            f.lbl(c, "n", 0, nx, yn - 0.4, "west", prefix=lab.split(", ")[1] + " ($n=$", suffix=")")
            nx += 4.0
    return f


# ----------------------------------------------------------------------------- Figure 2: information vs route


def fig2(rows):
    f = Fig("fig_info_vs_route", rows, "Trust rank agreement and distance to survey distributions by route (descriptive)")
    dy = 0.98
    cells = [  # label, trust-gps claim or None, tvd claim or None, style, colour
        ("Base model", None, "C9_TVD_base_mean_tvd_country_equal", "h", "cG"),
        ("First-cohort adapters", "B2_cohort1_trust_rho", "C9_TVD_adapter_mean_tvd_country_equal", "o", "cA"),
        ("Adapters + country-named prompt", "C9_TVD_adapter_persona_trust_gps_profile_block",
         "C9_TVD_adapter_persona_mean_tvd_country_equal", "t", "cD"),
        ("Country-named prompt (base model)", "PX_persona_trust_rho", "C9_TVD_persona_mean_tvd_country_equal", "s", "cB"),
        ("Sign-profile prompt (base model)", "PX_signprompt_trust_rho", None, "q", "cC"),
        ("Second-cohort adapters", "B2_bank2_trust_rho", None, "d", "cA"),
    ]
    top = 0.0
    ys = [top - 0.55 - i * dy for i in range(len(cells))]
    ybot = ys[-1] - 0.55
    pa = Panel(f, "A", 4.45, "-0.5", "1", 4.5, "Spearman rho (trust composite vs GPS trust coordinate), 42 countries",
               "profile-block bootstrap (26 blocks)")
    pb = Panel(f, "B", 10.8, "0.3", "0.55", 4.5, "mean total variation distance to survey answer shares, country-equal",
               "no interval banked for the four cell means")
    for p, ticks, dp, title, sub in (
            (pa, ["-0.5", "0", "0.5", "1"], 1, "A. TRUST only: rank agreement",
             "Spearman correlation with GPS trust\\\\higher = stronger rank agreement\\\\95\\% profile-block bootstrap"),
            (pb, ["0.3", "0.4", "0.5"], 1, "B. FULL strict battery: distance",
             "mean total variation distance (TVD)\\\\country-equal; lower = closer\\\\no interval banked")):
        f.zebra(p, ys, dy)
        f.axis(p, top, ybot, ticks, dp=dp, zero=(p is pa), title=title, sub=sub, tdy=1.45)
    for i, ((lab, tg, tv, m, col), y) in enumerate(zip(cells, ys)):
        bg = "zebra" if i % 2 == 0 else "white"
        f.text(4.3, y, lab, "east")
        if tg:
            f.ival(pa, tg, y - 0.05, m, col)
            if Decimal(cell(rows, tg, "value")) < Decimal("0.2"):  # beside the whisker, clear of the zero line
                f.lbl(tg, "value", 3, pa.x(cell(rows, tg, "hi")) + 0.12, y - 0.05, "west", fill=bg)
            else:
                f.lbl(tg, "value", 3, pa.x(cell(rows, tg, "value")), y + 0.20, "south", fill=bg)
        else:
            f.text(pa.x("0.1"), y, "\\shortstack[l]{undefined:\\\\constant composite}", "west", "\\footnotesize\\itshape")
        if tv:
            f.pval(pb, tv, y - 0.05, m, col)
            f.lbl(tv, "value", 3, pb.x(cell(rows, tv, "value")), y + 0.20, "south", fill=bg)
        else:
            f.text(pb.x("0.31"), y, "not scored", "west", "\\footnotesize\\itshape")
    # panel C: paired contrasts of mean TVD
    cy0 = ybot - 2.0
    contrasts = [
        ("Adapters minus base", "C9_TVD_adapter_minus_base_profile_block", "o", "cA"),
        ("Named prompt minus base", "C9_TVD_persona_minus_base_profile_block", "s", "cB"),
        ("Adapters + prompt minus base", "C9_TVD_adapter_persona_minus_base_profile_block", "t", "cD"),
        ("Adapters + prompt minus adapters", "C9_TVD_adapter_persona_minus_adapter_profile_block", "t", "cD"),
        ("Adapters + prompt minus prompt alone", "C9_TVD_adapter_persona_minus_persona_profile_block", "t", "cD"),
        ("Interaction (with minus without prompt)", "C9_TVD_interaction_profile_block", "h", "cG"),
    ]
    cys = [cy0 - 0.55 - i * dy for i in range(len(contrasts))]
    cbot = cys[-1] - 0.55
    pc = Panel(f, "C", 6.4, "-0.14", "0.12", 5.4, "paired difference in mean TVD", "paired profile-block bootstrap (26 blocks)")
    f.zebra(pc, cys, dy)
    f.axis(pc, cy0, cbot, ["-0.1", "0", "0.1"], dp=1, title="C. Paired differences in distance",
           sub="difference in mean TVD; paired profile-block bootstrap")
    for (lab, cid, m, col), y in zip(contrasts, cys):
        f.text(6.25, y, lab, "east")
        f.ival(pc, cid, y, m, col)
        f.lblci(cid, 3, 12.05, y, "west")
    f.text(pc.x("-0.135"), cbot - 0.75, "$\\leftarrow$ closer to survey", "west")
    f.text(pc.x("0.115"), cbot - 0.75, "farther $\\rightarrow$", "east")
    f.notes(cbot - 1.3, ["Descriptive (surface D), not preregistered. The base model's trust--GPS correlation is undefined "
                         "(constant composite), not zero. Trust is one dimension; TVD scores the full strict battery. "
                         "The crossing of the two readouts is descriptive: not a causal effect of fine-tuning, nor a "
                         "general law about weights versus prompts."])
    return f


# ----------------------------------------------------------------------------- Figure 3: retrospective screen


def fig3(rows):
    f = Fig("fig_screen", rows, "Retrospective item screen (registered A, permutation null, direct contrasts)")
    dy = 1.45
    top = 0.0
    ys = [top - 0.75, top - 0.75 - dy]
    ybot = ys[-1] - 0.6
    pa = Panel(f, "A", 3.2, "-0.15", "0.3", 5.0, "A: mean signed Spearman agreement with WVS-7 human country differences, selected items",
               "country bootstrap (42 countries)")
    pb = Panel(f, "B", 10.6, "-0.15", "0.3", 5.0, "A against its permutation null", "10,000 item-set permutations")
    ticks = ["-0.1", "0", "0.1", "0.2", "0.3"]
    f.zebra(pa, ys, dy)
    f.zebra(pb, ys, dy)
    f.axis(pa, top, ybot, ticks, dp=1, title="A. Size of $A$", sub="95\\% country-bootstrap interval", tdy=0.55)
    f.axis(pb, top, ybot, ticks, dp=1, title="B. $A$ against its null", sub="one-sided permutation $p$; no interval", tdy=0.55)
    routes = [("Trained adapters", "SCR_A_primary", "o", "cA", "SCR_p_perm", "SCR_null_q95", "SCR_null_mean"),
              ("Sign-profile prompt", "SP_A_primary", "q", "cB", "SP_p_perm", "SP_null_q95", None)]
    for (lab, a, m, col, pp, q95, nm), y in zip(routes, ys):
        f.text(3.05, y + 0.42, lab, "east")
        f.lbl(a, "n", 0, 3.05, y + 0.0, "east", suffix=" items")
        f.lblci(a, 3, 3.05, y - 0.42, "east")
        f.ival(pa, a, y, m, col)
        # panel B: observed A (no interval), null 95th percentile bar, null mean cross
        f.pval(pb, a, y, m, col)
        qv = cell(rows, q95, "value")
        pb.select()
        f.tex(f"\\draw[cG,line width=1.4pt] ({pb.x(qv):.3f},{y - 0.2:.3f})--({pb.x(qv):.3f},{y + 0.2:.3f});")
        pb.record(q95, "value", qv, "null_95th_percentile", {"y_cm": round(y, 3)})
        if nm:
            nv = cell(rows, nm, "value")
            f.tex(f"\\draw[cG,line width=0.9pt] ({pb.x(nv) - 0.07:.3f},{y - 0.07:.3f})--({pb.x(nv) + 0.07:.3f},{y + 0.07:.3f});")
            f.tex(f"\\draw[cG,line width=0.9pt] ({pb.x(nv) - 0.07:.3f},{y + 0.07:.3f})--({pb.x(nv) + 0.07:.3f},{y - 0.07:.3f});")
            pb.record(nm, "value", nv, "null_mean", {"y_cm": round(y, 3)})
        f.lbl(pp, "value", 4, pb.x("0.13"), y, "west", prefix="$p=$")
    # registered one-third-of-ceiling bar in panel A (a reference value; the table banks no interval for it)
    f.vref(pa, "SCR_one_third_ceiling", ybot, top - 0.0, "cG")
    ly = ybot - 0.95
    f.tex(f"\\draw[cG,dashed,line width=0.8pt] (0.0,{ly:.3f})--(0.5,{ly:.3f});")
    f.text(0.65, ly, "registered bar: one third of the wave 6--7 ceiling", "west", "\\footnotesize")
    f.text(0.65, ly - 0.42, "(a reference value; no interval banked)", "west", "\\footnotesize")
    f.lbl("SCR_one_third_ceiling", "value", 3, 6.6, ly - 0.42, "west", prefix="bar $=$")
    bx = 10.0
    f.tex(f"\\draw[cG,line width=1.4pt] ({bx:.2f},{ly - 0.13:.3f})--({bx:.2f},{ly + 0.13:.3f});")
    f.text(bx + 0.2, ly, "null 95th percentile", "west", "\\footnotesize")
    f.tex(f"\\draw[cG,line width=0.9pt] ({bx - 0.07:.3f},{ly - 0.55:.3f})--({bx + 0.07:.3f},{ly - 0.41:.3f});")
    f.tex(f"\\draw[cG,line width=0.9pt] ({bx - 0.07:.3f},{ly - 0.41:.3f})--({bx + 0.07:.3f},{ly - 0.55:.3f});")
    f.text(bx + 0.2, ly - 0.48, "null mean (adapters only)", "west", "\\footnotesize")
    # panel C: direct contrasts
    cy0 = ybot - 2.9
    groups = [("Adapters minus sign-profile prompt", [("own selected items", "SP_D_own", "o"), ("items both select", "SP_D_common", "h")]),
              ("Adapters minus face-valid reader", [("own selected items", "CMP_face_valid_D_own", "o"), ("items both select", "CMP_face_valid_D_common", "h")]),
              ("Adapters minus typed decision model", [("own selected items", "CMP_jev_D_own", "o"), ("items both select", "CMP_jev_D_common", "h")])]
    pc = Panel(f, "C", 5.0, "-0.3", "0.3", 6.2, "difference in A, adapters minus named route", "paired country bootstrap (2,000 draws)")
    rows_y, gy = [], []
    y = cy0 - 0.75
    for g, items in groups:
        gy.append(y)
        y -= 0.42
        for it in items:
            rows_y.append(y)
            y -= 0.6
        y -= 0.1
    cbot = y + 0.25
    f.axis(pc, cy0, cbot, ["-0.2", "-0.1", "0", "0.1", "0.2"], dp=1,
           title="C. Direct contrasts on the $A$ scale", sub="95\\% paired country bootstrap interval", tdy=0.55)
    k = 0
    for (g, items), yg in zip(groups, gy):
        f.text(0.0, yg, "\\textbf{" + g + "}", "west")
        for lab, cid, m in items:
            yy = rows_y[k]
            k += 1
            col = "cA"
            f.text(3.7, yy, lab, "east")
            f.lbl(cid, "n", 0, 4.85, yy, "east", prefix="$n=$")
            f.ival(pc, cid, yy, m, col)
            f.lblci(cid, 3, 11.45, yy, "west")
    f.notes(cbot - 0.65, ["Retrospective screen (WVS Wave 7); pre-piloting untested. An interval that covers zero is not "
                          "evidence of equivalence; the coverage-matched readers have only 5 and 9 common items.",
                          "The interval (A, C) and the permutation p (B) answer different questions: sampling variation "
                          "across countries versus rank among random item--sign assignments."])
    return f


# ----------------------------------------------------------------------------- Figure 4: factorial own effects


def nice(m):
    for s in ("0.05", "0.1", "0.2", "0.5", "1", "2", "5"):
        if m <= Decimal(s):
            return Decimal(s)
    return Decimal(10)


FX_ORDER = [("trust", "Trust"), ("negrecip", "Negative reciprocity"), ("altruism", "Altruism"),
            ("patience_Q50", "Patience (Q50)"), ("risktaking", "Risk taking"), ("patience_Q43", "Patience (Q43)"),
            ("posrecip", "Positive reciprocity")]


def fig4(rows):
    f = Fig("fig_factorial_own", rows, "Own effects of the six sign bits, trained vs prompted (full 7 x 6 matrix is not banked)")
    dy = 1.2
    top = 0.0
    ys = [top - 0.5 - i * dy for i in range(len(FX_ORDER))]
    CT, CP = 11.2, 13.6  # numeric columns: trained, prompt

    def headers(y):
        f.tex(f"\\mk{{o}}{{cA}}{{{CT - 1.35:.2f}}}{{{y:.3f}}}")
        f.text(CT, y, "trained", "east", "\\footnotesize")
        f.tex(f"\\mk{{q}}{{cB}}{{{CP - 1.35:.2f}}}{{{y:.3f}}}")
        f.text(CP, y, "prompt", "east", "\\footnotesize")

    f.text(0.0, top + 1.55, "\\textbf{A. Own (diagonal) effect of each sign bit on its own response surface}", "west")
    f.text(0.0, top + 1.1, "\\footnotesize\\textcolor{cS}{only the 7 own effects are banked, not the full 7$\\times$6 cross-effect matrix; no uncertainty interval is banked}", "west")
    f.text(0.0, top + 0.72, "\\footnotesize\\textcolor{cS}{raw composite units; each row has its own scale, so compare trained with prompt within a row, not across rows}", "west")
    headers(top + 0.25)
    for i, ((key, lab), y) in enumerate(zip(FX_ORDER, ys)):
        tb = f"FX_adapter64_{key}_own_beta"
        sb = f"FX_signprompt64_{key}_own_beta"
        mx = max(abs(Decimal(cell(rows, tb, "value"))), abs(Decimal(cell(rows, sb, "value"))))
        m = nice(mx)
        p = Panel(f, f"A{i + 1}", 3.6, str(-m), str(m), 5.2, f"own main effect on {lab} (composite units)", "none banked")
        p.select()
        xz, x0, x1 = p.x(0), p.x(-m), p.x(m)
        f.tex(f"\\fill[zebra] ({x0:.3f},{y - 0.3:.3f}) rectangle ({xz:.3f},{y + 0.3:.3f});")
        f.tex(f"\\draw[black,line width=0.9pt] ({xz:.3f},{y - 0.34:.3f})--({xz:.3f},{y + 0.34:.3f});")
        f.tex(f"\\draw[black,line width=0.5pt] ({x0:.3f},{y - 0.34:.3f})--({x1:.3f},{y - 0.34:.3f});")
        for t in (-m, Decimal(0), m):
            tx = p.x(t)
            f.tex(f"\\draw[black,line width=0.5pt] ({tx:.3f},{y - 0.34:.3f})--({tx:.3f},{y - 0.40:.3f});")
            f.tex(f"\\node[anchor=north,inner sep=1pt,font=\\scriptsize] at ({tx:.3f},{y - 0.40:.3f}) {{{fmt(t, 2 if m < 1 else 1)}}};")
        f.text(3.4, y, lab, "east")
        f.lval(p, tb, y + 0.07, "o", "cA")
        f.lval(p, sb, y - 0.10, "q", "cB")
        f.lbl(tb, "value", 3, CT, y, "east")
        f.lbl(sb, "value", 3, CP, y, "east")
    ya = ys[-1] - 1.0
    f.tex(f"\\fill[zebra] (3.6,{ya - 0.1:.3f}) rectangle (3.9,{ya + 0.1:.3f});")
    f.text(4.05, ya, "shaded half: against the intended direction of the bit", "west", "\\footnotesize")
    # panel B: entanglement summary
    summ = [("Bits dominant on their own surface (V5, of 6)", "FX_{r}64_V5_hits", "0", "6", ["0", "2", "4", "6"], 0),
            ("Own effects against intended direction (of 7)", "FX_{r}64_own_effects_wrong_signed", "0", "7", ["0", "3", "7"], 0),
            ("Surfaces whose largest mover is the trust bit (of 7)", "FX_{r}64_surfaces_largest_mover_is_trust_bit", "0", "7", ["0", "3", "7"], 0),
            ("Variance on first principal component", "FX_{r}64_pc1_share", "0", "1", ["0", "0.5", "1"], 1),
            ("Mean absolute correlation between surfaces", "FX_{r}64_mean_abs_inter_surface_r", "0", "1", ["0", "0.5", "1"], 1)]
    by0 = ya - 1.0
    f.text(0.0, by0, "\\textbf{B. Entanglement summary}", "west")
    f.text(0.0, by0 - 0.4, "\\footnotesize\\textcolor{cS}{counts and shares as banked; each row has its own scale; no interval banked}", "west")
    BT, BP = 12.2, 14.4
    hy = by0 - 0.85
    f.tex(f"\\mk{{o}}{{cA}}{{{BT - 1.35:.2f}}}{{{hy:.3f}}}")
    f.text(BT, hy, "trained", "east", "\\footnotesize")
    f.tex(f"\\mk{{q}}{{cB}}{{{BP - 1.35:.2f}}}{{{hy:.3f}}}")
    f.text(BP, hy, "prompt", "east", "\\footnotesize")
    sys_ = [hy - 0.75 - i * dy for i in range(len(summ))]
    for i, ((label, tpl, lo, hi, ticks, dp), y) in enumerate(zip(summ, sys_)):
        tid, sid = tpl.format(r="adapter"), tpl.format(r="signprompt")
        p = Panel(f, f"B{i + 1}", 6.3, lo, hi, 4.6, label, "none banked")
        p.select()
        x0, x1 = p.x(lo), p.x(hi)
        f.tex(f"\\draw[black,line width=0.5pt] ({x0:.3f},{y - 0.34:.3f})--({x1:.3f},{y - 0.34:.3f});")
        for t in ticks:
            tx = p.x(t)
            f.tex(f"\\draw[black,line width=0.5pt] ({tx:.3f},{y - 0.34:.3f})--({tx:.3f},{y - 0.40:.3f});")
            f.tex(f"\\node[anchor=north,inner sep=1pt,font=\\scriptsize] at ({tx:.3f},{y - 0.40:.3f}) {{{t}}};")
        f.text(6.1, y, label, "east", "\\footnotesize")
        f.lval(p, tid, y + 0.07, "o", "cA")
        f.lval(p, sid, y - 0.10, "q", "cB")
        f.lbl(tid, "value", 0 if dp == 0 else 3, BT, y, "east")
        f.lbl(sid, "value", 0 if dp == 0 else 3, BP, y, "east")
    yb = sys_[-1] - 1.1
    f.notes(yb, ["Trained: second-bank adapters; prompt: sign-profile prompt on the base model; 64 sign profiles, strict "
                 "battery, model side only. Descriptive. Bit-surface effects are changes in model response "
                 "distributions, not statements about internal mechanism."])
    return f


FIGS = [fig1, fig2, fig3, fig4]


# ----------------------------------------------------------------------------- manifest, verification, build


def build_all(rows, sha):
    figs = [fn(rows) for fn in FIGS]
    manifest = {
        "generator": "misc/paper_b/tools/build_figures.py",
        "inputs": [{"file": str(TABLE.relative_to(REPO)), "sha256": sha, "rows": len(rows)}],
        "note": "Every datum is the exact CSV string of the named claim_id and field. role=printed_label entries are numbers "
                "printed in the figure, rounded half-up from the same cell. x_cm positions are x0_cm + (value - data_min) * cm_per_unit.",
        "figures": [{"name": f.name, "title": f.title, "tex": f"{f.name}.tex", "pdf": f"{f.name}.pdf", "png": f"{f.name}.png",
                     "panels": f.panels, "data": f.data} for f in figs],
    }
    return figs, manifest


def write_sources(outdir, figs, manifest):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for f in figs:
        (outdir / f"{f.name}.tex").write_text(f.render(), encoding="utf-8")
    (outdir / "PLOT_MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=False) + "\n", encoding="utf-8")


def compile_figs(outdir, names, run=subprocess.run):
    """pdflatex (SOURCE_DATE_EPOCH fixed so the PDFs regenerate byte for byte) and pdftoppm previews."""
    outdir = Path(outdir)
    env = dict(os.environ, SOURCE_DATE_EPOCH="1760000000", FORCE_SOURCE_DATE="1", TEXMFVAR=str(outdir / ".texmf-var"))
    log = []
    for n in names:
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
            shutil.copy(outdir / f"{n}.tex", tmp)
            cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{n}.tex"]
            r = run(cmd, cwd=tmp, env=env, capture_output=True, text=True)
            log.append((" ".join(cmd), r.returncode))
            if r.returncode != 0:
                print(r.stdout[-3000:])
                raise SystemExit(f"pdflatex failed for {n}")
            shutil.copy(Path(tmp) / f"{n}.pdf", outdir / f"{n}.pdf")
        cmd = ["pdftoppm", "-png", "-r", "200", "-singlefile", str(outdir / f"{n}.pdf"), str(outdir / n)]
        r = run(cmd, env=env, capture_output=True, text=True)
        log.append((" ".join(cmd), r.returncode))
        if r.returncode != 0:
            raise SystemExit(f"pdftoppm failed for {n}")
    shutil.rmtree(outdir / ".texmf-var", ignore_errors=True)
    return log


MACRO = re.compile(r"^\\(ival|pval|lval|vref|lbl|lblci)((?:\{[^{}]*\})+)\s*$")
ARGS = re.compile(r"\{([^{}]*)\}")


def parse_tex(text):
    """Return the data-bearing macro calls in a figure's TeX as (macro, [args])."""
    out = []
    for line in text.splitlines():
        m = MACRO.match(line.strip())
        if m:
            out.append((m.group(1), ARGS.findall(m.group(2))))
    return out


def verify(figdir, table_path=TABLE, pinned=True):
    """Check figures/*.tex and PLOT_MANIFEST.json against the table. Returns a list of error strings."""
    errs = []
    rows, sha = load_table(table_path, pinned)
    figdir = Path(figdir)
    man = json.loads((figdir / "PLOT_MANIFEST.json").read_text())
    expected_figures, expected_manifest = build_all(rows, sha)
    if man != expected_manifest:
        errs.append("PLOT_MANIFEST.json differs from the generated manifest; regenerate before verification")
    expected_sources = {figure.name: figure.render() for figure in expected_figures}
    for fig in man["figures"]:
        tex = (figdir / fig["tex"]).read_text()
        if tex != expected_sources.get(fig["name"]):
            errs.append(f"{fig['name']}: TeX differs from the generated source; regenerate before verification")
        calls = parse_tex(tex)
        seen = set()
        for mac, a in calls:
            if mac in ("ival", "pval", "lval", "vref"):
                claim = a[0]
                if claim not in rows:
                    errs.append(f"{fig['name']}: unknown claim {claim}")
                    continue
                if mac == "ival":
                    got = {"ci_low": a[1], "value": a[2], "ci_high": a[3]}
                else:
                    got = {"value": a[1]}
                for col, s in got.items():
                    if s != rows[claim][col]:
                        errs.append(f"{fig['name']}: {claim}.{col} in TeX is {s}, table has {rows[claim][col]}")
                    seen.add((claim, col))
            elif mac == "lbl":
                claim, field, printed, prefix, suffix = a[:5]
                col = FIELD[field]
                s = rows[claim][col]
                exp = str(int(s)) if field == "n" else fmt(s, len(printed.split(".")[1]) if "." in printed else 0)
                if printed != exp:
                    errs.append(f"{fig['name']}: label {claim}.{col} prints {printed}, table rounds to {exp}")
            elif mac == "lblci":
                claim = a[0]
                for col, printed in zip(("value", "ci_low", "ci_high"), a[1:4]):
                    dp = len(printed.split(".")[1])
                    if printed != fmt(rows[claim][col], dp):
                        errs.append(f"{fig['name']}: ci label {claim}.{col} prints {printed}")
        # manifest agrees with the TeX
        for d in fig["data"]:
            if d["role"] == "printed_label":
                continue
            if d["claim_id"] not in rows or d["value"] != rows[d["claim_id"]][d["field"]]:
                errs.append(f"{fig['name']}: manifest datum {d['claim_id']}.{d['field']} disagrees with the table")
            if (d["claim_id"], d["field"]) not in seen and d["role"] not in ("null_95th_percentile", "null_mean"):
                errs.append(f"{fig['name']}: manifest datum {d['claim_id']}.{d['field']} is not drawn in the TeX")
        # endpoints and direction
        pan = {p["id"]: p for p in fig["panels"]}
        by = {}
        for d in fig["data"]:
            if d["role"] in ("interval_low", "point", "interval_high"):
                by.setdefault((d["panel"], d["claim_id"], d["y_cm"]), {})[d["role"]] = d
        for key, g in by.items():
            if len(g) == 3:
                lo, pt, hi = (Decimal(g[r]["value"]) for r in ("interval_low", "point", "interval_high"))
                if not lo <= pt <= hi:
                    errs.append(f"{fig['name']}: {key[1]} interval is not ordered low <= point <= high")
                if not (g["interval_low"]["x_cm"] <= g["point"]["x_cm"] <= g["interval_high"]["x_cm"]):
                    errs.append(f"{fig['name']}: {key[1]} drawn positions are not ordered")
        for d in fig["data"]:
            if d["role"] in ("interval_low", "point", "interval_high", "reference_line", "null_95th_percentile", "null_mean"):
                p = pan[d["panel"]]
                x = float(Decimal(p["x0_cm"]) + (Decimal(d["value"]) - Decimal(p["data_min"])) * Decimal(p["cm_per_unit"]))
                if abs(x - d["x_cm"]) > 1e-3:
                    errs.append(f"{fig['name']}: {d['claim_id']} x_cm {d['x_cm']} != mapped {x:.4f}")
                if Decimal(p["data_min"]) < 0 < Decimal(p["data_max"]):
                    xz = float(Decimal(p["x0_cm"]) + (0 - Decimal(p["data_min"])) * Decimal(p["cm_per_unit"]))
                    v = Decimal(d["value"])
                    if (v > 0) != (d["x_cm"] > xz) and v != 0:
                        errs.append(f"{fig['name']}: {d['claim_id']} is on the wrong side of the zero line")
                if not (Decimal(p["data_min"]) <= Decimal(d["value"]) <= Decimal(p["data_max"])):
                    errs.append(f"{fig['name']}: {d['claim_id']}.{d['field']} lies outside its panel axis")
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--table", default=str(TABLE))
    ap.add_argument("--out", default=str(FIGDIR))
    a = ap.parse_args(argv)
    if a.verify:
        errs = verify(a.out, a.table)
        for e in errs:
            print("ERROR", e)
        print("verify:", "FAIL" if errs else "ok")
        return 1 if errs else 0
    rows, sha = load_table(a.table)
    figs, manifest = build_all(rows, sha)
    write_sources(a.out, figs, manifest)
    n_data = sum(len(f["data"]) for f in manifest["figures"])
    print(f"wrote {len(figs)} TeX files and PLOT_MANIFEST.json ({n_data} manifest entries) to {a.out}")
    if not a.no_compile:
        for cmd, rc in compile_figs(a.out, [f.name for f in figs]):
            print(f"exit={rc}  {cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
