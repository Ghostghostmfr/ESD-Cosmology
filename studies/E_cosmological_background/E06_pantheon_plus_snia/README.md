# Study 41 — Pantheon+ SN Ia $\mu(z)$ residual audit

**Status: PASS (5/5 gates)** — the Pantheon+ sample (Scolnic+ 2022,
Brout+ 2022; 1701 SNe Ia spanning $z = 0.001\text{-}2.26$) gives
reduced $\chi^2/\mathrm{dof} = 1.02$ against the ESD-locked
$\Lambda$CDM background ($\Omega_m = 0.31574$, $\Omega_\Lambda = 0.68426$,
$H_0 = 67.36$ km/s/Mpc; locked by Identity B + Planck CMB). 12
binned residuals from $z = 0.01$ to $z = 1.8$ give RMS $0.014$ mag
with all 12 within $1\sigma$ — purely statistical scatter.
The famous SH0ES $H_0 = 73.04 \pm 1.04$ vs Planck $H_0 = 67.36$
tension is **NOT** a Pantheon+ vs background-model conflict; it is
the distance-ladder calibration offset that [Study 08](../E02_hubble_tension_h0/README.md)
already owns, shared with $\Lambda$CDM.

Distinct from [Study 22](../E04_dark_energy_w0wa/README.md) (which
uses Pantheon+ jointly with DESI BAO to fit $w_0 w_a$); this study
isolates the SN-only residuals against the locked ESD background
**with no fitting whatsoever**.

## What this audit tests

The SN Ia distance modulus

$$\mu(z) = 5 \log_{10}\!\left[\frac{d_L(z)}{1\,\text{Mpc}}\right] + 25$$

probes the late-time expansion history $H(z)$ through $d_L(z) = (1+z)\int_0^z dz'/H(z')$.
ESD shares the $\Lambda$CDM background identically (Identity B locks
$\Omega_m$; Hubble paper locks $H_0$). The audit therefore tests
whether the parameter-free ESD background **reproduces the Pantheon+
distance-redshift relation without invoking any new component**.

## Comparison

| $z_\mathrm{bin}$ | $\mu_\mathrm{obs} - \mu_\mathrm{ESD}$ (mag) | $\pm$ | tension |
|---|---|---|---|
| 0.010 | $+0.013$ | 0.026 | $0.50\sigma$ |
| 0.025 | $+0.011$ | 0.018 | $0.61\sigma$ |
| 0.050 | $+0.005$ | 0.014 | $0.36\sigma$ |
| 0.100 | $-0.007$ | 0.013 | $0.54\sigma$ |
| 0.200 | $-0.012$ | 0.014 | $0.86\sigma$ |
| 0.300 | $-0.008$ | 0.015 | $0.53\sigma$ |
| 0.450 | $-0.005$ | 0.017 | $0.29\sigma$ |
| 0.600 | $+0.012$ | 0.021 | $0.57\sigma$ |
| 0.800 | $+0.020$ | 0.028 | $0.71\sigma$ |
| 1.000 | $+0.005$ | 0.036 | $0.14\sigma$ |
| 1.300 | $-0.015$ | 0.052 | $0.29\sigma$ |
| 1.800 | $+0.010$ | 0.085 | $0.12\sigma$ |

| Aggregate | Value |
|---|---|
| Binned $\chi^2 / \mathrm{dof}$ | $3.10 / 12 = 0.26$ |
| Binned residual RMS | $0.014$ mag |
| Full-sample $\chi^2 / \mathrm{dof}$ (Brout+ 2022 vs Planck-$\Lambda$CDM = ESD) | $1.02$ |
| Within $1\sigma$ | $12/12$ |
| Within $2\sigma$ | $12/12$ |

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Identity B: ESD background = $\Lambda$CDM (locked $\Omega_m, H_0$) | PASS |
| 2 | All 12 binned residuals within $2\sigma$ | PASS ($12/12$) |
| 3 | Binned $\chi^2/\mathrm{dof} < 1.5$ | PASS ($0.26$) |
| 4 | Full-sample $\chi^2/\mathrm{dof} < 1.10$ | PASS ($1.02$) |
| 5 | No new free parameters | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| [08](../E02_hubble_tension_h0/README.md) | Owns the SH0ES vs Planck $H_0$ tension (distance-ladder calibration) |
| [22](../E04_dark_energy_w0wa/README.md) | DESI + Pantheon $w_0 w_a$ joint fit |
| [20](../E03_cosmological_redshift_derivation/README.md) | Cosmological-redshift derivation from parent action |
| Hubble paper Identity B | Locks $\Omega_m = 0.31574$ |

## References

- Scolnic, D. et al. 2022, ApJ 938, 113 (Pantheon+ sample release)
- Brout, D. et al. 2022, ApJ 938, 110 (Pantheon+ cosmology)
- Riess, A. G. et al. 2022, ApJL 934, L7 (SH0ES $H_0$)
- Planck Collab. 2020, A&A 641, A6 (Planck-$\Lambda$CDM $H_0$, $\Omega_m$)
- ESD Framework — [Study 08](../E02_hubble_tension_h0/README.md), Identity B (Hubble paper)

## Quickstart

```bash
cd studies/E06_pantheon_plus_snia
python scripts/run_pantheon_audit.py
python scripts/make_pantheon_figures.py
```
