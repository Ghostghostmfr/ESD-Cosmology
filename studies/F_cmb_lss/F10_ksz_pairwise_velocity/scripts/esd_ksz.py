"""ESD prediction for kSZ pairwise-velocity amplitude.

Linear-regime velocity field: by Study 19 applicability theorem
R(u) does NOT act on linear cosmological modes. The pairwise
velocity v_12(r) at separations 10-150 Mpc/h probes purely linear
density-velocity correlations, so the ESD-predicted amplitude
equals the LCDM amplitude at fixed Omega_m, sigma_8.

Conventional kSZ-amplitude parameterization (relative to LCDM
fiducial):
    A_kSZ = (f * sigma_8 * tau_bar) / (f * sigma_8 * tau_bar)_LCDM

When the optical depth tau_bar is independently measured (e.g.
X-ray or thermal-SZ), A_kSZ -> A_growth = f*sigma_8 / (f*sigma_8)_LCDM
which is the framework-locked unity.
"""
from __future__ import annotations


def A_ksz_esd(z: float = 0.55) -> float:
    """ESD-predicted kSZ amplitude ratio relative to LCDM fiducial.

    By Study 19 theorem: identically 1.0 (linear modes excluded
    from R(u))."""
    return 1.0


def fisher_snr_forecast(survey_name: str) -> float:
    """Coarse Fisher SNR forecast for upcoming kSZ surveys.

    Numbers from Smith+ 2018 PRD 97, 083501 and Sato-Polito+ 2021
    scaled by sample/sky-area ratios."""
    fisher_table = {
        "Simons Obs. x DESI":  35.0,
        "CMB-S4 x DESI":       65.0,
        "CMB-S4 x LSST":       80.0,
        "CMB-HD x LSST":      130.0,
    }
    return fisher_table.get(survey_name, 0.0)
