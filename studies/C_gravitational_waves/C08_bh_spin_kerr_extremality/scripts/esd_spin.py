"""ESD prediction for BH spin / Kerr ISCO.

Kerr ISCO radius (Bardeen-Press-Teukolsky 1972):
    Z1 = 1 + (1-chi^2)^(1/3) * ((1+chi)^(1/3) + (1-chi)^(1/3))
    Z2 = sqrt(3*chi^2 + Z1^2)
    r_ISCO/M = 3 + Z2 - sgn(chi)*sqrt((3-Z1)*(3+Z1+2Z2))     (prograde: -)
ISCO frequency: f_ISCO = (1/(2 pi M)) / (chi + (r_ISCO/M)^(3/2))  (geometrized)
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


def M_sec(M_Msun: float) -> float:
    return O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / O.C_M_S ** 3


def r_ISCO_over_M(chi: float) -> float:
    """Prograde ISCO. chi in [0, 0.998]."""
    z1 = 1.0 + (1.0 - chi ** 2) ** (1.0/3.0) * (
        (1.0 + chi) ** (1.0/3.0) + (1.0 - chi) ** (1.0/3.0))
    z2 = math.sqrt(3.0 * chi ** 2 + z1 ** 2)
    return 3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def g_ISCO(M_Msun: float, chi: float) -> float:
    r_m = r_ISCO_over_M(chi) * O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / O.C_M_S ** 2
    return O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / r_m ** 2


def R_at_ISCO(M_Msun: float, chi: float, H0: float = 67.36) -> float:
    return kernel(4.0 * g_ISCO(M_Msun, chi) / a_zero(H0))


def chi_max_pred() -> float:
    """ESD inherits Thorne 1974 bound identically."""
    return O.THORNE_MAX
