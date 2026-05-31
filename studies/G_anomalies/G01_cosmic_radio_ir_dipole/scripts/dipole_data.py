"""Literature data for the cosmic-dipole anomaly.

All values from the public references cited in the study README.
Speed of light in km/s for v/c convenience.
"""
from __future__ import annotations

from dataclasses import dataclass

C_KMS = 299_792.458

# --- CMB kinematic dipole (Planck 2018 VII, 1807.06205, Table 1) -----------
V_CMB_KMS       = 369.82
V_CMB_ERR_KMS   = 0.11
DIR_CMB_LDEG    = 264.021
DIR_CMB_BDEG    = 48.253
DIR_CMB_ERR_DEG = 0.011  # combined statistical uncertainty


@dataclass(frozen=True)
class DipoleSurvey:
    name: str
    D_obs: float
    D_err: float
    x: float       # cumulative number-count slope d log N / d log S (positive)
    alpha: float   # spectral index, S_nu ~ nu^-alpha
    dir_l_deg: float | None
    dir_b_deg: float | None
    offset_from_cmb_deg: float | None
    reference: str


# --- NVSS radio combined (Singal 2011 / Rubart & Schwarz 2013 consensus) ---
NVSS = DipoleSurvey(
    name="NVSS",
    D_obs=1.4e-2,
    D_err=0.4e-2,       # spread across analyses ~ (1.0--1.8) e-2
    x=1.0,
    alpha=0.75,
    dir_l_deg=253.0,
    dir_b_deg=27.0,
    offset_from_cmb_deg=25.0,
    reference="Singal 2011 ApJL 742 L23; Rubart & Schwarz 2013 A&A 555 A117",
)

# --- CatWISE2020 mid-IR AGN (Secrest et al. 2021 ApJL 908 L51) -------------
CATWISE = DipoleSurvey(
    name="CatWISE2020",
    D_obs=1.554e-2,
    D_err=0.198e-2,
    x=1.7,
    alpha=1.26,
    dir_l_deg=238.2,
    dir_b_deg=28.8,
    offset_from_cmb_deg=27.8,
    reference="Secrest et al. 2021 ApJL 908 L51",
)

# --- Joint NVSS + CatWISE (Secrest et al. 2022 ApJL 937 L31, ~5sigma) ------
JOINT = DipoleSurvey(
    name="NVSS+CatWISE joint",
    D_obs=1.45e-2,
    D_err=0.20e-2,
    x=1.35,             # population-weighted average
    alpha=1.0,          # population-weighted average
    dir_l_deg=247.0,
    dir_b_deg=28.0,
    offset_from_cmb_deg=26.0,
    reference="Secrest et al. 2022 ApJL 937 L31",
)


def all_surveys() -> tuple[DipoleSurvey, ...]:
    return (NVSS, CATWISE, JOINT)
