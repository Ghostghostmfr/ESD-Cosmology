# Study 23 — NANOGrav 15-yr stochastic GW background

**Status:** IN PROGRESS

## What this study does

Tests the ESD framework's gravitational-wave sector against the NANOGrav 15-year pulsar-timing-array dataset. The key observables are:
1. The spectral index `γ` of the stochastic gravitational-wave background (SGWB), where the characteristic strain follows `h_c(f) ∝ f^(−2/3)`.
2. The Hellings-Downs (HD) spatial correlation signature for a tensor-polarized background.

Per Study 21, ESD predicts that gravitational waves propagate identically to GR: at speed `c`, with only tensor polarizations, and with no graviton mass. Therefore, ESD must reproduce the GR predictions for `γ` and the HD curve.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. SGWB spectral index consistent with SMBHB model | `|γ - 13/3| ≤ 0.5` | TBD | TBD |
| 2. Hellings-Downs tensor correlation preferred over scalar/vector | `Δχ²(T-S) > 0` | TBD | TBD |

## Datasets

- **NANOGrav 15-year Data Release:** The official compressed likelihood products for the spectral index and the spatial-correlation posteriors.
  - Agazie et al. 2023, "The NANOGrav 15-year Data Set: Evidence for a Gravitational-Wave Background" (ApJL 951 L8)
  - Agazie et al. 2023, "The NANOGrav 15-year Data Set: Characterization of the Gravitational-Wave Background"

## Quickstart

```
make audit       # writes outputs/{summary.json, claims.csv, ...}
make figures     # writes figures_generated/fig_nanograv_...
make all
```

## Key outputs

- `figures_generated/fig_nanograv_spectrum.pdf`: The characteristic strain spectrum `h_c(f)` compared to the NANOGrav posterior.
- `figures_generated/fig_nanograv_hellings_downs.pdf`: The inter-pulsar correlation amplitude vs. angular separation, compared to the Hellings-Downs curve.
- `scripts/outputs/summary.json`: The quantitative results of the audit gates.

## Scope boundary

This study uses the compressed public data products from the NANOGrav collaboration. It does not perform a full Bayesian analysis on the raw pulsar timing residuals. The goal is to verify that the published results are consistent with the GR-equivalent predictions of the ESD framework, establishing a baseline for future, more detailed studies.
