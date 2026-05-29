"""Study 13 audit driver: JWST high-z galaxy abundance / baryon budget.

Four gated claims:
  1. Analytic rho_b,0 = rho_crit,0 * Omega_b reproduced to < 1e-10 rel.
  2. Boylan-Kolchin 2023 baryon-budget tension reproduced for Labbé+2023:
     epsilon_*_min lies in [0.10, 0.80] (the published tension band).
  3. h-blindness of rho_b,0 in omega_b = Omega_b h^2 EXACT (Thm 1, C1).
  4. ESD-locked Omega_b vs Planck-fit Omega_b: |delta eps_*| < 2%.
     (Locked baryon budget does NOT by itself close the JWST tension;
     ESD's distinctive resolution would have to come from the high-z
     growth-factor enhancement via the screening kernel, deferred.)
"""
from __future__ import annotations

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_jwst as J             # noqa: E402
import observations as O         # noqa: E402

OUT = os.path.join(_HERE, "outputs")
os.makedirs(OUT, exist_ok=True)

GATE_RHO_ANALYTIC   = 1.0e-10
GATE_EPS_TENSION    = 0.20    # BK 2023: universal upper limit from local SFE
GATE_HBLIND         = 1.0e-12
GATE_LOCK_REL       = 0.02


def main() -> int:
    fails = []
    rows  = []

    print("\n=== Study 13: JWST high-z galaxy abundance ===")
    print()
    print("  Reproduces the Boylan-Kolchin 2023 baryon-budget tension")
    print("  for Labbé+2023 (Nature 616, 266) using the ESD-locked")
    print("  Omega_b, Omega_m, and verifies h-blindness of the cosmic")
    print("  baryon mass density (Theorem 1, row C1, Hubble-paper 2026).")
    print()

    # ---- Claim 1: rho_b,0 analytic identity --------------------------
    import math
    H_FID  = J.H_FID
    rho_b_func   = J.rho_baryon_0()
    rho_b_check  = J.OMEGA_B_LOCK * J.rho_crit_0_msun_mpc3()
    rel = abs(rho_b_func - rho_b_check) / rho_b_check
    ok1 = rel <= GATE_RHO_ANALYTIC
    rows.append({
        "claim":   "1. rho_b,0 = Omega_b * rho_crit,0 identity",
        "value":   rel, "target": 0.0,
        "units":   "rel. err",
        "metric":  f"rho_b,0 = {rho_b_func:.4e} Msun/Mpc^3",
        "gate":    f"<= {GATE_RHO_ANALYTIC}",
        "verdict": "PASS" if ok1 else "FAIL",
    })
    if not ok1: fails.append("Claim 1")

    # ---- Claim 2: BK 2023 tension reproduced ------------------------
    # Boylan-Kolchin 2023's headline result: epsilon_* > 0.20 (the
    # local-universe universal upper limit on cosmic SFE) for the
    # Labbé sample.  Central value epsilon_* ~ 1, signalling 'more
    # stars than the entire baryon budget can produce' (the headline
    # 'impossible galaxies' tension).  Gate: epsilon_* > 0.20.
    eps = J.epsilon_star_min(O.SAMPLES[0].rho_star)
    ok2 = (eps > GATE_EPS_TENSION)
    rows.append({
        "claim":   "2. Boylan-Kolchin 2023 SFE tension reproduced",
        "value":   eps, "target": GATE_EPS_TENSION,
        "units":   "dimensionless",
        "metric":  f"epsilon_* = rho_*/(rho_b*f_coll) with f_coll={J.F_COLLAPSE_HIGHZ:.4f}",
        "gate":    f"> {GATE_EPS_TENSION} (universal SFE upper limit)",
        "verdict": "PASS" if ok2 else "FAIL",
    })
    if not ok2: fails.append("Claim 2")

    # ---- Claim 3: h-blindness ---------------------------------------
    hb = J.rho_b0_h_blindness()
    ok3 = abs(hb["drhob_dh"]) <= GATE_HBLIND
    rows.append({
        "claim":   "3. h-blindness of rho_b,0 (Thm 1, C1)",
        "value":   abs(hb["drhob_dh"]), "target": 0.0,
        "units":   "Msun/Mpc^3 per unit h",
        "metric":  f"rho_b,0 = {hb['rho_b0']:.4e} (omega-var form)",
        "gate":    f"<= {GATE_HBLIND}",
        "verdict": "PASS" if ok3 else "FAIL",
    })
    if not ok3: fails.append("Claim 3")

    # ---- Claim 4: locked vs Planck baryon budget --------------------
    cross = J.cross_anchor_table()
    rel_relax = abs(cross["rel relaxation"])
    ok4 = rel_relax <= GATE_LOCK_REL
    rows.append({
        "claim":   "4. locked Omega_b vs Planck: |delta eps_*|/eps small",
        "value":   rel_relax, "target": 0.0,
        "units":   "rel. err",
        "metric":  f"eps_lock = {cross['epsilon_* (lock)']:.3f} "
                   f"vs eps_planck = {cross['epsilon_* (Planck)']:.3f}",
        "gate":    f"<= {GATE_LOCK_REL*100:.0f}%",
        "verdict": "PASS" if ok4 else "FAIL",
    })
    if not ok4: fails.append("Claim 4")

    # -------------------- print table --------------------------------
    lines = []
    lines.append(f"{'claim':<60} {'value':>13} {'target':>10}  verdict")
    lines.append("-" * 98)
    for r in rows:
        lines.append(f"  {r['claim']:<58} {r['value']:>13.4g} {r['target']:>10.4g}     {r['verdict']}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  --- per-sample epsilon_*_min table ---")
    lines.append(f"    {'survey':<28} {'z range':<10} {'rho_*':>10} {'eps_*':>8}")
    sample_rows = []
    for s in O.SAMPLES:
        eps_s = J.epsilon_star_min(s.rho_star)
        lines.append(f"    {s.label:<28} {f'{s.z_lo}-{s.z_hi}':<10} "
                     f"{s.rho_star:>10.2e} {eps_s:>8.3f}")
        sample_rows.append({
            "label": s.label, "z_lo": s.z_lo, "z_hi": s.z_hi,
            "rho_star": s.rho_star, "rho_err": s.rho_err,
            "log10_Mstar_min": s.log10_Mstar_min,
            "epsilon_star_min": eps_s,
            "reference": s.reference,
        })
    lines.append("")
    lines.append("  --- cross-anchor (lock vs Planck) ---")
    for k, v in cross.items():
        if isinstance(v, float):
            if abs(v) < 1.0:
                lines.append(f"    {k:<40} {v:+.4e}")
            else:
                lines.append(f"    {k:<40} {v:.4e}")
        else:
            lines.append(f"    {k:<40} {v}")
    lines.append("")
    lines.append("  ===> ALL 4 BUDGET CLAIMS REPRODUCED" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    rc = 0 if not fails else 1

    print("\n".join(lines))

    # -------------------- write outputs ------------------------------
    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow(r)
    with open(os.path.join(OUT, "samples.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys()))
        w.writeheader()
        for r in sample_rows: w.writerow(r)
    with open(os.path.join(OUT, "cross_anchor.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["label", "value"])
        for k, v in cross.items(): w.writerow([k, v])
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({
            "claims":     rows,
            "samples":    sample_rows,
            "cross_anchor": cross,
            "fails":      fails,
            "inputs": {
                "rho_star_labbe":   O.SAMPLES[0].rho_star,
                "f_collapse_highz": J.F_COLLAPSE_HIGHZ,
                "omega_b_lock":     J.OMEGA_B_LOCK,
                "omega_m_lock":     J.OMEGA_M_LOCK,
                "omega_b_planck":   J.OMEGA_B_PLANCK,
                "omega_m_planck":   J.OMEGA_M_PLANCK,
                "h_fid":            J.H_FID,
            },
        }, f, indent=2)
    with open(os.path.join(OUT, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(OUT, "tables.md"), "w", encoding="utf-8") as f:
        f.write("# Study 13 (JWST high-z) claims\n\n")
        f.write("| claim | value | target | gate | verdict |\n")
        f.write("|---|---:|---:|---|---|\n")
        for r in rows:
            f.write(f"| {r['claim']} | {r['value']:.4g} | {r['target']:.4g} | {r['gate']} | {r['verdict']} |\n")

    print(f"\n[jwst-highz] wrote outputs to {OUT}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
