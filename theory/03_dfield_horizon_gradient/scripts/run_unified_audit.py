"""Unified D-gradient audit: anchor eta to Study 25, predict Studies 28 & 29.

Run with: python scripts/run_unified_audit.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import dfield_gradient as dg


# ---------------------------------------------------------------------------
# Observed inputs (from Studies 25/28/29)
# ---------------------------------------------------------------------------

# Study 25 JOINT NVSS+CatWISE dipole (Secrest et al. 2022 combined fit)
# Best estimate ~ 0.0154; sigma ~ 0.0033 (4.35 sigma vs CMB-kinematic 0.00461)
D_OBS_JOINT = 0.0154
D_OBS_JOINT_SIGMA = 0.0033
V_CMB_KMS = 369.82

# Study 29 hemispherical asymmetry (Planck 2018 SMICA)
A_HEMI_OBS = 0.066
A_HEMI_OBS_SIGMA = 0.021

# Study 28 plane-of-satellites significances vs LCDM (per-host)
PLANE_SIGMAS = {"MW VPOS": 3.92, "M31 GPoA": 4.10, "CenA Plane": 3.30}
JOINT_PLANE_SIGMA = 6.54   # Stouffer if-independent (Study 28 result)


# ---------------------------------------------------------------------------
# Anchor eta to NVSS-band of the joint dipole (use NVSS depth + x as proxy)
# ---------------------------------------------------------------------------

def main() -> dict:
    out: dict = {}

    # Use NVSS-equivalent geometry as the anchor (literature convention)
    eta, eta_sigma = dg.anchor_eta_to_dipole(
        d_obs=D_OBS_JOINT,
        d_obs_sigma=D_OBS_JOINT_SIGMA,
        v_kms=V_CMB_KMS,
        x_eb=dg.X_NVSS,
        chi_mpc=dg.CHI_NVSS_MPC,
    )
    d_kin = dg.kinematic_dipole_amplitude(V_CMB_KMS, dg.X_NVSS)
    out["anchor"] = {
        "D_kin_NVSS_alpha0p75": d_kin,
        "D_obs_joint": D_OBS_JOINT,
        "D_obs_joint_sigma": D_OBS_JOINT_SIGMA,
        "D_excess": D_OBS_JOINT - d_kin,
        "eta_best": eta,
        "eta_sigma": eta_sigma,
        "eta_significance": abs(eta) / eta_sigma if eta_sigma > 0 else float("inf"),
    }

    print("=" * 72)
    print("UNIFIED D-GRADIENT AUDIT")
    print("=" * 72)
    print()
    print("STEP 1 - ANCHOR: fit eta to NVSS+CatWISE joint dipole")
    print("-" * 72)
    print(f"  D_kin (NVSS, alpha=0.75) = {d_kin:.5f}")
    print(f"  D_obs (joint)            = {D_OBS_JOINT:.4f} +/- {D_OBS_JOINT_SIGMA:.4f}")
    print(f"  D_excess                 = {D_OBS_JOINT - d_kin:.4f}")
    print(f"  eta_best                 = {eta:.4e}")
    print(f"  eta_sigma                = {eta_sigma:.4e}")
    print(f"  eta significance         = {abs(eta)/eta_sigma:.2f} sigma")
    print()

    # -----------------------------------------------------------------------
    # STEP 2: predict Study 29 hemispherical asymmetry (Starobinsky-locked xi_P)
    # -----------------------------------------------------------------------
    xi_P = dg.xi_P_starobinsky()
    A_hemi_pred = dg.hemispherical_asymmetry_amplitude(eta, xi_P=xi_P)
    A_hemi_pred_max = dg.hemispherical_asymmetry_amplitude(eta + eta_sigma, xi_P=xi_P)
    A_hemi_pred_min = dg.hemispherical_asymmetry_amplitude(eta - eta_sigma, xi_P=xi_P)
    delta_hemi_sigma = (A_hemi_pred - A_HEMI_OBS) / A_HEMI_OBS_SIGMA

    out["predict_study29_hemi"] = {
        "xi_P_starobinsky": xi_P,
        "A_hemi_obs": A_HEMI_OBS,
        "A_hemi_obs_sigma": A_HEMI_OBS_SIGMA,
        "A_hemi_pred": A_hemi_pred,
        "A_hemi_pred_lower": A_hemi_pred_min,
        "A_hemi_pred_upper": A_hemi_pred_max,
        "delta_in_sigma": delta_hemi_sigma,
        "ratio_pred_over_obs": A_hemi_pred / A_HEMI_OBS,
    }
    print("STEP 2 - PREDICT: Study 29 hemispherical asymmetry amplitude")
    print("-" * 72)
    print(f"  xi_P (Starobinsky plateau) = {xi_P:.4f}  (= 2*sqrt(2/3))")
    print(f"  A_hemi_obs                 = {A_HEMI_OBS:.4f} +/- {A_HEMI_OBS_SIGMA:.4f}")
    print(f"  A_hemi_pred                = {A_hemi_pred:.4f}")
    print(f"  pred / obs                 = {A_hemi_pred / A_HEMI_OBS:.2f}")
    print(f"  deviation                  = {delta_hemi_sigma:+.2f} sigma")
    print()

    # -----------------------------------------------------------------------
    # STEP 3: predict Study 28 satellite-plane alignment excess
    # -----------------------------------------------------------------------
    excess = dg.satellite_plane_alignment_excess(eta, xi_lss=10.0)
    out["predict_study28_planes"] = {
        "eta_used": eta,
        "xi_lss": 10.0,
        "p_perp_excess_above_0p5": excess,
        "p_perp_predicted": 0.5 + excess,
    }
    print("STEP 3 - PREDICT: Study 28 satellite-plane perpendicular-alignment excess")
    print("-" * 72)
    print(f"  P(plane normal perp to g_hat)  ~ 0.5 + {excess:+.4f}")
    print(f"                                 = {0.5 + excess:.4f}")
    print(f"  (vs random 0.5; significant if eta * xi_lss > 0.1)")
    print()

    # -----------------------------------------------------------------------
    # STEP 4: directional consistency - best-fit g_hat
    # -----------------------------------------------------------------------
    # Master Book has NO derivation of a preferred axis (Ch.3, Ch.15 silent).
    # The honest test is: does ANY single g_hat fit both the dipole-excess
    # axis and the Planck hemispherical-axis simultaneously, AND are
    # satellite-plane normals perpendicular to it?
    #
    # Weight: the dipole axis and hemi axis are equally constrained at
    # 4-5 sigma each. Satellite-plane normals: weight 0.5 each (3-4 sigma).
    targets_primary = [
        ("NVSS dipole",    dg.NVSS_DIPOLE_DIR_LB[0],    dg.NVSS_DIPOLE_DIR_LB[1],    1.0),
        ("CatWISE dipole", dg.CATWISE_DIPOLE_DIR_LB[0], dg.CATWISE_DIPOLE_DIR_LB[1], 1.0),
        ("Planck hemi",    dg.PLANCK_HEMI_AXIS_LB[0],   dg.PLANCK_HEMI_AXIS_LB[1],   1.0),
    ]
    (g_l, g_b), cost_primary, sep_primary = dg.best_fit_axis(targets_primary)

    # Re-evaluate all reference directions against the best-fit g_hat
    directions = {
        "Planck hemi axis":     dg.PLANCK_HEMI_AXIS_LB,
        "Quad-oct alignment":   dg.QUADRUPOLE_OCTOPOLE_AXIS_LB,
        "Cold Spot":            dg.COLD_SPOT_LB,
        "NVSS dipole":          dg.NVSS_DIPOLE_DIR_LB,
        "CatWISE dipole":       dg.CATWISE_DIPOLE_DIR_LB,
        "CMB peculiar-v apex":  dg.CMB_DIPOLE_DIR_LB,
        "MW VPOS normal":       dg.MW_VPOS_NORMAL_LB,
        "M31 GPoA normal":      dg.M31_GPOA_NORMAL_LB,
        "CenA plane normal":    dg.CENA_PLANE_NORMAL_LB,
    }
    sep_table = {}
    print("STEP 4 - DIRECTIONAL CONSISTENCY (best-fit g_hat over data)")
    print("-" * 72)
    print(f"  Master Book has NO derivation of preferred axis; we FIT g_hat")
    print(f"  using the three primary anisotropy data points (NVSS, CatWISE,")
    print(f"  Planck-hemi), each weighted equally.")
    print()
    print(f"  Best-fit g_hat (l, b) = ({g_l:.1f}, {g_b:+.1f})")
    print(f"  Sum-of-axis-separations: {cost_primary:.1f} deg over 3 targets")
    print(f"  Mean axis-separation:    {cost_primary / 3.0:.1f} deg")
    print()
    print(f"  {'Reference direction':<24} {'(l, b)':<18} {'axis sep [deg]':>14}")
    print("  " + "-" * 64)
    for name, (l, b) in directions.items():
        sep_pole = dg.angular_separation_deg(g_l, g_b, l, b)
        sep_axis = min(sep_pole, 180.0 - sep_pole)
        sep_table[name] = {
            "l_deg": l,
            "b_deg": b,
            "sep_to_g_axis_deg": sep_axis,
        }
        marker = "  <- primary fit" if name in ("Planck hemi axis", "NVSS dipole", "CatWISE dipole") else ""
        print(f"  {name:<24} ({l:6.1f}, {b:+6.1f})   {sep_axis:>10.1f}    {marker}")
    out["directional_consistency"] = {
        "g_hat_best_fit_lb": [g_l, g_b],
        "primary_sum_of_separations_deg": cost_primary,
        "primary_mean_separation_deg": cost_primary / 3.0,
        "separations": sep_table,
    }
    print()

    # Satellite-plane perpendicularity check
    plane_perp_seps = [
        ("MW VPOS",    abs(sep_table["MW VPOS normal"]["sep_to_g_axis_deg"] - 90.0)),
        ("M31 GPoA",   abs(sep_table["M31 GPoA normal"]["sep_to_g_axis_deg"] - 90.0)),
        ("CenA Plane", abs(sep_table["CenA plane normal"]["sep_to_g_axis_deg"] - 90.0)),
    ]
    print("  Satellite-plane PERPENDICULARITY check (|sep - 90 deg|):")
    for name, dev in plane_perp_seps:
        print(f"    {name:<14} dev = {dev:6.1f} deg")
    print()
    out["plane_perpendicularity_deviation_deg"] = dict(plane_perp_seps)

    # -----------------------------------------------------------------------
    # STEP 5: DISFORMAL channel prediction - quad-oct alignment along g_hat
    # -----------------------------------------------------------------------
    # The disformal sector B(D)(partial D)^2 adds a parity-even quadrupolar
    # contribution along the SAME g_hat as the conformal dipolar channel.
    # Sharp prediction: observed quad-oct alignment axis must lie within
    # ~30 deg of g_hat. No new free parameter.
    quad_axis_sep = dg.disformal_quadrupole_axis_match_deg((g_l, g_b))
    quad_amp_estimate = dg.disformal_amplitude_estimate(eta)
    print("STEP 5 - DISFORMAL CHANNEL: predict quad-oct axis along g_hat")
    print("-" * 72)
    print(f"  Disformal sector B(D)(partial D)^2 sources parity-even quadrupole")
    print(f"  along g_hat with no new free direction.")
    print()
    print(f"  Observed quad-oct alignment axis: (l, b) = (240.0, +60.0)")
    print(f"  Best-fit g_hat axis:              (l, b) = ({g_l:.1f}, {g_b:+.1f})")
    print(f"  Axis separation:                  {quad_axis_sep:.1f} deg   "
          f"{'PASS' if quad_axis_sep < 35.0 else 'FAIL'}")
    print(f"  Estimated A_2 amplitude (beta_B ~ beta_m^2): {quad_amp_estimate:.2e}")
    print(f"  (Observed quadrupole suppression is ~30%; this estimate is")
    print(f"   subleading at O(eta^2) ~ 2e-4 - directional signature only)")
    print()
    out["predict_disformal_quad_oct"] = {
        "axis_separation_deg": quad_axis_sep,
        "amplitude_estimate": quad_amp_estimate,
        "passes_axis_test_lt_35_deg": quad_axis_sep < 35.0,
    }

    # -----------------------------------------------------------------------
    # Verdict
    # -----------------------------------------------------------------------
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)

    ratio = A_hemi_pred / A_HEMI_OBS
    amp_match = 0.3 < ratio < 3.0
    primary_mean_sep = cost_primary / 3.0

    # Per-target rather than mean: each anisotropy axis must lie within
    # 35 deg of g_hat for honest agreement.
    primary_seps = {
        "NVSS dipole":    sep_table["NVSS dipole"]["sep_to_g_axis_deg"],
        "CatWISE dipole": sep_table["CatWISE dipole"]["sep_to_g_axis_deg"],
        "Planck hemi":    sep_table["Planck hemi axis"]["sep_to_g_axis_deg"],
    }
    n_pass_primary = sum(1 for v in primary_seps.values() if v < 35.0)
    dir_match_strict = n_pass_primary == 3
    dir_match_majority = n_pass_primary >= 2

    plane_pass = {n: dev < 30.0 for n, dev in plane_perp_seps}
    n_pass_planes = sum(plane_pass.values())
    plane_mean_dev = sum(d for _, d in plane_perp_seps) / 3.0

    disformal_pass = quad_axis_sep < 35.0

    out["verdict"] = {
        "hemi_amplitude_within_factor_3": amp_match,
        "primary_axes_individual_lt_35": primary_seps,
        "primary_axes_n_pass_of_3": n_pass_primary,
        "all_three_primary_axes_aligned": dir_match_strict,
        "majority_primary_axes_aligned": dir_match_majority,
        "plane_perp_individual_dev_deg": dict(plane_perp_seps),
        "planes_n_pass_of_3": n_pass_planes,
        "disformal_quad_oct_axis_aligned": disformal_pass,
        "amplitude_ratio_pred_over_obs": ratio,
        "primary_axes_mean_separation_deg": primary_mean_sep,
        "plane_perp_mean_deviation_deg": plane_mean_dev,
    }

    print(f"  Hemi amplitude   pred/obs = {ratio:.2f}    {'PASS' if amp_match else 'FAIL'}")
    print(f"  Primary anisotropy axes individually < 35 deg from g_hat:")
    for n, v in primary_seps.items():
        print(f"    {n:<16} sep = {v:5.1f} deg   {'PASS' if v < 35 else 'FAIL'}")
    print(f"  Satellite-plane perpendicularity (|sep - 90| < 30 deg):")
    for n, dev in plane_perp_seps:
        print(f"    {n:<14} dev = {dev:5.1f} deg   {'PASS' if dev < 30 else 'FAIL'}")
    print(f"  Disformal quad-oct axis  sep = {quad_axis_sep:5.1f} deg   "
          f"{'PASS' if disformal_pass else 'FAIL'}")
    print()
    n_pass_total = (
        int(amp_match) + n_pass_primary + n_pass_planes + int(disformal_pass)
    )
    print(f"  Net: {n_pass_total} of 8 sub-tests pass with 3 d.o.f. (eta, l, b)")
    print()

    passed = sum([amp_match, dir_match_strict, n_pass_planes == 3])
    if amp_match and dir_match_strict and n_pass_planes == 3:
        verdict = "UNIFIED PICTURE SUPPORTED - single eta + g_hat explains all three"
    elif amp_match and dir_match_majority and n_pass_planes >= 2:
        verdict = (
            "PARTIAL SUPPORT - amplitude OK, majority of axes & planes align, "
            "but at least one observable misses (most likely Planck-hemi axis or M31 GPoA)"
        )
    elif amp_match and (dir_match_majority or n_pass_planes >= 2):
        verdict = "WEAK SUPPORT - amplitude OK but only one directional class lines up"
    else:
        verdict = "FALSIFIED - unified gradient ansatz fails directional tests"

    out["verdict"]["summary"] = verdict
    print(f"  {verdict}")
    print()

    # Write JSON
    out_dir = Path(__file__).parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "unified_summary.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  Wrote {out_path}")
    return out


if __name__ == "__main__":
    main()
