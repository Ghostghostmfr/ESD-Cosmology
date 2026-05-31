"""ESD prediction for Pantheon+ residuals - identical to LCDM background."""
from __future__ import annotations
from pantheon_data import H_0_LOCKED, OMEGA_M_LOCKED, mu_predicted


def mu_esd(z: float) -> float:
    """ESD-predicted distance modulus - LCDM-identical at locked params."""
    return mu_predicted(z)


def residual_esd(z: float, mu_obs: float) -> float:
    return mu_obs - mu_esd(z)
