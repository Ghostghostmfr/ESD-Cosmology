"""Derived cosmological quantities from the locked identities.

Every quantity here depends only on the combination 3 Omega_DM + Omega_b
(which is locked by Identity B), so it is identical under both the
primary and closure-pool readings.

See [HigginsonESDFramework2026] Ch. 4 for the derivation.
"""

import math

from .constants import PHI
from .identities import identity_B_rhs

# Physical constants in SI
C_LIGHT_M_S: float = 2.998e8           # speed of light [m / s]
MPC_M: float = 3.0857e22               # 1 Mpc in metres


def hubble_inverse_seconds(H0_kms_per_mpc: float) -> float:
    """Convert H0 from km/s/Mpc to 1/s."""
    return H0_kms_per_mpc * 1000.0 / MPC_M


def a_zero(H0_kms_per_mpc: float = 67.36) -> float:
    """MOND-scale acceleration a_0 [m / s^2].

        a_0 = c_light * H_0 * sqrt((3 Omega_DM + Omega_b) / (8 pi))

    Reading-independent (depends only on the Identity-B combination).
    """
    H0 = hubble_inverse_seconds(H0_kms_per_mpc)
    return C_LIGHT_M_S * H0 * math.sqrt(identity_B_rhs() / (8.0 * math.pi))


def m_D(H0_kms_per_mpc: float = 67.36) -> float:
    """Disformal screening mass m_D [1 / m].

        m_D = a_0 * phi / (c_light^2 * sqrt(8 pi))
    """
    return a_zero(H0_kms_per_mpc) * PHI / (C_LIGHT_M_S**2 * math.sqrt(8.0 * math.pi))


def lambda_D_over_RH(H0_kms_per_mpc: float = 67.36) -> float:
    """Disformal screening length lambda_D in units of the Hubble radius R_H."""
    R_H = C_LIGHT_M_S / hubble_inverse_seconds(H0_kms_per_mpc)
    return 1.0 / m_D(H0_kms_per_mpc) / R_H
