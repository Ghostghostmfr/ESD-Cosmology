# Study 12 - a_0 cross-anchor closure consistency

**Status:** GATE PASS (4/4 claims reproduced)

Verifies that the MOND-scale acceleration `a_0` used throughout the
esd-cosmology suite (Studies 02 BTFR, 03 rotation curves, 04 a_0
derivation, 05 RAR, 08 Hubble tension) traces back to a single
Identity-B-locked closure-pool value, and quantifies how the
Planck/SH0ES `H_0` tension translates into an `a_0` anchor mismatch.

Primary reference:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

## Identities verified

```
Bridge (C1 of Theorem 1):
  a_0 = c * H_0 * sqrt( (3 Omega_DM + Omega_b) / (8 pi) )

Equivalent omega-form (h-independent):
  a_0 = c * 100 km/s/Mpc * sqrt( (3 omega_DM + omega_b) / (8 pi) )
```

## What it reproduces

1. **Round-trip (claim 1):** `H_0 -> a_0(H_0) -> bridge_inversion(a_0)`
   returns the original `H_0` to **machine precision** (0 absolute
   residual).
2. **Planck-mode anchor (claim 2):** the bridge prediction at
   `H_0 = 67.36 km/s/Mpc` is `a_0 = 1.2015e-10 m/s^2`, matching the
   McGaugh+2016 RAR best-fit `a_0 = 1.20e-10 m/s^2` to **0.12%**
   (gate 2%).
3. **h-blindness (claim 3, Theorem 1 C1 row):** in the omega-form
   the derivative `d a_0 / d h = 0` **exactly** when `omega_DM` and
   `omega_b` are held fixed.  Not just numerically small -- the
   formula has no `h` reference.
4. **Single source of truth (claim 4):** every study's `a_0` value
   ties back to `esd_core.a_zero()` bit-for-bit; no per-study
   re-derivation of the constant.

## The H_0 tension expressed as an a_0 anchor mismatch

```
Mode        H_0 [km/s/Mpc]   a_0 [10^-10 m/s^2]   rel.err vs McGaugh
Planck      67.36            1.2015               +0.12%
SH0ES       73.04            1.3028               +8.56%
McGaugh     -                1.2000               0
```

SH0ES-mode `H_0` is structurally incompatible with the McGaugh+2016
RAR anchor at the ~9% level, while Planck-mode `H_0` matches it to
0.1%.  Theorem 1's h-blindness then implies SH0ES cannot be moved
to RAR by adjusting any ESD-distinctive channel internally.

## How to run

```pwsh
cd Research/Modeling/esd-cosmology/studies/12_a0_anchor
make audit         # exit 0 iff all 4 claims pass
make figures
```

## Primary citations

* James P. Higginson 2026, *ESD Framework: The Hubble Tension as a
  Structural h-Blindness Boundary and Mirror-Identity Classification
  of Dark Energy*, Zenodo DOI 10.5281/zenodo.20400097.
* McGaugh, Lelli, Schombert 2016, PRL 117, 201101 (SPARC RAR).
* Aghanim+ 2020, A&A 641, A6 (Planck 2018 H_0).
* Riess+ 2022, ApJL 934, L7 (SH0ES H_0).
