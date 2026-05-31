"""ESD cluster mass-function predictor (Study 36).

Clusters are bound virialized subsystems -> Study 19 applicability
axioms hold -> R(u) applies. The conformal D-channel inside a
collapsing region enhances the effective Newton coupling by

    G_eff/G_N = 1 + w_D(u_cl) * R(u_cl).

In spherical collapse this shifts the linearly-extrapolated
threshold delta_c (Bryan & Norman 1998; Schmidt+ 2009 for f(R)):

    delta_c_ESD ~ delta_c_LCDM * (G_eff/G_N)^{-2/3}

A lower delta_c means halos collapse from smaller initial
overdensities, lifting the high-mass tail of n(M, z). The shift in
ln n(M) follows from the Press-Schechter / Sheth-Tormen exponential:

    ln(n_ESD / n_LCDM)  ~  -(delta_c_ESD^2 - delta_c_LCDM^2) / (2 sigma^2(M))

For typical cluster sigma(M ~ 1e14) ~ 0.5, a 5% reduction in
delta_c gives a ~20-30% lift in n(M, z) at the high-mass tail.

Crucially, sigma_8 (the linear-field rms) is UNMODIFIED by R(u)
(Study 19: linear modes excluded by Axiom A1). The HMF lift is
ENTIRELY from the threshold shift, not from changing the underlying
linear power spectrum.
"""
from __future__ import annotations

import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE
from cluster_data import (
    OMEGA_M0_LOCKED, SIGMA_8_LOCKED, S_8_LOCKED, DELTA_C_LCDM,
    A_0_MOND_SI, G_NEWTON_SI, M_SUN_KG, MPC_M,
    CLUSTER_PROBE_SCALES, g_vir_cluster_si, u_vir_cluster,
)

B_BRIDGE: float = PHI ** 6 - 2.0


def _sigma_terms(u: float) -> tuple[float, float, float]:
    return u ** PHI, B_BRIDGE * (u ** Q_BRIDGE), C_CHANNEL


def kernel_R(u: float) -> float:
    tS, tE, tD = _sigma_terms(u)
    return S_NORM / (tS + tE + tD)


def channel_weights(u: float) -> tuple[float, float, float]:
    tS, tE, tD = _sigma_terms(u)
    sigma = tS + tE + tD
    return tS / sigma, tE / sigma, tD / sigma


def G_eff_over_G_N(u: float) -> float:
    """Conformal D-channel enhancement of effective Newton coupling
    at scale u. Bulk-density-sourced collapse uses w_D * R."""
    wS, wE, wD = channel_weights(u)
    return 1.0 + wD * kernel_R(u)


def delta_c_esd(u: float) -> float:
    """ESD-modified spherical collapse threshold.

    Standard scalar-tensor result (Schmidt+ 2009 for f(R)):
        delta_c_eff ~ delta_c_LCDM * (G_eff/G_N)^{-2/3}
    """
    Geff = G_eff_over_G_N(u)
    return DELTA_C_LCDM * Geff ** (-2.0 / 3.0)


def sigma_M_approx(M_solar: float) -> float:
    """Crude sigma(M) at z=0 in LCDM with sigma_8 = 0.81.

    Fitting form: sigma(M) ~ sigma_8 * (M / M_8)^{-0.30} where
    M_8 ~ 4e14 Msun (mass inside 8 Mpc/h sphere at mean density).
    Power index -0.30 is the standard quasi-linear approximation.
    """
    M_8 = 4.0e14
    return SIGMA_8_LOCKED * (M_solar / M_8) ** (-0.30)


def hmf_lift_factor(M_solar: float, R_Mpc: float) -> float:
    """Ratio n_ESD(M) / n_LCDM(M) at z=0 from threshold shift.

    Press-Schechter exponential: n ~ exp(-delta_c^2 / 2 sigma^2).
    Ratio = exp((delta_c_LCDM^2 - delta_c_ESD^2) / (2 sigma^2)).
    """
    u = u_vir_cluster(M_solar, R_Mpc)
    dc_esd = delta_c_esd(u)
    sigma_M = sigma_M_approx(M_solar)
    exponent = (DELTA_C_LCDM ** 2 - dc_esd ** 2) / (2.0 * sigma_M ** 2)
    return math.exp(exponent)


def cluster_state(M_solar: float, R_Mpc: float) -> dict:
    u = u_vir_cluster(M_solar, R_Mpc)
    wS, wE, wD = channel_weights(u)
    R_k = kernel_R(u)
    return {
        "M_solar": M_solar, "R_Mpc": R_Mpc,
        "g_vir_si": g_vir_cluster_si(M_solar, R_Mpc),
        "u": u,
        "R_kernel": R_k,
        "w_S": wS, "w_E": wE, "w_D": wD,
        "G_eff_over_G_N": G_eff_over_G_N(u),
        "delta_c_LCDM": DELTA_C_LCDM,
        "delta_c_ESD":  delta_c_esd(u),
        "sigma_M":      sigma_M_approx(M_solar),
        "hmf_lift_factor": hmf_lift_factor(M_solar, R_Mpc),
    }


def summary() -> dict:
    out = {
        "applicability_theorem": (
            "Study 19: clusters ARE bound subsystems, all axioms hold, "
            "R(u) applies. ESD predicts a calculable enhancement of "
            "the high-mass tail of n(M, z) at zero new parameters."
        ),
        "Omega_m0_locked": OMEGA_M0_LOCKED,
        "sigma_8_locked":  SIGMA_8_LOCKED,
        "S_8_locked":      S_8_LOCKED,
        "delta_c_LCDM":    DELTA_C_LCDM,
        "cluster_states": {label: cluster_state(M, R) for (label, M, R) in CLUSTER_PROBE_SCALES},
    }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=2))
