"""ESD prediction for NS tidal deformability.

Tidal coupling at NS surface (g ~ 2e12 m/s2) is deep in the high-u
regime where R(u) is negligible. ESD inherits the GR EOS-driven
Lambda identically.
"""
from __future__ import annotations
import math
from esd_core import a_zero
import observations as O

PHI    = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI = math.log(PHI)
P_EXP  = PHI
Q_EXP  = 2.0 * LN_PHI / PHI
S_NRM  = 16.0 * PHI + 1.0
B_AMP  = PHI ** 6 - 2.0
C_FLR  = (4.0 * LN_PHI - 1.0) / PHI


def kernel(u: float) -> float:
    if u <= 0.0:
        return S_NRM / C_FLR
    return S_NRM / (u ** P_EXP + B_AMP * u ** Q_EXP + C_FLR)


def g_NS_surface(M_Msun: float, R_km: float) -> float:
    R_m = R_km * 1000.0
    return O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / R_m ** 2


def R_at_NS(M_Msun: float, R_km: float, H0: float = 67.36) -> float:
    return kernel(4.0 * g_NS_surface(M_Msun, R_km) / a_zero(H0))


def Lambda_GR_APR(M_Msun: float) -> float:
    """APR-class fit Lambda(M_NS) from Annala+ 2018 / Hinderer+ 2010,
    coarse: Lambda(1.4) ~ 300, decreasing with mass."""
    return 300.0 * (1.4 / M_Msun) ** 6   # standard scaling Lambda ~ (R/M)^5 * k2


def Lambda_ESD(M_Msun: float, R_km: float, H0: float = 67.36) -> float:
    return Lambda_GR_APR(M_Msun) * (1.0 + R_at_NS(M_Msun, R_km, H0))
