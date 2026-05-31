"""Ringdown anchors."""
from __future__ import annotations
G_M3_KG_S2 = 6.67430e-11
C_M_S      = 2.99792458e8
M_SUN_KG   = 1.98892e30

# GW150914 final state (Abbott+ 2016)
GW150914 = {
    "Mf_Msun":   62.0,
    "Mf_err":    4.0,
    "chi_f":     0.67,
    "chi_f_err": 0.05,
    "redshift":  0.09,
    # Isi+ 2019 (PRL 123 111102), 220-mode (detector frame)
    "f220_Hz":   251.5,
    "f220_errp": 9.2,
    "f220_errm": 12.6,
    "tau220_ms": 4.0,
    "tau220_errp": 1.7,
    "tau220_errm": 2.5,
}

def f220_symm_err(d=GW150914) -> float:
    return 0.5 * (d["f220_errp"] + d["f220_errm"])
def tau220_symm_err(d=GW150914) -> float:
    return 0.5 * (d["tau220_errp"] + d["tau220_errm"])
