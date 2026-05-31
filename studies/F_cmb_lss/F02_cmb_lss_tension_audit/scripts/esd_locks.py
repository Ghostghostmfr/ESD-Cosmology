"""Framework cosmological locks for Study 06.

Single source of truth for the audit study. Every number here is
imported from `esd_core` so it cannot silently drift from the other
studies, with one exception:

  S_8 = 0.830426    [provenance pointer]
    Not derived in closed form -- requires a transfer function. The
    canonical computation lives in
      studies/F01_linear_cosmology_closure/scripts/compute_s8.py
    where it is computed using CLASS at the locked (Omega_m, Omega_b,
    n_s, A_s, H_0). The value 0.830426 is the headline output of
    that script's CLASS-internal cross-check. We hard-code it here
    (with provenance) so Study 06 stays self-contained: pip-installing
    `classy` is not required to run the audit.

If you want to recompute S_8 from scratch, run Study 01's
`make compute_s8` (requires CLASS), then update the constant below.
"""

from __future__ import annotations

import esd_core as ESD

# --- Identity A (dark-energy / matter split) -----------------------------
OMEGA_LAMBDA: float = ESD.OMEGA_LAMBDA_LOCK
OMEGA_M:      float = ESD.OMEGA_M_LOCK

# --- Identity B (baryon / dark-matter partition) -------------------------
# PRIMARY reading: Omega_b matched to Planck; Omega_DM solved from Id B.
OMEGA_B_PRIMARY:  float = ESD.OMEGA_B_INPUT
OMEGA_DM_PRIMARY: float = ESD.OMEGA_DM_FROM_IDB
# CLOSURE-POOL reading: Omega_b derived from c alone.
OMEGA_B_CLOSURE_POOL:  float = ESD.OMEGA_B_LOCK
OMEGA_DM_CLOSURE_POOL: float = ESD.OMEGA_DM_LOCK

# --- Primordial scalar / tensor locks (Starobinsky-class at N_*) ---------
NS_STAR:      float = ESD.NS_STAR
R_TENSOR:     float = ESD.R_TENSOR
N_T_STAR:     float = ESD.N_T_STAR
ALPHA_S_STAR: float = ESD.ALPHA_S_STAR
A_S_PIVOT:    float = ESD.A_S_PIVOT
K_PIVOT_MPC:  float = ESD.K_PIVOT_MPC
N_E_STAR:     float = ESD.N_E_STAR

# --- Inflation / reheating chain ----------------------------------------
T_REH_GEV: float = ESD.T_REH_GEV

# --- MOND-scale acceleration (Identity-B locked) ------------------------
def a0_si(H0_kms_per_mpc: float = 67.36) -> float:
    return ESD.a_zero(H0_kms_per_mpc)

# --- S_8 from Study 01 / CLASS cross-check ------------------------------
S_8_LOCK: float = 0.830426
S_8_PROVENANCE: str = (
    "studies/F01_linear_cosmology_closure/scripts/compute_s8.py "
    "(CLASS-internal sigma8 at locked Omega_m, Omega_b, n_s, A_s, H_0)"
)
