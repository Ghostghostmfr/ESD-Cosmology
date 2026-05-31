"""
ACT DR6 CMB-lensing published results used by the Study 24 audit.

Only values explicitly quoted in the peer-reviewed paper are used.
No bandpower digitization or re-fitting is performed.

Primary reference:
  Madhavacheril et al. 2024, ApJ 962, 113 (arXiv:2304.05203),
  "The Atacama Cosmology Telescope: DR6 Gravitational Lensing Map and
   Cosmological Parameters", abstract and Section 7 (headline parameter
   constraints).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class S8CMBLPosterior:
    """
    Published 1-D marginal on  S_8^{CMBL} = sigma_8 * (Omega_m / 0.3)^0.25
    from the ACT DR6 lensing analysis.
    """
    label: str
    median: float
    sigma: float
    source: str


# ---------------------------------------------------------------------------
# Headline ACT-only value (Madhavacheril et al. 2024, abstract):
#   sigma_8 (Omega_m / 0.3)^0.25 = 0.818 +/- 0.022
# ---------------------------------------------------------------------------
ACT_DR6_ONLY = S8CMBLPosterior(
    label="ACT DR6 only",
    median=0.818,
    sigma=0.022,
    source="Madhavacheril et al. 2024, ApJ 962 113 (arXiv:2304.05203), abstract",
)

# ---------------------------------------------------------------------------
# Combined with Planck NPIPE lensing (Madhavacheril et al. 2024, abstract):
#   sigma_8 (Omega_m / 0.3)^0.25 = 0.840 +/- 0.018
# ---------------------------------------------------------------------------
ACT_DR6_PLUS_NPIPE = S8CMBLPosterior(
    label="ACT DR6 + Planck NPIPE",
    median=0.840,
    sigma=0.018,
    source="Madhavacheril et al. 2024, ApJ 962 113 (arXiv:2304.05203), abstract",
)
