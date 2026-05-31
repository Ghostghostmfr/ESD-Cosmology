"""GW friction anchors."""
from __future__ import annotations

# GW170817 / NGC 4993 (Abbott+ 2017 PRL 119 161101)
GW170817 = {
    "dL_EM_Mpc":   40.7,
    "dL_EM_err":   2.4,
    "dL_GW_Mpc":   43.8,
    "dL_GW_errp":  2.9,
    "dL_GW_errm":  6.9,
    "z":           0.0099,
}

# Mukherjee+ 2021 MNRAS 502 1136 — LVK O3 + dark sirens
LVK_O3 = {
    "alpha_M_med":  -3.2,
    "alpha_M_errp":  3.4,
    "alpha_M_errm":  3.4,   # symmetrized 90% CL ~ +/- 3.4
    "bound_90pct":   6.6,
}
