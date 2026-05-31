"""Observed primordial abundances and Pitrou+ 2018 fit anchor."""
from __future__ import annotations

# Cooke+ 2018 (ApJ 855, 102): D/H = (2.527 +/- 0.030) x 10^-5
DH_OBS:     float = 2.527e-5
DH_OBS_ERR: float = 0.030e-5

# Aver+ 2021 (JCAP 03, 027): Yp = 0.2453 +/- 0.0034
YP_OBS:     float = 0.2453
YP_OBS_ERR: float = 0.0034

# Pitrou+ 2018 fit anchor (eta_10 = 6.143, N_eff = 3.045).
ETA10_FIT_ANCHOR: float = 6.143
DH_FIT_AT_ANCHOR: float = 2.527e-5
YP_FIT_AT_ANCHOR: float = 0.24709

DH_ETA_EXPONENT: float = -1.598     # d ln(D/H) / d ln(eta_10) at anchor
YP_ETA_SLOPE:    float = 0.0017     # Yp shift per dex in eta_10
