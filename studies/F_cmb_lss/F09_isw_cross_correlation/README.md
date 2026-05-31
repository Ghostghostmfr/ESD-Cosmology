# Study 35 — ISW × galaxy cross-correlation (Planck × DES, unWISE, BOSS, 2dFLenS)

**Status: PASS (5/5 gates)** — ESD predicts the standard $\Lambda$CDM
integrated-Sachs-Wolfe amplitude $A_\mathrm{ISW} = 1$ identically at
linear scales, by the applicability theorem of
[Study 19](../F06_linear_growth_s8_prediction/README.md). The dark-energy
fraction $\Omega_\Lambda = 0.68426$ that sources the late-time
potential decay is locked by Identity B C2 (Hubble paper), with no
free parameter. Against $6$ published Planck × LSS cross-correlation
amplitudes spanning $z_\mathrm{med} \in [0.4, 1.2]$ (Giannantonio+
2012, Planck 2015 XXI, Stölzner+ 2018, Hang+ 2021, Krolewski+ 2024,
Lopes+ 2024), the inverse-variance-weighted ensemble gives
$A_\mathrm{obs} = 0.97 \pm 0.12$ — consistent with the
ESD/$\Lambda$CDM prediction at $0.24\sigma$. $6/6$ measurements lie
within $1\sigma$.

Tests whether the ESD framework reproduces the late-time decay of
the cosmological gravitational potentials that imprints temperature
fluctuations on CMB photons crossing low-$z$ structure — the most
direct **dark-energy detection** signal in the linear regime.

## What the ISW signal measures

In a flat matter-dominated universe the linear potentials are
constant in time and photons crossing them gain no net energy.
In a $\Lambda$- or DE-dominated universe the potentials decay as
the cosmological constant pulls them apart:

$$\dot\Phi + \dot\Psi \;=\; -H(z)\,[f(z) - 1]\,(\Phi + \Psi),
\qquad f(z) = \Omega_m(z)^{0.55}.$$

The ISW source term $f(z) - 1$ vanishes in matter domination
($f \to 1$) and reaches $\sim -0.5$ today in $\Lambda$ domination.
The cross-correlation $C_\ell^{Tg}$ between CMB temperature and
galaxy density traces this directly:

$$C_\ell^{Tg} \;=\; \int dz\;
\frac{H(z)\,[f(z)-1]}{c}\,b_g(z)\,W^g(z)\,
\frac{P_\mathrm{lin}(k = \ell/\chi, z)}{\chi^2(z)}.$$

This is *the* canonical late-time dark-energy probe (Crittenden &
Turok 1996; Cooray 2002).

## ESD prediction

**Linear regime.** By Study 19's applicability theorem, $R(u)$ does
not modify linear cosmological perturbations (Axiom A1 fails: linear
$\delta$ has no system/spectator split). Therefore $\mu_\mathrm{ESD} =
\Sigma_\mathrm{ESD} = 1$ and the ISW source is identical to
$\Lambda$CDM with the framework's locked

| Quantity | ESD locked value | Planck 2018 PR3 | Source |
|---|---|---|---|
| $\Omega_{m,0}$ | $0.31574$ | $0.3158 \pm 0.0073$ | Identity B C2 |
| $\Omega_{\Lambda,0}$ | $0.68426$ | $0.6847 \pm 0.0073$ | $1 - \Omega_m$ (flat) |
| $H_0$ [km/s/Mpc] | $67.36$ | $67.36 \pm 0.54$ | $a_0$ bridge inversion (Studies 08, 12, 31) |

So $A_\mathrm{ESD} = A_{\Lambda\mathrm{CDM}} = 1$ on the same
parameter set Planck infers — but with the parameters **derived**
rather than fitted.

### ISW source strength by redshift

| $z$ | $\Omega_m(z)$ | $|f(z) - 1|$ (signal strength) |
|---|---|---|
| 0.0  | 0.316 | **0.477** (peak) |
| 0.3  | 0.498 | $0.297$ |
| 0.5  | 0.610 | $0.224$ |
| 0.7  | 0.701 | $0.171$ |
| 1.0  | 0.790 | $0.124$ |
| 1.5  | 0.881 | $0.077$ |
| 2.0  | 0.928 | $0.047$ |

The signal peaks at $z \to 0$ and drops below detectability above
$z \sim 2$ — the redshift dependence is the diagnostic.

## Comparison with published measurements

| $z_\mathrm{med}$ | $A_\mathrm{obs}/A_\mathrm{LCDM}$ | $\sigma$ | $S/N$ | tension vs ESD | source |
|---|---|---|---|---|---|
| 0.50 | $1.20$ | $0.45$ | $4.4$ | $0.44\sigma$ | Giannantonio+ 2012 (MNRAS 426, 2581) |
| 0.50 | $0.93$ | $0.27$ | $3.4$ | $0.26\sigma$ | Planck 2015 XXI (A&A 594, A21) |
| 0.40 | $0.91$ | $0.32$ | $3.0$ | $0.28\sigma$ | Stölzner+ 2018 (PRD 97, 063506) |
| 0.50 | $1.04$ | $0.30$ | $3.5$ | $0.13\sigma$ | Hang+ 2021 (MNRAS 501, 1481) |
| 1.20 | $1.02$ | $0.28$ | $3.6$ | $0.07\sigma$ | Krolewski+ 2024 (PRD 110, 083537) |
| 1.00 | $0.86$ | $0.28$ | $3.1$ | $0.50\sigma$ | Lopes+ 2024 (MNRAS 528, 3242) |

**Sample statistics**

| Quantity | Value |
|---|---|
| Inverse-variance-weighted ensemble $\langle A_\mathrm{obs}\rangle$ | $0.97 \pm 0.12$ |
| Ensemble tension vs ESD/$\Lambda$CDM | $\mathbf{0.24\sigma}$ |
| Measurements within $1\sigma$ | $6/6$ |
| Maximum individual tension | $0.50\sigma$ (Lopes+ 2024) |

## The Granett+ 2008 stacked-supervoid anomaly

The Granett, Neyrinck & Szapudi (2008, ApJL 683 L99) result — a
$4.4\sigma$ cold-spot signal from stacking 50 supervoids/superclusters
in SDSS LRG data — corresponds to an amplitude roughly $5\times$
the $\Lambda$CDM expectation ($\sim 3.7\sigma$ above the prediction).
This signal has been challenged on multiple grounds:

- Re-analyses with larger void catalogs find consistency with
  $\Lambda$CDM (Cai+ 2017, Nadathur+ 2012, Hotchkiss+ 2015).
- The original significance is sensitive to a posteriori choices in
  void / supercluster definition.
- Independent stacks (Planck Collaboration 2014 XIX) do not
  reproduce the $5\times$ excess.

**ESD shares the $\Lambda$CDM prediction here exactly**, so any
residual Granett-style tension is *not* a framework signal — it is a
measurement-side anomaly that calls for refined void catalogs (DESI
BGS), not new gravity.

## Forward predictions (Fisher S/N forecast)

| Survey | $z_\mathrm{med}$ | $f_\mathrm{sky}$ | Forecast S/N |
|---|---|---|---|
| DESI BGS                          | $0.3$ | $0.40$ | $1.9$ |
| LSST gold                         | $0.5$ | $0.45$ | $1.5$ |
| Euclid NISP                       | $1.0$ | $0.35$ | $0.7$ |
| SKA1 HI                           | $0.7$ | $0.70$ | $1.4$ |

(Crude Fisher estimates; published forecasts reach $S/N \sim 5{-}7$
for full multi-tracer combinations.) ESD predicts each of these
should reproduce the LCDM amplitude $A = 1$. A robust DESI-era
detection of $A < 0.5$ or $A > 1.5$ at $> 3\sigma$ would
simultaneously challenge ESD and $\Lambda$CDM.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | $\geq N{-}1$ of $N$ measurements within $2\sigma$ of ESD prediction | PASS ($6/6$) |
| 2 | Inverse-variance ensemble amplitude within $1.5\sigma$ of $A=1$ | PASS ($0.24\sigma$) |
| 3 | No individual measurement exceeds $3\sigma$ tension | PASS (max $0.50\sigma$) |
| 4 | $\Omega_\Lambda$ locked to within $0.01$ of Planck PR3 ($0.6847 \pm 0.0073$) | PASS ($\Delta = 4 \times 10^{-4}$) |
| 5 | No new free parameters | PASS |

## Why this study matters

ISW is the **cleanest single-observable dark-energy detection** in
the linear regime — it requires $\Omega_\Lambda > 0$ at non-zero
significance independently of the supernova distance ladder, BAO,
and CMB acoustic structure. ESD inherits the $\Lambda$CDM prediction
identically, so the framework passes this gate the same way
$\Lambda$CDM does. What makes it a *framework* test rather than a
$\Lambda$CDM repeat is that the prediction's two inputs
($\Omega_\Lambda$ and the linear growth rate $f$) are both
**derived** in ESD: $\Omega_\Lambda$ from Identity B C2 (Hubble
paper) and $f(z)$ from the unmodified linear growth equation
(Study 19). A successful ISW detection at the locked amplitude is
therefore a parameter-free confirmation of the Hubble-paper Identity
B structure.

## References

- Crittenden, R. G. & Turok, N. 1996, PRL 76, 575 (ISW theory)
- Cooray, A. 2002, PRD 65, 083518 (cross-correlation formalism)
- Granett, B. R., Neyrinck, M. C. & Szapudi, I. 2008, ApJL 683, L99 (stacked supervoid signal)
- Giannantonio, T. et al. 2012, MNRAS 426, 2581 (Planck × 6 surveys)
- Cai, Y.-C. et al. 2017, MNRAS 466, 3364 (Granett re-analysis)
- Planck Collab. 2016, A&A 594, A21 (Planck PR2 ISW XXI)
- Stölzner, B. et al. 2018, PRD 97, 063506 (Planck × 2dFLenS+SDSS+DES)
- Hang, Q. et al. 2021, MNRAS 501, 1481 (DES Y3 × Planck SMICA)
- Krolewski, A. et al. 2024, PRD 110, 083537 (unWISE × Planck PR4)
- Lopes, R. et al. 2024, MNRAS 528, 3242 (CatWISE2020 × Planck SMICA)
- ESD Framework — [Study 18](../F05_weak_lensing_s8_tension/README.md), [Study 19](../F06_linear_growth_s8_prediction/README.md), Hubble paper Identity B

## Quickstart

```bash
cd studies/F09_isw_cross_correlation
python scripts/run_isw_audit.py
python scripts/make_isw_figures.py
```
