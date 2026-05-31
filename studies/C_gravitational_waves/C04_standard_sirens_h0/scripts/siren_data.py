"""Standard-siren H_0 data (Study 40).

Gravitational-wave standard sirens give H_0 directly from the
inspiral amplitude (luminosity distance d_L) cross-matched with an
electromagnetic redshift (BNS counterpart, host galaxy, or dark-siren
statistical galaxy catalog).

In modified gravity with an extra graviton-friction term gamma:
   d_L^GW(z) = d_L^EM(z) * (1 + gamma * f(z))
ESD predicts gamma = 0 (no extra friction; see Study 21 GW sector
derivation), so d_L^GW / d_L^EM = 1 and H_0^siren matches H_0^CMB
at the framework-locked value 67.36 km/s/Mpc.

Published standard-siren H_0 measurements:
"""
from __future__ import annotations

H_0_LOCKED = 67.36   # ESD-locked Planck-CMB value (km/s/Mpc)

# (label, H_0, +sigma, -sigma, kind, citation)
SIREN_MEASUREMENTS = [
    ("GW170817 (BNS+EM)",      70.0,  12.0, 8.0, "bright",
     "Abbott+ 2017, Nature 551, 85 (single BNS)"),
    ("GW170817 + GRB JVLA",    70.3,   5.3, 5.0, "bright+VLBI",
     "Hotokezaka+ 2019, Nat. Astron. 3, 940 (VLBI inclination)"),
    ("GW190814 dark sirens",   75.0,  18.0, 7.0, "dark",
     "Vasylyev & Filippenko 2020, ApJ 902, 149 (NS-BH dark)"),
    ("GWTC-3 dark sirens",     68.0,   8.0, 6.0, "dark_statistical",
     "Abbott+ 2023, ApJ 949, 76 (LVK GWTC-3 stat catalog)"),
    ("LVK O3 BBH cosmography", 67.3,   5.4, 4.9, "dark_statistical",
     "Abbott+ 2021, ApJ 909, 218 (BBH population)"),
    ("DECam+GW170817 host",    71.9,   3.9, 3.1, "bright_redo",
     "Mukherjee+ 2021, A&A 646, A65 (peculiar-velocity corrected)"),
    ("LVK O4a (forecast)",     68.0,   2.5, 2.5, "forecast",
     "Chen+ 2018, Nature 562, 545 (50 BNS forecast)"),
    ("ET/CE (forecast)",       67.4,   0.5, 0.5, "forecast",
     "Borhanian+ 2020, ApJL 905, L28 (Einstein Telescope decade)"),
]
