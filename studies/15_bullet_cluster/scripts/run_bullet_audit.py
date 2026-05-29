"""Study 15 audit driver: dissociative cluster mergers (Bullet et al.).

Four gated claims:
  1. ESD M_tot/M_gas for Bullet East matches Clowe+2006 within 30%.
  2. Joint fit to 4 dissociative mergers: mean |residual|/sigma < 2.0.
  3. h-blindness: M_tot/M_b exactly h-blind (Theorem 1, C4).
  4. Dark-sector dominance: Omega_DM/Omega_b is > 80% of M_tot/M_b
     at cluster densities, so the lensing peak follows a non-gas
     component - the structural resolution of the Bullet test.
"""
from __future__ import annotations

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_bullet as E       # noqa: E402
import observations as O     # noqa: E402

OUT = os.path.join(_HERE, "outputs")
os.makedirs(OUT, exist_ok=True)

GATE_BULLET_REL    = 0.30
GATE_MEAN_RESID    = 2.0
GATE_HBLIND        = 1.0e-20
GATE_DM_DOMINANCE  = 0.80


def main() -> int:
    fails = []
    rows  = []

    print("\n=== Study 15: Dissociative cluster mergers (Bullet et al.) ===")
    print()
    print("  Reproduces the M_tot/M_gas ratio for the iconic")
    print("  'kill-MOND' merging-cluster systems using the ESD")
    print("  closure-pool C4 expression (Higginson 2026, Theorem 1):")
    print()
    print("      M_tot / M_b = (1 + R(u_cl)) + Omega_DM/Omega_b")
    print()
    print(f"  Omega_DM/Omega_b (locked) = {E.DM_OVER_B:.4f}")
    print()

    # ---- Claim 1: Bullet East ratio matches Clowe+2006 --------------
    bullet_east = O.SAMPLES[0]
    M_b = bullet_east.M_gas * 1.0e13
    R   = bullet_east.aperture_kpc / 1000.0
    pred = E.predict_ratio(M_b, R)
    ratio_pred = pred["M_tot/M_b"]
    rel = abs(ratio_pred - bullet_east.ratio_obs) / bullet_east.ratio_obs
    ok1 = rel <= GATE_BULLET_REL
    rows.append({
        "claim":   "1. Bullet East M_tot/M_gas reproduced",
        "value":   rel, "target": 0.0,
        "units":   "rel. err",
        "metric":  f"ESD={ratio_pred:.3f} vs obs={bullet_east.ratio_obs:.3f}",
        "gate":    f"<= {GATE_BULLET_REL*100:.0f}%",
        "verdict": "PASS" if ok1 else "FAIL",
    })
    if not ok1: fails.append("Claim 1")

    # ---- Claim 2: Joint fit to 4 mergers ----------------------------
    sample_rows = []
    resid_sigs = []
    dm_dom_list = []
    for m in O.SAMPLES:
        M_b_si = m.M_gas * 1.0e13
        R_mpc  = m.aperture_kpc / 1000.0
        p = E.predict_ratio(M_b_si, R_mpc)
        ratio_pred = p["M_tot/M_b"]
        resid = ratio_pred - m.ratio_obs
        resid_sig = resid / m.ratio_err
        resid_sigs.append(abs(resid_sig))
        dm_dom = E.dm_dominance_fraction(M_b_si, R_mpc)
        dm_dom_list.append(dm_dom)
        sample_rows.append({
            "label":         m.label,
            "M_gas_1e13":    m.M_gas,
            "M_tot_obs_1e13":m.M_total,
            "ratio_obs":     m.ratio_obs,
            "ratio_err":     m.ratio_err,
            "ratio_ESD":     ratio_pred,
            "residual_sigma": resid_sig,
            "DM_dominance":  dm_dom,
            "offset_kpc":    m.offset_kpc,
        })
    mean_resid = sum(resid_sigs)/len(resid_sigs)
    ok2 = mean_resid <= GATE_MEAN_RESID
    rows.append({
        "claim":   "2. Joint 4-merger M_tot/M_gas fit",
        "value":   mean_resid, "target": 0.0,
        "units":   "mean |resid|/σ",
        "metric":  f"4 mergers: Bullet E, Bullet Main, MACS J0025, A520",
        "gate":    f"<= {GATE_MEAN_RESID}σ",
        "verdict": "PASS" if ok2 else "FAIL",
    })
    if not ok2: fails.append("Claim 2")

    # ---- Claim 3: h-blindness ---------------------------------------
    hb = E.h_blindness_C4_bullet()
    ok3 = abs(hb["drdh"]) <= GATE_HBLIND
    rows.append({
        "claim":   "3. h-blindness of M_tot/M_b (Thm 1, C4)",
        "value":   abs(hb["drdh"]), "target": 0.0,
        "units":   "rel. err",
        "metric":  f"M_tot/M_b = {hb['ratio']:.4f} (bit-identical across h)",
        "gate":    f"<= {GATE_HBLIND}",
        "verdict": "PASS" if ok3 else "FAIL",
    })
    if not ok3: fails.append("Claim 3")

    # ---- Claim 4: dark-sector dominance -----------------------------
    min_dm_dom = min(dm_dom_list)
    ok4 = min_dm_dom >= GATE_DM_DOMINANCE
    rows.append({
        "claim":   "4. Dark sector dominates (offset structurally allowed)",
        "value":   min_dm_dom, "target": GATE_DM_DOMINANCE,
        "units":   "fraction",
        "metric":  f"min over 4 mergers of (Omega_DM/Omega_b) / (M_tot/M_b)",
        "gate":    f">= {GATE_DM_DOMINANCE*100:.0f}%",
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
    lines.append("  --- per-merger table ---")
    lines.append(f"    {'system':<28} {'ratio_obs':>10} {'±':>6} {'ratio_ESD':>10} {'σ':>6} {'DM%':>6} {'off_kpc':>8}")
    for r in sample_rows:
        lines.append(f"    {r['label']:<28} {r['ratio_obs']:>10.3f} "
                     f"{r['ratio_err']:>6.3f} {r['ratio_ESD']:>10.3f} "
                     f"{r['residual_sigma']:>+6.2f} "
                     f"{r['DM_dominance']*100:>5.1f}% {r['offset_kpc']:>8.0f}")
    lines.append("")
    lines.append("  ===> ALL 4 BULLET CLAIMS REPRODUCED" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    rc = 0 if not fails else 1

    print("\n".join(lines))

    # -------------------- write outputs ------------------------------
    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow(r)
    with open(os.path.join(OUT, "mergers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys()))
        w.writeheader()
        for r in sample_rows: w.writerow(r)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({
            "claims":   rows,
            "mergers":  sample_rows,
            "fails":    fails,
            "inputs": {
                "omega_dm_lock": E.OMEGA_DM_LOCK,
                "omega_b_lock":  E.OMEGA_B_LOCK,
                "DM_over_B":     E.DM_OVER_B,
                "a_0_si":        E.A0_SI,
                "closure_pool": {
                    "p": E.P_EXP, "q": E.Q_EXP, "s": E.S_NRM,
                    "b": E.B_AMP, "c": E.C_FLR,
                },
            },
        }, f, indent=2)
    with open(os.path.join(OUT, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(OUT, "tables.md"), "w", encoding="utf-8") as f:
        f.write("# Study 15 (bullet cluster) claims\n\n")
        f.write("| claim | value | target | gate | verdict |\n")
        f.write("|---|---:|---:|---|---|\n")
        for r in rows:
            f.write(f"| {r['claim']} | {r['value']:.4g} | {r['target']:.4g} | {r['gate']} | {r['verdict']} |\n")

    print(f"\n[bullet] wrote outputs to {OUT}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
