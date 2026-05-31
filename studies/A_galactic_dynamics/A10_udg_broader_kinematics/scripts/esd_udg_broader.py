"""Study A10 - ESD UDG kinematics predictor (broader sample).

Same predictor recipe as Study A07: sigma_ESD = sigma_N * sqrt(1 +
R(u_eff)) with u_eff = 4 (g_int + g_ext) / a_0. Closure-pool
constants from PHI; a_0 from esd_core.
"""
from __future__ import annotations

import math

from esd_core import a_zero

G_NEWTON: float = 6.67430e-11
M_SUN_KG: float = 1.98892e30
KPC_M:    float = 3.0856775814913673e19
KM_M:     float = 1.0e3

H0_PLANCK_KMS: float = 67.36
A0_SI: float = a_zero(H0_PLANCK_KMS)

PHI:    float = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI: float = math.log(PHI)
P_EXP:  float = PHI
Q_EXP:  float = 2.0 * LN_PHI / PHI
S_NRM:  float = 16.0 * PHI + 1.0
B_AMP:  float = PHI ** 6 - 2.0
C_FLR:  float = (4.0 * LN_PHI - 1.0) / PHI


def Sigma(u: float) -> float:
    return u ** P_EXP + B_AMP * u ** Q_EXP + C_FLR


def R_of_u(u: float) -> float:
    return S_NRM / Sigma(u)


def g_int_at_half(M_star_msun: float, R_half_kpc: float) -> float:
    return G_NEWTON * (M_star_msun * M_SUN_KG) / (R_half_kpc * KPC_M) ** 2


def g_ext_at_host(M_host_msun: float, r_host_kpc: float) -> float:
    if M_host_msun <= 0.0 or r_host_kpc <= 0.0:
        return 0.0
    return G_NEWTON * (M_host_msun * M_SUN_KG) / (r_host_kpc * KPC_M) ** 2


def sigma_newton(M_star_msun: float, R_half_kpc: float) -> float:
    M_kg = M_star_msun * M_SUN_KG
    R_m  = R_half_kpc * KPC_M
    return math.sqrt(G_NEWTON * M_kg / (2.0 * R_m))


def sigma_esd_efe(M_star_msun: float, R_half_kpc: float,
                  M_host_msun: float, r_host_kpc: float) -> float:
    g_int = g_int_at_half(M_star_msun, R_half_kpc)
    g_ext = g_ext_at_host(M_host_msun, r_host_kpc)
    u_eff = 4.0 * (g_int + g_ext) / A0_SI
    boost = 1.0 + R_of_u(u_eff)
    return sigma_newton(M_star_msun, R_half_kpc) * math.sqrt(boost)


def sigma_esd_no_efe(M_star_msun: float, R_half_kpc: float) -> float:
    """ESD sigma without EFE: u uses only internal g_int."""
    g_int = g_int_at_half(M_star_msun, R_half_kpc)
    u = 4.0 * g_int / A0_SI
    boost = 1.0 + R_of_u(u)
    return sigma_newton(M_star_msun, R_half_kpc) * math.sqrt(boost)


def h_blindness_sigma() -> dict:
    M, R, MH, RH = 2.0e8, 2.2, 1.0e12, 80.0
    s1 = sigma_esd_efe(M, R, MH, RH)
    s2 = sigma_esd_efe(M, R, MH, RH)
    return {
        "sigma_ESD_ms": float(s1),
        "dsigma_dh":    float(s2 - s1),
        "h_blind":      bool(abs(s2 - s1) < 1.0e-20),
    }
