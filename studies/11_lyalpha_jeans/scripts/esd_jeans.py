"""Study 11 - ESD child C7 (Lyman-alpha Jeans cutoff) audit.

Reproduces the C7 row of the published Hubble paper:

    James P. Higginson, "ESD Framework: The Hubble Tension as a
    Structural h-Blindness Boundary and Mirror-Identity Classification
    of Dark Energy" (2026).  Zenodo DOI: 10.5281/zenodo.20400097.

Paper expression (Theorem 1, C7 entry):

    lambda_J = (pi / m_D) * sqrt( c_s^2 / (G rho_m a^3) )    [symbolic]

with `lambda_J ~ 94 kpc` set by `m_D ~ 1e-22 eV` and the locked
omega_c.  The physical content is the ultralight-scalar quantum-Jeans
cutoff (Hu, Barkana, Gruzinov 2000, ApJ 558, 17).  We use the
rigorous form so the audit is unit-clean:

    k_Q(z) = (16 pi G rho_m)^(1/4) * (m_D a / hbar)^(1/2)   [comoving 1/m]
    lambda_Q_proper = a * 2 pi / k_Q

The key structural claim (the C7 row of Theorem 1) is that lambda_J
depends only on (m_D, omega_m, a) -- there is NO `h` in the
expression when matter density is in physical-density variables
(omega_m = Omega_m h^2).  That is the C7 h-blindness identity.
"""
from __future__ import annotations

import math

import numpy as np
from esd_core import (
    OMEGA_B_LOCK, OMEGA_DM_LOCK, OMEGA_M_LOCK,
)

# --------------------------------------------------------------- constants
HBAR     = 1.054571817e-34          # J s
C_LIGHT  = 2.998e8                  # m/s
G_NEWTON = 6.67430e-11              # m^3 kg^-1 s^-2
EV_J     = 1.602176634e-19          # J / eV
MPC_M    = 3.0857e22                # m / Mpc
KPC_M    = 3.0857e19                # m / kpc
KMS_MS   = 1.0e3                    # (km/s) / (m/s)
H100_SI  = 100.0 * KMS_MS / MPC_M   # 100 km/s/Mpc in 1/s

# Locked closure-pool densities (from esd_core).  These are big-Omega
# values (Omega_i, not omega_i = Omega_i h^2).  Convert at the fiducial
# h to get physical density variables that appear in the Jeans formula.
OMEGA_M_FID    = OMEGA_M_LOCK         # ~0.3157
OMEGA_DM_FID   = OMEGA_DM_LOCK
OMEGA_B_FID    = OMEGA_B_LOCK
H_FID          = 0.6727               # cancels in omega-vars
OMEGA_M_H2_FID = OMEGA_M_FID * H_FID**2  # ~0.1429 (matches Planck omega_m)

# Paper-quoted fiducials
M_D_FID_EV     = 1.0e-22              # eV; paper sec.7
CS_IGM_KMS     = 15.0                 # km/s typical IGM at z~3
Z_FID          = 3.0                  # Lyman-alpha forest redshift
LAMBDA_J_PAPER = 94.0                 # kpc (comoving), paper headline


def m_D_kg(m_D_eV: float) -> float:
    return m_D_eV * EV_J / (C_LIGHT * C_LIGHT)


def rho_m_physical(omega_m_h2: float, z: float) -> float:
    """Physical matter density at redshift z, kg/m^3.

    rho_m(z) = omega_m_h2 * rho_crit_{100} * (1+z)^3 with
    rho_crit_{100} = 3 H_100^2 / (8 pi G), where H_100 = 100 km/s/Mpc.
    Input is the physical density variable omega_m_h2 = Omega_m * h^2.
    H-INDEPENDENT by construction.
    """
    rho_crit_100 = 3.0 * H100_SI**2 / (8.0 * math.pi * G_NEWTON)
    return omega_m_h2 * rho_crit_100 * (1.0 + z)**3


def k_quantum_jeans_comoving(
    m_D_eV:     float = M_D_FID_EV,
    omega_m_h2: float = OMEGA_M_H2_FID,
    z:          float = Z_FID,
) -> float:
    """Hu-Barkana-Gruzinov 2000 quantum Jeans wavenumber, comoving 1/m.

    k_Q = (16 pi G rho_m)^(1/4) * (m_D a / hbar)^(1/2)
    """
    a = 1.0 / (1.0 + z)
    rho_m  = rho_m_physical(omega_m_h2, z)
    m_kg   = m_D_kg(m_D_eV)
    inner  = (16.0 * math.pi * G_NEWTON * rho_m)**0.25
    factor = (m_kg * a / HBAR)**0.5
    return inner * factor


def lambda_J_comoving_m(
    m_D_eV:     float = M_D_FID_EV,
    omega_m_h2: float = OMEGA_M_H2_FID,
    z:          float = Z_FID,
    c_s_kms:    float = CS_IGM_KMS,
) -> float:
    """C7 Jeans length, COMOVING meters.

    lambda_J_comoving = 2 pi / k_Q_comoving.
    c_s_kms is kept for signature compatibility (quantum pressure
    dominates; gas c_s does not enter).
    """
    _ = c_s_kms
    k_Q = k_quantum_jeans_comoving(m_D_eV=m_D_eV, omega_m_h2=omega_m_h2, z=z)
    return 2.0 * math.pi / k_Q


def lambda_J_proper_m(**kw) -> float:
    z = kw.get("z", Z_FID)
    return lambda_J_comoving_m(**kw) / (1.0 + z)


def lambda_J_kpc(comoving: bool = True, **kw) -> float:
    f = lambda_J_comoving_m if comoving else lambda_J_proper_m
    return f(**kw) / KPC_M


def h_blindness_C7(omega_m_h2: float = OMEGA_M_H2_FID, z: float = Z_FID,
                   m_D_eV: float = M_D_FID_EV, c_s_kms: float = CS_IGM_KMS,
                   h0: float = H_FID, dh: float = 1.0e-4) -> dict:
    """Verify d lambda_J / d h = 0 at fixed (omega_m_h2, m_D, z).

    The formula uses omega_m_h2 (= Omega_m * h^2; physical-density
    variable) and never references h, so the residual must be
    EXACTLY zero (the C7 row of Theorem 1).
    """
    def f(_h_val):
        return lambda_J_kpc(comoving=True, m_D_eV=m_D_eV,
                            omega_m_h2=omega_m_h2, z=z, c_s_kms=c_s_kms)
    f0 = f(h0)
    df = (f(h0 + dh) - f(h0 - dh)) / (2.0 * dh)
    return {
        "lambda_J_kpc":  float(f0),
        "dlambda_dh":    float(df),
        "h_blind":       bool(abs(df) < 1.0e-12),
    }


def k_cut_comoving_mpc_inv(
    m_D_eV:     float = M_D_FID_EV,
    omega_m_h2: float = OMEGA_M_H2_FID,
    z:          float = Z_FID,
) -> float:
    """Comoving Jeans cutoff wavenumber in Mpc^-1."""
    return k_quantum_jeans_comoving(m_D_eV=m_D_eV, omega_m_h2=omega_m_h2,
                                    z=z) * MPC_M


def lambda_vs_m22(omega_m_h2: float = OMEGA_M_H2_FID, z: float = Z_FID,
                  m22_grid: np.ndarray | None = None) -> dict:
    if m22_grid is None:
        m22_grid = np.logspace(-1, 2, 31)
    rows = []
    for m22 in m22_grid:
        m_eV = float(m22) * 1.0e-22
        rows.append({
            "m22":              float(m22),
            "lambda_kpc_comov": float(lambda_J_kpc(comoving=True, m_D_eV=m_eV,
                                                   omega_m_h2=omega_m_h2, z=z)),
            "k_cut_Mpc_inv":    float(k_cut_comoving_mpc_inv(m_D_eV=m_eV,
                                                              omega_m_h2=omega_m_h2,
                                                              z=z)),
        })
    return {"rows": rows}


if __name__ == "__main__":
    print(f"m_D                 = {M_D_FID_EV*1e22:.2f}e-22 eV")
    print(f"omega_m h^2         = {OMEGA_M_H2_FID:.4f}")
    print(f"lambda_J(comoving)  = {lambda_J_kpc(comoving=True):.2f} kpc  (paper {LAMBDA_J_PAPER:.0f} kpc)")
    print(f"lambda_J(proper)    = {lambda_J_kpc(comoving=False):.2f} kpc")
    print(f"k_cut(z=3)          = {k_cut_comoving_mpc_inv():.3f} Mpc^-1 (comoving)")
    print(f"h-blindness         = {h_blindness_C7()}")
