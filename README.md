# ESD — Energy–Space–Displacement

A classical unified field theory. A single covariant parent action and
five φ-locked closure constants carry one D/E/S channel grammar from
gravity to galaxies. Zero per-sector fit parameters once *G* and *H*₀
are fixed. Reproduction studies + theory derivations, all falsifiable.

---

## About

The frameworks parent action (below)
places the metric $g_{\mu\nu}$, the displacement scalar $D$, and the
electromagnetic potential $A_\mu$ under one Lagrangian, fed by a fixed
**closure pool** of five constants — all anchored on the golden ratio.


$$
\mathcal{S}_{\mathrm{ESD}}=\int d^4x\sqrt{-g}\left[\frac{R-2\Lambda_{\mathrm{eff}}}{16\pi G}-\frac{\alpha X_0}{2}\mathcal{F}(X/X_0)-V(D)-\tfrac14 Z(D)F_{\mu\nu}F^{\mu\nu}\right]+S_m[A^2(D)g_{\mu\nu},\psi_m]
$$


Fixed **closure pool** of the five constants:
| symbol | value | role |
|---|---|---|
| $\phi$ | $(1+\sqrt5)/2$ | discrete scaling, hierarchy clock |
| $q$ | $2\ln\phi/\phi \approx 0.5950$ | bridge / transition exponent |
| $c$ | $(4\ln\phi-1)/\phi \approx 0.5716$ | irreducible floor |
| $b$ | $\phi^6-2 \approx 15.944$ | rung-selected amplitude |
| $s$ | $16\phi+1 \approx 26.889$ | full-closure readout |

Together they assemble the screening form

$$
R(u)=\frac{s}{u^{\phi}+b\,u^{q}+c}, \qquad u=4g/a_0
$$

and three carrier channels — Displacement (anchor / drive),
Energy (bridge / transfer), Space (floor / completion) — that carry the
same grammar from cosmological scales down through galactic dynamics.

**What the framework is not:** a theory of everything, a
completed quantum-gravity derivation, a replacement for
observational studies/data. 

This repository is the cosmology slice — the gravitational and
large-scale-structure track of the full framework.

---

## What's in this repo

The repo has two parallel tracks: **reproduction studies** and
**theory derivations**. Each lives in a numbered folder, ships its
own audit and figures, and pulls every constant from one shared
`esd_core/` package.

- A **reproduction study** (`studies/NN_<name>/`) takes one
  published observational dataset or empirical relation and checks
  it against ESD's locked predictions — *no fitting, no tuning*.
  The audit is a pass/fail gate: either the dataset lies inside the
  framework's grammar or it doesn't.
- A **theory derivation** (`theory/NN_<name>/`) applies Paper 1's
  axioms (A1: bound-system locality, A2: acceleration definedness,
  A3: closure universality) to a regime the reproduction studies
  don't directly cover, and ships an audit that certifies whether
  the screening form *R(u)* applies, what it predicts, and — when
  honest — where the framework declines to make a prediction at all.

### `studies/` — reproduction studies (21)

| #  | study | domain |
|----|-------|--------|
| 01 | `01_linear_cosmology_disco`  | linear cosmology + galactic dynamics closure |
| 02 | `02_btfr`                    | baryonic Tully–Fisher relation |
| 03 | `03_sparc_rotation_curves`   | SPARC galaxy rotation curves |
| 04 | `04_a0_derivation`           | derivation of the MOND acceleration scale |
| 05 | `05_rar`                     | radial-acceleration relation |
| 06 | `06_cmb_lss_lock_audit`      | CMB + LSS consistency lock |
| 07 | `07_desi_y1_bao`             | DESI Y1 BAO |
| 08 | `08_hubble_tension`          | *H*₀ tension audit |
| 09 | `09_gw_propagation`          | GW170817 propagation speed |
| 10 | `10_cluster_ratio`           | cluster mass ratios |
| 11 | `11_lyalpha_jeans`           | Lyman-α / Jeans scale |
| 12 | `12_a0_anchor`               | independent *a*₀ anchor cross-check |
| 13 | `13_jwst_highz`              | JWST high-*z* galaxies |
| 14 | `14_wide_binaries`           | wide-binary acceleration test |
| 15 | `15_bullet_cluster`          | Bullet Cluster offset |
| 16 | `16_udg_dmfree`              | DM-free ultra-diffuse galaxies |
| 17 | `17_eht_shadows`             | EHT black-hole shadows |
| 18 | `18_s8_tension`              | *S*₈ tension |
| 19 | `19_growth_derivation`       | growth-of-structure derivation |
| 20 | `20_redshift_derivation`     | cosmological-redshift derivation |
| 21 | `21_gw_derivation`           | gravitational-wave sector derivation |

### `theory/` — applicability-theorem derivations

| #  | track | result |
|----|-------|--------|
| 01 | `01_bh_relational`  | black-hole horizons sit deep in *R(u)* ≪ 1; *S*ᴮᴴ unchanged |

### `esd_core/` — shared locked-constant package

Every study imports the closure pool, the kernel, and the locked
identities from one editable package, so no two studies can silently
drift apart.

---

## Suite status

**64 / 64 audits passing.**

- 44 reproduction gates across `studies/01–18`
- 12 derivation gates across `studies/19–21`
- 8 theory gates in `theory/01_bh_relational`

Honest negatives are reported in-place when the framework declines
to make a prediction. See each study's `scripts/outputs/*.json`.

---

## Quickstart

```bash
git clone https://github.com/<user>/esd-cosmology.git
cd esd-cosmology
python -m venv .venv
# Windows:  .venv\Scripts\Activate.ps1
# POSIX:    source .venv/bin/activate
pip install -e .                          # installs esd_core

# run any study
cd studies/05_rar
pip install -r requirements.txt
make all                                   # regenerates tables and figures

# run any theory derivation
cd ../../theory/01_bh_relational
pip install -r requirements.txt
make all
```

Docker images for bit-exact reproduction live under `docker/`.

---

## Repository layout

```
esd-cosmology/
├── esd_core/              shared locked constants and identities
├── studies/NN_<name>/     one self-contained reproduction per folder
├── theory/NN_<name>/      applicability-theorem derivations
├── docker/                shared base image
├── docs/                  replication guide
└── .github/workflows/     CI smoke tests
```

Each `studies/*/` and `theory/*/` folder follows the same convention:
`scripts/` (audit + figures), `scripts/outputs/` (JSON + CSV
artifacts), `paper/` (write-up), `Makefile`, `requirements.txt`.

---

## Citation

See [`CITATION.cff`](CITATION.cff) for the canonical citation block.
Each study's `paper/README.md` carries the paper-specific DOI once
assigned.

---

## License

See [`LICENSE`](LICENSE).
