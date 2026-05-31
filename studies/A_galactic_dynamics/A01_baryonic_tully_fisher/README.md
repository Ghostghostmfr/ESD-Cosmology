# Study 02 — Baryonic Tully–Fisher Relation (zero-parameter reproduction)

Replication of the standalone BTFR paper:

> Higginson, J. P. (2026). *A Zero-Parameter Prediction for the
> Baryonic Tully–Fisher Relation from the Golden-Ratio
> Gravitational Closure.*
> Zenodo. DOI: [10.5281/zenodo.20400008](https://doi.org/10.5281/zenodo.20400008).

Framework reference:

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*

This study reproduces the paper's headline numbers — RMS residual
0.268 dex (ESD) vs 0.283 dex (MOND), mean residual $-0.017$ dex
(ESD) vs $+0.103$ dex (MOND), effective slope $\alpha_{\rm eff}=3.84$
across $N = 129$ SPARC galaxies — using zero free parameters.

The analysis is pure numpy / scipy / matplotlib — no JAX, no
Boltzmann solver.

## Quickstart

```bash
# from the repo root, with esd_core already installed (`pip install -e .`)
cd studies/A01_baryonic_tully_fisher
pip install -r requirements.txt
make all          # fetch + residual analysis + figure
```

Outputs land in `scripts/outputs/`. Figures in `figures_generated/`.

## What reproduces what

| Paper item                            | Script                                  | Make target |
|---------------------------------------|-----------------------------------------|-------------|
| Table 1 (sample summary)              | `scripts/run_btfr_residuals.py`         | `make residuals` |
| §3 deep-regime slope                  | `scripts/run_btfr_residuals.py`         | `make residuals` |
| §4 ESD-vs-MOND residual comparison    | `scripts/run_btfr_residuals.py`         | `make residuals` |
| Headline numbers (RMS, mean, alpha)   | `scripts/outputs/btfr_residuals.{json,txt}` | `make residuals` |
| Fig. `btfr_comparison.png` (2-panel)  | `scripts/make_btfr_residuals_figure.py` | `make fig_residuals` |
| Fig. `G_u_variation.png`              | `scripts/make_btfr_residuals_figure.py` | `make fig_residuals` |

A fast slope-only sanity check is also kept around:

| Slope-only sanity check               | Script                              | Make target |
|---------------------------------------|-------------------------------------|-------------|
| OLS regression, cut-sensitivity scan  | `scripts/run_btfr_test.py`          | `make test_btfr` |
| Single-panel slope figure             | `scripts/make_btfr_figure.py`       | `make fig_btfr` |

## Data

Full SPARC distribution (Lelli, McGaugh & Schombert 2016, AJ 152
157) is fetched on first run and cached locally. Run
`make fetch_rotmod` to populate the cache without running the
analysis.

| File                                  | Source |
|---------------------------------------|--------|
| `data/SPARC_Lelli2016c.mrt`           | http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt |
| `data/Rotmod_LTG/<Galaxy>_rotmod.dat` | http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip |

## ESD prediction (locked, no fit parameters)

The published BTFR paper derives

$$V_f^{\,4} \;=\; \mathcal{G}(u)\;G\,M_b\,a_0,
\qquad
\mathcal{G}(u) \equiv \frac{u\,(1+R(u))^2}{4},
\qquad
u \equiv \frac{4\,g_N}{a_0},$$

with

$$R(u) \;=\; \frac{s}{u^{\,\varphi} + b\,u^{\,q} + c},
\quad
\varphi = \tfrac{1+\sqrt{5}}{2},\;
q = \tfrac{2\ln\varphi}{\varphi},\;
s = 16\varphi+1,\;
b = \varphi^6-2,\;
c = \tfrac{4\ln\varphi-1}{\varphi},$$

and $a_0$ is the framework's derived MOND-scale acceleration
(shared with study 01 via `esd_core.cosmology.a_zero`). In the
deep-MOND asymptote $\mathcal{G}\to 1$, recovering the MOND
relation $V_f^4 = G\,M_b\,a_0$.

For each galaxy we compute the Newtonian acceleration at the
flat-rotation radius from the SPARC mass-model components,

$$V_{\rm bar}^2(r) \;=\; \Upsilon_{\rm disk}\,V_{\rm disk}^2 + \Upsilon_{\rm bul}\,V_{\rm bul}^2 + |V_{\rm gas}|\,V_{\rm gas},
\qquad g_N \;=\; \frac{V_{\rm bar}^2}{r},$$

with $\Upsilon_{\rm disk}=0.5$, $\Upsilon_{\rm bul}=0.7$, taking
the median over the outer 20% of radial bins. The baryonic mass is
$M_b = 0.5\,L_{3.6} + 1.33\,M_{\rm HI}$.

## Acceptance

The runner compares the headline numbers from the published paper
against tolerances:

| Quantity              | Published | Tolerance |
|-----------------------|-----------|-----------|
| $N$ (Q $\le$ 2)       | 129       | $\pm 5$   |
| ESD mean residual     | $-0.017$  | 0.020 dex |
| ESD RMS residual      | $0.268$   | 0.010 dex |
| MOND mean residual    | $+0.103$  | 0.020 dex |
| MOND RMS residual     | $0.283$   | 0.010 dex |
| ESD effective $\alpha$ | $3.84$   | 0.05      |

Exit code 0 if all reproduce within tolerance, 1 if any are off,
3 on data/fit error.

## Paper

See [paper/README.md](paper/README.md) for the arXiv ID, Zenodo DOI,
and BibTeX block.
