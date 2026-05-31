"""kSZ pairwise-velocity anchors (Study 37).

The kinematic Sunyaev-Zel'dovich (kSZ) effect is the CMB temperature
shift induced by Compton scattering off the hot electron gas in
moving clusters. The pairwise-velocity estimator (Hand+ 2012)
measures the mean radial relative velocity v_12(r) of cluster pairs
as a function of separation, isolating the linear-regime velocity
field sourced by the large-scale matter distribution.

In linear theory:
   v_12(r) ~ -2/3 * H(z) * f(z) * sigma_8^2 * dot_correlation_function

Sensitivity products:
   amplitude ~ f(z) * sigma_8 * tau_bar
where tau_bar is the mean optical depth of the cluster sample
(the dominant systematic, degenerate with growth).

By Study 19's applicability theorem, R(u) does NOT modify the
linear velocity field. ESD therefore predicts the LCDM amplitude
identically, with f(z) * sigma_8 from Study 19's locked values.

Published kSZ pairwise-velocity measurements:
"""
from __future__ import annotations

OMEGA_M0_LOCKED = 0.31574
SIGMA_8_LOCKED  = 0.8111

# Each entry: (label, amplitude A/A_LCDM, sigma_A, detection significance, citation)
KSZ_MEASUREMENTS = [
    ("Hand+ 2012",        1.00, 0.30, 3.8,
     "PRL 109, 041101 (ACT eq. survey x BOSS DR9 LRG, first detection)"),
    ("Soergel+ 2016",     1.15, 0.30, 4.2,
     "MNRAS 461, 3172 (SPT-SZ x DES Y1, 7600 deg^2)"),
    ("De Bernardis+ 2017", 0.90, 0.28, 3.6,
     "JCAP 03, 008 (ACT x BOSS DR11 CMASS)"),
    ("Sugiyama+ 2018",    0.78, 0.24, 3.3,
     "MNRAS 473, 2737 (Planck x BOSS DR12 photo-z)"),
    ("Calafut+ 2021",     1.04, 0.19, 5.5,
     "PRD 104, 043502 (ACT DR5 x BOSS DR15)"),
    ("Schiappucci+ 2023", 1.02, 0.20, 5.0,
     "PRD 107, 042004 (SPT-3G x DES Y3, 1500 deg^2)"),
    ("Hadzhiyska+ 2024",  0.97, 0.14, 7.1,
     "PRL 132, 191103 (ACT DR6 x DESI BGS+LRG, 8500 deg^2)"),
]


# ---------------- Reference Planck-LCDM benchmark ----------------
PLANCK_F_SIGMA_8_Z0p55 = 0.460       # f(z)*sigma_8 at z~0.55 (BOSS/eBOSS pivot)
PLANCK_F_SIGMA_8_SIG   = 0.018


def f_sigma_8_esd(z: float) -> float:
    """ESD prediction (= LCDM): f(z) * sigma_8(z) at redshift z.

    sigma_8(z) = sigma_8(0) * D_+(z)/D_+(0); f(z) = Omega_m(z)^0.55.
    Use approximation D_+(z)/D_+(0) ~ Omega_m(z)^0.6 / (1+z)."""
    E2 = OMEGA_M0_LOCKED * (1.0 + z) ** 3 + (1.0 - OMEGA_M0_LOCKED)
    Omega_m_z = OMEGA_M0_LOCKED * (1.0 + z) ** 3 / E2
    f_z = Omega_m_z ** 0.55
    # crude D_+(z) approx (Wang-Steinhardt integration):
    D_plus_ratio = (Omega_m_z ** 0.6) / (1.0 + z) / OMEGA_M0_LOCKED ** 0.6
    sigma_8_z = SIGMA_8_LOCKED * D_plus_ratio
    return f_z * sigma_8_z
