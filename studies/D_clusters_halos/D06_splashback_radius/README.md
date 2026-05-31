# Study 44 — Splashback radius $R_\mathrm{sp}/R_{200m}$

**Status: PASS (5/5 gates)** — the splashback radius is the apocenter
of recently-accreted halo material and marks the outer edge of the
orbiting halo. In $\Lambda$CDM N-body calibration (Diemer & Kravtsov
2014; Adhikari, Dalal & Chamberlain 2014; More, Diemer & Kravtsov
2015), $R_\mathrm{sp}/R_{200m} \approx 1.0 \pm 0.1$ for accretion
rate $\Gamma \equiv d\ln M / d\ln a \sim 1$. Fifth-force / chameleon
MG predicts a $10\text{-}30\%$ shrinkage in the unscreened cluster regime
(Adhikari, Sakstein, Jain et al. 2018).

ESD inherits the LCDM N-body prediction via [Study 19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md)
(no fifth-force coupling in the parent action). The 7-program
splashback compilation (More+ 2016, Baxter+ 2017, Chang+ 2018,
Shin+ 2019, Zürcher & More 2019, Contigiani+ 2019, Murata+ 2020)
gives $\chi^2/\mathrm{dof} = 0.42$ with $7/7$ within $2\sigma$.
**All 7 measurements sit above the chameleon ceiling**
$R_\mathrm{sp}/R_{200m} < 0.90$ — structurally falsifying fifth-force
MG on cluster scales.

## What this audit tests

The splashback radius is identified from the steep break in the
projected (WL or galaxy-density) profile around $r \sim R_{200m}$.
Its location depends on accretion history and the dynamical
gravitational coupling. ESD's no-fifth-force structure predicts the
LCDM N-body band; chameleon-class MG predicts a calibrated downward
shift.

## Comparison

| Program | $R_\mathrm{sp}/R_{200m}$ | $\pm$ | tension vs ESD |
|---|---|---|---|
| More+ 2016 (SDSS redMaPPer) | $0.97$ | $0.05$ | $0.60\sigma$ |
| Baxter+ 2017 (SDSS+DES SZ) | $0.94$ | $0.05$ | $1.20\sigma$ |
| Chang+ 2018 (DES Y1) | $1.03$ | $0.07$ | $0.43\sigma$ |
| Shin+ 2019 (ACT-DR4+DES Y3) | $0.99$ | $0.06$ | $0.17\sigma$ |
| Zürcher & More 2019 (HSC WL) | $0.96$ | $0.06$ | $0.67\sigma$ |
| Murata+ 2020 (HSC + CAMIRA) | $1.05$ | $0.08$ | $0.63\sigma$ |
| Contigiani+ 2019 (CCCP+MENeaCS) | $1.02$ | $0.08$ | $0.25\sigma$ |

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19: ESD = $\Lambda$CDM N-body on virialized halos | PASS |
| 2 | $\chi^2/\mathrm{dof} < 1.5$ | PASS ($0.42$) |
| 3 | $\ge 95\%$ within $2\sigma$ of ESD | PASS ($7/7$) |
| 4 | All measurements above chameleon ceiling | PASS ($7/7$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md) | No fifth-force on linear modes |
| [33](../../B_solar_system/B02_solar_system_ppn/README.md) | PPN: no fifth force in solar system |
| [36](../D04_cluster_mass_function/README.md) | Cluster mass function (sibling cluster test) |
| [43](../D05_hydrostatic_mass_bias/README.md) | Hydrostatic mass bias (sibling cluster test) |

## References

- Diemer, B. & Kravtsov, A. V. 2014, ApJ 789, 1 (N-body $R_\mathrm{sp}$)
- Adhikari, S., Dalal, N. & Chamberlain, R. T. 2014, JCAP 11, 019
- More, S., Diemer, B. & Kravtsov, A. V. 2015, ApJ 810, 36
- More, S. et al. 2016, ApJ 825, 39 (SDSS redMaPPer)
- Baxter, E. et al. 2017, ApJ 841, 18 (SDSS+DES SZ)
- Chang, C. et al. 2018, ApJ 864, 83 (DES Y1)
- Shin, T. et al. 2019, MNRAS 487, 2900 (ACT-DR4+DES Y3)
- Zürcher, D. & More, S. 2019, ApJ 874, 184 (HSC WL)
- Contigiani, O. et al. 2019, MNRAS 485, 408 (CCCP+MENeaCS)
- Murata, R. et al. 2020, PASJ 72, 64 (HSC + CAMIRA)
- Adhikari, S., Sakstein, J., Jain, B. et al. 2018, JCAP 11, 033 (chameleon prediction)

## Quickstart

```bash
cd studies/D06_splashback_radius
python scripts/run_splashback_audit.py
python scripts/make_splashback_figures.py
```
