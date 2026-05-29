# Paper reference

This study reproduces the headline numbers of the standalone
ESD-framework supporting paper:

> Higginson, J. P. (2026).
> *Derivation of the MOND Acceleration Scale from the
> Energy-Space Displacement Framework.*
> Zenodo. DOI: [10.5281/zenodo.20399682](https://doi.org/10.5281/zenodo.20399682).

Framework reference:

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: [10.5281/zenodo.19283596](https://doi.org/10.5281/zenodo.19283596).

The full LaTeX source of the standalone $a_0$ paper lives in the
parent monorepo at
`Research/ESD_Supporting_Papers/a0_derivation/a0_paper.tex`.

## What this study reproduces

The standalone paper derives

$$
a_0 \;=\; c\,H_0\,\sqrt{\frac{3\,\Omega_{DM} + \Omega_b}{8\pi}}
$$

from the ESD displacement action with zero free parameters.
Numerical headline (Planck 2018 inputs, $H_0 = 67.4$ km/s/Mpc):

- coefficient $\sqrt{(3\Omega_{DM}+\Omega_b)/(8\pi)} = 0.18288$
- $a_0 = 1.198 \times 10^{-10}$ m/s² (within 0.17 % of McGaugh+2016)
- best-fit baryon weight $f_b = 0.354$ (theory prediction 1/3, residual $-0.18\,\%$)

This study reproduces each of those numbers bit-for-bit from
`esd_core.cosmology.a_zero` and the closed-form expressions in
`scripts/esd_a0.py`.
