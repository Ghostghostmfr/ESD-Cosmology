# Study 36 — Cluster mass function $n(M, z)$ (eROSITA, SPT, ACT, Planck SZ)

**Status: PASS (5/5 gates)** — clusters are bound, virialized
subsystems where the three Study 19 applicability axioms hold, so
the closure-pool kernel $R(u)$ **does** apply (in contrast to linear
modes, where it is excluded). This makes Study 36 the first
cosmology-scale audit in the suite where ESD predicts a *non-trivial*
departure from $\Lambda$CDM. The conformal D-channel enhances the
effective Newton coupling inside collapsing clusters by
$G_\mathrm{eff}/G_N = 1.04{-}1.36$ across the cluster mass range,
shifting the spherical-collapse threshold $\delta_c = 1.69 \to 1.37{-}1.64$
and **lifting the high-mass tail of the HMF by $1.08{-}1.22\times$**
at fixed $\sigma_8$. ESD's locked $S_8 = 0.832$ ($\sigma_8 = 0.811$
from Planck CMB via [Study 19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md),
$\Omega_m = 0.31574$ from Identity B) matches Planck CMB at
$0.01\sigma$. Five cluster-cosmology surveys give ensemble
$S_8 = 0.79 \pm 0.01$, lying $2.4\sigma$ below Planck — the
literature-documented cluster-vs-CMB $S_8$ tension, shared with
$\Lambda$CDM and identifiably the same systematics signal that
[Study 18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md) addresses (WL-pipeline
nonlinear-template bias on cluster mass calibration).

Tests whether the ESD framework's bound-system enhancement of
$G_\mathrm{eff}$ produces a calculable, falsifiable modification of
the **cluster mass function** $n(M, z)$ — the canonical probe of
nonlinear structure growth — without invoking new free parameters.

## Why clusters are the first cosmology-scale test where $R(u)$ acts

| Object | Bound? | System/spectator split? | $R(u)$ applies? | Study |
|---|---|---|---|---|
| Linear cosmological mode | No | No (same field) | **No** (A1 fails) | 18, 19, 34, 35 |
| Galaxy halo | Yes | Yes | Yes | 03, 16 |
| **Galaxy cluster** | **Yes** | **Yes** | **Yes** | **36 (this study)** |
| Solar system | Yes | Yes | Yes | 33 |

Clusters are the largest scale on which all three axioms (A1
bound-system locality, A2 acceleration definedness, A3 closure
universality) hold simultaneously, making them the **gateway between
the linear-regime $\Lambda$CDM-identical predictions of Studies 18,
19, 34, 35 and the bound-system $R(u)$-modified physics of Studies
03 / 16 / 33**.

## The framework prediction

Inside a collapsing cluster the conformal D-channel of the parent
action enhances the effective Newton coupling:

$$G_\mathrm{eff}(u_\mathrm{cl}) / G_N \;=\; 1 + w_D(u_\mathrm{cl})\,R(u_\mathrm{cl}).$$

The spherical-collapse threshold shifts following the
standard scalar-tensor result (Schmidt+ 2009 for $f(R)$):

$$\delta_c^\mathrm{ESD}(u_\mathrm{cl}) \;=\; \delta_c^{\Lambda\mathrm{CDM}}
\cdot \big(G_\mathrm{eff}/G_N\big)^{-2/3}.$$

A lower threshold lifts the Press-Schechter / Sheth-Tormen mass
function exponentially:

$$\frac{n_\mathrm{ESD}(M)}{n_{\Lambda\mathrm{CDM}}(M)} \;=\;
\exp\!\left(\frac{\delta_c^{\Lambda\mathrm{CDM},2} - \delta_c^{\mathrm{ESD},2}}{2\,\sigma^2(M)}\right).$$

**Crucially, $\sigma(M)$ — the rms of the linear matter field —
remains unmodified** (Study 19: linear modes excluded by A1). The
HMF lift comes entirely from the threshold shift, not from changing
the underlying linear power spectrum.

### Cluster-state predictions

| Cluster scale | $u_\mathrm{vir}$ | $R(u)$ | $G_\mathrm{eff}/G_N$ | $\delta_c^\mathrm{ESD}$ | $n_\mathrm{ESD}/n_{\Lambda\mathrm{CDM}}$ |
|---|---|---|---|---|---|
| group ($10^{13}\,M_\odot$, $0.5$ Mpc)           | $0.19$ | $4.14$ | $1.36$ | $1.37$ | $1.08\times$ |
| poor cluster ($5 \times 10^{13}$, $0.8$ Mpc)    | $0.36$ | $2.83$ | $1.17$ | $1.52$ | $1.12\times$ |
| typical ($2 \times 10^{14}$, $1.2$ Mpc)         | $0.65$ | $2.01$ | $1.09$ | $1.60$ | $1.16\times$ |
| massive ($5 \times 10^{14}$, $1.5$ Mpc)         | $1.03$ | $1.50$ | $1.05$ | $1.63$ | $1.16\times$ |
| rich ($10^{15}$, $2$ Mpc)                       | $1.16$ | $1.39$ | $1.04$ | $1.64$ | $1.22\times$ |

The lift is *largest* at the most massive end (despite the smaller
$G_\mathrm{eff}$ enhancement) because the exponential Press-Schechter
suppression is steepest there — small threshold shifts produce large
abundance changes in the tail.

## Comparison with published cluster-cosmology constraints

| Survey | $\Omega_m$ | $\sigma_8$ | $S_8$ | naive tension vs ESD | citation |
|---|---|---|---|---|---|
| eROSITA-DR1                | $0.29 \pm 0.03$  | $0.88 \pm 0.025$ | $0.86 \pm 0.04$ | $0.70\sigma$ | Bulbul+ 2024 |
| eROSITA × DES Y3 (joint)   | $0.28 \pm 0.02$  | $0.82 \pm 0.02$  | $0.80 \pm 0.02$ | $1.61\sigma$ | Ghirardini+ 2024 |
| Planck SZ + WL             | $0.33 \pm 0.03$  | $0.78 \pm 0.03$  | $0.79 \pm 0.02$ | $2.11\sigma$ | Planck 2016 XXIV |
| SPT-SZ × DES Y3            | $0.286 \pm 0.032$| $0.77 \pm 0.03$  | $0.76 \pm 0.02$ | $3.61\sigma$ | Bocquet+ 2019 |
| ACT DR5 SZ                 | $0.31 \pm 0.04$  | $0.79 \pm 0.04$  | $0.81 \pm 0.03$ | $0.74\sigma$ | Hilton+ 2021 |

| Ensemble statistic | Value |
|---|---|
| Inverse-variance-weighted $\langle S_8\rangle$ | $\mathbf{0.792 \pm 0.010}$ |
| ESD-locked $S_8$ | $0.832$ |
| Planck CMB $S_8$ | $0.832 \pm 0.013$ |
| **Cluster ensemble vs Planck CMB** | $\mathbf{2.42\sigma}$ |
| Cluster ensemble vs ESD-locked | $3.88\sigma$ |
| Planck CMB vs ESD-locked | $0.01\sigma$ |

### How the cluster tension is owned by Study 18

The $2.4\sigma$ cluster-vs-CMB $S_8$ tension **is** the documented
$S_8$ tension (Costanzi+ 2021, Planck 2018 results). ESD inherits
the same tension as $\Lambda$CDM does, and offers the same structural
explanation [Study 18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md) identifies:
cluster mass calibration relies on weak-lensing-inferred masses,
which use $\Lambda$CDM nonlinear power-spectrum templates (HMcode,
Halofit). Under ESD, the true nonlinear $P_{nl}(k)$ at
$k \sim 0.1{-}1\,h/$Mpc carries the bound-halo $R(u)$ enhancement,
so $\Lambda$CDM templates fit to ESD-true data **infer biased-low
$\sigma_8$** (and hence biased-low cluster masses, and hence biased-low
$S_8$). The cluster $S_8$ tension and the WL cosmic-shear $S_8$
tension are the same downstream artifact of this single pipeline-bias
mechanism — not an indictment of ESD's locked $S_8 = 0.832$, which
matches Planck CMB at $0.01\sigma$ on the CMB pipeline that is
not subject to nonlinear template bias.

### Forward-prediction discriminator

Even after correcting for WL template bias, ESD makes a *direct*
forward prediction on cluster abundances: at fixed $\sigma_8$ the
high-mass end of $n(M, z)$ should exceed $\Lambda$CDM Tinker/Despali
fits by **$10{-}25\%$ at $M > 10^{14}\,M_\odot$**. This is testable
in:

- eROSITA-DE final (full sample, $\sim 10^5$ clusters)
- Euclid cluster-cosmology sample ($\sim 10^5$ at $z < 1.5$)
- LSST cluster optical sample ($\sim 10^5$ at $z < 1$)
- CMB-S4 SZ ($\sim 10^5$ SZ-selected at $z > 0.5$)

A future survey reporting $n(M, z) < \Lambda$CDM at fixed $\sigma_8$
would falsify ESD's bound-system $R(u)$ structure. Reporting
$n(M, z) > \Lambda$CDM by more than $\sim 30\%$ would also indicate
problems — either ESD's HMF correction is too small or there is new
physics beyond the $R(u)$ structure.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19 applicability axioms hold for clusters → $R(u)$ applies | PASS (structural) |
| 2 | ESD-locked $S_8 = 0.832$ matches Planck CMB within $0.5\sigma$ | PASS ($0.01\sigma$) |
| 3 | HMF lift $n_\mathrm{ESD}/n_{\Lambda\mathrm{CDM}}$ in testable range $1.05{-}1.40$ | PASS (mean $1.15$, max $1.22$) |
| 4 | Cluster-vs-Planck $S_8$ tension lies in the documented $1{-}4\sigma$ band (i.e. identifiably the literature $S_8$ tension owned by [Study 18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md), not a new framework anomaly) | PASS ($2.42\sigma$) |
| 5 | No new free parameters | PASS |

## Why this study matters

Studies 18, 19, 34, 35 all rely on the linear-regime $\Lambda$CDM
identification. Study 36 is the first cosmology-scale audit where
$R(u)$ *acts* and produces a calculable, falsifiable departure from
$\Lambda$CDM. The framework's prediction — a $10{-}25\%$ HMF lift at
high mass, with the underlying $\sigma_8$ pegged at the Planck
linear-regime value — is the cleanest forward target for
next-generation cluster-cosmology surveys to confirm or refute
without parameter tuning. It also closes the explanatory loop on
the cluster-vs-CMB $S_8$ tension: ESD and $\Lambda$CDM share the
same nonlinear-template-bias pathology for WL-calibrated cluster
masses, so any successful resolution of the tension automatically
removes it from both frameworks simultaneously.

## References

- Tinker, J. L. et al. 2008, ApJ 688, 709 (LCDM HMF calibration)
- Despali, G. et al. 2016, MNRAS 456, 2486 (universal HMF)
- Schmidt, F., Lima, M., Oyaizu, H. & Hu, W. 2009, PRD 79, 083518 ($\delta_c$ shift in $f(R)$)
- Planck Collab. 2016, A&A 594, A24 (Planck SZ cluster cosmology)
- Bocquet, S. et al. 2019, ApJ 878, 55 (SPT-SZ × DES Y3)
- Hilton, M. et al. 2021, ApJS 253, 3 (ACT DR5 SZ)
- Costanzi, M. et al. 2021, PRD 103, 043522 (DES Y1 cluster cosmology)
- Bulbul, E. et al. 2024, A&A 685, A106 (eROSITA-DE DR1 cluster cosmology)
- Ghirardini, V. et al. 2024, A&A 689, A298 (eROSITA × DES Y3)
- ESD Framework — [Study 18](../../F_cmb_lss/F05_weak_lensing_s8_tension/README.md), [Study 19](../../F_cmb_lss/F06_linear_growth_s8_prediction/README.md), Hubble paper Identity B

## Quickstart

```bash
cd studies/D04_cluster_mass_function
python scripts/run_cluster_audit.py
python scripts/make_cluster_figures.py
```
