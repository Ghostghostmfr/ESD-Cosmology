"""SLACS-style strong-lens compilation for Study D07.

Sources: Bolton+ 2008 (ApJ 682, 964) SLACS survey; Auger+ 2010
(ApJ 724, 511) stellar masses and dark-matter fractions.

Values are representative published Chabrier-IMF M_* and Einstein-
radius f_DM(<R_E) for seven SLACS lenses. Where Auger+ 2010 does
not report a per-lens uncertainty on f_DM, we adopt the sample
systematic of +/- 0.10.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SLACSLens:
    label:         str
    z_lens:        float
    z_source:      float
    sigma_v_kms:   float
    M_star_msun:   float       # Chabrier IMF, Auger+ 2010
    R_E_kpc:       float
    theta_E_obs:   float       # arcsec
    f_DM_obs:      float       # Auger+ 2010, within R_E
    f_DM_err:      float
    reference:     str


# Representative SLACS subsample (Auger+ 2010 Table 4; Bolton+ 2008).
SAMPLES = [
    SLACSLens("SDSSJ0008-0004", 0.440, 1.192, 333.0, 2.6e11, 6.59, 1.16,
              0.40, 0.10, "Bolton+ 2008 / Auger+ 2010"),
    SLACSLens("SDSSJ0029-0055", 0.227, 0.931, 229.0, 1.2e11, 3.48, 0.96,
              0.32, 0.10, "Bolton+ 2008 / Auger+ 2010"),
    SLACSLens("SDSSJ0037-0942", 0.196, 0.632, 279.0, 2.1e11, 4.95, 1.53,
              0.40, 0.10, "Bolton+ 2008 / Auger+ 2010"),
    SLACSLens("SDSSJ0044+0113", 0.120, 0.197, 266.0, 1.0e11, 1.72, 0.79,
              0.20, 0.10, "Bolton+ 2008 / Auger+ 2010"),
    SLACSLens("SDSSJ0216-0813", 0.332, 0.523, 333.0, 3.6e11, 5.53, 1.16,
              0.40, 0.10, "Bolton+ 2008 / Auger+ 2010"),
    SLACSLens("SDSSJ0252+0039", 0.280, 0.982, 164.0, 0.9e11, 4.40, 1.04,
              0.55, 0.10, "Bolton+ 2008 / Auger+ 2010"),
    SLACSLens("SDSSJ2300+0022", 0.228, 0.464, 279.0, 1.7e11, 4.51, 1.24,
              0.45, 0.10, "Bolton+ 2008 / Auger+ 2010"),
]
