"""esd_core - shared locked constants and identities for the
Energy-Space-Displacement (ESD) framework.

Every cosmological study in this repository imports its locked numbers
from this package so that no two studies can silently drift apart.
Do not recompute or rewrite these values inside individual studies.

See [HigginsonESDFramework2026] for the full derivation of every
constant and identity exposed here.
"""

# Structural / closure-pool constants
from .constants import (
    C_CHANNEL,
    F12,
    LN_PHI,
    M_PL_GEV,
    N_PATH,
    N_PATH_D,
    PHI,
    Q_BRIDGE,
    S_NORM,
    beta,
    c,
    c2,
    c4,
    ln_phi,
    q,
)

# Cosmological identities and reading selector
from .identities import (
    OMEGA_B_INPUT,
    OMEGA_B_LOCK,
    OMEGA_B_PRIMARY,
    OMEGA_DM_FROM_IDB,
    OMEGA_DM_LOCK,
    OMEGA_DM_OVER_B_LOCK,
    OMEGA_LAMBDA_LOCK,
    OMEGA_M_LOCK,
    Reading,
    identity_B_rhs,
    omega_b,
    omega_b_closure_pool,
    omega_dm,
    omega_dm_from_identity_B,
    omega_lambda,
    omega_matter,
)

# Reading-independent derived cosmology
from .cosmology import (
    C_LIGHT_M_S,
    MPC_M,
    a_zero,
    hubble_inverse_seconds,
    lambda_D_over_RH,
    m_D,
)

# Inflation and reheating chain
from .inflation import (
    ALPHA_STAR,
    DELTA_REH,
    GAMMA_CHI_GEV,
    M_CHI_GEV,
    N_E_STAR,
    N_E_TOTAL,
    T_REH_GEV,
    gamma_chi_gev,
    t_reh_gev,
)

# Primordial power-spectrum locks
from .primordial import (
    A_S_PIVOT,
    ALPHA_S_STAR,
    K_PIVOT_MPC,
    NS_PLANCK_BAND,
    NS_PLANCK_MEAS,
    NS_PLANCK_SIGMA,
    NS_STAR,
    N_T_STAR,
    R_TENSOR,
)

__all__ = [
    # constants
    "PHI",
    "F12",
    "N_PATH",
    "N_PATH_D",
    "M_PL_GEV",
    "S_NORM",
    "beta",
    "c",
    "c2",
    "c4",
    "ln_phi",
    "q",
    "LN_PHI",
    "C_CHANNEL",
    "Q_BRIDGE",
    # identities
    "OMEGA_B_PRIMARY",
    "OMEGA_B_INPUT",
    "OMEGA_B_LOCK",
    "OMEGA_DM_FROM_IDB",
    "OMEGA_DM_LOCK",
    "OMEGA_DM_OVER_B_LOCK",
    "OMEGA_LAMBDA_LOCK",
    "OMEGA_M_LOCK",
    "Reading",
    "identity_B_rhs",
    "omega_b",
    "omega_b_closure_pool",
    "omega_dm",
    "omega_dm_from_identity_B",
    "omega_lambda",
    "omega_matter",
    # cosmology
    "C_LIGHT_M_S",
    "MPC_M",
    "a_zero",
    "hubble_inverse_seconds",
    "lambda_D_over_RH",
    "m_D",
    # inflation
    "ALPHA_STAR",
    "DELTA_REH",
    "GAMMA_CHI_GEV",
    "M_CHI_GEV",
    "N_E_STAR",
    "N_E_TOTAL",
    "T_REH_GEV",
    "gamma_chi_gev",
    "t_reh_gev",
    # primordial
    "A_S_PIVOT",
    "ALPHA_S_STAR",
    "K_PIVOT_MPC",
    "NS_PLANCK_BAND",
    "NS_PLANCK_MEAS",
    "NS_PLANCK_SIGMA",
    "NS_STAR",
    "N_T_STAR",
    "R_TENSOR",
]

__version__ = "0.1.0"
