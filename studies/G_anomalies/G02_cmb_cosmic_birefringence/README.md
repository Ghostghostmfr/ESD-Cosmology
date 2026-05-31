# Study 26 — CMB cosmic birefringence (Eskilt & Komatsu 2023 anomaly)

**Status:** GATES PENDING — run `make all` to evaluate.

Tests whether the ESD framework can accommodate the ~3.6σ measurement of
isotropic cosmic birefringence

$$\beta = 0.342^\circ \pm 0.094^\circ$$

(Eskilt & Komatsu 2023, joint Planck PR4 + WMAP analysis; consistent with
the original Minami & Komatsu 2020 Planck PR3 result β = 0.35° ± 0.14°
and the Eskilt 2022 NPIPE result β = 0.30° ± 0.11°).

## The anomaly

A frequency-independent rotation of the CMB linear-polarization plane by
an angle β between recombination and today would source nonzero EB and TB
cross-correlations:

$$C_\ell^{EB,\text{obs}} = \tfrac{1}{2} \sin(4\beta)\,
   \bigl(C_\ell^{EE} - C_\ell^{BB}\bigr).$$

Standard ΛCDM predicts β = 0 exactly (parity-conserving EM action).
Detection of β ≠ 0 would imply a parity-odd coupling between photons
and a slowly-evolving cosmological field — generically an axion-like
pseudo-scalar with a Chern–Simons term:

$$\mathcal{L}_{\text{CS}} = -\tfrac{1}{4}\, g(\phi)\, F_{\mu\nu}\,
   \tilde F^{\mu\nu}.$$

The induced rotation is β = (g/2) [φ(today) − φ(LSS)].

## ESD prediction: β = 0 exactly

The ESD parent action contains only the parity-even photon coupling:

$$S \supset -\tfrac{1}{4}\, Z(D)\, F_{\mu\nu} F^{\mu\nu}.$$

No g(D) F F̃ term appears. Crucially, ESD's strong-CP-no-axion paper
(`Research/ESD_Supporting_Papers/strong_cp_no_axion/`) closes the door
on adding one *after the fact*: the closure-pool capacity rule (EDF
App. D Q9) and the constant-ownership rule (App. D Q10) together
exclude **any** ultralight pseudo-Goldstone — including the
"string-theory axion descending from ∂μD" — from coupling to a
topological gauge density. The denominator capacity Σ(u) is already
fully consumed by the D-field's own geometry; no slack remains for a
secondary scalar without violating null results from atomic-clock
dark-matter experiments (ADMX, HAYSTAC, GNOME).

Therefore the ESD framework predicts

$$\beta_{\text{ESD}} = 0 \quad \text{exactly, no free parameter.}$$

The measurement β = 0.342° ± 0.094° is therefore a **3.64σ
honest-negative tension** under ESD — a direct falsifier candidate
if the signal is confirmed at ≥ 5σ by LiteBIRD, Simons Observatory,
or CMB-S4 with definitive miscalibration systematics control.

## Gates

| # | Claim | Gate | Verdict |
|---|-------|------|---------|
| 1 | ESD parent action contains no parity-odd photon term | structural audit of action | TBD |
| 2 | ESD framework forbids adding a g(D) F F̃ term post-hoc | strong-CP-no-axion exclusion (Q9, Q10) covers ∂μD-axions | TBD |
| 3 | β_obs consistent with ESD prediction β = 0 | \|β_obs / σ_β\| < 3 across all reported measurements | TBD |
| 4 | **Honest negative** — tension in σ reported per measurement | report | REPORTED |

Gate 3 is expected to **FAIL** for the Eskilt 2022 NPIPE and Eskilt &
Komatsu 2023 joint results (≥ 2.7σ each, joint 3.6σ). This makes the
cosmic-birefringence channel ESD's most direct currently-tensioned
parity-test falsifier.

## Datasets (encoded in `scripts/birefringence_data.py`)

| Analysis | β (deg) | σ_β (deg) | Source |
|---|---|---|---|
| Planck PR3 | 0.35 | 0.14 | Minami & Komatsu 2020 PRL 125 221301 |
| Planck PR4 NPIPE | 0.30 | 0.11 | Eskilt 2022 A&A 662 A10 |
| Planck PR4 + WMAP joint | 0.342 | 0.094 | Eskilt & Komatsu 2023 PRL 130 121301 |

Forecast precisions (for falsifier-discovery gating only):

| Experiment | forecast σ_β | timeline |
|---|---|---|
| LiteBIRD | ~0.05° | 2032 |
| Simons Obs LAT | ~0.1° | 2025–2028 |
| CMB-S4 | ~0.02° | 2030s |

## Quickstart

```bash
cd studies/G02_cmb_cosmic_birefringence
python scripts/run_birefringence_audit.py
python scripts/make_birefringence_figures.py
```

Outputs land in `scripts/outputs/` and `figures_generated/`.

## References

- Minami & Komatsu 2020, PRL 125, 221301 (arXiv:2011.11254)
- Eskilt 2022, A&A 662, A10 (arXiv:2201.13347)
- Eskilt & Komatsu 2023, PRD 106, 063503 / PRL 130, 121301 (arXiv:2205.13962)
- Carroll, Field, Jackiw 1990, PRD 41, 1231 (Chern–Simons rotation)
- Higginson 2026, "Strong CP Without an Axion", ESD Supporting Papers
- ADMX 2020, HAYSTAC 2018 (axion null results)
