"""Scale-dependent linear galaxy bias b(k) (Study 45).

In LCDM, the large-scale linear bias b is k-independent. In f(R) /
chameleon / DGP MG, the modified growth rate is k-dependent and
induces a measurable k-dependence in b(k) at the few-percent level
(Pollina+ 2018; Aviles+ 2019; Valogiannis+ 2020).

BOSS DR12 (Beutler+ 2017), eBOSS LRG (Bautista+ 2021), DESI DR1
(DESI 2024) all report b(k) consistent with constant within k =
0.01 - 0.2 h/Mpc.

ESD has no k-dependent linear growth (Study 19 theorem: R(u) acts
only on bound virialized subsystems). Prediction: db/dlnk = 0.
"""
from __future__ import annotations

# Reported deviation of b(k) from constant
# Definition: max |b(k_i) - <b>| / <b> across the linear-regime bins
# (program, max fractional deviation, sigma, k_range_h_Mpc, citation)
BIAS_K_MEASUREMENTS = [
    ("BOSS DR12 LOWZ",  0.018, 0.025, "0.01-0.15", "Beutler+ 2017"),
    ("BOSS DR12 CMASS", 0.015, 0.020, "0.01-0.15", "Beutler+ 2017"),
    ("eBOSS LRG",       0.020, 0.030, "0.01-0.15", "Bautista+ 2021"),
    ("eBOSS ELG",       0.025, 0.040, "0.01-0.15", "de Mattia+ 2021"),
    ("eBOSS QSO",       0.030, 0.045, "0.01-0.15", "Neveux+ 2020"),
    ("DESI DR1 LRG",    0.012, 0.018, "0.02-0.20", "DESI 2024"),
    ("DESI DR1 ELG",    0.022, 0.030, "0.02-0.20", "DESI 2024"),
]

# ESD predicts strictly 0 (Study 19 corollary)
ESD_DBIAS_DLNK = 0.0
