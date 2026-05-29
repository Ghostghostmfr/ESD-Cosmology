"""Study 09 — ESD disformal photon dispersion and GW170817 closure.

Reproduces Channel 1 of the published Hubble paper:

  James P. Higginson, "ESD Framework: The Hubble Tension as a Structural
  h-Blindness Boundary and Mirror-Identity Classification of Dark Energy"
  (2026). Zenodo DOI: 10.5281/zenodo.20400097.

Dispersion law:
    c_gamma^2(z) = 1 - eps_0 (1+z)^3 - eps_2 (1+z)^6
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad

import esd_core as ESD

# --- physical constants ---------------------------------------------------
C_LIGHT_M_S: float = 299_792_458.0
MPC_M:        float = 3.0856775814913673e22

# --- paper-quoted dispersion bounds (Sec. Channel 1) ---------------------
EPS0_PAPER_BOUND: float = 6.0e-15        # |eps_0| from GW170817
EPS2_PAPER_BOUND: float = 5.9e-19        # from photon-barrier c_gamma^2 >= 0
DELTA_H0_PAPER:   float = 0.12           # km/s/Mpc, max channel cap
Z_LSS:            float = 1089.95        # last-scattering surface (Planck 2018)

# Friedmann background for the angular-diameter integral
OMEGA_M_REF: float = 0.3158
OMEGA_B_REF: float = 0.04930
OMEGA_R_REF: float = 9.2e-5              # photons + 3.046 neutrinos
H0_REF_KM_S_MPC: float = 67.36
H0_REF_SI: float = H0_REF_KM_S_MPC * 1000.0 / MPC_M


# =========================================================================
#  Dispersion law
# =========================================================================
def c_gamma_sq(z: np.ndarray | float, eps0: float, eps2: float) -> np.ndarray | float:
    """Oscillation-averaged photon metric on FLRW: c_gamma^2(z) / c^2.

    The (1+z)^3 piece is sourced by the disformal `eps_0` coupling and is
    pinned by GW170817; the (1+z)^6 piece is sourced by `eps_2` and is
    pinned by the photon-barrier condition c_gamma^2 >= 0 at z = z_LSS.
    """
    one_plus_z = 1.0 + np.asarray(z)
    return 1.0 - eps0 * one_plus_z**3 - eps2 * one_plus_z**6


def photon_barrier_ok(eps0: float, eps2: float, z: float = Z_LSS) -> bool:
    """True iff the photon metric remains non-negative all the way to z."""
    return float(c_gamma_sq(z, eps0, eps2)) >= 0.0


def eps2_max_from_barrier(eps0: float, z: float = Z_LSS) -> float:
    """Largest eps_2 compatible with c_gamma^2(z) >= 0 for the given eps_0.

    Solves   1 - eps_0 (1+z)^3 - eps_2 (1+z)^6 = 0   for eps_2.
    """
    return (1.0 - eps0 * (1.0 + z) ** 3) / (1.0 + z) ** 6


# =========================================================================
#  GW170817 multi-messenger speed bound
# =========================================================================
def gw170817_eps0_bound(
    delta_t_s: float = 1.74,
    D_mpc:    float = 40.0,
) -> float:
    """|c_gamma - c_GW|/c <= delta_t_s / (D / c).

    Returns the symmetric bound on |eps_0|. With (delta_t=1.74 s,
    D=40 Mpc) -> ~4e-17, which sits comfortably under the published
    eps_0 < 6e-15 (the published bound includes Δ-allocation
    for any intrinsic GRB delay).
    """
    travel_s = D_mpc * MPC_M / C_LIGHT_M_S
    return delta_t_s / travel_s


def gw170817_delta_c_over_c() -> dict:
    """Reproduce the Abbott+2017 multi-messenger speed bound."""
    naive_bound = gw170817_eps0_bound(1.74, 40.0)
    return {
        "delta_t_s":          1.74,
        "D_lum_mpc":          40.0,
        "naive_bound":        naive_bound,
        "abbott2017_window":  (-3.0e-15, +7.0e-16),
        "paper_eps0_bound":   EPS0_PAPER_BOUND,
    }


# =========================================================================
#  Modified angular-diameter distance D_A(z_LSS) under disformal photons
# =========================================================================
def E_z(z: np.ndarray | float,
        Om: float = OMEGA_M_REF,
        Or: float = OMEGA_R_REF) -> np.ndarray | float:
    """H(z) / H_0 for flat LCDM with photons + 3 nu_eff."""
    return np.sqrt(Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + (1.0 - Om - Or))


def DA_factor(eps0: float, eps2: float, z_max: float = Z_LSS) -> float:
    """Ratio D_A(modified) / D_A(GR), to leading order in (eps_0, eps_2).

    With c_gamma(z) replacing c, the integrand dr/dz scales by c_gamma(z).
    """
    integrand_base = lambda z: 1.0 / E_z(z)
    integrand_mod  = lambda z: math.sqrt(max(c_gamma_sq(z, eps0, eps2), 0.0)) / E_z(z)
    base, _ = quad(integrand_base, 0.0, z_max, limit=200)
    mod,  _ = quad(integrand_mod,  0.0, z_max, limit=200)
    return mod / base


def delta_H0_from_dispersion(
    eps0: float = EPS0_PAPER_BOUND,
    eps2: float | None = None,
    H0:   float = H0_REF_KM_S_MPC,
) -> dict:
    """Inferred Delta H_0 from a saturated disformal dispersion.

    Keeping the CMB acoustic angle theta_* = r_s / D_A(z_*) fixed
    (the empirical Planck-pinned observable), a fractional shift
    f = D_A(mod)/D_A(GR) - 1 in the angular-diameter distance maps
    to a fractional shift in the inferred H_0:
        Delta H_0 / H_0  ~=  - Delta D_A / D_A
    (since r_s depends on omega_m h^2 only and is unchanged at fixed
     omega_m, while D_A ~ 1/H_0 to leading order in flat LCDM).
    """
    if eps2 is None:
        eps2 = eps2_max_from_barrier(eps0)
    f = DA_factor(eps0, eps2) - 1.0
    dH0 = -H0 * f
    return {
        "eps0":         eps0,
        "eps2":         eps2,
        "DA_ratio":     1.0 + f,
        "delta_DA_rel": f,
        "delta_H0":     dH0,
        "H0_ref":       H0,
    }
