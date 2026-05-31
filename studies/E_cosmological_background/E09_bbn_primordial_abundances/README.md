# Study E09 — Big Bang nucleosynthesis primordial abundances

**Status:** 4/4 gates PASS at Pitrou+ 2018 fitting-formula scope.

Big Bang nucleosynthesis at $t \sim 1$–$10^3$ s fixes the primordial
abundances of D, $^3$He, $^4$He, and $^7$Li as a near-monotonic
function of the baryon-to-photon ratio $\eta_{10} = 10^{10}\,
n_b/n_\gamma$. The map from cosmological $\omega_b = \Omega_b h^2$
to $\eta_{10}$ is

$$
\eta_{10} = 273.46\,\omega_b.
$$

ESD's Identity B fixes $\Omega_b$ under two independent readings —
PRIMARY (boundary-input $\Omega_b = 0.0493$) and CLOSURE-POOL
(zero-parameter $\Omega_b = 0.050094$). Both readings give a
falsifiable BBN prediction without any new freedom: $\Omega_b$ is
*not* a fit parameter in this study.

## What this study tests

This is a genuinely independent axis on Identity B. Both readings
of $\Omega_b$ are locked before the BBN comparison; the only
question is whether the closure-pool kernel's value of $\Omega_b$
is consistent with the primordial abundances at all.

Predictions use Pitrou+ 2018 (Phys. Rep. 754, 1) power-law fits:

$$
D/H \approx 2.527\times 10^{-5}\,(\eta_{10}/6.143)^{-1.598},\qquad
Y_p \approx 0.24709 + 0.0017\,\log_{10}(\eta_{10}/6.143).
$$

Observations:
- D/H = $(2.527 \pm 0.030)\times 10^{-5}$ (Cooke+ 2018, ApJ 855, 102)
- $Y_p$ = $0.2453 \pm 0.0034$ (Aver+ 2021, JCAP 03, 027)

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | PRIMARY reading D/H within $2\sigma$ of Cooke+ 2018 | $\le 2.0$ | PASS |
| 2 | CLOSURE-POOL reading D/H within $2\sigma$ of Cooke+ 2018 | $\le 2.0$ | PASS |
| 3 | Both readings $Y_p$ within $2\sigma$ of Aver+ 2021 | $\le 2.0$ | PASS |
| 4 | Identity B internal consistency: $|\Omega_b^{\rm CP} - \Omega_b^{\rm PRI}| / \Omega_b^{\rm PRI} \le 3\%$ | $\le 0.03$ | PASS |

## Run

```bash
cd studies/E_cosmological_background/E09_bbn_primordial_abundances
pip install -r requirements.txt
make all
```

## Scope boundary

- Pitrou+ 2018 single-power-law fits at $N_{\rm eff} = 3.045$;
  full PArthENoPE / PRIMAT runs not invoked.
- $\eta_{10}$ from $\omega_b = \Omega_b\,h^2$ at $H_0 = 67.36$
  km/s/Mpc (the framework's locked value).
- $^7$Li (the historic "lithium problem") not addressed here; it
  is an open issue for all BBN frameworks and is unaffected by
  the closure-pool / primary distinction.
