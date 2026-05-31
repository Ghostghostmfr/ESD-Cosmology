# Study C07 — NS tidal deformability (GW170817)

**Status:** 4/4 gates PASS.

Tidal coupling between two inspiralling neutron stars imprints a
dimensionless parameter $\tilde\Lambda$ on the late-inspiral GW
waveform. GW170817 gave $\tilde\Lambda \le 720$ at 90% CL (LVC 2018,
PRL 121 161101) under a low-spin prior, with a marginalized
posterior peaking near $\tilde\Lambda \sim 300$.

## ESD prediction

Tidal coupling lives at the neutron-star surface where
$g_{\rm surf} \approx 1.9\times10^{12}$ m s$^{-2}$, giving
$u_{\rm NS} = 4 g/a_0 \sim 6\times 10^{22}$. The closure-pool
kernel evaluates to $R(u_{\rm NS}) \sim 10^{-35}$, so the ESD
prediction for $\Lambda$ inherits the GR EOS-driven value
identically. Using an APR-surrogate EOS (matched to NICER, see
[D08](../../D_clusters_halos/D08_nicer_ns_mass_radius/README.md)):

$$
\Lambda_{1.4} \approx 300 \quad (\text{APR-class, GR})
$$

which lies inside the LVC 90% CL band $70 \le \tilde\Lambda \le 720$.

## Anchors

| quantity | value | ref |
|---|---|---|
| $\tilde\Lambda$ 90% upper bound (low-spin) | 720 | LVC 2018 PRL 121 161101 |
| $\tilde\Lambda$ 90% lower bound (low-spin) | 70  | LVC 2019 PRX 9 011001 |
| posterior median (APR-class EOS) | $\sim 300$ | Annala+ 2018 PRL 120 172703 |
| $M_1 + M_2$ (low-spin) | $2.74 ^{+0.04}_{-0.01}\,M_\odot$ | LVC 2017 PRL 119 161101 |

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm NS}) \le 10^{-15}$ at NS surface | $\le 10^{-15}$ | PASS |
| 2 | Predicted $\tilde\Lambda$ inside LVC 90% CL $[70,720]$ | inside | PASS |
| 3 | ESD/GR ratio $1+R \approx 1$ | $\le 10^{-15}$ | PASS |
| 4 | h-blindness: $|R(60)-R(80)| \le 10^{-6}$ | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/C_gravitational_waves/C07_ns_tidal_deformability
pip install -r requirements.txt
make all
```
