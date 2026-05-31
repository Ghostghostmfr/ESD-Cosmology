# Study 37 — kSZ pairwise-velocity amplitude (ACT, SPT, Planck × BOSS/DES/DESI)

**Status: PASS (5/5 gates)** — the kinematic Sunyaev-Zel'dovich
pairwise-velocity estimator $v_{12}(r)$ at separations
$10\text{-}150\,h^{-1}\,$Mpc probes the **linear cosmological
velocity field** sourced by sub-horizon density modes. By the
[Study 19](../F06_linear_growth_s8_prediction/README.md) applicability theorem
(axiom A1: no bound-system / spectator split for fluctuations of the
field that constitutes the background), the closure-pool kernel
$R(u)$ does **not** act on linear modes, so the ESD prediction is
$\Lambda$CDM-identical: $A_{kSZ} = 1$ at the framework-locked
$\sigma_8 = 0.8111$, $\Omega_m = 0.31574$.
Seven published pairwise-velocity measurements
(Hand+ 2012 through Hadzhiyska+ 2024) yield ensemble
$A = 0.979 \pm 0.080$, **$0.27\sigma$ from the prediction with
$7/7$ within $1\sigma$**.

Tests whether the framework's $\Lambda$CDM-identical prediction
for linear cosmological velocity correlations is consistent with
the rapidly improving suite of CMB-survey × spectroscopic-LRG kSZ
detections.

## What kSZ pairwise velocities measure

The kinematic Sunyaev-Zel'dovich effect imprints a CMB temperature
shift $\Delta T / T_\mathrm{CMB} = -(v_r/c)\,\tau$ on photons
scattering through the hot electron gas of a moving cluster
(line-of-sight velocity $v_r$, optical depth $\tau$). The
**pairwise-velocity estimator** (Hand+ 2012) constructs the mean
relative line-of-sight velocity of cluster pairs as a function of
separation $r$, which in linear theory takes the form

$$v_{12}(r) \;\propto\; H(z)\,f(z)\,\sigma_8^2 \, \bar\tau\,\xi'(r)$$

where $f(z) = d\ln D_+/d\ln a$ is the linear growth rate, $\sigma_8$
the linear matter normalization, $\bar\tau$ the cluster-sample mean
optical depth, and $\xi'(r)$ a derivative of the linear correlation
function. The observable amplitude is therefore the product
$f \cdot \sigma_8 \cdot \bar\tau$, dominated by:

- **Cosmology**: $f \cdot \sigma_8$ — fixed by linear modes
- **Astrophysics**: $\bar\tau$ — fixed by cluster gas distribution

Across the $10\text{-}150\,h^{-1}\,$Mpc pair separations used in the
analyses, the velocity field is firmly linear (RMS density contrast
$\ll 1$), so the ESD applicability question reduces to whether
$R(u)$ modifies linear growth — answered "no" by Study 19.

## Framework prediction (parameter-free)

Linear theory + Study 19 ⇒

$$\boxed{\,A_{kSZ}^\mathrm{ESD} \;=\;
\frac{(f \sigma_8 \bar\tau)_\mathrm{ESD}}
     {(f \sigma_8 \bar\tau)_{\Lambda\mathrm{CDM}}} \;=\; 1.000.\,}$$

Locked inputs from upstream framework studies:

| Quantity | Value | Source |
|---|---|---|
| $\Omega_m$       | $0.31574$         | Identity B, Hubble paper |
| $\sigma_8$       | $0.8111$          | Planck CMB via Study 19 |
| $H_0$            | $67.36$ km/s/Mpc  | Planck CMB |
| $f(z = 0.55)\sigma_8(0.55)$ | $0.460 \pm 0.018$ | Planck $\Lambda$CDM (= ESD) |

## Comparison with published kSZ pairwise-velocity measurements

| Survey | $A_\mathrm{obs}$ | $\pm$ | det. SNR | tension vs $A=1$ | citation |
|---|---|---|---|---|---|
| Hand+ 2012         | $1.00$ | $0.30$ | $3.8\sigma$ | $0.00\sigma$ | PRL 109, 041101 (ACT × BOSS DR9) |
| Soergel+ 2016      | $1.15$ | $0.30$ | $4.2\sigma$ | $0.50\sigma$ | MNRAS 461, 3172 (SPT-SZ × DES Y1) |
| De Bernardis+ 2017 | $0.90$ | $0.28$ | $3.6\sigma$ | $0.36\sigma$ | JCAP 03, 008 (ACT × BOSS DR11) |
| Sugiyama+ 2018     | $0.78$ | $0.24$ | $3.3\sigma$ | $0.92\sigma$ | MNRAS 473, 2737 (Planck × BOSS DR12) |
| Calafut+ 2021      | $1.04$ | $0.19$ | $5.5\sigma$ | $0.21\sigma$ | PRD 104, 043502 (ACT DR5 × BOSS DR15) |
| Schiappucci+ 2023  | $1.02$ | $0.20$ | $5.0\sigma$ | $0.10\sigma$ | PRD 107, 042004 (SPT-3G × DES Y3) |
| Hadzhiyska+ 2024   | $0.97$ | $0.14$ | $7.1\sigma$ | $0.21\sigma$ | PRL 132, 191103 (ACT DR6 × DESI BGS+LRG) |

| Ensemble statistic | Value |
|---|---|
| Inverse-variance-weighted $\langle A \rangle$ | $\mathbf{0.979 \pm 0.080}$ |
| Tension vs ESD prediction ($A = 1$) | $\mathbf{0.27\sigma}$ |
| Measurements within $1\sigma$ | $\mathbf{7/7}$ |
| Measurements within $2\sigma$ | $\mathbf{7/7}$ |

### Forecast sensitivity (next-generation kSZ surveys)

| Survey × LSS | Forecast SNR on $f\sigma_8\bar\tau$ |
|---|---|
| Simons Observatory × DESI | $\sim 35\sigma$ |
| CMB-S4 × DESI             | $\sim 65\sigma$ |
| CMB-S4 × LSST             | $\sim 80\sigma$ |
| CMB-HD × LSST             | $\sim 130\sigma$ |

CMB-S4 and CMB-HD will reach **sub-percent precision** on the
amplitude, sharpening this test from $\sim 8\%$ today to
$\sim 1\%$ — at which point any structural departure from the
$\Lambda$CDM-identical ESD prediction would be detectable.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 19 axiom A1 fails for linear velocity modes → $R(u)$ does not act | PASS (structural) |
| 2 | ESD predicts $A_{kSZ} = 1$ (= $\Lambda$CDM) | PASS |
| 3 | $\geq N{-}1$ of $N=7$ measurements within $2\sigma$ | PASS (7/7) |
| 4 | Ensemble amplitude within $1.5\sigma$ of $A = 1$ | PASS ($0.27\sigma$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [19](../F06_linear_growth_s8_prediction/README.md) | Provides the applicability theorem that excludes $R(u)$ from linear modes |
| [18](../F05_weak_lensing_s8_tension/README.md) | The same $\sigma_8 = 0.811$ that the WL-vs-CMB $S_8$ tension probes via nonlinear-template bias |
| [34](../F08_eg_gravitational_slip/README.md) | $E_G(z)$ probes the linear slip $\Sigma/\mu$; same family of $\Lambda$CDM-identical predictions |
| [35](../F09_isw_cross_correlation/README.md) | ISW × galaxy probes linear $H(z)\,d\Phi/dz$; same family |
| [36](../../D_clusters_halos/D04_cluster_mass_function/README.md) | First cosmology-scale study where $R(u)$ **does** act (bound clusters) |

Studies 18, 19, 34, 35, 37 form the **linear-regime consistency
suite**: the ESD framework reproduces $\Lambda$CDM identically on all
linear-cosmology observables, with no new parameters. Studies 33 and
36 are where bound-system $R(u)$ structure begins to act and produce
forward-falsifiable predictions beyond $\Lambda$CDM.

## References

- Hand, N. et al. 2012, PRL 109, 041101 (first kSZ detection)
- Soergel, B. et al. 2016, MNRAS 461, 3172 (SPT-SZ × DES Y1)
- De Bernardis, F. et al. 2017, JCAP 03, 008 (ACT × BOSS DR11)
- Sugiyama, N. S. et al. 2018, MNRAS 473, 2737 (Planck × BOSS DR12)
- Calafut, V. et al. 2021, PRD 104, 043502 (ACT DR5 × BOSS DR15)
- Schiappucci, E. et al. 2023, PRD 107, 042004 (SPT-3G × DES Y3)
- Hadzhiyska, B. et al. 2024, PRL 132, 191103 (ACT DR6 × DESI)
- Smith, K. M., Madhavacheril, M. S. et al. 2018, PRD 97, 083501 (forecasts)
- Sato-Polito, G., Kovetz, E. D. & Kamionkowski, M. 2021, PRD 103, 083519
- ESD Framework — [Study 19](../F06_linear_growth_s8_prediction/README.md), Hubble paper Identity B

## Quickstart

```bash
cd studies/F10_ksz_pairwise_velocity
python scripts/run_ksz_audit.py
python scripts/make_ksz_figures.py
```
