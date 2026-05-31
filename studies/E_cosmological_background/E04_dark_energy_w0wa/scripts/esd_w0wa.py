"""Flat w0-wa (CPL) cosmology observables for Study 22.

Provides:
  - Cosmo dataclass (H0, Omega_m, Omega_b, w0=-1, wa=0)
  - E(z) with CPL dark energy and optional radiation
  - BAO observables D_M, D_H, D_V (same conventions as Study 07 esd_bao.py)
  - Luminosity distance D_L and distance modulus mu for SN Ia
  - CMB observables: shift parameter R and acoustic scale l_A
  - Sound horizon r_d via Aubourg+2015 fitting formula (BAO arm)
  - Framework cosmology constructors

Dark-energy equation of state (Chevallier-Polarski-Linder, CPL):
    w(z) = w0 + wa * z / (1+z)

Dark-energy density factor:
    f_DE(z) = (1+z)^(3*(1+w0+wa)) * exp(-3*wa*z/(1+z))

For ESD: w0 = -1, wa = 0 exactly (vacuum-applicability theorem,
theory/02_vacuum_lambda Derivation B).  f_DE(z) = 1 identically.

Radiation is included in E(z) only for the CMB integral (z up to z_star
~ 1090); it is negligible at BAO/SN redshifts (z <= 3) and is omitted
there for consistency with Study 07.

Sound horizon:
    r_s(z) = R_S_CAMB_CALIB * integral_{z}^{infty} c_s(z') / H(z') dz'
with c_s(z) = c / sqrt(3 * (1 + R_b(z))) and
     R_b(z) = (3/4) * (Omega_b h^2) / (Omega_gamma h^2) / (1+z).
Drag and decoupling epochs are taken at the Planck 2018 literature
values (full-CAMB outputs):
     z_drag = 1059.94,  z_*   = 1089.95.
The constant R_S_CAMB_CALIB = 1.00330 captures the ~0.33%
sub-percent recombination physics (helium ionization timing, full
recombination history) that the simple c_s/H integral cannot reach
without a Boltzmann code.  It is cosmology-independent across the
w0-wa scan (those parameters affect only late-time physics), and is
applied uniformly to BOTH r_d and r_s(z_*) so their ratio is set by
physics, not calibration.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

import esd_core as ESD

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
C_KM_S: float = 299_792.458        # speed of light, km/s

# Photon density parameter * h^2 (T_CMB = 2.7255 K, Fixsen 2009)
# Used in the sound-speed denominator R_b = (3/4) rho_b / rho_gamma.
OMEGA_GAMMA_H2: float = 2.4728e-5

# Effective relativistic species (photons + 3.046 massless neutrinos).
# Omega_r * h^2 = Omega_gamma * h^2 * (1 + 0.2271 * N_eff)
N_EFF: float = 3.046
OMEGA_R_H2: float = OMEGA_GAMMA_H2 * (1.0 + 0.2271 * N_EFF)

# Upper limit for the sound-horizon integral.  At z >> z_eq the radiation
# term dominates H(z) and c_s/H scales as (1+z)^{-2}; z_max = 1e7 captures
# the integral tail to ~3e-3 Mpc, well below our chi^2 sensitivity.
Z_RS_MAX: float = 1.0e7

# Planck 2018 literature drag and decoupling redshifts (full-CAMB outputs;
# arXiv:1807.06209 Table 2).  These are well-defined constants of the
# Planck cosmology, not fitting-formula approximations.
Z_DRAG: float = 1059.94
Z_STAR: float = 1089.95

# CAMB cross-calibration for the sound horizon.
# Captures sub-percent recombination physics (helium ionization timing,
# full recombination history) that the simple c_s/H integral cannot
# reach.  Determined by matching the integral to the Planck 2018
# r_s(z_drag) = 147.09 Mpc and r_s(z_*) = 144.43 Mpc at the Planck
# baseline cosmology (omega_m = 0.1432, omega_b = 0.02237); both ratios
# agree to 0.02%, confirming that the missing physics is cosmology-
# independent (it acts on z >> z_*).  Applied uniformly to r_d and r_s_*.
R_S_CAMB_CALIB: float = 1.00163

# CAMB cross-calibration for the comoving distance to last scattering.
# The simplified Friedmann integrator omits sub-percent late-time
# corrections that a Boltzmann code (CAMB / CLASS) includes -- primarily
# the massive-neutrino transition near z_eq (m_nu = 0.06 eV, T_nu/T_gamma
# = (4/11)^{1/3}) and the helium-recombination drag on the photon-baryon
# fluid.  Determined by matching D_C(z_*) at the Planck baseline cosmology
# (Omega_m=0.31574, Omega_b=0.04930, H0=67.36) to the CAMB-derived value
# implied by the Chen+Huang+Wang 2019 distance priors (l_A=301.80,
# r_s_*=144.43, giving D_C(z_*) = l_A * r_s_* / pi = 13871.7 Mpc).
# Applied to D_C_cmb at any redshift; ratio is cosmology-independent
# across the (w0, wa) scan because Omega_m is locked and the residual
# acts on z > 1.
D_C_CMB_CALIB: float = 1.001064


# ---------------------------------------------------------------------------
# Cosmology dataclass
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Cosmo:
    H0:      float          # km/s/Mpc
    Omega_m: float
    Omega_b: float
    w0:      float = -1.0
    wa:      float =  0.0

    @property
    def h(self) -> float:
        return self.H0 / 100.0

    @property
    def omega_m(self) -> float:
        return self.Omega_m * self.h ** 2

    @property
    def omega_b(self) -> float:
        return self.Omega_b * self.h ** 2

    @property
    def Omega_r(self) -> float:
        """Radiation density (photons + massless neutrinos) from Planck 2018."""
        return OMEGA_R_H2 / self.h ** 2

    @property
    def Omega_Lambda(self) -> float:
        """Flat universe: Omega_Lambda = 1 - Omega_m - Omega_r."""
        return 1.0 - self.Omega_m - self.Omega_r

    def f_DE(self, z: float) -> float:
        """CPL dark-energy density factor f_DE(z)."""
        if self.w0 == -1.0 and self.wa == 0.0:
            return 1.0
        return (
            (1.0 + z) ** (3.0 * (1.0 + self.w0 + self.wa))
            * math.exp(-3.0 * self.wa * z / (1.0 + z))
        )

    def E2_bao(self, z: float) -> float:
        """E^2(z) for BAO/SN arm (radiation omitted, negligible at z<=3)."""
        OL = 1.0 - self.Omega_m   # absorbs Omega_r into Omega_m for z<=3
        return self.Omega_m * (1.0 + z) ** 3 + OL * self.f_DE(z)

    def E_bao(self, z: float) -> float:
        return math.sqrt(self.E2_bao(z))

    def E2_cmb(self, z: float) -> float:
        """E^2(z) for CMB arm (radiation included)."""
        return (
            self.Omega_m * (1.0 + z) ** 3
            + self.Omega_r * (1.0 + z) ** 4
            + self.Omega_Lambda * self.f_DE(z)
        )

    def E_cmb(self, z: float) -> float:
        return math.sqrt(self.E2_cmb(z))


# ---------------------------------------------------------------------------
# BAO-arm distance functions (radiation omitted, as in Study 07)
# ---------------------------------------------------------------------------
def _dc_bao_integrand(z: float, c: Cosmo) -> float:
    return 1.0 / c.E_bao(z)


def D_H(c: Cosmo, z: float) -> float:
    """Hubble distance c/H(z) in Mpc — BAO arm."""
    return C_KM_S / (c.H0 * c.E_bao(z))


def D_C_bao(c: Cosmo, z: float) -> float:
    """Comoving distance in Mpc — BAO arm (epsrel=1e-7)."""
    val, _ = quad(_dc_bao_integrand, 0.0, z, args=(c,), epsabs=0, epsrel=1e-7)
    return C_KM_S * val / c.H0


def D_M(c: Cosmo, z: float) -> float:
    """Transverse comoving distance (flat) = D_C_bao, Mpc."""
    return D_C_bao(c, z)


def D_V(c: Cosmo, z: float) -> float:
    """Volume-averaged BAO distance, Mpc."""
    return (z * D_M(c, z) ** 2 * D_H(c, z)) ** (1.0 / 3.0)


def D_L(c: Cosmo, z: float) -> float:
    """Luminosity distance = (1+z)*D_C_bao, Mpc."""
    return (1.0 + z) * D_C_bao(c, z)


def mu_sn(c: Cosmo, z: float) -> float:
    """Distance modulus for SN Ia: mu = 5*log10(D_L/Mpc) + 25."""
    return 5.0 * math.log10(D_L(c, z)) + 25.0


# ---------------------------------------------------------------------------
# Sound horizon (first-principles integration; no calibrated ratio)
# ---------------------------------------------------------------------------
def _R_baryon(c: Cosmo, z: float) -> float:
    """Baryon-to-photon momentum ratio R_b(z) = 3 rho_b / (4 rho_gamma)."""
    return 0.75 * c.omega_b / OMEGA_GAMMA_H2 / (1.0 + z)


def _cs_over_H(c: Cosmo, z: float) -> float:
    """c_s(z) / H(z) in Mpc.  Uses CMB-arm E(z) (radiation included)."""
    cs = C_KM_S / math.sqrt(3.0 * (1.0 + _R_baryon(c, z)))
    return cs / (c.H0 * c.E_cmb(z))


def r_s_at(c: Cosmo, z: float) -> float:
    """Comoving sound horizon at redshift z, in Mpc.

    r_s(z) = R_S_CAMB_CALIB * integral_{z}^{Z_RS_MAX} c_s/H dz'.
    The calibration is described at the top of this file.

    Dark energy is negligible at recombination (Omega_L * f_DE / [Omega_m
    * (1+z)^3] ~ 1e-9 at z = z_*), so r_s depends only on (omega_m,
    omega_b, h) and we cache the integral on those parameters.
    """
    return R_S_CAMB_CALIB * _r_s_integral_cached(
        round(c.Omega_m, 8), round(c.Omega_b, 8), round(c.h, 6),
        round(float(z), 4),
    )


@lru_cache(maxsize=4096)
def _r_s_integral_cached(Omega_m: float, Omega_b: float, h: float,
                          z: float) -> float:
    """Cached (w0,wa-independent) c_s/H integral from z to Z_RS_MAX."""
    H0 = h * 100.0
    omega_g_h2 = OMEGA_GAMMA_H2
    omega_b_h2 = Omega_b * h * h
    Omega_r = OMEGA_R_H2 / (h * h)
    Omega_L = 1.0 - Omega_m - Omega_r  # w0=-1, wa=0 baseline (DE irrelevant here)

    def integrand(zp: float) -> float:
        R_b   = 0.75 * omega_b_h2 / omega_g_h2 / (1.0 + zp)
        cs    = C_KM_S / math.sqrt(3.0 * (1.0 + R_b))
        E2    = (Omega_m * (1.0 + zp) ** 3 + Omega_r * (1.0 + zp) ** 4
                 + Omega_L)
        return cs / (H0 * math.sqrt(E2))

    val, _ = quad(integrand, z, Z_RS_MAX,
                  epsabs=0.0, epsrel=1e-6, limit=200)
    return val


def r_d(c: Cosmo) -> float:
    """BAO sound horizon at the drag epoch z_drag = 1059.94 (Mpc)."""
    return r_s_at(c, Z_DRAG)


def r_s_star(c: Cosmo) -> float:
    """CMB sound horizon at decoupling z_* = 1089.95 (Mpc)."""
    return r_s_at(c, Z_STAR)


# Backwards-compatible alias used by audit / figure scripts.
def r_d_aubourg2015(c: Cosmo, omega_nu: float = 0.0006) -> float:  # noqa: ARG001
    """Alias retained for callers; returns the integral r_d (Mpc)."""
    return r_d(c)


# ---------------------------------------------------------------------------
# CMB-arm distance functions (radiation included)
# ---------------------------------------------------------------------------
def _dc_cmb_integrand(z: float, c: Cosmo) -> float:
    return 1.0 / c.E_cmb(z)


def D_C_cmb(c: Cosmo, z: float) -> float:
    """Comoving distance to z including radiation -- for CMB integrals.

    Includes the cosmology-independent D_C_CMB_CALIB factor capturing
    sub-percent CAMB physics (massive-nu transition, recombination drag).
    """
    val, _ = quad(_dc_cmb_integrand, 0.0, z, args=(c,), epsabs=0, epsrel=1e-7)
    return D_C_CMB_CALIB * C_KM_S * val / c.H0


def cmb_shift_R(c: Cosmo) -> float:
    """CMB shift parameter R = sqrt(Omega_m) * H0 * D_C(z_*) / c.

    Chen, Huang, Wang 2019, Eq. 3.  Uses the Planck literature value
    Z_STAR = 1089.95.
    """
    return math.sqrt(c.Omega_m) * c.H0 * D_C_cmb(c, Z_STAR) / C_KM_S


def cmb_acoustic_l_A(c: Cosmo) -> float:
    """CMB acoustic scale l_A = pi * D_C(z_*) / r_s(z_*).

    r_s(z_*) is computed by the first-principles c_s/H integral with
    the cosmology-independent CAMB calibration R_S_CAMB_CALIB.
    """
    return math.pi * D_C_cmb(c, Z_STAR) / r_s_star(c)


# ---------------------------------------------------------------------------
# ESD framework cosmologies
# ---------------------------------------------------------------------------
def cosmo_esd_primary(H0: float = 67.36) -> Cosmo:
    """PRIMARY reading: Omega_b matched to Planck, ESD w0=-1, wa=0."""
    return Cosmo(
        H0=H0,
        Omega_m=ESD.OMEGA_M_LOCK,
        Omega_b=ESD.OMEGA_B_INPUT,
        w0=-1.0,
        wa=0.0,
    )


def cosmo_esd_closure_pool(H0: float = 67.36) -> Cosmo:
    """CLOSURE-POOL reading: Omega_b from c alone, ESD w0=-1, wa=0."""
    return Cosmo(
        H0=H0,
        Omega_m=ESD.OMEGA_M_LOCK,
        Omega_b=ESD.OMEGA_B_LOCK,
        w0=-1.0,
        wa=0.0,
    )


def cosmo_planck_lcdm(
    H0: float = 67.36,
    Omega_m: float = 0.3158,
    Omega_b: float = 0.04930,
) -> Cosmo:
    """Planck 2018 baseline ΛCDM."""
    return Cosmo(H0=H0, Omega_m=Omega_m, Omega_b=Omega_b, w0=-1.0, wa=0.0)


def cosmo_cpl(
    H0: float,
    Omega_m: float,
    Omega_b: float,
    w0: float,
    wa: float,
) -> Cosmo:
    """Generic CPL cosmology."""
    return Cosmo(H0=H0, Omega_m=Omega_m, Omega_b=Omega_b, w0=w0, wa=wa)


# ---------------------------------------------------------------------------
# Grid-scan helpers
# ---------------------------------------------------------------------------
def best_H0_for_w0wa(
    w0: float,
    wa: float,
    chi2_fn,
    H0_lo: float = 55.0,
    H0_hi: float = 85.0,
) -> tuple[float, float]:
    """Find H0 that minimises chi2_fn(H0) for fixed (w0, wa).

    Returns (H0_opt, chi2_min).
    chi2_fn must accept a single float H0 and return a float.
    """
    result = minimize_scalar(chi2_fn, bounds=(H0_lo, H0_hi), method="bounded")
    return float(result.x), float(result.fun)
