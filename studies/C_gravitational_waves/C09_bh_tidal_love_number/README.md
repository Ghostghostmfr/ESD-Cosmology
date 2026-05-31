# Study C09 — Black-hole tidal Love number $k_2$

**Status:** 4/4 gates PASS (zero-parameter null prediction).

The quadrupolar tidal Love number $k_2$ quantifies the static
deformability of a compact object in an external tidal field. In
general relativity the result for a black hole is exact and
remarkable: a Schwarzschild or Kerr black hole has a **vanishing**
Love number,

$$
k_2^{\rm BH} = 0 \quad\Longrightarrow\quad \Lambda^{\rm BH} = \tfrac{2}{3}\,k_2\,C^{-5} = 0,
$$

with horizon compactness $C = GM/(Rc^2) = 1/2$
(Binnington & Poisson 2009; Damour & Nagar 2009;
Gürlebeck 2015 PRL **114** 151102; Chia 2021 PRD **104** 024013).

This is distinct from the existing benchmarks: C05 (ringdown 220 QNM)
tests the *dynamical* fundamental-mode frequency, and C08 tests spin
*extremality* — neither tests the *static* Love number $k_2$.

## ESD prediction

The ESD tensor sector reduces identically to GR
(GW-sector applicability theorem, Study C02). At a black-hole horizon
the surface gravity is $\kappa = c^4/(4GM)$, giving for a $30\,M_\odot$
BH $g_{\rm horizon}\simeq 5\times10^{11}$ m s$^{-2}$ and hence

$$
u_{\rm horizon} = \frac{4 g_{\rm horizon}}{a_0}\simeq 1.7\times10^{22},
\qquad R(u_{\rm horizon})\simeq 3\times10^{-35}.
$$

The static $\ell=2$ tidal-response problem is therefore solved in a
metric that is GR's to a fractional precision of $\sim10^{-35}$, so the
vanishing-Love-number theorem is inherited:
$k_2^{\rm ESD} = 0$ with $|k_2^{\rm ESD}-0|\le R(u_{\rm horizon})$.
No free parameter enters.

This is a **falsifiable null**: a confirmed nonzero black-hole Love
number ($k_2\neq0$) would break ESD's GR-equivalent strong-field
sector. It discriminates against exotic compact objects (boson stars
$k_2\sim10$–$100$; gravastars $k_2<0$; wormholes $k_2\sim O(0.1$–$1)$;
Cardoso+ 2017 PRD **95** 084014).

## Anchors

| source | quantity | value | ref |
|---|---|---|---|
| Kerr theorem | $k_2^{\rm BH}$ | $0$ (exact) | Binnington & Poisson 2009; Gürlebeck 2015 |
| GW170817 | $\tilde\Lambda$ (90% CL) | $\le 720$ (low-spin) | Abbott+ 2019 PRX 9 011001 |
| GW190425 | $\tilde\Lambda$ (90% CL) | $\le 600$ | Abbott+ 2020 ApJL 892 L3 |

The BH prediction $\Lambda=0$ lies inside every bound; the bounds set
the scale at which a nonzero BH Love number would become detectable.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm horizon})$ at $30\,M_\odot$ | $\le 10^{-12}$ | PASS |
| 2 | $k_2^{\rm ESD}=0$ (Kerr theorem inherited), deviation bound | $\le 10^{-12}$ | PASS |
| 3 | $\Lambda^{\rm BH}=0$ inside all tidal 90% CL bounds | all inside | PASS |
| 4 | $h$-blindness: $\lvert R(60)-R(80)\rvert$ at horizon | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/C_gravitational_waves/C09_bh_tidal_love_number
pip install -r requirements.txt
make all
```

Outputs are written to `scripts/outputs/` (claims.csv, samples.csv,
summary.json) and `figures_generated/` (fig_love.png/pdf).
