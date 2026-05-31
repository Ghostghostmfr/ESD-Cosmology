# Study 17 — EHT photon-ring shadows (M87* and Sgr A*)

**Status:** 4/4 reproduction claims PASS.

## What this study reproduces

The Event Horizon Telescope measured the photon-ring angular diameters
of M87* (EHT Collaboration 2019: θ = 42 ± 3 μas) and Sgr A* (EHT
Collaboration 2022: θ = 51.8 ± 2.3 μas). Both measurements are
consistent with the Schwarzschild prediction θ = 2√27 GM/(c² D).

ESD's closure-pool kernel R(u) = s/Σ(u) is built to add an
infrared-only correction (matters at u ~ 1, i.e. g ~ a_0). In the
strong-field regime near a black hole horizon, u = 4g_N/a_0 is
astronomically large, so R(u) → 0 by construction. This study
verifies that ESD reproduces the GR shadow predictions to absurd
precision and remains consistent with the EHT measurements.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. ESD ring diameter matches GR (strong-field) | rel ≤ 1e-6 | 0 | PASS |
| 2. EHT measurements consistent with ESD/GR | ≤ 2σ | 0.77σ | PASS |
| 3. Closure correction R(u) at photon sphere negligible | ≤ 1e-10 | 3.3e-21 | PASS |
| 4. h-blindness of θ_ring (Thm 1 via a_0) | ≤ 1e-15 | 0 | PASS |

## Per-source table

| | M87* | Sgr A* |
|---|---:|---:|
| Mass (M_☉) | 6.5e9 | 4.154e6 |
| Distance | 16.8 Mpc | 8.275 kpc |
| θ_obs (μas) | 42.0 ± 3.0 | 51.8 ± 2.3 |
| θ_GR (μas) | 39.70 | 51.51 |
| **θ_ESD (μas)** | **39.70** | **51.51** |
| R(u_ps) | 3.3e-21 | 2.3e-26 |
| tension | 0.77σ | 0.13σ |

## Interpretation

This is a **null test** for ESD: the framework's IR-only screening
mechanism is structurally invisible at the strong-field scale probed
by EHT. The closure-pool correction R(u) at the photon sphere is
~10^-21 for M87* and ~10^-26 for Sgr A* — eighteen orders of
magnitude below any measurable astrophysical effect.

This complements Studies 13–16 (where ESD reproduces deep-MOND
phenomenology) by demonstrating that the framework does **not**
introduce spurious modifications in regimes where GR has been
precision-tested. The closure-pool kernel is genuinely
acceleration-localized, not a global modification of gravity.

## Run

```
make audit       # writes outputs/{claims.csv,summary.json,...}
make figures     # writes figures_generated/{fig_ring_compare,...}
make all
```
