"""Cosmic chronometers H(z) (Study 42).

Differential dating of passively evolving early-type galaxies
(Jimenez & Loeb 2002) gives model-independent H(z) from dz/dt of
the matched-age galaxy ensemble. Distinct from BAO, SN, and CMB
probes: requires no cosmological model assumption.

Moresco+ compilation: ~32 H(z) points spanning z = 0.07-2.0.
"""
from __future__ import annotations
import math


H_0_LOCKED       = 67.36
OMEGA_M_LOCKED   = 0.31574

# (z, H_obs km/s/Mpc, sigma, citation_short)
CHRONOMETER_DATA = [
    (0.07,  69.0,  19.6,  "Zhang+ 2014"),
    (0.09,  69.0,  12.0,  "Simon+ 2005"),
    (0.12,  68.6,  26.2,  "Zhang+ 2014"),
    (0.17,  83.0,  8.0,   "Simon+ 2005"),
    (0.179, 75.0,  4.0,   "Moresco+ 2012"),
    (0.199, 75.0,  5.0,   "Moresco+ 2012"),
    (0.2,   72.9,  29.6,  "Zhang+ 2014"),
    (0.27,  77.0,  14.0,  "Simon+ 2005"),
    (0.28,  88.8,  36.6,  "Zhang+ 2014"),
    (0.352, 83.0,  14.0,  "Moresco+ 2012"),
    (0.3802,83.0,  13.5,  "Moresco+ 2016"),
    (0.4,   95.0,  17.0,  "Simon+ 2005"),
    (0.4004,77.0,  10.2,  "Moresco+ 2016"),
    (0.4247,87.1,  11.2,  "Moresco+ 2016"),
    (0.4497,92.8,  12.9,  "Moresco+ 2016"),
    (0.47,  89.0,  49.6,  "Ratsimbazafy+ 2017"),
    (0.4783,80.9,  9.0,   "Moresco+ 2016"),
    (0.48,  97.0,  62.0,  "Stern+ 2010"),
    (0.593, 104.0, 13.0,  "Moresco+ 2012"),
    (0.68,  92.0,  8.0,   "Moresco+ 2012"),
    (0.781, 105.0, 12.0,  "Moresco+ 2012"),
    (0.875, 125.0, 17.0,  "Moresco+ 2012"),
    (0.88,  90.0,  40.0,  "Stern+ 2010"),
    (0.9,   117.0, 23.0,  "Simon+ 2005"),
    (1.037, 154.0, 20.0,  "Moresco+ 2012"),
    (1.3,   168.0, 17.0,  "Simon+ 2005"),
    (1.363, 160.0, 33.6,  "Moresco 2015"),
    (1.43,  177.0, 18.0,  "Simon+ 2005"),
    (1.53,  140.0, 14.0,  "Simon+ 2005"),
    (1.75,  202.0, 40.0,  "Simon+ 2005"),
    (1.965, 186.5, 50.4,  "Moresco 2015"),
    (2.0,   222.0, 7.0,   "Borghi+ 2022"),
]


def H_z_LCDM(z: float) -> float:
    """ESD = LCDM background H(z) at locked params."""
    return H_0_LOCKED * math.sqrt(
        OMEGA_M_LOCKED * (1 + z) ** 3 + (1 - OMEGA_M_LOCKED)
    )
