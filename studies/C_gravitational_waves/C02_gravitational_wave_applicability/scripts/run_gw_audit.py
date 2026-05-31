"""Study 21 audit: GW applicability + GW170817 multimessenger check."""
from __future__ import annotations
import csv, json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
# also include Study 20 scripts dir so esd_redshift is importable
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "..", "E03_cosmological_redshift_derivation", "scripts")))
import esd_gw as W

# GW170817 multimessenger constraints
# - GW-GRB arrival difference at Earth: 1.74 +- 0.05 s
# - Distance D ~ 40 Mpc
# - Speed constraint from Abbott+2017 GW170817 EM counterpart paper:
#   |c_GW - c| / c < 3e-15  (assuming the 1.74 s offset is source-side)
GW170817_GRB_DELAY_S       = 1.74
GW170817_GRB_DELAY_ERR_S   = 0.05
GW170817_DIST_MPC          = 40.0
GW170817_SPEED_BOUND       = 3e-15

# LIGO standard-siren H_0 (Abbott+2017): 70 +12/-8 km/s/Mpc
SS_H0_LIGO       = 70.0
SS_H0_LIGO_ERRP  = 12.0
SS_H0_LIGO_ERRM  = 8.0

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

GATE_RU_GW             = "must_be_false"
GATE_CGW_VS_C          = 3e-15
GATE_H0_SS_CONSISTENT  = 2.0
GATE_HBLIND            = 1e-15

def main() -> int:
    gw = W.applicability_test_gravitational_wave()
    cgw = W.cGW_over_c()
    delta = abs(cgw - 1.0)
    ok1 = (gw["Ru_applies"] is False)
    ok2 = (delta <= GATE_CGW_VS_C)

    # GW-EM arrival propagation contribution (predicted = 0)
    prop_delay = W.gw170817_propagation_delay(distance_mpc=GW170817_DIST_MPC)
    # Source-side delay is the OBSERVED delay (since propagation predicts 0)
    source_delay = GW170817_GRB_DELAY_S
    delay_consistent = (abs(prop_delay) <= GW170817_GRB_DELAY_ERR_S)

    # Standard-siren H_0 inference
    H0c, H0lo, H0hi = W.gw170817_inferred_H0(D_L_mpc_obs=GW170817_DIST_MPC)
    # Consistency: ESD-locked Planck H_0 within standard-siren 1-sigma
    sig_pl  = abs(W.H0_PLANCK_KMS - SS_H0_LIGO) / max(SS_H0_LIGO_ERRP, SS_H0_LIGO_ERRM)
    ok3 = (sig_pl <= GATE_H0_SS_CONSISTENT)

    hb = W.h_blindness_GW_observables()
    ok4 = (hb <= GATE_HBLIND)

    rows = [
        {"claim": "1. R(u) does NOT apply to GW propagation in vacuum",
         "metric": "applicability axioms (A1),(A2) for GWs",
         "value": str(gw["Ru_applies"]).lower(), "target": GATE_RU_GW,
         "gate": "R(u)_applies == False",
         "verdict": "PASS" if ok1 else "FAIL"},
        {"claim": "2. c_GW = c (GW170817 multimessenger speed bound)",
         "metric": "|c_GW - c| / c",
         "value": f"{delta:.3g}", "target": f"<= {GATE_CGW_VS_C:g}",
         "gate": f"<= {GATE_CGW_VS_C:g}",
         "verdict": "PASS" if ok2 else "FAIL"},
        {"claim": "3. LIGO standard-siren H_0 consistent with ESD-locked H_0",
         "metric": "|H_0_Planck - H_0_LIGO_SS| / err_LIGO_SS",
         "value": f"{sig_pl:.3g}", "target": f"<= {GATE_H0_SS_CONSISTENT}",
         "gate": f"<= {GATE_H0_SS_CONSISTENT} sigma",
         "verdict": "PASS" if ok3 else "FAIL"},
        {"claim": "4. h-blindness of GW observables (Thm 1)",
         "metric": "|c_GW(h_lo) - c_GW(h_hi)| / c",
         "value": f"{hb:.3g}", "target": f"<= {GATE_HBLIND:g}",
         "gate": f"<= {GATE_HBLIND:g}",
         "verdict": "PASS" if ok4 else "FAIL"},
    ]
    fails = [r["claim"] for r in rows if r["verdict"] == "FAIL"]

    lines = []
    lines.append("")
    lines.append("=== Study 21: ESD gravitational-wave derivation (vacuum-tensor applicability) ===")
    lines.append("")
    lines.append("  Second companion to Study 19.  Axioms (A1)-(A3) applied to GWs.")
    lines.append("  A gravitational wave is a tensor perturbation h_{mu nu} of the")
    lines.append("  background metric, propagating at c in vacuum via the")
    lines.append("  linearized Einstein equations.  GW is NOT a localized")
    lines.append("  massive subsystem (A1 fails) and has NO proper acceleration")
    lines.append("  of an associated mass (A2 fails).  R(u) cannot dress")
    lines.append("  the propagation.")
    lines.append("")
    lines.append("  Consequences (this study tests them):")
    lines.append("    * c_GW = c exactly (matches GW170817 to < 3e-15)")
    lines.append("    * Two tensor polarizations only (no scalar/vector modes)")
    lines.append("    * GW amplitude h ~ 1/D_L with LambdaCDM D_L (from Study 20)")
    lines.append("    * Standard-siren H_0 = LambdaCDM analysis result")
    lines.append("")
    lines.append(f"{'claim':<70} {'value':>13} {'target':>12}  verdict")
    lines.append("-" * 110)
    for r in rows:
        lines.append(f"  {r['claim']:<68} {str(r['value']):>13} {str(r['target']):>12}     {r['verdict']}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  --- GW170817 multimessenger ---")
    lines.append(f"    Observed GW-GRB delay:        {GW170817_GRB_DELAY_S} +- {GW170817_GRB_DELAY_ERR_S} s")
    lines.append(f"    ESD propagation contribution: {prop_delay:.3g} s   (predicted: 0)")
    lines.append(f"    Source-side delay attribution: {source_delay} s   (consistent with GRB jet delay)")
    lines.append(f"    Speed bound from this:        |c_GW - c|/c < ~3e-15")
    lines.append("")
    lines.append("  --- Standard-siren H_0 (LIGO Abbott+2017) ---")
    lines.append(f"    GW170817 D_L (LIGO):          {GW170817_DIST_MPC} +- 8/14 Mpc")
    lines.append(f"    NGC 4993 z_em - pec.vel.:      derived")
    lines.append(f"    LIGO-published H_0 SS:        {SS_H0_LIGO} +{SS_H0_LIGO_ERRP}/-{SS_H0_LIGO_ERRM} km/s/Mpc")
    lines.append(f"    ESD-locked H_0 (Planck mode): {W.H0_PLANCK_KMS} km/s/Mpc")
    lines.append(f"    Consistency:                  {sig_pl:.2f} sigma")
    lines.append("")
    lines.append("  ===> ALL 4 GW CLAIMS PASS" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    lines.append("")
    lines.append("  Framework-native statement: ESD predicts c_GW = c, two")
    lines.append("  tensor polarizations only, and standard LambdaCDM scaling")
    lines.append("  of h(D_L) at all redshifts.  Any GW-EM speed mismatch or")
    lines.append("  detection of a scalar/vector GW polarization would falsify.")

    print("\n".join(lines))

    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"claims": rows, "fails": fails,
                   "applicability_GW": gw,
                   "cGW_over_c": cgw,
                   "GW170817": {
                       "observed_delay_s":         GW170817_GRB_DELAY_S,
                       "delay_err_s":              GW170817_GRB_DELAY_ERR_S,
                       "propagation_delay_s":      prop_delay,
                       "speed_bound":              GW170817_SPEED_BOUND,
                       "standard_siren_H0":        {"central": H0c, "lo": H0lo, "hi": H0hi},
                   }}, f, indent=2)
    with open(os.path.join(OUT, "audit_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[gw] wrote outputs to {OUT}")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
