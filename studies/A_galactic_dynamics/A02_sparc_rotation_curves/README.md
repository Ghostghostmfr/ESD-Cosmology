# Study 03 — SPARC Rotation Curves (zero-parameter reproduction)

Replication of paper 1's *SPARC Benchmark Validation* section:

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: [10.5281/zenodo.19283596](https://doi.org/10.5281/zenodo.19283596).

and of the dedicated rotation-curve companion paper:

> Higginson, J. P. (2026). *Rotation Curve Predictions for 175 SPARC
> Galaxies from the Golden-Ratio Gravitational Closure.*

This study runs the locked golden-ratio closure against MOND
(simple-interpolation reference) at every measured radius of every
SPARC galaxy and reproduces the paper's win / tie / loss tallies and
$\sum\Delta\chi^2$ totals.

The analysis is pure numpy / scipy / matplotlib — no JAX, no
Boltzmann solver. End-to-end runtime on a laptop CPU: $\sim 1$
second for the fits, a few seconds for the figures.

## Quickstart

```bash
# from the repo root, with esd_core already installed (`pip install -e .`)
cd studies/A02_sparc_rotation_curves
pip install -r requirements.txt
make all          # residual analysis + all three figures
```

Outputs land in `scripts/outputs/`. Figures in `figures_generated/`.

## What reproduces what

| Paper item                                  | Script                                  | Make target |
|---------------------------------------------|-----------------------------------------|-------------|
| Per-galaxy $\chi^2$ table                   | `scripts/run_rotation_curves.py`        | `make residuals` |
| W/T/L tally + $\sum\Delta\chi^2$ headline   | `scripts/run_rotation_curves.py`        | `make residuals` |
| Rotation-curve gallery (4 W, 4 T, 4 L)      | `scripts/make_rotation_curves_figures.py` | `make figures` |
| $\Delta\chi^2$ distribution histogram       | `scripts/make_rotation_curves_figures.py` | `make figures` |
| ESD vs MOND reduced-$\chi^2$ scatter        | `scripts/make_rotation_curves_figures.py` | `make figures` |

## Data

The full SPARC distribution (175 rotation-curve files + master MRT,
0.21 MB) is shipped inline at [data/](data/). `make all` runs
fully offline; no network access required.

## ESD prediction (locked, no fit parameters)

At every measured radius $r$ of a SPARC galaxy,

$$V_{\rm bar}^2(r) \;=\; |V_{\rm gas}|\,V_{\rm gas}
                       + \Upsilon_{\rm d}\,|V_{\rm disk}|\,V_{\rm disk}
                       + \Upsilon_{\rm b}\,|V_{\rm bul}|\,V_{\rm bul},
\qquad g_N(r) \;=\; V_{\rm bar}^2(r)\,/\,r,$$

and the predicted circular velocity is

$$V_{\rm pred}(r) \;=\; \sqrt{\, g_N(r)\,\bigl(1 + R(u)\bigr)\,r\,},
\qquad u \;\equiv\; \dfrac{4\,g_N(r)}{a_0},$$

with locked anomalous-acceleration ratio

$$R(u) \;=\; \dfrac{s}{u^{\,\varphi} + b\,u^{\,q} + c},
\quad
\varphi = \tfrac{1+\sqrt{5}}{2},\;
q = \tfrac{2\ln\varphi}{\varphi},\;
s = 16\varphi+1,\;
b = \varphi^6-2,\;
c = \tfrac{4\ln\varphi-1}{\varphi},$$

and $a_0 = 1.2\times 10^{-{10}}\,\mathrm{m\,s^{-2}}$ (paper 1's
literal MOND-scale value; the framework-derived value
$1.2015\times 10^{-{10}}$ from `esd_core.cosmology.a_zero` differs
by $0.13\%$ and produces statistically identical results).

The MOND reference uses the simple interpolation function

$$g_{\rm MOND}(g_N) \;=\; \dfrac{g_N}{1 - \exp(-\sqrt{g_N/a_0})}.$$

## M/L strategies

Paper 1 reports two strategies; this study runs both:

1. **Fixed M/L** (zero per-galaxy parameters): $\Upsilon_{\rm d} = 0.5$,
   $\Upsilon_{\rm b} = 0.7$ (population-synthesis defaults).
2. **Best-fit M/L** from a published $13 \times 9 = 117$-point grid
   in $(\Upsilon_{\rm d},\Upsilon_{\rm b})$. Only the M/L vary —
   the ESD constants $\{p, q, s, b, c\}$ stay locked.

Classification (tie margin $\Delta = 1.0$):

- **W**in: $\Delta\chi^2 \equiv \chi^2_{\rm ESD} - \chi^2_{\rm MOND} < -1$
- **L**oss: $\Delta\chi^2 > +1$
- **T**ie:  $|\Delta\chi^2| \le 1$

## Acceptance

The runner compares against the paper's published numbers:

| Quantity                                                | Published | Tolerance |
|---------------------------------------------------------|-----------|-----------|
| Sample size $N$                                         | 175       | $\pm 2$   |
| Grid M/L — wins                                         | 53        | $\pm 2$   |
| Grid M/L — losses                                       | 24        | $\pm 2$   |
| Grid M/L — ties                                         | 94 ($^*$) | $\pm 6$   |
| Grid M/L — $\sum\Delta\chi^2$                           | $-843$    | $\pm 30$  |
| Fixed M/L — wins                                        | 73        | $\pm 2$   |
| Fixed M/L — ties                                        | 55        | $\pm 6$   |
| Fixed M/L — losses                                      | 47        | $\pm 2$   |
| Fixed M/L — $\sum\Delta\chi^2$                          | $-588$    | $\pm 30$  |
| Fixed M/L — galaxies with $\chi^2_\nu({\rm ESD}) < \chi^2_\nu({\rm MOND})$ | 110 | $\pm 5$ |

$^*$ Paper 1 runs its head-to-head on 171 late-type galaxies
(4 early-type excluded). This study runs on all 175 and inherits
$\sim\!4$ extra ties; W and L counts and $\sum\Delta\chi^2$ are
unaffected at the listed tolerance.

Exit code 0 if all reproduce within tolerance, 1 if any are off,
3 on data error.

## Paper

See [paper/README.md](paper/README.md) for citation metadata.
