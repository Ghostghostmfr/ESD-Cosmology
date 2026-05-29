"""Multi-messenger GW + EM observations used as inputs to Study 09."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GWEvent:
    name:        str
    delta_t_s:   float     # GRB lag relative to GW merger
    D_lum_mpc:   float     # luminosity distance to host
    ref:         str
    has_em:      bool      # True iff EM counterpart confirmed


EVENTS = [
    GWEvent("GW170817 + GRB170817A",
            delta_t_s=1.74,
            D_lum_mpc=40.0,
            ref="Abbott+ 2017, ApJL 848, L13",
            has_em=True),
    # All subsequent BNS detections lack EM counterparts; included for
    # reference but they don't tighten the speed bound.
    GWEvent("GW190425 (BNS, no EM)",
            delta_t_s=float("nan"),
            D_lum_mpc=159.0,
            ref="Abbott+ 2020, ApJL 892, L3",
            has_em=False),
    GWEvent("GW230529 (NSBH, no EM)",
            delta_t_s=float("nan"),
            D_lum_mpc=201.0,
            ref="Abbott+ 2024, ApJL 970, L34",
            has_em=False),
]
