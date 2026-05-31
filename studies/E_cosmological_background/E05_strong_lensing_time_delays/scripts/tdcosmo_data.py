"""TDCOSMO + H0LiCOW strong-lens time-delay anchors and constants."""
from __future__ import annotations

# -------------------- physical / cosmological constants -------------------
C_LIGHT_KM_S: float    = 299_792.458       # km/s
MPC_KM: float          = 3.0857e19         # km in 1 Mpc
G_NEWTON_SI: float     = 6.6743e-11        # m^3 / (kg s^2)
A0_MOND_SI: float      = 1.2015e-10        # m/s^2  (Study 12 anchor)
M_SUN_KG: float        = 1.98892e30
KPC_M: float           = 3.0857e19         # m
PC_M: float            = 3.0857e16

# -------------------- LCDM parameters (Planck 2018, fiducial) -------------
H0_PLANCK: float       = 67.36             # km/s/Mpc
H0_PLANCK_SIGMA: float = 0.54
H0_SH0ES: float        = 73.04             # km/s/Mpc  (Riess+ 2022)
H0_SH0ES_SIGMA: float  = 1.04
OMEGA_M: float         = 0.3158
OMEGA_L: float         = 1.0 - OMEGA_M

# -------------------- ESD framework prediction ----------------------------
# H_0 from the a_0 bridge inversion (studies 08, 12, 20, 21).
# See studies/A05_a0_multi_tracer_anchor and studies/E02_hubble_tension_h0/paper.
H0_ESD: float          = 67.36             # km/s/Mpc  (Planck-anchored)
H0_ESD_SIGMA: float    = 0.54              # inherits Planck uncertainty

# -------------------- TDCOSMO 6-lens sample observables -------------------
# Lens redshifts and source redshifts for the H0LiCOW / TDCOSMO sample
# (Wong+ 2020, MNRAS 498, 1420; Suyu+ 2017 individual papers).
TDCOSMO_LENSES = {
    "B1608+656":   {"z_lens": 0.6304, "z_src": 1.394},
    "RXJ1131-1231":{"z_lens": 0.295,  "z_src": 0.654},
    "HE0435-1223": {"z_lens": 0.4546, "z_src": 1.693},
    "SDSS1206+4332":{"z_lens": 0.745, "z_src": 1.789},
    "WFI2033-4723":{"z_lens": 0.6575, "z_src": 1.662},
    "PG1115+080":  {"z_lens": 0.311,  "z_src": 1.722},
}

# Wong+ 2020 (H0LiCOW) - 6-lens combined H_0 (rigid power-law mass profile)
H0_TDCOSMO_WONG2020: float       = 73.3
H0_TDCOSMO_WONG2020_SIGMA_PLUS: float  = 1.7
H0_TDCOSMO_WONG2020_SIGMA_MINUS: float = 1.8

# Birrer+ 2020 (TDCOSMO-IV) - 6-lens + 33 SLACS, mass-sheet-flexible
H0_TDCOSMO_IV: float             = 67.4
H0_TDCOSMO_IV_SIGMA_PLUS: float  = 4.1
H0_TDCOSMO_IV_SIGMA_MINUS: float = 3.2

# Representative time-delay distance (B1608+656, Suyu+ 2010)
# D_dt_obs = (1+z_l) * D_l * D_s / D_ls, in Mpc.
D_DT_B1608_MPC: float   = 5156.0
D_DT_B1608_SIGMA: float = 296.0           # ~5.7 %

# -------------------- representative strong-lens scales -------------------
# Use a generic massive elliptical lens for u_lens estimate.
SIGMA_V_LENS_KM_S: float = 250.0           # central velocity dispersion
THETA_E_ARCSEC: float    = 1.5             # typical Einstein radius
D_L_TYPICAL_MPC: float   = 1500.0          # ~ z_l = 0.5 angular diameter
