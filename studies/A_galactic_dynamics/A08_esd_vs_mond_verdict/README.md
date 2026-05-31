# Study 48 — ESD vs MOND: Formal Statistical Verdict (175 SPARC Galaxies)

Formal head-to-head statistical comparison of the ESD golden-ratio
closure against MOND (simple interpolation) across the full 175-galaxy
SPARC sample.

Framework reference:

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: [10.5281/zenodo.19283596](https://doi.org/10.5281/zenodo.19283596)

Companion paper (per-galaxy curves):

> Higginson, J. P. (2026). *Rotation Curve Predictions for 175 SPARC
> Galaxies from the Golden-Ratio Gravitational Closure.*

---

## What this study is and is not

**Study 03** (`A02_sparc_rotation_curves`) runs both theories at every
measured radius and reproduces the paper's per-galaxy table. Its job is
*zero-parameter reproduction*.

**This study** asks the comparative question explicitly: *given the same
galaxy sample, the same mass-to-light freedom, and the same baryonic
data, which theory fits better and by how much?* The output is a formal
statistical verdict — W/T/L counts, the signed Δχ² total, the Δχ²
distribution, and a per-galaxy scatter — with the same reproducibility
contract.

The analysis reads from study 03's `galaxy_results.csv`, so there is no
duplicate computation.

### Two operating modes

| Command | What it does | Prerequisite |
|---|---|---|
| `make summary` | Generates two verdict figures (`wtl_comparison.png`, `delta_chi2_summary.png`) directly from the published headline numbers embedded in the script. **Always works on a fresh clone.** | None |
| `make all` | Full verification: re-reads the per-galaxy CSV from study 03 and checks every W/T/L count against the published result. | `make residuals` in `A02_sparc_rotation_curves` |

---

## Comparison design

Both theories are given identical conditions:

| Property | ESD | MOND |
|---|---|---|
| Interpolation function | golden-ratio R(u) — zero free parameters | simple-IF µ(x) = x/(1+x) |
| MOND scale a₀ | 1.2 × 10⁻¹⁰ m s⁻² (same value for both) | 1.2 × 10⁻¹⁰ m s⁻² |
| M/L freedom (disk Υ_d, bulge Υ_b) | grid-searched over 13×9 = 117 points | same grid, same points |
| Baryonic inputs | V_gas, V_disk, V_bul from SPARC | identical |
| Classification margin | Δ = 1.0 in χ² | — |

Neither theory has any per-galaxy fitted constants beyond (Υ_d, Υ_b).
The five ESD closure constants {φ, q, s, b, c} are locked; they are
not tuned to the SPARC sample in any way.

### Fixed-M/L variant

A second comparison uses zero M/L freedom: Υ_d = 0.5, Υ_b = 0.7
(population-synthesis defaults). This gives both theories no fitted
parameters at all — the purest zero-free-parameter test.

---

## Results

### Grid M/L (best-fit Υ_d, Υ_b for each theory independently)

| Metric | Value |
|---|---|
| Sample (paper 1 head-to-head, late-type only) | **171** galaxies |
| Sample (this study, full SPARC) | 175 galaxies |
| ESD wins (Δχ² < −1) | **53** |
| Ties (|Δχ²| ≤ 1) | 94 (paper) / 98 (full 175) |
| ESD losses (Δχ² > +1) | **24** |
| **Σ Δχ²** | **−843** |

Paper 1 excludes 4 early-type galaxies from the head-to-head; all 4
always fall inside the tie band and do not affect W, L, or Σ Δχ².
This study runs all 175 and inherits 4 extra ties (T: 94→98). The
headline verdict — **53 wins, 24 losses, Σ Δχ² = −843** — is
identical either way.

### Fixed M/L (zero per-galaxy freedom)

| Metric | Value |
|---|---|
| ESD wins | **73** |
| Ties | **55** |
| ESD losses | **47** |
| **Σ Δχ²** | **−588** |
| Galaxies with χ²ᵥ(ESD) < χ²ᵥ(MOND) | **110 / 175** |

Even at zero per-galaxy freedom — no M/L adjustment allowed —
ESD achieves a lower reduced-χ² than MOND in 110 of 175 galaxies
and a net Σ Δχ² = −588.

---

## Framework interpretation

The ESD closure function

$$R(u) = \frac{s}{u^\varphi + b\,u^q + c}, \qquad u = \frac{4\,g_N}{a_0}$$

is not a generalization of MOND's interpolation function — it is derived
from the golden-ratio spectral structure of the parent action (see paper
1, §3). The five constants {φ, q, s, b, c} are set by φ = (1+√5)/2
before any galaxy data is seen. The improvement over MOND is therefore
not a fit residual; it is a structural prediction.

The win/tie/loss classification is deliberately conservative (Δ = 1.0
rather than, say, 3.0). Relaxing to Δ = 3.0 increases the W and reduces
the T count without changing Σ Δχ².

---

## Quickstart

```bash
# from repo root with esd_core installed
cd studies/A08_esd_vs_mond_verdict

# run study 03 first to build the galaxy_results.csv
cd ../A02_sparc_rotation_curves && make residuals && cd ../A08_esd_vs_mond_verdict

# then build the comparison figures
make all
```

Outputs land in `scripts/outputs/`. Figures in `figures_generated/`.

---

## What reproduces what

| Output | Script | Make target |
|---|---|---|
| `verdict_summary.{json,txt}` — W/T/L, Σ Δχ² | `scripts/esd_vs_mond_verdict.py` | `make verdict` |
| `delta_chi2_histogram.png` | `scripts/esd_vs_mond_verdict.py` | `make verdict` |
| `esd_vs_mond_scatter.png` | `scripts/esd_vs_mond_verdict.py` | `make verdict` |
| `cumulative_delta_chi2.png` | `scripts/esd_vs_mond_verdict.py` | `make verdict` |

---

## Acceptance gate

| Quantity | Published | Tolerance | Note |
|---|---|---|---|
| N total (full SPARC) | 175 | ±2 | |
| Grid W | 53 | ±2 | paper: 171 late-type |
| Grid T | 94 | ±6 | +4 if running all 175 |
| Grid L | 24 | ±2 | |
| Grid Σ Δχ² | −843 | ±30 | unchanged 171 vs 175 |
| Fixed W | 73 | ±2 |
| Fixed L | 47 | ±2 |
| Fixed Σ Δχ² | −588 | ±30 |
| Galaxies with χ²ᵥ(ESD) < χ²ᵥ(MOND), fixed M/L | 110 | ±5 |

Study passes if and only if every acceptance gate passes.
