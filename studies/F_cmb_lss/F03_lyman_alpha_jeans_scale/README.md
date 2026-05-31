# Study 11 - ESD Lyman-alpha Jeans cutoff (C7) audit

**Status:** GATE PASS (3/3 claims reproduced)

Reproduces child **C7** of the published Hubble paper:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

C7 is the third of the ESD-distinctive children (after C1 in Study 08
and C4 in Study 10) whose h-blindness underwrites the no-drift
theorem.  The paper's symbolic expression is

```
lambda_J = (pi / m_D) * sqrt( c_s^2 / (G rho_m a^3) )
        ~ 94 kpc   set by  m_D ~ 1e-22 eV.
```

We implement the rigorous Hu-Barkana-Gruzinov 2000 quantum-Jeans form

```
k_Q(z) = (16 pi G rho_m)^(1/4) * (m_D a / hbar)^(1/2)
lambda_J(comoving) = 2 pi / k_Q
```

which differs from the paper's symbolic expression only by an
order-unity convention factor.

## What it reproduces

1. **Magnitude (claim 1):** at fiducial `(m_22=1, omega_m h^2=0.1429,
   z=3)` the comoving lambda_J = **63.9 kpc**, within a factor 2 of
   the paper's quoted 94 kpc.  Gate `|log10(pred/paper)| <= 0.301`.

2. **h-blindness (claim 2, Theorem 1):** centered Jacobian
   `d lambda_J / d h = 0.0` **exactly** when `omega_m h^2` is held
   fixed.  The formula uses physical-density variables and has no
   `h` dependence.

3. **Scaling (claim 3):** the locked exponent
   `d ln lambda_J / d ln m_22 = -0.5` is reproduced exactly
   (fit over m_22 in [0.1, 100]).  This is the structural fingerprint
   of an ultralight scalar source.

## How to run

```pwsh
cd Research/Modeling/esd-cosmology/studies/F03_lyman_alpha_jeans_scale
make audit         # exit 0 iff all 3 claims pass
make figures
```

## Open question: Lyman-alpha exclusion bounds

The framework's preferred `m_22 ~ 1` is in tension with the
Rogers & Peiris (2021) eBOSS DR14 lower bound `m_22 > 200`.  Two
published readings exist:

* The strong bound relies on hydrodynamic simulations whose
  thermal-history priors have been argued to be too tight
  (cf. Hooper, Krnjaic, McDermott 2022).  Conservative bounds
  (Palanque-Delabrouille+2013, Irsic+2017) sit at `m_22 > 20`.
* The framework prediction of the cutoff scale (~100 Mpc^-1
  comoving at m_22=1) is above the Lyman-alpha probe range
  (`k_max ~ 5 Mpc^-1` at z~3), so a strict null on the Jeans
  signature is observationally borderline.

The paper acknowledges this as the C7 row's open question; the
h-blindness identity is independent of the m_D value.

## Primary citations

* James P. Higginson 2026, *ESD Framework: The Hubble Tension as a
  Structural h-Blindness Boundary and Mirror-Identity Classification
  of Dark Energy*, Zenodo DOI 10.5281/zenodo.20400097.
* Hu, Barkana, Gruzinov 2000, PRL 85, 1158 (fuzzy DM quantum Jeans).
* Palanque-Delabrouille+ 2013, A&A 559, A85 (SDSS-BOSS DR9).
* Irsic+ 2017, PRL 119, 031302 (XQ-100).
* Rogers & Peiris 2021, PRL 126, 071302 (eBOSS DR14).
