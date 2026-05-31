# Simulations

Simulation-class studies for the Energy-Space-Displacement (ESD)
framework. Same public-repo conventions as `studies/`: every
sub-folder is fully self-contained, reproducible from `make all`,
and pulls every locked constant from `esd_core/`.

Where `studies/` does **closed-form prediction vs one survey**,
`simulations/` does **end-to-end numerical evolution**: N-body,
semi-analytic galaxy formation, cosmic-web topology, halo merger
trees, etc.

## Why this section exists

ΛCDM's credibility chain runs through Millennium (2005),
IllustrisTNG, EAGLE, and FIRE. ESD has, to date, zero studies of
that class. This section closes that gap.

## Index

| #  | Title                                                           | Status     |
|----|-----------------------------------------------------------------|------------|
| 01 | [D-field N-body simulation (mini-Millennium analog)](01_dfield_nbody/) | Scaffold |

## Conventions

Identical to `studies/`. Read [`../docs/adding_a_study.md`](../docs/adding_a_study.md)
for the full rules. The only addition for simulations is:

* **`snapshots/`** — per-step particle/grid dumps. Auto-ignored by
  the parent `.gitignore`. Use `snapshots/large/` for anything above
  100 MB.
* **`scripts/run_sim.py`** is the canonical entry point. Each
  `make` target either runs `run_sim.py` with different flags, or
  runs an analysis script that consumes existing snapshots.
* **Determinism gate** — every simulation must expose a `--seed`
  flag and a regression test that hashes a small fiducial run.

## Hardware notes (development machine)

* GPU: NVIDIA RTX 5090 (CUDA, JAX-friendly).
* CPU: avoid heavy parallel CPU work to limit thermal load — prefer
  GPU offload for the dominant solver step.
