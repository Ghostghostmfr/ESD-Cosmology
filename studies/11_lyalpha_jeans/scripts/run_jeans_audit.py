"""Study 11 audit driver: ESD child C7 (Lyman-alpha Jeans cutoff).

Three gated claims:
  1. lambda_J (comoving) at fiducial m_22=1, z=3 within factor 2 of the
     paper's 94 kpc.  Factor-2 tolerance because the paper formula
     (pi/m_D) sqrt(c_s^2 / (G rho_m a^3)) is symbolic; the rigorous
     Hu-Barkana-Gruzinov quantum-Jeans length gives 64 kpc with the
     same omega_m, z, m_22.  Within factor 2 of 94 kpc <=> log10 ratio
     under 0.301.
  2. h-blindness of C7 (Theorem 1, row C7): d lambda_J / d h = 0
     EXACTLY when omega_m_h2 is held fixed.
  3. Scaling exponent lambda_J(m22) ~ m22^{-1/2} (the Hu-Barkana-Gruzinov
     result the paper expression must reproduce parametrically).
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_jeans as J             # noqa: E402
import observations as OBS        # noqa: E402

OUT = os.path.join(_HERE, "outputs")
os.makedirs(OUT, exist_ok=True)

# ---------------------------- gates --------------------------------------
GATE_LAMBDA_LOG_RATIO = math.log10(2.0)   # |log10(pred/paper)| <= log10(2)
GATE_HBLIND           = 1.0e-12           # exact
GATE_SLOPE_TOL        = 0.01              # |slope - (-0.5)| <= 0.01


def main() -> int:
    fails = []
    rows  = []

    print("\n=== Study 11: ESD child C7 (Lya Jeans cutoff) audit ===")
    print()
    print("  Reproduces row C7 of the published Hubble paper Theorem 1")
    print("  (Higginson 2026, Zenodo 10.5281/zenodo.20400097).")
    print()
    print(f"  Closure inputs: omega_m h^2 = {J.OMEGA_M_H2_FID:.4f}")
    print(f"                  m_D          = {J.M_D_FID_EV*1e22:.2f}e-22 eV")
    print(f"                  z            = {J.Z_FID:.1f}")
    print()

    # ---- Claim 1: numerical magnitude --------------------------------
    lam_pred = J.lambda_J_kpc(comoving=True)
    log_ratio = abs(math.log10(lam_pred / J.LAMBDA_J_PAPER))
    ok1 = log_ratio <= GATE_LAMBDA_LOG_RATIO
    rows.append({
        "claim":   "1. lambda_J(comoving) within factor 2 of paper 94 kpc",
        "value":   log_ratio, "target": 0.0,
        "units":   "|log10(pred/paper)|",
        "metric":  f"pred={lam_pred:.2f} kpc  vs  paper={J.LAMBDA_J_PAPER:.0f} kpc",
        "gate":    f"|log10| <= {GATE_LAMBDA_LOG_RATIO:.3f}  (factor 2)",
        "verdict": "PASS" if ok1 else "FAIL",
    })
    if not ok1: fails.append("Claim 1")

    # ---- Claim 2: h-blindness ---------------------------------------
    hb = J.h_blindness_C7()
    dr_dh = hb["dlambda_dh"]
    ok2 = abs(dr_dh) <= GATE_HBLIND
    rows.append({
        "claim":   "2. h-blindness of C7 (Thm 1)",
        "value":   abs(dr_dh), "target": 0.0,
        "units":   "kpc",
        "metric":  f"lambda_J(comov) = {hb['lambda_J_kpc']:.4f} kpc",
        "gate":    f"|d lambda_J / d h| <= {GATE_HBLIND}",
        "verdict": "PASS" if ok2 else "FAIL",
    })
    if not ok2: fails.append("Claim 2")

    # ---- Claim 3: scaling exponent lambda ~ m_22^{-1/2} -------------
    scan = J.lambda_vs_m22()
    m22  = np.array([r["m22"] for r in scan["rows"]])
    lam  = np.array([r["lambda_kpc_comov"] for r in scan["rows"]])
    slope, _ = np.polyfit(np.log10(m22), np.log10(lam), 1)
    ok3 = abs(slope - (-0.5)) <= GATE_SLOPE_TOL
    rows.append({
        "claim":   "3. lambda_J ~ m_22^{-1/2} scaling",
        "value":   slope, "target": -0.5,
        "units":   "d ln lambda / d ln m_22",
        "metric":  f"fit over m_22 in [0.1, 100]  (31 samples)",
        "gate":    f"|slope - (-0.5)| <= {GATE_SLOPE_TOL}",
        "verdict": "PASS" if ok3 else "FAIL",
    })
    if not ok3: fails.append("Claim 3")

    # ---- Per-bound Lyman-alpha comparison (informational) -----------
    lya_rows = []
    k_pred = J.k_cut_comoving_mpc_inv()
    for s in OBS.SAMPLES:
        lya_rows.append({
            "name":       s.name,
            "k_max_Mpc":  s.k_max_Mpc,
            "k_cut_pred": k_pred,
            "m22_bound":  s.m22_bound,
            "ref":        s.ref,
        })

    # -------------------- print table --------------------------------
    lines = []
    lines.append(f"{'claim':<60} {'value':>10} {'target':>10}  verdict")
    lines.append("-" * 95)
    for r in rows:
        lines.append(f"  {r['claim']:<58} {r['value']:>10.4g} {r['target']:>10.4g}     {r['verdict']}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append(f"  --- Lyman-alpha 1D power spectrum comparison ---")
    lines.append(f"  framework k_cut(z=3) = {k_pred:.2f} Mpc^-1 (comoving)")
    for s in OBS.SAMPLES:
        lines.append(f"    {s.name:<50} k_max={s.k_max_Mpc:>5.1f} Mpc^-1   m22>{s.m22_bound:>5.1f}")
    lines.append("")
    lines.append("  ===> ALL 3 C7 CLAIMS REPRODUCED" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    rc = 0 if not fails else 1

    print("\n".join(lines))

    # -------------------- write outputs ------------------------------
    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow(r)
    with open(os.path.join(OUT, "lya_samples.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lya_rows[0].keys()))
        w.writeheader()
        for r in lya_rows: w.writerow(r)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({
            "claims":      rows,
            "lya_samples": lya_rows,
            "scan":        scan["rows"],
            "fails":       fails,
            "inputs": {
                "omega_m_h2":     J.OMEGA_M_H2_FID,
                "m_D_eV":         J.M_D_FID_EV,
                "z":              J.Z_FID,
                "paper_lambda":   J.LAMBDA_J_PAPER,
                "predicted_lambda_kpc_comov": lam_pred,
                "predicted_k_cut_Mpc":         k_pred,
                "slope_lambda_vs_m22":          float(slope),
            },
        }, f, indent=2)
    with open(os.path.join(OUT, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(OUT, "tables.md"), "w", encoding="utf-8") as f:
        f.write("# Study 11 (C7) claims\n\n")
        f.write("| claim | value | target | gate | verdict |\n")
        f.write("|---|---:|---:|---|---|\n")
        for r in rows:
            f.write(f"| {r['claim']} | {r['value']:.4g} | {r['target']:.4g} | {r['gate']} | {r['verdict']} |\n")

    print(f"\n[lya-jeans] wrote outputs to {OUT}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
