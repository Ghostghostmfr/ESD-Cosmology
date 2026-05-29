# Study 05 — SPARC Radial Acceleration Relation (zero-parameter reproduction)

Replication of paper 1's RAR figure and its headline numbers, using
the locked golden-ratio closure with zero per-galaxy free parameters
(fixed M/L baseline). See [paper/README.md](paper/README.md) for the
full citations.

## Quickstart

```bash
# from the repo root, with esd_core already installed (pip install -e .)
cd studies/05_rar
pip install -r requirements.txt
make all          # RAR aggregation + figures
```

Outputs land in [scripts/outputs/](scripts/outputs/);
figures in [figures_generated/](figures_generated/).

## What reproduces what

| Paper item                                            | Script                       | Make target |
|-------------------------------------------------------|------------------------------|-------------|
| Sample size (~3,450 data points across 175 galaxies)  | `scripts/run_rar.py`         | `make rar`  |
| $\Delta\chi^2_{\rm fixed} = -588$ (ESD vs MOND, fixed M/L; matches Study 03) | `scripts/run_rar.py`         | `make rar`  |
| Log-residual mean $\approx 0$ for both models         | `scripts/run_rar.py`         | `make rar`  |
| Fig. `fig:rar` top panel ($g_{\rm obs}$ vs $g_{\rm bar}$) | `scripts/make_rar_figures.py`  | `make figures` |
| Fig. `fig:rar` bottom panel (running median + band)   | `scripts/make_rar_figures.py`| `make figures` |

*Paper headline $\Delta\chi^2 = -843$ and $\chi^2_\nu \approx 12$ are from
the per-galaxy $13\times 9$ grid analysis in Table I, not Fig. `fig:rar`
(whose caption is explicit about fixed M/L); those are reproduced by Study 03.*

## Relationship to other studies

- **Study 02 (BTFR)** uses the same closure to predict flat-velocity
  asymptotes; it's the deep-MOND projection of the same RAR locus.
- **Study 03 (rotation curves)** runs the per-galaxy $\chi^2$ analysis
  on the same 175 galaxies; the $\Delta\chi^2 = -843$ here is the same
  number aggregated point-by-point instead of galaxy-by-galaxy --
  this is the cross-check.
- **Study 04 ($a_0$ derivation)** locks the $a_0 = 1.2\times10^{-10}$ m/s²
  that enters $u = 4 g_{\rm bar}/a_0$.

The four studies together test the same closure on three statistically
independent SPARC observables (flat-V asymptote, full curve, binned
RAR locus) with no shared free parameters.

## Acceptance gate

`scripts/run_rar.py` returns exit code 0 iff every headline number
reproduces within the tolerances declared at the top of that file
(point count $\pm 200$, residual mean $\pm 0.05$ dex,
$\Delta\chi^2_{\rm fixed} \pm 30$).
