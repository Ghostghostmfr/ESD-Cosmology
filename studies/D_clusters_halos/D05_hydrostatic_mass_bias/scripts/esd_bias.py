"""ESD prediction for hydrostatic mass bias.

(1 - b_H) is governed by the X-ray ICM physics (turbulence, non-thermal
pressure, accretion) - not the cosmological model directly. ESD shares
LCDM structure formation in the linear regime (Study 19 theorem;
R(u) doesn't act on linear modes), and its R(u) correction to bound
virialized halos is sigma-suppressed at cluster scales relative to
the dominant non-thermal pressure budget. The framework therefore
predicts the WL-measured 1 - b_H ~ 0.75 - 0.85, NOT the Planck-required
0.58. The Planck-SZ gap is the canonical sigma_8 tension owned by
Study 18.
"""
from __future__ import annotations

# WL-program mean (gold-standard channel for ESD comparison)
ESD_PREDICTED_1MB_CENTER = 0.78   # consistent with WL programs
ESD_PREDICTED_1MB_RANGE  = 0.10   # mean +/- range covers WL spread
