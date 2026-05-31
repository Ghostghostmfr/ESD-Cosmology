# Simulation 01 — D-field N-Body (mini-Millennium analog)

Replication package for the first full cosmological N-body run of the
Energy-Space-Displacement (ESD) framework.

> Higginson, J. P. (2026). *ESD Framework: Non-Linear Structure
> Formation from a Locked D-Field N-Body Simulation.* (in preparation)

## What this is

A particle-mesh (PM) cosmological simulation that evolves a
collisionless dark-matter-equivalent fluid under the **ESD-modified
Poisson equation**

```
nabla^2 Phi = 4 pi G rho_eff [1 + R(u)]
```

where `R(u) = s / Sigma(u)` is the closure-pool kernel from
`esd_core/`, exposed by Theory 01. No new tunable parameters; every
constant comes from `esd_core/`.

## Why this is a one-of-a-kind study

* ESD has 24 closed-form-prediction studies. This is its **first**
  end-to-end simulation.
* Closes the simulation-class gap relative to ΛCDM's Millennium,
  IllustrisTNG, EAGLE, FIRE.
* Output snapshots feed every downstream simulation (02_galform_pipeline,
  03_cosmic_web_topology, …) so this is the canonical foundation run.

## Quickstart

```bash
cd simulations/01_dfield_nbody
pip install -r requirements.txt
make all
```

Outputs land in `outputs/` (CSV tables, summary numbers) and
`figures_generated/` (PNG/PDF). Particle snapshots land in
`snapshots/` (auto-ignored by git).

## What reproduces what

| Paper item                  | Script                             | Make target          |
|----------------------------|------------------------------------|----------------------|
| Initial conditions (IC)     | `scripts/ic_zeldovich.py`         | `make ic`            |
| Modified-Poisson PM solver  | `scripts/run_sim.py`              | `make sim`           |
| Halo finder (FOF)           | `scripts/find_halos.py`           | `make halos`         |
| Halo mass function          | `scripts/halo_mass_function.py`   | `make hmf`           |
| Two-point ξ(r)              | `scripts/two_point_xi.py`         | `make xi`            |
| Density profile (NFW vs ESD)| `scripts/halo_profile.py`         | `make profile`       |

(Script names are placeholders until each sub-task is built.)

## Status

| Sub-task | Description                                | Status      |
|----------|--------------------------------------------|-------------|
| 1.1      | PM solver skeleton (FFT-based, GR baseline)| not started |
| 1.2      | ESD modification: `1 + R(u)` source        | not started |
| 1.3      | Zel'dovich initial conditions              | not started |
| 1.4      | FOF halo finder                            | not started |
| 1.5      | Halo mass function (Press–Schechter compare)| not started |
| 1.6      | Two-point correlation ξ(r)                 | not started |
| 1.7      | Density profile (NFW vs ESD)               | not started |

Tackle one sub-task per session. Sub-task 1.1 (GR-baseline PM solver)
is the first concrete piece; ESD modification (1.2) is bolted on top
after 1.1 reproduces a Newtonian baseline at small box size.

## Hardware

* Target: 50 h⁻¹ Mpc box, 256³ particles (~17M).
* GPU: RTX 5090 via JAX (cuda backend) — dominant solver step is the
  PM FFT, which is GPU-bound. CPU steps (FOF, IO) kept serial to
  avoid thermal load.
* Wall time target (full run, 50 steps a=0.02→1.0): ≤ 30 min on 5090.

## Citation

`[HigginsonESDFramework2026]`.
