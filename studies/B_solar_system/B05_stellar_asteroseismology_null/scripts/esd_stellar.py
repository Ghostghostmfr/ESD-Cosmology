"""ESD stellar NULL predictor."""
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


def delta_nu_pred(H0: float = 67.36) -> float:
    """Solar Delta_nu under ESD: standard value modulated by R(u) <<1."""
    R = R_at_g(O.G_STELLAR_INTERIOR, H0)
    return O.DELTA_NU_SUN_MESA_UHZ * (1.0 + R)


def sirius_b_vgr_pred(H0: float = 67.36) -> float:
    """Sirius B gravitational redshift under ESD.

    ESD reduces to GR in the WD-surface regime (R(u) << 1), so the
    framework adopts the published GR null-geodesic value directly
    rather than the simple GM/(Rc) approximation.
    """
    M = O.SIRIUS_B_M_MSUN * O.M_SUN_KG
    R_m = O.SIRIUS_B_R_RSUN * O.R_SUN_M
    g_surface = O.G_M3_KG_S2 * M / R_m ** 2
    R_u = R_at_g(g_surface, H0)
    return O.SIRIUS_B_VGR_GR_KMS * (1.0 + R_u)
