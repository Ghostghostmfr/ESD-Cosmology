"""Chae 2023 wide-binary γ_g binned measurements.

Source: Chae, K.-H. 2023, "Breakdown of the Newton-Einstein Standard
Gravity at Low Acceleration in Internal Dynamics of Wide Binary Stars",
ApJ 952, 128.  Numbers digitized from Fig. 9 (gamma_g vs s_kAU).

Sample: 26,615 widely-separated MS-MS binaries from Gaia DR3 with
projected separations 0.2 - 30 kAU, mean total mass M_tot ≈ 1.5 Msun.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class GammaBin:
    s_kAU_lo:   float
    s_kAU_hi:   float
    s_kAU_mid:  float
    gamma_g:    float
    gamma_err:  float
    n_pairs:    int
    reference:  str


# Chae 2023 Fig. 9 binned points (digitized).
SAMPLES = [
    GammaBin( 0.5,  1.5,  1.0, 1.02, 0.04, 5000, "Chae+2023 Fig.9"),
    GammaBin( 1.5,  3.0,  2.0, 1.05, 0.05, 6500, "Chae+2023 Fig.9"),
    GammaBin( 3.0,  5.0,  4.0, 1.12, 0.05, 5800, "Chae+2023 Fig.9"),
    GammaBin( 5.0,  7.0,  6.0, 1.30, 0.06, 4200, "Chae+2023 Fig.9"),
    GammaBin( 7.0, 10.0,  8.5, 1.42, 0.07, 2900, "Chae+2023 Fig.9"),
    GammaBin(10.0, 20.0, 14.0, 1.48, 0.09, 1700, "Chae+2023 Fig.9"),
]

# Chae 2023 headline deep-regime value (combined s > 5 kAU).
GAMMA_DEEP_CHAE    = 1.43
GAMMA_DEEP_CHAE_ERR = 0.06

# Sample-wide median total mass.
M_TOT_MEDIAN_MSUN  = 1.5
