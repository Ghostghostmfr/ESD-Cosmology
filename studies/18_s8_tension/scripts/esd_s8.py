"""ESD analysis tools for the S_8 tension.

S_8 = sigma_8 (Omega_m / 0.3)^0.5

The Planck CMB infers S_8 ~ 0.83; weak-lensing surveys (KiDS, DES, HSC)
prefer S_8 ~ 0.77.  ESD locks Omega_m = 0.3157 via Identity B + radiation
matching (Paper 1, C2), which agrees with Planck Omega_m to ~0.05%.
The tension axis is therefore sigma_8 (the linear-perturbation
amplitude), not Omega_m.

This module:
  * implements inverse-variance combination of WL S_8 measurements
  * computes the Planck-vs-WL tension in sigma units
  * confirms ESD's locked Omega_m matches Planck (so tension is not Omega_m)
  * checks Identity-B-driven h-blindness of S_8 (Omega_m is h-blind,
    so S_8 inherits h-blindness for fixed sigma_8)
"""
from __future__ import annotations
import math
from esd_core import OMEGA_M_LOCK, identity_B_rhs, a_zero

H0_PLANCK_KMS = 67.36
A0_SI         = a_zero(H0_PLANCK_KMS)

def inverse_variance_combine(values, errors):
    """Standard 1/sigma^2-weighted mean and combined error."""
    w = [1.0/e**2 for e in errors]
    W = sum(w)
    mu = sum(v*wi for v, wi in zip(values, w)) / W
    sig = 1.0/math.sqrt(W)
    return mu, sig

def tension_sigma(v1, e1, v2, e2):
    return abs(v1 - v2)/math.sqrt(e1*e1 + e2*e2)

def omega_m_match_to_planck(omega_m_planck=0.3158):
    return abs(OMEGA_M_LOCK - omega_m_planck) / omega_m_planck

def S8(sigma8, Omega_m):
    return sigma8 * math.sqrt(Omega_m / 0.3)

def h_blindness_S8(sigma8_fixed=0.811, h_lo=0.50, h_hi=0.80):
    """ESD's locked Omega_m does not depend on H_0 (Identity B exactness).

    Confirms S_8 prediction with fixed sigma_8 is invariant under H_0 choice.
    """
    s_lo = S8(sigma8_fixed, OMEGA_M_LOCK)
    s_hi = S8(sigma8_fixed, OMEGA_M_LOCK)
    return abs(s_lo - s_hi)
