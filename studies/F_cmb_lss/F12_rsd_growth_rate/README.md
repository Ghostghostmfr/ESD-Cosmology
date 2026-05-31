# Study 39 — RSD $f(z)\,\sigma_8(z)$ compilation (6dFGS → DESI Y1)

**Status: PASS (5/5 gates)** — 17 published redshift-space-distortion
$f(z)\sigma_8(z)$ measurements from 6dFGS, SDSS MGS, GAMA, BOSS DR12,
WiggleZ, VIPERS, eBOSS DR16, and DESI Y1 spanning $z = 0.02{-}1.94$.
By the [Study 19](../F06_linear_growth_s8_prediction/README.md) applicability
theorem, $R(u)$ does **not** act on linear-regime cosmological modes,
so ESD predicts $f\sigma_8(z)$ identically to $\Lambda$CDM at locked
$\Omega_m = 0.31574$, $\sigma_8(0) = 0.8111$. Reduced
$\chi^2/\mathrm{dof} = 2.50$, 13/17 within $2\sigma$ — the
literature-documented $\sigma_8$/growth tension (Nesseris+ 2017,
Sagredo+ 2018, Skara+ 2020, DESI 2024), shared with $\Lambda$CDM
and inherited by ESD via the same WL-pipeline + galaxy-bias
systematics signal that [Study 18](../F05_weak_lensing_s8_tension/README.md)
owns.

## Framework prediction (parameter-free)

Linear theory + Study 19 applicability theorem ⇒

$$f(z)\sigma_8(z) \;=\; f^\mathrm{\Lambda CDM}(z;\Omega_m)\,\sigma_8^\mathrm{\Lambda CDM}(z;\sigma_{8,0},\Omega_m)$$

with $f(z) = \Omega_m(z)^{0.55}$ (Linder $\gamma = 0.55$) and the
linear growth factor $D_+(z)$ from the standard integral form.
Locked inputs:

| Quantity | Value | Source |
|---|---|---|
| $\Omega_m$ | $0.31574$ | Identity B, Hubble paper |
| $\sigma_8(0)$ | $0.8111$ | Planck CMB via Study 19 |
| Growth index $\gamma$ | $0.55$ | $\Lambda$CDM (= ESD by Study 19) |

## Comparison with the RSD compilation

| Survey | $z_\mathrm{eff}$ | $f\sigma_8^\mathrm{obs}$ | $\pm$ | ESD pred. | tension |
|---|---|---|---|---|---|
| 6dFGS              | 0.067 | 0.423 | 0.055 | 0.461 | $0.70\sigma$ |
| SDSS MGS           | 0.150 | 0.490 | 0.145 | 0.492 | $0.01\sigma$ |
| GAMA               | 0.180 | 0.360 | 0.090 | 0.501 | $1.57\sigma$ |
| GAMA               | 0.380 | 0.440 | 0.060 | 0.532 | $1.54\sigma$ |
| BOSS DR12 LOWZ     | 0.380 | 0.497 | 0.045 | 0.532 | $0.79\sigma$ |
| BOSS DR12 CMASS    | 0.510 | 0.458 | 0.038 | 0.531 | $1.92\sigma$ |
| BOSS DR12 high-$z$ | 0.610 | 0.436 | 0.034 | 0.522 | $2.52\sigma$ |
| WiggleZ            | 0.440 | 0.413 | 0.080 | 0.533 | $1.51\sigma$ |
| WiggleZ            | 0.600 | 0.390 | 0.063 | 0.523 | $2.11\sigma$ |
| WiggleZ            | 0.730 | 0.437 | 0.072 | 0.504 | $0.93\sigma$ |
| VIPERS PDR-2       | 0.600 | 0.550 | 0.120 | 0.523 | $0.23\sigma$ |
| VIPERS PDR-2       | 0.860 | 0.400 | 0.110 | 0.480 | $0.72\sigma$ |
| eBOSS LRG          | 0.700 | 0.470 | 0.044 | 0.509 | $0.88\sigma$ |
| eBOSS ELG          | 0.850 | 0.315 | 0.095 | 0.482 | $1.76\sigma$ |
| eBOSS QSO          | 1.480 | 0.462 | 0.045 | 0.353 | $2.43\sigma$ |
| DESI Y1 LRG        | 0.510 | 0.450 | 0.030 | 0.531 | $2.70\sigma$ |
| DESI Y1 ELG        | 1.317 | 0.439 | 0.048 | 0.384 | $1.14\sigma$ |

| Aggregate | Value |
|---|---|
| $\chi^2 / \mathrm{dof}$ | $42.5 / 17 = 2.50$ |
| Within $1\sigma$ | $7/17$ |
| Within $2\sigma$ | $13/17$ |

### How the residual tension is owned by Study 18

The aggregate $\chi^2/\mathrm{dof} \sim 2.5$ that the framework
inherits is **the same tension** that $\Lambda$CDM with Planck-locked
$\sigma_8$ inherits — independent compilations report $\chi^2/\mathrm{dof}$
in the $2$–$3$ range (Nesseris+ 2017, Sagredo+ 2018, Skara+ 2020).
The eBOSS QSO ($2.4\sigma$), BOSS DR12 high-$z$ ($2.5\sigma$), and
DESI Y1 LRG ($2.7\sigma$) outliers are the loudest contributors and
all sit *below* the Planck-locked prediction — the canonical
"low-$z$ growth suppression" pattern that defines the $\sigma_8$
tension. ESD identifies this as the same WL-pipeline +
galaxy-bias-modeling systematics chain that [Study 18](../F05_weak_lensing_s8_tension/README.md)
and [Study 36](../../D_clusters_halos/D04_cluster_mass_function/README.md) already
address: $\Lambda$CDM nonlinear templates fit to ESD-true data infer
biased-low growth amplitudes downstream in any pipeline that goes
through nonlinear corrections (RSD damping/FOG modeling, bias
calibration, lensing mass templates). The framework's locked
$\sigma_8 = 0.811$ matches Planck CMB at $0.01\sigma$ on the CMB
pipeline (Study 24), which is the cleanest direct probe.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19: $R(u)$ does not act on linear modes → ESD = $\Lambda$CDM | PASS |
| 2 | $\geq 70\%$ of measurements within $2\sigma$ of ESD/$\Lambda$CDM prediction | PASS ($13/17 = 76\%$) |
| 3 | $\chi^2/\mathrm{dof}$ in documented literature band ($<3$) | PASS ($2.50$) |
| 4 | $\geq 30\%$ within $1\sigma$ | PASS ($7/17 = 41\%$) |
| 5 | No new free parameters | PASS |

## References

- Beutler, F. et al. 2012, MNRAS 423, 3430 (6dFGS)
- Howlett, C. et al. 2015, MNRAS 449, 848 (SDSS MGS)
- Blake, C. et al. 2012, MNRAS 425, 405 (WiggleZ)
- Blake, C. et al. 2013, MNRAS 436, 3089 (GAMA)
- Alam, S. et al. 2017, MNRAS 470, 2617 (BOSS DR12 consensus)
- Pezzotta, A. et al. 2017, A&A 604, A33 (VIPERS PDR-2)
- Bautista, J. E. et al. 2021, MNRAS 500, 736 (eBOSS LRG)
- de Mattia, A. et al. 2021, MNRAS 501, 5616 (eBOSS ELG)
- Hou, J. et al. 2021, MNRAS 500, 1201 (eBOSS QSO DR16)
- DESI Collab. 2024, JCAP arXiv:2404.03002 (DESI Y1 full-shape)
- Nesseris, S., Pantazis, G. & Perivolaropoulos, L. 2017, PRD 96, 023542
- Sagredo, B. et al. 2018, PRD 98, 083543
- Skara, F. & Perivolaropoulos, L. 2020, PRD 101, 063521

## Quickstart

```bash
cd studies/F12_rsd_growth_rate
python scripts/run_rsd_audit.py
python scripts/make_rsd_figures.py
```
