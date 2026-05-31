"""EHT 2019 (M87*) and EHT 2022 (Sgr A*) measurements."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class EHTSource:
    label:        str
    M_solar:      float       # mass estimate (independent of EHT)
    M_err_solar:  float
    D_m:          float       # distance in metres
    D_err_m:      float
    theta_obs_rad: float      # measured ring angular diameter
    theta_err_rad: float
    reference:    str

from esd_eht import MUAS, MPC_M, KPC_M  # type: ignore

SOURCES = [
    # M87*: EHT 2019 (Paper I), mass from stellar dynamics (Gebhardt+2011)
    EHTSource(
        label="M87*",
        M_solar=6.5e9, M_err_solar=0.7e9,
        D_m=16.8*MPC_M, D_err_m=0.8*MPC_M,
        theta_obs_rad=42.0*MUAS, theta_err_rad=3.0*MUAS,
        reference="EHT Collaboration 2019 (ApJL 875 L1)",
    ),
    # Sgr A*: EHT 2022, mass + distance from GRAVITY (Abuter+2019)
    EHTSource(
        label="Sgr A*",
        M_solar=4.154e6, M_err_solar=0.014e6,
        D_m=8.275*KPC_M, D_err_m=0.034*KPC_M,
        theta_obs_rad=51.8*MUAS, theta_err_rad=2.3*MUAS,
        reference="EHT Collaboration 2022 (ApJL 930 L12)",
    ),
]
