# Study 22 — DESI Y1 BAO + Planck 2018 CMB prior joint w₀-wₐ test

**Status:** GATES PENDING — run `make all` to evaluate.

Tests whether the ESD framework's exact prediction of **w₀ = −1, wₐ = 0**
(constant vacuum energy, from `theory/02_vacuum_lambda` Derivation B) is
consistent with the joint dark-energy equation-of-state constraint from
DESI Y1 BAO + the Planck 2018 CMB compressed distance prior.

An optional Pantheon+ SN arm runs automatically when the binned data file
is present; see [`scripts/pantheon_plus_data.py`](scripts/pantheon_plus_data.py)
for download instructions.

---

## What this study does

ESD's vacuum-applicability theorem (Axioms A1 and A2 both fail for a
uniform vacuum; see `theory/02_vacuum_lambda`) forces

$$w_0 = -1, \quad w_a = 0$$

at all redshifts. This study asks: does the combination of DESI Y1
BAO measurements + the Planck 2018 CMB shift parameters falsify that
prediction at ≥ 3σ?

The CPL (Chevallier-Polarski-Linder) dark-energy parameterisation is

$$w(z) = w_0 + w_a \frac{z}{1+z}$$

and the dark-energy density factor is

$$f_\mathrm{DE}(z) = (1+z)^{3(1+w_0+w_a)}\,\exp\!\left(-\frac{3 w_a z}{1+z}\right).$$

For ESD: $f_\mathrm{DE}(z) \equiv 1$ — no free parameters.

---

## Gates

| # | Claim | Gate | Verdict |
|---|-------|------|---------|
| 1 | ESD (w₀=−1, wₐ=0) consistent with DESI Y1 BAO alone | \|Δχ²_BAO(ESD − Planck-ΛCDM)\| ≤ 5 | TBD |
| 2 | ESD consistent with BAO + CMB joint constraint | Δχ²_2D(ESD vs best-fit CPL) < 11.83 (< 3σ) | TBD |
| 3 | **Honest negative** — w₀-wₐ tension level reported | Δχ²_2D reported with σ conversion | REPORTED |

Gate 1 inherits the Study 07 criterion: the framework's locked
(Ω_m, Ω_b) are near Planck so the BAO-only Δχ² should be small.

Gate 2 tests whether the DESI Y1 + CMB joint preference for w₀ ≠ −1
rises above 3σ. Published DESI Y1 + Planck CMB results place the
tension at ~2.3σ (arXiv:2404.03002 Table 4, BAO + CMB); ESD predicts
exactly ΛCDM for this sector, so Gate 2 is expected to pass at DESI
Y1 precision but is the leading falsifier candidate as DESI Y3/Y5 and
Euclid Y1 data accumulate.

Gate 3 is always reported regardless of the pass/fail of Gates 1–2.

---

## Datasets

### Core (self-contained, encoded in Python)
| Dataset | Source | Measurements |
|---------|--------|--------------|
| DESI Y1 BAO | Adame et al. 2024, arXiv:2404.03002, Table 1 | 7 tracers (BGS, LRG1/2/3+ELG1, ELG2, QSO, Lyα QSO) |
| Planck 2018 CMB compressed prior | Chen, Huang, Wang 2019, arXiv:1902.09081, Table 1 | R, l_A, Ω_b h² + correlation matrix |

### Optional (requires data download)
| Dataset | Source | Notes |
|---------|--------|-------|
| Pantheon+ 20-bin SN | Brout et al. 2022, ApJ 938, 110 | see `scripts/pantheon_plus_data.py` |

---

## Quickstart

```bash
# from repo root, with esd_core installed (pip install -e .)
cd studies/E04_dark_energy_w0wa
pip install -r requirements.txt
make all       # audit + figures
```

Outputs land in [`scripts/outputs/`](scripts/outputs/);
figures in [`figures_generated/`](figures_generated/).

### Make targets

| Target | Action |
|--------|--------|
| `make all` | dirs + audit + figures |
| `make audit` | chi² scan + gate check → `outputs/summary.json` |
| `make figures` | w₀-wₐ contour + BAO residuals |
| `make clean` | remove outputs and generated figures |

---

## Key outputs

- `outputs/summary.json` — gate verdicts, Δχ², tension sigma, best-fit (w₀, wₐ, H₀)
- `outputs/chi2_grid.npz` — 2D profiled χ² grid in the w₀-wₐ plane
- `figures_generated/fig_w0wa_contours.{png,pdf}` — χ² contours with ESD prediction
- `figures_generated/fig_bao_residuals.{png,pdf}` — per-tracer residuals (ESD vs best-fit CPL vs Planck-ΛCDM)

---

## Framework-native statement

ESD's **vacuum channel** alone predicts w₀ = −1, wₐ = 0 as a
**theorem** (not a fit), derived in `theory/02_vacuum_lambda`.

**Multi-channel framing (canonical):** the parent action (ESD Framework Ch.3)
also contains a D-field sector (`V(D)` potential + `αX₀F(X/X₀)`
kinetic + `A²(D)` matter-coupling drag). These channels are NOT
subject to the vacuum-applicability theorem and can contribute an
effective time-evolving component to the observed w(z). The
quantity tested against DESI Y1 is therefore the SUM

$$w_\mathrm{eff}(z) = \frac{\Omega_\Lambda(-1) + \Omega_V(z)\,w_V(z) + \Omega_\mathrm{kin}(z)\,w_\mathrm{kin}(z)}{\Omega_\mathrm{DE,total}(z)}\,,$$

with the vacuum contribution exactly −1 by theorem and the D-field
contribution naturally O(0.1) in w_a for canonical late-time slopes
of V(D). See [theory/02_vacuum_lambda §11](../../../theory/02_vacuum_lambda/README.md)
for the full multi-channel decomposition.

**Falsifier (sharpened):** a detected w_a deviation EXCEEDING the
natural D-field-rolling contribution (~O(0.1)) at ≥ 5σ would falsify
the *combined* vacuum + D-sector picture, not the vacuum theorem
alone. DESI Y3/Y5 + Euclid Y1 are the next decisive datasets.

See [`paper/README.md`](paper/README.md) for data and theory citations.
