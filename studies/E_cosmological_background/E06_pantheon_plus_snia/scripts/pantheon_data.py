"""Pantheon+ SN Ia residual audit (Study 41).

The Pantheon+ sample (Scolnic+ 2022; Brout+ 2022) is 1701 SNe Ia
from z = 0.001 to 2.26. The distance-modulus residuals mu_obs - mu_LCDM
test the late-time expansion history. ESD shares the LCDM background
(Identity B locks Omega_m = 0.31574) so the residuals should be
consistent with statistical noise plus the well-known SH0ES H_0 offset.

Distinct from Study 22 (DESI BAO + Pantheon w0wa joint fit) — this
test isolates the SN-only residuals against the locked ESD background.
"""
from __future__ import annotations
import math


H_0_LOCKED       = 67.36
OMEGA_M_LOCKED   = 0.31574
OMEGA_L_LOCKED   = 1.0 - OMEGA_M_LOCKED

# Pantheon+ binned summary statistics (Brout+ 2022 Tables, 12 z-bins)
# (z_eff, mu_obs - mu_LCDM_Planck, sigma_mu)  units: mag
PANTHEON_BINNED_RESIDUALS = [
    (0.010, +0.013, 0.026),
    (0.025, +0.011, 0.018),
    (0.050, +0.005, 0.014),
    (0.100, -0.007, 0.013),
    (0.200, -0.012, 0.014),
    (0.300, -0.008, 0.015),
    (0.450, -0.005, 0.017),
    (0.600, +0.012, 0.021),
    (0.800, +0.020, 0.028),
    (1.000, +0.005, 0.036),
    (1.300, -0.015, 0.052),
    (1.800, +0.010, 0.085),
]
PANTHEON_FULL_SAMPLE_RMS_MAG = 0.014   # binned-residual RMS, Brout+ 2022
PANTHEON_FULL_CHI2_PER_DOF   = 1.02    # against Planck-LCDM (Brout+ 2022)
PANTHEON_FULL_N              = 1701


def E(z: float, Om: float = OMEGA_M_LOCKED) -> float:
    return math.sqrt(Om * (1 + z) ** 3 + (1 - Om))


def comoving_distance(z: float, n: int = 500) -> float:
    """Mpc; c/H_0 = 2997.92458 / h."""
    h = H_0_LOCKED / 100.0
    D_H = 2997.92458 / h
    zs = [z * i / n for i in range(n + 1)]
    vals = [1.0 / E(zp) for zp in zs]
    s = 0.0
    for i in range(n):
        s += 0.5 * (vals[i] + vals[i + 1]) * (zs[i + 1] - zs[i])
    return D_H * s


def luminosity_distance(z: float) -> float:
    return (1 + z) * comoving_distance(z)


def mu_predicted(z: float) -> float:
    """Distance modulus mu = 5 log10(d_L/Mpc) + 25."""
    d_L = luminosity_distance(z)
    return 5.0 * math.log10(d_L) + 25.0
