# Study C10 — Black-hole ringdown echoes

**Status:** 5/5 gates PASS (zero-parameter null prediction).

Gravitational-wave **echoes** are repeated, progressively damped copies
of the main ringdown signal that arrive *after* the fundamental
quasinormal-mode (QNM) ring-down. They are the smoking-gun signature
of an exotic compact object (ECO) whose inner boundary is partially
**reflecting** rather than a classical absorbing horizon — e.g.
Planck-scale-corrected horizons, gravastars, wormholes, firewalls, and
fuzzballs (Cardoso, Franzin & Pani 2016 PRL **116** 171101;
Cardoso & Pani 2019 Living Rev. Rel. **22** 4).

This is distinct from the existing benchmark C05, which tests the
*fundamental* $220$ QNM frequency and damping time. Echoes probe the
**inner boundary condition** at the horizon, a separate prediction.

## ESD prediction

By the GW-sector applicability theorem (Study C02) the ESD tensor
sector reduces identically to GR, and near the horizon
$u = 4g/a_0 \sim 10^{22}$ so the closure kernel $R(u)\to 0$
($\sim 3\times10^{-35}$ for a $62\,M_\odot$ remnant). ESD therefore
inherits the **classical, perfectly absorbing** GR horizon: there is no
reflective inner surface, so the inner-boundary reflectivity and echo
amplitude both vanish exactly,

$$
\mathcal{R}_{\rm wall}^{\rm ESD} = 0, \qquad A_{\rm echo}^{\rm ESD} = 0,
\qquad |\mathcal{R}_{\rm wall}^{\rm ESD}-0|\le R(u_{\rm horizon}).
$$

No free parameter enters. A reflective surface at proper distance
$\epsilon$ from the horizon *would* produce an echo train with delay
$\Delta t_{\rm echo}\sim 2(GM/c^3)|\ln\epsilon|$; ESD predicts **no**
echo at any cadence, a **falsifiable null** broken by any confirmed
($\ge 5\sigma$) echo detection. The same null discriminates against the
ECO alternatives above.

## Anchors

| search | constraint | significance | ref |
|---|---|---|---|
| Abedi+ 2017 (GW150914/151226/170104) | tentative echoes | $2.5$–$4.2\sigma$ (claim) | Abedi, Dykaar & Afshordi 2017 PRD 96 082004 |
| Westerweck+ 2018 (re-analysis) | consistent with noise | $\lesssim 1\sigma$ | Westerweck+ 2018 PRD 97 124037 |
| LVK TGR O3 | no confirmed echo | $\lesssim 1\sigma$ | Abbott+ 2021 PRD 103 122002 |

No statistically significant echo survives trials correction; the ESD
prediction $\mathcal{R}_{\rm wall}=0$ is consistent with every search.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm horizon})$ at $62\,M_\odot$ | $\le 10^{-12}$ | PASS |
| 2 | Classical horizon: reflectivity $=$ echo amplitude $= 0$ (bound) | $\le 10^{-12}$ | PASS |
| 3 | $\mathcal{R}_{\rm wall}=0$ inside all echo-search bounds | all inside | PASS |
| 4 | No confirmed ($\ge 5\sigma$) echo detection in data | $< 5\sigma$ | PASS |
| 5 | $h$-blindness: $\lvert R(60)-R(80)\rvert$ at horizon | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/C_gravitational_waves/C10_bh_ringdown_echoes
pip install -r requirements.txt
make all
```

Outputs are written to `scripts/outputs/` (claims.csv, samples.csv,
summary.json) and `figures_generated/` (fig_echoes.png/pdf).
