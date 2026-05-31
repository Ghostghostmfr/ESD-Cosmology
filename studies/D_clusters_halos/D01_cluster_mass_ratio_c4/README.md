# Study 10 - ESD cluster ratio C4 audit

**Status:** GATE PASS (4/4 claims reproduced)

Reproduces child **C4** of the published Hubble paper:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

C4 is the second of the three ESD-distinctive children whose
h-blindness underwrites the no-drift theorem. The paper's expression is

```
M_tot / M_b  =  ( 1 + R(u_cl) )  +  Omega_DM / Omega_b
            R(u) = s / Sigma(u)
        Sigma(u) = u^p + b u^q + c
        (p, q, b, c, s)  all locked by the parent action.
```

## What it reproduces

1. **Direct R_500c measurements (claim 1a):** the framework predicts
   f_b = M_b / M_tot at R_500c against X-COP, Planck-SZ, and CHEX-MATE
   to **max pull 0.81 sigma** over the three samples.  CHEX-MATE
   matches at exactly **0.00 sigma**.

2. **R_200c extrapolations (claim 1b):** the two model-dependent
   outskirt-extrapolated samples (X-COP extrap., XMM Outskirts) sit
   at +2.5 sigma — the framework predicts a slightly *lower* f_b in
   the deep-ESD outskirts (u_cl ~ 0.7) than the observations infer
   when assuming a power-law gas profile beyond the data.  Within the
   ~3 sigma gate this is consistent.  An honest open question: this
   could be (i) the assumed gas extrapolation systematically pushing
   f_b toward cosmic, or (ii) a real framework prediction the
   measurement disagrees with at modest significance.

3. **h-blindness (Theorem 1):** centered-difference Jacobian
   `d ln (M_tot/M_b) / d h = 0` **exactly** (no numerical residual,
   not just <1e-9) — the prediction is in `omega`-variables
   throughout.

4. **Cosmic asymptote:** `f_b(u -> infinity) = Omega_b / Omega_m =
   0.1587` to one part in 10^9.  Deep-Newton clusters recover the
   cosmic baryon fraction exactly.

## How to run

```pwsh
cd Research/Modeling/esd-cosmology/studies/D01_cluster_mass_ratio_c4
make audit         # exit 0 iff all 4 claims pass
make figures
```

## Per-sample summary

| sample              | radius  | u_cl | R(u)  | f_b pred | f_b obs | pull |
|---------------------|---------|------|-------|----------|---------|------|
| X-COP               | R_500c  | 1.61 | 1.123 | 0.1347   | 0.131   | -0.73 |
| Planck SZ           | R_500c  | 1.65 | 1.107 | 0.1350   | 0.126   | -0.81 |
| CHEX-MATE relaxed   | R_500c  | 1.65 | 1.107 | 0.1350   | 0.135   | +0.00 |
| X-COP extrap.       | R_200c  | 0.68 | 1.953 | 0.1211   | 0.146   | +2.49 |
| XMM Outskirts       | R_200c  | 0.84 | 1.709 | 0.1248   | 0.155   | +2.52 |

## Primary citations

* James P. Higginson 2026, *ESD Framework: The Hubble Tension as a
  Structural h-Blindness Boundary and Mirror-Identity Classification of
  Dark Energy*, Zenodo DOI 10.5281/zenodo.20400097.
* Eckert+ 2019, A&A 621, A40 (X-COP cluster baryon fractions).
* Planck 2015 Results XXIV, A&A 594, A24 (Planck SZ baryon census).
* CHEX-MATE Collaboration 2024, A&A 686, A185.
* Ettori+ 2019, A&A 621, A39 (XMM Cluster Outskirts).
* Aghanim+ 2020, A&A 641, A6 (Planck 2018 cosmic f_b).
