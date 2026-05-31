"""S2 / Sgr A* anchors (GRAVITY+ 2020)."""
from __future__ import annotations
G_M3_KG_S2 = 6.67430e-11
M_SUN_KG   = 1.98892e30
AU_M       = 1.495978707e11

M_BH_MSUN: float = 4.297e6            # GRAVITY+ 2020
M_BH_KG:   float = M_BH_MSUN * M_SUN_KG

S2_A_AU:   float = 970.0              # GRAVITY+ 2020 semi-major axis
S2_E:      float = 0.8847
S2_RPERI_M: float = S2_A_AU * AU_M * (1.0 - S2_E)
S2_RAPO_M:  float = S2_A_AU * AU_M * (1.0 + S2_E)

G_PERI = G_M3_KG_S2 * M_BH_KG / S2_RPERI_M ** 2
G_APO  = G_M3_KG_S2 * M_BH_KG / S2_RAPO_M ** 2

F_SP_MEAS: float = 1.10
F_SP_ERR:  float = 0.19
