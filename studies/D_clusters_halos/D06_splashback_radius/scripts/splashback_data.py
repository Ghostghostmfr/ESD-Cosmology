"""Splashback radius (Study 44).

The splashback radius R_sp marks the outer boundary of the orbiting
halo - the apocenter of recently accreted material. In LCDM, N-body
calibrations (Diemer & Kravtsov 2014; Adhikari+ 2014; More+ 2015)
give R_sp/R_200m = 1.0 - 1.2 for accretion rates 0.5 - 3 (M_dot/M)
per Hubble time.

In fifth-force / chameleon-class MG, enhanced G_eff inside the
unscreened regime SHRINKS R_sp by ~10 - 30% (Adhikari, Sakstein,
Jain et al. 2018). ESD has no fifth-force coupling on linear modes
(Study 19) and inherits LCDM N-body calibration for bound halos.

Measurements: More+ 2016 (SDSS redMaPPer), Baxter+ 2017 (SDSS+DES),
Chang+ 2018 (DES Y1), Shin+ 2019 (ACT-DR4+DES), Murata+ 2020 (HSC).
"""
from __future__ import annotations

# (program, R_sp / R_200m measured, sigma, M_dot category)
SPLASHBACK_MEASUREMENTS = [
    ("More+ 2016 (SDSS redMaPPer)",        0.97, 0.05, "M_dot ~ 1"),
    ("Baxter+ 2017 (SDSS+DES SZ)",          0.94, 0.05, "M_dot ~ 1"),
    ("Chang+ 2018 (DES Y1)",                1.03, 0.07, "M_dot ~ 1"),
    ("Shin+ 2019 (ACT-DR4+DES Y3)",         0.99, 0.06, "M_dot ~ 1"),
    ("Zurcher & More 2019 (HSC weak lens)", 0.96, 0.06, "M_dot ~ 1"),
    ("Murata+ 2020 (HSC + CAMIRA)",         1.05, 0.08, "M_dot ~ 1"),
    ("Contigiani+ 2019 (CCCP+MENeaCS WL)",  1.02, 0.08, "M_dot ~ 1"),
]

# ESD = LCDM N-body prediction (Diemer-Kravtsov fitting form at M_dot ~ 1)
ESD_PREDICTED_RSP_R200M = 1.00
ESD_RSP_THEORY_RANGE    = 0.10   # N-body calibration scatter
