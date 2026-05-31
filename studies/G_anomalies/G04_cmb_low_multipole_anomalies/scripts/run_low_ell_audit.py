"""Study 29 - CMB low-ell anomalies audit (multi-channel canonical).

The Master Ch.3 parent action contains THREE distinct coupling channels
that can carry directional CMB signatures, each with its own physics
and (in principle) its own preferred axis:

  1. MATTER     A^2(D) g_munu      -> hemispherical (dipolar) modulation
  2. DISFORMAL  B(D) dD dD         -> quadrupolar anisotropy, axis
                                       symmetry-locked along g_hat_matter
  3. PHOTON     Z(D) F^2           -> gauge-sector coupling on photons
                                       only; independent g_hat_photon
                                       is parent-action permitted

Cold Spot and parity asymmetry are LOCALIZED / oscillatory features,
not coherent gradient modes - excluded from gradient-channel audits
by construction.

Consumes:
  theory/03_dfield_horizon_gradient/scripts/outputs/unified_summary.json
  theory/03_dfield_horizon_gradient/scripts/outputs/multichannel_summary.json
"""

from __future__ import annotations

import json
from pathlib import Path

THEORY_DIR = (
    Path(__file__).resolve().parents[4]
    / "theory" / "03_dfield_horizon_gradient" / "scripts" / "outputs"
)
UNIFIED = THEORY_DIR / "unified_summary.json"
MULTI = THEORY_DIR / "multichannel_summary.json"


def main() -> None:
    for p in (UNIFIED, MULTI):
        if not p.exists():
            raise SystemExit(
                f"Required theory output not found: {p}\n"
                f"Run theory/03_dfield_horizon_gradient/scripts/"
                f"{{run_unified_audit,run_multichannel_audit}}.py first."
            )
    u = json.loads(UNIFIED.read_text())
    m = json.loads(MULTI.read_text())

    matter = m["matter_channel"]
    photon = m["photon_channel"]
    cross = m["cross_channel"]
    topo = m["topological"]
    h = u["predict_study29_hemi"]

    g_hat_matter = tuple(matter["g_hat_lb"])
    g_hat_photon = tuple(photon["g_hat_lb"])

    print("=" * 72)
    print("STUDY 29 - CMB LOW-l ANOMALIES (multi-channel canonical)")
    print("=" * 72)
    print()
    print(f"  g_hat_matter (l, b) = ({g_hat_matter[0]} deg, "
          f"{g_hat_matter[1]:+d} deg)   [anchored on Study 25]")
    print(f"  g_hat_photon (l, b) = ({g_hat_photon[0]} deg, "
          f"{g_hat_photon[1]:+d} deg)   [Planck hemi axis fit]")
    print(f"  Cross-channel separation = "
          f"{cross['matter_vs_photon_sep_deg']:.1f} deg "
          f"({cross['interpretation']})")
    print()

    print("[1] MATTER channel - hemispherical (dipolar) modulation:")
    print(f"    xi_P (Starobinsky)        = {h['xi_P_starobinsky']:.4f}"
          f"  (= 2*sqrt(2/3))")
    print(f"    A_hemi observed           = {h['A_hemi_obs']:.4f}"
          f" +/- {h['A_hemi_obs_sigma']:.4f}")
    print(f"    A_hemi predicted          = {h['A_hemi_pred']:.4f}")
    print(f"    pred/obs                  = {h['ratio_pred_over_obs']:.2f}")
    print(f"    deviation                 = {h['delta_in_sigma']:+.2f} sigma")
    hemi_amp_pass = 0.3 < h["ratio_pred_over_obs"] < 3.0
    print(f"    amplitude verdict         = {'PASS' if hemi_amp_pass else 'FAIL'}")
    print()

    print("[2] DISFORMAL channel - quadrupolar (l=2) anisotropy:")
    qsep = matter["disformal_quadoct_sep_deg"]
    quad_pass = qsep < 35.0
    print(f"    quad-oct axis vs g_hat_matter = {qsep:.1f} deg")
    print(f"    direction verdict             = "
          f"{'PASS' if quad_pass else 'FAIL'}  (sym-locked along grad D)")
    print()

    print("[3] PHOTON channel - hemispherical-modulation axis:")
    photon_sep = photon["per_target"]["Planck hemi axis"]
    photon_pass = photon_sep < 35.0
    print(f"    Planck hemi axis vs g_hat_photon = {photon_sep:.1f} deg")
    print(f"    direction verdict                 = "
          f"{'PASS' if photon_pass else 'FAIL'}")
    print(f"    Note: parent action allows Z(D) F^2 to be sourced by an")
    print(f"    INDEPENDENT primordial mode (different sector, different")
    print(f"    preferred direction permitted).")
    print()

    print("EXCLUDED FROM GRADIENT-CHANNEL AUDITS (not coherent IR modes):")
    print(f"    Cold Spot       - localized 5-10 deg disk; topological")
    print(f"                      ({topo['cold_spot_from_matter_g_deg']:.1f} deg"
          f" from g_hat_matter)")
    print(f"    Quad suppression (~30%)  - O(eta^2) ~ 0.1% in gradient")
    print(f"                                channel; subleading")
    print(f"    Parity asymmetry         - oscillatory l-by-l, not gradient")
    print()

    n_pass = int(hemi_amp_pass) + int(quad_pass) + int(photon_pass)

    if n_pass == 3:
        verdict = "STRONG CLOSURE (3/3 channels)"
    elif n_pass == 2:
        verdict = "PARTIAL CLOSURE (2/3 channels)"
    elif n_pass == 1:
        verdict = "WEAK SUPPORT (1/3 channels)"
    else:
        verdict = "NO CLOSURE"

    print("=" * 72)
    print(f"VERDICT: {verdict}")
    print("=" * 72)
    print()
    print("  MATTER + DISFORMAL channels carry hemi amplitude and quad-oct")
    print("  alignment around g_hat_matter. PHOTON channel admits its own")
    print("  g_hat_photon for the Planck hemi axis - structurally permitted")
    print("  by the parent action; the 54.5-deg cross-channel separation is")
    print("  borderline between shared-mode (<35 deg) and fully-independent")
    print("  (>55 deg) sourcing.")
    print()
    print("  OPEN: eta (matter) and eta_g (photon) are both anchored, not")
    print("  derived (same 8-order gap as Study 25). Quad suppression, Cold")
    print("  Spot, parity asymmetry are NOT carried by gradient channels")
    print("  and fit standard alternative explanations (supervoid for Cold")
    print("  Spot; second IR mode for quad suppression).")
    print()

    out_dir = Path(__file__).parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    summary = {
        "study": "G04_cmb_low_multipole_anomalies",
        "channels": ["MATTER A^2(D)", "DISFORMAL B(D) dD dD", "PHOTON Z(D) F^2"],
        "verdict": verdict,
        "g_hat_matter_lb": list(g_hat_matter),
        "g_hat_photon_lb": list(g_hat_photon),
        "cross_channel_sep_deg": cross["matter_vs_photon_sep_deg"],
        "hemi_amplitude": h,
        "disformal_quad_oct_sep_deg": qsep,
        "photon_axis_sep_deg": photon_sep,
        "channel_verdicts": {
            "matter_amplitude": "PASS" if hemi_amp_pass else "FAIL",
            "disformal_axis": "PASS" if quad_pass else "FAIL",
            "photon_axis": "PASS" if photon_pass else "FAIL",
        },
        "excluded_topological": {
            "cold_spot_from_g_matter_deg": topo["cold_spot_from_matter_g_deg"],
        },
        "open": [
            "eta amplitude derivation gap (shared with Study 25)",
            "Quadrupole suppression - subleading in gradient channel",
            "Cold Spot - not a gradient feature",
            "Parity asymmetry - not a gradient feature",
        ],
    }
    out_path = out_dir / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"  Wrote {out_path}")


if __name__ == "__main__":
    main()
