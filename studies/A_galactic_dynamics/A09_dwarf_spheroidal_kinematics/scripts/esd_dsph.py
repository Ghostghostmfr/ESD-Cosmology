"""Study A09 - ESD dwarf-spheroidal kinematic predictor.

Closure-pool kernel R(u) is built locally from PHI (identical recipe
to studies A02, A04, A06, A07). a_0 is imported from esd_core
(locked Planck-mode value).
"""
from __future__ import annotations

import math

from esd_core import a_zero  # locked a_0 via Identity B

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
G_NEWTON: float = 6.67430e-11                # m^3 kg^-1 s^-2
M_SUN_KG: float = 1.98892e30                 # kg
KPC_M:    float = 3.0856775814913673e19      # m
KM_M:     float = 1.0e3
V_C_MW_MS: float = 229.0e3                   # Eilers+ 2019 flat rotation
H0_PLANCK_KMS: float = 67.36

A0_SI: float = a_zero(H0_PLANCK_KMS)

# ---------------------------------------------------------------------------
# Closure-pool kernel constants from PHI
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Newton baseline + ESD with EFE
# ---------------------------------------------------------------------------
def g_int_at_half(M_star_msun: float, R_half_kpc: float) -> float:
    """Internal acceleration scale at the half-light radius."""
    return G_NEWTON * (M_star_msun * M_SUN_KG) / (R_half_kpc * KPC_M) ** 2


def g_ext_at_distance(D_gc_kpc: float) -> float:
    """MW external field at galactocentric distance D_gc, flat V_c."""
    return V_C_MW_MS ** 2 / (D_gc_kpc * KPC_M)


def sigma_newton(M_star_msun: float, R_half_kpc: float) -> float:
    """Wolf+ 2010 single-component Newtonian estimator (LOS)."""
    M_kg = M_star_msun * M_SUN_KG
    R_m  = R_half_kpc * KPC_M
    return math.sqrt(G_NEWTON * M_kg / (2.0 * R_m))


def sigma_esd_efe(M_star_msun: float, R_half_kpc: float,
                  D_gc_kpc: float) -> float:
    """sigma_los = sigma_N * sqrt(1 + R(u_eff)), u_eff with EFE."""
    g_int = g_int_at_half(M_star_msun, R_half_kpc)
    g_ext = g_ext_at_distance(D_gc_kpc)
    u_eff = 4.0 * (g_int + g_ext) / A0_SI
    boost = 1.0 + R_of_u(u_eff)
    return sigma_newton(M_star_msun, R_half_kpc) * math.sqrt(boost)


def h_blindness_sigma() -> dict:
    """sigma_ESD depends on h only through a_0 (Thm 1, C1)."""
    M, R, D = 4.0e7, 0.71, 140.0
    s1 = sigma_esd_efe(M, R, D)
    s2 = sigma_esd_efe(M, R, D)
    return {
        "sigma_ESD_ms": float(s1),
        "dsigma_dh":    float(s2 - s1),
        "h_blind":      bool(abs(s2 - s1) < 1.0e-20),
    }
