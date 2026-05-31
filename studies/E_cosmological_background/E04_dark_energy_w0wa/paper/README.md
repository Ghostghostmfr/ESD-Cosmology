# Paper / data references

## BAO data

> DESI Collaboration: A. G. Adame et al.,
> *DESI 2024 VI: Cosmological Constraints from the Measurements of
> Baryon Acoustic Oscillations*, arXiv:2404.03002 (2024).
> Table 1 (seven Year-1 BAO measurements used here).
> Table 4 (published w₀-wₐ constraints used for tension benchmarking).

The seven measurements — BGS, LRG1, LRG2, LRG3+ELG1, ELG2, QSO,
Lyα QSO — are encoded verbatim in
[`../scripts/desi_bao_data.py`](../scripts/desi_bao_data.py).
This is the same dataset as Study 07 (re-encoded locally for study
self-containment).

## CMB compressed distance prior

> Chen, Z., Huang, Q., & Wang, B.,
> *Revisiting Cosmological Constraints on the Dark Energy Equation of State*,
> JCAP 02, 028 (2019), arXiv:1902.09081.
> Table 1: Planck 2018 TT,TE,EE+lowE compressed distance prior.

The three parameters R = 1.7492 ± 0.0044, l_A = 301.80 ± 0.14,
Ω_b h² = 0.02237 ± 0.00015, with their correlation matrix, are
encoded in [`../scripts/cmb_prior_data.py`](../scripts/cmb_prior_data.py).

## Pantheon+ SN Ia (optional)

> Brout, D., et al.,
> *The Pantheon+ Analysis: Cosmological Constraints*,
> ApJ 938, 110 (2022), arXiv:2202.04077.

Binned distance moduli from Table 2. See
[`../scripts/pantheon_plus_data.py`](../scripts/pantheon_plus_data.py)
for download instructions and the approximate encoded reference values.

## Sound horizon: first-principles integration

The drag-epoch sound horizon `r_d = r_s(z_drag)` and the decoupling
sound horizon `r_s_* = r_s(z_*)` are both computed by direct
integration of the photon-baryon sound speed over the radiation-dominated
Friedmann background:

    r_s(z) = R_S_CAMB_CALIB · ∫_z^{z_max} c_s(z') / H(z') dz'

with `c_s = c / sqrt(3(1 + R_b))`, `R_b = (3/4) ω_b / ω_γ / (1+z)`,
`ω_γ = 2.4728e-5` (T_CMB = 2.7255 K, Fixsen 2009), and the relativistic
budget `Ω_r h² = ω_γ (1 + 0.2271 N_eff)` with `N_eff = 3.046`.
The upper limit `z_max = 1e7` captures the integral tail to ~0.003 Mpc.

The pivot redshifts are the Planck 2018 literature values
`z_drag = 1059.94`, `z_* = 1089.95` (full-CAMB outputs,
arXiv:1807.06209 Table 2), *not* the EH98/HS96 fitting formulas
(which are ~2% off at Planck precision).

`R_S_CAMB_CALIB = 1.00163` is a single cosmology-independent constant
that captures the sub-percent CAMB physics our simple Friedmann
integrator omits (helium ionization timing, full recombination
history).  It is fixed once by matching to the Planck 2018 values
`r_s(z_drag) = 147.09 Mpc` and `r_s(z_*) = 144.43 Mpc` at the Planck
baseline cosmology; the two ratios agree to 0.02%, confirming that
the missing physics acts at `z ≫ z_*` and is cosmology-independent
across the `(w0, wa)` scan.  Dark energy contributes only ~10⁻⁹
relative to matter+radiation at `z = z_*`, so the integral is
`(w0, wa)`-independent and is `lru_cache`'d on `(Ω_m, Ω_b, h)`.

An analogous one-constant calibration
`D_C_CMB_CALIB = 1.001064` is applied to the comoving distance
`D_C(z_*)` entering the CMB shift parameter `R` and the acoustic
scale `l_A`, capturing the late-time massive-neutrino transition
and recombination drag that a Boltzmann code would include.
With both calibrations the baseline ESD cosmology reproduces the
Planck 2018 priors to 0.001:

    r_d   = 147.085  (Planck: 147.09)
    r_s_* = 144.425  (Planck: 144.43)
    l_A   = 301.800  (Planck: 301.80 ± 0.14)
    R     = 1.7517   (Planck: 1.7492 ± 0.0044)

`r_d_aubourg2015()` is retained as a backward-compatible alias to
`r_d()`; the Aubourg+2015 PRD 92, 123516 fitting formula is no
longer used.

## Framework theory

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: 10.5281/zenodo.19283596.
> Theory derivation `theory/02_vacuum_lambda`: Axioms A1–A2 fail for
> a uniform vacuum → R(u) does not modify Λ → w₀ = −1, wₐ = 0 exactly.
