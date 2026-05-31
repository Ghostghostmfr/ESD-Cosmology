"""BH spin anchors."""
from __future__ import annotations
G_M3_KG_S2 = 6.67430e-11
C_M_S      = 2.99792458e8
M_SUN_KG   = 1.98892e30

THORNE_MAX = 0.998

OBSERVATIONS = [
    {"object": "GRS 1915+105",    "channel": "X-ray reflection",
     "M_Msun": 12.4, "chi": 0.98, "chi_err": 0.01,
     "ref": "McClintock+ 2006"},
    {"object": "MCG-6-30-15",     "channel": "X-ray reflection",
     "M_Msun": 4.5e6, "chi": 0.97, "chi_err": 0.02,
     "ref": "Brenneman & Reynolds 2006"},
    {"object": "GW150914 remnant","channel": "GW ringdown",
     "M_Msun": 62.0, "chi": 0.67, "chi_err": 0.05,
     "ref": "Abbott+ 2016"},
    {"object": "GWTC-3 max",      "channel": "GW ringdown",
     "M_Msun": 90.0, "chi": 0.87, "chi_err": 0.10,
     "ref": "Abbott+ 2023 PRX 13 011048"},
]
