# Study 09 - ESD GW propagation (disformal photon channel)

**Status:** GATE PASS (3/3 channel-1 claims reproduced)

Reproduces Channel 1 of the published Hubble paper:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

Channel 1 is the **only finite-cap channel** in the paper's 6-channel
drift budget (Table 1).  All other channels are either structurally
absent (C4), ruled out (C5), or capped at <1e-6 km/s/Mpc (C2, C3, C6).
So if any channel is going to allow drift in H_0, it has to be this
one.  The disformal photon channel itself caps at 0.12 km/s/Mpc — a
factor ~47 below the SH0ES gap.

## What it reproduces

The paper's dispersion law for the oscillation-averaged photon metric
on FLRW is
```
c_gamma^2(z) / c^2  =  1  -  eps_0 (1 + z)^3  -  eps_2 (1 + z)^6
```
with two free coefficients pinned by independent experiments:

1. **GW170817 multi-messenger speed bound.** Combining the 1.74 s lag
   between GW arrival and GRB170817A over the ~40 Mpc luminosity
   distance gives a naive `|c_gamma - c_GW|/c <= 4.2e-16`. The paper's
   adopted bound is `|eps_0| < 6e-15`, which adds headroom for any
   intrinsic GRB delay (~10 s allowed). Study 09 reports the naive
   bound and verifies it sits inside the paper window.

2. **Photon-barrier condition.** The dispersion `c_gamma^2(z)` must
   stay non-negative all the way to last scattering `z_LSS = 1090`.
   With `eps_0 = 6e-15` saturated, this caps `eps_2_max <= 5.93e-19`,
   matching the paper's `5.9e-19` quote to 0.5%.

3. **Saturated channel contribution to H_0.** Modifying the integrand
   of the comoving distance to last scattering by `c_gamma(z)/c` and
   holding the CMB acoustic angle `theta_*` fixed yields
   `Delta D_A / D_A = -1.7e-3` and therefore `Delta H_0 = +0.114
   km/s/Mpc` — matching the paper's Table 1 cap of 0.12 km/s/Mpc
   to 5%. The remaining 5% is the difference between the simple
   `theta_*-fixed` mapping used here and the full angular-power
   spectrum fit used in the paper.

## How to run

```pwsh
cd Research/Modeling/esd-cosmology/studies/09_gw_propagation
make audit         # exit 0 iff all 3 claims reproduce
make figures
```

## What this study does NOT cover

* GW propagation friction (the Sigma_T amplitude term in modified
  gravity).  ESD predicts standard amplitude evolution because the
  disformal coupling enters the metric only through the photon sector,
  not the graviton sector.  A standalone test would use the GW170817
  standard-siren H_0 = 70 +/- 12 km/s/Mpc (consistent with both
  Planck and SH0ES at >2-sigma uncertainty).
* Higher polarizations.  ESD's parent action is a metric theory
  (rank-2 graviton only), so it predicts the two GR polarizations
  exactly.  This is consistent with the LIGO-Virgo polarization
  constraints on GW150914 and GW170814.

## Primary citations

* James P. Higginson 2026, *ESD Framework: The Hubble Tension as a
  Structural h-Blindness Boundary and Mirror-Identity Classification of
  Dark Energy*, Zenodo DOI 10.5281/zenodo.20400097.
* Abbott+ 2017, ApJL 848, L13 (GW170817 + GRB170817A multi-messenger).
* Abbott+ 2017, Nature 551, 85 (GW170817 standard-siren H_0).
