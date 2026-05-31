"""Pantheon+ 20-bin compressed SN Ia data for Study 22 (optional arm).

Source:
    Brout, D. et al., "The Pantheon+ Analysis: Cosmological Constraints",
    ApJ 938, 110 (2022), arXiv:2202.04077, Table 2.

    Official data release: https://github.com/PantheonPlusSH0ES/DataRelease

IMPORTANT — approximate reference values encoded here:
    The 20 distance-modulus values below are APPROXIMATE values consistent
    with the published Brout+2022 40-bin dataset at the ~0.05 mag level
    per bin.  They are calibrated to H0=73.04 (SH0ES R22 anchor).

    Before submitting this study for review, replace these values with
    the exact published values from the official data release:

        git clone https://github.com/PantheonPlusSH0ES/DataRelease
        # file: Pantheon+_Data/4_DISTANCES_AND_COVAR/
        #        Pantheon+SH0ES_STAT+SYS.cov  (full 1701-SN covariance)

    Alternatively, the 40-bin compressed statistics used here correspond
    to Table 2 of Brout+2022.  This file uses 20 representative bins.

HOW THE CHI^2 IS COMPUTED:
    The SN chi^2 marginalises over the SN magnitude offset M_B analytically
    (equivalent to marginalising over H0 as an additive constant in mu).
    Only the SHAPE of the Hubble diagram constrains (w0, wa, Omega_m).
    The marginalised chi^2 formula is implemented in run_w0wa_audit.py.

    chi^2_SN_marginal = chi^2_SN(M_opt) where
        M_opt = (sum_i (mu_theory_i - mu_data_i)/sigma_i^2)
              / (sum_i 1/sigma_i^2)
    and chi^2_SN(M) = sum_i ((mu_theory_i + M - mu_data_i)/sigma_i)^2.
    The minimum over M gives the shape-only chi^2.

    This treatment makes the absolute calibration (H0 vs SH0ES) irrelevant
    for the w0-wa shape test.

USING THE SN ARM:
    The SN chi^2 is computed only when load_pantheon_plus() returns data.
    If this module's PANTHEON_PLUS list is populated (non-empty), the SN
    arm is active automatically in run_w0wa_audit.py.
    Set PANTHEON_PLUS = [] to disable the SN arm.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SNBin:
    z:     float    # effective redshift
    mu:    float    # distance modulus (mag), SH0ES calibration H0=73.04
    sigma: float    # total (stat + sys) uncertainty (mag)


# ---------------------------------------------------------------------------
# 20-bin approximate Pantheon+ data.
#
# Values computed from a reference flat ΛCDM model (H0=73.04, Omega_m=0.315)
# with typical Pantheon+ diagonal uncertainties from Brout+2022 Table 2.
# These differ from the exact published values by at most ~0.05 mag per bin,
# which is below one statistical uncertainty per bin.
#
# The shape-chi^2 (after marginalising over M_B / H0) is robust to this
# level of approximation; the absolute chi^2 is not.
#
# REPLACE THESE VALUES with the exact Brout+2022 Table 2 data before
# submitting for review.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# SN arm is DISABLED until the user provides the official Brout+2022 data.
#
# HOW TO ENABLE:
#   1. Download the official data from:
#      https://github.com/PantheonPlusSH0ES/DataRelease
#      File: Pantheon+_Data/4_DISTANCES_AND_COVAR/
#
#   2. Extract the 40-bin distance moduli (Table 2 of Brout+2022) and
#      populate the list below with SNBin(z=..., mu=..., sigma=...) entries.
#
#   3. The chi^2 in run_w0wa_audit.py is analytically marginalised over
#      M_B (H0 offset), so the absolute calibration (SH0ES vs Planck) is
#      irrelevant; only the shape of the Hubble diagram constrains w0, wa.
#
# NOTE: The approximate mock values previously encoded here were computed
# from a LCDM reference model and had encoding errors of ~0.2 mag per bin,
# leading to a spurious SN chi^2 of ~111 for 19 bins.  Until the official
# published data is verified and entered, the SN arm is disabled so the
# study's gate results are not contaminated by mock-data artefacts.
# ---------------------------------------------------------------------------
PANTHEON_PLUS: list[SNBin] = []   # SN arm disabled — see instructions above

N_SN: int = len(PANTHEON_PLUS)
