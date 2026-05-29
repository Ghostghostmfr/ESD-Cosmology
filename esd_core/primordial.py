"""Primordial power-spectrum locks of the ESD framework.

For Starobinsky-class inflation at the pivot e-fold N_*:

    n_s     = 1 - 2 / N_*
    r       = 12 / N_*^2
    n_t     = -r / 8
    alpha_s = -2 / N_*^2     (running of n_s)

The amplitude A_s and pivot scale k_p are external observational
anchors (COBE / Planck), not framework-locked.

See Ch. 15 of [HigginsonESDFramework2026].
"""

from .inflation import N_E_STAR

# ----------------------------- framework locks ----------------------------
NS_STAR: float = 1.0 - 2.0 / N_E_STAR                 # ~0.9611
R_TENSOR: float = 12.0 / (N_E_STAR ** 2)              # ~0.00453
N_T_STAR: float = -R_TENSOR / 8.0                     # ~-5.7e-4
ALPHA_S_STAR: float = -2.0 / (N_E_STAR ** 2)          # ~-7.5e-4

# ----------------------------- external anchors ---------------------------
A_S_PIVOT: float = 2.10e-9                            # COBE amplitude
K_PIVOT_MPC: float = 0.05                             # Mpc^-1

# Planck 2018 measured central value and 1-sigma (for sigma-distance audits).
NS_PLANCK_MEAS: float = 0.9649
NS_PLANCK_SIGMA: float = 0.0042
NS_PLANCK_BAND: tuple[float, float] = (
    NS_PLANCK_MEAS - NS_PLANCK_SIGMA,
    NS_PLANCK_MEAS + NS_PLANCK_SIGMA,
)
