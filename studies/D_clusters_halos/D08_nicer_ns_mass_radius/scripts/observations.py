"""NICER NS anchors."""
from __future__ import annotations
G_M3_KG_S2 = 6.67430e-11
M_SUN_KG   = 1.98892e30

SOURCES = [
    {"name": "J0030+0451", "M": 1.44,  "M_err": 0.15,
     "R_km": 13.02, "R_err_p": 1.24, "R_err_m": 1.06,
     "ref": "Miller+ 2019 ApJL 887 L24"},
    {"name": "J0740+6620", "M": 2.08,  "M_err": 0.07,
     "R_km": 13.7,  "R_err_p": 2.6,  "R_err_m": 1.5,
     "ref": "Miller+ 2021 ApJL 918 L28"},
    {"name": "J0437-4715", "M": 1.418, "M_err": 0.044,
     "R_km": 11.36, "R_err_p": 0.95, "R_err_m": 0.63,
     "ref": "Choudhury+ 2024 ApJL 971 L20"},
]

def R_symm_err(s):
    return 0.5 * (s["R_err_p"] + s["R_err_m"])
