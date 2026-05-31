"""Planck 2018 CMB compressed distance prior for Study 22.

Source:
    Chen, Z., Huang, Q., & Wang, B.
    "Revisiting Cosmological Constraints on the Dark Energy Equation of State"
    JCAP 02, 028 (2019), arXiv:1902.09081
    Table 1: Planck 2018 TT,TE,EE+lowE

Three compressed parameters:
    R      = 1.7492 +/- 0.0044     CMB shift parameter
    l_A    = 301.80 +/- 0.14       acoustic scale
    Omega_b*h^2 = 0.02237 +/- 0.00015

Correlation matrix (Table 2 of Chen+2019):
    rho(R, l_A)           = -0.490
    rho(R, Omega_b*h^2)   = -0.660
    rho(l_A, Omega_b*h^2) =  0.600

The chi^2 contribution is:
    chi^2_CMB = Delta_x^T C^{-1} Delta_x
where Delta_x = x_model - x_data, x = (R, l_A, omega_b).

Model values are computed in esd_w0wa.py: cmb_shift_R, cmb_acoustic_l_A.
The Omega_b*h^2 constraint acts as a prior on the baryon density; for
the ESD PRIMARY reading it is satisfied by construction (omega_b_PRIMARY
matches Planck).
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# Measured values and uncertainties
# ---------------------------------------------------------------------------
R_PLANCK:      float = 1.7492
R_SIG:         float = 0.0044

L_A_PLANCK:    float = 301.80
L_A_SIG:       float = 0.14

OMEGA_BH2_PLANCK: float = 0.02237
OMEGA_BH2_SIG:    float = 0.00015

# Correlation matrix  rho[i,j] for x = (R, l_A, omega_b*h^2)
_RHO = np.array([
    [ 1.000, -0.490, -0.660],
    [-0.490,  1.000,  0.600],
    [-0.660,  0.600,  1.000],
])

_SIGMA = np.array([R_SIG, L_A_SIG, OMEGA_BH2_SIG])

# Covariance matrix C and its inverse
CMB_COV: np.ndarray = np.outer(_SIGMA, _SIGMA) * _RHO
CMB_CINV: np.ndarray = np.linalg.inv(CMB_COV)

X_DATA: np.ndarray = np.array([R_PLANCK, L_A_PLANCK, OMEGA_BH2_PLANCK])


def chi2_cmb(R_model: float, l_A_model: float, omega_bh2_model: float) -> float:
    """CMB chi^2 contribution for a given set of model observables."""
    dx = np.array([R_model, l_A_model, omega_bh2_model]) - X_DATA
    return float(dx @ CMB_CINV @ dx)
