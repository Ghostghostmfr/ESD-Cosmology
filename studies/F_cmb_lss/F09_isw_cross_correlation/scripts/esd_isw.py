"""ESD ISW x galaxy cross-correlation predictor (Study 35).

Linear-regime ISW is unmodified by R(u) per Study 19's applicability
theorem (Axiom A1 fails for linear delta of the cosmological field).
The ISW source term is

    dot(Phi + Psi) ~ - H(z) [f(z) - 1] (Phi + Psi)

which is fixed entirely by the background expansion H(z) and the
linear growth f(z) = Omega_m(z)^gamma. ESD's locked
Omega_m,0 = 0.31574 -> Omega_L,0 = 0.68426 reproduces the Planck-LCDM
ISW amplitude identically.

The Granett+ 2008 stacked-supervoid result (5x LCDM, 3.7sigma
discrepancy) is therefore shared by ESD; it is a *measurement*-side
anomaly, not a framework signal.
"""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE
from isw_data import (
    OMEGA_M0_LOCKED, OMEGA_L0_LOCKED, H0_KM_S_MPC,
    A_isw_esd, potential_decay_rate, Omega_L_locked,
)


def E_of_z(z: float) -> float:
    return (OMEGA_M0_LOCKED * (1.0 + z) ** 3 + OMEGA_L0_LOCKED) ** 0.5


def H_of_z_per_Mpc(z: float) -> float:
    return H0_KM_S_MPC * E_of_z(z) / 299792.458   # 1/Mpc


def isw_source_strength(z: float) -> float:
    """Magnitude of d ln(Phi+Psi)/d ln a, normalised so >0 means signal.

    In matter dom this is 0; in Lambda dom it is ~ 0.5.
    """
    return abs(potential_decay_rate(z))


def isw_amplitude_relative_to_lcdm() -> float:
    """ESD predicts the LCDM ISW amplitude: A = 1."""
    return A_isw_esd()


def isw_signal_to_noise_fisher(survey_z_med: float, f_sky: float = 0.5) -> float:
    """Crude Fisher S/N forecast for ISW x galaxy cross at z_med.

    Standard result: ISW S/N maxes around z ~ 0.5-1 with S/N ~ 5-7
    for a full-sky low-z galaxy survey. Above z ~ 2 the signal drops
    because Lambda becomes subdominant."""
    src = isw_source_strength(survey_z_med)
    # Heuristic: S/N ~ 10 * src * sqrt(f_sky) for z_med ~ 0.5
    base = 10.0 * src * f_sky ** 0.5
    # Lambda dominance cuts off at high z:
    if survey_z_med > 1.0:
        base *= (1.0 / survey_z_med) ** 0.5
    return base


def summary() -> dict:
    return {
        "applicability_theorem": (
            "Study 19: linear-regime ISW is unmodified by R(u); ESD = LCDM. "
            "Omega_L = 0.68426 locked by Identity B C2 fixes the amplitude."
        ),
        "Omega_m0_locked": OMEGA_M0_LOCKED,
        "Omega_L0_locked": OMEGA_L0_LOCKED,
        "H0_km_s_Mpc": H0_KM_S_MPC,
        "A_isw_esd": isw_amplitude_relative_to_lcdm(),
        "isw_source_strength_by_z": {
            f"{z:.2f}": isw_source_strength(z) for z in (0.0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0)
        },
        "fisher_snr_forecast": {
            "DESI_BGS_z_med_0p3":     isw_signal_to_noise_fisher(0.3, 0.4),
            "Euclid_NISP_z_med_1p0":  isw_signal_to_noise_fisher(1.0, 0.35),
            "LSST_gold_z_med_0p5":    isw_signal_to_noise_fisher(0.5, 0.45),
            "SKA1_HI_z_med_0p7":      isw_signal_to_noise_fisher(0.7, 0.7),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=2))
