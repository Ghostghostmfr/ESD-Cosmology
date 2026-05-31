"""DES/KiDS/Planck mu_0, Sigma_0 phenomenological MG parameters (Study 46).

The phenomenological MG framework (Zhao+ 2009; Pogosian & Silvestri
2008) modifies the linear-regime Poisson and lensing equations:

    k^2 Psi = -4 pi G a^2 (1 + mu_0) rho_m delta
    k^2 (Psi + Phi) = -8 pi G a^2 (1 + Sigma_0) rho_m delta

LCDM has mu_0 = Sigma_0 = 0. Surveys (Planck 2018, DES Y3, KiDS-1000)
fit these to their data and report constraints.

ESD on linear modes = LCDM exactly (Study 19); therefore ESD predicts
mu_0 = Sigma_0 = 0 structurally - no free parameter to fit.
"""
from __future__ import annotations

# (survey, mu_0 mean, mu_0 sigma, Sigma_0 mean, Sigma_0 sigma, citation)
PHENO_MG_MEASUREMENTS = [
    ("Planck 2018 TT,TE,EE+lowE+lensing+BAO",
     -0.05, 0.25, +0.03, 0.05, "Planck 2020 VI"),
    ("DES Y3 3x2pt + Planck CMB",
     -0.04, 0.32, +0.04, 0.13, "DES Y3 MG 2023"),
    ("KiDS-1000 cosmic shear + Planck",
     +0.02, 0.27, -0.01, 0.10, "Asgari+ 2021 / Troester+ 2021"),
    ("DES Y1 shear + Planck",
     -0.20, 0.40, +0.04, 0.15, "Joudaki+ 2018"),
    ("CFHTLenS + Planck 2015",
     -0.10, 0.35, -0.02, 0.12, "Joudaki+ 2017"),
]

ESD_MU0    = 0.0
ESD_SIGMA0 = 0.0
