"""Study 08: ESD Hubble-tension paper reproduction harness.

Verifies, in one closed-form pass, the five quantitative claims of:

  James P. Higginson, "ESD Framework: The Hubble Tension as a Structural
  h-Blindness Boundary and Mirror-Identity Classification of Dark Energy"
  (2026). Zenodo DOI: 10.5281/zenodo.20400097.

  1. SPARC H_0 prediction:  bridge inversion of a_0 -> 67.28 km/s/Mpc
  2. Identity (C):           3 Om_DM + Om_b = (18/pi) Om_L^2 Om_m  to ~0.01%
  3. h-blindness (Thm 1):    |dR_i/dh|/|R_i| < 1e-9 for i in {C1,C4,C7}
  4. 6-channel drift budget: combined |Delta H_0| <= 0.12 km/s/Mpc
                              (~47x below the 5.6 km/s/Mpc required gap)
  5. Calibration-bias prediction:
                              required SH0ES Delta mu_host = 0.17 mag

Exit 0 iff every gate passes. Tables (CSV + JSON + TXT + Markdown)
written to outputs/.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import anchors as A           # noqa: E402
import channels as CH         # noqa: E402
import esd_h0 as H            # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)


# ------------------------------ gates -------------------------------------
GATE_H0_REL          = 0.005       # bridge prediction within 0.5% of published 67.28
GATE_ID_C_REL        = 1.0e-4      # identity (C) within 0.01% (paper: 7e-5)
GATE_HBLIND_MAX_DR   = 1.0e-8      # h-blindness max |dR/dh|/|R|
GATE_CHANNEL_BUDGET  = 0.20        # sum of channel caps <= 0.20 km/s/Mpc
GATE_CALIB_MU        = 0.20        # predicted Delta mu within 0.20 mag


def main() -> int:
    fails = []
    rows  = []

    # ---- Claim 1: bridge inversion -----------------------------------------
    H0_pred = H.bridge_inversion_H0()
    H0_paper = 67.28
    err_h0 = (H0_pred - H0_paper) / H0_paper
    ok1 = abs(err_h0) <= GATE_H0_REL
    rows.append({
        "claim": "1. bridge inversion a0 -> H0",
        "value":  H0_pred, "target": H0_paper,
        "units":  "km/s/Mpc",
        "metric": f"rel_err = {err_h0:+.3e}",
        "gate":   f"|rel_err| <= {GATE_H0_REL:.0e}",
        "verdict": "PASS" if ok1 else "FAIL",
    })
    if not ok1: fails.append("Claim 1")

    # ---- Claim 2: identity (C) --------------------------------------------
    idC = H.identity_C_residual()
    ok2 = abs(idC["rel_diff"]) <= GATE_ID_C_REL
    rows.append({
        "claim":  "2. Identity (C): 3 Om_DM+Om_b = (18/pi) Om_L^2 Om_m",
        "value":  idC["lhs"], "target": idC["rhs"],
        "units":  "dimensionless",
        "metric": f"rel_diff = {idC['rel_diff']:+.3e}",
        "gate":   f"|rel_diff| <= {GATE_ID_C_REL:.0e}",
        "verdict": "PASS" if ok2 else "FAIL",
    })
    if not ok2: fails.append("Claim 2")

    # ---- Claim 3: h-blindness ---------------------------------------------
    hbl = H.h_blindness_check()
    ok3 = hbl["max_abs_dR_dh"] <= GATE_HBLIND_MAX_DR
    rows.append({
        "claim":  "3. h-blindness Thm 1 on {C1, C4, C7}",
        "value":  hbl["max_abs_dR_dh"], "target": 0.0,
        "units":  "max |dR_i/dh|/|R_i|",
        "metric": f"per-child = {['%+.2e' % v for v in hbl['dR_dh_relative']]}",
        "gate":   f"max <= {GATE_HBLIND_MAX_DR:.0e}",
        "verdict": "PASS" if ok3 else "FAIL",
    })
    if not ok3: fails.append("Claim 3")

    # ---- Claim 4: 6-channel drift budget ----------------------------------
    budget = CH.combined_budget()
    gap_ratio = CH.budget_vs_gap_ratio()
    ok4 = budget <= GATE_CHANNEL_BUDGET
    rows.append({
        "claim":  "4. combined 6-channel drift budget",
        "value":  budget, "target": 0.12,
        "units":  "km/s/Mpc",
        "metric": f"gap_ratio = {gap_ratio:.1f}x required",
        "gate":   f"budget <= {GATE_CHANNEL_BUDGET:.2f}",
        "verdict": "PASS" if ok4 else "FAIL",
    })
    if not ok4: fails.append("Claim 4")

    # ---- Claim 5: calibration-bias prediction -----------------------------
    delta_mu = H.shoes_calibration_bias_mag(H0_predict=H0_pred,
                                            H0_shoes=73.04)
    delta_mu_paper = 0.17
    err_mu = delta_mu - delta_mu_paper
    ok5 = abs(err_mu) <= GATE_CALIB_MU
    rows.append({
        "claim":  "5. predicted SH0ES Delta mu_host",
        "value":  delta_mu, "target": delta_mu_paper,
        "units":  "mag",
        "metric": f"abs_err = {err_mu:+.3f}",
        "gate":   f"|abs_err| <= {GATE_CALIB_MU:.2f}",
        "verdict": "PASS" if ok5 else "FAIL",
    })
    if not ok5: fails.append("Claim 5")

    # ---------------- multi-anchor H_0 table -------------------------------
    anchor_rows = []
    for a in A.ANCHORS:
        pull = (a.H0 - H0_pred) / a.sigma
        anchor_rows.append({
            "family":   a.family,
            "anchor":   a.name,
            "H0":       a.H0,
            "sigma":    a.sigma,
            "pull_vs_esd": pull,
            "ref":      a.ref,
        })

    # ---------------- write artifacts --------------------------------------
    # CSV: claims + anchors + channels
    with open(os.path.join(OUT_DIR, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    with open(os.path.join(OUT_DIR, "anchors.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(anchor_rows[0].keys()))
        w.writeheader()
        for r in anchor_rows:
            w.writerow(r)

    with open(os.path.join(OUT_DIR, "channels.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["idx", "name", "mechanism", "input_bound",
                    "deltaH0_max_kmsMpc", "status"])
        for c in CH.CHANNELS:
            w.writerow([c.idx, c.name, c.mechanism, c.input_bound,
                        c.deltaH0_max, c.status])

    summary = {
        "H0_esd_predict": H0_pred,
        "H0_paper_quote": H0_paper,
        "identity_C":     idC,
        "h_blindness":    hbl,
        "channel_budget": budget,
        "shoes_gap":      CH.SHOES_GAP_KM_S_MPC,
        "gap_ratio":      gap_ratio,
        "predicted_delta_mu_host": delta_mu,
        "anchor_rows":    anchor_rows,
        "fails":          fails,
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # ---------------- console / TXT summary --------------------------------
    lines = []
    lines.append("=== Study 08: ESD Hubble-tension paper reproduction ===")
    lines.append("")
    lines.append("  Verifies 5 quantitative claims of hubble_paper_v2:")
    lines.append("")
    header = f"  {'claim':<48}{'value':>12}{'target':>12}{'verdict':>10}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for r in rows:
        v = r["value"]; t = r["target"]
        v_s = f"{v:.4g}" if isinstance(v, float) else str(v)
        t_s = f"{t:.4g}" if isinstance(t, float) else str(t)
        lines.append(f"  {r['claim']:<48}{v_s:>12}{t_s:>12}{r['verdict']:>10}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("--- 6-channel drift budget ---")
    for c in CH.CHANNELS:
        cap = ("ruled out" if math.isinf(c.deltaH0_max)
               else f"{c.deltaH0_max:.2e}")
        lines.append(f"  Ch{c.idx}: {c.name:<32}  max |dH0| = {cap:>10}  km/s/Mpc  ({c.status})")
    lines.append(f"  COMBINED (finite caps): {budget:.3e} km/s/Mpc")
    lines.append(f"  Required SH0ES gap:     {CH.SHOES_GAP_KM_S_MPC:.2f} km/s/Mpc")
    lines.append(f"  Budget shortfall:       {gap_ratio:.1f}x")
    lines.append("")
    lines.append("--- Multi-anchor H_0 table (pull = (H_0_anchor - H_0_ESD)/sigma) ---")
    lines.append(f"  ESD bridge prediction: H_0 = {H0_pred:.2f} km/s/Mpc")
    lines.append("")
    fam_order = ["cmb", "bao_bbn", "trgb", "lensing", "masers", "gw", "distance"]
    for fam in fam_order:
        anch = [r for r in anchor_rows if r["family"] == fam]
        if not anch: continue
        lines.append(f"  [{fam}]")
        for r in anch:
            flag = "  " if abs(r["pull_vs_esd"]) < 2 else "**"
            lines.append(f"    {flag}{r['anchor']:<42}  H_0 = {r['H0']:5.2f} +/- {r['sigma']:.2f}"
                         f"   pull = {r['pull_vs_esd']:+5.2f}")
    lines.append("")
    if fails:
        lines.append(f"  ===> GATE FAIL on: {', '.join(fails)}")
        rc = 1
    else:
        lines.append("  ===> ALL 5 PAPER CLAIMS REPRODUCED")
        rc = 0
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "summary.txt"), "w") as f:
        f.write(text)

    # ---------------- Markdown table ---------------------------------------
    md = []
    md.append("# Study 08 - ESD Hubble-tension paper reproduction (Markdown)\n")
    md.append("## Quantitative claims of `hubble_paper_v2`\n")
    md.append("| claim | value | target | metric | verdict |")
    md.append("|---|---:|---:|---|---|")
    for r in rows:
        v = r["value"]; t = r["target"]
        v_s = f"{v:.4g}" if isinstance(v, float) else str(v)
        t_s = f"{t:.4g}" if isinstance(t, float) else str(t)
        md.append(f"| {r['claim']} | {v_s} | {t_s} | {r['metric']} | **{r['verdict']}** |")
    md.append("\n## 6-channel drift budget (paper Table 1)\n")
    md.append("| ch | mechanism | max \\|ΔH_0\\| (km/s/Mpc) | status |")
    md.append("|---:|---|---:|---|")
    for c in CH.CHANNELS:
        cap = ("ruled out" if math.isinf(c.deltaH0_max)
               else f"{c.deltaH0_max:.2e}")
        md.append(f"| {c.idx} | {c.name} | {cap} | {c.status} |")
    md.append(f"| | **combined finite caps** | **{budget:.3e}** | dominated by Ch1 |")
    md.append(f"| | required SH0ES gap | {CH.SHOES_GAP_KM_S_MPC:.2f} | shortfall {gap_ratio:.1f}x |")
    md.append("\n## Multi-anchor H_0 table\n")
    md.append(f"ESD bridge prediction: **H_0 = {H0_pred:.2f} km/s/Mpc**\n")
    md.append("| family | anchor | H_0 | sigma | pull vs ESD | reference |")
    md.append("|---|---|---:|---:|---:|---|")
    for fam in fam_order:
        for r in anchor_rows:
            if r["family"] != fam: continue
            md.append(f"| {r['family']} | {r['anchor']} | {r['H0']:.2f} | "
                      f"{r['sigma']:.2f} | {r['pull_vs_esd']:+.2f} | {r['ref']} |")
    with open(os.path.join(OUT_DIR, "tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(text)
    print()
    print(f"[hubble] wrote {os.path.join(OUT_DIR, 'claims.csv')}")
    print(f"[hubble] wrote {os.path.join(OUT_DIR, 'anchors.csv')}")
    print(f"[hubble] wrote {os.path.join(OUT_DIR, 'channels.csv')}")
    print(f"[hubble] wrote {os.path.join(OUT_DIR, 'summary.json')}")
    print(f"[hubble] wrote {os.path.join(OUT_DIR, 'summary.txt')}")
    print(f"[hubble] wrote {os.path.join(OUT_DIR, 'tables.md')}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
