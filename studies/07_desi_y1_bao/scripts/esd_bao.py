"""Flat-LCDM BAO observables (D_M, D_H, D_V) and the Aubourg+ 2015
fitting formula for the sound horizon r_d.

We deliberately stay closed-form so Study 07 has no CLASS/CAMB
dependency. The fitting-formula r_d agrees with CAMB to ~0.3% over
the Planck-favored region (Aubourg et al. 2015, PRD 92, 123516,
Eq. 16); this is well below the DESI Y1 statistical precision on
individual D_M/r_d, D_H/r_d data points (typically 1-3%).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

import esd_core as ESD

C_KM_S: float = 299_792.458    # km/s


@dataclass(frozen=True)
class Cosmo:
    H0:      float   # km/s/Mpc
    Omega_m: float
    Omega_b: float

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
    def Omega_Lambda(self) -> float:
        # We absorb Omega_r into Omega_m at z=0 (negligible <1e-4 effect on
        # BAO distances); flat LCDM with the framework's Identity-A split.
        return 1.0 - self.Omega_m


def H_of_z(c: Cosmo, z: float) -> float:
    """km/s/Mpc -- flat LCDM ignoring radiation (BAO-relevant z range)."""
    return c.H0 * math.sqrt(c.Omega_m * (1.0 + z) ** 3 + c.Omega_Lambda)


def D_H(c: Cosmo, z: float) -> float:
    """Hubble distance c/H(z) in Mpc."""
    return C_KM_S / H_of_z(c, z)


def D_C(c: Cosmo, z: float) -> float:
    """Comoving line-of-sight distance, Mpc."""
    val, _ = quad(lambda zp: 1.0 / H_of_z(c, zp), 0.0, z, epsabs=0, epsrel=1e-9)
    return C_KM_S * val


def D_M(c: Cosmo, z: float) -> float:
    """Transverse comoving distance (flat universe = D_C), Mpc."""
    return D_C(c, z)


def D_V(c: Cosmo, z: float) -> float:
    """Volume-averaged distance, Mpc."""
    return (z * D_M(c, z) ** 2 * D_H(c, z)) ** (1.0 / 3.0)


def r_d_aubourg2015(c: Cosmo, omega_nu: float = 0.0006) -> float:
    """Sound horizon at the drag epoch (Mpc).

    Aubourg+ 2015 (PRD 92, 123516) Eq. 16 fitting formula, calibrated
    to CAMB to ~0.3% over the Planck-favored region. Default omega_nu
    corresponds to one massive neutrino at the minimum-mass threshold.
    """
    return (
        55.154
        * math.exp(-72.3 * (omega_nu + 0.0006) ** 2)
        / (c.omega_m ** 0.25351 * c.omega_b ** 0.12807)
    )


# --------------------- ESD framework cosmologies --------------------------
def cosmo_esd_primary(H0: float = 67.36) -> Cosmo:
    """PRIMARY reading: Omega_b matched to Planck."""
    return Cosmo(H0=H0, Omega_m=ESD.OMEGA_M_LOCK, Omega_b=ESD.OMEGA_B_INPUT)


def cosmo_esd_closure_pool(H0: float = 67.36) -> Cosmo:
    """CLOSURE-POOL reading: Omega_b from c alone (zero-parameter)."""
    return Cosmo(H0=H0, Omega_m=ESD.OMEGA_M_LOCK, Omega_b=ESD.OMEGA_B_LOCK)


def cosmo_planck_lcdm(H0: float = 67.36, Omega_m: float = 0.3158,
                       Omega_b: float = 0.04930) -> Cosmo:
    """Planck 2018 baseline LCDM for sanity comparison."""
    return Cosmo(H0=H0, Omega_m=Omega_m, Omega_b=Omega_b)
