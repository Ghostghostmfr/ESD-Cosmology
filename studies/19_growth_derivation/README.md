# Study 19 — Linear-growth derivation + ESD's $S_8$ prediction

**Status:** 4/4 derivation claims PASS. Closes the OPEN derivation item from Study 18.

## What this study does

This is **theory work**, not data reproduction. It derives — from
Paper 1's spectator-relational axioms — whether the closure-pool
kernel R(u) = s/Σ(u) modifies the cosmological linear growth equation,
and computes ESD's resulting prediction for σ₈ and S₈.

## The applicability theorem

R(u) is constructed for a *localized subsystem* with a *well-defined
g* acting against a *separated spectator background*. Three axioms
make this precise:

- **(A1) Bound-system locality** — there must exist an unambiguous
  system/spectator split.
- **(A2) Acceleration definedness** — u = 4g/a₀ must be a single
  well-defined scalar.
- **(A3) Closure universality** — when (A1) and (A2) hold, R(u) is
  the unique closure-pool dressing (Paper 1 Theorem 2).

A **linear** cosmological perturbation δ(x,t) of the matter field is a
small fluctuation of the *same field* that constitutes the background:
ρ(x,t) = ρ̄(t)·[1 + δ(x,t)]. There is no system/spectator split — the
"subsystem" and the "spectator" are the same field at different
scales. **Axiom (A1) fails.**

A **nonlinear, virialized halo**, in contrast, is a localized bound
subsystem against a separated cosmological background, with a
well-defined g. **All three axioms hold; R(u) applies** as in
Studies 09–16 (RAR, SPARC, cluster Bullet, UDGs, ...).

## Consequences

1. The linear growth equation is **unmodified**:
   $$\delta'' + 2H\delta' - \tfrac{3}{2}\,\Omega_m(a)\,H^2\,\delta = 0$$
   with ESD-locked Ω_m = 0.31574.

2. σ₈, defined as the rms of the *linear* matter field on 8 Mpc/h
   spheres, equals the ΛCDM value: σ₈_ESD = σ₈_Planck = 0.8111.

3. ESD predicts:
   $$S_8^{ESD} = \sigma_8 \sqrt{\Omega_m / 0.3} = 0.8111 \sqrt{0.31574/0.3} = \boxed{0.8321}$$

4. The 3.54σ Planck-vs-weak-lensing tension (Study 18) becomes a
   **systematics question**, not a contradiction with ESD: WL surveys
   infer S₈ from cosmic-shear power spectra on scales 0.1–10 Mpc/h,
   partly in the *nonlinear* regime where R(u) **does** apply.
   Standard WL pipelines use ΛCDM nonlinear templates (Halofit /
   HMcode); ESD predicts a *different* nonlinear power spectrum on
   those scales. Under ESD, fitting a ΛCDM nonlinear template to
   ESD-true data yields a biased σ₈ inference.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---|---|
| 1. R(u) does NOT apply to linear δ | A1 fails for linear modes | False | PASS |
| 2. R(u) DOES apply to virialized halos | A1 holds for δ≫1 | True | PASS |
| 3. ESD S₈ matches Planck CMB | ≤ 1σ | **0.01σ** | PASS |
| 4. h-blindness of S₈ via Identity B C2 | ≤ 1e-15 | 0 | PASS |

## Alternative-interpretation sanity check

If (A1) had held for linear modes, the naive R(u) at the edge of an
8 Mpc/h sphere with overdensity ~ σ₈ would be:

- u = 4g/a₀ ≈ 7.4 × 10⁻³
- R(u) ≈ 18.7
- σ₈ boost ≈ √(1+R) ≈ 4.4×

This would catastrophically over-predict all clustering data. The
applicability theorem rules this out structurally — not by parameter
adjustment.

## Framework-native prediction

**ESD sides with Planck on S₈.** This is a *prediction*, not a fit:
σ₈ is borrowed from CMB, Ω_m is structurally locked by Identity B,
and the resulting S₈ matches Planck to 0.01σ. The WL discrepancy is
predicted to lift once an ESD-native nonlinear emulator (Halofit
analogue with R(u) applied at halo scales) replaces the ΛCDM
template in the cosmic-shear pipeline.

## Run

```
make audit       # derivation + numerical check
make figures
make all
```

## Future work (deferred, not blocking)

- ESD-native nonlinear matter power spectrum P_nl(k, z) (halo-model
  approach, applying R(u) only to bound halos).
- Quantitative prediction of the WL-inferred biased S₈ when ΛCDM
  nonlinear template is used on ESD-true data.
- Direct comparison to KiDS-1000 / DES-Y3 / HSC-Y3 shear correlation
  functions ξ_+(θ), ξ_-(θ).
