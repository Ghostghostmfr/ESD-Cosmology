# Study 06 — CMB & LSS lock audit (cross-survey tension table)

Closed-form audit: every reading-independent framework lock is
compared to the published constraint from Planck 2018, KiDS-1000,
DES Y3, SH0ES, BBN (Cooke+2018), BICEP/Keck-21, and McGaugh+2016.
See [paper/README.md](paper/README.md) for the full citations.

Unlike Studies 02–05, this study has **no data download and no
fit** — it is purely a tension/pull table from numbers the framework
already commits to. It runs in milliseconds.

## Quickstart

```bash
# from the repo root, with esd_core already installed (pip install -e .)
cd studies/F02_cmb_lss_tension_audit
pip install -r requirements.txt
make all          # audit + figures
```

Outputs land in [scripts/outputs/](scripts/outputs/);
figures in [figures_generated/](figures_generated/).

## What gets audited

| Observable      | Lock source                          | Surveys compared against        |
|-----------------|--------------------------------------|---------------------------------|
| $\Omega_m$, $\Omega_\Lambda$ | Identity A (`esd_core`)    | Planck 2018                     |
| $\Omega_b$ (both readings)   | Identity B (`esd_core`)    | Planck 2018, BBN (Cooke+2018)   |
| $\Omega_{DM}$ (both readings)| Identity B (`esd_core`)    | Planck 2018                     |
| $\omega_b h^2$               | $\Omega_b h^2$             | Planck 2018, BBN                |
| $n_s$           | $1 - 2/N_*$ (`esd_core.primordial`)  | Planck 2018                     |
| $\alpha_s$      | $-2/N_*^2$                           | Planck 2018                     |
| $r$ (tensor/scalar) | $12/N_*^2$                       | BICEP/Keck-21 (95 % UL)         |
| $A_s$           | COBE anchor (external)               | Planck 2018                     |
| $H_0$           | Planck-anchored 67.36                | Planck 2018, SH0ES              |
| $S_8$, $\sigma_8$ | Study 01 / CLASS at locked inputs  | Planck 2018, KiDS-1000, DES Y3  |
| $a_0$           | Study 04 / Identity-B locked         | McGaugh+2016                    |

## Acceptance gate

`scripts/run_cmb_lss_audit.py` returns exit 0 iff every
reading-independent lock is within **2 σ** of the *Planck 2018* central
value. KiDS-1000 / DES Y3 / SH0ES pulls are reported for transparency
but do not gate — they ARE the live cosmological tensions, and any
framework's job is to either resolve them or be honest about which
side of each tension it sits on.

## Two figures

- [`fig_S8_Om_tension`](figures_generated/fig_S8_Om_tension.pdf) —
  the framework lock plotted as a star on the $(\Omega_m, S_8)$ plane
  alongside the 1 σ ellipses of Planck, KiDS-1000, and DES Y3.
- [`fig_pull_bars`](figures_generated/fig_pull_bars.pdf) — signed
  $(lock - mean)/\sigma$ across every (survey, observable) pair.

## Notes

- $S_8 = 0.830426$ is hard-coded with provenance pointer back to
  [Study 01's `compute_s8.py`](../F01_linear_cosmology_closure/scripts/compute_s8.py).
  This study deliberately does not require CLASS installed.
- The framework lives close to Planck on every locked observable and
  sits between Planck and KiDS-1000/DES Y3 on $S_8$ — i.e. it sits on
  the high-$S_8$ side of the well-known weak-lensing tension.
