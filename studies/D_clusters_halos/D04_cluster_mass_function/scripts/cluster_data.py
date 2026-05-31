"""Cluster mass function anchors (Study 36).

Galaxy clusters are *bound, virialized* subsystems with a clear
system/spectator split (the cluster against the cosmological
background), so ALL three Study 19 axioms hold and R(u) APPLIES.
This is in contrast to linear cosmological perturbations
(Studies 18/19/34/35 where R(u) is excluded by Axiom A1).

The cluster mass function n(M, z) is therefore a genuine ESD
discriminator: the effective Newton coupling inside a collapsing
cluster is enhanced by 1 + w_D(u_cl) * R(u_cl), which shifts the
spherical-collapse threshold delta_c downward and lifts the
high-mass tail of n(M, z).

Cluster mass scales:
   M_200 ~ 1e14 - 1e15 Msun
   R_200 ~ 1 - 2 Mpc
   g_vir ~ G M / R^2  ~  3 - 10 x 10^{-12} m/s^2
   u_vir = 4 g / a_0  ~  0.1 - 0.3
   R(u_vir) ~ 3 - 5    -> non-trivial enhancement

Published anchors:
"""
from __future__ import annotations

# Locked cosmological parameters
OMEGA_M0_LOCKED = 0.31574                 # Identity B C2
SIGMA_8_LOCKED  = 0.8111                  # ESD = Planck-CMB (Study 19)
S_8_LOCKED      = SIGMA_8_LOCKED * (OMEGA_M0_LOCKED / 0.3) ** 0.5
DELTA_C_LCDM    = 1.686                   # spherical-collapse threshold, EdS
A_0_MOND_SI     = 1.20e-10
G_NEWTON_SI     = 6.67430e-11
M_SUN_KG        = 1.98892e30
MPC_M           = 3.0857e22

# ---------------- Published cluster cosmology constraints ----------------
# (label, Omega_m, +sig, -sig, sigma_8, +sig, -sig, S_8, +sig, -sig, citation)
CLUSTER_COSMOLOGY = [
    ("eROSITA DR1",  0.29, 0.03, 0.03, 0.88, 0.02, 0.03, 0.86, 0.04, 0.04,
     "Bulbul+ 2024 A&A 685, A106 (eROSITA-DE 5259 clusters)"),
    ("eROSITA + DES Y3", 0.28, 0.02, 0.02, 0.82, 0.02, 0.02, 0.80, 0.02, 0.02,
     "Ghirardini+ 2024 A&A 689, A298 (joint with WL mass calib)"),
    ("Planck SZ + WL",  0.33, 0.03, 0.03, 0.78, 0.03, 0.03, 0.79, 0.02, 0.02,
     "Planck 2016 XXIV A&A 594, A24 (439 SZ clusters)"),
    ("SPT-SZ x DES Y3", 0.286, 0.032, 0.032, 0.77, 0.03, 0.03, 0.76, 0.02, 0.02,
     "Bocquet+ 2019 ApJ 878, 55 (SPT 343 clusters)"),
    ("ACT DR5 SZ",      0.31, 0.04, 0.04, 0.79, 0.04, 0.04, 0.81, 0.03, 0.03,
     "Hilton+ 2021 ApJS 253, 3 (4195 ACT clusters)"),
]


# ---------------- Reference Planck CMB anchor ----------------
PLANCK_OMEGA_M = 0.3158
PLANCK_OMEGA_M_SIG = 0.0073
PLANCK_SIGMA_8 = 0.8111
PLANCK_SIGMA_8_SIG = 0.0060
PLANCK_S_8     = 0.832
PLANCK_S_8_SIG = 0.013


# ---------------- Typical cluster gravitational scales ----------------
def g_vir_cluster_si(M_solar: float, R_Mpc: float) -> float:
    """Virial gravitational acceleration at cluster radius."""
    return G_NEWTON_SI * M_solar * M_SUN_KG / (R_Mpc * MPC_M) ** 2


def u_vir_cluster(M_solar: float, R_Mpc: float) -> float:
    """u = 4 g_vir / a_0."""
    return 4.0 * g_vir_cluster_si(M_solar, R_Mpc) / A_0_MOND_SI


CLUSTER_PROBE_SCALES = [
    ("group_M_1e13_R_0p5Mpc",   1e13, 0.5),
    ("poor_M_5e13_R_0p8Mpc",    5e13, 0.8),
    ("typical_M_2e14_R_1p2Mpc", 2e14, 1.2),
    ("massive_M_5e14_R_1p5Mpc", 5e14, 1.5),
    ("rich_M_1e15_R_2Mpc",      1e15, 2.0),
]
