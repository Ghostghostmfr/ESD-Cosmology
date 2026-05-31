"""
Gravitational-wave sector theory for ESD.

Per Study 21 (`C02_gravitational_wave_applicability`), the closure-pool kernel R(u) does not
apply to propagating tensor modes. This is because a gravitational wave is
a fluctuation of the metric itself, not a bound system relative to a
spectator frame, failing axiom (A1).

Therefore, the GW sector of ESD is identical to General Relativity:
- Propagation speed is exactly `c`.
- Polarizations are purely tensor (plus, cross).
- There is no graviton mass.

This module provides the theoretical predictions for the observables tested
in Study 23:
- The Hellings-Downs correlation curve for a tensor-polarized SGWB.
- The expected spectral index `gamma = 13/3` for an SGWB sourced by
  supermassive black hole binaries (SMBHBs) evolving purely through
  gravitational radiation.
"""
from __future__ import annotations

import numpy as np


def hellings_downs_tensor(theta_rad: np.ndarray) -> np.ndarray:
    """
    Computes the Hellings-Downs correlation for a tensor-polarized,
    isotropic, and unpolarized stochastic gravitational-wave background.

    Args:
        theta_rad: Array of angular separations between pulsars in radians.

    Returns:
        Array of expected correlation values.
    """
    # The ORF is often written with x = (1 - cos(theta))/2
    x = (1.0 - np.cos(theta_rad)) / 2.0
    return 1.5 * x * np.log(x) - 0.25 * x + 0.5


# The expected spectral index for an SGWB from a population of SMBHBs
# whose orbital evolution is dominated by GW emission.
# h_c(f)^2 is proportional to f^(-gamma).
SMBHB_EXPECTED_GAMMA = 13.0 / 3.0
