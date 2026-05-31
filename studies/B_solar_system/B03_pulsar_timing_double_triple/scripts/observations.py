"""J0737-3039 and J0337+1715 measured anchors (with citations)."""
from __future__ import annotations
import math

G_M3_KG_S2: float = 6.67430e-11
C_M_S:      float = 2.99792458e8
M_SUN_KG:   float = 1.98892e30

# Double pulsar J0737-3039A/B (Kramer+ 2021, PRX 11, 041050)
J0737 = {
    "Pb_s":         2.4541846 * 3600.0,            # orbital period (s)
    "e":            0.0877775,
    "M_A_Msun":     1.338185,                       # +/- 0.000014 (PRX 11.041050 Tab 2)
    "M_B_Msun":     1.248868,                       # +/- 0.000013
    "omdot_deg_yr": 16.899323,  "omdot_err": 0.00013,
    "Pbdot_meas":  -1.247920e-12, "Pbdot_err": 7e-18,
    "gamma_ms":     0.384045,   "gamma_err": 0.000094,
    "r_us":         6.162,      "r_err": 0.021,
    "s_sini":       0.999936,   "s_err": 7e-6,
}

# J0337+1715 strong-EP bound (Voisin+ 2020 A&A 638 A24, 95% CL)
J0337 = {
    "Delta_95CL":   1.8e-6,
    "Delta_meas":  -1.1e-6,
    "Delta_err":    1.7e-6,
}

# Acceleration scales (m/s^2)
NS_MASS_KG    = J0737["M_A_Msun"] * M_SUN_KG
NS_RADIUS_M   = 12.0e3                              # typical NS radius
J0737_A_M     = 8.784e8                             # semi-major axis A (m); a sin i / s
G_NS_SURFACE  = G_M3_KG_S2 * NS_MASS_KG / NS_RADIUS_M ** 2
G_ORBITAL_PSR = G_M3_KG_S2 * NS_MASS_KG / J0737_A_M ** 2

def post_keplerian_GR():
    """GR post-Keplerian predictions for J0737 at masses in J0737 dict."""
    M = (J0737["M_A_Msun"] + J0737["M_B_Msun"]) * M_SUN_KG
    Pb = J0737["Pb_s"]; e = J0737["e"]
    n = 2 * math.pi / Pb
    GMc3 = G_M3_KG_S2 * M / C_M_S ** 3
    # 1PN periastron advance
    omdot = 3.0 * (GMc3 ** (2.0/3.0)) * (n ** (5.0/3.0)) / (1.0 - e * e)
    omdot_deg_yr = math.degrees(omdot) * 3.15576e7
    return {"omdot_deg_yr": omdot_deg_yr}
