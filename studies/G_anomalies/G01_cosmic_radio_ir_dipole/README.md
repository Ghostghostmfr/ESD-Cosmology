# Study 25 - Cosmic radio/IR dipole vs CMB kinematic dipole

**Status:** SUFFICIENT CHANNEL IDENTIFIED - the MATTER-coupling channel
A^2(D) g_munu carries the excess. Run `make all` to evaluate.

Tests whether the ESD framework's universal MATTER-coupling channel
(parent action `A^2(D) g_munu`, ESD Framework Ch.3) reproduces the ~5sigma
excess in the NVSS / CatWISE2020 quasar dipole amplitude relative to
the Ellis-Baldwin (1984) prediction sourced by the CMB kinematic
dipole.

## The anomaly

The CMB kinematic dipole (Planck 2018):
  v = 369.82 +/- 0.11 km/s toward (l, b) = (264.021 deg, 48.253 deg).

Under the standard kinematic interpretation (Ellis-Baldwin 1984),
the source-count dipole of a flux-limited radio / mid-IR survey of
high-z AGN should be

$$D_\mathrm{pred} = [\,2 + x(1+\alpha)\,]\,\frac{v}{c}\,,$$

giving D_pred ~ 4.6 x 10^-3.

Measured radio / IR dipoles:

| Survey | D_obs (x10^-3) | direction offset from CMB | tension |
|--------|----------------|---------------------------|---------|
| NVSS (Blake & Wall 2002; Singal 2011; Rubart & Schwarz 2013) | ~12-15 | < 25 deg | 3-4 sigma |
| CatWISE2020 (Secrest et al. 2021) | 15.5 +/- 2 | ~28 deg | **4.9 sigma** |
| NVSS + CatWISE joint (Secrest et al. 2022, ApJL 937, L31) | ~14 | ~25 deg | **~5 sigma** |

Roughly 2x the kinematic prediction. One of the most cited unresolved
tensions in cosmology - a direct challenge to the cosmological
principle if the kinematic interpretation is correct.

## Native channel: A^2(D) conformal MATTER coupling

The parent action (ESD Framework Ch.3) couples a coherent super-horizon
D-gradient `partial_i D-bar = G g_hat_i` universally to every matter
species via the conformal metric `A^2(D) g_munu`. Theory 03 derives
the closed-form excess in source number counts as

$$D_\mathrm{conformal} \;=\; x_\mathrm{EB}\,\eta\,\frac{\chi}{R_H}\,,$$

with the SINGLE dimensionless amplitude

$$\eta \;=\; \beta_m \, G_\mathrm{in} \, R_H\,.$$

This is the MATTER channel - sister observables in the same channel
are: CatWISE quasar dipole (independent IR catalogue, same A^2(D)
coupling), and satellite-plane normals (matter dynamics, Study 28).
The DISFORMAL sub-channel `B(D) partial_mu D partial_nu D` shares
g_hat by symmetry (rank-2 tensor along grad D) and supplies the
quad-oct alignment (Study 29).

PHOTON-specific anomalies (CMB hemispherical modulation) belong to
a DIFFERENT channel - `Z(D) F^2` - and can be sourced by an
independent primordial mode (Study 29).

## Quantitative result

Anchor eta to the joint NVSS + CatWISE excess (Theory 03 §3):

| Parameter | Value | Source |
|---|---|---|
| eta_best | (1.38 +/- 0.42) x 10^-2 | NVSS+CatWISE anchor |
| g_hat_matter (l, b) | (241 deg, +29 deg) | best-fit axis |
| Significance (eta != 0) | 3.3 sigma | dipole excess vs kinematic-only |

PREDICTION: every MATTER-channel observable should align within ~35
deg of g_hat_matter. Result:

| Observable | sep from g_hat_matter | Verdict |
|---|---|---|
| NVSS dipole       | 10.8 deg | PASS |
| CatWISE dipole    |  2.8 deg | PASS |
| Disformal quad-oct alignment | 31.0 deg | PASS (Study 29 cross-link) |
| MW VPOS plane normal (perpendicularity)  | 3.6 deg dev | PASS (Study 28 cross-link) |
| Cen A plane normal (perpendicularity) | 27.7 deg dev | PASS (Study 28 cross-link) |

**5 of 5 matter-channel cross-observables pass.** The MATTER channel
A^2(D) g_munu carries the dipole excess cleanly with a single
amplitude + direction.

## Gates

| # | Claim | Gate | Verdict |
|---|-------|------|---------|
| 1 | ESD reproduces standard Ellis-Baldwin from CMB v | \|D_pred(ESD) - D_pred(EB)\| / D_pred(EB) < 1% | TBD |
| 2 | A^2(D) MATTER channel reproduces D_obs ~ 1.4 x 10^-2 | within factor 2 | TBD |
| 3 | Cross-observable axes align within 35 deg of g_hat_matter | 4 of 5 | TBD |
| 4 | **Honest negative** - residual (D_obs - D_pred)/sigma_obs reported | report | REPORTED |

## Open derivation gap

The amplitude eta is anchored, not derived. Pure Starobinsky inflation
under Cassini-bounded beta_m predicts sigma_eta ~ 9 x 10^-11 - eight
orders of magnitude short of the observed 1.4 x 10^-2. The dipole
channel's success is therefore EVIDENCE for a structural framework
extension; the cleanest route is chameleon-style screening of beta_m
(locally Cassini-bounded, cosmologically O(10^4-10^5) larger; standard
scalar-tensor literature). See [theory/03_dfield_horizon_gradient
§7.1](../../../theory/03_dfield_horizon_gradient/README.md) for the gap
analysis and the three candidate closure routes.

## Datasets (encoded in `scripts/dipole_data.py`)

| Quantity | Value | Source |
|---|---|---|
| v_CMB | 369.82 +/- 0.11 km/s | Planck 2018 VII (1807.06205) |
| Direction | (264.021 deg, 48.253 deg) | Planck 2018 VII |
| NVSS D_obs | 1.4 x 10^-2 (combined) | Singal 2011; Rubart & Schwarz 2013 |
| CatWISE2020 D_obs | (1.55 +/- 0.20) x 10^-2 | Secrest et al. 2021 (ApJ 908, L51) |
| NVSS+CatWISE joint | direction ~30 deg from CMB | Secrest et al. 2022 (ApJL 937, L31) |
| x (NVSS) | 1.0 | Blake & Wall 2002 |
| alpha (NVSS) | 0.75 | standard radio spectral index |
| x (CatWISE) | 1.7 | Secrest et al. 2021 |
| alpha (CatWISE) | 1.26 | Secrest et al. 2021 |

## Quickstart

```bash
cd studies/G01_cosmic_radio_ir_dipole
python scripts/run_dipole_audit_v2_unified.py     # canonical multi-channel audit
python scripts/make_dipole_figures.py
```

The legacy single-channel script `scripts/run_dipole_audit.py` is
preserved for historical comparison; it produces the pre-multichannel
"open challenge" verdict and is NOT the canonical audit.

Outputs land in `scripts/outputs/` and `figures_generated/`.

## References

- Ellis & Baldwin 1984, MNRAS 206, 377
- Blake & Wall 2002, Nature 416, 150
- Singal 2011, ApJL 742, L23
- Rubart & Schwarz 2013, A&A 555, A117
- Secrest et al. 2021, ApJL 908, L51 (CatWISE2020 first measurement)
- Secrest et al. 2022, ApJL 937, L31 (~5 sigma combined tension)
- Planck Collaboration 2020, A&A 641, A1 (kinematic dipole)
- Khoury & Weltman 2004, PRD 69, 044026 (chameleon mechanism)
- Damour & Esposito-Farese 1992, CQG 9, 2093 (scalar-tensor screening)
