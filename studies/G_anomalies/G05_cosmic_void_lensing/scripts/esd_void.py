"""ESD void-profile predictor (three-channel closure kernel).

The parent action (Master Ch.3) has three channels:

   - D-channel  A^2(D) g_munu       conformal,  bulk-density sourced
   - E-channel  B(D) dD dD          disformal,  gradient sourced
   - S-channel  Z(D) F^2 (spectator) floor / UV completion

These three channels appear additively in the closure-kernel
denominator (esd_core/constants.py):

   R(u)  =  s / Sigma(u),     Sigma(u) = u^phi + b u^q + c
                                       \\___/  \\____/  \\_/
                                        S       E       D
                                        UV      bridge  floor

so we decompose

   tau_S(u) = u^phi                       (S-channel weight in Sigma)
   tau_E(u) = b * u^q                     (E-channel weight in Sigma)
   tau_D(u) = c                           (D-channel weight in Sigma)
   w_X(u)   = tau_X(u) / Sigma(u)         (channel fraction, sums to 1)
   R_X(u)   = w_X(u) * R(u)               (channel-resolved kernel)

In a void the two sub-regions are NOT sourced by the same channel:

   Interior (uniform low density, r < R_v):
        sourced by bulk density rho_eff = rho_bar (1 + delta_c) < 0
        -> D-channel dominates
        -> amplifier = sqrt(1 + R_D(u_void))

   Wall (compensation ridge, r ~ 1.1 R_v):
        sourced by the gradient of delta across the wall
        -> E-channel dominates
        -> amplifier = sqrt(1 + R_E(u_wall))
        with u_wall set by the wall acceleration (gradient-sourced),
        not the void-interior acceleration; u_wall >> u_void.

This is the genuine three-channel ESD prediction. The single-channel
collapse (one R(u) acting on both interior and wall via the same
sqrt(1+R) factor) is the scalar-tensor proxy and overshoots void
diagnostics by ~6x. We do not implement that here.

Interior depth is capped at delta = -1 by non-linear unitarity (can't
evacuate more than 100% of the cosmic mean).
"""
from __future__ import annotations

import math
from pathlib import Path
import sys

THIS = Path(__file__).resolve()
sys.path.insert(0, str(THIS.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE

from void_data import (
    A0_MOND_SI, G_NEWTON_SI, MPC_M, RHO_MEAN_KG_M3,
    R_V_TYPICAL_MPC, DELTA_INT_TYPICAL,
    HSW_ALPHA, HSW_BETA, HSW_RS_OVER_RV,
)

B_BRIDGE: float = PHI ** 6 - 2.0
R_FLOOR: float = S_NORM / C_CHANNEL
AMP_FLOOR: float = math.sqrt(1.0 + R_FLOOR)


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


# ============================ u at sub-regions ============================
def u_void(r_v_mpc: float = R_V_TYPICAL_MPC,
           delta_int: float = DELTA_INT_TYPICAL) -> float:
    """u_eff in the void interior (r = R_v / 2)."""
    r_m = 0.5 * r_v_mpc * MPC_M
    rho_residual = RHO_MEAN_KG_M3 * (1.0 + delta_int)
    mass_enc = (4.0 / 3.0) * math.pi * r_m ** 3 * rho_residual
    g_si = G_NEWTON_SI * abs(mass_enc) / r_m ** 2
    return 4.0 * g_si / A0_MOND_SI


def u_wall(r_v_mpc: float = R_V_TYPICAL_MPC,
           delta_int: float = DELTA_INT_TYPICAL) -> float:
    """u_eff at the compensation wall (r ~ R_v).

    Wall acceleration sources from the full mass deficit inside R_v
    acting at radius R_v.
    """
    R_m = r_v_mpc * MPC_M
    mass_def = (4.0 / 3.0) * math.pi * R_m ** 3 * RHO_MEAN_KG_M3 \
        * abs(delta_int)
    g_si = G_NEWTON_SI * mass_def / R_m ** 2
    return 4.0 * g_si / A0_MOND_SI


# ============================ HSW mapping =================================
def hsw_profile(r_over_rv: float,
                delta_c: float,
                wall_amp: float,
                alpha: float = HSW_ALPHA,
                beta: float = HSW_BETA,
                rs_over_rv: float = HSW_RS_OVER_RV) -> float:
    core = delta_c * (1.0 - (r_over_rv / rs_over_rv) ** alpha) / \
        (1.0 + (r_over_rv) ** beta)
    wall = wall_amp * math.exp(-0.5 * ((r_over_rv - 1.10) / 0.18) ** 2)
    return core + wall


def esd_profile_parameters(delta_c_lcdm: float,
                           wall_amp_lcdm: float) -> dict:
    """Three-channel ESD mapping.

    Interior: D-channel amplifier at u_void.
    Wall:     E-channel amplifier at u_wall.
    """
    u_in = u_void()
    u_wl = u_wall()

    R_S_in, R_E_in, R_D_in = R_channels(u_in)
    R_S_wl, R_E_wl, R_D_wl = R_channels(u_wl)

    amp_D_interior = math.sqrt(1.0 + R_D_in)
    amp_E_wall = math.sqrt(1.0 + R_E_wl)

    delta_c_raw = delta_c_lcdm * amp_D_interior
    delta_c_capped = max(delta_c_raw, -1.0)
    wall_amp_esd = wall_amp_lcdm * amp_E_wall

    wS_in, wE_in, wD_in = channel_weights(u_in)
    wS_wl, wE_wl, wD_wl = channel_weights(u_wl)

    return {
        "delta_c_lcdm":    delta_c_lcdm,
        "wall_amp_lcdm":   wall_amp_lcdm,
        # interior (D-channel)
        "u_void":          u_in,
        "R_total_interior": kernel_R(u_in),
        "R_D_interior":    R_D_in,
        "R_E_interior":    R_E_in,
        "R_S_interior":    R_S_in,
        "w_D_interior":    wD_in,
        "w_E_interior":    wE_in,
        "w_S_interior":    wS_in,
        "amp_D_interior":  amp_D_interior,
        "delta_c_esd_raw": delta_c_raw,
        "delta_c_esd":     delta_c_capped,
        "delta_c_saturated": delta_c_raw <= -1.0,
        # wall (E-channel)
        "u_wall":          u_wl,
        "R_total_wall":    kernel_R(u_wl),
        "R_D_wall":        R_D_wl,
        "R_E_wall":        R_E_wl,
        "R_S_wall":        R_S_wl,
        "w_D_wall":        wD_wl,
        "w_E_wall":        wE_wl,
        "w_S_wall":        wS_wl,
        "amp_E_wall":      amp_E_wall,
        "wall_amp_esd":    wall_amp_esd,
        # reference
        "R_floor":         R_FLOOR,
        "amp_floor_single_channel": AMP_FLOOR,
    }


# =========================== lensing predictor ============================
def _sigma_R(R_over_rv: float,
             delta_c_esd: float,
             wall_amp_esd: float,
             r_v_mpc: float,
             z_max_rv: float = 3.0,
             n_z: int = 800) -> float:
    """Projected surface mass density Sigma(R) in h Msun/pc^2.

    Sigma(R)  =  rho_mean * R_v * 2 * integral_0^z_max delta(sqrt(R^2+z^2)) dz
    (R, z in units of R_v; result has the surface_norm prefactor below).
    """
    import numpy as np
    zs = np.linspace(0.0, z_max_rv, n_z)
    rs = np.sqrt(R_over_rv ** 2 + zs ** 2)
    delta_los = np.array([hsw_profile(r, delta_c_esd, wall_amp_esd)
                          for r in rs])
    # factor 2 for symmetric LOS [-z_max, +z_max]:
    integral = 2.0 * float(np.trapezoid(delta_los, zs))
    rho_mean_msun_pc3 = RHO_MEAN_KG_M3 / (1.989e30) * (3.0857e16) ** 3
    surface_norm = rho_mean_msun_pc3 * (r_v_mpc * 1.0e6)
    return integral * surface_norm


def delta_sigma_peak(delta_c_esd: float,
                     wall_amp_esd: float,
                     r_v_mpc: float = R_V_TYPICAL_MPC,
                     r_over_rv_eval: float = 1.0,
                     n_inner: int = 80) -> float:
    """Excess surface mass density Delta Sigma(R) = mean Sigma(<R) - Sigma(R).

    DES Y3 (Fang+ 2019) measure this contrast, not Sigma itself, so the
    interior void emptiness shows up as a large NEGATIVE Sigma_bar(<R_v)
    relative to the wall-dominated Sigma(R_v).
    """
    import numpy as np
    R = r_over_rv_eval
    # Sigma(R)
    sigma_R = _sigma_R(R, delta_c_esd, wall_amp_esd, r_v_mpc)
    # area-weighted mean Sigma inside R: (2/R^2) integral_0^R R' Sigma(R') dR'
    Rps = np.linspace(1e-3, R, n_inner)
    sig_arr = np.array([_sigma_R(Rp, delta_c_esd, wall_amp_esd, r_v_mpc)
                        for Rp in Rps])
    sigma_mean_inside = (2.0 / R ** 2) * float(np.trapezoid(Rps * sig_arr, Rps))
    return sigma_mean_inside - sigma_R


def summary() -> dict:
    u_in = u_void()
    u_wl = u_wall()
    wS_in, wE_in, wD_in = channel_weights(u_in)
    wS_wl, wE_wl, wD_wl = channel_weights(u_wl)
    RS_in, RE_in, RD_in = R_channels(u_in)
    RS_wl, RE_wl, RD_wl = R_channels(u_wl)
    return {
        "u_void":             u_in,
        "u_wall":             u_wl,
        "u_wall_over_u_void": u_wl / u_in,
        "R_total_interior":   kernel_R(u_in),
        "R_total_wall":       kernel_R(u_wl),
        "R_D_interior":       RD_in,
        "R_E_wall":           RE_wl,
        "w_D_interior":       wD_in,
        "w_E_wall":           wE_wl,
        "amp_D_interior":     math.sqrt(1.0 + RD_in),
        "amp_E_wall":         math.sqrt(1.0 + RE_wl),
        "amp_floor_single_channel": AMP_FLOOR,
    }
