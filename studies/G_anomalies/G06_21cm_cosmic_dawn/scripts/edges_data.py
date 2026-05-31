"""EDGES / SARAS-3 21cm cosmic-dawn anchors and constants."""
from __future__ import annotations

# -------------------- physical / cosmological constants -------------------
C_LIGHT_KM_S: float    = 299_792.458
MPC_KM: float          = 3.0857e19
G_NEWTON_SI: float     = 6.6743e-11
A0_MOND_SI: float      = 1.2015e-10            # Study 12 a_0 anchor
T_CMB_K: float         = 2.7255                # Fixsen 2009
NU_21_MHZ: float       = 1420.4057517
M_PROTON_KG: float     = 1.6726e-27
K_B_J_K: float         = 1.380649e-23
SIGMA_T_M2: float      = 6.6524587e-29
H_PLANCK_J_S: float    = 6.62607015e-34

# Planck 2018 cosmology
H0_KM_S_MPC: float     = 67.36
OMEGA_M: float         = 0.3158
OMEGA_B: float         = 0.04930
OMEGA_L: float         = 1.0 - OMEGA_M
H_REDUCED: float       = H0_KM_S_MPC / 100.0
RHO_CRIT_KG_M3: float  = 1.8788e-26 * H_REDUCED ** 2
RHO_B_KG_M3: float     = OMEGA_B * RHO_CRIT_KG_M3
N_H0_M3: float         = (0.76 * RHO_B_KG_M3) / M_PROTON_KG  # hydrogen num density today

# -------------------- ESD framework H_0 prediction ------------------------
H0_ESD: float          = 67.36
H0_ESD_SIGMA: float    = 0.54

# -------------------- cosmic-dawn target redshift -------------------------
# EDGES absorption-trough centre is at nu ~ 78 MHz -> z ~ 17.2.
NU_EDGES_MHZ: float    = 78.1
Z_COSMIC_DAWN: float   = NU_21_MHZ / NU_EDGES_MHZ - 1.0    # ~ 17.19

# Thermal-decoupling redshift (Compton coupling efficiency drops here).
Z_THERMAL_DECOUPLING: float = 200.0

# -------------------- 21cm brightness-temperature anchors -----------------
# Standard adiabatic prediction (Furlanetto+ 2006, Pritchard & Loeb 2012):
#   T_b at the cosmic-dawn trough is in the range -150 to -250 mK,
#   depending on how fully T_s couples to T_gas before X-ray heating.
T_B_LCDM_CENTRAL_MK: float = -220.0
T_B_LCDM_SIGMA_MK: float   = 40.0

# EDGES Bowman+ 2018, Nature 555, 67. Absorption depth at 78 MHz:
T_B_EDGES_MK: float            = -500.0
T_B_EDGES_SIGMA_PLUS_MK: float = 200.0       # downward (toward 0) error
T_B_EDGES_SIGMA_MINUS_MK: float= 200.0       # upward (toward more negative)

# SARAS-3 Singh+ 2022, Nature Astronomy 6, 607.
# 95.3 % CL rejection of the EDGES best-fit profile.
# Equivalent 2-sigma envelope for T_b at z ~ 17:
T_B_SARAS3_UPPER_MK: float =  50.0           # mK (residual scatter)
T_B_SARAS3_LOWER_MK: float = -300.0          # mK (depth rejected below this)

# -------------------- representative cosmic-dawn scale --------------------
# Mean-IGM acceleration scale at z = z_cosmic_dawn:
#   g_cosmic = H(z) * v_pec_IGM
# where the dominant peculiar velocity at cosmic dawn is set by linear-
# theory growth, v_pec ~ 10-50 km/s.
V_PEC_IGM_KM_S: float = 30.0
