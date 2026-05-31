"""Cosmicflows-4 peculiar velocities (Study 47).

The z~0 peculiar-velocity field probes the growth amplitude fsigma_8
directly through the linear continuity equation. Cosmicflows-4
(Tully+ 2023; Said+ 2024; Howlett+ 2017 / 2022 6dFGS-v; Boruah+ 2020
SFI++/A2; Lilow & Nusser 2021 2M++) consistently report
fsigma_8(z~0) = 0.36 - 0.46 - on the high side of Planck-LCDM
(fsigma_8(0) ~ 0.43).

ESD shares Planck-LCDM linear growth (Study 19); the peculiar-velocity
amplitude is therefore at the same value as in the sigma_8 tension
family - within the cosmic-flows error budget, but slightly low vs
some compilations. Pattern is the SAME as Studies 36, 39, 43 - the
canonical sigma_8 family, owned by Study 18.
"""
from __future__ import annotations

H_0_LOCKED       = 67.36
OMEGA_M_LOCKED   = 0.31574
SIGMA_8_LOCKED   = 0.8111
GAMMA_LINDER     = 0.55

# ESD-predicted fsigma_8(z=0): use Linder gamma growth
# Omega_m(0) = 0.31574; f(0) = Omega_m^0.55 = 0.31574^0.55 = 0.53538
# sigma_8(0) = 0.8111
# fsigma_8(0) = 0.53538 * 0.8111 = 0.43425
ESD_FSIGMA8_Z0 = (OMEGA_M_LOCKED ** GAMMA_LINDER) * SIGMA_8_LOCKED

# (program, fsigma_8(z~0) measured, sigma, citation)
PECULIAR_VEL_MEASUREMENTS = [
    ("6dFGSv (Huterer+ 2017)",              0.428, 0.066, "Huterer+ 2017"),
    ("6dFGSv (Adams & Blake 2020)",         0.384, 0.052, "Adams & Blake 2020"),
    ("2MTF (Howlett+ 2017)",                0.505, 0.085, "Howlett+ 2017"),
    ("SDSS PV (Howlett+ 2017)",             0.452, 0.077, "Howlett+ 2017"),
    ("SFI++/A2 (Boruah+ 2020)",             0.400, 0.040, "Boruah+ 2020"),
    ("2M++ (Lilow & Nusser 2021)",          0.421, 0.038, "Lilow & Nusser 2021"),
    ("Cosmicflows-3 (Said+ 2020)",          0.460, 0.060, "Said+ 2020"),
    ("Cosmicflows-4 (Said+ 2024)",          0.413, 0.034, "Said+ 2024"),
]
