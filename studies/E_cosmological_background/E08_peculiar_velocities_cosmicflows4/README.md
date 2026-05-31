# Study 47 — Cosmicflows-4 peculiar-velocity $f\sigma_8(z{\approx}0)$

**Status: PASS (5/5 gates)** — the local ($z \lesssim 0.05$)
peculiar-velocity field probes the linear growth amplitude
$f\sigma_8$ directly via the continuity equation
$\nabla \cdot \mathbf{v}_p / aH = -f \delta_m$.

ESD inherits $\Lambda$CDM linear growth ([Study 19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md))
with locked $\Omega_m = 0.31574$, $\sigma_8 = 0.8111$, and Linder
exponent $\gamma = 0.55$, giving

$$f\sigma_8(z=0) = \Omega_m^{0.55} \sigma_8 = 0.31574^{0.55} \times 0.8111 = 0.4302.$$

The 8-program peculiar-velocity compilation (6dFGSv, 2MTF, SDSS PV,
SFI++/A2, 2M++, Cosmicflows-3/4) gives $\chi^2/\mathrm{dof} = 0.35$
with $8/8$ within $1\sigma$ — fully consistent.

## Comparison

| Program | $f\sigma_8(z{\approx}0)$ | $\pm$ | tension |
|---|---|---|---|
| 6dFGSv (Huterer+ 2017) | $0.428$ | $0.066$ | $0.03\sigma$ |
| 6dFGSv (Adams & Blake 2020) | $0.384$ | $0.052$ | $0.89\sigma$ |
| 2MTF (Howlett+ 2017) | $0.505$ | $0.085$ | $0.88\sigma$ |
| SDSS PV (Howlett+ 2017) | $0.452$ | $0.077$ | $0.28\sigma$ |
| SFI++/A2 (Boruah+ 2020) | $0.400$ | $0.040$ | $0.76\sigma$ |
| 2M++ (Lilow & Nusser 2021) | $0.421$ | $0.038$ | $0.24\sigma$ |
| Cosmicflows-3 (Said+ 2020) | $0.460$ | $0.060$ | $0.50\sigma$ |
| Cosmicflows-4 (Said+ 2024) | $0.413$ | $0.034$ | $0.51\sigma$ |

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19: ESD = $\Lambda$CDM linear growth | PASS |
| 2 | $\ge 95\%$ within $2\sigma$ | PASS ($8/8$) |
| 3 | $\chi^2/\mathrm{dof} < 1.5$ | PASS ($0.35$) |
| 4 | $\ge 50\%$ within $1\sigma$ | PASS ($8/8$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md) | Owns $\sigma_8$ tension family |
| [19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md) | Linear-regime applicability theorem |
| [24](../../F_cmb_lss/F07_act_dr6_cmb_lensing/README.md) | ACT lensing $S_8$ confirmation |
| [37](../../F_cmb_lss/F10_ksz_pairwise_velocity/README.md) | kSZ pairwise-velocity sibling |
| [39](../../F_cmb_lss/F12_rsd_growth_rate/README.md) | RSD $f\sigma_8(z)$ compilation |

## References

- Tully, R. B. et al. 2023, ApJ 944, 94 (Cosmicflows-4)
- Said, K. et al. 2024, MNRAS (Cosmicflows-4 $f\sigma_8$)
- Said, K. et al. 2020, MNRAS 497, 1275 (Cosmicflows-3 $f\sigma_8$)
- Boruah, S. S., Hudson, M. J. & Lavaux, G. 2020, MNRAS 498, 2703
- Lilow, R. & Nusser, A. 2021, MNRAS 507, 1557 (2M++)
- Howlett, C. et al. 2017, MNRAS 471, 3135 (2MTF, SDSS PV)
- Huterer, D., Shafer, D. L., Scolnic, D. M. & Schmidt, F. 2017, JCAP 05, 015 (6dFGSv)
- Adams, C. & Blake, C. 2020, MNRAS 494, 3275 (6dFGSv revised)

## Quickstart

```bash
cd studies/E08_peculiar_velocities_cosmicflows4
python scripts/run_pv_audit.py
python scripts/make_pv_figures.py
```
