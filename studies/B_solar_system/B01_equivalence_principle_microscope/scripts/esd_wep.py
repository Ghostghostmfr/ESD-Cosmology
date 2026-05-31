"""ESD WEP-violation predictor (Master Book Ch. 4 sec. 4.7).

Composition-dependent Eotvos ratio between species A and B:

    eta_{A,B}(u) = beta_m^2(u) * (beta_Z/beta_m)(u) * |Delta f_EM|

The universal beta_m piece renormalises G and is invisible to the EP;
only the gauge-bridge beta_Z piece, gated by the EM binding fraction,
produces a composition-dependent signal. The beta_m^2 screening factor
inherited from Cassini-PPN safety drives the prediction far below
experimental sensitivity.
"""
from __future__ import annotations

from wep_data import (
    BETA_M_SQ_EARTH,
    BETA_Z_OVER_BETA_M_EARTH,
    DELTA_F_EM_PT_TI,
)


def eta_esd(beta_m_sq: float = BETA_M_SQ_EARTH,
            beta_z_over_beta_m: float = BETA_Z_OVER_BETA_M_EARTH,
            delta_f_em: float = DELTA_F_EM_PT_TI) -> float:
    """ESD-predicted Eotvos ratio for a Pt-Ti pair at Earth."""
    return beta_m_sq * beta_z_over_beta_m * abs(delta_f_em)


def eta_breakdown() -> dict:
    return {
        "beta_m_sq_screening":     BETA_M_SQ_EARTH,
        "beta_Z_over_beta_m":      BETA_Z_OVER_BETA_M_EARTH,
        "delta_f_em_pt_ti":        DELTA_F_EM_PT_TI,
        "eta_pt_ti_esd":           eta_esd(),
    }
