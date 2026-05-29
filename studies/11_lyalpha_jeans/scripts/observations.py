"""Lyman-alpha forest cutoff observations (literature values).

Lyman-alpha 1D flux power spectrum at z~3 from SDSS BOSS / eBOSS
constrains ultralight scalar DM through the small-scale suppression
relative to CDM.  Three benchmark analyses are catalogued here.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LyAlphaBound:
    """Lyman-alpha cutoff measurement / bound."""
    name:        str
    k_max_skm:   float  # max k probed [s/km] (Lya line-of-sight wavenumber)
    k_max_Mpc:   float  # equivalent comoving Mpc^-1 at z~3 (rough conversion)
    m22_bound:   float  # 95% C.L. lower bound on m_a in units of 1e-22 eV
    bound_kind:  str    # "exclusion" or "preferred"
    ref:         str


# Conversion at z~3 for IGM Hubble flow: k [Mpc^-1] ~ k [s/km] * H(z)/(1+z)
# H(z=3) ~ 320 km/s/Mpc, so k[Mpc^-1] ~ k[s/km] * 80
SAMPLES = [
    LyAlphaBound(
        name        = "SDSS-BOSS DR9 (Palanque-Delabrouille+2013)",
        k_max_skm   = 0.02,
        k_max_Mpc   = 1.6,
        m22_bound   = 21.08,
        bound_kind  = "exclusion",
        ref         = "Palanque-Delabrouille+2013, A&A 559, A85",
    ),
    LyAlphaBound(
        name        = "XQ-100 (Irsic+2017)",
        k_max_skm   = 0.07,
        k_max_Mpc   = 5.6,
        m22_bound   = 20.0,
        bound_kind  = "exclusion",
        ref         = "Irsic+2017, PRL 119, 031302",
    ),
    LyAlphaBound(
        name        = "eBOSS DR14 (Rogers & Peiris 2021)",
        k_max_skm   = 0.07,
        k_max_Mpc   = 5.6,
        m22_bound   = 200.0,
        bound_kind  = "exclusion",
        ref         = "Rogers & Peiris 2021, PRL 126, 071302",
    ),
]
