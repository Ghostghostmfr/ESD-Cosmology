"""
Phase 3 Step 3: closure derivation of effective fifth-force coupling
on linear cosmological perturbations.

ESD Framework (Higginson 2026) Ch.4 architecture (read together):
  L57:   "the same canonical normalization that locked the golden-ratio
          response eliminates the remaining action-side ratio beta_m^2/alpha"
  L111:  "c^4 descends from two factors of the canonical normalization
          kappa = 1/c on the matter bridge at the DEEP-MOND FLOOR"
  R(u) = s/Sigma(u) with Sigma(u) = u^phi + b u^q + c, q = 2 ln phi / phi
  Deep-MOND limit: R(u -> 0) = s/c ~ 47 (saturation at IR floor)
  Newtonian limit: R(u -> inf) = s/u^phi -> 0

Interpretation:
  - R(u) is the STATIC nonlinear matter-bridge closure for galactic
    systems (single dominant acceleration g_N).
  - kappa = 1/c is the deep-MOND-floor canonical normalization.
  - On LINEAR cosmological perturbations the kinetic function is in
    its linear regime F(Y) -> Y with F'(0) fixed by canonical
    normalization, and beta_m^2/alpha is structurally absorbed by
    the closure that fixes a_0 and the locked Omega's.
  - Therefore the framework's LINEAR-PERTURBATION prediction is
    LCDM with the closure-locked (Omega_m, Omega_DM, Omega_b, Omega_L).
  - The R(u) closure applies to STATIC SPHERICAL galactic systems
    (rotation curves, clusters) -- NOT to linear cosmological growth.

This script computes the static R(u) closure on the operationally
relevant range and confirms:
  - galactic regime (u ~ 0.01 - 1): R(u) ~ O(1-50), the MOND signature
  - cluster regime (u ~ 1 - 100): R(u) ~ O(0.01 - 1), the transition
  - cosmological Newtonian sub-horizon (u >> 100): R(u) -> 0, LCDM-like
"""
from __future__ import annotations
import math
import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI = math.log(PHI)
C_CLOSURE = (4.0 * LN_PHI - 1.0) / PHI
S_CLOSURE = 16.0 * PHI + 1.0
B_CLOSURE = PHI**6 - 2.0
Q_CLOSURE = 2.0 * LN_PHI / PHI

KAPPA = 1.0 / C_CLOSURE  # matter-bridge normalization at deep-MOND floor

def Sigma(u):
    return u**PHI + B_CLOSURE * u**Q_CLOSURE + C_CLOSURE

def R(u):
    return S_CLOSURE / Sigma(u)

print("=" * 72)
print("Phase 3 Step 3: closure derivation of effective coupling")
print("=" * 72)
print(f"\nClosure pool")
print(f"  phi   = {PHI:.10f}")
print(f"  c     = {C_CLOSURE:.10f}  -> kappa = 1/c = {KAPPA:.10f}")
print(f"  s     = {S_CLOSURE:.10f}")
print(f"  b     = {B_CLOSURE:.10f}")
print(f"  q     = 2 ln phi / phi = {Q_CLOSURE:.10f}")

print(f"\nMatter-bridge canonical normalization at deep-MOND floor")
print(f"  kappa = 1/c = {KAPPA:.6f}")
print(f"  kappa^2 = 1/c^2 = {KAPPA**2:.6f}")
print(f"  This sets the static-galactic deep-MOND amplitude R(0) = s/c = {S_CLOSURE/C_CLOSURE:.4f}")
print(f"  (corresponds to galactic deep-MOND boost factor)")

print(f"\nStatic R(u) closure on the operational u-range")
print(f"  R(u) = g/g_N - 1 = s / Sigma(u)")
print(f"  Sigma(u) = u^phi + b u^q + c")
print()
print(f"  {'u':>12} {'Sigma(u)':>14} {'R(u)':>14} {'regime':>30}")
print(f"  " + "-"*72)
u_grid = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 1e6, 1e21]
labels = ["deep MOND", "deep MOND", "MOND", "transition", "cluster",
          "Galaxy/cosmo edge", "deep Newton", "lab", "solar system (Cassini)"]
for u, lbl in zip(u_grid, labels):
    print(f"  {u:>12.3e} {Sigma(u):>14.4e} {R(u):>14.4e} {lbl:>30}")

print(f"\nStructural interpretation:")
print(f"  - galactic systems (u <~ 1): R(u) >> 1, MOND-like enhancement")
print(f"  - clusters (u ~ 1-10): R(u) ~ 0.1-1, transition")
print(f"  - linear cosmological sub-horizon: R(u) -> 0, LCDM-like")
print(f"  - solar system (u ~ 1e21): R(u) ~ {R(1e21):.2e} (Cassini-safe)")

print(f"\nCassini bound check: beta^2(u_solar) < 1e-9")
print(f"  If beta^2/alpha(u) effective <= R(u)/2 (standard scalar-tensor map),")
print(f"  then beta^2(u_solar)/alpha = R(1e21)/2 = {R(1e21)/2:.3e}")
print(f"  vs MICROSCOPE/Cassini bound 1e-9")
if R(1e21)/2 < 1e-9:
    print(f"  -> framework safely satisfies Cassini at solar-system u")
else:
    print(f"  -> framework VIOLATES Cassini at solar-system u  (would falsify)")

print(f"\n" + "=" * 72)
print(f"Phase 3 Step 3 CONCLUSION")
print(f"=" * 72)
print(f"""
1. R(u) is the framework's STATIC NONLINEAR closure for systems with a
   single dominant acceleration g_N (galaxies, clusters, solar system).

2. The matter-bridge canonical normalization kappa = 1/c is fixed at the
   DEEP-MOND FLOOR. Two factors of kappa = 1/c produce the c^4 weight in
   the cosmological identity (B):  3 Omega_DM + Omega_b = 8 pi c^4 Omega_m.

3. Ch.4 L57: the canonical normalization that locks a_0 also
   ELIMINATES beta_m^2/alpha as a free parameter. The action-level
   coupling is structurally absorbed into a_0 + the locked Omega values.

4. THEREFORE on linear cosmological perturbations:
   - mu_eff(k, a) = 1  (no separate fifth-force boost)
   - The framework's growth prediction IS LCDM at the locked Omega's.
   - Phase 2a + Phase 3 Step 2 already realized this prediction.

5. Static R(u) closure governs:
   - Galactic rotation curves  (R(u <~ 1) sets MOND-like signature)
   - Cluster mass calibration  (R(u ~ 1) sets weak-lensing residual)
   - Solar-system tests        (R(u ~ 1e21) << 1, Cassini-safe)

6. The fsigma_8 chi^2/dof = 0.44 from Step 2 at beta^2/alpha = 0 IS the
   framework's prediction. The 'bracket exercise' was a sanity test that
   confirmed RSD data is consistent with the framework's structural
   absorption of beta^2/alpha into the locked cosmology.

7. Falsification routes for Phase 3 thread now live in:
   - Disformal lensing M_lens/M_dyn through beta_Z/beta_m = b
   - SPARC rotation-curve precision (a_0 = 1.20e-10 lock)
   - Cluster weak-lensing mass discrepancy at u ~ 1-10
   - Cosmological H_0 from partition formula (predicts 67.28, SH0ES at 73)
""")
