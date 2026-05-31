# Study 04 — $a_0$ derivation (zero-parameter reproduction)

Replication of the standalone ESD-framework supporting paper that
derives the MOND acceleration constant $a_0$ from first principles
(see [paper/README.md](paper/README.md) for the full citation).

This study has **no data download** — $a_0$ is a closed-form
prediction from the locked Identity B and Planck cosmological
parameters. The entire reproduction runs in milliseconds.

## Quickstart

```bash
# from the repo root, with esd_core already installed (pip install -e .)
cd studies/A03_a0_first_principles
pip install -r requirements.txt
make all          # derivation + figures
```

Outputs land in [scripts/outputs/](scripts/outputs/);
figures in [figures_generated/](figures_generated/).

## What reproduces what

| Paper item                                                                | Script                                | Make target |
|---------------------------------------------------------------------------|---------------------------------------|-------------|
| Eq. `a0_main` — closed-form $a_0$ expression                              | `scripts/esd_a0.py`                   | (library)   |
| Eq. `a0_num` — coefficient 0.18288 and $a_0 = 1.198\times10^{-10}$ m/s²   | `scripts/run_a0_derivation.py`        | `make derivation` |
| Sec. *Sensitivity scan* — best-fit $f_b = 0.354$ to RAR canonical         | `scripts/run_a0_derivation.py`        | `make derivation` |
| Residuals at $f_b = 1/3$ ($-0.17\,\%$) and $f_b = 1/2$ ($+1.26\,\%$)       | `scripts/run_a0_derivation.py`        | `make derivation` |
| Fig. 1 — $f_b$ sensitivity scan                                            | `scripts/make_a0_figures.py`          | `make figures`    |
| Bonus: $a_0(H_0)$ across the Planck / SH0ES range                          | `scripts/make_a0_figures.py`          | `make figures`    |

## Two reading-modes

`scripts/esd_a0.py` exposes two equivalent ways to compute $a_0$:

- **paper mode** — direct Planck means $\Omega_{DM} = 0.264$,
  $\Omega_b = 0.049$. Gives the standalone-paper headline
  $a_0(67.4) = 1.198\times10^{-10}$ m/s² and coefficient $0.18288$.
- **framework mode** — uses Identity B's closure
  $8\pi c^4 \Omega_m$, exported as `esd_core.cosmology.a_zero`.
  Gives the slightly different combination
  $3\Omega_{DM}+\Omega_b = 0.847$, coefficient $0.18358$, and
  $a_0(67.4) = 1.2022\times10^{-10}$ m/s² — closer still to the
  McGaugh canonical $1.20\times10^{-10}$.

Both are reading-independent in the sense of
[`esd_core.identities`](../../../esd_core/identities.py); they differ
only in whether $(\Omega_{DM},\Omega_b)$ are fed in from Planck
directly or routed through Identity B's algebraic closure.

## Acceptance gate

`scripts/run_a0_derivation.py` returns exit code 0 iff every
headline number in the paper reproduces within the tolerances
declared at the top of that file. Closed-form predictions are
checked to ~$5 \times 10^{-13}$ m/s² (~0.04 % of $a_0$).
