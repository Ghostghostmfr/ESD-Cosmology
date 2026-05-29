"""ESD framework's locked predictions for the BTFR study.

Public API:
  a_zero_SI(H0)         - locked MOND-scale acceleration [m/s^2], from esd_core.
  PHI, Q_EXP, S_PHI,
  B_PHI, C_PHI          - golden-ratio closure constants (no fit).
  R_esd(u)              - anomalous-acceleration ratio R(u) = s/(u^phi + b*u^q + c).
  G_btfr(u)             - BTFR prefactor G(u) = u*(1 + R(u))^2 / 4.
  predicted_btfr_slope() - deep-MOND asymptote: slope of log V_f vs log M_b = 1/4.
  baryonic_mass_solar(L36, MHI, Upsilon_*) - SPARC M_b reconstruction.

Constants are locked by the golden ratio (Higginson 2026, DOI
10.5281/zenodo.20400008):

    phi = (1 + sqrt(5)) / 2
    q   = 2 * ln(phi) / phi
    s   = 16 * phi + 1
    b   = phi^6 - 2
    c   = (4 * ln(phi) - 1) / phi

The BTFR equation derived from the framework is

    V_f^4 = G(u) * G * M_b * a_0,    u = 4 * g_N / a_0

reducing to MOND (V_f^4 = G * M_b * a_0) when G(u) = 1.
"""

from __future__ import annotations

import math

from esd_core.cosmology import a_zero

# Golden-ratio closure constants (locked, identical to the paper).
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
Q_EXP: float = 2.0 * math.log(PHI) / PHI
S_PHI: float = 16.0 * PHI + 1.0
B_PHI: float = PHI**6 - 2.0
C_PHI: float = (4.0 * math.log(PHI) - 1.0) / PHI

# SPARC mass-to-light defaults (population synthesis).
UPSILON_DISK: float = 0.5
UPSILON_BULGE: float = 0.7

# Standard physical constants.
G_SI: float = 6.674e-11        # m^3 kg^-1 s^-2
MSUN_KG: float = 1.989e30      # kg


def a_zero_SI(H0_kms_per_mpc: float = 67.36) -> float:
    """Locked MOND-scale acceleration a_0 [m / s^2]."""
    return a_zero(H0_kms_per_mpc)


def predicted_btfr_slope() -> float:
    """Deep-MOND asymptote: slope of log10(V_f) vs log10(M_b)."""
    return 0.25


def R_esd(u: float) -> float:
    """Anomalous-acceleration ratio R(u) = s / (u^phi + b*u^q + c)."""
    denom = u**PHI + B_PHI * u**Q_EXP + C_PHI
    return S_PHI / denom


def G_btfr(u: float) -> float:
    """BTFR prefactor G(u) = u * (1 + R(u))^2 / 4."""
    return u * (1.0 + R_esd(u))**2 / 4.0


def baryonic_mass_solar(L36_1e9_Lsun: float,
                        MHI_1e9_Msun: float,
                        upsilon_star: float = UPSILON_DISK,
                        helium_correction: float = 1.33) -> float:
    """Reconstruct M_b [Msun] from SPARC's 3.6um luminosity and HI mass.

    M_b = upsilon_star * L_3.6 + helium_correction * M_HI

    Defaults follow Higginson 2026 / Lelli et al. 2016: stellar M/L
    at 3.6um = 0.5, helium correction = 1.33.
    """
    M_star = upsilon_star * L36_1e9_Lsun * 1.0e9
    M_gas = helium_correction * MHI_1e9_Msun * 1.0e9
    return M_star + M_gas
