"""ESD prediction for the isotropic CMB-birefringence angle beta.

Structural derivation
---------------------
1. The ESD parent action (Paper 1, eq. for L_EM) couples the photon
   field only through the parity-EVEN term

       L_EM = -1/4 Z(D) F_{munu} F^{munu}.

   No g(D) F F~ Chern-Simons term is present.

2. The strong-CP-no-axion paper (Higginson 2026, App. D Q9 & Q10)
   structurally excludes any ultralight pseudo-Goldstone coupled to a
   topological gauge density:
     - Q9 (closure-pool capacity): Sigma(u) is fully consumed by the
       D-field's own geometry; no slack for a secondary scalar.
     - Q10 (constant-ownership): the gauge-sector identities
       (sin^2 theta_W = ln phi - 1/4, alpha_s = phi - 3/2, theta_QCD=0)
       are already saturated; introducing g(D) F F~ would overconstrain.
   The exclusion is explicit for the string-theory axion descending
   from d_mu D, which is precisely the candidate that could otherwise
   source CMB birefringence in this framework.

3. Therefore the prediction is parameter-free:

       beta_ESD = 0  exactly.

Any observed beta != 0 at >= 5 sigma after systematic miscalibration
control would falsify either (a) the parent action's parity-even
restriction or (b) the strong-CP-no-axion exclusion mechanism.
"""
from __future__ import annotations


BETA_ESD_DEG = 0.0
ESD_BETA_FREE_PARAMETERS = 0


def esd_beta() -> float:
    """ESD-predicted isotropic birefringence angle in degrees."""
    return BETA_ESD_DEG


def tension_sigma(beta_obs_deg: float, sigma_obs_deg: float) -> float:
    """Tension in sigma between an observed beta and the ESD prediction."""
    return (beta_obs_deg - BETA_ESD_DEG) / sigma_obs_deg


def action_audit() -> dict:
    """Structural audit of the parent action photon sector."""
    return {
        "parity_even_term_present":   "-1/4 Z(D) F_{munu} F^{munu}",
        "parity_odd_term_present":    None,
        "post_hoc_g(D)F_Ftilde":      "excluded by Q9, Q10 (Higginson 2026)",
        "axion_from_d_mu_D":          "explicitly excluded",
        "free_parameters":            ESD_BETA_FREE_PARAMETERS,
    }
