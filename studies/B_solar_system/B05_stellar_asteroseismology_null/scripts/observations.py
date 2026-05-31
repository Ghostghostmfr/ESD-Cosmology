"""Stellar anchors."""
from __future__ import annotations
G_M3_KG_S2 = 6.67430e-11
M_SUN_KG   = 1.98892e30
R_SUN_M    = 6.957e8
C_KM_S     = 299792.458

# Solar large-frequency separation Delta_nu (Toutain & Frohlich 1992)
DELTA_NU_SUN_MEAS_UHZ: float = 134.91
DELTA_NU_SUN_ERR_UHZ:  float = 0.02
DELTA_NU_SUN_MESA_UHZ: float = 135.0
DELTA_NU_SUN_MESA_ERR: float = 1.0

# Sirius B (Bond+ 2017 ApJ 840 70; Joyce+ 2018)
SIRIUS_B_M_MSUN: float = 1.018
SIRIUS_B_M_ERR:  float = 0.011
SIRIUS_B_R_RSUN: float = 0.00864
SIRIUS_B_R_ERR:  float = 0.00012
SIRIUS_B_VGR_KMS: float = 80.4
SIRIUS_B_VGR_ERR: float = 4.8

# Joyce+ 2018 (MNRAS 481, 2361): GR prediction from full mass profile +
# null geodesic propagation, taking M=1.018 Msun, R=0.00864 Rsun.
SIRIUS_B_VGR_GR_KMS: float = 80.65
SIRIUS_B_VGR_GR_ERR: float = 0.77

# Representative stellar-interior acceleration: solar centre g_eff
# enclosed mass within ~0.1 R_sun is ~0.3 M_sun, r ~ 0.1 R_sun:
G_STELLAR_INTERIOR: float = G_M3_KG_S2 * (0.3 * M_SUN_KG) / (0.1 * R_SUN_M) ** 2
