"""Locked cosmological identities of the ESD framework.

Identity A - dark-energy closure
    Omega_Lambda = 2 pi c^2 / 3
    Omega_m      = 1 - Omega_Lambda

Identity B - matter partition closure
    3 Omega_DM + Omega_b = 8 pi c^4 Omega_m

The framework admits two operational readings of Identity B:

    (1) PRIMARY (boundary-input): Omega_b is taken from observation
        (Planck 2018: 0.0493), and Omega_DM is solved from Identity B.
        This is the headline reading used by every CMB-anchored
        prediction.

    (2) CLOSURE-POOL (zero-parameter): Omega_b is derived from c
        alone using Identity B closed against matter closure
        (Omega_m = Omega_b + Omega_DM). This is the secondary
        falsifiable reading that emits Omega_b = 0.050094.

Every quantity that depends only on the combination 3 Omega_DM + Omega_b
(notably a_0, m_D, lambda_D, n_s, S_8) is identical under both readings.
The readings only differ on Omega_b itself, omega_b h^2, and the BAO
chi^2/dof against DESI Y1.

See [HigginsonESDFramework2026] Ch. 4 for the derivation.
"""

from __future__ import annotations

import math
from enum import Enum

from .constants import c2, c4


# ----------------------------- reading selector ---------------------------
class Reading(str, Enum):
    """Which operational reading of Identity B to use."""

    PRIMARY = "primary"             # Omega_b matched to Planck 2018
    CLOSURE_POOL = "closure-pool"   # Omega_b derived from c alone

    @classmethod
    def parse(cls, value: str | "Reading") -> "Reading":
        """Accept enum, canonical string, or common aliases."""
        if isinstance(value, cls):
            return value
        v = str(value).strip().lower().replace("_", "-")
        if v in ("primary", "boundary-input", "input", "planck"):
            return cls.PRIMARY
        if v in ("closure-pool", "cp", "derived", "zero-parameter"):
            return cls.CLOSURE_POOL
        raise ValueError(
            f"Unknown reading {value!r}. "
            f"Use one of: 'primary', 'closure-pool'."
        )


# Boundary-input baryon density (Planck 2018 anchor).
OMEGA_B_PRIMARY: float = 0.0493


# ----------------------------- Identity A ---------------------------------
def omega_lambda() -> float:
    """Identity A: Omega_Lambda = 2 pi c^2 / 3."""
    return 2.0 * math.pi * c2 / 3.0


def omega_matter() -> float:
    """Identity A complement: Omega_m = 1 - Omega_Lambda."""
    return 1.0 - omega_lambda()


# ----------------------------- Identity B ---------------------------------
def identity_B_rhs() -> float:
    """Right-hand side of Identity B: 8 pi c^4 Omega_m."""
    return 8.0 * math.pi * c4 * omega_matter()


def omega_b_closure_pool() -> float:
    """Closure-pool (zero-parameter) prediction for Omega_b.

    Derived by closing Identity B against matter closure
    (Omega_m = Omega_b + Omega_DM, i.e. Omega_DM = Omega_m - Omega_b):

        Omega_b = Omega_m / (1 + (8 pi c^4 - 1) / (3 - 8 pi c^4))

    Numerical value at the locked c: 0.050094.
    """
    rhs_ratio = (8.0 * math.pi * c4 - 1.0) / (3.0 - 8.0 * math.pi * c4)
    return omega_matter() / (1.0 + rhs_ratio)


def omega_dm_from_identity_B(omega_b: float) -> float:
    """Solve Identity B for Omega_DM given Omega_b (either reading).

        Omega_DM = (8 pi c^4 Omega_m - Omega_b) / 3
    """
    return (identity_B_rhs() - omega_b) / 3.0


# ----------------------------- reading dispatchers ------------------------
def omega_b(reading: Reading | str = Reading.PRIMARY) -> float:
    """Return Omega_b under the requested reading."""
    r = Reading.parse(reading)
    if r is Reading.PRIMARY:
        return OMEGA_B_PRIMARY
    return omega_b_closure_pool()


def omega_dm(reading: Reading | str = Reading.PRIMARY) -> float:
    """Return Omega_DM under the requested reading.

    Both readings satisfy Identity B exactly; only the Omega_b input
    differs. Omega_DM is then fixed.
    """
    return omega_dm_from_identity_B(omega_b(reading))


# ----------------------------- materialised LOCK constants ----------------
# Numeric snapshots of the identities, exposed as module-level constants for
# scripts that prefer attribute access (`ESD.OMEGA_M_LOCK`) over a function
# call. These are reading-INDEPENDENT closure values; the per-reading
# baryon/dark-matter numbers live on the dispatchers above.
OMEGA_LAMBDA_LOCK: float = omega_lambda()                  # ~0.684264
OMEGA_M_LOCK: float = omega_matter()                       # ~0.315736

# Closure-pool ("derived") snapshot.
_8PI_C4: float = 8.0 * math.pi * c4
OMEGA_DM_OVER_B_LOCK: float = (_8PI_C4 - 1.0) / (3.0 - _8PI_C4)
OMEGA_B_LOCK: float = omega_b_closure_pool()               # closure-pool
OMEGA_DM_LOCK: float = OMEGA_M_LOCK - OMEGA_B_LOCK         # closure-pool

# Primary (boundary-input) snapshot.
OMEGA_B_INPUT: float = OMEGA_B_PRIMARY                     # 0.0493 (Planck)
OMEGA_DM_FROM_IDB: float = omega_dm_from_identity_B(OMEGA_B_INPUT)  # ~0.265907

