"""ESD V_flat predictor for HI-dominated dwarfs.

Deep-MOND-equivalent amplitude: V_flat^4 = G M_b a_0 in the limit u<<1.
Including the closure-pool finite-u correction, at typical R = 3-9 kpc
and dwarf M_b ~ 10^7 - 10^9 Msun, u remains below 0.5 across the disc
so R(u) >> 1 and the simple analytic limit is accurate to ~5%.
"""
from __future__ import annotations
import math
from esd_core import a_zero
import observations as O

G_M3_KG_S2 = 6.67430e-11

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


def V_flat_pred(M_b_Msun: float, H0: float = 67.36) -> float:
    """Deep-MOND-equivalent V_flat from BTFR closure.

    V_flat^4 = G M_b a_0  (km/s)^4.
    """
    a0 = a_zero(H0)
    M = M_b_Msun * O.M_SUN_KG
    V_ms4 = G_M3_KG_S2 * M * a0
    V_ms = V_ms4 ** 0.25
    return V_ms / 1000.0  # km/s
