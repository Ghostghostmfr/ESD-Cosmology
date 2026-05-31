"""ESD prediction for black-hole ringdown echoes.

The GW-sector applicability theorem (Study C02) makes the ESD tensor
sector reduce identically to GR, and at the photon sphere /
near-horizon region u = 4 g / a0 is deep in the high-u regime where
the locked closure kernel R(u) -> 0. ESD therefore inherits the
classical, perfectly *absorbing* GR horizon: there is no reflective
inner boundary, so the inner-boundary reflectivity and the echo
amplitude both vanish,

    R_wall^ESD = 0,   A_echo^ESD = 0,

with |R_wall^ESD - 0| <= O(R(u_horizon)). No free parameter enters.

For completeness the module also computes the echo time delay that a
reflective surface *would* produce, so the prediction "no echo at this
cadence" is explicit and falsifiable.
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
    """Geometrized mass GM/c^3 [s]."""
    return O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / O.C_M_S ** 3


def g_horizon(M_Msun: float) -> float:
    """Schwarzschild surface gravity kappa = c^4 / (4 G M) [m/s^2]."""
    M_kg = M_Msun * O.M_SUN_KG
    return O.C_M_S ** 4 / (4.0 * O.G_M3_KG_S2 * M_kg)


def R_at_horizon(M_Msun: float, H0: float = 67.36) -> float:
    return kernel(4.0 * g_horizon(M_Msun) / a_zero(H0))


def wall_reflectivity_ESD(M_Msun: float, H0: float = 67.36) -> float:
    """ESD inner-boundary reflectivity: 0 (classical absorbing horizon)."""
    return O.WALL_REFLECTIVITY_GR * (1.0 + R_at_horizon(M_Msun, H0))


def echo_amplitude_ESD(M_Msun: float, H0: float = 67.36) -> float:
    """ESD echo amplitude relative to the main ringdown: 0."""
    return O.ECHO_AMPLITUDE_GR * (1.0 + R_at_horizon(M_Msun, H0))


def wall_reflectivity_dev_bound(M_Msun: float, H0: float = 67.36) -> float:
    """Upper bound on |R_wall^ESD - 0|, set by the fractional metric
    deviation R(u_horizon)."""
    return R_at_horizon(M_Msun, H0)


def echo_delay_if_reflective(M_Msun: float, epsilon: float) -> float:
    """Echo time delay [s] a reflective surface at proper distance
    epsilon from the horizon WOULD produce: Delta t ~ 2 (GM/c^3)|ln eps|.
    ESD predicts NO such echo (reflectivity 0); this is the cadence at
    which a future detection would falsify the prediction."""
    return 2.0 * M_sec(M_Msun) * abs(math.log(epsilon))
