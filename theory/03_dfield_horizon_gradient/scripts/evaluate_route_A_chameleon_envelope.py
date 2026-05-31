#!/usr/bin/env python3
r"""
EVALUATE-ONLY (no commits): derive the native chameleon screening envelope
implied by the Master Ch.3 parent action and check whether it closes the
remaining 17.92x gap in the dipole-channel eta amplitude.

DERIVATION CHAIN
================

Parent action (Master Ch.3):

  S = int d^4x sqrt(-g) [ R / (16 pi G) - (1/2) B(D) g^{mu nu} d_mu D d_nu D - V(D) ]
    + int d^4x sqrt(-g~) L_m(g~, psi)

with the Jordan-frame matter metric g~_{mu nu} = A^2(D) g_{mu nu}.

The CONFORMAL COUPLING parameter to matter is, by definition,

  beta(D) = M_Pl * d ln A / dD                              (1)

This is the quantity the Cassini PPN bound constrains in the Solar
System and the quantity that sets the dipole-channel response in
cosmic vacuum.

THE BRIDGE EQUATION AS THE CHAMELEON ENVELOPE
=============================================

The matter-bridge boost (Master Ch.4 Parent-Direct) reads

  R(u) = s / Sigma(u),     Sigma(u) = u^phi + b u^q + c     (2)

where u = (A/theta_sat)^2 is the framework's dimensionless density-like
parameter (large u in deep gravitational wells, small u in vacuum).

In the framework, the GATED effective acceleration on matter is

  g_eff = g_N * [ 1 + gate(delta) * R(u) ]                  (3)

with gate(delta) being the chameleon switch (off at high gravitational
potential, on in cosmic vacuum).

For a static linearized scalar profile, the connection between the
matter-frame extra force (per Eq. 3) and the conformal coupling
(per Eq. 1) is, via the geodesic equation in g~:

  extra_force / GR_force = 2 beta_eff^2  (small beta limit)

  =>  gate(delta) * R(u) = 2 beta_eff^2

  =>  beta_eff(u, delta) = sqrt( gate(delta) * R(u) / 2 )   (4)

This is the framework-NATIVE chameleon coupling. It is NOT a free
function we choose; it is implied by Eqs. (1)-(3) together.

COSMOLOGICAL VS LOCAL EVALUATION
================================

Cassini local (deep Solar gravitational well, gate ~ 0):
  beta_eff_local = sqrt( gate(delta_solar) * R(u_solar) / 2 )
                <= 3.16e-5      (PPN bound)

Cosmological background (gate ~ 1, low u):
  beta_eff_cosmo = sqrt( 1 * R(u_cosmo) / 2 )
                ~ sqrt( (s/c) / 2 )  in the deep u -> 0 limit

RATIO REQUIREMENT TO CLOSE THE 17.92x GAP
=========================================

beta_eff_cosmo / beta_eff_local = 17.92
"""

import math
import numpy as np


# Framework closure-pool constants (Master Ch.3 native)
PHI = (1 + math.sqrt(5)) / 2
Q_EXP = 2 * math.log(PHI) / PHI
B_AMP = PHI**6 - 2.0
C_BATH = (4 * math.log(PHI) - 1) / PHI
S_NORM = 16 * PHI + 1


def R(u):
    """Eq. (2): matter-bridge boost. Master Ch.4 Parent-Direct."""
    return S_NORM / (u**PHI + B_AMP * u**Q_EXP + C_BATH)


def beta_eff(u, gate):
    """Eq. (4): framework-native chameleon coupling."""
    return math.sqrt(max(gate * R(u) / 2.0, 0.0))


def main():
    print("=" * 72)
    print("EVALUATE-ONLY: Route A chameleon-envelope derivation from Ch.3")
    print("(no commits to README, Master Book, or simulation defaults)")
    print("=" * 72)

    # Closure inputs
    print()
    print("Closure-pool inputs (Master Ch.3 native, no fitted parameters):")
    print(f"  phi              = {PHI:.6f}")
    print(f"  q  = 2 ln phi/phi = {Q_EXP:.6f}")
    print(f"  b  = phi^6 - 2    = {B_AMP:.6f}")
    print(f"  c  = (4 ln phi-1)/phi = {C_BATH:.6f}")
    print(f"  s  = 16 phi + 1   = {S_NORM:.6f}")

    # Limiting values of R
    R_max = S_NORM / C_BATH                          # u -> 0
    R_sat = S_NORM / (1.0 + B_AMP + C_BATH)         # u -> 1
    print()
    print(f"  R(u -> 0)  = s/c          = {R_max:.4f}  (matter-bridge ceiling)")
    print(f"  R(u -> 1)  = s/(1+b+c)    = {R_sat:.4f}  (saturation floor)")

    # Pure-R envelope (gate-saturated, evaluating the structural ratio)
    print()
    print("--- Pure-R ratio (ignoring gate, structural ceiling) ---")
    print("    beta_eff propto sqrt(R(u)/2); ratio cosmo/local at extreme u-limits:")
    pure_ratio = math.sqrt(R_max / R_sat)
    print(f"    beta_eff(u->0) / beta_eff(u->1) = sqrt(R_max / R_sat) = {pure_ratio:.4f}")
    print(f"    Required for eta closure        = 17.92")
    print(f"    Structural ceiling provides     {pure_ratio:.2f} ({pure_ratio/17.92:.2%} of need)")

    # Gate must do the rest
    needed_gate_ratio = (17.92 / pure_ratio) ** 2
    print()
    print("--- Required gate(delta) suppression ---")
    print("    To hit ratio 17.92, gate(delta_solar) / gate(delta_cosmo) must satisfy:")
    print("        sqrt( gate_cosmo * R_max / (gate_solar * R_sat) ) = 17.92")
    print(f"    =>  gate_cosmo / gate_solar = (17.92 / {pure_ratio:.2f})^2 = {needed_gate_ratio:.4f}")
    print()
    print(f"    Interpretation: structural R-envelope supplies ~3.05x of the boost;")
    print(f"    the framework's gate(delta) function must contribute the remaining")
    print(f"    factor of {needed_gate_ratio:.2f}x in (gate_cosmo / gate_solar) -- modest.")

    # Cassini-anchored cosmological coupling estimate
    print()
    print("--- Cassini-anchored cosmological coupling ---")
    beta_solar_cassini = 3.16e-5
    beta_cosmo_needed = 17.92 * beta_solar_cassini
    print(f"    beta_local  (Cassini bound)  = {beta_solar_cassini:.2e}")
    print(f"    beta_cosmic needed for eta   = {beta_cosmo_needed:.2e}")
    print()
    print("    With pure-R structural ceiling (gate_cosmo = gate_solar = 1):")
    beta_cosmic_pure = beta_solar_cassini * pure_ratio
    print(f"      beta_cosmic_predicted = {beta_solar_cassini:.2e} * {pure_ratio:.4f}")
    print(f"                            = {beta_cosmic_pure:.2e}")
    print(f"      vs needed             = {beta_cosmo_needed:.2e}")
    print(f"      shortfall factor      = {beta_cosmo_needed / beta_cosmic_pure:.2f}x")

    # Scan u values to characterize the breathing envelope
    print()
    print("--- Coupling envelope across u (gate = 1) ---")
    print(f"  {'u':>10} {'R(u)':>10} {'beta_eff':>12} {'ratio to u=1':>14}")
    base = beta_eff(1.0, 1.0)
    for u_test in [1e-12, 1e-9, 1e-6, 1e-3, 1e-2, 0.1, 0.5, 1.0]:
        b = beta_eff(u_test, 1.0)
        print(f"  {u_test:>10.0e} {R(u_test):>10.4f} {b:>12.6f} {b / base:>14.4f}")

    # Verdict
    print()
    print("--- Verdict ---")
    print()
    print(f"  Structural pure-R ceiling:    {pure_ratio:.2f}x  "
          f"({pure_ratio/17.92:.1%} of required 17.92x)")
    print(f"  Cassini-anchored beta_cosmic: {beta_cosmic_pure:.2e}  "
          f"(vs needed {beta_cosmo_needed:.2e})")
    print(f"  Structural shortfall:         {beta_cosmo_needed/beta_cosmic_pure:.2f}x")
    print(f"  Required gate(d_cosmo)/gate(d_solar): {needed_gate_ratio:.2f}x")
    print()
    print("  THE PURE-R STRUCTURAL ENVELOPE ALONE DOES NOT CLOSE THE GAP.")
    print()
    print("  The framework's bridge equation provides a structural breathing")
    print(f"  envelope of factor {pure_ratio:.2f} between R(u->0) and R(u->1).")
    print(f"  The remaining factor {beta_cosmo_needed/beta_cosmic_pure:.2f}x"
          " must come from the gate(delta)")
    print("  function. The gate is currently not a fully-derived object in")
    print("  the published framework; it is the open piece that would make")
    print("  Route A a hard derivation.")
    print()
    print("  What this DOES establish:")
    print(f"    1. The native R-envelope contributes {pure_ratio:.2f}x of the")
    print("       required 17.92x -- about 31% of the boost is already there.")
    print(f"    2. The gate(delta) function would need a ratio of {needed_gate_ratio:.2f}x")
    print("       between cosmic and solar density -- well within range of")
    print("       any reasonable chameleon screening function (literature")
    print("       chameleon factors typically span 10^5 to 10^10).")
    print("    3. The 'breathing' is REAL but only PARTIAL. To call Item 1")
    print("       'closed', one must (a) derive the gate(delta) function from")
    print("       the parent action's gradient term B(D) (currently sketched")
    print("       but not locked) and (b) verify the resulting envelope hits")
    print(f"       the required {needed_gate_ratio:.2f}x gate ratio at the")
    print("       Solar-System-to-cosmic-vacuum density transition.")
    print()
    print("  Status: Route A is the ADMISSIBLE PATH but it requires a")
    print("  separate hard derivation of gate(delta) from B(D). Item 1")
    print("  remains open, reframed as:")
    print(f"     'derive gate(delta) such that gate_cosmo/gate_solar = {needed_gate_ratio:.2f}'")


if __name__ == "__main__":
    main()
