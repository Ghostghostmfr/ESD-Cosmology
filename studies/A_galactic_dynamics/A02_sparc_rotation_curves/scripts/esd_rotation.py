"""ESD framework's locked predictions for the SPARC rotation-curve study.

Public API:
  PHI, P_EXP, Q_EXP, S_PHI, B_PHI, C_PHI - golden-ratio closure constants.
  A0_SI               - MOND-scale acceleration (literal paper value, no fit).
  KPC_TO_M            - 1 kpc in metres.
  R_esd(u), g_esd(g_N), g_esd_vec(g_N_arr) - ESD anomalous + total acceleration.
  g_mond(g_N), g_mond_vec(g_N_arr) - MOND simple-interpolation reference.
  compute_vbar(vg, vd, vb, Ud, Ub) - signed-square baryonic velocity.
  compute_gN(r_kpc, vbar_kms)      - Newtonian acceleration at radius r.
  vel_from_g(r_kpc, g_total)       - inverse: v(r) = sqrt(g*r).
  chi2(v_pred, v_obs, err_v)       - chi^2 statistic (mask err<=0).

Constants are locked by the golden ratio (Higginson 2026, paper 1):

    phi = (1 + sqrt(5)) / 2
    p   = phi
    q   = 2 ln(phi) / phi
    s   = 16 phi + 1
    b   = phi^6 - 2
    c   = (4 ln(phi) - 1) / phi

The ESD prediction at each radius is

    g_total(r) = g_N(r) * (1 + R(u)),   u = 4 g_N / a_0,
    R(u)       = s / (u^p + b u^q + c),

with baryonic velocity

    V_bar(r) = sqrt( |V_gas| V_gas
                   + Upsilon_disk  |V_disk| V_disk
                   + Upsilon_bulge |V_bul|  V_bul )

and Newtonian source g_N(r) = V_bar^2 / r.  The predicted circular
velocity is v(r) = sqrt(g_total(r) * r).
"""

from __future__ import annotations

import math

import numpy as np

# Golden-ratio closure constants (locked, identical to paper 1).
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI: float = math.log(PHI)
P_EXP: float = PHI
Q_EXP: float = 2.0 * LN_PHI / PHI
S_PHI: float = 16.0 * PHI + 1.0
B_PHI: float = PHI**6 - 2.0
C_PHI: float = (4.0 * LN_PHI - 1.0) / PHI

# Numerical MOND-scale acceleration used in paper 1's SPARC section.
# The framework-derived value from esd_core.cosmology.a_zero(67.36) is
# 1.2015e-10 m/s^2 (0.13% larger).  We use the paper's literal value
# here so the head-to-head numerical comparison reproduces bit-for-bit.
A0_SI: float = 1.2e-10

KPC_TO_M: float = 3.085677581491367e19  # 1 kpc in metres

# Population-synthesis mass-to-light defaults (Schombert 2014; same as
# paper 1's "fixed M/L" baseline).
UPSILON_DISK_FIXED: float = 0.5
UPSILON_BULGE_FIXED: float = 0.7

# Grid for the per-galaxy M/L sweep used in paper 1's main analysis.
UPS_D_GRID: tuple[float, ...] = (
    0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5,
)
UPS_B_GRID: tuple[float, ...] = (
    0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
)


# ----------------------------------------------------------------------- ESD

def _sigma(u: float | np.ndarray) -> float | np.ndarray:
    return u**P_EXP + B_PHI * u**Q_EXP + C_PHI


def R_esd(u: float) -> float:
    return S_PHI / _sigma(u)


def g_esd(g_n: float) -> float:
    if g_n <= 0:
        return 0.0
    u = 4.0 * g_n / A0_SI
    return g_n * (1.0 + R_esd(u))


def g_esd_vec(g_n_arr: np.ndarray) -> np.ndarray:
    out = np.zeros_like(g_n_arr)
    mask = g_n_arr > 0
    gn = g_n_arr[mask]
    u = 4.0 * gn / A0_SI
    out[mask] = gn * (1.0 + S_PHI / (u**P_EXP + B_PHI * u**Q_EXP + C_PHI))
    return out


# ----------------------------------------------------------------------- MOND

def g_mond(g_n: float) -> float:
    """MOND simple-interpolation reference: g = g_N / (1 - exp(-sqrt(g_N/a0)))."""
    if g_n <= 0:
        return 0.0
    x = math.sqrt(g_n / A0_SI)
    return g_n / (1.0 - math.exp(-x))


def g_mond_vec(g_n_arr: np.ndarray) -> np.ndarray:
    out = np.zeros_like(g_n_arr)
    mask = g_n_arr > 0
    gn = g_n_arr[mask]
    x = np.sqrt(gn / A0_SI)
    out[mask] = gn / (1.0 - np.exp(-x))
    return out


# -------------------------------------------------------- rotation-curve glue

def _signed_sq(v: np.ndarray) -> np.ndarray:
    return np.sign(v) * v**2


def compute_vbar(v_gas: np.ndarray,
                 v_disk: np.ndarray,
                 v_bul: np.ndarray,
                 upsilon_disk: float,
                 upsilon_bulge: float) -> np.ndarray:
    total = (_signed_sq(v_gas)
             + upsilon_disk * _signed_sq(v_disk)
             + upsilon_bulge * _signed_sq(v_bul))
    return np.sqrt(np.maximum(total, 0.0))


def compute_gN(r_kpc: np.ndarray, vbar_kms: np.ndarray) -> np.ndarray:
    return (vbar_kms * 1.0e3)**2 / (r_kpc * KPC_TO_M)


def vel_from_g(r_kpc: np.ndarray, g_total: np.ndarray) -> np.ndarray:
    return np.sqrt(np.maximum(g_total * r_kpc * KPC_TO_M, 0.0)) / 1.0e3


def chi2(v_pred: np.ndarray, v_obs: np.ndarray, err_v: np.ndarray) -> float:
    mask = err_v > 0
    return float(np.sum(((v_pred[mask] - v_obs[mask]) / err_v[mask])**2))
