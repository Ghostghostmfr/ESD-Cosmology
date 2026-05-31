"""Observational anchors for Study 30 - Cosmic Void Lensing.

All numbers are quoted from the listed references; no fits.
"""
from __future__ import annotations

# --- HSW universal-profile parameters (Hamaus, Sutter, Wandelt 2014) ----
# Central depth range across the BOSS / SDSS void samples in Hamaus+ 2014
# Tab. 1 (R_v in [10, 80] Mpc/h), bracketing the L*-galaxy void population.
HSW_DELTA_C_RANGE   = (-0.95, -0.70)
# Wall (compensation ridge) amplitude range from the same sample.
HSW_WALL_AMP_RANGE  = ( 0.02,  0.10)
# Wall position in units of R_v (essentially geometric, weak environmental).
HSW_WALL_POS_RV     = 1.10
# HSW shape parameters (alpha, beta) at fiducial scale R_v ~ 25 Mpc/h.
HSW_ALPHA           = 2.0
HSW_BETA            = 8.0
# Interior dimensionless scale r_s / R_v (Hamaus+ 2014 best-fit).
HSW_RS_OVER_RV      = 0.82

# --- DES Y3 void lensing stack (Fang et al. 2019, MNRAS 490, 3573) -------
# Peak tangential shear in dimensionless excess surface density units
# Delta Sigma_t / Sigma_crit-equivalent (their Fig. 8, void radius bin
# 15-25 Mpc/h, stacked over ~ 6300 voids).
# Reported amplitude at R / R_v ~ 1 in units of h Msun/pc^2:
DES_Y3_DELTA_SIGMA_PEAK   = -3.1   # h Msun / pc^2
DES_Y3_DELTA_SIGMA_SIGMA  =  0.6   # 1-sigma
DES_Y3_R_OVER_RV_PEAK     =  1.00

# --- Cosmological anchors -------------------------------------------------
# Cosmic mean matter density today (h-independent ratio convention).
# Used only to bound u_void = 4 g / a_0 inside a typical void.
RHO_MEAN_KG_M3            = 2.775e-27 * 0.31    # Omega_m h^2 nominal
G_NEWTON_SI               = 6.674e-11           # m^3 kg^-1 s^-2
A0_MOND_SI                = 1.20e-10            # m s^-2 (Milgrom anchor)
MPC_M                     = 3.0857e22

# Typical L*-galaxy void effective radius for the u-estimate (Mpc).
R_V_TYPICAL_MPC           = 20.0
# Typical interior contrast for the u-estimate (mid of HSW range).
DELTA_INT_TYPICAL         = -0.85
