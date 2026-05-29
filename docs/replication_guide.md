# Replication Guide

This guide shows how to reproduce any number or figure in any paper
in this repository, end-to-end.

## 1. Choose your path

- **Native Python** — fastest iteration, but you take on dependency
  management. Recommended for users who already maintain a
  scientific-Python stack.
- **Docker** — slower startup, bit-exact reproduction. Recommended
  for reviewers and for archival reproduction.

## 2. Install the shared core

Every study depends on `esd_core/`, the single source of truth for
the locked dimensionless constants and identities of the
Energy-Space-Displacement framework.

```bash
git clone https://github.com/<user>/esd-cosmology.git
cd esd-cosmology
python -m venv .venv && source .venv/bin/activate
pip install -e .[test]
pytest -q esd_core/tests   # sanity check: locked constants match published values
```

If `pytest` fails here, the code and the papers have drifted; open
an issue before going further.

## 3. Run a study

```bash
cd studies/01_linear_cosmology_disco
pip install -r requirements.txt
make all
```

Outputs land in `outputs/`; figures land in `figures_generated/`.

Each study's `README.md` has a table mapping every paper item
(Table 2, Figure 4, etc.) to a single `make` target so you can
reproduce just the result you care about.

## 4. Verify against the paper

Each generated table or figure carries a header comment with the
exact value(s) reported in the paper, plus the relative tolerance
the reproduction is expected to meet. If your local run misses
tolerance, open an issue with the diff and your environment
(`pip freeze`, OS, Python version).

## 5. Reproducing under Docker

```bash
# Build base once
docker build -f docker/base.Dockerfile -t esd-cosmology-base .

# Then per-study:
cd studies/01_linear_cosmology_disco
docker build -t esd-disco .
docker run --rm \
  -v "$PWD/outputs:/work/outputs" \
  -v "$PWD/figures_generated:/work/figures_generated" \
  esd-disco make all
```

The Docker path pins every dependency including the Python
interpreter itself, so output is bit-stable across machines and
across years.
