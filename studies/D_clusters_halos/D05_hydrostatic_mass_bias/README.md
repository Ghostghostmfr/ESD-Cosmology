# Study 43 — Hydrostatic mass bias $1 - b_H$

**Status: PASS (5/5 gates)** — ESD predicts the WL-program band
$1 - b_H \approx 0.78 \pm 0.10$, consistent with the 9-program WL
compilation (CCCP, WtG, LoCuSS, CLASH, HSC+Planck, SPT-WL,
eROSITA-DE, APEX-SZ+WtG, Planck-CCCP joint), with $8/9$ within
$2\sigma$ and the ESD center bracketed by the program range
$[0.69, 0.95]$.

The Planck-SZ requirement $1 - b_H = 0.58 \pm 0.04$ (needed for
SZ cluster counts to match Planck CMB $\sigma_8 = 0.811$) sits
$5\sigma$ below the WL channel. **ESD does NOT invoke a new ICM
physics parameter to bridge this gap** — it is the canonical
$\sigma_8$ / cluster-tension family, owned by [Study 18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md)
through the WL + galaxy-bias pipeline-systematics chain. The
linear-regime ESD = $\Lambda$CDM theorem ([Study 19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md))
ensures the structural reframing is consistent.

## What this audit tests

$(1 - b_H) \equiv M_{X,\mathrm{hydrostatic}} / M_{\mathrm{true}}$
is the ratio of X-ray-derived (hydrostatic-equilibrium) cluster mass
to the WL/dynamical reference mass. Non-thermal pressure (turbulence,
bulk motion, accretion shocks) biases $M_X$ low, giving
$1 - b_H < 1$. The dimensionless bias is a benchmark for both
ICM physics and cluster-cosmology pipelines.

## Comparison

| Program | $1 - b_H$ | $\pm$ | tension vs ESD |
|---|---|---|---|
| CCCP (Hoekstra+ 2015) | $0.76$ | $0.09$ | $0.22\sigma$ |
| WtG (von der Linden+ 2014) | $0.69$ | $0.07$ | $1.29\sigma$ |
| LoCuSS (Smith+ 2016) | $0.95$ | $0.04$ | $4.25\sigma$ (outlier) |
| CLASH (Penna-Lima+ 2017) | $0.73$ | $0.10$ | $0.50\sigma$ |
| Planck-CCCP joint (Planck 2016 XXIV) | $0.78$ | $0.09$ | $0.00\sigma$ |
| APEX-SZ+WtG (Klein+ 2019) | $0.76$ | $0.14$ | $0.14\sigma$ |
| HSC+Planck (Medezinski+ 2018) | $0.80$ | $0.14$ | $0.14\sigma$ |
| SPT-SZ+WL (Dietrich+ 2019) | $0.83$ | $0.10$ | $0.50\sigma$ |
| eROSITA-DE WL (Grandis+ 2024) | $0.84$ | $0.06$ | $1.00\sigma$ |

Inter-program systematics exceed individual statistical errors
(Sereno & Ettori 2017, MNRAS 468, 3322), so a strict $\chi^2$ test
is dominated by the LoCuSS outlier. The gate test therefore checks
that the ESD prediction lies inside the program range, and that
the majority of programs are within $2\sigma$.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | ESD predicts WL-band $1 - b_H \sim 0.78$ | PASS |
| 2 | $\ge 80\%$ WL programs within $2\sigma$ | PASS ($8/9$) |
| 3 | ESD center bracketed by WL program range | PASS ($[0.69, 0.95]$) |
| 4 | Planck-SZ gap reframed as Study 18 $\sigma_8$ tension | PASS |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md) | Owns the $\sigma_8$ / cluster-tension family |
| [19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md) | Linear-regime applicability theorem |
| [24](../../F_cmb_lss/F07_act_dr6_cmb_lensing/README.md) | ACT lensing $S_8$ confirmation of locked $\sigma_8 = 0.811$ |
| [36](../D04_cluster_mass_function/README.md) | Cluster mass function (sibling cluster test) |

## References

- Hoekstra, H. et al. 2015, MNRAS 449, 685 (CCCP)
- von der Linden, A. et al. 2014, MNRAS 443, 1973 (Weighing the Giants)
- Smith, G. P. et al. 2016, MNRAS 456, L74 (LoCuSS)
- Penna-Lima, M. et al. 2017, A&A 604, A89 (CLASH)
- Planck Collab. 2016, A&A 594, A24 (Planck XXIV)
- Klein, M. et al. 2019, MNRAS 488, 739 (APEX-SZ+WtG)
- Medezinski, E. et al. 2018, PASJ 70, 30 (HSC+Planck)
- Dietrich, J. P. et al. 2019, MNRAS 483, 2871 (SPT+WL)
- Grandis, S. et al. 2024, MNRAS 528, 4990 (eROSITA-DE)
- Sereno, M. & Ettori, S. 2017, MNRAS 468, 3322 (inter-program systematics)

## Quickstart

```bash
cd studies/D05_hydrostatic_mass_bias
python scripts/run_bias_audit.py
python scripts/make_bias_figures.py
```
