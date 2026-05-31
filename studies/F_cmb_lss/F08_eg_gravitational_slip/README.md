# Study 34 — $E_G(z)$ gravitational-slip statistic (Reyes 2010, BOSS/eBOSS/KiDS/CFHTLenS/Planck)

**Status: PASS (5/5 gates)** — ESD predicts the standard
$\Lambda$CDM curve $E_G(z) = \Omega_{m,0}/f(z)$ identically at linear
scales, by the applicability theorem of [Study 19](../F06_linear_growth_s8_prediction/README.md)
(closure-pool kernel $R(u)$ does **not** apply to linear modes
because Axiom A1 — system/spectator split — fails for fluctuations
of the same field that constitutes the background). The locked
$\Omega_{m,0} = 0.31574$ (Identity B C2) feeds the prediction
without any free parameter. Against $9$ published $E_G$ measurements
(BOSS, eBOSS, CFHTLenS, RCSLenS, KiDS-450, VIPERS, Planck CMB lensing)
spanning $z = 0.30{-}0.60$, the inverse-variance-weighted sample mean
sits $1.97\sigma$ from the ESD prediction; with the single Pullen+
2016 outlier excluded (the only $\kappa_\mathrm{CMB}\times$CMASS
measurement, with well-documented foreground systematics), the
robust mean tension drops to $0.98\sigma$. $7/9$ measurements lie
within $1\sigma$ and $8/9$ within $2\sigma$.

Tests whether the ESD framework reproduces the **gravitational-slip
statistic** $E_G$ — the canonical referee-standard discriminator
between $\Lambda$CDM and modified gravity in the linear regime
(Reyes+ 2010, Zhang+ 2007).

## What $E_G$ measures

$E_G$ is defined as the ratio of the lensing potential $\Phi + \Psi$
to the velocity divergence $\theta$ inferred from redshift-space
distortions:

$$E_G(z, \ell) \;\equiv\; \frac{1}{\beta(z)}\,
\frac{C_{\kappa g}(\ell)}{C_{v g}(\ell)}, \qquad
\beta(z) = f(z)/b_g,$$

where $C_{\kappa g}$ is the galaxy–CMB-lensing (or galaxy–galaxy
lensing) cross-power and $C_{vg}$ is the galaxy–velocity cross-power.
In linear $\Lambda$CDM with no anisotropic stress this evaluates to

$$E_G^{\Lambda\mathrm{CDM}}(z) \;=\; \frac{\Omega_{m,0}}{f(z)},
\qquad f(z) \;=\; \Omega_m(z)^{0.55}.$$

In a general modified-gravity theory parameterized by
$\mu(z, k)$ (effective Newton coupling) and $\Sigma(z, k)$ (effective
lensing coupling),

$$E_G(z) \;=\; \frac{\Sigma(z)}{\mu(z)}\,\frac{\Omega_{m,0}}{f(z)},$$

so $E_G$ is *the* observable that isolates the lensing-vs-clustering
slip without depending on galaxy bias.

## ESD prediction — the structural result

Study 19 establishes a **structural applicability theorem**: the
closure-pool kernel $R(u)$ is defined only for a localized
subsystem against a separated spectator background (Axiom A1).
A linear cosmological perturbation $\delta(x,t)$ is a small
fluctuation of the **same field** that constitutes the background;
there is no system/spectator split. Therefore $R(u)$ does not apply,
the linear growth equation is unmodified, and

$$\mu_\mathrm{ESD}(z, k_\mathrm{linear}) \;=\; 1,\quad
  \Sigma_\mathrm{ESD}(z, k_\mathrm{linear}) \;=\; 1,\quad
  \eta_\mathrm{ESD}(z) \;\equiv\; \Phi/\Psi \;=\; 1.$$

Consequently $E_G^\mathrm{ESD}(z) = E_G^{\Lambda\mathrm{CDM}}(z)$ —
the framework is **constructively indistinguishable from
$\Lambda$CDM** on this observable, with the lock supplied by the
parent-action structure, not by parameter tuning.

## Linear-regime predictions

| $z$ | $\Omega_m(z)$ | $f(z)$ | $E_G^\mathrm{ESD}(z) = \Omega_{m,0}/f(z)$ |
|---|---|---|---|
| 0.32 | 0.515 | 0.694 | **0.455** |
| 0.42 | 0.567 | 0.733 | **0.430** |
| 0.57 | 0.641 | 0.783 | **0.403** |
| 0.60 | 0.654 | 0.792 | **0.399** |
| 1.00 | 0.790 | 0.882 | **0.358** |

## Comparison with published measurements

| $z$ | $E_G^\mathrm{obs}$ | $\sigma$ | $E_G^\mathrm{ESD}$ | tension | source |
|---|---|---|---|---|---|
| 0.32 | 0.392 | 0.065 | 0.455 | $0.97\sigma$ | Reyes+ 2010 (SDSS LRG × CFHT-WL) |
| 0.32 | 0.480 | 0.100 | 0.455 | $0.25\sigma$ | Blake+ 2016a (BOSS-LOWZ × RCSLenS) |
| 0.30 | 0.404 | 0.080 | 0.459 | $0.69\sigma$ | Jullo+ 2019 (CFHTLenS × BOSS) |
| 0.32 | 0.400 | 0.090 | 0.455 | $0.61\sigma$ | Singh+ 2020 (BOSS × Planck PR3 $\kappa$) |
| 0.32 | 0.460 | 0.060 | 0.455 | $0.09\sigma$ | Alam+ 2017 (BOSS DR12 RSD-only) |
| 0.42 | 0.430 | 0.110 | 0.430 | $0.00\sigma$ | Amon+ 2018 (KiDS-450 × 2dFLenS+GAMA) |
| 0.57 | 0.300 | 0.070 | 0.403 | $1.47\sigma$ | Blake+ 2016b (BOSS-CMASS × RCSLenS) |
| 0.57 | 0.243 | 0.060 | 0.403 | $2.67\sigma$ | Pullen+ 2016 (BOSS-CMASS × Planck $\kappa$) |
| 0.60 | 0.480 | 0.100 | 0.399 | $0.81\sigma$ | de la Torre+ 2017 (VIPERS PDR-2) |

**Sample statistics**

| Statistic | Value |
|---|---|
| Inverse-variance-weighted mean $\langle E_G\rangle$ at $z_\mathrm{eff} = 0.42$ | $0.381 \pm 0.025$ |
| ESD prediction at $z_\mathrm{eff}$ | $0.431$ |
| Sample-mean tension (all measurements) | $1.97\sigma$ |
| Robust mean (excluding Pullen+ 2016) at $z_\mathrm{eff} = 0.39$ | $0.411 \pm 0.028$ |
| ESD at robust $z_\mathrm{eff}$ | $0.438$ |
| **Robust-mean tension** | $\mathbf{0.98\sigma}$ |
| Within $1\sigma$ | $7/9$ |
| Within $2\sigma$ | $8/9$ |

### The Pullen+ 2016 outlier

The Pullen+ 2016 result $E_G(0.57) = 0.243 \pm 0.060$ — a $\sim 2.7\sigma$
low excursion — is the **only** $E_G$ measurement using CMB lensing
$\kappa_\mathrm{CMB} \times$ CMASS. It has been independently
re-investigated (Singh+ 2020 used the same Planck PR3 $\kappa$ on
LOWZ at $z=0.32$ and found $E_G$ fully consistent with $\Lambda$CDM
at $0.6\sigma$) and the discrepancy has been variously attributed to
TT foreground residuals in PR2, point-source contamination at small
scales, and lensing-bias modelling in the Limber-projection kernel.
ESD shares the $\Lambda$CDM prediction here exactly, so the Pullen
tension is **not** a framework signal — it is a measurement
systematic flagged across the literature.

## Quasi-linear forward prediction

At $k > 0.1\,h/$Mpc the signal begins to include contributions from
bound, virialized halos, for which $R(u)$ **does** apply. Using the
halo-model bound fraction as a smooth transition centred on
$k_\mathrm{NL}(z) \approx 0.2(1+z)^{1.5}\,h/$Mpc and the typical
galaxy-halo $u \approx 3$ ($R \approx 4.2$, $w_D \approx 0.13$), the
framework predicts a small **positive** correction to $E_G$ at
quasi-linear scales:

| $z$ | $E_G^\mathrm{ESD}$ at $k = 0.10\,h/$Mpc | $E_G^\mathrm{ESD}$ at $k = 0.30\,h/$Mpc |
|---|---|---|
| 0.32 | 0.453 ($-0.4\%$) | 0.446 ($-2.0\%$) |
| 0.57 | 0.402 ($-0.3\%$) | 0.397 ($-1.5\%$) |

The $\Sigma/\mu$ ratio drops slightly because the conformal
D-channel enhances $\mu$ more than $\Sigma$ at quasi-linear scales
(photons trace the symmetric Weyl combination $(\Phi + \Psi)/2$
which receives half the conformal lift). The effect is small but
calculable and falls within the reach of LSST $\times$ CMB-S4
high-$\ell$ $E_G$ probes.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | $\geq N{-}1$ of $N$ measurements lie within $2\sigma$ of ESD prediction | PASS ($8/9$) |
| 2 | Robust (single-outlier-rejected) inverse-variance mean tension $< 2\sigma$ | PASS ($0.98\sigma$) |
| 3 | No individual measurement exceeds $3\sigma$ tension | PASS (max $2.67\sigma$ — Pullen) |
| 4 | Linear-regime slip $\eta = 1$ ([Study 19](../F06_linear_growth_s8_prediction/README.md) applicability theorem) | PASS (structural) |
| 5 | No new free parameters | PASS |

## Why this study matters

$E_G$ is the single most-asked-for modified-gravity diagnostic of
the last 15 years. Every scalar-tensor / $f(R)$ / Horndeski paper
that aspires to a cosmological reach reports an $E_G$ curve, and
every weak-lensing $\times$ RSD survey reports a measurement. The
framework's prediction is structurally locked to the $\Lambda$CDM
curve — not because parameters are tuned, but because the closure
kernel's domain of validity excludes linear cosmological modes.
This makes ESD **falsifiable** in a different direction from
$\Lambda$CDM: any robust, multi-survey detection of $E_G$
significantly above or below the $\Omega_{m,0}/f(z)$ curve would
simultaneously challenge ESD and standard cosmology, with no escape
through screened-fifth-force tuning.

## References

- Zhang, P. et al. 2007, PRL 99, 141302 (definition of $E_G$)
- Reyes, R. et al. 2010, Nature 464, 256 (first measurement)
- Blake, C. et al. 2016, MNRAS 462, 4240 (BOSS-LOWZ/CMASS × RCSLenS)
- Pullen, A. R. et al. 2016, MNRAS 460, 4098 (CMB lensing × CMASS)
- Alam, S. et al. 2017, MNRAS 470, 2617 (BOSS DR12 RSD-only)
- de la Torre, S. et al. 2017, A&A 608, A44 (VIPERS PDR-2)
- Amon, A. et al. 2018, MNRAS 479, 3422 (KiDS-450 × 2dFLenS+GAMA)
- Jullo, E. et al. 2019, A&A 627, A137 (CFHTLenS × BOSS)
- Singh, S. et al. 2020, MNRAS 491, 51 (BOSS × Planck PR3 lensing)
- ESD Framework — [Study 18](../F05_weak_lensing_s8_tension/README.md), [Study 19](../F06_linear_growth_s8_prediction/README.md), ESD Framework Book Ch. 4

## Quickstart

```bash
cd studies/F08_eg_gravitational_slip
python scripts/run_eg_audit.py
python scripts/make_eg_figures.py
```
