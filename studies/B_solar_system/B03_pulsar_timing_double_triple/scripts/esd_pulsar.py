"""ESD strong-field pulsar predictor.

Closure-pool kernel suppression in the u>>1 limit and a GR-recovery
check on J0737's periastron advance. Both predictions are h-blind.
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


def u_of_g(g_ms2: float, H0: float = 67.36) -> float:
    return g_ms2 / a_zero(H0)


def R_at(g_ms2: float, H0: float = 67.36) -> float:
    return kernel(u_of_g(g_ms2, H0))


def predict_orbital_R(H0: float = 67.36) -> float:
    return R_at(O.G_ORBITAL_PSR, H0)


def predict_surface_R(H0: float = 67.36) -> float:
    return R_at(O.G_NS_SURFACE, H0)


def gr_omdot_recovery_frac() -> float:
    """|omdot_pred - omdot_meas| / omdot_meas at GR-recovery level."""
    pred = O.post_keplerian_GR()["omdot_deg_yr"]
    meas = O.J0737["omdot_deg_yr"]
    return abs(pred - meas) / meas


def h_blindness() -> float:
    a = predict_orbital_R(60.0); b = predict_orbital_R(80.0)
    return abs(a - b)
