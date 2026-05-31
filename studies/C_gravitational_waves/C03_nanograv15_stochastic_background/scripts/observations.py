"""
NANOGrav 15-year published results used by the Study 23 audit.

This module deliberately uses ONLY values that are explicitly quoted in the
peer-reviewed NANOGrav 15-year papers. We do NOT digitize plot points or
re-fit anything; doing so would introduce extraction errors that are far
larger than the published uncertainties.

Primary references:
  - Agazie et al. 2023, ApJL 951 L8 (arXiv:2306.16213):
    "The NANOGrav 15-year Data Set: Evidence for a Gravitational-Wave Background"
  - Agazie et al. 2023, ApJL 951 L9 (arXiv:2306.16220):
    "The NANOGrav 15-year Data Set: Constraints on Supermassive Black Hole
     Binaries from the Gravitational-Wave Background"

The full binned ORF and posterior samples are released by NANOGrav at:
  https://github.com/nanograv/15yr_stochastic_analysis
with the raw data files hosted on Google Drive (linked from that repo).
Reproducing those binned values requires downloading the pickle archive;
the audit below uses only the headline published numbers, which is the
correct level of granularity for a falsification test of GR-like tensor
gravitational waves.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpectralPosterior:
    """
    Published posterior summary for the spectral index of the
    HD-correlated common-red process.

    h_c(f)^2 is proportional to f^(-gamma); equivalently
    Omega_GW(f) is proportional to f^(5-gamma).
    """
    gamma_median: float
    gamma_sigma: float  # symmetric 68% credible half-width (approx)
    log10_A_median: float
    log10_A_sigma: float
    source: str


@dataclass(frozen=True)
class HDDetection:
    """
    Published evidence that the inter-pulsar correlations follow the
    Hellings-Downs (tensor) pattern, as opposed to alternative ORFs
    (monopole, dipole, uncorrelated).
    """
    sigma_significance: float  # detection significance in equivalent sigma
    bayes_factor_hd_vs_curn: float  # HD-correlated vs common-uncorrelated
    source: str


# ---------------------------------------------------------------------------
# Spectral index of the HD-correlated power-law model.
#
# Source: Agazie et al. 2023, ApJL 951 L8, Section 4 / Figure 1 (HD model row)
# Headline quoted value: gamma = 3.2 +/- 0.6 (68% CI, approximately symmetric);
# log10(A_yr) = -14.19 +/- 0.36 (68% CI).
# These are the marginalized 1-D posterior summaries the collaboration
# quotes in the abstract and Section 4.
# ---------------------------------------------------------------------------
NANOGRAV_15YR_SPECTRAL = SpectralPosterior(
    gamma_median=3.2,
    gamma_sigma=0.6,
    log10_A_median=-14.19,
    log10_A_sigma=0.36,
    source="Agazie et al. 2023, ApJL 951 L8 (arXiv:2306.16213), Section 4 / Fig. 1",
)

# ---------------------------------------------------------------------------
# Hellings-Downs detection significance.
#
# Source: Agazie et al. 2023, ApJL 951 L8, abstract / Section 5:
# "We report evidence for HD-correlated signals at the 3-4 sigma level".
# The Bayes factor of the HD-correlated model versus the common-uncorrelated
# red-noise (CURN) model is ~200 in the headline analysis.
# We adopt the conservative end of the quoted range (3 sigma) for the audit
# threshold.
# ---------------------------------------------------------------------------
NANOGRAV_15YR_HD_DETECTION = HDDetection(
    sigma_significance=3.0,
    bayes_factor_hd_vs_curn=200.0,
    source="Agazie et al. 2023, ApJL 951 L8 (arXiv:2306.16213), abstract & Section 5",
)
