"""Black-hole tidal Love-number anchors.

The GR result is exact: a Schwarzschild or Kerr black hole has a
vanishing quadrupolar tidal Love number, k2 = 0, hence dimensionless
tidal deformability Lambda = 0 (Binnington & Poisson 2009;
Damour & Nagar 2009; Guerlebeck 2015 PRL 114 151102; Chia 2021
PRD 104 024013).

Current gravitational-wave data place upper bounds on the tidal
deformability of compact binaries; the BH prediction Lambda = 0 lies
inside every bound. Exotic compact objects (boson stars, gravastars)
predict k2 != 0 and are increasingly constrained.
"""
from __future__ import annotations

G_M3_KG_S2 = 6.67430e-11
C_M_S      = 2.99792458e8
M_SUN_KG   = 1.98892e30

# GR / Kerr exact result (theorem, no free parameter)
K2_KERR_GR     = 0.0
C_SCHWARZSCHILD = 0.5   # horizon compactness GM/(R c^2) for Schwarzschild

# Representative BH masses (Msun) spanning the astrophysical range
BH_MASSES_MSUN = [
    {"object": "LIGO stellar-mass BH", "M_Msun": 30.0},
    {"object": "GW190521 remnant",      "M_Msun": 142.0},
    {"object": "Sgr A* (Galactic SMBH)","M_Msun": 4.3e6},
    {"object": "M87* (EHT SMBH)",       "M_Msun": 6.5e9},
]

# Tightest current tidal-deformability bounds (90% CL upper limits on the
# effective tidal deformability). The BH prediction Lambda = 0 sits inside
# each. These also set the scale at which a *nonzero* BH Love number would
# become detectable.
TIDAL_BOUNDS = [
    {"event": "GW170817", "Lambda_upper_90CL": 720.0,
     "kind": "effective Lambda-tilde (low-spin)",
     "ref": "Abbott+ 2019 PRX 9 011001"},
    {"event": "GW190425", "Lambda_upper_90CL": 600.0,
     "kind": "effective Lambda-tilde",
     "ref": "Abbott+ 2020 ApJL 892 L3"},
]

# Alternatives to a Kerr BH that predict a *nonzero* Love number, i.e. the
# objects this null test discriminates against.
EXOTIC_ALTERNATIVES = [
    {"object": "boson star",  "k2": "~ 10 to 100", "ref": "Cardoso+ 2017 PRD 95 084014"},
    {"object": "gravastar",   "k2": "< 0 (negative)", "ref": "Cardoso+ 2017 PRD 95 084014"},
    {"object": "wormhole",    "k2": "O(0.1 to 1), nonzero", "ref": "Cardoso & Pani 2019 LRR 22 4"},
]
