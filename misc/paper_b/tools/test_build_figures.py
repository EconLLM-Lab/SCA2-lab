"""Parent-owned adversarial checks for plots built from the frozen Paper B table.

Only the public/banked aggregate numbers table is read. No respondent inputs are opened.
"""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_figures as BF  # noqa: E402


def fresh_figures(tmp_path):
    rows, sha = BF.load_table()
    figures, manifest = BF.build_all(rows, sha)
    BF.write_sources(tmp_path, figures, manifest)
    return rows, figures, manifest


def test_frozen_table_pin_and_count():
    rows, sha = BF.load_table()
    assert len(rows) == 562
    assert sha == BF.TABLE_SHA


def test_modified_table_is_rejected(tmp_path):
    altered = tmp_path / "altered.csv"
    altered.write_bytes(BF.TABLE.read_bytes() + b"\n")
    with pytest.raises(SystemExit, match="is not the pinned"):
        BF.load_table(altered)


def test_generated_sources_and_manifest_are_deterministic(tmp_path):
    rows, figures, manifest = fresh_figures(tmp_path)
    again, manifest_again = BF.build_all(rows, BF.TABLE_SHA)
    assert manifest == manifest_again
    assert [f.render() for f in figures] == [f.render() for f in again]
    for figure in figures:
        assert (tmp_path / f"{figure.name}.tex").read_text() == figure.render()
    assert BF.verify(tmp_path) == []


def test_every_manifest_value_and_coordinate_matches_table(tmp_path):
    rows, _, manifest = fresh_figures(tmp_path)
    for figure in manifest["figures"]:
        panels = {panel["id"]: panel for panel in figure["panels"]}
        for datum in figure["data"]:
            value = rows[datum["claim_id"]][datum["field"]]
            assert datum["value"] == value
            if "x_cm" not in datum:
                continue
            panel = panels[datum["panel"]]
            coordinate = Decimal(panel["x0_cm"]) + (
                Decimal(value) - Decimal(panel["data_min"])
            ) * Decimal(panel["cm_per_unit"])
            assert abs(coordinate - Decimal(str(datum["x_cm"]))) <= Decimal("0.000051")
            assert Decimal(panel["data_min"]) <= Decimal(value) <= Decimal(panel["data_max"])


def test_three_links_keep_all_surfaces_and_both_adapter_cohorts(tmp_path):
    _, _, manifest = fresh_figures(tmp_path)
    figure = next(f for f in manifest["figures"] if f["name"] == "fig_three_links")
    points = {(d["panel"], d["claim_id"]) for d in figure["data"] if d["role"] == "point"}
    surfaces = ("trust", "risktaking", "posrecip", "altruism", "negrecip", "patience_q43", "patience_q50")
    expected = {
        (panel, f"C9_{cohort}_{relation}_{surface}_spearman_rho")
        for panel, relation in (("p1", "adapter_gps"), ("p2", "adapter_human"))
        for cohort in ("a", "b")
        for surface in surfaces
    }
    expected |= {("p3", f"C9_a_human_gps_{surface}_spearman_rho") for surface in surfaces}
    assert points == expected


def test_three_links_distinguish_bootstrap_units(tmp_path):
    _, _, manifest = fresh_figures(tmp_path)
    figure = next(f for f in manifest["figures"] if f["name"] == "fig_three_links")
    units = {p["id"]: p["interval"] for p in figure["panels"]}
    assert "profile-block" in units["p1"] and "profile-block" in units["p2"]
    assert "country bootstrap" in units["p3"]


def test_screen_keeps_direct_contrasts_not_just_separate_p_values(tmp_path):
    _, _, manifest = fresh_figures(tmp_path)
    figure = next(f for f in manifest["figures"] if f["name"] == "fig_screen")
    points = {d["claim_id"] for d in figure["data"] if d["role"] == "point" and d["panel"] == "C"}
    assert points == {
        "SP_D_own", "SP_D_common", "CMP_face_valid_D_own", "CMP_face_valid_D_common",
        "CMP_jev_D_own", "CMP_jev_D_common",
    }


def test_screen_criterion_is_human_country_differences_not_gps(tmp_path):
    _, _, manifest = fresh_figures(tmp_path)
    figure = next(f for f in manifest["figures"] if f["name"] == "fig_screen")
    panel = next(p for p in figure["panels"] if p["id"] == "A")
    assert "human" in panel["quantity"].lower()
    assert "with GPS" not in panel["quantity"]


def test_constant_base_ranking_is_not_plotted_as_zero(tmp_path):
    _, figures, manifest = fresh_figures(tmp_path)
    figure = next(f for f in manifest["figures"] if f["name"] == "fig_info_vs_route")
    ranking_ids = {d["claim_id"] for d in figure["data"] if d["panel"] == "A"}
    assert all("base_mean_tvd" not in claim for claim in ranking_ids)
    tex = next(f.render() for f in figures if f.name == "fig_info_vs_route")
    assert "undefined:" in tex and "constant composite" in tex


def test_mutating_plotted_point_is_caught(tmp_path):
    rows, _, _ = fresh_figures(tmp_path)
    target = tmp_path / "fig_three_links.tex"
    claim = "C9_a_adapter_gps_trust_spearman_rho"
    row = rows[claim]
    old = f"\\ival{{{claim}}}{{{row['ci_low']}}}{{{row['value']}}}"
    new = f"\\ival{{{claim}}}{{{row['ci_low']}}}{{0.0}}"
    text = target.read_text()
    assert old in text
    target.write_text(text.replace(old, new, 1))
    assert any(f"{claim}.value in TeX" in error for error in BF.verify(tmp_path))


def test_mutating_interval_endpoint_is_caught(tmp_path):
    rows, _, _ = fresh_figures(tmp_path)
    target = tmp_path / "fig_three_links.tex"
    claim = "C9_a_adapter_gps_trust_spearman_rho"
    old = f"\\ival{{{claim}}}{{{rows[claim]['ci_low']}}}"
    text = target.read_text()
    assert old in text
    target.write_text(text.replace(old, f"\\ival{{{claim}}}{{0.0}}", 1))
    assert any(f"{claim}.ci_low in TeX" in error for error in BF.verify(tmp_path))


def test_mutating_printed_label_is_caught(tmp_path):
    fresh_figures(tmp_path)
    target = tmp_path / "fig_info_vs_route.tex"
    old = r"\lbl{B2_cohort1_trust_rho}{value}{0.744}"
    text = target.read_text()
    assert old in text
    target.write_text(text.replace(old, r"\lbl{B2_cohort1_trust_rho}{value}{0.745}", 1))
    assert any("label B2_cohort1_trust_rho.value" in error for error in BF.verify(tmp_path))


def test_mutating_coordinate_transform_is_caught(tmp_path):
    fresh_figures(tmp_path)
    target = tmp_path / "fig_three_links.tex"
    old = r"\Px+((#1)-(\Pmin))*\Psc"
    text = target.read_text()
    assert old in text
    target.write_text(text.replace(old, r"\Px-((#1)-(\Pmin))*\Psc", 1))
    assert any("generated source" in error for error in BF.verify(tmp_path))


def test_dropped_manifest_figure_is_caught(tmp_path):
    fresh_figures(tmp_path)
    target = tmp_path / "PLOT_MANIFEST.json"
    manifest = json.loads(target.read_text())
    manifest["figures"].pop()
    target.write_text(json.dumps(manifest))
    assert any("generated manifest" in error for error in BF.verify(tmp_path))


def test_mutating_manifest_value_is_caught(tmp_path):
    fresh_figures(tmp_path)
    target = tmp_path / "PLOT_MANIFEST.json"
    manifest = json.loads(target.read_text())
    manifest["figures"][0]["data"][0]["value"] = "0.123456"
    target.write_text(json.dumps(manifest))
    assert any("manifest datum" in error for error in BF.verify(tmp_path))
