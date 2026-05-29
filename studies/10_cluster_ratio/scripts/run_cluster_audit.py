"""Study 10 - cluster ratio C4 audit.

Verifies, against the published Hubble paper child C4:

  1. M_tot/M_b prediction reproduces X-COP / CHEX-MATE / Planck-SZ
     cluster baryon fractions at sub-2-sigma per sample.
  2. h-blindness Theorem 1: d ln (M_tot/M_b) / d h = 0 exactly at
     fixed (M_obs, R_obs, omega_b, omega_c).
  3. Cosmic asymptote: as u_cl -> infinity (deep Newton), the
     baryon fraction reaches Omega_b / Omega_m = 0.156 to <0.1%.

Exit 0 iff all three pass.
"""
from __future__ import annotations

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_cluster as C            # noqa: E402
import observations as OBS         # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------- gates --------------------------------------
GATE_MAX_PULL_R500   = 2.0     # direct-measurement samples
GATE_MAX_PULL_OUTER  = 3.0     # R_200c extrapolations (model-dependent)
GATE_HBLIND          = 1.0e-12 # exact h-blindness
GATE_COSMIC_REL      = 1.0e-3  # asymptote within 0.1% of Omega_b/Omega_m


def main() -> int:
    fails = []
    rows  = []

    # ---------- Claim 1: per-sample fb predictions ------------------
    sample_rows = []
    max_pull_r500  = 0.0
    max_pull_outer = 0.0
    for s in OBS.SAMPLES:
        if s.radius_def == "R_inf":
            continue
        u  = C.u_cluster(s.M_500_solar, s.R_def_mpc)
        fb_pred = C.baryon_fraction(u)
        pull = (s.f_b - fb_pred) / s.sigma
        if s.radius_def == "R_500c":
            max_pull_r500 = max(max_pull_r500, abs(pull))
        else:
            max_pull_outer = max(max_pull_outer, abs(pull))
        sample_rows.append({
            "sample":     s.name,
            "radius_def": s.radius_def,
            "u_cl":       u,
            "R_of_u":     C.R_of_u(u),
            "fb_pred":    fb_pred,
            "fb_obs":     s.f_b,
            "sigma":      s.sigma,
            "pull":       pull,
            "ref":        s.ref,
        })
    ok1 = max_pull_r500 <= GATE_MAX_PULL_R500
    rows.append({
        "claim":  "1a. C4 vs direct R_500c f_b (max pull)",
        "value":  max_pull_r500, "target": 0.0,
        "units":  "sigma",
        "metric": f"3 R_500c samples (X-COP, Planck-SZ, CHEX-MATE)",
        "gate":   f"max |pull| <= {GATE_MAX_PULL_R500}",
        "verdict": "PASS" if ok1 else "FAIL",
    })
    if not ok1: fails.append("Claim 1a")

    ok1b = max_pull_outer <= GATE_MAX_PULL_OUTER
    rows.append({
        "claim":  "1b. C4 vs R_200c extrapolations (max pull)",
        "value":  max_pull_outer, "target": 0.0,
        "units":  "sigma",
        "metric": "2 R_200c samples (model-dependent extrap.)",
        "gate":   f"max |pull| <= {GATE_MAX_PULL_OUTER}",
        "verdict": "PASS" if ok1b else "FAIL",
    })
    if not ok1b: fails.append("Claim 1b")

    # ---------- Claim 2: h-blindness exact -----------------------------
    hbl = C.h_blindness_C4()
    ok2 = hbl["h_blind"] and abs(hbl["dr_dh_rel"]) <= GATE_HBLIND
    rows.append({
        "claim":  "2. h-blindness of C4 (Thm 1)",
        "value":  hbl["dr_dh_rel"], "target": 0.0,
        "units":  "d ln (M_tot/M_b) / d h",
        "metric": f"M_tot/M_b = {hbl['value']:.4f}",
        "gate":   f"|dr/dh| <= {GATE_HBLIND}",
        "verdict": "PASS" if ok2 else "FAIL",
    })
    if not ok2: fails.append("Claim 2")

    # ---------- Claim 3: cosmic asymptote ------------------------------
    fb_asymp = C.baryon_fraction(1e6)   # u_cl >> 1 -> R -> 0
    fb_cosmic = C.OMEGA_B_LOCK / (C.OMEGA_B_LOCK + C.OMEGA_DM_LOCK)
    rel = (fb_asymp - fb_cosmic) / fb_cosmic
    ok3 = abs(rel) <= GATE_COSMIC_REL
    rows.append({
        "claim":  "3. cosmic asymptote f_b(u->inf) = Omega_b/Omega_m",
        "value":  fb_asymp, "target": fb_cosmic,
        "units":  "dimensionless",
        "metric": f"rel_err = {rel:+.3e}",
        "gate":   f"|rel_err| <= {GATE_COSMIC_REL}",
        "verdict": "PASS" if ok3 else "FAIL",
    })
    if not ok3: fails.append("Claim 3")

    # ---------------- write artifacts -----------------------------------
    with open(os.path.join(OUT_DIR, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
        for r in rows: w.writerow(r)

    with open(os.path.join(OUT_DIR, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys())); w.writeheader()
        for r in sample_rows: w.writerow(r)

    summary = {
        "claims":       rows,
        "samples":      sample_rows,
        "h_blindness":  hbl,
        "cosmic":       {"f_b_asymp": fb_asymp, "f_b_cosmic": fb_cosmic,
                         "rel_err": rel},
        "constants":    {"PHI": C.PHI, "Q": C.Q_EXP, "C_FLR": C.C_FLR,
                         "B_AMP": C.B_AMP, "S_NRM": C.S_NRM,
                         "DM_OVER_B": C.DM_OVER_B,
                         "A0_SI": C.A0_SI},
        "fails":        fails,
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    lines = []
    lines.append("=== Study 10: ESD cluster ratio C4 audit ===")
    lines.append("")
    lines.append("  Reproduces child C4 of the published Hubble paper")
    lines.append("  (Higginson 2026, Zenodo 10.5281/zenodo.20400097).")
    lines.append("")
    lines.append(f"  Locked: phi={C.PHI:.5f}  q={C.Q_EXP:.5f}  c={C.C_FLR:.5f}")
    lines.append(f"          b={C.B_AMP:.4f}  s={C.S_NRM:.4f}")
    lines.append(f"  Omega_DM / Omega_b = {C.DM_OVER_B:.4f}")
    lines.append("")
    header = f"  {'claim':<48}{'value':>14}{'target':>14}{'verdict':>10}"
    lines.append(header); lines.append("  " + "-" * (len(header) - 2))
    for r in rows:
        v = r["value"]; t = r["target"]
        v_s = f"{v:.4g}" if isinstance(v, float) else str(v)
        t_s = f"{t:.4g}" if isinstance(t, float) else str(t)
        lines.append(f"  {r['claim']:<48}{v_s:>14}{t_s:>14}{r['verdict']:>10}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  --- per-sample comparison ---")
    head = f"    {'sample':<42}{'u_cl':>8}{'R(u)':>8}{'fb_pred':>10}{'fb_obs':>10}{'pull':>8}"
    lines.append(head)
    for r in sample_rows:
        lines.append(f"    {r['sample']:<42}{r['u_cl']:>8.2f}{r['R_of_u']:>8.3f}"
                     f"{r['fb_pred']:>10.4f}{r['fb_obs']:>10.4f}{r['pull']:>+8.2f}")
    lines.append("")
    lines.append(f"  Cosmic asymptote: f_b(u->inf) = {fb_asymp:.6f}")
    lines.append(f"                     Omega_b/Omega_m = {fb_cosmic:.6f}")
    lines.append("")
    lines.append("  ===> ALL 4 C4 CLAIMS REPRODUCED" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    rc = 0 if not fails else 1
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "summary.txt"), "w") as f:
        f.write(text)

    # ---- Markdown ----
    md = ["# Study 10 - ESD cluster ratio C4 audit (Markdown)\n"]
    md.append(f"Reproduces child C4 of Higginson 2026 (Zenodo "
              f"10.5281/zenodo.20400097).\n")
    md.append("## Claims\n")
    md.append("| claim | value | target | metric | verdict |")
    md.append("|---|---:|---:|---|---|")
    for r in rows:
        v = r["value"]; t = r["target"]
        v_s = f"{v:.4g}" if isinstance(v, float) else str(v)
        t_s = f"{t:.4g}" if isinstance(t, float) else str(t)
        md.append(f"| {r['claim']} | {v_s} | {t_s} | {r['metric']} | **{r['verdict']}** |")
    md.append("\n## Per-sample comparison\n")
    md.append("| sample | radius | u_cl | R(u) | f_b pred | f_b obs | pull | reference |")
    md.append("|---|---|---:|---:|---:|---:|---:|---|")
    for r in sample_rows:
        md.append(f"| {r['sample']} | {r['radius_def']} | {r['u_cl']:.2f} | "
                  f"{r['R_of_u']:.3f} | {r['fb_pred']:.4f} | {r['fb_obs']:.4f} | "
                  f"{r['pull']:+.2f} | {r['ref']} |")
    with open(os.path.join(OUT_DIR, "tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(text)
    print(f"\n[cluster] wrote outputs to {OUT_DIR}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
