"""Black-hole ringdown-echo anchors.

A perfectly absorbing (classical GR) horizon produces NO post-ringdown
echoes: the ringdown signal decays monotonically through the
quasinormal-mode (QNM) tail. Echoes are the signature of an exotic
compact object (ECO) with a partially *reflecting* inner boundary at
proper distance epsilon from the would-be horizon -- e.g.
Planck-scale-corrected horizons, gravastars, wormholes, firewalls,
fuzzballs (Cardoso, Franzin & Pani 2016 PRL 116 171101;
Cardoso & Pani 2019 Living Rev. Rel. 22 4).

The echo train arrives with a characteristic delay set by the
light-crossing time between the photon sphere and the reflective
surface:

    Delta t_echo ~ 2 * (G M / c^3) * |ln(epsilon)|,

and amplitude proportional to the surface reflectivity coefficient
|R_wall|. A classical horizon has |R_wall| = 0.

Searches for echoes in LVK data have so far returned NO statistically
significant detection once trials are accounted for
(Abedi+ 2017 claimed 2.5-4.2 sigma; Westerweck+ 2018 and the LVK
TGR catalogues find significance consistent with noise,
<~ 2 sigma / no confirmed echo).
"""
from __future__ import annotations

G_M3_KG_S2 = 6.67430e-11
C_M_S      = 2.99792458e8
M_SUN_KG   = 1.98892e30

# GR / classical-horizon result (theorem, no free parameter)
WALL_REFLECTIVITY_GR = 0.0   # perfectly absorbing horizon -> no echoes
ECHO_AMPLITUDE_GR    = 0.0

# Representative remnant masses (Msun)
REMNANTS = [
    {"object": "GW150914 remnant", "M_Msun": 62.0, "chi": 0.67},
    {"object": "GW170817 remnant", "M_Msun": 2.7,  "chi": 0.80},
    {"object": "GW190521 remnant", "M_Msun": 142.0,"chi": 0.72},
]

# Echo searches: reported reflectivity / significance constraints.
# "R_wall_upper" = 90% CL upper bound on the inner-boundary reflectivity
# (consistent with 0 for a classical horizon); "sigma_claim" = reported
# detection significance after trials.
ECHO_SEARCHES = [
    {"search": "Abedi+ 2017 (GW150914/151226/170104)",
     "R_wall_upper": 1.0, "sigma_claim": 2.5,
     "ref": "Abedi, Dykaar & Afshordi 2017 PRD 96 082004"},
    {"search": "Westerweck+ 2018 (re-analysis)",
     "R_wall_upper": 1.0, "sigma_claim": 1.0,
     "ref": "Westerweck+ 2018 PRD 97 124037"},
    {"search": "LVK TGR O3 (Isi+ / Abbott+ 2021)",
     "R_wall_upper": 1.0, "sigma_claim": 1.0,
     "ref": "Abbott+ 2021 PRD 103 122002"},
]

# ECO alternatives that DO predict echoes (the targets this null
# discriminates against).
ECO_ALTERNATIVES = [
    {"object": "Planck-scale corrected horizon",
     "epsilon": 1.6e-35 / 1.0, "R_wall": "0.1-1", "ref": "Cardoso+ 2016 PRL 116 171101"},
    {"object": "gravastar", "epsilon": 1e-10, "R_wall": "~1",
     "ref": "Mazur & Mottola 2004 PNAS 101 9545"},
    {"object": "wormhole",  "epsilon": 1e-20, "R_wall": "O(0.1-1)",
     "ref": "Cardoso & Pani 2019 LRR 22 4"},
]
