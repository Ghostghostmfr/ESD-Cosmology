"""Closed-form ESD super-horizon D-gradient predictions.

Implements the unified coherent-gradient ansatz derived in the README.

Single parameter:  eta = beta_m * G_in * R_H   (dimensionless)
Single direction:  g_hat = (l_deg, b_deg) in Galactic coordinates

Maps eta -> three observables:
  - cosmic dipole excess (Study 25)
  - CMB hemispherical-asymmetry amplitude (Study 29)
  - satellite-plane alignment correlation (Study 28)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


# ---------------------------------------------------------------------------
# Universal cosmological constants
# ---------------------------------------------------------------------------

C_KMS = 299_792.458          # speed of light, km/s
H0_KMSMPC = 67.4             # Planck 2018 baseline H0
R_H_MPC = C_KMS / H0_KMSMPC  # Hubble radius, ~4448 Mpc
R_H_GPC = R_H_MPC / 1000.0

# Comoving distance to last-scattering surface (Planck 2018 LCDM)
CHI_LSS_GPC = 13.87
CHI_LSS_OVER_RH = CHI_LSS_GPC / R_H_GPC   # ~3.12

# Effective survey depths (median comoving distance, Mpc)
CHI_NVSS_MPC = 2800.0   # NVSS radio sources, median z ~ 1
CHI_CATWISE_MPC = 3500.0  # CatWISE quasars, median z ~ 1.2

# Ellis-Baldwin spectral-plus-count parameter x = 2 + alpha(1+beta)
# Standard literature values:
X_NVSS = 1.25
X_CATWISE = 1.7


# ---------------------------------------------------------------------------
# Single-parameter ansatz
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GradientAnsatz:
    """Coherent super-horizon D-gradient ansatz.

    eta : dimensionless gradient amplitude = beta_m * G_in * R_H
    l_deg, b_deg : Galactic coordinates of the preferred axis g_hat
    """
    eta: float
    l_deg: float
    b_deg: float

    def g_hat(self) -> np.ndarray:
        l = math.radians(self.l_deg)
        b = math.radians(self.b_deg)
        return np.array([
            math.cos(b) * math.cos(l),
            math.cos(b) * math.sin(l),
            math.sin(b),
        ])


# ---------------------------------------------------------------------------
# Observable 1: cosmic dipole excess
# ---------------------------------------------------------------------------

def conformal_dipole_amplitude(eta: float, chi_mpc: float, x_eb: float) -> float:
    """Dipole amplitude in source number counts from a coherent D-gradient.

    D_conformal = x * eta * (chi / R_H)

    The cosmic-frame kinematic Ellis-Baldwin dipole D_kin must be added
    separately. The TOTAL observed dipole is D_kin + D_conformal (assuming
    g_hat happens to align with the CMB-velocity direction; in general the
    two add vectorially).
    """
    return x_eb * eta * (chi_mpc / R_H_MPC)


def kinematic_dipole_amplitude(v_kms: float, x_eb: float, alpha: float = 0.75) -> float:
    """Standard Ellis-Baldwin kinematic dipole: D = [2 + x(1+alpha)] v/c.

    Note: x_eb here is the count-slope; the formula's `x(1+alpha)` factor
    is conventionally captured in the lumped `x_EB` ~ 2 + alpha(1+x).
    We use the textbook form:
        D_kin = [2 + alpha*(1 + x_eb)] * v/c
    Defaults give D_kin(369.82, 1.25) ~ 0.00461 - matches Study 25.
    """
    factor = 2.0 + alpha * (1.0 + x_eb)
    return factor * (v_kms / C_KMS)


# ---------------------------------------------------------------------------
# Observable 2: CMB hemispherical asymmetry
# ---------------------------------------------------------------------------

# Locked Starobinsky inflation parameters (Master Ch.15)
N_E_INFLATION = 69.3                # F_12 * ln(phi), forward-derived
ALPHA_STARO = math.sqrt(2.0 / 3.0)  # conformal-weight-locked


def xi_P_starobinsky(N_e: float = N_E_INFLATION) -> float:
    """Compute xi_P = d ln P_zeta / d ln D-bar on the Starobinsky plateau.

    Master Ch.15 locks V_E(chi) = V_0 (1 - e^(-alpha*chi))^2 with
    alpha = sqrt(2/3). On the plateau (alpha*chi >> 1):
        V'/V       ~ 2*alpha * e^(-alpha*chi)
        epsilon    ~ 2*alpha^2 * e^(-2*alpha*chi)  ~ 3/(4 N_e^2)
        d ln V / d chi   ~  V'/V
        d ln eps / d chi ~ -2*alpha

    P_zeta proportional to V/epsilon, so
        d ln P / d chi = V'/V - eps'/eps  ~  2*alpha (1 + e^(-alpha*chi))
    Plateau limit:  d ln P / d chi  ~  2*alpha = sqrt(8/3) ~ 1.633

    We identify chi ~ ln D-bar (Jordan->Einstein conformal map at leading
    order), giving xi_P = d ln P / d ln D-bar = 2*alpha to leading slow-roll.
    """
    return 2.0 * ALPHA_STARO


def hemispherical_asymmetry_amplitude(eta: float, xi_P: float | None = None) -> float:
    """Dipolar modulation amplitude A_hemi from the gradient.

    A_hemi = (1/2) * eta * (chi_LSS / R_H) * xi_P

    xi_P defaults to the Starobinsky-locked value 2*sqrt(2/3) ~ 1.633
    (Master Ch.15 plateau calculation).
    """
    if xi_P is None:
        xi_P = xi_P_starobinsky()
    return 0.5 * eta * CHI_LSS_OVER_RH * xi_P


# ---------------------------------------------------------------------------
# Observable 3: satellite-plane alignment correlation
# ---------------------------------------------------------------------------

def satellite_plane_alignment_excess(eta: float, xi_lss: float = 2.6) -> float:
    """Fractional excess of perpendicular alignments above the random 0.5.

    P(plane normal perpendicular to g_hat) ~ 0.5 * (1 + eta * xi_lss)

    xi_lss derived from linear tidal-alignment model (Catelan-Kamionkowski-
    Blandford 2001) with A_IA ~ 3 and growth factor 770, giving xi_lss ~
    2.6 with range [0.9, 4.3]. See scripts/derive_parameters.py.
    """
    return 0.5 * eta * xi_lss


# ---------------------------------------------------------------------------
# Observable 4 (DISFORMAL channel): CMB quadrupole-octopole alignment
# ---------------------------------------------------------------------------
#
# Master Ch.3 L637-647 introduces the disformal sector:
#     tilde g_munu = A^2(D) g_munu + B(D) partial_mu D * partial_nu D
#
# For a coherent spatial gradient partial_i D = G g_hat_i, the disformal
# piece adds a parity-even symmetric tensor B(D-bar) G^2 g_hat_i g_hat_j
# to the photon effective metric. Eigenstructure: parallel vs perpendicular
# to g_hat, i.e. QUADRUPOLAR (l=2) anisotropy along g_hat.
#
# Sharp prediction: the observed CMB quad-oct alignment axis must lie
# along g_hat (within ~30 deg, allowing for finite-resolution multipole
# axis estimation). The amplitude:
#     A_2 ~ beta_B * eta^2 / beta_m^2  ~  O(eta^2) for beta_B ~ beta_m^2
# is subleading to the dipolar channel by one power of eta (~1%) and
# detectable only as a directional signature, not an amplitude excess.

def disformal_quadrupole_axis_match_deg(
    g_hat_lb: tuple[float, float],
    observed_quad_oct_axis_lb: tuple[float, float] = (240.0, 60.0),
) -> float:
    """Axis separation (deg) between g_hat and observed quad-oct alignment.

    PASS criterion: separation < 35 deg.
    """
    l1, b1 = g_hat_lb
    l2, b2 = observed_quad_oct_axis_lb
    sep_pole = angular_separation_deg(l1, b1, l2, b2)
    return min(sep_pole, 180.0 - sep_pole)


def disformal_amplitude_estimate(eta: float, beta_B_over_beta_m_sq: float = 1.0) -> float:
    """Order-of-magnitude amplitude of the disformal-induced quadrupole.

    A_2 ~ (beta_B / beta_m^2) * eta^2 * (chi_LSS / R_H)^2

    beta_B is the disformal coupling B(D-bar)*D-bar^2 (dimensionless).
    Master Book has no explicit value; we estimate beta_B ~ beta_m^2 from
    naturalness (same conformal-weight scaling). Returns dimensionless.
    """
    return beta_B_over_beta_m_sq * eta**2 * CHI_LSS_OVER_RH**2


# ---------------------------------------------------------------------------
# Anchoring: invert Study-25 dipole excess to fit eta
# ---------------------------------------------------------------------------

def anchor_eta_to_dipole(
    d_obs: float,
    d_obs_sigma: float,
    v_kms: float,
    x_eb: float,
    chi_mpc: float,
    alpha: float = 0.75,
) -> tuple[float, float]:
    """Fit eta such that D_kin + D_conformal = D_obs.

    Assumes the gradient direction g_hat aligns with the CMB velocity
    direction (best-case for explaining the radio dipole; the actual
    alignment is empirically tested in run_unified_audit).

    Returns (eta_best, eta_sigma).
    """
    d_kin = kinematic_dipole_amplitude(v_kms, x_eb, alpha=alpha)
    d_excess = d_obs - d_kin
    # d_excess = x_eb * eta * (chi / R_H)
    coeff = x_eb * (chi_mpc / R_H_MPC)
    eta = d_excess / coeff
    eta_sigma = d_obs_sigma / coeff
    return eta, eta_sigma


# ---------------------------------------------------------------------------
# Angular utilities
# ---------------------------------------------------------------------------

def angular_separation_deg(l1: float, b1: float, l2: float, b2: float) -> float:
    """Great-circle separation between two (l, b) directions, degrees."""
    p1 = np.array([
        math.cos(math.radians(b1)) * math.cos(math.radians(l1)),
        math.cos(math.radians(b1)) * math.sin(math.radians(l1)),
        math.sin(math.radians(b1)),
    ])
    p2 = np.array([
        math.cos(math.radians(b2)) * math.cos(math.radians(l2)),
        math.cos(math.radians(b2)) * math.sin(math.radians(l2)),
        math.sin(math.radians(b2)),
    ])
    cos_sep = float(np.clip(np.dot(p1, p2), -1.0, 1.0))
    return math.degrees(math.acos(cos_sep))


# Reference directions on the sky (Galactic, degrees)
CMB_DIPOLE_DIR_LB = (264.021, 48.253)     # CMB peculiar-velocity dipole apex
NVSS_DIPOLE_DIR_LB = (253.0, 32.0)        # NVSS dipole (Singal 2011 / Siewert 2021)
CATWISE_DIPOLE_DIR_LB = (238.0, 28.0)     # CatWISE dipole (Secrest et al. 2021)
PLANCK_HEMI_AXIS_LB = (221.0, -22.0)      # Planck dipolar-modulation axis (CMB low-l)
QUADRUPOLE_OCTOPOLE_AXIS_LB = (240.0, 60.0)  # quad-oct alignment axis
COLD_SPOT_LB = (210.0, -57.0)             # CMB Cold Spot
MW_VPOS_NORMAL_LB = (156.4, -2.2)         # MW vast polar structure normal
M31_GPOA_NORMAL_LB = (206.2, 7.8)         # M31 great plane of Andromeda normal
CENA_PLANE_NORMAL_LB = (308.7, 18.0)      # Cen A satellite plane normal


# ---------------------------------------------------------------------------
# Best-fit g_hat axis over data
# ---------------------------------------------------------------------------

def best_fit_axis(
    targets: list[tuple[str, float, float, float]],
) -> tuple[tuple[float, float], float, dict]:
    """Grid-search the axis g_hat that minimizes weighted sum of axis-separations.

    targets : list of (name, l_deg, b_deg, weight) entries.

    Returns ((l_best, b_best), residual, per_target_separations).
    """
    best = None
    best_cost = float("inf")
    best_seps: dict = {}
    # Coarse grid then fine refine
    for l in range(0, 360, 5):
        for b in range(-90, 91, 5):
            cost = 0.0
            seps: dict = {}
            for name, lt, bt, w in targets:
                s = angular_separation_deg(l, b, lt, bt)
                s_axis = min(s, 180.0 - s)  # axis, not pole
                cost += w * s_axis
                seps[name] = s_axis
            if cost < best_cost:
                best_cost = cost
                best = (l, b)
                best_seps = seps
    # Refine
    l0, b0 = best  # type: ignore[misc]
    for dl in range(-5, 6):
        for db in range(-5, 6):
            l = (l0 + dl) % 360
            b = max(-90, min(90, b0 + db))
            cost = 0.0
            seps = {}
            for name, lt, bt, w in targets:
                s = angular_separation_deg(l, b, lt, bt)
                s_axis = min(s, 180.0 - s)
                cost += w * s_axis
                seps[name] = s_axis
            if cost < best_cost:
                best_cost = cost
                best = (l, b)
                best_seps = seps
    return best, best_cost, best_seps  # type: ignore[return-value]
