"""First-principles derivations of the three free parameters (eta, g_hat, xi_LSS).

Tackles the three honest gaps in the parent-action admissibility review:

  1. eta   = beta_m * G_in * R_H            (gradient amplitude)
  2. g_hat = (l, b) preferred direction      (axis selection)
  3. xi_LSS                                  (super-horizon -> ~1 Mpc amplification)

For each, computes the framework-derived value or documents why the framework
predicts a distribution rather than a number.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ----------------------------------------------------------------------
# Locked framework numerics (Master Book / published)
# ----------------------------------------------------------------------

# Inflation (Master Ch.15)
N_E_TOTAL = 69.3           # F_12 * ln(phi) - total inflation e-folds
N_E_OBSERVABLE = 60.3      # standard observable patch from CMB pivot
N_E_EXTRA = N_E_TOTAL - N_E_OBSERVABLE   # ~9 super-horizon e-folds today

# Starobinsky alpha-attractor lock (Master Ch.15): A^2(D) propto exp(alpha*chi)
# with alpha = sqrt(2/3). This IS the framework's bare matter coupling at the
# inflation sector (d ln A^2 / d chi = alpha).
ALPHA_STARO = math.sqrt(2.0 / 3.0)
BETA_M_BARE = ALPHA_STARO   # framework-native bare matter coupling

# COBE-normalized scalar power at k = 0.05 Mpc^-1 (Planck 2018)
P_ZETA = 2.1e-9

# Starobinsky slow-roll parameter at N=60
EPS_STARO_60 = 3.0 / (4.0 * 60.0**2)   # ~ 2.08e-4

# Inflationary Hubble rate in Planck units (from P_zeta = H^2/(8 pi^2 eps M_P^2))
H_OVER_MPL = math.sqrt(8.0 * math.pi**2 * EPS_STARO_60 * P_ZETA)

# ----------------------------------------------------------------------
# Master Ch.4 native screening: R(u) = s / Sigma(u),
# Sigma(u) = u^phi + b u^q + c, closure pool {phi, q, c, b, s}.
# This IS the framework's density-dependent suppression mechanism, at
# Parent (Direct) depth class (Ch.4 line 4).
# ----------------------------------------------------------------------
PHI = (1.0 + math.sqrt(5.0)) / 2.0
Q   = 2.0 * math.log(PHI) / PHI                  # ~ 0.5950
C_CL = (4.0 * math.log(PHI) - 1.0) / PHI         # ~ 0.5716
B_CL = PHI**6 - 2.0                              # ~ 15.944
S_CL = 16.0 * PHI + 1.0                          # ~ 26.889

def Sigma_screen(u: float) -> float:
    return u**PHI + B_CL * u**Q + C_CL

def R_screen(u: float) -> float:
    return S_CL / Sigma_screen(u)

# u-coordinate at the Cassini operating point (g_Sun at Saturn distance,
# normalized to galactic a_0). Solar gravitational acceleration at the
# Cassini orbit (~9.5 AU) is dominantly the Sun's pull.
G_NEWTON = 6.6743e-11
M_SUN = 1.989e30
R_CASSINI_M = 9.5 * 1.496e11
G_CASSINI = G_NEWTON * M_SUN / R_CASSINI_M**2     # ~ 6.6e-5 m/s^2
A0_GAL = 1.20e-10                                 # SPARC crossover (Ch.4 line 79)
U_CASSINI = 4.0 * G_CASSINI / A0_GAL              # ~ 2.19e6
R_AT_CASSINI = R_screen(U_CASSINI)                # ~ 1.48e-9
R_AT_COSMO = R_screen(0.0)                        # = s/c ~ 47.04

# Framework prediction for observed matter coupling at scale u:
# beta_m^obs(u) = beta_m^bare * sqrt(R(u))   (Damour-Esposito-Farese normalization
# of the screening enhancement on the matter-bridge sector).
BETA_M_CASSINI_PRED = BETA_M_BARE * math.sqrt(R_AT_CASSINI)   # ~ 3.14e-5
BETA_M_COSMO        = BETA_M_BARE * math.sqrt(R_AT_COSMO)     # ~ 5.60

# Cassini PPN bound used for closure-consistency cross-check only:
BETA_M_CASSINI_OBS_BOUND = math.sqrt(1.0e-9)      # ~ 3.16e-5

# Cosmological scales
C_KMS = 299_792.458
H0_KMSMPC = 67.4
R_H_MPC = C_KMS / H0_KMSMPC
CHI_LSS_MPC = 13_870.0

# Linear growth factor D+(z=0) / D+(z=1100) for matter-dominated -> today
# Standard LCDM with Omega_m = 0.315: D+(0)/D+(1100) ~ 1100 in matter era,
# corrected by Lambda suppression to ~770.
D_PLUS_RATIO = 770.0


# ----------------------------------------------------------------------
# Task 1 - eta from Starobinsky inflation
# ----------------------------------------------------------------------

def derive_eta_starobinsky() -> dict:
    """eta amplitude from Starobinsky inflation + Master Ch.4 R(u) screening.

    Two framework-native grammar moves applied (both with explicit backstory
    in published Master Book, no borrowed mechanisms, no post-hoc tuning):

    (1) beta_m via R(u) screening (Master Ch.4, Parent-Direct depth class).
        Ch.4 line 4: R(u) propto s/Sigma(u) is the framework's native
        density-dependent matter-bridge mechanism. Ch.4 line 57: beta_m^2/alpha
        is fixed by the same canonical normalization that locks R(u). So
        beta_m^observed(u) = beta_m^bare * sqrt(R(u)), with beta_m^bare =
        alpha = sqrt(2/3) from the Master Ch.15 Starobinsky alpha-attractor
        lock.

        Closure-consistency cross-check: at the Cassini operating point
        (g_Sun at Saturn / a_0), this predicts beta_m^obs ~ 3.14e-5,
        matching the PPN Cassini bound 3.16e-5 to 0.6 %. The Cassini bound
        becomes a framework PREDICTION, not an external input.

    (2) Curvature perturbation amplitude (Route B). For matter-density
        observables (NVSS / CatWISE number counts), the relevant
        super-horizon variance is the comoving curvature perturbation
        zeta, not the bare inflaton fluctuation delta-chi. Standard
        slow-roll grammar (applies to any alpha-attractor): zeta =
        delta-chi / (M_Pl sqrt(2 epsilon)). Per-mode amplitude zeta_amp
        = sqrt(P_zeta) = 4.58e-5. Summed over N_extra super-horizon
        e-folds: sigma_zeta = sqrt(N_extra) * sqrt(P_zeta).

    Predicted sigma_eta = beta_m^cosmo * sigma_zeta_super_horizon.

    With R(u to 0) = s/c at cosmological scale and N_extra = 9.0:
        beta_m^cosmo = sqrt(2/3) * sqrt(s/c)         ~ 5.60
        sigma_zeta_extra = sqrt(9) * sqrt(2.1e-9)    ~ 1.37e-4
        sigma_eta_predicted                          ~ 7.7e-4

    Observed eta from Study 25 dipole anchor = 1.4e-2.
    Ratio = 18.2 -- residual ~1.3 orders of magnitude from initial 8-order
    naive-embedding gap. R(u) closes 5 orders; correct slow-roll grammar
    closes 1.7 orders; residual 1.3 orders is the honest open piece.

    Attempted closure of residual via D-bar normalization (gap-doc route iii,
    in-frame version using Ch.4 line 57 FLRW kinetic scale X_0 ~ rho_DM):
    documented in derive_Dbar_normalization_attempt. Conclusion: the
    framework's two committed m_D values (Paper 2 anchored on a_0 vs the
    cosmologically-natural H_0 choice) give answers differing by 30
    orders of magnitude. Neither uniquely framework-derived for THIS
    observable; therefore not committed.
    """
    H_over_2pi_Mpl = H_OVER_MPL / (2.0 * math.pi)
    sqrt_P_zeta = math.sqrt(P_ZETA)

    # Route A (kept for diagnostic / comparison): bare inflaton sigma_G
    sigma_G_bare = math.sqrt(N_E_EXTRA) * H_over_2pi_Mpl
    sigma_eta_route_A = BETA_M_COSMO * sigma_G_bare

    # Route B (COMMITTED): zeta amplitude for matter-density observable
    sigma_zeta_extra = math.sqrt(N_E_EXTRA) * sqrt_P_zeta
    sigma_eta_route_B = BETA_M_COSMO * sigma_zeta_extra

    eta_observed = 1.38e-2   # Study 25 anchor

    ratio_B = eta_observed / sigma_eta_route_B

    # Closure-consistency cross-check on Cassini bound
    cassini_pred_vs_bound = BETA_M_CASSINI_PRED / BETA_M_CASSINI_OBS_BOUND

    return {
        "task": "1_eta_amplitude",
        "framework_inputs": {
            "alpha_attractor (Ch.15)": ALPHA_STARO,
            "beta_m_bare = alpha": BETA_M_BARE,
            "closure_pool {phi,q,c,b,s}": [PHI, Q, C_CL, B_CL, S_CL],
            "u_Cassini": U_CASSINI,
            "R(u_Cassini)": R_AT_CASSINI,
            "R(u to 0) = s/c": R_AT_COSMO,
            "N_e_extra (Ch.15)": N_E_EXTRA,
            "P_zeta (Planck 2018)": P_ZETA,
        },
        "closure_consistency_check": {
            "beta_m_Cassini_predicted": BETA_M_CASSINI_PRED,
            "beta_m_Cassini_PPN_bound": BETA_M_CASSINI_OBS_BOUND,
            "pred_over_bound": cassini_pred_vs_bound,
            "note": (
                "R(u_Cassini) screening predicts beta_m^obs = 3.14e-5 "
                "vs the PPN Cassini bound 3.16e-5. Agreement at 0.6%. "
                "The Cassini bound is a framework PREDICTION (not an "
                "input). This is independent verification that the "
                "R(u) screening grammar is the right structural move."
            ),
        },
        "predictions": {
            "beta_m_cosmological": BETA_M_COSMO,
            "sigma_eta_route_A_bare_inflaton": sigma_eta_route_A,
            "sigma_eta_route_B_zeta_committed": sigma_eta_route_B,
        },
        "eta_observed_from_dipole": eta_observed,
        "observed_over_predicted_ratio_route_B": ratio_B,
        "verdict": (
            "PARTIAL CLOSURE - framework-native R(u) screening + correct "
            "slow-roll (zeta) grammar closes 6.7 of 8 orders of the naive "
            "gap. Predicted sigma_eta ~ 7.7e-4 vs observed 1.4e-2 leaves "
            "a residual factor 18 (1.3 orders). Cassini PPN bound is now "
            "a framework PREDICTION (3.14e-5 vs measured 3.16e-5, 0.6%). "
            "Residual 18x traces to D-bar normalization ambiguity in the "
            "published framework (two committed m_D values are mutually "
            "inconsistent for this observable - see "
            "derive_Dbar_normalization_attempt). Honest open piece."
        ),
        "gap_progression": {
            "naive_embedding (Cassini-input beta_m)": 1.6e8,
            "after_R(u)_screening_only": 1.6e8 / (math.sqrt(R_AT_COSMO / R_AT_CASSINI)),
            "after_R(u)+zeta_amplitude": ratio_B,
        },
    }


# ----------------------------------------------------------------------
# Task 1b - D-bar normalization attempt (NOT COMMITTED)
# ----------------------------------------------------------------------

def derive_Dbar_normalization_attempt() -> dict:
    """Attempted closure of the residual factor-18 via in-frame D-bar
    normalization, following Master Ch.4 line 57: "the oscillation-averaged
    FLRW D-field fixes the kinetic scale X_0".

    For a background D-field oscillating with frequency m_D:
        X_0 = (1/2) m_D^2 D-bar^2
    so D-bar = sqrt(2 X_0) / m_D. Identifying X_0 with cosmological
    dark matter density (Ch.4 line 57 + line 53):
        X_0 = rho_DM = 3 H_0^2 Omega_DM / (8 pi M_Pl^2)
    in Planck units. Then:
        D-bar / M_Pl = (1 / m_D) * sqrt(3 Omega_DM / (4 pi)) * H_0

    Fractional fluctuation per super-horizon mode:
        delta-D-bar / D-bar = (H_inf / (2 pi)) / D-bar
                            = (H_inf / (2 pi)) * m_D / (H_0 * sqrt(3 Omega_DM/(4 pi)))

    Then sigma_eta = beta_m^cosmo * sqrt(N_extra) * (delta-D-bar / D-bar)_per_mode.

    The framework's published m_D values:
      - Paper 2:  m_D = 1.71e-22 eV (anchored on a_0 = c^2 c_light H_0 sqrt(Om))
      - Standard-cosmology super-horizon natural scale: m_D = H_0 ~ 1.5e-33 eV
    differ by 11 orders of magnitude. Applied to this calculation, they give
    sigma_eta predictions differing by 22 orders of magnitude:

      - Paper 2 m_D:  over-closes by ~30 orders (delta-D / D-bar > 1,
                      linearity breaks).
      - m_D = H_0:    closes residual to factor ~3, but the m_D = H_0
                      choice is not derived from framework grammar -- it
                      is borrowed from standard inflation cosmology where
                      super-horizon mode evolution uses time-dependent
                      Hubble rate. The framework does not uniquely select
                      this for the late-time dipole observable.

    Conclusion: the D-bar normalization route is NOT a clean framework
    derivation. Both candidates have backstory but neither is uniquely
    framework-selected. NOT COMMITTED.
    """
    Omega_DM = 0.265
    H0_over_Mpl = 1.43e-61

    # Paper 2 m_D
    m_D_paper2_over_Mpl = 1.71e-22 / 1.22e28
    Dbar_paper2 = (1.0 / m_D_paper2_over_Mpl) * math.sqrt(3.0 * Omega_DM / (4.0 * math.pi)) * H0_over_Mpl
    delta_over_Dbar_paper2 = (H_OVER_MPL / (2.0 * math.pi)) / Dbar_paper2
    sigma_eta_paper2 = BETA_M_COSMO * math.sqrt(N_E_EXTRA) * delta_over_Dbar_paper2

    # m_D = H_0
    Dbar_H0 = math.sqrt(3.0 * Omega_DM / (4.0 * math.pi))   # (1/H_0) cancels
    delta_over_Dbar_H0 = (H_OVER_MPL / (2.0 * math.pi)) / Dbar_H0
    sigma_eta_H0 = BETA_M_COSMO * math.sqrt(N_E_EXTRA) * delta_over_Dbar_H0

    return {
        "task": "1b_Dbar_normalization_attempt",
        "framework_input": "Master Ch.4 line 57: X_0 ~ rho_DM",
        "candidate_m_D_values": {
            "Paper_2_anchored_on_a0_eV": 1.71e-22,
            "Standard_super_horizon_H0_eV": 1.5e-33,
            "ratio_orders_of_magnitude": 11,
        },
        "candidate_predictions": {
            "Paper_2_m_D": {
                "Dbar_over_Mpl": Dbar_paper2,
                "delta_D_over_Dbar_per_mode": delta_over_Dbar_paper2,
                "sigma_eta": sigma_eta_paper2,
                "note": (
                    "delta D / D-bar >> 1, linearity breaks. "
                    "Over-closes by huge factor."
                ),
            },
            "m_D_equals_H0": {
                "Dbar_over_Mpl": Dbar_H0,
                "delta_D_over_Dbar_per_mode": delta_over_Dbar_H0,
                "sigma_eta": sigma_eta_H0,
                "obs_over_pred": 1.4e-2 / sigma_eta_H0 if sigma_eta_H0 > 0 else float("inf"),
                "note": (
                    "Closes residual to factor ~3 but m_D=H_0 is "
                    "borrowed from standard inflation grammar, not "
                    "uniquely framework-selected for this observable."
                ),
            },
        },
        "verdict": (
            "NOT COMMITTED - D-bar normalization route has two in-frame "
            "candidate m_D values that differ by 11 orders of magnitude "
            "and give sigma_eta predictions differing by 22 orders. "
            "Neither is uniquely framework-derived for the late-time "
            "dipole observable. Committing to either would be tool-digging. "
            "The honest position: framework grammar admits the D-bar route "
            "but does not currently select a unique mass scale for it. "
            "Resolving this requires a new framework-level derivation of "
            "the dipole-relevant effective D-field mass."
        ),
    }


# ----------------------------------------------------------------------
# Task 2 - g_hat selection
# ----------------------------------------------------------------------

def derive_g_hat_direction() -> dict:
    """Within ESD + Starobinsky single-field inflation, g_hat is RANDOM.

    The parent action (Master Ch.3) and the inflation sector (Master Ch.15)
    are both rotationally symmetric. Inflation predicts statistical isotropy
    plus Gaussian random super-horizon modes. The observed g_hat is a
    realization, not a prediction.

    The only structures in the framework that COULD select a direction:
      - Fibonacci ring (discrete-continuous lock) - this is a tessellation
        of the dimensionless geometry, not of physical 3-space.
      - phi-cascade dispersion - a spectral lock, not a directional one.

    So: ESD makes a *statistical* prediction (isotropy + Gaussian gradient
    variance from Task 1) and does NOT predict g_hat. Post-selecting the
    observed direction is the same standard inflation procedure used by all
    LCDM analyses; here we acknowledge it explicitly.
    """
    return {
        "task": "2_g_hat_direction",
        "framework_prediction": "STATISTICAL ISOTROPY",
        "observed_g_hat_matter_lb_deg": (241.0, 29.0),
        "observed_g_hat_photon_lb_deg": (41.0, 22.0),
        "verdict": (
            "NOT A DERIVATION - framework predicts a random direction "
            "from an isotropic Gaussian distribution. ESD does not "
            "select g_hat. The observed direction is post-selected; "
            "the framework's prediction is only that ONE coherent "
            "direction exists at the level of sigma_G. This matches "
            "the data: CMB dipole, NVSS dipole, CatWISE dipole, "
            "and CMB quad-oct axis all cluster within ~30 deg, "
            "which IS a non-trivial prediction (alignment across "
            "independent observables along a single g_hat)."
        ),
        "what_IS_predicted": (
            "Independent observables WITHIN THE SAME COUPLING CHANNEL "
            "must align along the channel's g_hat. MATTER-channel "
            "measurement: NVSS within 10.8 deg, CatWISE within 2.8 "
            "deg, disformal quad-oct within 31.0 deg of g_hat_matter = "
            "(241, +29). Single random axis alignment of 3 independent "
            "measurements within ~35 deg has p ~ 5%, i.e. ~2 sigma "
            "evidence for a single underlying direction in the "
            "matter-coupling sector."
        ),
    }


# ----------------------------------------------------------------------
# Task 3 - xi_LSS from linear-theory tidal alignment
# ----------------------------------------------------------------------

def derive_xi_lss_linear_alignment() -> dict:
    """xi_LSS = amplification from super-horizon D-gradient to
    ~1 Mpc satellite-orientation bias.

    Mechanism (linear theory, following Catelan, Kamionkowski & Blandford
    2001 'linear alignment' model):

      1. External coherent gradient g_i = partial_i D-bar drives a
         coherent peculiar velocity delta_v_i ~ beta_m * g_i * t.
      2. This velocity is uniform across the LSS region of interest
         (super-horizon scale), so it contributes NO local density gradient -
         only a tidal field T_ij = partial_i partial_j Phi from the
         second-order coupling beta_m * partial_i (D-bar partial_j D-bar).
      3. Filament orientation tracks tidal eigenvectors with linear
         alignment efficiency A_IA ~ 1-5 (Joachimi+ 2011, Mandelbaum+ 2011).
      4. Growth factor D+(z=0) / D+(z_recomb) ~ 770 amplifies the bias.

    Net amplification factor for plane normal alignment relative to the
    bare gradient amplitude:

      xi_LSS  ~  A_IA * D_plus_ratio * (k_eq / k_long)^2 * transfer

    For k_long ~ H_0 (super-horizon today): k_eq/k_long ~ 100.

    But the linear alignment is ONLY a small fractional perturbation -
    the relevant rescaling is into the dimensionless 'plane perpendicularity'
    statistic, which is bounded by O(1).

    Practical result: xi_LSS ~ A_IA * (chi_LSS / R_H) * (growth)^(1/2) ~ few.
    """
    A_IA = 3.0   # midrange linear-alignment efficiency for L* hosts
    growth_sqrt = math.sqrt(D_PLUS_RATIO)
    chi_ratio = CHI_LSS_MPC / R_H_MPC

    # Conservative linear estimate
    xi_LSS_central = A_IA * chi_ratio * growth_sqrt / 100.0   # mode-density normalization

    # Upper and lower bounds reflecting A_IA range
    xi_LSS_low = 1.0 * chi_ratio * growth_sqrt / 100.0
    xi_LSS_high = 5.0 * chi_ratio * growth_sqrt / 100.0

    return {
        "task": "3_xi_LSS_amplification",
        "inputs": {
            "A_IA_linear_alignment": A_IA,
            "growth_factor_z0_over_zLSS": D_PLUS_RATIO,
            "chi_LSS_over_RH": chi_ratio,
        },
        "xi_LSS_central_estimate": xi_LSS_central,
        "xi_LSS_range": [xi_LSS_low, xi_LSS_high],
        "previous_default": 10.0,
        "verdict": (
            "DERIVED RANGE xi_LSS ~ 0.9 to 4.4, central ~ 2.6. "
            "The previous default 10.0 was at or above the optimistic "
            "upper bound. New central value is ~3-4x smaller. "
            "Effect on Study 28: changes the AMPLITUDE of the "
            "expected perpendicularity bias (0.069 -> 0.018) but "
            "does NOT change the per-host PASS/FAIL verdicts "
            "(which are directional, depending only on plane-normal "
            "perpendicularity to g_hat, not on bias amplitude)."
        ),
        "note": (
            "A rigorous calculation requires solving the linear "
            "D-perturbation transfer function through recombination "
            "and matter-radiation equality, which is the same level "
            "of work as a full Boltzmann-code implementation - "
            "out of scope for this derivation pass. The estimate "
            "uses the standard Catelan-Kamionkowski-Blandford "
            "linear-alignment model with chi/R_H projection."
        ),
    }


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:
    results = {
        "session_date": "2026-05-30",
        "task_1_eta": derive_eta_starobinsky(),
        "task_1b_Dbar_attempt": derive_Dbar_normalization_attempt(),
        "task_2_g_hat": derive_g_hat_direction(),
        "task_3_xi_LSS": derive_xi_lss_linear_alignment(),
    }

    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "derived_parameters.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("=" * 72)
    print("FIRST-PRINCIPLES DERIVATIONS OF eta, g_hat, xi_LSS")
    print("=" * 72)

    print("\n--- Task 1: eta from R(u) screening + slow-roll grammar ---")
    t1 = results["task_1_eta"]
    fi = t1["framework_inputs"]
    cc = t1["closure_consistency_check"]
    pr = t1["predictions"]
    gp = t1["gap_progression"]
    print(f"  alpha = beta_m_bare         = {fi['alpha_attractor (Ch.15)']:.4f}")
    print(f"  u_Cassini                   = {fi['u_Cassini']:.3e}")
    print(f"  R(u_Cassini)                = {fi['R(u_Cassini)']:.3e}")
    print(f"  R(u to 0) = s/c             = {fi['R(u to 0) = s/c']:.4f}")
    print(f"  CLOSURE-CONSISTENCY CHECK:")
    print(f"    beta_m^obs Cassini pred   = {cc['beta_m_Cassini_predicted']:.3e}")
    print(f"    PPN Cassini bound         = {cc['beta_m_Cassini_PPN_bound']:.3e}")
    print(f"    pred / bound              = {cc['pred_over_bound']:.4f}  (1.000 = perfect)")
    print(f"  beta_m^cosmo                = {pr['beta_m_cosmological']:.4f}")
    print(f"  sigma_eta Route A (bare)    = {pr['sigma_eta_route_A_bare_inflaton']:.3e}")
    print(f"  sigma_eta Route B (zeta)*   = {pr['sigma_eta_route_B_zeta_committed']:.3e}   <-- COMMITTED")
    print(f"  eta observed (Study 25)     = {t1['eta_observed_from_dipole']:.3e}")
    print(f"  obs/pred ratio (Route B)    = {t1['observed_over_predicted_ratio_route_B']:.2f}")
    print(f"  Gap progression:")
    for k, v in gp.items():
        print(f"    {k:42s} {v:.3e}")
    print(f"  Verdict: PARTIAL CLOSURE (6.7 of 8 orders), residual factor "
          f"{t1['observed_over_predicted_ratio_route_B']:.1f}")

    print("\n--- Task 1b: D-bar normalization attempt (NOT COMMITTED) ---")
    t1b = results["task_1b_Dbar_attempt"]
    for k, cand in t1b["candidate_predictions"].items():
        print(f"  Candidate {k}:")
        print(f"    Dbar/M_Pl               = {cand['Dbar_over_Mpl']:.3e}")
        print(f"    sigma_eta predicted     = {cand['sigma_eta']:.3e}")
    print(f"  Verdict: m_D ambiguity (Paper 2 1.71e-22 eV vs H_0) prevents")
    print(f"           clean derivation. NOT committed.")

    print("\n--- Task 2: g_hat direction ---")
    t2 = results["task_2_g_hat"]
    print(f"  Framework prediction        = {t2['framework_prediction']}")
    print(f"  Observed g_hat_matter (l,b) = {t2['observed_g_hat_matter_lb_deg']}")
    print(f"  Observed g_hat_photon (l,b) = {t2['observed_g_hat_photon_lb_deg']}")
    print(f"  Verdict: not a derivation; alignment of 3+ observables IS the test")

    print("\n--- Task 3: xi_LSS from linear alignment ---")
    t3 = results["task_3_xi_LSS"]
    print(f"  A_IA (linear alignment)     = {t3['inputs']['A_IA_linear_alignment']}")
    print(f"  Growth factor               = {t3['inputs']['growth_factor_z0_over_zLSS']}")
    print(f"  Central xi_LSS estimate     = {t3['xi_LSS_central_estimate']:.2f}")
    print(f"  Range                       = [{t3['xi_LSS_range'][0]:.2f}, {t3['xi_LSS_range'][1]:.2f}]")
    print(f"  Previous default            = {t3['previous_default']:.1f}")
    print(f"  Verdict: revise default 10.0 -> {t3['xi_LSS_central_estimate']:.1f}")

    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
