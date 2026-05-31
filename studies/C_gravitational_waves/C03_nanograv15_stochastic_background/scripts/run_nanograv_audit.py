"""
Study 23 audit: NANOGrav 15-yr stochastic GW background versus the ESD
gravitational-wave sector prediction.

ESD's prediction for propagating tensor modes is identical to General
Relativity (see Study 21): pure tensor polarizations propagating at c,
producing the Hellings-Downs (HD) inter-pulsar correlation pattern, and
with a stochastic background sourced by inspiralling supermassive black
hole binaries (SMBHBs) whose orbital evolution is GW-driven, giving
gamma_th = 13/3 for h_c^2(f) proportional to f^(-gamma).

Two audits:

  1. Spectral consistency: tension between the published HD-correlated
     posterior on gamma and the SMBHB prediction gamma = 13/3.
     Passes if the tension is below the standard 3-sigma threshold used
     in particle physics / cosmology to declare model compatibility.

  2. HD-correlation detection: the NANOGrav collaboration's headline
     evidence that the spatial correlations follow the HD pattern (as
     opposed to monopole, dipole, or uncorrelated alternatives).
     Passes if the published significance reaches the conventional
     3-sigma evidence level.

The study uses only published, peer-reviewed headline numbers - it does
not re-fit pulsar timing residuals or digitize plot points. Reproducing
the full likelihood is outside the scope of a consistency audit and would
require enterprise + the multi-GB NANOGrav data release.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow `python scripts/run_nanograv_audit.py` from the study root.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.esd_gw import SMBHB_EXPECTED_GAMMA  # noqa: E402
from scripts.observations import (  # noqa: E402
    NANOGRAV_15YR_HD_DETECTION,
    NANOGRAV_15YR_SPECTRAL,
)

# Standard physics convention: a discrepancy below 3 sigma is "compatible",
# 3-5 sigma is "tension", above 5 sigma is "incompatible".
TENSION_PASS_THRESHOLD_SIGMA = 3.0

# Conventional evidence threshold for claiming a detection.
HD_DETECTION_PASS_THRESHOLD_SIGMA = 3.0


def run_spectral_audit() -> tuple[bool, float]:
    """Test compatibility of the observed gamma posterior with the
    SMBHB-driven theoretical prediction gamma = 13/3."""
    obs = NANOGRAV_15YR_SPECTRAL
    theory = SMBHB_EXPECTED_GAMMA

    tension = abs(obs.gamma_median - theory) / obs.gamma_sigma
    passed = tension < TENSION_PASS_THRESHOLD_SIGMA

    print("--- Spectral index audit ---")
    print(f"  observed gamma   : {obs.gamma_median:.2f} +/- {obs.gamma_sigma:.2f}")
    print(f"  theory  gamma    : {theory:.4f}  (13/3, GW-driven SMBHB)")
    print(f"  tension          : {tension:.2f} sigma")
    print(f"  pass threshold   : < {TENSION_PASS_THRESHOLD_SIGMA:.1f} sigma")
    print(f"  source           : {obs.source}")
    print(f"  -> {'PASS' if passed else 'FAIL'}")
    return passed, tension


def run_hd_audit() -> tuple[bool, float]:
    """Test that NANOGrav's published HD evidence meets the conventional
    detection threshold required for an ESD-consistent (tensor-only) GWB."""
    obs = NANOGRAV_15YR_HD_DETECTION
    passed = obs.sigma_significance >= HD_DETECTION_PASS_THRESHOLD_SIGMA

    print("\n--- Hellings-Downs correlation audit ---")
    print(f"  published HD significance : {obs.sigma_significance:.1f} sigma")
    print(f"  HD vs CURN Bayes factor   : {obs.bayes_factor_hd_vs_curn:.0f}")
    print(f"  pass threshold            : >= {HD_DETECTION_PASS_THRESHOLD_SIGMA:.1f} sigma")
    print(f"  source                    : {obs.source}")
    print(f"  -> {'PASS' if passed else 'FAIL'}")
    return passed, obs.sigma_significance


def main() -> int:
    print("=" * 60)
    print(" ESD Study 23 audit: NANOGrav 15-yr stochastic GW background")
    print("=" * 60)

    spectral_pass, tension = run_spectral_audit()
    hd_pass, hd_sigma = run_hd_audit()

    print("\n--- Summary ---")
    print(f"  spectral gamma vs 13/3 : {'PASS' if spectral_pass else 'FAIL'}"
          f"  (tension = {tension:.2f} sigma)")
    print(f"  HD correlation pattern : {'PASS' if hd_pass else 'FAIL'}"
          f"  (significance = {hd_sigma:.1f} sigma)")

    overall = spectral_pass and hd_pass
    print()
    if overall:
        print("[OVERALL PASS] NANOGrav 15-yr results are consistent with ESD's")
        print("               GR-equivalent GW sector (Study 21 prediction).")
    else:
        print("[OVERALL FAIL] At least one ESD prediction is in tension with")
        print("               NANOGrav 15-yr results.")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
