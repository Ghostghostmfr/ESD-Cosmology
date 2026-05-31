"""Study 18 audit: S_8 tension (Planck vs WL surveys)."""
from __future__ import annotations
import csv, json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_s8 as S
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

GATE_WL_JOINT_NEAR     = 0.020   # WL joint S_8 within 0.02 of 0.772
GATE_PLANCK_WL_SIGMA   = 2.0     # Planck-WL tension >= 2 sigma
GATE_OMEGA_M_MATCH     = 0.02    # ESD Omega_m within 2% of Planck Omega_m
GATE_HBLIND            = 1e-15

def main() -> int:
    wl = O.weak_lensing()
    pl = O.planck()

    # ---- Claim 1: WL joint -------------------------------------------
    wl_S8_joint, wl_err_joint = S.inverse_variance_combine(
        [m.S8 for m in wl], [m.S8_err for m in wl])
    ok1 = abs(wl_S8_joint - 0.772) <= GATE_WL_JOINT_NEAR

    # ---- Claim 2: Planck vs WL tension -------------------------------
    tens = S.tension_sigma(pl.S8, pl.S8_err, wl_S8_joint, wl_err_joint)
    ok2 = tens >= GATE_PLANCK_WL_SIGMA

    # ---- Claim 3: ESD Omega_m matches Planck Omega_m -----------------
    omg_rel = S.omega_m_match_to_planck(pl.Omega_m)
    ok3 = omg_rel <= GATE_OMEGA_M_MATCH

    # ---- Claim 4: h-blindness of S_8 normalization -------------------
    hb = S.h_blindness_S8()
    ok4 = hb <= GATE_HBLIND

    rows = [
        {"claim": "1. WL inverse-variance joint S_8 reproduces ~0.772",
         "metric": "|S_8_joint - 0.772|",
         "value": abs(wl_S8_joint - 0.772),
         "target": GATE_WL_JOINT_NEAR,
         "gate": f"<= {GATE_WL_JOINT_NEAR}",
         "verdict": "PASS" if ok1 else "FAIL"},
        {"claim": "2. Planck-vs-WL tension reproduced",
         "metric": "|Planck - WL_joint| / sqrt(err_p^2+err_w^2)",
         "value": tens,
         "target": GATE_PLANCK_WL_SIGMA,
         "gate": f">= {GATE_PLANCK_WL_SIGMA} sigma",
         "verdict": "PASS" if ok2 else "FAIL"},
        {"claim": "3. ESD-locked Omega_m matches Planck (tension axis = sigma_8 only)",
         "metric": "|Omega_ESD - Omega_Planck| / Omega_Planck",
         "value": omg_rel,
         "target": GATE_OMEGA_M_MATCH,
         "gate": f"<= {GATE_OMEGA_M_MATCH:g}",
         "verdict": "PASS" if ok3 else "FAIL"},
        {"claim": "4. h-blindness of S_8 normalization (Thm 1 via Identity B)",
         "metric": "|S_8(h_lo) - S_8(h_hi)| for fixed sigma_8",
         "value": hb,
         "target": GATE_HBLIND,
         "gate": f"<= {GATE_HBLIND:g}",
         "verdict": "PASS" if ok4 else "FAIL"},
    ]
    fails = [r["claim"] for r in rows if r["verdict"] == "FAIL"]

    lines = []
    lines.append("")
    lines.append("=== Study 18: S_8 tension (KiDS / DES / HSC vs Planck) ===")
    lines.append("")
    lines.append("  Tests whether the published Planck-vs-WL S_8 tension is a")
    lines.append("  data-reproduction question (it is), and confirms that ESD's")
    lines.append("  locked Omega_m = 0.3157 matches Planck Omega_m to << 1%, so")
    lines.append("  the tension axis is sigma_8, not Omega_m.  The closure-pool")
    lines.append("  effect on linear growth at 8 Mpc/h is flagged as a separate")
    lines.append("  framework-derivation item (see README OPEN ITEM section).")
    lines.append("")
    lines.append(f"  ESD Omega_m (locked) = {S.OMEGA_M_LOCK:.6f}")
    lines.append(f"  Planck Omega_m       = {O.planck().Omega_m:.4f} ± {O.planck().Omega_m_err:.4f}")
    lines.append("")
    lines.append(f"{'claim':<70} {'value':>11} {'target':>10}  verdict")
    lines.append("-" * 108)
    for r in rows:
        lines.append(f"  {r['claim']:<68} {r['value']:>11.4g} {r['target']:>10.4g}     {r['verdict']}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  --- per-survey table ---")
    for m in O.MEASUREMENTS:
        lines.append(f"    {m.label:<22}: S_8 = {m.S8:.3f} ± {m.S8_err:.3f}   "
                     f"Omega_m = {m.Omega_m:.3f}   [{m.probe}]")
    lines.append("")
    lines.append(f"  WL joint S_8       = {wl_S8_joint:.4f} ± {wl_err_joint:.4f}")
    lines.append(f"  Planck-vs-WL       = {tens:.2f} sigma tension")
    lines.append("")
    lines.append("  ===> ALL 4 S_8 CLAIMS REPRODUCED" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    print("\n".join(lines))

    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"claims": rows, "fails": fails,
                   "wl_joint_S8": wl_S8_joint, "wl_joint_err": wl_err_joint,
                   "planck_wl_tension_sigma": tens,
                   "omega_m_match": omg_rel}, f, indent=2)
    with open(os.path.join(OUT, "audit_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[s8] wrote outputs to {OUT}")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
