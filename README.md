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

The repo has three parallel tracks: **reproduction studies**,
**theory derivations**, and **simulations**. Each lives in a
numbered folder, ships its own audit and figures, and pulls every
constant from one shared `esd_core/` package.

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
- A **simulation** (`simulations/NN_<name>/`) takes the locked
  kernel into end-to-end numerical evolution (N-body,
  stream-spray, etc.) where the closed-form studies stop. Same
  reproducibility contract: `make all`, deterministic `--seed`,
  every constant from `esd_core/`.

### `studies/` — reproduction studies (66)

Studies are grouped by physical regime.

#### A — Galactic Dynamics & MOND-scale tests

| #  | study | domain |
|----|-------|--------|
| 02 | `A01_baryonic_tully_fisher`                    | baryonic Tully–Fisher relation |
| 03 | `A02_sparc_rotation_curves`   | SPARC galaxy rotation curves (175 galaxies, zero-parameter) |
| 04 | `A03_a0_first_principles`           | derivation of the MOND acceleration scale |
| 05 | `A04_radial_acceleration_relation`                     | radial-acceleration relation |
| 12 | `A05_a0_multi_tracer_anchor`               | independent *a*₀ anchor cross-check |
| 14 | `A06_wide_binary_acceleration`           | wide-binary acceleration test |
| 16 | `A07_dm_free_galaxies`              | DM-free ultra-diffuse galaxies |
| 48 | `A08_esd_vs_mond_verdict`             | **ESD vs MOND: formal statistical verdict** (Δχ²=−843, W/T/L=53/98/24) |
| 49 | `A09_dwarf_spheroidal_kinematics`     | MW classical dSph σ_los under EFE (Walker+, McConnachie) |
| 50 | `A10_udg_broader_kinematics`          | UDG kinematics under EFE (DF2/DF4/NGC5846-UDG1/DF44) |
| 51 | `A11_local_group_timing_argument`     | Local Group timing-argument mass (Kahn–Woltjer) |
| 54 | `A12_hi_dwarf_rotation`               | HI-dominated dwarf BTFR (WLM, DDO 154) |

#### B — Solar System & Local Gravity

| #  | study | domain |
|----|-------|--------|
| 27 | `B01_equivalence_principle_microscope`          | MICROSCOPE 2022 weak-equivalence-principle bound (Pt–Ti) |
| 33 | `B02_solar_system_ppn`        | solar-system PPN bounds (Cassini γ, LLR β, Mercury) |
| 55 | `B03_pulsar_timing_double_triple`     | strong-field pulsar timing (J0737 + J0337 SEP) |
| 56 | `B04_s2_orbit_sgra`                   | S2 Schwarzschild precession at Sgr A* |
| 57 | `B05_stellar_asteroseismology_null`   | stellar-interior NULL (solar Δν + Sirius B v_gr) |
| 60 | `B06_inverse_square_law_lab`          | tabletop inverse-square-law (Eöt-Wash, HUST) |

#### C — Gravitational Waves & Multi-Messenger

| #  | study | domain |
|----|-------|--------|
| 09 | `C01_gravitational_wave_speed`          | GW170817 propagation speed |
| 21 | `C02_gravitational_wave_applicability`           | gravitational-wave sector derivation |
| 23 | `C03_nanograv15_stochastic_background`  | NANOGrav 15-yr stochastic GW background |
| 40 | `C04_standard_sirens_h0`      | standard-siren *H*₀ (GW170817 + dark sirens GWTC-3, LVK O4a, ET/CE forecast) |
| 58 | `C05_bh_ringdown_qnm`         | BH ringdown 220-mode (Isi+ 2019 GW150914) |
| 61 | `C06_gw_friction_running_mp`  | GW friction / running Planck mass (Mukherjee+ 2021 LVK O3) |
| 62 | `C07_ns_tidal_deformability`  | NS tidal deformability λ̃ (GW170817 LVC 2018) |
| 63 | `C08_bh_spin_kerr_extremality`| BH spin distribution + Thorne bound (X-ray reflection, GWTC-3) |
| 64 | `C09_bh_tidal_love_number`    | BH tidal Love number *k*₂=0 (Kerr null; GW170817/GW190425 bounds) |
| 65 | `C10_bh_ringdown_echoes`      | BH ringdown echoes (absorbing-horizon null; Abedi+ 2017, Westerweck+ 2018, LVK TGR) |
| 66 | `C11_bh_scalar_qnm`           | BH scalar quasi-normal modes (no-hair null; GW170814 pol., Isi+ 2019, GWTC-3) |

#### D — Clusters, Halos & Compact Objects

| #  | study | domain |
|----|-------|--------|
| 10 | `D01_cluster_mass_ratio_c4`           | cluster mass ratios |
| 15 | `D02_bullet_cluster_mergers`          | Bullet Cluster offset |
| 17 | `D03_eht_black_hole_shadows`             | EHT black-hole shadows |
| 36 | `D04_cluster_mass_function`   | cluster HMF *n*(*M*, *z*) (eROSITA, SPT, ACT, Planck SZ) |
| 43 | `D05_hydrostatic_mass_bias`   | hydrostatic mass bias 1−*b*_H (CCCP, WtG, LoCuSS, CLASH, HSC, SPT-WL, eROSITA-DE) |
| 44 | `D06_splashback_radius`       | splashback radius *R*ₛₚ/*R*₂₀₀ₘ (SDSS+DES+ACT+HSC; falsifies chameleon) |
| 52 | `D07_strong_lens_einstein_radius_function` | SLACS Einstein-radius function (Bolton+, Auger+ Chabrier-IMF) |
| 59 | `D08_nicer_ns_mass_radius`    | NICER NS mass–radius (J0030, J0740, J0437) |

#### E — Cosmological Background & Expansion History

| #  | study | domain |
|----|-------|--------|
| 07 | `E01_desi_y1_bao`             | DESI Y1 BAO |
| 08 | `E02_hubble_tension_h0`          | *H*₀ tension audit |
| 20 | `E03_cosmological_redshift_derivation`     | cosmological-redshift derivation |
| 22 | `E04_dark_energy_w0wa`      | DESI Y1 BAO + Planck CMB *w*₀-*w*ₐ joint test |
| 31 | `E05_strong_lensing_time_delays` | H0LiCOW / TDCOSMO time-delay *H*₀ |
| 41 | `E06_pantheon_plus_snia`      | Pantheon+ SN Ia μ(*z*) residuals (Brout+ 2022, Scolnic+ 2022) |
| 42 | `E07_cosmic_chronometers`  | cosmic-chronometer *H*(*z*) (Moresco+ compilation, 32 model-independent points) |
| 47 | `E08_peculiar_velocities_cosmicflows4`         | Cosmicflows-4 peculiar-velocity *fσ*₈(*z*≈0) (6dFGSv, 2MTF, SDSS PV, SFI++/A2, 2M++, CF-3/4) |
| 53 | `E09_bbn_primordial_abundances` | BBN D/H + Y_p under both Identity B readings (Cooke+ 2018, Aver+ 2021) |

#### F — CMB, LSS & Linear Regime

| #  | study | domain |
|----|-------|--------|
| 01 | `F01_linear_cosmology_closure`  | linear cosmology + galactic dynamics closure |
| 06 | `F02_cmb_lss_tension_audit`      | CMB + LSS consistency lock |
| 11 | `F03_lyman_alpha_jeans_scale`           | Lyman-α / Jeans scale |
| 13 | `F04_jwst_high_z_galaxies`              | JWST high-*z* galaxies |
| 18 | `F05_weak_lensing_s8_tension`              | *S*₈ tension |
| 19 | `F06_linear_growth_s8_prediction`       | growth-of-structure derivation |
| 24 | `F07_act_dr6_cmb_lensing`         | ACT DR6 CMB lensing *S*₈ᶜᴹᴮᴸ consistency |
| 34 | `F08_eg_gravitational_slip`   | *E*_G(*z*) gravitational-slip statistic (Reyes+, Blake+, Singh+, …) |
| 35 | `F09_isw_cross_correlation`        | ISW × galaxy cross-correlation (Planck × NVSS/2MASS/WISE/DESI) |
| 37 | `F10_ksz_pairwise_velocity` | kSZ pairwise-velocity amplitude (ACT/SPT × BOSS/DES/DESI) |
| 38 | `F11_primordial_tensor_ratio`     | primordial tensor-to-scalar ratio *r* (BICEP/Keck, LiteBIRD, CMB-S4) |
| 39 | `F12_rsd_growth_rate`             | RSD *fσ*₈(*z*) compilation (6dFGS, BOSS, eBOSS, DESI Y1) |
| 45 | `F13_scale_dependent_galaxy_bias`    | scale-dependent linear bias *b*(*k*) (BOSS DR12, eBOSS, DESI DR1; falsifies *f*(*R*)/DGP) |
| 46 | `F14_des_y3_modified_gravity`         | phenomenological MG (μ₀, Σ₀) (Planck, DES Y3, KiDS-1000, DES Y1, CFHTLenS) |

#### G — Anomalies, Tensions & Open Falsifiers

| #  | study | domain |
|----|-------|--------|
| 25 | `G01_cosmic_radio_ir_dipole`           | NVSS / CatWISE2020 source-count dipole vs CMB kinematic dipole |
| 26 | `G02_cmb_cosmic_birefringence`       | Eskilt & Komatsu 2023 isotropic cosmic-birefringence anomaly |
| 28 | `G03_satellite_plane_anomaly`     | MW VPOS / M31 GPoA / Cen A satellite-plane alignment |
| 29 | `G04_cmb_low_multipole_anomalies`             | Planck 2018 low-ℓ anomaly bundle (C₂, quad–oct, hemispherical) |
| 30 | `G05_cosmic_void_lensing`            | void abundance + void-lensing convergence (BOSS / DES Y3) |
| 32 | `G06_21cm_cosmic_dawn`        | EDGES / SARAS-3 cosmic-dawn 21-cm absorption |

### `theory/` — applicability-theorem derivations (3)

| #  | track | result |
|----|-------|--------|
| 01 | `01_bh_relational`            | black-hole horizons sit deep in *R(u)* ≪ 1; *S*ᴮᴴ unchanged |
| 02 | `02_vacuum_lambda`            | (A1)+(A2) fail for the vacuum → *R(u)* does **not** modify Λ; 10/10 claims |
| 03 | `03_dfield_horizon_gradient`  | super-horizon D-gradient ansatz unifying studies 25, 28, 29 (one *ĝ*, three faces); honest η-amplitude gap in §7 |

### `simulations/` — end-to-end numerical evolution

| #  | track | scope |
|----|-------|-------|
| 01 | `01_dfield_nbody`    | particle-mesh cosmological N-body under the ESD-modified Poisson equation (mini-Millennium analog) |
| 02 | `02_tidal_streams`   | GD-1 / Sagittarius / Pal 5 stream morphology, ESD vs GR discrimination in the MW halo |

### `esd_core/` — shared locked-constant package

Every study imports the closure pool, the kernel, and the locked
identities from one editable package, so no two studies can silently
drift apart.

---

## Suite status

**66 reproduction studies + 3 theory derivations + 2 simulations.**
Of the 66 studies, 64 land at PASS against published data, one is a
partial closure (Study 30, cosmic-void lensing — kernel passes, the
HSW analytic profile saturates; needs a full ESD void solve), and one
is an open falsifier under active tension (Study 26, CMB cosmic
birefringence — ESD predicts β=0 exactly, PR4+WMAP reports
0.342°±0.094° at 3.6σ; independent radio-galaxy CPR limits ≲1° side
with β=0). Study-specific gate definitions are documented in each
folder's `README.md`.

**Reproduction studies (`studies/`).**  Studies are grouped into seven
physical-regime bands (A–G).

- **Group A (Galactic Dynamics & MOND-scale):** Studies 02, 03, 04,
  05, 12, 14, 16, 48. The core rotation-curve, BTFR, RAR, wide-binary,
  and DM-free-UDG tests. Study 48 is the dedicated ESD vs MOND head-to-head
  verdict (Δχ²=−843, W/T/L=53/98/24 across 175 SPARC galaxies).
- **Group B (Solar System & Local Gravity):** Studies 27, 33. PPN
  bounds and WEP.
- **Group C (Gravitational Waves & Multi-Messenger):** Studies 09, 21,
  23, 40, 58, 61, 62, 63, 64, 65, 66. Propagation speed, GW-sector
  derivation, NANOGrav, standard-siren *H*₀, ringdown 220-mode, GW
  friction, NS tidal deformability, BH spin, and the strong-field BH
  null suite — tidal Love number (*k*₂=0), ringdown echoes, and scalar
  quasi-normal modes.
- **Group D (Clusters, Halos & Compact Objects):** Studies 10, 15, 17,
  36, 43, 44. Mass ratios, Bullet Cluster, EHT, HMF, hydrostatic bias,
  and splashback (chameleon falsifier).
- **Group E (Cosmological Background & Expansion History):** Studies 07,
  08, 20, 22, 31, 41, 42, 47. BAO, *H*₀ tension, SN Ia, *H*(*z*),
  peculiar velocities, and strong-lens time delays.
- **Group F (CMB, LSS & Linear Regime):** Studies 01, 06, 11, 13, 18,
  19, 24, 34, 35, 37, 38, 39, 45, 46. Linear growth, CMB lensing,
  *E*_G, ISW, kSZ, RSD *fσ*₈, tensor-to-scalar ratio, and
  phenomenological MG parameters. In this regime ESD = ΛCDM identically
  (Study 19 applicability theorem); the framework's locked Ω_m = 0.31574
  and σ₈ = 0.8111 are inherited from Planck CMB via Identity B.
- **Group G (Anomalies, Tensions & Open Falsifiers):** Studies 25, 26,
  28, 29, 30, 32. Cosmic dipole, CMB birefringence, satellite planes,
  low-ℓ power, void lensing, 21-cm cosmic dawn.

**Three structural categories** carry the predictions:

- **Linear-regime ESD = ΛCDM** (Study 19 applicability theorem):
  Studies 18, 19, 20, 24, 34, 35, 37, 39, 40, 41, 42, 45, 46, 47
  (linear growth, CMB lensing, *E*_G, ISW, kSZ, RSD, sirens, SN μ(*z*),
  *H*(*z*), b(k), μ₀/Σ₀, peculiar velocities). ESD reproduces ΛCDM
  identically with no new parameters; the framework's locked
  Ω_m = 0.31574 and σ₈ = 0.8111 are inherited from Planck CMB via
  Identity B.
- **Bound-system R(u) acts** (A1, A2, A3 all satisfied): Studies 02,
  03, 04, 05, 10, 14, 16, 33, 36, 43, 44, 48 (galaxies, clusters, solar
  system, hydrostatic mass, splashback, ESD vs MOND head-to-head).
  Forward-falsifiable departures from GR/ΛCDM where the closure-pool
  kernel enhances *G*_eff and shifts collapse thresholds.
- **Honest negatives / open falsifiers**: `theory/03` super-horizon
  D-gradient amplitude η (8-order gap under naive Starobinsky
  embedding — needs screening or non-inflationary source, see §7
  of that folder); `theory/02` Λ_vacuum (R(u) shown NOT to act).

**Theory derivations (`theory/01-03`).** `theory/01_bh_relational`
(*S*ᴮᴴ unchanged, R(u) ≪ 1 deep inside horizons; 8/8 gates).
`theory/02_vacuum_lambda` (10/10; R(u) does not act on Λ).
`theory/03_dfield_horizon_gradient` (unifying studies 25, 28, 29
through one *ĝ*; honest η-amplitude gap in §7).

**Simulations (`simulations/01-02`).** `simulations/01_dfield_nbody`
(particle-mesh cosmological N-body, mini-Millennium analog).
`simulations/02_tidal_streams` (GD-1, Sagittarius, Pal 5 stream
morphology in the MW halo).

Honest negatives are reported in-place when the framework declines
to make a prediction. See each study's `scripts/outputs/*.json`.

---

## Quickstart

```bash
git clone https://github.com/ghostghostmfr/esd-cosmology.git
cd esd-cosmology
python -m venv .venv
# Windows:  .venv\Scripts\Activate.ps1
# POSIX:    source .venv/bin/activate
pip install -e .                          # installs esd_core

# run any study (studies are grouped by physical regime)
cd studies/A_galactic_dynamics/A04_radial_acceleration_relation
pip install -r requirements.txt
make all                                   # regenerates tables and figures

# run any theory derivation
cd ../../../theory/01_bh_relational
pip install -r requirements.txt
make all

# run any simulation
cd ../../simulations/01_dfield_nbody
pip install -r requirements.txt
make all                                   # deterministic via --seed
```

Docker images for bit-exact reproduction live under `docker/`.

---

## Repository layout

```
esd-cosmology/
├── esd_core/                    shared locked constants and identities
├── studies/
│   ├── A_galactic_dynamics/     galactic dynamics & MOND-scale tests (02–05, 12, 14, 16, 48)
│   ├── B_solar_system/          solar system & local gravity (27, 33)
│   ├── C_gravitational_waves/   GW & multi-messenger (09, 21, 23, 40)
│   ├── D_clusters_halos/        clusters, halos & compact objects (10, 15, 17, 36, 43, 44)
│   ├── E_cosmological_background/ expansion history & background (07, 08, 20, 22, 31, 41, 42, 47)
│   ├── F_cmb_lss/               CMB, LSS & linear regime (01, 06, 11, 13, 18, 19, 24, 34, 35, 37–39, 45, 46)
│   └── G_anomalies/             anomalies, tensions & open falsifiers (25, 26, 28–30, 32)
├── theory/NN_<name>/            applicability-theorem derivations
├── simulations/NN_<name>/       end-to-end numerical evolution (N-body, streams)
├── docker/                      shared base image
├── docs/                        replication guide
├── visualizations/              local-only; .gitignored until promoted
└── .github/workflows/           CI smoke tests
```

Each `studies/GROUP/NN_*/`, `theory/*/`, and `simulations/*/` folder follows
the same convention: `scripts/` (audit + figures), `scripts/outputs/`
(JSON + CSV artifacts), `paper/` (write-up), `Makefile`,
`requirements.txt`. Simulations additionally expose a `snapshots/`
dump directory and a `--seed` flag for deterministic runs.

---

## Citation

See [`CITATION.cff`](CITATION.cff) for the canonical citation block.
Each study's `paper/README.md` carries the paper-specific DOI once
assigned.

---

## License

See [`LICENSE`](LICENSE).
