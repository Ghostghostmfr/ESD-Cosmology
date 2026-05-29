# Adding a New Study

Each study is a fully self-contained subfolder under `studies/`.
Use the existing `01_linear_cosmology_disco/` folder as a template.

## Layout

```
studies/NN_<short_name>/
├── README.md                # paper title, "what reproduces what" table, quickstart
├── requirements.txt         # pinned study-specific dependencies
├── Dockerfile               # FROM esd-cosmology-base; thin layer
├── Makefile                 # `make all` + per-item targets
├── scripts/                 # phase/step runners; one Python entry per Make target
├── data/                    # small reference data; large data via download script
└── paper/README.md          # paper metadata (arXiv ID, DOI, BibTeX)
```

`outputs/` and `figures_generated/` are auto-created by `make` and
git-ignored.

## Rules

1. **Locked constants come from `esd_core/`.** Never re-derive φ, c,
   c², c⁴, β, Ω_Λ, Ω_m, or Identity-B closure values inside a study.
   `from esd_core import PHI, c, omega_lambda, omega_b_closure_pool`
   and so on.

2. **No hardcoded absolute paths.** Use paths relative to the study
   root, or accept an output directory via environment variable
   (`OUTPUT_DIR`) with a sensible default.

3. **Pin everything.** `requirements.txt` uses `==` specifiers
   captured from a verified working `pip freeze`. Bounded ranges
   (`>=`) are only acceptable for `esd_core` and `pytest`.

4. **One Python entry per Make target.** Each `scripts/<name>.py`
   exposes a `main()` and an `if __name__ == "__main__": main()`
   block. The Make target calls it directly; no shell wrappers.

5. **Output discipline.** Tables write CSV or TXT to `outputs/`;
   figures write PNG (and PDF for paper-grade) to `figures_generated/`.
   Each output file's header (CSV comment, or sidecar `.meta.json`)
   records: script name, locked-constant hash from `esd_core`,
   numpy/scipy versions, and the timestamp.

6. **Cite the framework correctly.** In docstrings and comments,
   refer to the framework as *the Energy-Space-Displacement (ESD)
   framework* with citation key `[HigginsonESDFramework2026]`.
   Do not use internal nicknames.

7. **Add a row to the top-level README's study index** when your
   study lands.

## Regression test

If your study computes any value already exposed by `esd_core/`,
add a regression test to `esd_core/tests/` so future studies cannot
silently shift the published number.
