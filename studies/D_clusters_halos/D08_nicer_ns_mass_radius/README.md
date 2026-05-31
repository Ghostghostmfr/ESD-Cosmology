# Study D08 — NICER NS mass–radius

**Status:** 4/4 gates PASS.

NICER X-ray timing of millisecond pulsars provides simultaneous
mass and radius measurements via rotating-hot-spot waveform fits.
Three high-precision sources:

- **PSR J0030+0451** (Miller+ 2019 ApJL 887, L24; Riley+ 2019 ApJL
  887, L21): $M = 1.44^{+0.15}_{-0.14}\,M_\odot$,
  $R = 13.02^{+1.24}_{-1.06}$ km (Miller+).
- **PSR J0740+6620** (Miller+ 2021 ApJL 918, L28): the heaviest
  precisely-measured NS, $M = 2.08\pm 0.07\,M_\odot$,
  $R = 13.7^{+2.6}_{-1.5}$ km.
- **PSR J0437-4715** (Choudhury+ 2024 ApJL 971, L20):
  $M = 1.418\pm 0.044\,M_\odot$, $R = 11.36^{+0.95}_{-0.63}$ km.

## Framework expectation

At a NS surface, $g \sim 10^{12}$ m/s² so $u \gg 10^{21}$ and the
closure-pool kernel $R(u) \to 0$ to far below current NICER
fractional precision (~5–15% on $R$). The TOV equation is therefore
GR-identical, and *the framework is consistent with NICER iff the GR
TOV $M$–$R$ curve under a reasonable nuclear EoS passes through the
NICER ellipses*. ESD does not modify the EoS.

We adopt a representative APR-style polytropic surrogate (Tolman
VII modulated) calibrated to reproduce the canonical $1.4\,M_\odot$
radius at 12.5 km and the maximum mass at 2.2 $M_\odot$.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm NS}) \le 10^{-15}$ at all 3 NICER sources | $\le 10^{-15}$ | PASS |
| 2 | Median $|R_{\rm pred} - R_{\rm obs}|/R_{\rm obs} \le 0.15$ | $\le 0.15$ | PASS |
| 3 | All 3 sources within $\le 2\sigma$ on $R$ | $\le 2.0$ | PASS |
| 4 | h-blind | $\le 10^{-6}$ | PASS |

## Scope boundary

A nuclear EoS uncertainty band exists in the literature spanning
$\sim 11$–$13$ km at $1.4\,M_\odot$. The point of this study is *not*
to fit the EoS; it is to check that ESD does not break a strong-field
test it cannot improve. The APR-surrogate is illustrative; replacing
it with another EoS in the band does not change the verdict.

## Run

```bash
cd studies/D_clusters_halos/D08_nicer_ns_mass_radius
pip install -r requirements.txt
make all
```
