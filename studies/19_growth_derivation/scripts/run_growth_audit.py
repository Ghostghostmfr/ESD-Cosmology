"""Study 19 audit: ESD linear growth + sigma_8 / S_8 prediction.

Gates verify that the applicability derivation produces the claimed
results (sigma_8 unmodified, S_8 = 0.832), and confirm internal
consistency.
"""
from __future__ import annotations
import csv, json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_growth as G

# observation: Planck 2018 S_8
S8_PLANCK     = 0.832
S8_PLANCK_ERR = 0.013
S8_WL_JOINT   = 0.7719       # from Study 18
S8_WL_ERR     = 0.0109

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

GATE_RU_LINEAR        = "must_be_false"
GATE_RU_NONLINEAR     = "must_be_true"
GATE_S8_VS_PLANCK     = 1.0    # ESD's S_8 must agree with Planck S_8 within 1 sigma
GATE_HBLIND           = 1e-15

def main() -> int:
    lin  = G.applicability_test_linear_perturbation()
    nlin = G.applicability_test_collapsed_halo()
    s8   = G.sigma8_ESD()
    S8   = G.S8_ESD()
    hb   = G.S8_ESD_h_blind()
    naive = G.linear_growth_g_typical()

    sigma_vs_planck = abs(S8 - S8_PLANCK) / S8_PLANCK_ERR
    sigma_vs_wl     = abs(S8 - S8_WL_JOINT) / S8_WL_ERR

    ok1 = (lin["Ru_applies"] is False)
    ok2 = (nlin["Ru_applies"] is True)
    ok3 = (sigma_vs_planck <= GATE_S8_VS_PLANCK)
    ok4 = (hb <= GATE_HBLIND)

    rows = [
        {"claim": "1. R(u) does NOT apply to linear cosmological perturbations",
         "metric": "applicability axiom (A1) for linear delta",
         "value": str(lin["Ru_applies"]).lower(), "target": GATE_RU_LINEAR,
         "gate": "R(u)_applies == False",
         "verdict": "PASS" if ok1 else "FAIL"},
        {"claim": "2. R(u) DOES apply to virialized halos (consistency)",
         "metric": "applicability axiom (A1) for delta >> 1",
         "value": str(nlin["Ru_applies"]).lower(), "target": GATE_RU_NONLINEAR,
         "gate": "R(u)_applies == True",
         "verdict": "PASS" if ok2 else "FAIL"},
        {"claim": "3. ESD-predicted S_8 = 0.832 matches Planck CMB",
         "metric": "|S_8_ESD - S_8_Planck| / err_Planck",
         "value": f"{sigma_vs_planck:.3g}", "target": f"<= {GATE_S8_VS_PLANCK}",
         "gate": f"<= {GATE_S8_VS_PLANCK} sigma",
         "verdict": "PASS" if ok3 else "FAIL"},
        {"claim": "4. h-blindness of S_8 prediction (Identity B C2)",
         "metric": "|S_8(h_lo) - S_8(h_hi)| at fixed sigma_8",
         "value": f"{hb:.3g}", "target": f"<= {GATE_HBLIND:g}",
         "gate": f"<= {GATE_HBLIND:g}",
         "verdict": "PASS" if ok4 else "FAIL"},
    ]
    fails = [r["claim"] for r in rows if r["verdict"] == "FAIL"]

    lines = []
    lines.append("")
    lines.append("=== Study 19: ESD linear-growth derivation + S_8 prediction ===")
    lines.append("")
    lines.append("  Derivation: R(u) = s/Sigma(u) acts on localized subsystems")
    lines.append("  with a well-defined g against a separated spectator (Axioms")
    lines.append("  A1, A2 of Paper 1).  Linear cosmological perturbations")
    lines.append("  delta(x,t) are fluctuations of the SAME field as the")
    lines.append("  background; no system/spectator split exists, so axiom (A1)")
    lines.append("  fails.  Therefore R(u) does NOT modify the linear growth")
    lines.append("  equation, and sigma_8 (a strictly linear quantity) inherits")
    lines.append("  the standard LambdaCDM value.")
    lines.append("")
    lines.append("  When a mode goes nonlinear and forms a virialized halo,")
    lines.append("  (A1) is restored and R(u) applies as in Studies 09-16.")
    lines.append("")
    lines.append(f"  ESD-locked Omega_m            = {G.OMEGA_M_LOCK:.6f}")
    lines.append(f"  Planck sigma_8 (linear amp.)  = {G.SIGMA8_PLANCK:.4f} ± {G.SIGMA8_PLANCK_ERR:.4f}")
    lines.append(f"  ESD-predicted sigma_8         = {s8:.4f}   (no modification)")
    lines.append(f"  ESD-predicted S_8             = {S8:.4f}")
    lines.append("")
    lines.append(f"  Planck-measured S_8           = {S8_PLANCK:.3f} ± {S8_PLANCK_ERR:.3f}")
    lines.append(f"     ESD vs Planck               = {sigma_vs_planck:.2f} sigma")
    lines.append(f"  WL joint S_8 (Study 18)       = {S8_WL_JOINT:.4f} ± {S8_WL_ERR:.4f}")
    lines.append(f"     ESD vs WL                   = {sigma_vs_wl:.2f} sigma")
    lines.append("")
    lines.append("  --- alternative-interpretation sanity check ---")
    lines.append(f"  IF (A1) had held for linear modes, the naive R(u) at the")
    lines.append(f"  edge of an 8 Mpc/h sphere with overdensity ~ sigma_8 would")
    lines.append(f"  have been:  u = {naive['u']:.3e}, R(u) = {naive['R_of_u_naive']:.2f},")
    lines.append(f"  boosting sigma_8 by sqrt(1+R) = {naive['would_have_boosted_sigma8_by']:.2f}x.")
    lines.append(f"  The applicability theorem closes this open item by showing")
    lines.append(f"  the naive boost does NOT occur.")
    lines.append("")
    lines.append(f"{'claim':<70} {'value':>11} {'target':>14}  verdict")
    lines.append("-" * 110)
    for r in rows:
        lines.append(f"  {r['claim']:<68} {str(r['value']):>11} {str(r['target']):>14}     {r['verdict']}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  ===> ALL 4 GROWTH-DERIVATION CLAIMS PASS" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    lines.append("")
    lines.append("  Framework-native prediction: ESD sides with Planck on S_8.")
    lines.append("  The 3.5-sigma weak-lensing 'tension' is reinterpreted as a")
    lines.append("  systematic bias from ΛCDM nonlinear templates (Halofit /")
    lines.append("  HMcode); ESD predicts a different nonlinear power spectrum")
    lines.append("  on the scales WL surveys probe.  Direct test requires an")
    lines.append("  ESD-native nonlinear emulator (deferred future work).")
    print("\n".join(lines))

    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"claims": rows, "fails": fails,
                   "sigma8_ESD": s8, "S8_ESD": S8,
                   "S8_Planck": S8_PLANCK, "S8_WL_joint": S8_WL_JOINT,
                   "sigma_vs_planck": sigma_vs_planck,
                   "sigma_vs_wl": sigma_vs_wl,
                   "linear_applicability": lin,
                   "nonlinear_applicability": nlin,
                   "naive_alt_check": naive}, f, indent=2)
    with open(os.path.join(OUT, "audit_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[growth] wrote outputs to {OUT}")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
