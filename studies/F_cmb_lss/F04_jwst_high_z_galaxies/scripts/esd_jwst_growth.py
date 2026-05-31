"""Study 13 extension - applicability of R(u) to the JWST baryon-budget
tension, against Study 19's linear-growth applicability theorem.

The Study 13 README floated a "deferred resolution" path:

    "A full ESD resolution would require enhanced linear growth at
     z=7-10 from the closure-pool D-field's screening kernel R(u),
     which is deferred to a future study"

This module checks that path against Study 19's published theorem.

Study 19 (`esd_growth.applicability_test_linear_perturbation`) proves
that axiom (A1) of the relational-spectator construction FAILS for
linear cosmological perturbations: delta(x,t) is a fluctuation of the
same matter field that constitutes the background, so there is no
system/spectator split.  R(u) therefore does NOT apply to the linear
growth equation, and sigma(M, z) and f_collapse(>M, z) are identical
to LCDM.

This routine:
  1. Re-imports the Study 19 applicability theorem and verifies it
     returns axiom (A1) FAIL for the linear regime.
  2. Computes what the JWST tension WOULD have looked like if the
     deferred-resolution path were taken (i.e. naive R(u) boost on
     D(z)) - for honest comparison, not as a viable physical path.
  3. Computes R(u) at the characteristic ACCELERATION of a collapsed
     z=8 halo (the regime where (A1) IS restored), to see whether
     in-halo R(u) provides any headroom for raising the cosmic
     star-formation-efficiency ceiling epsilon*_max.
  4. Reports the verdict honestly:
       - Linear-growth resolution path: CLOSED by Study 19 theorem.
       - In-halo R(u) at z=8 halo edge: numerical value reported.
       - Net effect on JWST tension: stated explicitly.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

# Make Study 19's growth module importable.
_STUDY_19 = Path(__file__).resolve().parents[2] / "F06_linear_growth_s8_prediction" / "scripts"
if str(_STUDY_19) not in sys.path:
    sys.path.insert(0, str(_STUDY_19))

from esd_core import OMEGA_M_LOCK, OMEGA_B_LOCK
from esd_growth import (   # type: ignore[import-not-found]
    R_of_u,
    applicability_test_linear_perturbation,
    applicability_test_collapsed_halo,
)
from esd_jwst import (
    RHO_STAR_LABBE, F_COLLAPSE_HIGHZ, EPS_STAR_BK2023, EPS_STAR_BK2023_HI,
    epsilon_star_min, rho_baryon_0,
)


# --- physical constants (SI) ----------------------------------------------
G_SI    = 6.67430e-11
MSUN_KG = 1.98892e30
MPC_M   = 3.0856775814913673e22
KPC_M   = MPC_M / 1.0e3
A0_SI   = 1.2e-10               # MOND a_0, matches sim01 / esd_jwst convention


# Critical density at z=0 in SI for h=0.6736 (Planck/ESD lock).
H0_PLANCK_SI = 67.36 * 1.0e3 / MPC_M
RHO_CRIT_0_SI = 3.0 * H0_PLANCK_SI**2 / (8.0 * math.pi * G_SI)


# --- linear-growth applicability check ------------------------------------

def linear_growth_applicability() -> dict:
    """Cite Study 19's theorem: does R(u) modify the linear growth eqn?"""
    return applicability_test_linear_perturbation()


# --- naive (would-be) growth boost: forbidden by Study 19 -----------------

def naive_growth_boost(z: float, u_proxy: float = 1.0) -> dict:
    """If R(u) DID modify linear growth (it does NOT, per Study 19),
    what factor would D(z) and sigma(M,z) be boosted by?

    Use the simple flat-mu approximation mu_eff = 1 + R(u_proxy) in
    the growth equation, evaluated at a single representative u.
    This is computed only for SCALE of the would-be effect; it is
    NOT a physically valid prediction.
    """
    R = R_of_u(u_proxy)
    # Quasi-static estimate: D(z) -> D(z) * sqrt(1 + R) over a few e-folds.
    # The exact factor depends on integration; sqrt(mu) is the WKB
    # leading order for a constant-mu growth equation.
    sigma_boost = math.sqrt(1.0 + R)
    # delta_c is unchanged; nu = delta_c/sigma so:
    delta_c = 1.686
    nu_old  = delta_c / 1.0   # arbitrary normalization; only ratio matters
    nu_new  = nu_old / sigma_boost
    # f_collapse ~ erfc(nu/sqrt2) is exponentially sensitive in nu.
    f_old = math.erfc(nu_old / math.sqrt(2.0))
    f_new = math.erfc(nu_new / math.sqrt(2.0))
    return {
        "z":             z,
        "u_proxy":       u_proxy,
        "R(u_proxy)":    R,
        "sigma_boost":   sigma_boost,
        "f_collapse_old":     f_old,
        "f_collapse_new":     f_new,
        "f_collapse_ratio":   f_new / f_old if f_old > 0 else float("inf"),
        "epsilon_star_reduction_factor": f_new / f_old if f_old > 0 else 0.0,
        "PHYSICALLY_VALID":  False,
        "reason_invalid":    "Study 19 theorem: axiom (A1) fails for linear modes.",
    }


# --- in-halo R(u) at a representative z=8 halo edge -----------------------

def in_halo_acceleration(M_halo_msun: float, z: float,
                          delta_vir: float = 200.0) -> dict:
    """Compute g at the virial radius of a halo of mass M_halo at z.

    Uses the spherical-collapse virial overdensity delta_vir relative
    to rho_crit(z).  In matter domination (good at z >> 0):

        rho_crit(z) = rho_crit_0 * (Omega_m (1+z)^3 + 1 - Omega_m)
        r_vir       = [3 M / (4 pi delta_vir rho_crit(z))]^(1/3)
        g_vir       = G M / r_vir^2
    """
    Ez2 = OMEGA_M_LOCK * (1.0 + z)**3 + (1.0 - OMEGA_M_LOCK)
    rho_crit_z = RHO_CRIT_0_SI * Ez2
    M = M_halo_msun * MSUN_KG
    r_vir = (3.0 * M / (4.0 * math.pi * delta_vir * rho_crit_z))**(1.0/3.0)
    g_vir = G_SI * M / r_vir**2
    u = 4.0 * g_vir / A0_SI
    return {
        "M_halo_msun": M_halo_msun,
        "z":            z,
        "r_vir_kpc":    r_vir / KPC_M,
        "g_vir_m_s2":   g_vir,
        "u":            u,
        "R(u)":         R_of_u(u),
        "epsilon_max_dressed": EPS_STAR_BK2023 * (1.0 + R_of_u(u)),
    }


# --- main report ----------------------------------------------------------

def verdict() -> dict:
    """End-to-end honest verdict for the JWST tension under ESD."""
    eps_obs = epsilon_star_min(RHO_STAR_LABBE)
    # in-halo dressing at the BK threshold halo mass, evaluated at z=8.
    halo = in_halo_acceleration(M_halo_msun=10.0**10.7, z=8.0)
    R_inhalo = halo["R(u)"]
    eps_max_dressed = EPS_STAR_BK2023 * (1.0 + R_inhalo)

    # is the tension closed?
    closed_by_inhalo = eps_obs <= eps_max_dressed
    # how much would in-halo boost have to be?
    R_required = max(0.0, eps_obs / EPS_STAR_BK2023 - 1.0)

    return {
        "epsilon_star_observed":  eps_obs,
        "epsilon_max_standard":   EPS_STAR_BK2023,
        "tension_factor":         eps_obs / EPS_STAR_BK2023,
        "linear_growth_path":     "CLOSED (Study 19 theorem; axiom A1 fails)",
        "in_halo_R(u)_at_z8":     R_inhalo,
        "epsilon_max_dressed":    eps_max_dressed,
        "tension_closed_by_inhalo": closed_by_inhalo,
        "R_required_to_close":    R_required,
        "halo_diagnostic":        halo,
    }


def main() -> int:
    print("=" * 72)
    print("Study 13 extension - R(u) applicability to JWST baryon-budget tension")
    print("=" * 72)
    print()
    print("--- Step 1: Linear-growth applicability (Study 19 theorem) ---")
    a = linear_growth_applicability()
    print(f"  axiom (A1) bound-system locality   : {a['A1_bound_system_locality']}")
    print(f"  axiom (A2) acceleration definedness: {a['A2_acceleration_definedness']}")
    print(f"  axiom (A3) closure-universality    : {a['A3_closure_universality']}")
    print(f"  R(u) applies to linear growth      : {a['Ru_applies']}")
    print(f"  rationale: {a['rationale']}")
    print()

    print("--- Step 2: Naive would-be growth boost (forbidden) ---")
    naive = naive_growth_boost(z=8.0, u_proxy=1.0)
    print(f"  u_proxy                 = {naive['u_proxy']}")
    print(f"  R(u_proxy)              = {naive['R(u_proxy)']:.3f}")
    print(f"  sigma boost factor      = {naive['sigma_boost']:.3f}")
    print(f"  f_collapse ratio        = {naive['f_collapse_ratio']:.3f}")
    print(f"  PHYSICALLY VALID        : {naive['PHYSICALLY_VALID']}")
    print(f"  why not                 : {naive['reason_invalid']}")
    print()

    print("--- Step 3: In-halo R(u) at characteristic z=8 BK halo ---")
    halo = in_halo_acceleration(M_halo_msun=10.0**10.7, z=8.0)
    print(f"  M_halo (BK threshold)   = 10^10.7 Msun")
    print(f"  r_vir at z=8            = {halo['r_vir_kpc']:.3f} kpc")
    print(f"  g_vir                   = {halo['g_vir_m_s2']:.3e} m/s^2")
    print(f"  u = 4 g / a_0           = {halo['u']:.3e}")
    print(f"  R(u)                    = {halo['R(u)']:.3e}")
    print()

    print("--- Step 4: Verdict ---")
    v = verdict()
    print(f"  observed epsilon_*       = {v['epsilon_star_observed']:.3f}")
    print(f"  standard epsilon_*_max   = {v['epsilon_max_standard']:.2f}")
    print(f"  tension factor (obs/max) = {v['tension_factor']:.2f} x")
    print(f"  linear-growth path       : {v['linear_growth_path']}")
    print(f"  in-halo R(u) at z=8      = {v['in_halo_R(u)_at_z8']:.3e}")
    print(f"  in-halo-dressed eps_max  = {v['epsilon_max_dressed']:.3f}")
    print(f"  tension closed in-halo?  : {v['tension_closed_by_inhalo']}")
    print(f"  R required to close      = {v['R_required_to_close']:.2f}")
    print()

    print("--- Honest summary ---")
    if v["tension_closed_by_inhalo"]:
        print("  ESD closes the JWST baryon-budget tension via in-halo R(u).")
    else:
        print("  ESD does NOT close the JWST baryon-budget tension via R(u).")
        print(f"  * Linear-growth path is forbidden (Study 19 theorem).")
        print(f"  * In-halo R(u) at z=8 BK halos is too small (R = "
              f"{v['in_halo_R(u)_at_z8']:.3e}) - halos are compact at high z,")
        print(f"    so g >> a_0 and R(u) -> 0 (UV-clean limit).")
        print(f"  * Would need R >= {v['R_required_to_close']:.2f} - not available")
        print(f"    in this acceleration regime.")
        print(f"  * Resolution must come from another channel (gas cooling,")
        print(f"    SFE physics, or observational systematics in M_*).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
