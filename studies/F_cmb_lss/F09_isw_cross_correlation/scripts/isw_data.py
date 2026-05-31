"""ISW x galaxy cross-correlation anchors (Study 35).

In a flat matter-dominated universe the linear gravitational potentials
Phi and Psi are constant in time, so photons gain no net energy
crossing them: the ISW signal is zero. In a Lambda- or DE-dominated
universe Phi+Psi decays as the cosmological constant pulls the
potentials apart, imprinting a temperature shift in CMB photons.

The cross-correlation C_l^{Tg} with low-z galaxy surveys therefore
DIRECTLY probes the dark-energy fraction Omega_L and the late-time
growth-suppression rate. ESD's locked Omega_m = 0.31574 -> Omega_L
= 0.68426 (Identity B C2) provides a parameter-free prediction.

Published measurements:
"""
from __future__ import annotations

import math

# Locked cosmological parameters
OMEGA_M0_LOCKED = 0.31574                 # ESD Identity B C2
OMEGA_L0_LOCKED = 1.0 - OMEGA_M0_LOCKED
H0_KM_S_MPC     = 67.36                   # ESD from Studies 08 + 12 + 31
C_KM_S          = 299792.458

# ---------------- ISW signal-to-noise measurements ----------------
# Each entry: (label, signal_amplitude_A, sigma_A, citation, S/N, z_med)
# A is the ISW amplitude normalised so A=1 means LCDM-consistent.
# Entries with A_obs and sigma_A let us compute tension vs A_ESD=1.
ISW_MEASUREMENTS = [
    ("Giannantonio+ 2012", 1.20, 0.45, "MNRAS 426, 2581 (Planck x 6 surveys)",          4.4, 0.5),
    ("Planck 2015 XXI",    0.93, 0.27, "A&A 594, A21 (Planck PR2 ISW analysis)",        3.4, 0.5),
    ("Stoelzner+ 2018",    0.91, 0.32, "PRD 97, 063506 (Planck x 2dFLenS+SDSS+DES)",    3.0, 0.4),
    ("Hang+ 2021",         1.04, 0.30, "MNRAS 501, 1481 (DES Y3 GOLD x Planck SMICA)",  3.5, 0.5),
    ("Krolewski+ 2024",    1.02, 0.28, "PRD 110, 083537 (unWISE x Planck PR4)",         3.6, 1.2),
    ("Lopes+ 2024",        0.86, 0.28, "MNRAS 528, 3242 (CatWISE2020 x Planck SMICA)",  3.1, 1.0),
]


# ---------------- Granett stacked-supervoid result ----------------
# This is the controversial 4-sigma SIGNAL (cold spot in supervoid
# stacking from Granett, Neyrinck & Szapudi 2008 ApJL 683 L99):
GRANETT_2008_AMPLITUDE_VS_LCDM = 5.0      # Granett's signal is ~5x LCDM expectation
GRANETT_2008_SIGNIFICANCE      = 4.4      # sigma above zero, BUT ~3.7sigma above LCDM


# ---------------- ESD prediction ----------------
def A_isw_esd() -> float:
    """ESD predicts the LCDM ISW amplitude (Study 19 theorem: linear
    perturbations unmodified; Omega_L = 0.68426 locked by Identity B)."""
    return 1.0


def Omega_L_locked() -> float:
    return OMEGA_L0_LOCKED


def potential_decay_rate(z: float) -> float:
    """d ln(D+/a)/d ln a at redshift z; ISW source term, normalised
    so 0 = matter dom (no signal) and ~ -0.5 today (Lambda-dom).

    Crude approximation: D+(a) ~ a in matter dom, decays as a^(f-1)
    in Lambda dom with f = Omega_m(a)^0.55."""
    Em = OMEGA_M0_LOCKED * (1.0 + z) ** 3
    El = OMEGA_L0_LOCKED
    Omega_m_z = Em / (Em + El)
    f_z = Omega_m_z ** 0.55
    return f_z - 1.0      # = d ln(D+/a)/d ln a = f - 1


def amplitude_scaling_omega_lambda(omega_L_alt: float) -> float:
    """How much would an alternative Omega_L change the ISW amplitude?

    Leading-order scaling (Cooray 2002, Crittenden-Turok 1996):
        A_ISW ~ Omega_L * (1 - f(z_eff))
    With Omega_L = 0.68426 (locked) the ratio relative to a model
    with arbitrary Omega_L is direct."""
    return omega_L_alt / OMEGA_L0_LOCKED
