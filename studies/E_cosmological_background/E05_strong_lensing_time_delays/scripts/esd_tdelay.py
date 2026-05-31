"""ESD time-delay predictor (three-channel closure kernel).

Three-channel decomposition of the parent action (Master Ch.3):

   D-channel  A^2(D) g_munu       conformal,  bulk-density sourced
   E-channel  B(D) dD dD          disformal,  gradient sourced
   S-channel  Z(D) F^2            photon bridge (locked at floor)

For a strong-lens time-delay measurement there are TWO regimes:

1. LENS-SCALE PHYSICS (Einstein radius, r ~ 5-15 kpc):

      g(R_E) ~ sigma_v^2 / R_E  ~  1.86e-10 m/s^2  (massive elliptical)
      u_lens = 4 g(R_E) / a_0   ~  6.2

   This is the MOND TRANSITION REGIME (u ~ O(1)), not deep IR.
   The closure kernel is well off the floor:
      R(u_lens) ~ 0.40, R_D ~ 0.003, R_E ~ 0.28, R_S ~ 0.12
      w_D ~ 0.009, w_E ~ 0.71, w_S ~ 0.29
   D-channel modification of the Fermat potential is
   amp_D = sqrt(1 + R_D) ~ 1.002 - a 0.2 % enhancement, well below
   the ~10 % mass-sheet-degeneracy floor. The E and S channels carry
   most of the (small) closure pool at lens scales and do not modify
   the standard parametric-lens Fermat potential. The lens-scale ESD
   signature is therefore NEGLIGIBLE.

2. COSMOLOGICAL DISTANCES (D_l, D_s, D_ls):

      D_dt = (1 + z_l) * D_l * D_s / D_ls
      H(z) sets the angular-diameter distances.

   This is the ONLY ESD signature in the time-delay anchor: H_0 and
   H(z) are framework-locked.  In ESD the H_0 prediction
   (Studies 08, 12) is

        H_0^ESD  =  c * sqrt(8 pi / i_dB) / a_0  =  67.36 km/s/Mpc

   identical to Planck within Planck's error budget. The framework's
   modification of H(z) at z < 2 is sub-1% (D-field dark-energy
   sector, theory/02_vacuum_lambda) and below TDCOSMO precision.

Net ESD prediction for the TDCOSMO inferred H_0:

      H_0^TDCOSMO,ESD  =  67.36 +/- 0.54 km/s/Mpc.

This is consistent with Birrer+ 2020 (TDCOSMO-IV, 67.4 +4.1/-3.2,
mass-sheet flexible) and in 2-3 sigma tension with Wong+ 2020
(73.3 +1.7/-1.8, rigid power-law lens models).
"""
from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np
from scipy import integrate

THIS = Path(__file__).resolve()
sys.path.insert(0, str(THIS.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE

from tdcosmo_data import (
    A0_MOND_SI, C_LIGHT_KM_S, MPC_KM, KPC_M, M_SUN_KG, G_NEWTON_SI,
    H0_ESD, OMEGA_M, OMEGA_L,
    SIGMA_V_LENS_KM_S, THETA_E_ARCSEC, D_L_TYPICAL_MPC,
)

B_BRIDGE: float = PHI ** 6 - 2.0
R_FLOOR: float = S_NORM / C_CHANNEL


# ============================ kernel + channels ===========================
def _sigma_terms(u: float) -> tuple[float, float, float]:
    tau_S = u ** PHI
    tau_E = B_BRIDGE * (u ** Q_BRIDGE)
    tau_D = C_CHANNEL
    return tau_S, tau_E, tau_D


def kernel_R(u: float) -> float:
    tS, tE, tD = _sigma_terms(u)
    return S_NORM / (tS + tE + tD)


def channel_weights(u: float) -> tuple[float, float, float]:
    tS, tE, tD = _sigma_terms(u)
    sigma = tS + tE + tD
    return tS / sigma, tE / sigma, tD / sigma


def R_channels(u: float) -> tuple[float, float, float]:
    wS, wE, wD = channel_weights(u)
    R = kernel_R(u)
    return wS * R, wE * R, wD * R


# ============================ lens-scale u ================================
def u_lens(sigma_v_km_s: float = SIGMA_V_LENS_KM_S,
           theta_E_arcsec: float = THETA_E_ARCSEC,
           D_l_mpc: float = D_L_TYPICAL_MPC) -> dict:
    """u_eff at the Einstein radius of a typical SIS lens.

    g(R_E) ~ sigma_v^2 / R_E   (SIS isothermal sphere acceleration).
    """
    theta_E_rad = theta_E_arcsec * math.pi / (180.0 * 3600.0)
    R_E_m = theta_E_rad * D_l_mpc * MPC_KM * 1.0e3       # Mpc -> m
    sigma_v_m_s = sigma_v_km_s * 1.0e3
    g_si = sigma_v_m_s ** 2 / R_E_m
    u = 4.0 * g_si / A0_MOND_SI
    wS, wE, wD = channel_weights(u)
    RS, RE, RD = R_channels(u)
    return {
        "R_E_kpc":         R_E_m / KPC_M,
        "g_lens_si":       g_si,
        "u_lens":          u,
        "R_total":         kernel_R(u),
        "R_D":             RD,
        "R_E":             RE,
        "R_S":             RS,
        "w_D":             wD,
        "w_E":             wE,
        "w_S":             wS,
        "amp_D_lens":      math.sqrt(1.0 + RD),
    }


# ============================ cosmology (flat LCDM-like) =================
def E_of_z(z: float, omega_m: float = OMEGA_M) -> float:
    """Dimensionless H(z)/H_0 = sqrt(Omega_m (1+z)^3 + Omega_L)."""
    return math.sqrt(omega_m * (1.0 + z) ** 3 + (1.0 - omega_m))


def comoving_distance_mpc(z: float,
                          H0_km_s_mpc: float,
                          omega_m: float = OMEGA_M) -> float:
    """Line-of-sight comoving distance D_C(z) in Mpc, flat universe."""
    integrand = lambda zp: 1.0 / E_of_z(zp, omega_m)
    integral, _ = integrate.quad(integrand, 0.0, z, limit=200)
    return C_LIGHT_KM_S / H0_km_s_mpc * integral


def angular_diameter_distance_mpc(z_a: float, z_b: float,
                                  H0_km_s_mpc: float,
                                  omega_m: float = OMEGA_M) -> float:
    """D_A between z_a and z_b (z_a < z_b), flat universe, Mpc."""
    if z_b <= z_a:
        return 0.0
    DC_a = comoving_distance_mpc(z_a, H0_km_s_mpc, omega_m)
    DC_b = comoving_distance_mpc(z_b, H0_km_s_mpc, omega_m)
    return (DC_b - DC_a) / (1.0 + z_b)


def time_delay_distance_mpc(z_l: float, z_s: float,
                            H0_km_s_mpc: float,
                            omega_m: float = OMEGA_M) -> float:
    """D_dt = (1+z_l) D_l D_s / D_ls,  in Mpc."""
    D_l  = angular_diameter_distance_mpc(0.0, z_l, H0_km_s_mpc, omega_m)
    D_s  = angular_diameter_distance_mpc(0.0, z_s, H0_km_s_mpc, omega_m)
    D_ls = angular_diameter_distance_mpc(z_l, z_s, H0_km_s_mpc, omega_m)
    return (1.0 + z_l) * D_l * D_s / D_ls


# ============================ H_0 inversion ===============================
def H0_from_D_dt(D_dt_obs_mpc: float, z_l: float, z_s: float,
                 omega_m: float = OMEGA_M) -> float:
    """Invert observed D_dt to H_0 at fixed Omega_m (D_dt ~ 1/H_0)."""
    H0_ref = 100.0
    D_dt_ref = time_delay_distance_mpc(z_l, z_s, H0_ref, omega_m)
    return H0_ref * (D_dt_ref / D_dt_obs_mpc)


def summary() -> dict:
    lens = u_lens()
    return {
        "u_lens":          lens["u_lens"],
        "R_total_lens":    lens["R_total"],
        "R_D_lens":        lens["R_D"],
        "w_D_lens":        lens["w_D"],
        "w_E_lens":        lens["w_E"],
        "w_S_lens":        lens["w_S"],
        "amp_D_lens":      lens["amp_D_lens"],
        "R_floor":         R_FLOOR,
        "H0_esd_km_s_mpc": H0_ESD,
    }
