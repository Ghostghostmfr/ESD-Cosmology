"""Study 17 audit: ESD vs EHT shadow measurements."""
from __future__ import annotations
import csv, json, os, sys, math

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_eht as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

GATE_ESD_VS_GR_REL     = 1e-6   # ESD must match GR ring diameter to < 1e-6
GATE_OBS_VS_ESD_SIGMA  = 2.0    # ESD must be within 2σ of EHT measurement
GATE_R_AT_PHOTON_SPH   = 1e-10  # closure correction at photon sphere
GATE_HBLIND            = 1e-15  # θ_ring must be h-blind to extreme precision

def main() -> int:
    rows = []; sample = []
    worst_esd_vs_gr = 0.0
    worst_sigma     = 0.0
    worst_R         = 0.0
    worst_hblind    = 0.0
    for s in O.SOURCES:
        th_gr  = E.theta_ring_GR(s.M_solar, s.D_m)
        th_es, R = E.theta_ring_ESD(s.M_solar, s.D_m)
        rel    = abs(th_es - th_gr)/th_gr
        # combined obs-side σ from θ_err only (mass/distance enter
        # systematically into both pred and ratio; EHT quotes
        # combined θ_obs and its error)
        sig    = abs(th_es - s.theta_obs_rad)/s.theta_err_rad
        hb     = E.h_blindness_theta(s.M_solar, s.D_m)
        worst_esd_vs_gr = max(worst_esd_vs_gr, rel)
        worst_sigma     = max(worst_sigma, sig)
        worst_R         = max(worst_R, R)
        worst_hblind    = max(worst_hblind, hb)
        sample.append({
            "label": s.label,
            "theta_obs_muas": s.theta_obs_rad/E.MUAS,
            "theta_err_muas": s.theta_err_rad/E.MUAS,
            "theta_GR_muas":  th_gr/E.MUAS,
            "theta_ESD_muas": th_es/E.MUAS,
            "rel_ESD_vs_GR": rel,
            "R_at_photon_sphere": R,
            "sigma_obs_vs_ESD": sig,
            "h_blindness":  hb,
            "reference":    s.reference,
        })

    ok1 = worst_esd_vs_gr <= GATE_ESD_VS_GR_REL
    ok2 = worst_sigma     <= GATE_OBS_VS_ESD_SIGMA
    ok3 = worst_R         <= GATE_R_AT_PHOTON_SPH
    ok4 = worst_hblind    <= GATE_HBLIND

    rows = [
        {"claim": "1. ESD ring diameter matches GR (strong-field)",
         "metric": "max |θ_ESD - θ_GR|/θ_GR over M87*, Sgr A*",
         "value": worst_esd_vs_gr, "target": GATE_ESD_VS_GR_REL,
         "gate": f"<= {GATE_ESD_VS_GR_REL:g}",
         "verdict": "PASS" if ok1 else "FAIL"},
        {"claim": "2. EHT measurements consistent with ESD/GR",
         "metric": "max |θ_ESD - θ_obs|/θ_err over M87*, Sgr A*",
         "value": worst_sigma, "target": GATE_OBS_VS_ESD_SIGMA,
         "gate": f"<= {GATE_OBS_VS_ESD_SIGMA:g}σ",
         "verdict": "PASS" if ok2 else "FAIL"},
        {"claim": "3. Closure correction R(u) negligible at photon sphere",
         "metric": "max R(u_photon_sphere)",
         "value": worst_R, "target": GATE_R_AT_PHOTON_SPH,
         "gate": f"<= {GATE_R_AT_PHOTON_SPH:g}",
         "verdict": "PASS" if ok3 else "FAIL"},
        {"claim": "4. h-blindness of θ_ring (Thm 1 via a_0)",
         "metric": f"max |Δθ(H0_lo,H0_hi)|/θ_GR",
         "value": worst_hblind, "target": GATE_HBLIND,
         "gate": f"<= {GATE_HBLIND:g}",
         "verdict": "PASS" if ok4 else "FAIL"},
    ]
    fails = [r["claim"] for r in rows if r["verdict"] == "FAIL"]

    lines = []
    lines.append("")
    lines.append("=== Study 17: EHT photon-ring shadows (M87* + Sgr A*) ===")
    lines.append("")
    lines.append("  Strong-field test: at the photon sphere r = 3 GM/c²,")
    lines.append("  the Newtonian g is enormous so u = 4 g/a_0 is huge,")
    lines.append("  making the closure-pool correction R(u) ~ 1/u^p ≈ 0.")
    lines.append("  ESD should reproduce GR shadow predictions exactly to")
    lines.append("  any measurable precision, matching EHT observations.")
    lines.append("")
    lines.append(f"  a_0 (locked)        = {E.A0_SI:.4e} m/s^2")
    lines.append("")
    lines.append(f"{'claim':<60} {'value':>13} {'target':>10}  verdict")
    lines.append("-" * 98)
    for r in rows:
        lines.append(f"  {r['claim']:<58} {r['value']:>13.4g} {r['target']:>10.4g}     {r['verdict']}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  --- per-source table ---")
    for r in sample:
        lines.append(f"    {r['label']:<8}: θ_obs = {r['theta_obs_muas']:.2f} ± {r['theta_err_muas']:.2f} μas")
        lines.append(f"             θ_GR  = {r['theta_GR_muas']:.4f} μas")
        lines.append(f"             θ_ESD = {r['theta_ESD_muas']:.4f} μas  (rel vs GR = {r['rel_ESD_vs_GR']:.2e})")
        lines.append(f"             R(u_ps) = {r['R_at_photon_sphere']:.3e}     {r['sigma_obs_vs_ESD']:.2f}σ from obs")
    lines.append("")
    lines.append("  ===> ALL 4 EHT CLAIMS REPRODUCED" if not fails
                 else f"  ===> GATE FAIL on: {', '.join(fails)}")
    print("\n".join(lines))

    with open(os.path.join(OUT, "claims.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "sample.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sample[0].keys())); w.writeheader(); w.writerows(sample)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"claims": rows, "sample": sample, "fails": fails}, f, indent=2)
    with open(os.path.join(OUT, "audit_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[eht] wrote outputs to {OUT}")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
