"""Cluster baryon-fraction measurements used by Study 10.

Each entry is a published f_b = M_b / M_tot at a defined cluster radius
(R_2500c, R_500c, or R_200c) with 1-sigma error.  Sample-median values
are quoted for stacked samples.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClusterFb:
    name:         str
    f_b:          float       # baryon fraction at R_def
    sigma:        float
    radius_def:   str         # "R_2500c" | "R_500c" | "R_200c"
    M_500_solar:  float       # representative cluster mass [Msun]
    R_def_mpc:    float       # radius for the f_b measurement
    ref:          str


SAMPLES = [
    ClusterFb("X-COP (12 nearby clusters)",
              f_b=0.131, sigma=0.005, radius_def="R_500c",
              M_500_solar=5.0e14, R_def_mpc=1.20,
              ref="Eckert+ 2019, A&A 621, A40"),
    ClusterFb("X-COP extrapolated to R_200c",
              f_b=0.146, sigma=0.010, radius_def="R_200c",
              M_500_solar=5.0e14, R_def_mpc=1.85,
              ref="Eckert+ 2019, A&A 621, A40"),
    ClusterFb("Planck SZ baryon census",
              f_b=0.126, sigma=0.011, radius_def="R_500c",
              M_500_solar=6.0e14, R_def_mpc=1.30,
              ref="Planck 2015 XXIV, A&A 594, A24"),
    ClusterFb("CHEX-MATE relaxed subset",
              f_b=0.135, sigma=0.008, radius_def="R_500c",
              M_500_solar=6.0e14, R_def_mpc=1.30,
              ref="CHEX-MATE Collaboration 2024, A&A 686, A185"),
    ClusterFb("XMM Cluster Outskirts Project (XCOP-extreme)",
              f_b=0.155, sigma=0.012, radius_def="R_200c",
              M_500_solar=8.0e14, R_def_mpc=2.10,
              ref="Ettori+ 2019, A&A 621, A39"),
    # Cosmic asymptote: at and beyond the virial radius f_b -> Omega_b/Omega_m
    ClusterFb("Planck cosmic f_b (asymptote)",
              f_b=0.156, sigma=0.003, radius_def="R_inf",
              M_500_solar=0.0, R_def_mpc=0.0,
              ref="Aghanim+ 2020, A&A 641, A6"),
]
