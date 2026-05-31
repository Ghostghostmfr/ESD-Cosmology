"""ESD GW friction prediction: Study 21 gives gamma = 0 (no extra friction)."""
from __future__ import annotations

H_0_LOCKED = 67.36


def gw_friction_gamma() -> float:
    """ESD-predicted modified-gravity GW friction parameter.

    Study 21 (GW sector derivation) shows the disformal B(D) channel
    has vanishing transverse-traceless friction at sub-horizon scales
    because the conformal sector A^2(D) carries all the metric
    perturbation. Result: gamma = 0, i.e. d_L^GW = d_L^EM identically."""
    return 0.0


def d_L_ratio(z: float) -> float:
    """d_L^GW(z) / d_L^EM(z) - ESD prediction."""
    return 1.0   # for any z, since gamma = 0


def H_0_predicted_siren() -> float:
    """ESD-predicted standard-siren H_0 - matches CMB-locked value."""
    return H_0_LOCKED
