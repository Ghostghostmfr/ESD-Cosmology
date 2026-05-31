"""ESD prediction for the black-hole tidal Love number k2.

At a black-hole horizon the surface gravity is enormous, so
u = 4 g / a0 is deep in the high-u regime where the locked closure
kernel R(u) -> 0 by construction. The static l=2 tidal-response
problem is therefore solved in a metric that is GR's to a fractional
precision of R(u_horizon) ~ 1e-35, so the Kerr vanishing-Love-number
theorem is inherited:

    k2_ESD(BH) = 0,   with |k2_ESD - 0| <= O(R(u_horizon)).

No free parameter enters.
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


def g_horizon(M_Msun: float) -> float:
    """Schwarzschild surface gravity kappa = c^4 / (4 G M) [m/s^2]."""
    M_kg = M_Msun * O.M_SUN_KG
    return O.C_M_S ** 4 / (4.0 * O.G_M3_KG_S2 * M_kg)


def R_at_horizon(M_Msun: float, H0: float = 67.36) -> float:
    """Closure kernel evaluated at the horizon scale of a BH."""
    return kernel(4.0 * g_horizon(M_Msun) / a_zero(H0))


def k2_BH_GR() -> float:
    """Exact GR / Kerr quadrupolar Love number (theorem)."""
    return O.K2_KERR_GR


def k2_BH_ESD(M_Msun: float, H0: float = 67.36) -> float:
    """ESD value: k2_GR multiplied by the GR-recovered metric response.
    Since k2_GR = 0 and R(u_horizon) -> 0, this is 0 exactly."""
    return k2_BH_GR() * (1.0 + R_at_horizon(M_Msun, H0))


def k2_BH_ESD_dev_bound(M_Msun: float, H0: float = 67.36) -> float:
    """Upper bound on |k2_ESD - k2_GR|: the fractional metric deviation
    R(u_horizon) bounds the induced static l=2 response."""
    return R_at_horizon(M_Msun, H0)


def Lambda_BH(k2: float, compactness: float = O.C_SCHWARZSCHILD) -> float:
    """Dimensionless tidal deformability Lambda = (2/3) k2 C^-5."""
    return (2.0 / 3.0) * k2 * compactness ** (-5.0)
