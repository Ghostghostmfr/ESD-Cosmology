"""ESD prediction for GW friction.

The ESD tensor sector reduces identically to GR (Study 19
applicability theorem; no extra gravitational degree of freedom in
the metric sector). Therefore:

    alpha_M = 0      (running-Planck-mass coefficient)
    d_L^GW / d_L^EM = 1   identically.

These are structural predictions, h-independent.
"""
from __future__ import annotations
import math


def alpha_M_ESD(H0: float = 67.36) -> float:
    """Structural: tensor sector = GR ==> 0 identically."""
    return 0.0


def distance_ratio(z: float, H0: float = 67.36) -> float:
    """d_L^GW / d_L^EM under ESD. Identically 1."""
    return math.exp(-0.5 * alpha_M_ESD(H0) * z)   # = 1 since alpha_M=0
