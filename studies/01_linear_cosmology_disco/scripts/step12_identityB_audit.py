"""Step 12: Identity B structural audit (Option 1)

ESD Framework (Higginson 2026) Ch.4 derives Identity (B) as a TOPOLOGICAL-REFLECTION identity
with three structurally explicit inputs:

   3 Omega_DM + Omega_b  =  8 pi c^4 Omega_m              (Eq. gravity-identityB-master)
        ^                       ^   ^
        | weight-3 from D-field | | | c^4 = kappa^{-2}, two factors of
        | isotropic 3D gradient | | | canonical normalization kappa = 1/c
        | projection            | | |   on the matter bridge at the
        |                       | | |   deep-MOND floor (Ch.4 L111)
        |                       | | |
   1 from baryon Jordan-frame   | |
   trace of T_munu (Ch.4 L111)  | |
                                | |
                  8 pi from Einstein gravitational coupling
                  (Friedmann prefactor; fixed by definition of Omega)

Combined with closure Omega_m = Omega_DM + Omega_b and Identity A
(Omega_Lambda = 2 pi c^2 / 3) + flatness, the system uniquely fixes:

   Omega_b / Omega_m = (3 - 8 pi c^4) / 2
   Omega_DM / Omega_m = (8 pi c^4 - 1) / 2

QUESTION: where could a closure-pool correction factor (currently set
to 1) hide that would shift 8 pi c^4 by the small amount needed to
bring Omega_b from 0.0501 to ~0.0493 (Planck central)?

The audit below:
 (a) computes the EXACT magnitude of correction needed
 (b) tests every structurally legitimate location where it could enter
 (c) checks whether any closure-pool factor of that size has a derived
     (not numerological) provenance in the ESD Framework (Higginson 2026)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
import esd_core as ESD  # noqa: E402

c = ESD.C_CHANNEL
phi = ESD.PHI
LN_PHI = ESD.LN_PHI

# --- The locked numbers ------------------------------------------------
EIGHT_PI_C4 = 8.0 * math.pi * c**4
OMEGA_M = ESD.OMEGA_M_LOCK
OMEGA_B = ESD.OMEGA_B_LOCK
OMEGA_DM = ESD.OMEGA_DM_LOCK

# Planck central (TT,TE,EE+lowE):
OMEGA_B_PLANCK = 0.0493     # central from Aghanim+ 2020 (omega_b h^2 = 0.02237, h = 0.6736)
OMEGA_B_SIGMA = 0.00033     # ~0.7% on Omega_b directly (1.6 sigma * 0.7% ~ 0.0005)
# Treat the 1.6% framework-vs-Planck gap in Omega_b as the target to close

print("=" * 78)
print("STEP 12: Identity B canonical-normalization audit (Option 1)")
print("=" * 78)
print()
print(f"  c               = {c:.10f}")
print(f"  8 pi c^4 (lock) = {EIGHT_PI_C4:.6f}")
print(f"  Omega_m   lock  = {OMEGA_M:.6f}")
print(f"  Omega_b   lock  = {OMEGA_B:.6f}   (ESD Framework (Higginson 2026) Ch.4 says 1.6% off Planck)")
print(f"  Omega_b Planck  = {OMEGA_B_PLANCK:.6f}")
print(f"  Omega_DM  lock  = {OMEGA_DM:.6f}   (Ch.4 says 0.24% off Planck)")
print(f"  Omega_DM/Omega_b lock   = {OMEGA_DM/OMEGA_B:.4f}")
print()

# --- (a) Required correction magnitude ---------------------------------
# Omega_b / Omega_m = (3 - 8 pi c^4) / 2
# Target Omega_b/Omega_m = OMEGA_B_PLANCK / OMEGA_M = ?
target_ratio = OMEGA_B_PLANCK / OMEGA_M
needed_8pic4 = 3.0 - 2.0 * target_ratio
delta_coef = needed_8pic4 - EIGHT_PI_C4
delta_rel = delta_coef / EIGHT_PI_C4

print("-- (a) Required correction to 8 pi c^4 to close the Omega_b gap --")
print(f"  Target Omega_b/Omega_m  = {target_ratio:.6f}  (current {OMEGA_B/OMEGA_M:.6f})")
print(f"  Required 8 pi c^4       = {needed_8pic4:.6f}")
print(f"  Current  8 pi c^4       = {EIGHT_PI_C4:.6f}")
print(f"  Delta (absolute)        = {delta_coef:+.6f}")
print(f"  Delta (relative)        = {delta_rel*100:+.4f} %")
print()
print("  -> The closure-pool factor we need is approximately:")
print(f"     8 pi c^4 -> 8 pi c^4 * (1 + {delta_rel:.5f})")
print()

# --- (b) Catalogue of structurally legitimate insertion points ----------
print("-- (b) Where could such a correction enter, structurally? --")
print()
print("  L1: Inside the channel weight on Omega_DM (currently exactly 3)")
print("      -> Would require derived isotropy-breaking; rigid in 3+1d FLRW")
print()
print("  L2: Inside the baryon Jordan-frame trace weight (currently exactly 1)")
print("      -> Would require derived conformal-frame mismatch; not in Ch.4")
print()
print("  L3: Inside the Einstein 8 pi prefactor")
print("      -> FIXED by definition of Omega; not a closure-pool insertion")
print()
print("  L4: Inside the canonical normalization kappa = 1/c")
print("      -> c^4 = kappa^(-2)x2 from deep-MOND floor. The deep-MOND")
print("         derivation is at galactic acceleration; the FLRW use is at")
print("         cosmic scale. A finite renormalization kappa_FLRW = kappa_MOND")
print("         * (1 + eps) WOULD show up as 8 pi c^4 -> 8 pi c^4 * (1 + 2 eps)")
print(f"         giving eps_needed = {delta_rel/2.0*100:+.4f} %")
print()
print("  L5: Missing term on the LHS (Omega_r weighted by some channel count)")
print("      -> Omega_r ~ 9.2e-5 at z=0; weight w_r contribution to LHS:")
print(f"         w_r * Omega_r / (8 pi c^4 Omega_m) = {1.0/(EIGHT_PI_C4*OMEGA_M):.4f}")
print(f"         needed to absorb delta = {delta_rel*100:.4f}%")
omr = 9.2e-5
w_r_needed = delta_rel * EIGHT_PI_C4 * OMEGA_M / omr
print(f"         Required weight: w_r = {w_r_needed:.2f}")
print(f"         Not structurally available (Stefan-Boltzmann radiation")
print(f"         is traceless so its T_munu trace is zero -> w_r = 0)")
print()
print("  L6: Finite-rung correction from the inflation cascade truncation")
print("      F_12 = 144 is the total e-fold rung count (Ch.15). The current")
print("      projection treats the de Sitter boundary as N_e -> infinity.")
print("      A leading finite-rung correction would be O(1/F_12) ~ 0.0069")
print(f"      Needed: {delta_rel:.5f} -- this is {delta_rel/(1.0/144):.3f} x (1/F_12)")
print()

# --- (c) Closure-pool candidates of the needed magnitude ----------------
print("-- (c) Closure-pool numbers of the right magnitude (~0.19%) --")
print()

# Fibonacci numbers
F = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
candidates = []
for n in range(8, 17):
    Fn = F[n]
    candidates.append((f"1/F_{n}", 1.0/Fn))
candidates.extend([
    ("c^2/F_12",       c**2 / 144),
    ("c^4/F_8",        c**4 / 21),
    ("c^4/F_9",        c**4 / 34),
    ("LN_PHI/F_13",    LN_PHI/233),
    ("(1-1/phi)/F_12", (1-1/phi)/144),
    ("1/(F_12*phi)",   1.0/(144*phi)),
    ("c^2/(2 F_12)",   c**2/(2*144)),
    ("c^4/F_12",       c**4/144),
])

print(f"  Target relative correction: {delta_rel:+.5f}  (= {delta_rel*100:+.4f}%)")
print()
print(f"  {'candidate':<22} {'value':>10} {'pct':>10} {'Omega_b if used':>17}")
print(f"  {'-'*22} {'-'*10} {'-'*10} {'-'*17}")
for name, val in candidates:
    coef_new = EIGHT_PI_C4 * (1.0 + val)
    omb_new = OMEGA_M * (3.0 - coef_new) / 2.0
    flag = ""
    if abs(omb_new - OMEGA_B_PLANCK) < 0.0005:
        flag = "  <-- close to Planck"
    print(f"  {name:<22} {val:>10.5f} {val*100:>+9.4f}% {omb_new:>17.5f}{flag}")
print()
print("  Note: 'close to Planck' candidates are all numerologically")
print("  consistent with the gap, but NONE are derived from a ESD Framework (Higginson 2026)")
print("  closure-pool identity. They are post-hoc fits.")
print()

# --- The deeper objection ----------------------------------------------
print("-- The ESD Framework (Higginson 2026) Ch.4 L91 ALREADY rejects closure-pool fitting to Omega_b --")
print()
print("  Quote (Ch.4 L91): 'The simple ad-hoc closure-pool fits to the baryon")
print("  fraction Omega_b/Omega_m ~ 0.157 within the small pool {phi^k, q, c,")
print("  1-1/phi^k} all fail at the percent precision now available from CMB")
print("  and BBN; the nearest naive candidates (1/phi^4 = 0.146, 1/phi^3 - ")
print("  1/phi^4 = 0.090) miss by 7 to 40 percentage-points-of-fraction, and")
print("  promoting them would be empirical numerology.'")
print()
print("  Inserting a closure-pool correction factor of size ~0.19% into the")
print("  Identity B coefficient is the SAME ACTIVITY -- fitting Omega_b to")
print("  data via a pool number -- and falls under the same warning.")
print()

# --- The structurally honest conclusion --------------------------------
print("=" * 78)
print("AUDIT VERDICT")
print("=" * 78)
print("""
The required correction to 8 pi c^4 (+0.19%) has the right order of
magnitude for closure-pool numerical accidents (1/F_n, c^k/F_n,
LN_PHI/F_n), but NO candidate from the framework's derived pool gives
this correction as a structural consequence:

  - L1, L2 (channel weights):   rigid (isotropy + Jordan trace are
                                 derived; not adjustable)
  - L3     (Einstein 8 pi):     rigid (definition of Omega)
  - L4     (deep-MOND kappa vs FLRW kappa renormalization):
                                NOT derived in current Ch.4. Would be
                                a NEW derivation step, not a fit.
  - L5     (radiation weight):  zero (T_munu^rad is traceless)
  - L6     (finite F_12 cascade truncation):
                                magnitude plausible but no closed
                                form derived in current Ch.15.

The ESD Framework (Higginson 2026) itself (Ch.4 L91) anticipates this audit and rejects
post-hoc closure-pool fitting to Omega_b as numerology.

==> Option 1 result: the +2.4 sigma Omega_b h^2 tension lives in
    Identity B's coefficient, and the only honest in-frame moves
    to close it are the genuinely NEW derivations L4 or L6:

    L4) Derive whether kappa = 1/c picks up a finite renormalization
        between the deep-MOND boundary (where it's locked) and the
        FLRW background (where it's used).  This would be a Ch.4
        addition: a new propagation step linking the two anchor
        scales of kappa.

    L6) Derive whether the de Sitter boundary projection picks up an
        O(1/F_12) correction from the finite total e-fold count
        F_12 = 144.  This would be a Ch.15 + Ch.4 link: the inflation
        cascade truncation feeding into the cosmological-reduction
        projection.

Either L4 or L6 is a legitimate research move (NOT numerology) because
they would introduce closure-pool factors as DERIVED consequences of
identified physics, not as post-hoc fits.  Both are bookmark-able as
future precision research; neither is a same-day write-up move.

For the current closure paper, the honest record is:

    "Identity B carries the +1.6% residual on Omega_b at the precision
    currently available. The residual lives in the canonical-normalization
    coefficient c^4 and is not absorbable into closure-pool numerology
    (Ch.4 L91). Two NEW derivation routes (deep-MOND -> FLRW finite
    renormalization of kappa; finite-rung correction to the de Sitter
    boundary projection) could close it; both are flagged as open
    precision items."
""")
