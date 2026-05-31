"""ESD prediction for ISL Yukawa alpha.

At lab scale, ambient acceleration ~ Earth surface gravity. R(u_lab)
is tiny; no scalar dilaton in the ESD metric sector (Study 19), so
the predicted Yukawa coefficient is zero (modulo R-suppressed
corrections at the kernel level which we report explicitly).
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


def R_lab(H0: float = 67.36) -> float:
    return kernel(4.0 * O.GRAV_LAB / a_zero(H0))


def alpha_ESD(lambda_um: float, H0: float = 67.36) -> float:
    """Yukawa coefficient under ESD: 0 by tensor-sector = GR.
    Wavelength dependence is none; kernel-suppression bound is R_lab.
    """
    return 0.0
