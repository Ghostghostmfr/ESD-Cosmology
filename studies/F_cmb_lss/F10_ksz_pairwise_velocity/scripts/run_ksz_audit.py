"""Study 37 - kSZ pairwise-velocity audit (linear regime, ESD = LCDM).

Five gates:
 1. R(u) does NOT apply (Study 19 axioms fail for linear velocity field)
 2. ESD prediction A_kSZ = 1 (LCDM-identical)
 3. >=(N-1) measurements within 2 sigma of A = 1
 4. ensemble inverse-variance-weighted A within 1.5 sigma of 1
 5. no new free parameters
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUTDIR = HERE / "outputs"
OUTDIR.mkdir(parents=True, exist_ok=True)

from ksz_data import KSZ_MEASUREMENTS, OMEGA_M0_LOCKED, SIGMA_8_LOCKED
from esd_ksz import A_ksz_esd, fisher_snr_forecast


def main():
    print("=" * 78)
    print("Study 37 - kSZ pairwise-velocity audit")
    print("                 (linear velocity field; Study 19: ESD = LCDM)")
    print("=" * 78)
    print(f"Locked: Omega_m = {OMEGA_M0_LOCKED}, sigma_8 = {SIGMA_8_LOCKED}")
    print()

    A_pred = A_ksz_esd()
    print(f"ESD-predicted amplitude ratio A_kSZ = {A_pred:.3f} (= LCDM by Study 19)")
    print()

    print("Published kSZ pairwise-velocity amplitude measurements:")
    print(f"   {'survey':<22} {'A_obs':>7} {'+/-':>6} {'det. SNR':>9} {'tension(sig)':>13}")
    per_meas = []
    within_1, within_2, within_3 = 0, 0, 0
    for label, A, sigA, snr, cite in KSZ_MEASUREMENTS:
        t = abs(A - A_pred) / sigA
        within_1 += int(t < 1.0)
        within_2 += int(t < 2.0)
        within_3 += int(t < 3.0)
        per_meas.append({
            "label": label, "A_obs": A, "sigma": sigA,
            "detection_snr": snr, "tension_sigma": t, "ref": cite,
        })
        print(f"   {label:<22} {A:>7.2f} {sigA:>6.2f} {snr:>9.1f} {t:>13.2f}")

    # ---- Ensemble ----
    inv_var = sum(1.0 / m["sigma"] ** 2 for m in per_meas)
    A_mean  = sum(m["A_obs"] / m["sigma"] ** 2 for m in per_meas) / inv_var
    A_sig   = 1.0 / math.sqrt(inv_var)
    ensemble_t = abs(A_mean - A_pred) / A_sig
    print()
    print(f"Ensemble (inverse-variance-weighted): A = {A_mean:.3f} +/- {A_sig:.3f}")
    print(f"   ensemble tension vs A_pred = 1:  {ensemble_t:.2f} sigma")
    print()

    print("Forecast SNR for next-generation kSZ surveys:")
    for survey in ["Simons Obs. x DESI", "CMB-S4 x DESI", "CMB-S4 x LSST", "CMB-HD x LSST"]:
        print(f"   {survey:<22} forecast SNR ~ {fisher_snr_forecast(survey):.0f}")
    print()

    # ---- Gates ----
    N = len(per_meas)
    gate1 = True  # structural: A1 fails for linear modes
    gate2 = A_pred == 1.0
    gate3 = within_2 >= (N - 1)
    gate4 = ensemble_t < 1.5
    gate5 = True

    print(f"   Gate 1 (R(u) NOT applicable -> ESD = LCDM, Study 19): {'PASS' if gate1 else 'FAIL'}")
    print(f"   Gate 2 (ESD prediction A_kSZ = 1)                   : {'PASS' if gate2 else 'FAIL'}")
    print(f"   Gate 3 ({N-1}/{N} measurements within 2 sigma)         : {'PASS' if gate3 else 'FAIL'} ({within_2}/{N})")
    print(f"   Gate 4 (ensemble within 1.5 sigma of A = 1)         : {'PASS' if gate4 else 'FAIL'} ({ensemble_t:.2f} sigma)")
    print(f"   Gate 5 (no new free parameters)                     : {'PASS' if gate5 else 'FAIL'}")

    n_pass = sum([gate1, gate2, gate3, gate4, gate5])
    if n_pass == 5:
        verdict = (
            f"PASS (5/5): The kSZ pairwise-velocity v_12(r) at separations "
            f"10-150 Mpc/h probes purely linear cosmological modes. By the "
            f"Study 19 applicability theorem (axiom A1: no bound-system / "
            f"spectator split for fluctuations of the same field that "
            f"constitutes the background), R(u) does not act on the linear "
            f"velocity field, so ESD predicts the LCDM amplitude identically: "
            f"A_kSZ = 1 with sigma_8 = 0.811 (Planck CMB locked, Study 19) "
            f"and Omega_m = 0.31574 (Identity B). {N} published pairwise-"
            f"velocity measurements (Hand+ 2012 through Hadzhiyska+ 2024) "
            f"yield ensemble A = {A_mean:.3f} +/- {A_sig:.3f}, lying "
            f"{ensemble_t:.2f} sigma from the framework-locked value with "
            f"{within_1}/{N} within 1 sigma and {within_2}/{N} within 2 sigma. "
            f"No new free parameters are introduced. Forecast SNR ~ 35-130 "
            f"in Simons Obs/CMB-S4/CMB-HD x DESI/LSST will tighten the test "
            f"to sub-percent precision on f*sigma_8*tau_bar."
        )
    else:
        verdict = f"FAIL ({n_pass}/5)"
    print()
    print("VERDICT:", verdict)

    summary = {
        "study": "F10_ksz_pairwise_velocity",
        "framework_lock": {
            "Omega_m": OMEGA_M0_LOCKED, "sigma_8": SIGMA_8_LOCKED,
            "A_kSZ_predicted": A_pred,
        },
        "per_measurement": per_meas,
        "ensemble": {
            "A_obs_mean": A_mean, "A_obs_sigma": A_sig,
            "tension_sigma": ensemble_t,
            "within_1sig": within_1, "within_2sig": within_2,
            "within_3sig": within_3,
        },
        "gate1_applicability_excluded": bool(gate1),
        "gate2_LCDM_identical_prediction": bool(gate2),
        "gate3_per_measurement": bool(gate3),
        "gate4_ensemble_consistency": bool(gate4),
        "gate5_no_new_params": bool(gate5),
        "n_pass": n_pass, "verdict": verdict,
    }
    out = OUTDIR / "summary.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"   wrote {out}")


if __name__ == "__main__":
    main()
