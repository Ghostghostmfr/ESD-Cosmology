# Paper reference

This study reproduces the Radial Acceleration Relation (RAR) figure and
headline numbers of paper 1:

> Higginson, J. P. (2026).
> *Gravity, Electromagnetism, and the Dark Sector from a Single
> Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: [10.5281/zenodo.19283596](https://doi.org/10.5281/zenodo.19283596).
> Sec. *SPARC Benchmark Validation*, Fig. `fig:rar`.

The RAR observable was introduced by

> McGaugh, S. S., Lelli, F., & Schombert, J. M. (2016).
> *Radial Acceleration Relation in Rotationally Supported Galaxies.*
> Phys. Rev. Lett. **117**, 201101.
> [arXiv:1609.05917](https://arxiv.org/abs/1609.05917).

## What this study reproduces

Across **175 SPARC galaxies** at the **fixed-M/L baseline**
($\Upsilon_d = 0.5$, $\Upsilon_b = 0.7$ -- zero per-galaxy parameters)
we aggregate

$$
g_{\rm bar}(r) = \frac{V_{\rm bar}^2(r)}{r},
\qquad
g_{\rm obs}(r) = \frac{V_{\rm obs}^2(r)}{r}
$$

across all valid data points, evaluate the locked ESD prediction

$$
g_{\rm ESD}(r) \;=\; g_{\rm bar}(r)\,\bigl(1 + R(u)\bigr),
\qquad u = 4\,g_{\rm bar}/a_0,
$$

and the canonical MOND simple-$\nu$ reference

$$
g_{\rm MOND}(r) \;=\; \frac{g_{\rm bar}(r)}{1 - \exp(-\sqrt{g_{\rm bar}/a_0})},
$$

then bin the log-residuals $\log_{10}(g_{\rm obs}/g_{\rm model})$ in
$\log_{10} g_{\rm bar}$ bins and report the running median plus 16/84
percentile band.

Headline targets (paper 1 Sec. SPARC, Fig. `fig:rar` -- the figure caption
is explicit that the residual band is computed at fixed M/L):

- $\sim 3{,}450$ valid data points across 175 galaxies
- $\Delta\chi^2_{\rm ESD-MOND} = -588$ at fixed M/L
  (the paper's headline $-843$ and $\chi^2_\nu \approx 12$ are from the
  per-galaxy $13\times 9$ grid analysis in Table I, not Fig. `fig:rar`;
  those are reproduced by Study 03.)
- log-residual mean centred near $0$ for both models

The cross-check $\Delta\chi^2_{\rm fixed} = -588$ matches Study 03's
fixed-M/L headline bit-for-bit (same data, same physics, different
aggregation), which is the expected internal-consistency result.
