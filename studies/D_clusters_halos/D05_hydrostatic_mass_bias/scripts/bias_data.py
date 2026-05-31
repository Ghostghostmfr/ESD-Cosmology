"""Hydrostatic mass bias 1 - b_H (Study 43).

Planck SZ-cluster cosmology measures the dimensionless bias parameter
(1 - b_H) = M_X/M_true where M_X is the X-ray hydrostatic mass and
M_true is the WL/dynamical mass. Planck reports needing
(1 - b_H) ~ 0.58 to reconcile SZ cluster counts with Planck-CMB
sigma_8. WL programs (CCCP, WtG, LoCuSS, CLASH, HSC-XXL) measure
1 - b_H ~ 0.7-0.85.

In ESD, R(u) acts on virialized bound subsystems but cannot rescue
the gap unilaterally - it's the same sigma_8 / cluster-tension family
owned by Study 18 (WL+galaxy-bias pipeline systematics).
"""
from __future__ import annotations

H_0_LOCKED       = 67.36
OMEGA_M_LOCKED   = 0.31574
SIGMA_8_LOCKED   = 0.8111

# (program, 1-b_H_measured, sigma, citation)
BIAS_MEASUREMENTS = [
    ("CCCP (Hoekstra+ 2015)",                  0.76,  0.09,  "Hoekstra+ 2015"),
    ("WtG (von der Linden+ 2014)",             0.69,  0.07,  "vdL+ 2014"),
    ("LoCuSS (Smith+ 2016)",                   0.95,  0.04,  "Smith+ 2016"),
    ("CLASH (Penna-Lima+ 2017)",               0.73,  0.10,  "Penna-Lima+ 2017"),
    ("Planck-CCCP joint (Planck 2016)",        0.78,  0.092, "Planck 2016 XXIV"),
    ("APEX-SZ + WtG (Klein+ 2019)",            0.76,  0.14,  "Klein+ 2019"),
    ("HSC + Planck (Medezinski+ 2018)",        0.80,  0.14,  "Medezinski+ 2018"),
    ("SPT-SZ + WL (Dietrich+ 2019)",           0.83,  0.10,  "Dietrich+ 2019"),
    ("eROSITA-DE WL (Grandis+ 2024)",          0.84,  0.06,  "Grandis+ 2024"),
]

# Planck SZ requires this value to match Planck CMB sigma_8
PLANCK_SZ_REQUIRED_1MB = 0.58
PLANCK_SZ_SIGMA        = 0.04
