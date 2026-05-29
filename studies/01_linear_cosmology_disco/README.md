# Study 01 — Linear-Cosmology and Galactic-Dynamics Closure

Replication package for:

> Higginson, J. P. (2026). *ESD Framework: Linear-Cosmology and
> Galactic-Dynamics Closure of the Zero-Parameter Golden-Ratio
> Cosmology.*

This package regenerates every table and figure in the paper from
the locked constants exposed by `esd_core/` plus the linear-cosmology
solver runs (DISCO-EB).

## Quickstart

```bash
# from the repo root, with esd_core already installed (see top-level README)
cd studies/01_linear_cosmology_disco
pip install -r requirements.txt
make all
```

Outputs land in `outputs/`. The figure files are written into
`figures_generated/`.

## What reproduces what

| Paper item            | Script                                      | Make target  |
|-----------------------|---------------------------------------------|--------------|
| Table 2 (locked params) | `scripts/phase1_locked_constants.py`     | `make table2`|
| §2.4 Phase 2a P(k)    | `scripts/phase2a_pk_residual.py`            | `make phase2a` |
| §3.x Step 1 audit     | `scripts/step01_dfield_constants_audit.py`  | `make step01` |
| ...                   | (see Makefile for the full list)            |              |
| Figure 1 (CMB peak)   | `scripts/step19_cmb_peak_ratio.py` + `scripts/make_step19_figure.py` | `make fig_cmb_peak` |
| Figure 4 (BAO Route A)| `scripts/step08_routeA_bao.py`              | `make fig_bao` |
| Figure 5 (shear shape)| `scripts/step08_routeB_shear_shape.py`      | `make fig_shear` |

(The exact script names will be locked in during the port from
`Research/Modeling/disco_eb_esd/` into this package — placeholder
until the audit pass completes.)

## Docker

```bash
# from the repo root, after building the base image
cd studies/01_linear_cosmology_disco
docker build -t esd-disco .
docker run --rm -v "$PWD/outputs:/work/outputs" \
                -v "$PWD/figures_generated:/work/figures_generated" \
                esd-disco make all
```

## Paper

See [`paper/README.md`](paper/README.md) for the arXiv ID, Zenodo DOI,
and citation block.
