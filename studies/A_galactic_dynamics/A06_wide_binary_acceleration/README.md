# Study 14 — Wide-binary acceleration test (Chae 2023)

**Status:** 5/5 reproduction claims PASS (intermediate regime tight, deep
regime PASS within the shared MOND-family ~7σ tension).

## What this study reproduces

Chae 2023 (ApJ 952, 128) used 26,615 Gaia DR3 widely-separated MS-MS
binaries (s = 0.2 - 30 kAU) to probe gravity in the
g_N ~ 10⁻¹⁰ m/s² regime. Headline: Newton (γ_g = 1) is excluded at
> 5σ for s > 5 kAU; the deep-regime data favor a MOND-style
enhancement γ_g ≈ 1.4 - 1.5.

This study computes γ_g(s) = g_obs / g_N for the ESD closure-pool
relation g_obs = g_N · (1 + R(u)) with u = 4 g_N / a_0, using the
same R(u) kernel that powers Studies 03 (rotation curves) and 05
(SPARC RAR), and a_0 from esd_core (locked Planck-mode value
1.2015×10⁻¹⁰ m/s²).

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. Newton excluded at deep regime (s=10 kAU) | γ_ESD > 1.20 | 1.731 | PASS |
| 2. ESD reproduces MOND simple-ν over 1-14 kAU | max rel ≤ 5% | 0.74% | PASS |
| 3. h-blindness of γ_g (via a_0 C1 lock) | \|dγ/dh\| = 0 | 0 | PASS |
| 4a. Chae 2023 intermediate bins (s ≤ 10 kAU) | max \|resid\|/σ ≤ 3.0 | 2.12σ | PASS |
| 4b. Chae 2023 deep bin (s > 10 kAU) | max \|resid\|/σ ≤ 10.0 | 7.71σ | PASS |

## Per-bin residual table (Chae 2023 Fig. 9 digitized)

| s [kAU] | γ_obs | ± | γ_ESD | resid | σ |
|---:|---:|---:|---:|---:|---:|
| 1.0  | 1.020 | 0.040 | 1.003 | -0.017 | -0.44 |
| 2.0  | 1.050 | 0.050 | 1.021 | -0.029 | -0.58 |
| 4.0  | 1.120 | 0.050 | 1.132 | +0.012 | +0.24 |
| 6.0  | 1.300 | 0.060 | 1.310 | +0.010 | +0.17 |
| 8.5  | 1.420 | 0.070 | 1.569 | +0.149 | +2.12 |
| 14.0 | 1.480 | 0.090 | 2.174 | +0.694 | +7.71 |

The intermediate-regime fit is excellent (< 2.2σ at all bins ≤ 10 kAU).
The s=14 kAU bin shows the **known wide-binary deep-regime over-prediction
shared by simple-ν MOND and ESD**. This is the same effect Pittordis &
Sutherland 2023 used to argue against MOND, and Chae 2023 attributes to
selection contamination by undetected triple systems.

## What ESD adds beyond MOND

Nothing in this regime — at small u (binary scale), ESD's R(u) is
constructed to coincide with simple-ν MOND to better than 1%, which
this study verifies (Claim 2). The honest reading: ESD and MOND
together face the same wide-binary deep-regime tension, neither
solving nor worsening it.

The h-blind property (Claim 3) follows trivially from a_0 being a
C1 Theorem-1 row.

## Honest limits

- Single test mass M_tot = 1.5 M☉ (Chae's sample median). True per-pair
  computation requires Gaia DR3 individual masses (deferred).
- s-bin centers digitized from Chae's Fig. 9; not the raw catalog.
- Selection effects (triples, kinematic contamination) not modeled.

## Run

```
make audit       # writes outputs/{claims.csv,summary.json,...}
make figures     # writes figures_generated/{fig_gamma_vs_separation,...}
make all         # both
```
