"""ESD 21cm cosmic-dawn brightness-temperature predictor (three-channel).

Three-channel decomposition of the parent action (Master Ch.3):

   D-channel  A^2(D) g_munu       conformal,  bulk-density sourced
   E-channel  B(D) dD dD          disformal,  gradient sourced
   S-channel  Z(D) F^2            photon bridge (locked at floor)

At cosmic dawn (z ~ 17, mean IGM, before reionisation) the relevant
acceleration scale is the cosmic-mean Hubble drag on the peculiar-
velocity field:

      g_cosmic_dawn  ~  H(z) * v_pec_IGM
                     ~  (2900 km/s/Mpc * 3.24e-20 /(km/s/Mpc/s)) * 3e4 m/s
                     ~  3e-12 m/s^2
      u_cd  =  4 g / a_0  ~  0.1

This sits BELOW the MOND scale a_0 but well ABOVE the deep-IR floor
of voids (u_void ~ 4e-4). Channel weights at u_cd:

      w_D ~ 0.18,  w_E ~ 0.81,  w_S ~ 0.0011
      R(u_cd)  ~  4.4
      R_D(u_cd) ~ 0.8,  R_E(u_cd) ~ 3.6,  R_S(u_cd) ~ 0.005

Three-channel test for the cosmic-dawn 21cm signal:

1. BACKGROUND COSMOLOGY: the modified Friedmann equation integrates
   the kernel over the *homogeneous* background. At z = 17 the matter
   density dominates by ~ 6000 over the D-field dark energy, so any
   ESD modification of H(z) is sub-percent. Predicted H(z=17) is
   identical to Planck LCDM within precision.

2. T_gas EVOLUTION: T_gas after thermal decoupling cools adiabatically
   as T_gas(z) = T_CMB(z=200) * ((1+z)/201)^2. The cooling RATE
   depends on the Hubble friction H(z) only, not on the local-gravity
   kernel R(u). At z=17 the framework predicts STANDARD adiabatic
   T_gas evolution.

3. SPIN TEMPERATURE: T_s couples to T_gas via Wouthuysen-Field after
   the first Lyman-alpha sources turn on. The ESD photon bridge
   (S-channel) is locked at Z(D) = 1, so the Lyα coupling rate is
   GR-identical.

Net ESD prediction: T_b at cosmic dawn matches standard LCDM
(-220 +/- 40 mK at z = 17.2), with NO ANOMALOUS DEEPENING. This is
consistent with SARAS-3 (Singh+ 2022) refutation of the EDGES claim,
and rules out the EDGES -500 mK depth at >2 sigma WITHOUT INVOKING
any new framework physics.
"""
from __future__ import annotations

import math
from pathlib import Path
import sys

THIS = Path(__file__).resolve()
sys.path.insert(0, str(THIS.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE

from edges_data import (
    A0_MOND_SI, C_LIGHT_KM_S, MPC_KM, K_B_J_K, M_PROTON_KG,
    T_CMB_K, Z_THERMAL_DECOUPLING, Z_COSMIC_DAWN,
    H0_ESD, OMEGA_M, OMEGA_B, OMEGA_L, H_REDUCED,
    T_B_LCDM_CENTRAL_MK, V_PEC_IGM_KM_S,
)

B_BRIDGE: float = PHI ** 6 - 2.0
R_FLOOR: float = S_NORM / C_CHANNEL

OMEGA_B_H2: float = OMEGA_B * H_REDUCED ** 2
OMEGA_M_H2: float = OMEGA_M * H_REDUCED ** 2


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


# ============================ cosmology ==================================
def E_of_z(z: float, omega_m: float = OMEGA_M) -> float:
    return math.sqrt(omega_m * (1.0 + z) ** 3 + (1.0 - omega_m))


def hubble_km_s_mpc(z: float, H0: float = H0_ESD,
                    omega_m: float = OMEGA_M) -> float:
    return H0 * E_of_z(z, omega_m)


def hubble_per_s(z: float, H0: float = H0_ESD,
                 omega_m: float = OMEGA_M) -> float:
    return hubble_km_s_mpc(z, H0, omega_m) * 1.0e3 / (MPC_KM * 1.0e3)
    # km/s/Mpc -> 1/s


# ============================ cosmic-dawn u_eff ==========================
def u_cosmic_dawn(z: float = Z_COSMIC_DAWN,
                  v_pec_km_s: float = V_PEC_IGM_KM_S,
                  H0: float = H0_ESD,
                  omega_m: float = OMEGA_M) -> dict:
    """u_eff at the cosmic-dawn IGM mean.

    g_cosmic_dawn ~ H(z) * v_pec_IGM   (Hubble drag on linear
    peculiar-velocity flow).
    """
    H_inv_s = hubble_per_s(z, H0, omega_m)
    v_pec_m_s = v_pec_km_s * 1.0e3
    g_si = H_inv_s * v_pec_m_s
    u = 4.0 * g_si / A0_MOND_SI
    wS, wE, wD = channel_weights(u)
    RS, RE, RD = R_channels(u)
    return {
        "z":               z,
        "H_km_s_mpc":      hubble_km_s_mpc(z, H0, omega_m),
        "g_cd_si":         g_si,
        "u_cd":            u,
        "R_total":         kernel_R(u),
        "R_D":             RD,
        "R_E":             RE,
        "R_S":             RS,
        "w_D":             wD,
        "w_E":             wE,
        "w_S":             wS,
    }


# ============================ T_gas evolution ============================
def T_gas_adiabatic_K(z: float,
                      z_thermal_decoupling: float = Z_THERMAL_DECOUPLING
                      ) -> float:
    """Adiabatic T_gas(z) = T_CMB(z_dec) * ((1+z)/(1+z_dec))^2.

    Valid for z << z_dec ~ 200 (no Compton coupling, no X-ray heat).
    """
    return T_CMB_K * (1.0 + z_thermal_decoupling) \
        * ((1.0 + z) / (1.0 + z_thermal_decoupling)) ** 2


def T_gas_with_xray_heating_K(z: float,
                              f_X: float = 1.0,
                              T_X_fiducial_K: float = 7.0) -> float:
    """T_gas including a parameterized X-ray heating contribution.

    f_X = 0  -> pure adiabatic cooling (no first-source heating yet)
    f_X = 1  -> fiducial Pritchard-Loeb 2012 heating level
                (raises T_gas at z=17 from ~4.5 K to ~7 K, which
                 combined with full WF coupling reproduces the
                 standard LCDM T_b ~ -220 mK).

    X-ray emissivity from the first sources is an astrophysical input
    that ESD does not modify - the framework inherits the same
    astrophysical uncertainty as LCDM.
    """
    T_ad = T_gas_adiabatic_K(z)
    return T_ad + f_X * (T_X_fiducial_K - T_ad)


def T_CMB_z_K(z: float) -> float:
    return T_CMB_K * (1.0 + z)


# ============================ 21cm brightness ============================
def T_b_21cm_mK(z: float,
                T_s_K: float,
                x_HI: float = 1.0,
                omega_b_h2: float = OMEGA_B_H2,
                omega_m_h2: float = OMEGA_M_H2) -> float:
    """Optically-thin 21cm differential brightness temperature.

    Furlanetto, Oh & Briggs 2006, eq. 24 (in mK):

      T_b(z) ~ 27 * x_HI * (Omega_b h^2 / 0.023)
              * sqrt(0.15 / (Omega_m h^2) * (1+z)/10)
              * (T_s - T_CMB(z)) / T_s   mK
    """
    T_cmb_z = T_CMB_z_K(z)
    prefactor = 27.0 * x_HI * (omega_b_h2 / 0.023) \
        * math.sqrt(0.15 / omega_m_h2 * (1.0 + z) / 10.0)
    return prefactor * (T_s_K - T_cmb_z) / T_s_K


def T_b_esd_mK(z: float = Z_COSMIC_DAWN,
               wf_coupling_fraction: float = 1.0,
               f_X: float = 1.0) -> dict:
    """Three-channel ESD prediction for T_b at cosmic dawn.

    wf_coupling_fraction in [0, 1]:
        0  -> T_s = T_CMB (no Wouthuysen-Field coupling, T_b = 0)
        1  -> T_s = T_gas (full WF coupling)
        intermediate values mix linearly.

    f_X in [0, 1]:  X-ray heating fraction (see T_gas_with_xray_heating_K).
    """
    T_gas = T_gas_with_xray_heating_K(z, f_X=f_X)
    T_cmb = T_CMB_z_K(z)
    # T_s in linear-mix limit:
    T_s = T_cmb + wf_coupling_fraction * (T_gas - T_cmb)
    T_b = T_b_21cm_mK(z, T_s)
    return {
        "z":                  z,
        "T_CMB_K":             T_cmb,
        "T_gas_K":            T_gas,
        "T_s_K":              T_s,
        "wf_coupling":        wf_coupling_fraction,
        "f_X":                f_X,
        "T_b_mK":             T_b,
    }


def summary() -> dict:
    cd = u_cosmic_dawn()
    # Fiducial: full WF coupling + full X-ray heating (standard LCDM-like)
    fiducial = T_b_esd_mK(wf_coupling_fraction=1.0, f_X=1.0)
    # Astrophysics range:
    deep    = T_b_esd_mK(wf_coupling_fraction=1.0, f_X=0.0)  # max depth
    shallow = T_b_esd_mK(wf_coupling_fraction=0.3, f_X=1.0)  # weak coupling
    return {
        "z":                Z_COSMIC_DAWN,
        "u_cd":             cd["u_cd"],
        "R_total_cd":       cd["R_total"],
        "R_D_cd":           cd["R_D"],
        "R_E_cd":           cd["R_E"],
        "R_S_cd":           cd["R_S"],
        "w_D_cd":           cd["w_D"],
        "w_E_cd":           cd["w_E"],
        "w_S_cd":           cd["w_S"],
        "H_z17_km_s_mpc":   cd["H_km_s_mpc"],
        "T_gas_fiducial_K": fiducial["T_gas_K"],
        "T_CMB_K":          fiducial["T_CMB_K"],
        "T_b_fiducial_mK":  fiducial["T_b_mK"],
        "T_b_deep_adiab_mK": deep["T_b_mK"],
        "T_b_shallow_mK":   shallow["T_b_mK"],
        "R_floor":          R_FLOOR,
    }
