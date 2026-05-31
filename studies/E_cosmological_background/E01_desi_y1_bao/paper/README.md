# Paper / data references

## Data

> DESI Collaboration: A. G. Adame, et al.,
> *DESI 2024 VI: Cosmological Constraints from the Measurements of
> Baryon Acoustic Oscillations*, arXiv:2404.03002 (2024).
> Table 1 (the seven Year-1 BAO measurements used here).

The seven measurements -- BGS, LRG1, LRG2, LRG3+ELG1, ELG2, QSO, Ly-alpha QSO --
are encoded verbatim in [`scripts/desi_y1_data.py`](../scripts/desi_y1_data.py)
including the within-tracer (D_M, D_H) correlation coefficients.

## Framework reference

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: [10.5281/zenodo.19283596](https://doi.org/10.5281/zenodo.19283596).
> Ch. 4 (Identities A and B; the dark-energy / matter and baryon /
> dark-matter splits used here).

## Sound horizon

The comoving sound horizon at the drag epoch is computed in closed
form via the Aubourg+ 2015 fitting formula:

> Aubourg, E. et al., *Cosmological implications of baryon acoustic
> oscillation measurements*, PRD 92, 123516 (2015), Eq. 16.

This is calibrated to CAMB at the ~0.3 % level over the Planck-favored
region, which is well below the per-data-point precision of DESI Y1.
Any residual r_d normalization bias cancels in the *differential* test
that this study gates on (Delta chi^2 between framework and Planck
baseline at the same r_d formula).
