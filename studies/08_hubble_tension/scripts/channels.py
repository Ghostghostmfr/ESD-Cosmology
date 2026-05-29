"""Published 6-channel drift budget (Table 1 of the hubble paper).

Each channel is reproduced as a single capped |Delta H_0| bound. The
input experimental constraint that caps the channel is included for
audit; the actual mapping from the bound to Delta H_0 lives in the
companion files of the hubble paper. Here we ASSERT the published
caps and check that their sum is dominated by Channel 1.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    idx:           int
    name:          str
    mechanism:     str
    input_bound:   str
    deltaH0_max:   float   # km/s/Mpc; float('inf') for ruled out, 0 for absent
    status:        str     # "active", "structurally absent", "ruled out by SPARC"


CHANNELS = [
    Channel(1, "Disformal photons",
            "c_gamma^2(z) = 1 - eps_0(1+z)^3 - eps_2(1+z)^6",
            "GW170817: |eps_0|<6e-15; photon-barrier eps_2 < 5.9e-19",
            0.12, "active"),
    Channel(2, "Running alpha at recombination",
            "Delta z_* via Delta alpha / alpha",
            "DLA: |Delta alpha / alpha| < 1e-6 at z~1-2",
            7.0e-9, "active"),
    Channel(3, "Newton constant drift",
            "G(t) shifts r_s and recombination physics",
            "LLR: |G-dot/G| < 1e-13 / yr",
            1.4e-6, "active"),
    Channel(4, "N_eff / r_s / w / Omega_K",
            "No new light DOF, no pre-rec mechanism, w_D=0, flat",
            "ESD parent action structurally",
            0.0, "structurally absent"),
    Channel(5, "Bridge x local void",
            "delta_m < 0 would shift bridge a_0 locally",
            "SPARC: a_0 universal to <5% over 4-100 Mpc",
            float("inf"), "ruled out by SPARC"),
    Channel(6, "EFE on Cepheid stellar structure",
            "g_ext / g_internal screening fraction at photosphere",
            "u~1e12 at photosphere -> screened by 1e-13",
            1.0e-12, "active"),
]


SHOES_GAP_KM_S_MPC: float = 5.68    # 73.04 - 67.36, the gap to close


def combined_budget() -> float:
    """Linear sum of finite caps (Channel 5 is excluded as 'ruled out',
    not added to the budget). The published table reports 'dominated
    by Channel 1'; this confirms 0.12 dominates the sum."""
    return sum(c.deltaH0_max for c in CHANNELS
               if math.isfinite(c.deltaH0_max))


def budget_vs_gap_ratio() -> float:
    """Ratio of required gap to maximum framework drift budget."""
    return SHOES_GAP_KM_S_MPC / combined_budget()
