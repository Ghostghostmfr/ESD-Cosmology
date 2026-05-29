"""ESD-framework H_0 closures used in Study 08.

All numbers are derived in closed form from `esd_core` plus the
McGaugh+2016 RAR anchor a_0. Three core operations:

  1. bridge_inversion_H0(a_0)          -- C1 of the published hubble paper
  2. identity_C_residual()             -- Eq. (C), parameter-free
  3. h_blindness_jacobian()            -- Theorem 1 of the published paper
"""

from __future__ import annotations

import math

import numpy as np

import esd_core as ESD

C_LIGHT_M_S: float = 299_792_458.0
MPC_M:        float = 3.0856775814913673e22

# Planck-anchored reference point used by the published paper.
H0_PLANCK_REF: float = 67.36
OMEGA_M_PLANCK: float = 0.3158
OMEGA_B_PLANCK: float = 0.04930
OMEGA_DM_PLANCK: float = OMEGA_M_PLANCK - OMEGA_B_PLANCK

A0_MCGAUGH_2016: float = 1.20e-10           # m s^-2 (RAR anchor)


# -------------------------------------------------------------------------
#  C1: bridge inversion -- predict H_0 from a_0
# -------------------------------------------------------------------------
def bridge_inversion_H0(
    a0: float = A0_MCGAUGH_2016,
    omega_dm: float = ESD.OMEGA_DM_LOCK,
    omega_b: float = ESD.OMEGA_B_LOCK,
) -> float:
    """Solve a_0 = c H_0 sqrt((3 Omega_DM + Omega_b)/(8 pi)) for H_0.

    Returns H_0 in km/s/Mpc. With the McGaugh+2016 a_0 = 1.20e-10 and
    the Planck-anchored (Omega_DM, Omega_b), this reproduces the
    published value 67.28 km/s/Mpc from SPARC alone (paper Sec. 1).
    """
    rad = math.sqrt((3.0 * omega_dm + omega_b) / (8.0 * math.pi))
    H0_si = a0 / (C_LIGHT_M_S * rad)            # 1/s
    return H0_si * MPC_M / 1000.0               # km/s/Mpc


# -------------------------------------------------------------------------
#  Identity (C):  3 Omega_DM + Omega_b = (18/pi) Omega_Lambda^2 Omega_m
# -------------------------------------------------------------------------
def identity_C_lhs(omega_dm: float, omega_b: float) -> float:
    return 3.0 * omega_dm + omega_b


def identity_C_rhs(omega_Lambda: float, omega_m: float) -> float:
    return (18.0 / math.pi) * omega_Lambda * omega_Lambda * omega_m


def identity_C_residual(
    omega_dm: float = ESD.OMEGA_DM_LOCK,
    omega_b: float = ESD.OMEGA_B_LOCK,
    omega_Lambda: float = ESD.OMEGA_LAMBDA_LOCK,
    omega_m: float = ESD.OMEGA_M_LOCK,
) -> dict:
    lhs = identity_C_lhs(omega_dm, omega_b)
    rhs = identity_C_rhs(omega_Lambda, omega_m)
    return {
        "lhs": lhs, "rhs": rhs,
        "abs_diff":  lhs - rhs,
        "rel_diff":  (lhs - rhs) / lhs,
    }


# -------------------------------------------------------------------------
#  Theorem 1: h-blindness of ESD-distinctive children
# -------------------------------------------------------------------------
def child_C1(theta: np.ndarray) -> float:
    """C1 = a_0 from the bridge, expressed in terms of (h, omega_b, omega_c)."""
    h, omega_b, omega_c = theta
    H0_si = h * 100_000.0 / MPC_M
    # Use density variables: Omega_i = omega_i / h^2
    Om_DM = omega_c / (h * h)
    Om_b  = omega_b / (h * h)
    return C_LIGHT_M_S * H0_si * math.sqrt((3*Om_DM + Om_b) / (8*math.pi))


def child_C4(theta: np.ndarray) -> float:
    """C4 = cluster total/baryon ratio - 1 = R(u_cl) + Omega_DM/Omega_b.

    R(u_cl) is the screening response at a cluster characteristic u; here
    we treat it as a fixed constant (not h-dependent) for the Jacobian
    test. The point of Theorem 1 is the omega_c/omega_b part.
    """
    h, omega_b, omega_c = theta
    R_u_cl = 0.0    # screening response is u-only, h-independent
    return R_u_cl + omega_c / omega_b


def child_C7(theta: np.ndarray) -> float:
    """C7 = Lyman-alpha Jeans cutoff lambda_J, set by m_D and omega_c.

    For the Jacobian we use the published proportionality
        lambda_J ~ (1/m_D) * sqrt(c_s^2 / (G rho_m a^3))
    expressed in omega_c. m_D and c_s are framework-fixed (not h).
    """
    h, omega_b, omega_c = theta
    # lambda_J ~ 1 / sqrt(rho_m) ~ 1 / sqrt(omega_c)
    return 1.0 / math.sqrt(omega_c)


def child_C2(theta: np.ndarray) -> float:
    """C2 = CMB acoustic angle theta_*  (NOT an ESD-distinctive child --
    included to show its h-column is non-zero, so the full J has rank 3
    over (C1,C2,C4,C7) but the ESD-distinctive subset has rank 2)."""
    h, omega_b, omega_c = theta
    # theta_* ~ r_s / D_A; both scale with h in a non-cancelling way.
    # Sketch: theta_* ~ omega_b^0.13 * omega_m^0.25 * h  (Hu & Sugiyama-ish)
    omega_m = omega_b + omega_c
    return h * omega_m ** 0.25 * omega_b ** 0.13


def numerical_jacobian(
    children=(child_C1, child_C2, child_C4, child_C7),
    theta0=(0.6736, 0.02237, 0.1200),
    eps: float = 1e-5,
) -> np.ndarray:
    """Centered-difference Jacobian d C_i / d theta_j at theta0,
    normalized by C_i(theta0). Returns shape (n_children, 3).
    """
    theta0 = np.array(theta0, dtype=float)
    J = np.zeros((len(children), 3))
    for i, ch in enumerate(children):
        f0 = ch(theta0)
        for j in range(3):
            tp = theta0.copy(); tp[j] += eps
            tm = theta0.copy(); tm[j] -= eps
            J[i, j] = (ch(tp) - ch(tm)) / (2 * eps * f0)
    return J


def h_blindness_check(
    children_distinctive=(child_C1, child_C4, child_C7),
    theta0=(0.6736, 0.02237, 0.1200),
    eps: float = 1e-5,
) -> dict:
    """Compute |partial R_i / partial h| / |R_i| for each distinctive child.

    Theorem 1 (paper) requires this to be < 1e-9 for every i. The
    cluster-ratio C4 evaluation uses R(u_cl)=0 as a placeholder; the
    paper's formal proof is in Sec. 'h-blindness theorem'.
    """
    J = numerical_jacobian(children_distinctive, theta0, eps)
    return {
        "theta0": list(theta0),
        "children": [ch.__name__ for ch in children_distinctive],
        "dR_dh_relative": [float(J[i, 0]) for i in range(len(children_distinctive))],
        "max_abs_dR_dh":  float(np.max(np.abs(J[:, 0]))),
        "rank_estimate":  int(np.linalg.matrix_rank(J, tol=1e-8)),
    }


# -------------------------------------------------------------------------
#  Calibration-bias inversion: SH0ES Delta-mu_host that would absorb the
#  H_0 offset, per paper Sec. 'Astrophysical Distance Ladder Calibration'.
# -------------------------------------------------------------------------
def shoes_calibration_bias_mag(
    H0_predict: float = 67.28,
    H0_shoes: float = 73.04,
) -> float:
    """Delta mu_host = (5/ln 10) * Delta H_0 / H_0 ."""
    return (5.0 / math.log(10.0)) * (H0_shoes - H0_predict) / H0_predict
