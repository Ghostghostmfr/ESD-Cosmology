"""HI-dominated dwarf anchors.

AGC 114905 is intentionally not included in the audit set: its
inclination is poorly determined (32 deg quoted but Sellwood &
McGaugh 2022 argue for >= 45 deg, while Banik et al. need ~10 deg
to recover the BTFR). A single-aperture V_flat audit cannot
discriminate. The fair version of that test is a full HI-cube
re-analysis, deferred to a future study.
"""
from __future__ import annotations
M_SUN_KG = 1.98892e30

SOURCES = [
    {"name": "WLM",     "V_flat_kms": 38.0, "V_err": 4.0,
     "M_b_Msun": 7.4e7, "M_b_err": 1.5e7,
     "ref": "Iorio+ 2017 MNRAS 466 4159"},
    {"name": "DDO 154", "V_flat_kms": 49.0, "V_err": 3.0,
     "M_b_Msun": 3.0e8, "M_b_err": 0.6e8,
     "ref": "Iorio+ 2017 MNRAS 466 4159"},
]
