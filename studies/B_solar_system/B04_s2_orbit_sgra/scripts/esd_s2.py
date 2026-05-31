"""ESD S2 predictor: kernel suppression at galactic-center scales."""
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


def R_at_g(g: float, H0: float = 67.36) -> float:
    return kernel(g / a_zero(H0))


def f_SP_pred(H0: float = 67.36) -> float:
    """ESD prediction for the GRAVITY f_SP modifier.

    With R(u) << 1 across the S2 orbit, the orbit reduces to pure GR,
    hence f_SP = 1 + R(u_peri) ~ 1 to machine precision.
    """
    return 1.0 + R_at_g(O.G_PERI, H0)


def n_sigma_fSP(H0: float = 67.36) -> float:
    return abs(f_SP_pred(H0) - O.F_SP_MEAS) / O.F_SP_ERR
