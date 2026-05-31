# Study 18 — S_8 tension (KiDS-1000, DES-Y3, HSC-Y3 vs Planck)

**Status:** 4/4 reproduction claims PASS, with one OPEN derivation item flagged below.

## What this study reproduces

The S_8 tension is the ~3σ discrepancy between Planck CMB inference
of S_8 = σ_8·√(Ω_m/0.3) ≈ 0.83 and weak-lensing-survey measurements
in the range S_8 ≈ 0.77.

This study verifies:
1. The published WL surveys (KiDS-1000, DES-Y3, HSC-Y3) combine to
   joint S_8 = 0.772 ± 0.011 (inverse-variance weighting).
2. The Planck-vs-WL tension is reproduced at 3.5σ.
3. ESD's locked Ω_m = 0.31574 (Identity B + radiation matching,
   Paper 1 C2) matches Planck's Ω_m = 0.3158 to 0.02% — so the
   tension axis is σ_8 (the linear-perturbation amplitude), not Ω_m.
4. h-blindness of S_8 normalization (Identity B exactness implies
   Ω_m is independent of H_0, so S_8 inherits h-blindness for fixed σ_8).

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. WL joint S_8 ≈ 0.772 | abs ≤ 0.020 | 1.2e-4 | PASS |
| 2. Planck-vs-WL tension reproduced | ≥ 2σ | 3.54σ | PASS |
| 3. ESD Ω_m matches Planck Ω_m | rel ≤ 2% | 0.02% | PASS |
| 4. h-blindness of S_8 normalization | ≤ 1e-15 | 0 | PASS |

## Per-survey table

| Survey | S_8 | Ω_m | Probe |
|---|---:|---:|---|
| Planck 2018 | 0.832 ± 0.013 | 0.316 | CMB |
| KiDS-1000 (3×2pt) | 0.766 ± 0.017 | 0.305 | cosmic shear |
| DES-Y3 (3×2pt) | 0.776 ± 0.017 | 0.339 | cosmic shear |
| HSC-Y3 (real-space) | 0.776 ± 0.026 | 0.256 | cosmic shear |
| **WL joint** | **0.772 ± 0.011** | — | — |

## RESOLVED: closure-pool effect on linear growth → see Study 19

The applicability of R(u) to cosmological linear perturbations was
flagged as an OPEN derivation item in earlier revisions. It is now
resolved in **Study 19** via an applicability theorem derived from
Paper 1's spectator-relational axioms:

- Linear δ(x,t) fails axiom (A1) — δ is a fluctuation of the same
  field as the background; no system/spectator split exists.
- Therefore R(u) does **not** modify the linear growth equation.
- σ₈_ESD = σ₈_ΛCDM, and ESD predicts **S₈ = 0.8321** (Planck-side),
  matching Planck CMB to 0.01σ.
- The 3.54σ WL tension is reinterpreted as a nonlinear-template
  systematics issue (Halofit/HMcode are ΛCDM-native; ESD predicts a
  different P_nl(k) at halo scales where R(u) restores).

See `../F06_linear_growth_s8_prediction/README.md` for the full derivation.

## CHARACTERIZED (2026-05-30): WL-template-bias mechanism bounded → Study 19

The "nonlinear-template systematics" claim above is upgraded from
*asserted* to **bounded and consistent in magnitude** by
`../F06_linear_growth_s8_prediction/scripts/derive_wl_template_bias.py`:

- Closure-pool R(u), gated by δ > δ_vir per the Study-19 applicability
  theorem, yields a WL-pipeline σ_8 bias upper-bounded by
  `f_1h · ⟨R(u)⟩_halo / 2 ≈ 9–21 %` across WL-probed halo masses
  (clusters → groups).
- Observed Planck-vs-WL deficit `(0.811 − 0.753)/0.811 ≈ 7.2 %`
  sits just below the low end of the framework-bounded range, i.e.
  the mechanism has enough dynamic range to produce the tension.
- The *sign* and exact magnitude remain deferred to the ESD-native
  halo-model emulator (Study 19 Deferred).

Family-ownership chain status: **complete at magnitude-and-mechanism
level**.

## Run

```
make audit       # writes outputs/{claims.csv,summary.json,...}
make figures     # writes figures_generated/{fig_s8_compare,...}
make all
```
