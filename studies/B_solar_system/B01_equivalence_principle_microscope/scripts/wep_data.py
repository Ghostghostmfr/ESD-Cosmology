"""MICROSCOPE WEP-test data + ESD framework inputs.

All framework constants lifted from Master Book Ch. 4 sec. 4.7
(channel-ratio derivation) and the Cassini-anchored PPN result earlier
in the same section.
"""
from __future__ import annotations

# --- Experimental bounds ---------------------------------------------------
MICROSCOPE_2022_ETA_BOUND   = 2.7e-15   # Touboul+ 2022 PRL 129 121102 (95% CL)
MICROSCOPE2_FORECAST_ETA    = 1.0e-17   # Berge+ 2018 PRL 120 141101

# --- ESD framework inputs at Earth (u_Earth from Cassini PPN derivation) ---
# beta_m^2 ~ 10^-9: screening factor that delivers GR-PPN recovery in
#                   the solar system, set by Cassini gamma-1 ~ 2.1e-5 bound.
BETA_M_SQ_EARTH             = 1.0e-9

# (beta_Z/beta_m)(u_Earth): channel ratio between the gauge bridge and the
# conformal channel, output of Master Ch. 4 Eq. (channel-ratio-running).
BETA_Z_OVER_BETA_M_EARTH    = 2.6e-11

# Pt-Ti EM binding-fraction contrast (standard nuclear-physics tables).
DELTA_F_EM_PT_TI            = 1.0e-3
