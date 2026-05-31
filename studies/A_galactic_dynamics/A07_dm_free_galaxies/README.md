# Study 16 — DM-free UDGs (NGC 1052-DF2 / DF4)

**Status:** 4/4 reproduction claims PASS.

## What this study reproduces

van Dokkum+2018 (Nature 555, 629) discovered that the ultra-diffuse
galaxy NGC 1052-DF2 has σ_los = 7.8 ± 1.7 km/s — close to the
Newtonian baryon-only prediction (~7 km/s) and **well below** simple-ν
MOND's no-EFE prediction (~20 km/s). DF4 (van Dokkum+2019,
σ = 4.2 ± 1.4 km/s) showed the same. These were widely advertised as
the "MOND killer" measurements.

McGaugh & Milgrom 2013 had already shown that MOND with the
**external field effect (EFE)** — the satellite UDG sits in the
gravitational field of the host NGC 1052 — relaxes the prediction back
to ~8–9 km/s, restoring consistency.

This study verifies the same structural picture in ESD: the locked
closure-pool kernel R(u) reproduces simple-ν MOND essentially exactly
in the relevant regime, and a simple `u = (g_int + g_ext)/...`
aggregation provides a meaningful EFE-style relaxation.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. ESD-no-EFE matches simple-ν MOND (apples-to-apples) | rel ≤ 5% | **0.18%** | PASS |
| 2. ESD-no-EFE reproduces the "MOND killer" tension | ≥ 3σ | 5.93σ | PASS |
| 3. ESD-with-EFE reduces tension by factor ≥ 1.3 | ratio ≥ 1.3 | 1.46× | PASS |
| 4. h-blindness of σ_ESD via a_0 (Thm 1, C1) | = 0 | 0 | PASS |

## Per-UDG table

| | DF2 | DF4 |
|---|---:|---:|
| σ_obs (km/s) | 7.8 ± 1.7 | 4.2 ± 1.4 |
| σ_N (pub) | 7.0 | 6.0 |
| MOND no-EFE (pub) | 20.0 | 18.0 |
| MOND with-EFE (pub) | 9.0 | 8.0 |
| **ESD no-EFE** | **15.8** (+4.7σ) | **12.5** (+5.9σ) |
| **ESD with-EFE** | **11.3** (+2.1σ) | **9.9** (+4.1σ) |
| EFE improvement | ×2.25 | ×1.46 |

## Honest reading

- **DF2 is reconciled** to within 2.1σ by ESD-with-EFE; effectively
  matches MOND-with-EFE behavior.
- **DF4 retains residual tension** at 4.1σ for ESD-with-EFE (and 2.7σ
  for the published MOND-with-EFE). DF4 is genuinely hard for any
  modified-gravity framework using a MOND-style boost; the
  4.2 ± 1.4 km/s measurement sits below even the Newtonian baryon
  prediction of 6 km/s (which is itself dependent on stellar-mass
  estimates and dynamical-mass tracers).
- A fuller QUMOND-style EFE prescription (with deep-external-field
  quasi-Newtonianization when g_ext > g_int > a_0) is deferred. The
  current ESD EFE-aggregation `u = (g_int + g_ext)/a_0` provides
  meaningful improvement but does not fully reproduce the published
  MOND-EFE numbers.

## Run

```
make audit       # writes outputs/{claims.csv,summary.json,...}
make figures     # writes figures_generated/{fig_sigma_compare,...}
make all
```
