"""ESD three-channel PPN predictor for the Solar system (Study 33).

Three-channel decomposition:

   D-channel: A^2(D) g_munu      conformal,  modifies effective G_eff
                                 -> PPN gamma deviation
   E-channel: B(D) dD dD          disformal,  gradient sourced
                                 -> PPN beta deviation
   S-channel: Z(D) F^2            photon bridge (locked at floor Z=1)
                                 -> no light-bending modification beyond
                                    what A^2 already provides

At Solar-system scales the gravitational acceleration vastly EXCEEDS
the MOND scale a_0 = 1.2e-10 m/s^2:

   g_Earth_orbit  ~  G M_sun / (1 AU)^2  ~  5.9e-3 m/s^2
   u_Earth        =  4 g / a_0           ~  2.0e8
   g_Cassini       ~  G M_sun / (1.6 R_sun)^2  ~  1.1e2 m/s^2
   u_Cassini       ~  3.6e12

This is DEEP DEEP UV - the kernel sits well below the floor R_floor by
many orders of magnitude. The dominant channel scaling:

   tau_S ~ u^phi      ~  u^1.618    -> grows fastest
   tau_E ~ B * u^q    ~  u^0.595
   tau_D ~ const = c  ~  0.572

For u >> 1, R(u) = S_NORM / Sigma(u) << 1 because Sigma(u) is enormous.
Specifically at u = 2e8: tau_S ~ 6e13, R ~ 4.5e-13.

ESD PPN deviations are then *extremely* suppressed:

   |gamma_ESD - 1|  ~  w_S(u) * R(u)  ~  R(u) ~ 1e-13
   |beta_ESD  - 1|  ~  w_E(u) * R(u)  ~  1e-13 * (B/u^(phi-q))

Both lie ORDERS OF MAGNITUDE below the Cassini and LLR bounds. ESD
reproduces GR in the Solar system without invoking any screening
mechanism.

In addition, the conformal coupling A(D) gives rise to a possible
time variation of G_eff through cosmological D-field evolution.
With D-bar evolving on a Hubble timescale H_0 and a coupling
beta_m bounded by Cassini, the Gdot/G prediction is:

    |Gdot/G|  ~  2 * beta_m^2 * H_0
              ~  2 * (3.2e-5)^2 * 6.94e-11 /yr
              ~  1.4e-19 /yr

This is six orders of magnitude below the LLR bound 1e-13/yr.
"""
from __future__ import annotations

import math
from pathlib import Path
import sys

THIS = Path(__file__).resolve()
sys.path.insert(0, str(THIS.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE

from ppn_data import (
    A0_MOND_SI, G_NEWTON_SI, M_SUN_KG,
    R_EARTH_ORBIT_M, R_MERCURY_ORBIT_M, R_CASSINI_CLOSEST_M,
    G_EARTH_ORBIT_SI, G_CASSINI_SI, G_EARTH_SURFACE_SI,
)

B_BRIDGE: float = PHI ** 6 - 2.0
R_FLOOR: float = S_NORM / C_CHANNEL

# Effective conformal coupling at Solar-gravity (Cassini-bounded):
BETA_M_CASSINI: float = 3.16e-5            # sqrt(|gamma-1|/2) from |gamma-1| < 2e-9
H0_PER_YR: float = 6.94e-11                 # H0 = 67.36 km/s/Mpc in 1/yr


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


def u_from_g(g_si: float) -> float:
    return 4.0 * g_si / A0_MOND_SI


# ============================ PPN predictions ============================
def gamma_minus_1_esd(u: float) -> float:
    """ESD prediction for |gamma - 1| at scale u.

    The D-channel conformal factor A^2(D) ~ 1 + 2 beta_m delta D, so
    the metric perturbation in the t-t and r-r components scales as
    delta-A^2 ~ 2 beta_m delta D where delta D is sourced by the local
    body. The PPN gamma deviation traces R(u) (the inverse of the
    Sigma normalisation) since R measures how much of the closure
    kernel is "available" to enhance the conformal coupling.

    In the deep-UV limit u >> 1, R(u) -> 0 algebraically as u^(-phi),
    so |gamma - 1| -> 0.
    """
    wS, wE, wD = channel_weights(u)
    R = kernel_R(u)
    return wS * R                       # photon bridge correction


def beta_minus_1_esd(u: float) -> float:
    """ESD prediction for |beta - 1|: gradient-coupling deviation.

    Sourced by the E-channel (gradient term in the parent action),
    weighted by w_E(u) * R(u). In the deep UV the gradient channel
    is dominated by the S-channel because tau_S ~ u^phi >> u^q ~ tau_E.
    """
    wS, wE, wD = channel_weights(u)
    R = kernel_R(u)
    return wE * R


def eta_nordtvedt_esd(u: float) -> float:
    """Nordtvedt parameter eta_N = 4(beta-1) - (gamma-1)."""
    return 4.0 * beta_minus_1_esd(u) - gamma_minus_1_esd(u)


def gdot_over_g_per_yr_esd(beta_m: float = BETA_M_CASSINI,
                           H0_per_yr: float = H0_PER_YR) -> float:
    """ESD prediction for |Gdot/G| from cosmological D-field drift.

    Scalar-tensor result (Damour & Nordtvedt 1993):
        Gdot/G  ~  -2 beta_m^2 (Dot D-bar / D-bar)
                ~   2 beta_m^2 H_0
    """
    return 2.0 * beta_m ** 2 * H0_per_yr


# ============================ Solar-system scales ========================
def solar_system_scales() -> dict:
    u_earth   = u_from_g(G_EARTH_ORBIT_SI)
    u_mercury = u_from_g(G_NEWTON_SI * M_SUN_KG / R_MERCURY_ORBIT_M ** 2)
    u_cassini = u_from_g(G_CASSINI_SI)
    u_surface = u_from_g(G_EARTH_SURFACE_SI)
    out = {}
    for label, u in [("earth_orbit", u_earth),
                     ("mercury_orbit", u_mercury),
                     ("cassini_closest", u_cassini),
                     ("earth_surface", u_surface)]:
        wS, wE, wD = channel_weights(u)
        R = kernel_R(u)
        out[label] = {
            "u":              u,
            "R":              R,
            "w_S":            wS,
            "w_E":            wE,
            "w_D":            wD,
            "gamma_minus_1":  gamma_minus_1_esd(u),
            "beta_minus_1":   beta_minus_1_esd(u),
            "eta_nordtvedt":  eta_nordtvedt_esd(u),
        }
    return out


def summary() -> dict:
    s = solar_system_scales()
    s["gdot_over_g_per_yr"] = gdot_over_g_per_yr_esd()
    s["R_floor"] = R_FLOOR
    s["beta_m_cassini"] = BETA_M_CASSINI
    s["H0_per_yr"] = H0_PER_YR
    return s


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=2))
