# Study 08 - ESD Hubble-tension paper reproduction

**Status:** GATE PASS (all 5 published claims reproduced)

This study is a faithful computational reproduction of the published
ESD Hubble-tension paper:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

It is not a re-litigation of the SH0ES/Planck tension; it confirms
that the paper's positive claims hold when re-evaluated independently
from the framework-locked constants exported by `esd_core`.

## What it reproduces

1. **C1 (bridge inversion):** Inverting
   `a_0 = c · H_0 · sqrt((3 Ω_DM + Ω_b) / (8π))` for `H_0` using the
   McGaugh+2016 RAR anchor `a_0 = 1.20e-10 m/s²` and the
   framework-locked `(Ω_DM, Ω_b)` yields **H_0 ≈ 67.28 km/s/Mpc** —
   consistent with Planck to 0.1%, discrepant with SH0ES by ~8% (5.6
   km/s/Mpc).
2. **Identity (C):** `3 Ω_DM + Ω_b = (18/π) Ω_Λ² Ω_m`, reproduced to
   machine precision (10⁻¹⁶) using framework-locked `(Ω_Λ, Ω_m,
   Ω_DM, Ω_b)`.  The paper quotes 0.007 % residual using Planck-2018
   means as inputs; the framework lock is constructed so (C) is an
   exact algebraic consequence of (A)+(B).
3. **h-blindness Theorem (Thm 1):** Centered-difference Jacobian
   |∂R_i/∂h|/|R_i| < 10⁻⁸ for every ESD-distinctive child
   {C1=bridge, C4=cluster ratio, C7=Lyα Jeans}.  The non-distinctive
   acoustic-angle child C2 is non-zero (rank 3 over the full set).
4. **6-channel drift budget (paper Table 1):** Combined |ΔH_0| ≤ 0.12
   km/s/Mpc, dominated by Channel 1 (disformal photons).  A factor
   ~47 below the 5.6 km/s/Mpc gap required by SH0ES → framework
   predicts **no H_0 drift** can resolve the tension.
5. **Calibration-bias prediction:** Δμ_host ≈ 0.18 mag (paper quotes
   0.17) — the targeted distance-ladder systematic that would absorb
   the SH0ES offset.

## Multi-anchor table

The pull table groups H_0 anchors by family (CMB / BAO+BBN / TRGB /
lensing / masers / GW / distance-ladder).  Only the distance-ladder
(Cepheid SH0ES) and one of the two TDCOSMO lensing readings are
discrepant at >2σ; every CMB and BAO+BBN anchor lies <2σ from the ESD
bridge prediction.  This is the empirical asymmetry the paper
explains: the SH0ES outlier is calibration-systematic, not drift.

## How to run

```pwsh
cd Research/Modeling/esd-cosmology/studies/08_hubble_tension
make audit         # exit 0 iff all 5 claims reproduce
make figures
```

## Primary citations

* James P. Higginson 2026, *ESD Framework: The Hubble Tension as a
  Structural h-Blindness Boundary and Mirror-Identity Classification of
  Dark Energy*, Zenodo DOI 10.5281/zenodo.20400097.
* McGaugh, Lelli & Schombert 2016, ApJL 836, 152.
* Riess+ 2022, ApJL 934, L7.
* Aghanim+ (Planck) 2020, A&A 641, A6.
* DESI 2024, arXiv:2404.03002.
* Freedman+ 2024, arXiv:2408.06153.
* Wong+ 2020, MNRAS 498, 1420.
* Abbott+ 2017, Nature 551, 85.
