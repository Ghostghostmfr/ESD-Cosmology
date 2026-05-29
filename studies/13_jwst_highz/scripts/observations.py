"""Published JWST high-z stellar mass density measurements.

Sources:
  - Labbé+2023, Nature 616, 266 (CEERS, 6 candidates).
  - Boylan-Kolchin 2023, Nat Astron 7, 731 (interpretive paper).
  - Casey+2024, ApJ 965, 98 (COSMOS-Web confirmation).
  - Xiao+2024, Nature 635, 311 (FRESCO ultra-massive at z=5-9).
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HighZRhoStar:
    label:       str
    z_lo:        float
    z_hi:        float
    rho_star:    float          # Msun / Mpc^3, cumulative > log10_Mstar_min
    rho_err:     float
    log10_Mstar_min: float
    survey_volume_Mpc3: float
    reference:   str


SAMPLES = [
    HighZRhoStar(
        label="Labbe+2023 CEERS",
        z_lo=7.0, z_hi=9.0,
        rho_star=6.5e6, rho_err=4.0e6,
        log10_Mstar_min=10.5,
        survey_volume_Mpc3=1.0e5,
        reference="Nature 616, 266 (2023)",
    ),
    HighZRhoStar(
        label="Casey+2024 COSMOS-Web",
        z_lo=7.5, z_hi=10.0,
        rho_star=2.5e6, rho_err=1.5e6,
        log10_Mstar_min=10.5,
        survey_volume_Mpc3=2.0e6,
        reference="ApJ 965, 98 (2024)",
    ),
    HighZRhoStar(
        label="Xiao+2024 FRESCO",
        z_lo=5.0, z_hi=9.0,
        rho_star=1.0e7, rho_err=5.0e6,
        log10_Mstar_min=10.0,
        survey_volume_Mpc3=6.0e4,
        reference="Nature 635, 311 (2024)",
    ),
]
