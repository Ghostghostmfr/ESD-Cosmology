"""ESD framework's locked prediction for the MOND acceleration a_0.

Standalone paper:
    Higginson, J. P. (2026). Derivation of the MOND Acceleration Scale
    from the Energy-Space Displacement Framework.
    Zenodo. DOI: 10.5281/zenodo.20399682

Key identity (Eq. a0_cosmo of the standalone paper):

    a_0 = c * H_0 * sqrt((3 Omega_DM + Omega_b) / (8 pi))

Two reading-modes are exposed here:

  paper_mode (boundary-input):
      Uses Planck 2018 mean values directly --- Omega_DM = 0.264,
      Omega_b = 0.049 --- reproducing the paper's headline
      a_0 = 1.198e-10 m/s^2 at H_0 = 67.4 km/s/Mpc.

  framework_mode (Identity-B locked):
      Uses the closure 8 pi c^4 Omega_m, which gives the slightly
      different combination 3 Omega_DM + Omega_b = 0.8470.
      Numerical value a_0(67.4) = 1.2022e-10 m/s^2.

Both are reading-independent in the sense of esd_core.identities:
they differ only in whether one feeds Planck (Omega_DM, Omega_b)
in directly or routes them through Identity B's closure.

No fit parameters in either mode.
"""

from __future__ import annotations

import math

from esd_core.cosmology import C_LIGHT_M_S, MPC_M, a_zero, hubble_inverse_seconds
from esd_core.identities import identity_B_rhs

# -- Planck 2018 boundary values (used by the standalone paper) --------------
OMEGA_DM_PLANCK: float = 0.264
OMEGA_B_PLANCK: float = 0.049
H0_PLANCK: float = 67.36           # Planck 2018 (km/s/Mpc)
H0_PAPER: float = 67.4             # rounded value used in standalone paper
H0_SH0ES: float = 73.04            # Riess+2022 SH0ES (km/s/Mpc)

# -- Canonical RAR measurement (McGaugh+2016) --------------------------------
A0_RAR_MCGAUGH: float = 1.20e-10   # m/s^2
A0_RAR_MCGAUGH_ERR: float = 0.026e-10


def a0_paper_mode(H0_kms_per_mpc: float = H0_PAPER,
                  Omega_DM: float = OMEGA_DM_PLANCK,
                  Omega_b: float = OMEGA_B_PLANCK,
                  f_b: float = 1.0 / 3.0) -> float:
    """Boundary-input a_0 using direct Planck values (standalone paper mode).

        a_0 = c * H_0 * sqrt((3 Omega_DM + Omega_b) / (8 pi))   if f_b = 1/3

    (More generally the baryon weight f_b multiplies Omega_b/Omega_DM
    inside the sqrt -- this is the same scan the paper reports for the
    f_b sensitivity figure; the 1/3 isotropy value is the prediction.)
    """
    H0 = hubble_inverse_seconds(H0_kms_per_mpc)
    combination = Omega_DM + (3.0 * f_b) * Omega_b
    # Recover the standard form when f_b = 1/3:
    #   Omega_DM + Omega_b/1  = ...
    # but the paper's actual scan uses
    #   a_0 = c sqrt(G (rho_DM + f_b rho_b))
    # = c H_0 sqrt((Omega_DM + f_b Omega_b) * 3/(8 pi)).
    # The 1/3 prediction reproduces (3 Omega_DM + Omega_b)/(8 pi).
    combination_density = Omega_DM + f_b * Omega_b
    return C_LIGHT_M_S * H0 * math.sqrt(3.0 * combination_density / (8.0 * math.pi))


def a0_framework_mode(H0_kms_per_mpc: float = H0_PLANCK) -> float:
    """Identity-B locked a_0, exactly as exported by esd_core.cosmology."""
    return a_zero(H0_kms_per_mpc)


def a0_milgrom_coincidence(H0_kms_per_mpc: float = H0_PAPER) -> float:
    """Milgrom's 1/(2 pi) coincidence: a_0 = c H_0 / (2 pi)."""
    H0 = hubble_inverse_seconds(H0_kms_per_mpc)
    return C_LIGHT_M_S * H0 / (2.0 * math.pi)


def esd_coefficient_paper() -> float:
    """The 0.18288 coefficient of the standalone paper (Planck mean values)."""
    return math.sqrt((3.0 * OMEGA_DM_PLANCK + OMEGA_B_PLANCK) / (8.0 * math.pi))


def esd_coefficient_framework() -> float:
    """The 0.18358 coefficient from Identity-B closure (locked framework)."""
    return math.sqrt(identity_B_rhs() / (8.0 * math.pi))


def fb_sensitivity_scan(n: int = 401):
    """Scan baryon weight f_b in [0,1] and return (fb_grid, a0_grid_SI).

    Mirrors Sec. 'Sensitivity scan over the baryon weight' of the paper.
    """
    import numpy as np
    fb = np.linspace(0.0, 1.0, n)
    a0 = np.array([a0_paper_mode(H0_PAPER, f_b=float(x)) for x in fb])
    return fb, a0


def fb_best_fit_to_rar(target: float = A0_RAR_MCGAUGH) -> float:
    """Locate f_b that exactly reproduces the canonical RAR value (paper: 0.354)."""
    import numpy as np
    fb, a0 = fb_sensitivity_scan(n=200001)
    return float(fb[int(np.argmin(np.abs(a0 - target)))])
