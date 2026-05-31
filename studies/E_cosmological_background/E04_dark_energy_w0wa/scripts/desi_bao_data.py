"""DESI Y1 BAO measurements (Adame et al. 2024, arXiv:2404.03002, Table 1).

Re-encoded locally from Study 07 (desi_y1_data.py) for study
self-containment.  Values are verbatim from Table 1 of the DESI Y1 paper.

Each tracer reports either D_V/r_d (BGS, QSO) or a (D_M/r_d, D_H/r_d)
pair with a within-tracer correlation coefficient rho.  Cross-tracer
covariance is assumed zero (standard for BAO compilations).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DV:
    name:    str
    z_eff:   float
    DV_rd:   float
    sigma:   float


@dataclass(frozen=True)
class DMDH:
    name:    str
    z_eff:   float
    DM_rd:   float
    DM_sig:  float
    DH_rd:   float
    DH_sig:  float
    rho:     float   # correlation coefficient between D_M and D_H


# Table 1 of arXiv:2404.03002.
DESI_Y1 = [
    DV  ("BGS",          z_eff=0.295, DV_rd=7.93,  sigma=0.15),
    DMDH("LRG1",         z_eff=0.510, DM_rd=13.62, DM_sig=0.25,
                          DH_rd=20.98, DH_sig=0.61, rho=-0.445),
    DMDH("LRG2",         z_eff=0.706, DM_rd=16.85, DM_sig=0.32,
                          DH_rd=20.08, DH_sig=0.60, rho=-0.420),
    DMDH("LRG3+ELG1",    z_eff=0.930, DM_rd=21.71, DM_sig=0.28,
                          DH_rd=17.88, DH_sig=0.35, rho=-0.389),
    DMDH("ELG2",         z_eff=1.317, DM_rd=27.79, DM_sig=0.69,
                          DH_rd=13.82, DH_sig=0.42, rho=-0.444),
    DV  ("QSO",          z_eff=1.491, DV_rd=26.07, sigma=0.67),
    DMDH("Lya QSO",      z_eff=2.330, DM_rd=39.71, DM_sig=0.94,
                          DH_rd=8.52,  DH_sig=0.17, rho=-0.477),
]

# Total degrees of freedom.
N_MEAS = sum(2 if isinstance(t, DMDH) else 1 for t in DESI_Y1)   # 12
