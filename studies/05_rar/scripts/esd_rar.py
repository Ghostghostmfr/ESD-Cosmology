"""ESD framework's locked predictions for the Radial Acceleration Relation.

Same locked constants as study 03 (golden-ratio closure of paper 1).

Public API:
    PHI, P_EXP, Q_EXP, S_PHI, B_PHI, C_PHI - golden-ratio closure constants.
    A0_SI               - MOND-scale acceleration (literal paper value).
    KPC_TO_M            - 1 kpc in metres.
    UPSILON_DISK_FIXED, UPSILON_BULGE_FIXED - fixed-M/L baseline.
    R_esd(u), g_esd_vec(g_bar) - ESD anomalous + total acceleration.
    g_mond_vec(g_bar)          - MOND simple-interpolation reference.
    compute_vbar(...)          - signed-square baryonic velocity (kpc, km/s).
    compute_g(...)             - V^2 / r in m/s^2.

The RAR observable is the joint (g_bar, g_obs) distribution across all
SPARC data points and the running median + 16/84 band of the residual
log10(g_obs / g_model).  This module exposes only the model-side
mapping; binning is in run_rar.py.
"""

from __future__ import annotations

import math

import numpy as np

# Golden-ratio closure constants (locked).
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI: float = math.log(PHI)
P_EXP: float = PHI
Q_EXP: float = 2.0 * LN_PHI / PHI
S_PHI: float = 16.0 * PHI + 1.0
B_PHI: float = PHI**6 - 2.0
C_PHI: float = (4.0 * LN_PHI - 1.0) / PHI

# Paper 1 literal value of a_0 (so the comparison matches bit-for-bit).
A0_SI: float = 1.2e-10
KPC_TO_M: float = 3.085677581491367e19

# Population-synthesis mass-to-light defaults (paper 1 fixed-M/L baseline).
UPSILON_DISK_FIXED: float = 0.5
UPSILON_BULGE_FIXED: float = 0.7


def R_esd(u: np.ndarray | float) -> np.ndarray | float:
    return S_PHI / (u**P_EXP + B_PHI * u**Q_EXP + C_PHI)


def g_esd_vec(g_bar: np.ndarray) -> np.ndarray:
    out = np.zeros_like(g_bar, dtype=float)
    mask = g_bar > 0
    gb = g_bar[mask]
    u = 4.0 * gb / A0_SI
    out[mask] = gb * (1.0 + S_PHI / (u**P_EXP + B_PHI * u**Q_EXP + C_PHI))
    return out


def g_mond_vec(g_bar: np.ndarray) -> np.ndarray:
    out = np.zeros_like(g_bar, dtype=float)
    mask = g_bar > 0
    gb = g_bar[mask]
    x = np.sqrt(gb / A0_SI)
    out[mask] = gb / (1.0 - np.exp(-x))
    return out


def _signed_sq(v: np.ndarray) -> np.ndarray:
    return np.sign(v) * v**2


def compute_vbar(v_gas: np.ndarray, v_disk: np.ndarray, v_bul: np.ndarray,
                 upsilon_disk: float, upsilon_bulge: float) -> np.ndarray:
    total = (_signed_sq(v_gas)
             + upsilon_disk * _signed_sq(v_disk)
             + upsilon_bulge * _signed_sq(v_bul))
    return np.sqrt(np.maximum(total, 0.0))


def compute_g(r_kpc: np.ndarray, v_kms: np.ndarray) -> np.ndarray:
    """V^2 / r in SI m/s^2 (r in kpc, V in km/s)."""
    return (v_kms * 1.0e3)**2 / (r_kpc * KPC_TO_M)
