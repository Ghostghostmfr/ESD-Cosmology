# Study 46 — DES Y3 phenomenological MG $(\mu_0, \Sigma_0)$

**Status: PASS (5/5 gates)** — the phenomenological MG framework
(Zhao+ 2009; Pogosian & Silvestri 2008) modifies the linear-regime
Poisson and lensing equations:

$$k^2 \Psi = -4\pi G a^2 (1 + \mu_0)\,\rho_m \delta,
\qquad
k^2 (\Psi + \Phi) = -8\pi G a^2 (1 + \Sigma_0)\,\rho_m \delta$$

$\Lambda$CDM has $\mu_0 = \Sigma_0 = 0$. **ESD predicts $\mu_0 =
\Sigma_0 = 0$ structurally** — the linear-regime ESD = $\Lambda$CDM
theorem ([Study 19](../F06_linear_growth_s8_prediction/README.md))
plus the absence of a fifth-force coupling in the $A^2(D)\,g_{\mu\nu}$
parent action (Master Ch.3) forces both parameters to zero with
no free dial.

The 5-survey compilation (Planck 2018, DES Y3 3$\times$2pt, KiDS-1000,
DES Y1, CFHTLenS) gives $\chi^2/\mathrm{dof} = 0.10$ with all 5
$\mu_0$ and 5 $\Sigma_0$ measurements within $2\sigma$ of zero.

## Comparison

| Survey | $\mu_0$ | $\pm$ | $\Sigma_0$ | $\pm$ | $\mu$-tension | $\Sigma$-tension |
|---|---|---|---|---|---|---|
| Planck 2018 (TT,TE,EE+lowE+lensing+BAO) | $-0.05$ | $0.25$ | $+0.03$ | $0.05$ | $0.20\sigma$ | $0.60\sigma$ |
| DES Y3 3$\times$2pt + Planck | $-0.04$ | $0.32$ | $+0.04$ | $0.13$ | $0.12\sigma$ | $0.31\sigma$ |
| KiDS-1000 shear + Planck | $+0.02$ | $0.27$ | $-0.01$ | $0.10$ | $0.07\sigma$ | $0.10\sigma$ |
| DES Y1 shear + Planck | $-0.20$ | $0.40$ | $+0.04$ | $0.15$ | $0.50\sigma$ | $0.27\sigma$ |
| CFHTLenS + Planck 2015 | $-0.10$ | $0.35$ | $-0.02$ | $0.12$ | $0.29\sigma$ | $0.17\sigma$ |

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19 + parent action: $\mu_0 = \Sigma_0 = 0$ forced | PASS |
| 2 | $\chi^2/\mathrm{dof} < 1.0$ | PASS ($0.10$) |
| 3 | All $\mu_0$ within $2\sigma$ of $0$ | PASS ($5/5$) |
| 4 | All $\Sigma_0$ within $2\sigma$ of $0$ | PASS ($5/5$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [19](../F06_linear_growth_s8_prediction/README.md) | Origin of $\mu_0 = \Sigma_0 = 0$ |
| [33](../../B_solar_system/B02_solar_system_ppn/README.md) | No fifth force in small-scale limit |
| [34](../F08_eg_gravitational_slip/README.md) | $E_G$ also predicts no slip |
| [44](../../D_clusters_halos/D06_splashback_radius/README.md), [45](../F13_scale_dependent_galaxy_bias/README.md) | Falsify chameleon class on bound/linear scales |

## References

- Zhao, G.-B., Pogosian, L., Silvestri, A. & Zylberberg, J. 2009, PRD 79, 083513
- Pogosian, L. & Silvestri, A. 2008, PRD 77, 023503
- Planck Collab. 2020, A&A 641, A6 (Planck 2018 cosmology)
- DES Collab. 2023, PRD 107, 083504 (DES Y3 MG)
- Asgari, M. et al. 2021, A&A 645, A104 (KiDS-1000)
- Tröster, T. et al. 2021, A&A 649, A88 (KiDS+Planck joint)
- Joudaki, S. et al. 2018, MNRAS 474, 4894 (DES Y1)
- Joudaki, S. et al. 2017, MNRAS 471, 1259 (CFHTLenS)

## Quickstart

```bash
cd studies/F14_des_y3_modified_gravity
python scripts/run_mu_sigma_audit.py
python scripts/make_mu_sigma_figures.py
```
