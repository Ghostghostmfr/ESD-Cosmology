"""Local Group orbital observables and direct baryonic mass."""
from __future__ import annotations

# Present-day separation MW <-> M31 (van der Marel+ 2012).
R_TODAY_KPC: float = 770.0

# Radial relative velocity (M31 approaching MW). Negative = inbound.
V_RADIAL_TODAY_KMS: float = -109.4

# Age of the universe (Planck 2018).
T_AGE_GYR: float = 13.787

# Direct Local Group baryonic mass budget (Msun):
#   MW (stars + gas + cold halo)  ~ 6e10  (McMillan 2017)
#   M31 (stars + gas)             ~ 1.2e11 (Tamm+ 2012)
#   LG dwarfs (gas + stars)       ~ 1e9   (catalogue sum)
# Total ~ 1.8e11 Msun. Allow +/- ~50% systematic uncertainty.
M_BARYON_OBS_MSUN: float = 1.8e11
M_BARYON_OBS_LO:   float = 0.8e11
M_BARYON_OBS_HI:   float = 3.0e11

# Canonical Newton timing-argument range (Li & White 2008,
# Partridge+ 2013, Penarrubia+ 2014).
M_LG_NEWTON_LO_MSUN: float = 3.0e12
M_LG_NEWTON_HI_MSUN: float = 6.0e12
