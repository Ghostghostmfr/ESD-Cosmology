# Study 45 — Scale-dependent linear galaxy bias $b(k)$

**Status: PASS (5/5 gates)** — ESD predicts **strictly constant**
linear galaxy bias $b$ across the large-scale linear regime, as a
direct corollary of the [Study 19](../F06_linear_growth_s8_prediction/README.md)
applicability theorem: $R(u)$ does not act on linear cosmological
modes, and the parent action's $A^2(D) g_{\mu\nu}$ (Master Ch.3)
is conformal — it cannot generate $k$-dependent linear growth.

In contrast, $f(R)$, chameleon, DGP, and other MG classes generate
a measurable few-percent $k$-dependence in $b(k)$ at $k \sim
0.1\,h\,$Mpc$^{-1}$ (Pollina+ 2018; Aviles+ 2019; Valogiannis+
2020). The 7-program survey compilation (BOSS DR12 LOWZ/CMASS,
eBOSS LRG/ELG/QSO, DESI DR1 LRG/ELG) gives $\chi^2/\mathrm{dof}
= 0.48$ with $7/7$ measurements within $1\sigma$ of the constant-$b$
prediction.

## What this audit tests

Linear galaxy bias is defined by $\delta_g(k) = b(k)\delta_m(k)$
in the linear regime. ESD's $\sigma_8$, $f(z)$, and matter power
spectrum equal $\Lambda$CDM in this regime, so $b$ is $k$-independent
by construction. The audit tests the measured deviations
$\max_k |b(k_i) - \langle b\rangle|/\langle b\rangle$ across the
fitted linear range.

## Comparison

| Program | deviation | $\pm$ | $k$-range ($h$/Mpc) | tension |
|---|---|---|---|---|
| BOSS DR12 LOWZ (Beutler+ 2017) | $0.018$ | $0.025$ | $0.01\text{-}0.15$ | $0.72\sigma$ |
| BOSS DR12 CMASS (Beutler+ 2017) | $0.015$ | $0.020$ | $0.01\text{-}0.15$ | $0.75\sigma$ |
| eBOSS LRG (Bautista+ 2021) | $0.020$ | $0.030$ | $0.01\text{-}0.15$ | $0.67\sigma$ |
| eBOSS ELG (de Mattia+ 2021) | $0.025$ | $0.040$ | $0.01\text{-}0.15$ | $0.62\sigma$ |
| eBOSS QSO (Neveux+ 2020) | $0.030$ | $0.045$ | $0.01\text{-}0.15$ | $0.67\sigma$ |
| DESI DR1 LRG (DESI 2024) | $0.012$ | $0.018$ | $0.02\text{-}0.20$ | $0.67\sigma$ |
| DESI DR1 ELG (DESI 2024) | $0.022$ | $0.030$ | $0.02\text{-}0.20$ | $0.73\sigma$ |

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19 corollary: ESD predicts $db/d\ln k = 0$ | PASS |
| 2 | $\chi^2/\mathrm{dof} < 1.5$ | PASS ($0.48$) |
| 3 | $100\%$ within $2\sigma$ of constant | PASS ($7/7$) |
| 4 | $\ge 70\%$ within $1\sigma$ of constant | PASS ($7/7$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [19](../F06_linear_growth_s8_prediction/README.md) | Applicability theorem (origin of corollary) |
| [24](../F07_act_dr6_cmb_lensing/README.md) | $\sigma_8$ lock for $b\sigma_8$ measurements |
| [33](../../B_solar_system/B02_solar_system_ppn/README.md) | No fifth force in small-scale limit |
| [44](../../D_clusters_halos/D06_splashback_radius/README.md) | Falsifies chameleon at cluster scale |

## References

- Beutler, F. et al. 2017, MNRAS 466, 2242 (BOSS DR12)
- Bautista, J. E. et al. 2021, MNRAS 500, 736 (eBOSS LRG)
- de Mattia, A. et al. 2021, MNRAS 501, 5616 (eBOSS ELG)
- Neveux, R. et al. 2020, MNRAS 499, 210 (eBOSS QSO)
- DESI Collab. 2024, arXiv:2404.03002 (DESI DR1)
- Pollina, G. et al. 2018, MNRAS 487, 3217 (MG bias prediction)
- Aviles, A. et al. 2019, JCAP 2019, 049
- Valogiannis, G. et al. 2020, PRD 101, 123525

## Quickstart

```bash
cd studies/F13_scale_dependent_galaxy_bias
python scripts/run_bias_k_audit.py
python scripts/make_bias_k_figures.py
```
