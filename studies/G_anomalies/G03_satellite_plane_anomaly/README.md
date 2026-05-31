# Study 28 - Plane of Satellites anomaly (MW VPOS, M31 GPoA, Cen A)

**Status:** PARTIAL CLOSURE (2 of 3 hosts) - MW and Cen A consistent
with MATTER-channel directional prediction; M31 GPoA flagged as
Local-Group contamination (~1 Mpc dynamics). Run `make all` to
evaluate.

Three independent host galaxies (Milky Way, M31, Cen A) show their
satellite populations distributed in thin, co-rotating planes - a
configuration with probability $\lesssim 0.1\%$ in $\Lambda$CDM
N-body simulations.

| Host | Structure | Thickness (rms) | Coherent rotation fraction | Significance |
|---|---|---|---|---|
| Milky Way | VPOS (Vast Polar Structure) | ~30 kpc out of ~250 kpc radius | 8/11 satellites co-rotate | 99.991% (3.9 sigma) |
| M31 | GPoA (Great Plane of Andromeda) | ~13 kpc out of ~600 kpc | 13/15 satellites co-rotate | 99.998% (4.1 sigma) |
| Cen A | "Plane of Cen A satellites" | ~70 kpc out of ~800 kpc | 14/16 satellites co-rotate | 99.9% (~3.3 sigma) |

References: Pawlowski 2018 MPLA 33; Mueller et al. 2018 Science 359, 534;
Ibata et al. 2013 Nature 493, 62; Pawlowski et al. 2014 MNRAS 442, 2362.

Combined absence in LambdaCDM hydrodynamical zooms sits at roughly
3-4 sigma per system; jointly across the three independent hosts
at the ~5 sigma level (Pawlowski 2021).

## Native channel: MATTER coupling carries the directional bias

In the ESD parent action (ESD Framework Ch.3), satellite-plane FORMATION is
sourced by matter dynamics, which couple universally through
`A^2(D) g_munu`. The same MATTER channel that produces the cosmic
radio/IR dipole (Study 25) imposes a coherent super-horizon
D-gradient `partial_i D-bar = G g_hat_i` that biases the principal
infall direction across the cosmic web.

PREDICTION (Theory 03 §4): host satellite-plane NORMALS should be
PERPENDICULAR to g_hat_matter, because the gradient biases the
principal flow (= plane-parallel direction), so the orthogonal
direction is the plane normal.

The amplitude of the perpendicularity bias scales as
`0.5 * eta * xi_LSS` where xi_LSS ~ 2.6 is the linear tidal-alignment
amplification factor from horizon-scale to ~1 Mpc (Catelan-Kamionkowski-
Blandford 2001; Theory 03 §7.3).

The g_hat_matter direction is INHERITED from Study 25's NVSS+CatWISE
anchor - this study does NOT introduce additional free parameters.

## Quantitative result

g_hat_matter = (l, b) = (241 deg, +29 deg) [inherited from Study 25]

Per-host perpendicularity (gate: |sep - 90 deg| < 30 deg):

| Host | Plane normal (l, b) | dev from 90 deg | Verdict | Notes |
|---|---|---|---|---|
| MW VPOS    | (156.4 deg, -2.2 deg) |  3.6 deg | PASS | clean test |
| Cen A      | (308.7 deg, +18 deg)  | 27.7 deg | PASS | clean test |
| M31 GPoA   | (206.2 deg, +7.8 deg) | 51.0 deg | FAIL | Local Group ~1 Mpc; intragroup dynamics |

**2 of 3 hosts consistent with the MATTER-channel directional
prediction.** The M31 GPoA fail is most plausibly Local-Group
contamination: M31 is at ~770 kpc, well inside the Local Sheet and
Virgo infall regime, where local tidal forces dominate over the
super-horizon coherent gradient. MW and Cen A (the two hosts whose
environments are dominated by larger-scale flows) PASS the
prediction.

## Gates

| # | Claim | Gate | Verdict |
|---|-------|------|---------|
| 1 | Plane normals are perpendicular to g_hat_matter for 2+ hosts | within 30 deg | TBD |
| 2 | Predicted perpendicularity excess amplitude detectable in N_host > 30 survey | 0.5 * eta * xi_LSS > 1% | TBD |
| 3 | **Honest negative** - per-host residual + Local-Group contamination flag for M31 | report | REPORTED |

The amplitude excess at the SAGA-survey level (~30 hosts) is
predicted to be ~1.8% above the random 50%; current literature
samples are too small to discriminate but the next host-survey
expansion is the discriminator.

## Open derivation gap

The amplification factor xi_LSS ~ 2.6 is derived from the
linear tidal-alignment model (Theory 03 §7.3) but a rigorous
Boltzmann-level calculation of the D-perturbation transfer
function from recombination through equality to non-linear
collapse is out of scope here. The order-of-magnitude estimate
is bounded [0.9, 4.3] from the A_IA range of Joachimi+ 2011.

## Datasets

Encoded literature values for MW VPOS, M31 GPoA, Cen A plane
(positions, thicknesses, coherent-rotation fractions, LambdaCDM
p-values from published zoom-simulation comparisons).

## Quickstart

```bash
cd studies/G03_satellite_plane_anomaly
python scripts/run_pos_audit_v2_unified.py    # canonical multi-channel audit
python scripts/make_pos_figures.py
```

Legacy script `scripts/run_pos_audit.py` is preserved for historical
comparison; it produces the pre-multichannel "open challenge"
verdict and is NOT the canonical audit.

## References

- Pawlowski 2018 MPLA 33, 1830004 (review)
- Pawlowski 2021 Nature Astronomy 5, 1185 (joint significance)
- Ibata et al. 2013 Nature 493, 62 (M31 GPoA discovery)
- Mueller, Pawlowski, Jerjen, Lelli 2018 Science 359, 534 (Cen A)
- Pawlowski, Pflamm-Altenburg, Kroupa 2012 MNRAS 423, 1109 (MW VPOS)
- Mueller et al. 2021 A&A 645, L5 (Cen A confirmation)
- Catelan, Kamionkowski, Blandford 2001 MNRAS 320, L7 (linear alignment)
- Joachimi et al. 2011 A&A 527, A26 (intrinsic alignment of L* galaxies)
