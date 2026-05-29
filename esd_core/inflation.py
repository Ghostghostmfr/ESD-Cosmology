"""Inflation and reheating chain for the Energy-Space-Displacement framework.

All values follow from the parent-action conformal weight beta = sqrt(2/3)
and the Fibonacci e-fold lock F_12 ln(phi). See Ch. 15 of
[HigginsonESDFramework2026].

Closure chain
-------------
    alpha_*  = sqrt(2/3)            (Starobinsky attractor)
    N_total  = F_12 ln(phi)         = 69.295 e-folds
    Delta_reh = 17.82               (parent-action conformal reheating delay)
    N_*      = N_total - Delta_reh  = 51.475
    Gamma_chi = m_chi^3 / (24 pi M_Pl^2)
    T_reh    = (90 / (pi^2 g_*))^(1/4) * sqrt(Gamma_chi * M_Pl)

The factor 1/(24 pi) is the four-channel sum of the parent-action
Higgs-portal decay (4 doublet channels x 1/(8 pi) x 1/2 identical-final-
state, equivalent to the Bezrukov-Gorbunov 1/(6 pi) when N_h = 4 channels
are summed before the 1/2).
"""

import math

from .constants import F12, M_PL_GEV, beta, ln_phi

# ----------------------------- e-fold ledger ------------------------------
# Total e-folds: Fibonacci F_12 times the parent log-ratio.
N_E_TOTAL: float = F12 * ln_phi                       # ~69.295

# Reheating delay (LOCK; closes Master Ch.15 line-192 open item).
DELTA_REH: float = 17.82                              # e-folds

# Pivot e-folds before end of inflation.
N_E_STAR: float = N_E_TOTAL - DELTA_REH               # ~51.475

# ----------------------------- reheating chain ----------------------------
# COBE-anchored scalaron mass.
M_CHI_GEV: float = 3.336e13

# Conformal weight (re-exported for inflation users).
ALPHA_STAR: float = beta                              # sqrt(2/3)


def gamma_chi_gev() -> float:
    """Parent-action Higgs-portal decay width.

        Gamma_chi = m_chi^3 / (24 pi M_Pl^2)
    """
    return M_CHI_GEV**3 / (24.0 * math.pi * M_PL_GEV**2)


def t_reh_gev(g_star: float = 106.75) -> float:
    """Reheating temperature from instantaneous-thermalisation matching.

        T_reh = (90 / (pi^2 g_*))^(1/4) sqrt(Gamma_chi M_Pl)
    """
    Gamma = gamma_chi_gev()
    return (90.0 / (math.pi**2 * g_star))**0.25 * math.sqrt(Gamma * M_PL_GEV)


# Cached LOCK values at the framework's g_* = 106.75 baseline.
GAMMA_CHI_GEV: float = gamma_chi_gev()                # ~83.3
T_REH_GEV: float = t_reh_gev()                        # ~7.70e9
