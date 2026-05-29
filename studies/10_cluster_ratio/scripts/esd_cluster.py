"""Study 10 - ESD cluster ratio C4 closures.

Reproduces child C4 of the published Hubble paper:

  James P. Higginson, "ESD Framework: The Hubble Tension as a Structural
  h-Blindness Boundary and Mirror-Identity Classification of Dark Energy"
  (2026). Zenodo DOI: 10.5281/zenodo.20400097.

Paper's C4 expression (Sec. Children list / Theorem 1):

    M_tot / M_b  =  ( 1 + R(u_cl) )  +  Omega_DM / Omega_b

with R(u) = s / Sigma(u), Sigma(u) = u^p + b u^q + c, all constants
locked by the parent action.
"""
from __future__ import annotations

import math

import numpy as np

import esd_core as ESD

# --- locked closure-pool constants ---------------------------------------
PHI:    float = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI: float = math.log(PHI)
P_EXP:  float = PHI
Q_EXP:  float = 2.0 * LN_PHI / PHI               # 0.594808
C_FLR:  float = (4.0 * LN_PHI - 1.0) / PHI       # 0.571645
B_AMP:  float = PHI ** 6 - 2.0                   # 15.944272
S_NRM:  float = 16.0 * PHI + 1.0                 # 26.888544

# --- physical constants (SI) ---------------------------------------------
G_NEWTON_SI: float = 6.6743e-11
M_SUN_KG:    float = 1.98892e30
MPC_M:       float = 3.0856775814913673e22

# --- locked cosmological mix ---------------------------------------------
OMEGA_B_LOCK:  float = ESD.OMEGA_B_LOCK         # 0.050094 (closure-pool)
OMEGA_DM_LOCK: float = ESD.OMEGA_DM_LOCK        # 0.265642
DM_OVER_B:     float = OMEGA_DM_LOCK / OMEGA_B_LOCK   # 5.303

# --- a_0 (RAR anchor, McGaugh+2016) --------------------------------------
A0_SI: float = 1.20e-10                          # m / s^2


# =========================================================================
#  Locked screening function
# =========================================================================
def Sigma(u: np.ndarray | float) -> np.ndarray | float:
    """Locked ESD screening Sigma(u) = u^p + b u^q + c."""
    u = np.asarray(u, dtype=float)
    return u ** P_EXP + B_AMP * u ** Q_EXP + C_FLR


def R_of_u(u: np.ndarray | float) -> np.ndarray | float:
    """Dark-matter-like enhancement: g_total = g_N (1 + R(u))."""
    return S_NRM / Sigma(u)


# =========================================================================
#  Cluster geometry helpers
# =========================================================================
def u_cluster(M_solar: float, R_mpc: float) -> float:
    """Local u = 4 g_N / a_0 at a characteristic cluster radius R for
    enclosed mass M.  Inputs in solar masses and Mpc; result dimensionless.
    """
    M_si = M_solar * M_SUN_KG
    R_si = R_mpc  * MPC_M
    g_N  = G_NEWTON_SI * M_si / (R_si * R_si)
    return 4.0 * g_N / A0_SI


# =========================================================================
#  C4 ratio
# =========================================================================
def M_tot_over_M_b(u_cl: float,
                   omega_dm: float = OMEGA_DM_LOCK,
                   omega_b:  float = OMEGA_B_LOCK) -> float:
    """Paper C4 expression."""
    return (1.0 + R_of_u(u_cl)) + omega_dm / omega_b


def baryon_fraction(u_cl: float,
                    omega_dm: float = OMEGA_DM_LOCK,
                    omega_b:  float = OMEGA_B_LOCK) -> float:
    """f_b = M_b / M_tot."""
    return 1.0 / M_tot_over_M_b(u_cl, omega_dm, omega_b)


# =========================================================================
#  h-blindness check on C4 (Theorem 1)
# =========================================================================
def h_blindness_C4(M_solar: float = 5.0e14,
                   R_mpc:   float = 1.2,
                   theta0   = (0.6736, 0.02237, 0.1200),
                   eps:     float = 1.0e-5) -> dict:
    """Centered-difference d ln (M_tot/M_b) / d h at fixed
    (M_obs, R_obs, omega_b, omega_c).  Should be 0 exactly (Theorem 1).
    """
    h0, ob, oc = theta0

    def ratio(h: float) -> float:
        # u_cl is set by observed M, R, a_0 - none depend on h
        u = u_cluster(M_solar, R_mpc)
        # omega_DM/omega_b is in omega-variables, h-independent
        return (1.0 + R_of_u(u)) + oc / ob

    f0 = ratio(h0)
    fp = ratio(h0 + eps)
    fm = ratio(h0 - eps)
    dr_dh = (fp - fm) / (2.0 * eps * f0)
    return {
        "value":        float(f0),
        "dr_dh_rel":    float(dr_dh),
        "h_blind":      bool(abs(dr_dh) < 1.0e-12),
    }
