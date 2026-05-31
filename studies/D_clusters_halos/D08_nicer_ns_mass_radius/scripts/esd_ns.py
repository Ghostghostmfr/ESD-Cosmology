"""ESD NS predictor.

ESD reduces to GR at NS-surface accelerations. We use an APR-surrogate
M-R relation (smooth single-mode polytrope tuned to canonical values):
    R(M) ~ R0 - alpha * (M/Msun - 1.4)^2
with R0 = 12.5 km, alpha = 2.4 km/Msun^2, valid for 1.0 <= M <= 2.3 Msun.

The point is consistency, not EoS fitting; any EoS in the modern band
gives the same verdict because ESD does not modify it.
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


def R_at_surface(M_Msun: float, R_km: float, H0: float = 67.36) -> float:
    R_m = R_km * 1e3
    g = O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / R_m ** 2
    return kernel(g / a_zero(H0))


def R_pred_km(M_Msun: float) -> float:
    R0 = 12.5
    alpha = 2.4
    return R0 - alpha * (M_Msun - 1.4) ** 2
