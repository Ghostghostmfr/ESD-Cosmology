"""ESD inflation prediction: Starobinsky-plateau slow-roll.

Master Ch. 15 (parent-action sector for inflation): the ESD parent
action admits a unique Starobinsky-class plateau attractor when the
disformal B(D)*partial-D-partial-D coefficient runs to its high-D
fixed point. Single-field slow-roll on the plateau gives
   epsilon = 3 / (4 N_e^2)
   eta     = -1 / N_e
yielding
   r   = 16 epsilon = 12 / N_e^2
   n_s = 1 + 2 eta - 6 epsilon ~ 1 - 2 / N_e

No new free parameters: N_e is set by reheating-temperature
constraints to N_e ~ 50-60.
"""
from __future__ import annotations


def epsilon_starobinsky(N_e: float) -> float:
    return 3.0 / (4.0 * N_e ** 2)


def eta_starobinsky(N_e: float) -> float:
    return -1.0 / N_e


def r_predicted(N_e: float) -> float:
    """Tensor-to-scalar ratio at e-fold N_e."""
    return 16.0 * epsilon_starobinsky(N_e)


def n_s_predicted(N_e: float) -> float:
    """Scalar spectral index at e-fold N_e."""
    return 1.0 + 2.0 * eta_starobinsky(N_e) - 6.0 * epsilon_starobinsky(N_e)


def consistency_relation(N_e: float) -> float:
    """Single-field consistency: n_t = -r/8."""
    return -r_predicted(N_e) / 8.0
