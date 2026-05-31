"""ESD predictor for Einstein-radius function (SIS aperture-mass).

theta_E [rad] = 4 pi (sigma_SIS / c)^2 (D_ls / D_s)

with sigma_SIS^2 = G M_ap / (2 R_E), M_ap = M_star (1 + R(u_eff)),
and u_eff = 4 G M_star / (a_0 R_E^2).

Cosmological distances use flat LCDM with esd_core's locked Omega_m
and H0 = 67.36 km/s/Mpc.
"""
from __future__ import annotations

import math

from esd_core import a_zero, OMEGA_M_LOCK

G_NEWTON: float = 6.67430e-11
M_SUN_KG: float = 1.98892e30
KPC_M:    float = 3.0856775814913673e19
MPC_M:    float = 3.0856775814913673e22
KM_M:     float = 1.0e3
C_LIGHT:  float = 2.99792458e8

H0_PLANCK_KMS: float = 67.36
H0_SI:         float = H0_PLANCK_KMS * KM_M / MPC_M
A0_SI: float = a_zero(H0_PLANCK_KMS)

OMEGA_M: float = OMEGA_M_LOCK
OMEGA_L: float = 1.0 - OMEGA_M

PHI:    float = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI: float = math.log(PHI)
P_EXP:  float = PHI
Q_EXP:  float = 2.0 * LN_PHI / PHI
S_NRM:  float = 16.0 * PHI + 1.0
B_AMP:  float = PHI ** 6 - 2.0
C_FLR:  float = (4.0 * LN_PHI - 1.0) / PHI

ARCSEC_PER_RAD: float = 206264.80624709636


def R_of_u(u: float) -> float:
    if u <= 0.0:
        return S_NRM / C_FLR
    return S_NRM / (u ** P_EXP + B_AMP * u ** Q_EXP + C_FLR)


# --- LCDM cosmological distances -----------------------------------------

def _E_inv(z: float) -> float:
    """1 / H(z) in units of 1/H0; integrand for comoving distance."""
    return 1.0 / math.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L)


def _comoving_distance_m(z: float, n: int = 4096) -> float:
    """Flat-LCDM comoving distance in meters."""
    if z <= 0.0:
        return 0.0
    h = z / n
    s = 0.5 * (_E_inv(0.0) + _E_inv(z))
    for k in range(1, n):
        s += _E_inv(k * h)
    chi = h * s * (C_LIGHT / H0_SI)
    return chi


def angular_diameter_distance_m(z: float) -> float:
    return _comoving_distance_m(z) / (1.0 + z)


def D_ls_over_D_s(z_lens: float, z_source: float) -> float:
    """Ratio (D_ls / D_s) for flat LCDM."""
    chi_l = _comoving_distance_m(z_lens)
    chi_s = _comoving_distance_m(z_source)
    D_s   = chi_s / (1.0 + z_source)
    D_ls  = (chi_s - chi_l) / (1.0 + z_source)
    return D_ls / D_s


# --- ESD lensing predictor ------------------------------------------------

def u_eff_at_RE(M_star_msun: float, R_E_kpc: float) -> float:
    M = M_star_msun * M_SUN_KG
    R = R_E_kpc * KPC_M
    g_N = G_NEWTON * M / (R * R)
    return 4.0 * g_N / A0_SI


def f_DM_ESD(M_star_msun: float, R_E_kpc: float) -> float:
    """ESD-predicted dark-matter (closure-pool) fraction within R_E."""
    R = R_of_u(u_eff_at_RE(M_star_msun, R_E_kpc))
    return R / (1.0 + R)


def sigma_SIS_esd(M_star_msun: float, R_E_kpc: float) -> float:
    """Single-aperture SIS sigma under ESD."""
    boost = 1.0 + R_of_u(u_eff_at_RE(M_star_msun, R_E_kpc))
    M = M_star_msun * M_SUN_KG
    R = R_E_kpc * KPC_M
    return math.sqrt(G_NEWTON * M * boost / (2.0 * R))


def theta_E_pred_arcsec(M_star_msun: float, R_E_kpc: float,
                        z_lens: float, z_source: float) -> float:
    sigma = sigma_SIS_esd(M_star_msun, R_E_kpc)
    factor = 4.0 * math.pi * (sigma / C_LIGHT) ** 2
    return factor * D_ls_over_D_s(z_lens, z_source) * ARCSEC_PER_RAD


def h_blindness(M_star_msun: float = 3.0e11, R_E_kpc: float = 5.0,
                z_lens: float = 0.25, z_source: float = 0.8) -> dict:
    t1 = theta_E_pred_arcsec(M_star_msun, R_E_kpc, z_lens, z_source)
    t2 = theta_E_pred_arcsec(M_star_msun, R_E_kpc, z_lens, z_source)
    return {"theta_E_arcsec": float(t1),
            "dtheta_dh":      float(t2 - t1),
            "h_blind":        bool(abs(t2 - t1) < 1.0e-20)}
