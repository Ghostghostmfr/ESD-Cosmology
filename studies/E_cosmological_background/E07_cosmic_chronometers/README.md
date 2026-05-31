# Study 42 — Cosmic chronometers $H(z)$

**Status: PASS (5/5 gates)** — the 32-point cosmic-chronometer
compilation (Simon+ 2005, Stern+ 2010, Moresco+ 2012/2015/2016,
Zhang+ 2014, Ratsimbazafy+ 2017, Borghi+ 2022) gives $\chi^2/\mathrm{dof}
= 0.66$ against the ESD-locked $\Lambda$CDM background
($H_0 = 67.36$, $\Omega_m = 0.31574$), with $26/32$ within $1\sigma$
and $31/32$ within $2\sigma$.

Cosmic chronometers (Jimenez & Loeb 2002) extract $H(z)$ from
$dz/dt$ of passively evolving early-type galaxies — a
**model-independent** measurement requiring no FRW distance
assumption. This is therefore the cleanest possible test of ESD's
locked background expansion across $z = 0.07\text{-}2.0$.

## What this audit tests

$$H(z) = -\frac{1}{1+z}\frac{dz}{dt}$$

extracted from differential ages of matched-age early-type galaxy
pairs. ESD inherits the $\Lambda$CDM background via Identity B
(Hubble paper) so the prediction is parameter-free at the locked
$(H_0, \Omega_m)$.

## Comparison summary

| Aggregate | Value |
|---|---|
| Number of measurements | 32 |
| Redshift range | $0.07 \le z \le 2.0$ |
| $\chi^2 / \mathrm{dof}$ | $21.19 / 32 = 0.66$ |
| Within $1\sigma$ | $26 / 32$ ($81\%$) |
| Within $2\sigma$ | $31 / 32$ ($97\%$) |

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Identity B: ESD background = $\Lambda$CDM | PASS |
| 2 | $\chi^2/\mathrm{dof} < 1.5$ | PASS ($0.66$) |
| 3 | $\ge 95\%$ within $2\sigma$ | PASS ($31/32$) |
| 4 | $\ge 60\%$ within $1\sigma$ | PASS ($26/32$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [08](../E02_hubble_tension_h0/README.md) | SH0ES vs Planck $H_0$ tension |
| [22](../E04_dark_energy_w0wa/README.md) | DESI + Pantheon $w_0 w_a$ |
| [41](../E06_pantheon_plus_snia/README.md) | SN Ia $\mu(z)$ residuals (sibling background test) |

## References

- Jimenez, R. & Loeb, A. 2002, ApJ 573, 37 (differential-age method)
- Simon, J., Verde, L., & Jimenez, R. 2005, PRD 71, 123001
- Stern, D. et al. 2010, JCAP 02, 008
- Moresco, M. et al. 2012, JCAP 08, 006
- Moresco, M. 2015, MNRAS 450, L16
- Moresco, M. et al. 2016, JCAP 05, 014
- Zhang, C. et al. 2014, RAA 14, 1221
- Ratsimbazafy, A. L. et al. 2017, MNRAS 467, 3239
- Borghi, N. et al. 2022, ApJ 928, L4

## Quickstart

```bash
cd studies/E07_cosmic_chronometers
python scripts/run_cc_audit.py
python scripts/make_cc_figures.py
```
