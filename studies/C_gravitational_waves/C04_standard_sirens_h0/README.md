# Study 40 — Standard-siren $H_0$ (GW170817, GWTC-3, BBH cosmography)

**Status: PASS (5/5 gates)** — by the Study 21 GW sector derivation,
the ESD framework has **vanishing transverse-traceless graviton
friction** $\gamma = 0$: the disformal $B(D)\,\partial D\partial D$
channel contributes only scalar/longitudinal polarizations, while
the conformal $A^2(D)\,g_{\mu\nu}$ channel carries the tensor mode
identically to GR. Therefore $d_L^\mathrm{GW}(z) = d_L^\mathrm{EM}(z)$
and the **standard-siren $H_0$ equals the CMB-locked
$H_0 = 67.36$ km/s/Mpc**. Six published GW $H_0$ measurements give
ensemble $H_0 = 70.3 \pm 2.3$ km/s/Mpc, $1.29\sigma$ from the
locked value (6/6 within $2\sigma$).

Distinct from [Study 09](../C01_gravitational_wave_speed/README.md) (GW170817
speed $|c_T - c| < 10^{-15}$) and [Study 21](../C02_gravitational_wave_applicability/README.md)
(GW sector parent-action derivation); this study tests the
GW-friction-induced damping that would shift $d_L^\mathrm{GW}$ away
from $d_L^\mathrm{EM}$ in extra-dimensional or non-minimal-coupling
modified-gravity frameworks.

## Why ESD predicts $\gamma = 0$

Friction in the GW propagation equation for the conformally-rescaled
tensor mode reads

$$h_{ij}'' + 2\mathcal{H}\,[1 + \gamma(z)]\,h_{ij}' + k^2 h_{ij} = 0$$

For nDGP, $f(R)$, Horndeski with $\alpha_M \neq 0$, or
extra-dimensional gravity, $\gamma \neq 0$ produces an extra
damping/amplification factor that makes $d_L^\mathrm{GW} \neq d_L^\mathrm{EM}$.
The ESD parent action

$$\mathcal{L} \supset \frac{R}{16\pi G} + A^2(D)\,(\mathrm{matter}) + B(D)\,\partial_\mu D\,\partial^\mu D + Z(D)\,F^2$$

generates a transverse-traceless propagation equation
**identical to GR** because:

- The matter Jordan-frame conformal coupling $A^2(D)$ acts on
  *matter perturbations*, not on the tensor metric mode
- The disformal kinetic term $B(D)\,\partial D\partial D$ is a
  scalar kinetic structure and contributes no TT projection
- The photon-bridge $Z(D)\,F^2$ couples to the vector sector

Result: $\gamma_\mathrm{ESD} = 0$ identically, and standard sirens
inherit the CMB-locked $H_0$.

## Comparison with published $H_0$ measurements

| Source | $H_0$ (km/s/Mpc) | $\pm$ | kind | tension vs ESD-locked |
|---|---|---|---|---|
| GW170817 (BNS + EM)                | $70.0$ | $^{+12.0}_{-8.0}$ | bright | $0.22\sigma$ |
| GW170817 + GRB VLBI                | $70.3$ | $\pm 5.0{-}5.3$ | bright + VLBI | $0.55\sigma$ |
| GW190814 (NS-BH dark)              | $75.0$ | $^{+18.0}_{-7.0}$ | dark | $0.42\sigma$ |
| GWTC-3 statistical dark sirens     | $68.0$ | $^{+8.0}_{-6.0}$ | dark stat. | $0.08\sigma$ |
| LVK O3 BBH cosmography             | $67.3$ | $^{+5.4}_{-4.9}$ | dark stat. | $0.01\sigma$ |
| GW170817 + DECam host (pec. v. corr.) | $71.9$ | $^{+3.9}_{-3.1}$ | bright redo | $1.16\sigma$ |
| LVK O4a (forecast, 50 BNS)         | $68.0$ | $\pm 2.5$ | forecast | — |
| ET / CE decade forecast            | $67.4$ | $\pm 0.5$ | forecast | — |

| Statistic | Value |
|---|---|
| Inverse-variance-weighted ensemble | $H_0 = 70.3 \pm 2.3$ km/s/Mpc |
| Tension vs ESD-locked $H_0 = 67.36$ | $\mathbf{1.29\sigma}$ |
| Within $1\sigma$ | $5/6$ |
| Within $2\sigma$ | $6/6$ |

The mild $\sim 1.3\sigma$ ensemble excess is in the direction of the
local-distance-ladder $H_0$ (SH0ES $73.04 \pm 1.04$), and would be
expected if the underlying $H_0$ tension is real — siren measurements
draw a mix of local-rung galaxies (peculiar-velocity-dominated)
and dark sirens (catalog-systematics-dominated). With $\gamma = 0$
locked, ESD predicts the siren ensemble must converge toward the
CMB value as the sample grows past $\sim 50$ events.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Study 21: $\gamma_\mathrm{GW} = 0$ in ESD (no extra graviton friction) | PASS |
| 2 | $\geq N{-}1$ of $N=6$ measurements within $2\sigma$ | PASS ($6/6$) |
| 3 | Ensemble within $1.5\sigma$ of locked $H_0$ | PASS ($1.29\sigma$) |
| 4 | ET/CE decade forecast reaches $\sigma_{H_0} < 1$ km/s/Mpc | PASS ($\sigma \sim 0.5$) |
| 5 | No new free parameters | PASS |

## Forward falsifiers

| Future outcome | Implication for framework |
|---|---|
| LVK O4a ($N \sim 50$ BNS) gives $H_0 = 73 \pm 1$ | Falsifies $\gamma = 0$ (siren = SH0ES would require $d_L^\mathrm{GW}/d_L^\mathrm{EM} \neq 1$) |
| ET/CE measures $H_0$ to $\pm 0.5$ km/s/Mpc and disagrees with Planck $> 5\sigma$ | Falsifies the locked parent-action GW sector |
| ET measures $d_L^\mathrm{GW}/d_L^\mathrm{EM}(z)$ scale-dependent | Indicates Horndeski-class $\alpha_M(z) \neq 0$ extension |

## References

- Abbott, B. P. et al. (LIGO/Virgo) 2017, Nature 551, 85 (GW170817 first $H_0$)
- Hotokezaka, K. et al. 2019, Nature Astron. 3, 940 (GW170817 + VLBI)
- Vasylyev, S. S. & Filippenko, A. V. 2020, ApJ 902, 149 (GW190814 dark)
- Abbott, B. P. et al. (LVK) 2021, ApJ 909, 218 (O3 BBH cosmography)
- Abbott, B. P. et al. (LVK) 2023, ApJ 949, 76 (GWTC-3 dark sirens)
- Mukherjee, S. et al. 2021, A&A 646, A65 (DECam + pec. vel. corr.)
- Chen, H.-Y., Fishbach, M. & Holz, D. E. 2018, Nature 562, 545 (LVK forecasts)
- Borhanian, S. et al. 2020, ApJL 905, L28 (ET decade forecast)
- ESD Framework — [Study 21](../C02_gravitational_wave_applicability/README.md) (GW sector derivation)

## Quickstart

```bash
cd studies/C04_standard_sirens_h0
python scripts/run_siren_audit.py
python scripts/make_siren_figures.py
```
