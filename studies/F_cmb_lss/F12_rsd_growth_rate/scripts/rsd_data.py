"""RSD f*sigma_8(z) compilation (Study 39).

Redshift-space distortions probe the linear growth rate via the
quadrupole/hexadecapole of the galaxy correlation function. The
combination f(z)*sigma_8(z) is extracted from multipole fits and is
the canonical model-independent growth probe.

By Study 19 applicability theorem (linear modes excluded from R(u)),
ESD predicts f(z)*sigma_8(z) identical to LCDM at locked
Omega_m = 0.31574 and sigma_8(0) = 0.8111.

Data: 17 published f*sigma_8 measurements spanning z = 0.02 to 1.94.
"""
from __future__ import annotations

OMEGA_M0_LOCKED = 0.31574
SIGMA_8_LOCKED  = 0.8111

# (label, z_eff, fsigma8_obs, sigma, citation)
FSIGMA8_MEASUREMENTS = [
    ("6dFGS",          0.067, 0.423, 0.055, "Beutler+ 2012, MNRAS 423"),
    ("SDSS MGS",       0.150, 0.490, 0.145, "Howlett+ 2015, MNRAS 449"),
    ("GAMA",           0.180, 0.360, 0.090, "Blake+ 2013, MNRAS 436"),
    ("GAMA",           0.380, 0.440, 0.060, "Blake+ 2013, MNRAS 436"),
    ("BOSS DR12 LOWZ", 0.380, 0.497, 0.045, "Alam+ 2017, MNRAS 470 (DR12 consensus)"),
    ("BOSS DR12 CMASS",0.510, 0.458, 0.038, "Alam+ 2017, MNRAS 470"),
    ("BOSS DR12 high-z",0.610, 0.436, 0.034, "Alam+ 2017, MNRAS 470"),
    ("WiggleZ",        0.440, 0.413, 0.080, "Blake+ 2012, MNRAS 425"),
    ("WiggleZ",        0.600, 0.390, 0.063, "Blake+ 2012, MNRAS 425"),
    ("WiggleZ",        0.730, 0.437, 0.072, "Blake+ 2012, MNRAS 425"),
    ("VIPERS PDR-2",   0.600, 0.550, 0.120, "Pezzotta+ 2017, A&A 604"),
    ("VIPERS PDR-2",   0.860, 0.400, 0.110, "Pezzotta+ 2017, A&A 604"),
    ("eBOSS LRG",      0.700, 0.470, 0.044, "Bautista+ 2021, MNRAS 500"),
    ("eBOSS ELG",      0.850, 0.315, 0.095, "de Mattia+ 2021, MNRAS 501"),
    ("eBOSS QSO",      1.480, 0.462, 0.045, "Hou+ 2021, MNRAS 500 (DR16 QSO)"),
    ("DESI Y1 LRG",    0.510, 0.450, 0.030, "DESI Collab 2024, JCAP (Y1 full-shape)"),
    ("DESI Y1 ELG",    1.317, 0.439, 0.048, "DESI Collab 2024, JCAP (Y1 full-shape)"),
]
