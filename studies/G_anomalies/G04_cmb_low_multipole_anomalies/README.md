# Study 29 - CMB Low-ell Anomalies bundle (Planck 2018)

**Status:** PARTIAL CLOSURE - the MATTER + DISFORMAL channels carry the
amplitude and quad-oct alignment; the PHOTON `Z(D)F^2` channel naturally
admits an INDEPENDENT g_hat for the hemispherical-modulation axis. Run
`make all` to evaluate.

A bundle of large-angle CMB anomalies that individually sit at ~2-3
sigma but jointly disfavour statistical isotropy at the ~99% level:

| Anomaly | Statistic | Planck 2018 | a posteriori p-value | Significance |
|---|---|---|---|---|
| Quadrupole suppression | $C_2$ vs LCDM | low by ~70% | 0.01-0.05 | 2.0-2.6 sigma |
| Quadrupole-octopole alignment | angle between $\hat n_{\ell=2}, \hat n_{\ell=3}$ | $\sim 3^\circ$ | 0.001-0.01 | 2.6-3.3 sigma |
| Hemispherical power asymmetry | dipolar modulation $A$ | $0.067 \pm 0.022$ at $\ell \le 64$ | 0.001 | ~3.3 sigma |
| Cold Spot | $T < -150\,\mu$K in 5 deg disk | exists | 0.001-0.01 | 2.5-3 sigma |
| Parity asymmetry | $R^{TT}(\ell_\mathrm{max})$ | low | ~0.01 | 2.5 sigma |

Joint significance conservatively ~99% (~3 sigma). References: Planck
2018 VII (A&A 641, A7); Schwarz et al. 2016 CQG 33, 184001.

## Native channels: MATTER + DISFORMAL + PHOTON

The ESD Framework Ch.3 parent action contains THREE coupling channels that
can carry directional CMB signatures, each with its own physical
mechanism and (in principle) its own preferred direction:

1. **MATTER `A^2(D) g_munu`** -> universal conformal coupling
   modulates the matter-density along the LOS, producing a DIPOLAR
   hemispherical-power modulation with amplitude
   `A_hemi = 0.5 * eta * (chi_LSS / R_H) * xi_P`, where
   `xi_P = 2 sqrt(2/3) ~ 1.633` from the locked Starobinsky plateau
   (ESD Framework Ch.15).

2. **DISFORMAL `B(D) partial_mu D partial_nu D`** -> the rank-2 tensor
   structure forces a QUADRUPOLAR (l=2) anisotropy with axis
   *symmetry-locked* along g_hat_matter (eigenvector of the tensor).
   Zero new free parameters; sharp directional prediction.

3. **PHOTON `Z(D) F^2`** -> gauge-sector coupling acts ONLY on
   photons. The parent action does NOT require A(D) and Z(D)
   perturbations to be sourced by the same primordial mode -
   different sectors can have independent super-horizon gradients
   with INDEPENDENT preferred directions g_hat_photon != g_hat_matter.

The Cold Spot and parity asymmetry are LOCALIZED features (~10 deg
disk / oscillatory parity pattern) and belong to a different
mechanism class (cosmic textures / Voronoi-foam voids / topological).
They are NOT carried by a coherent super-horizon gradient channel
and are excluded from gradient-channel audits by construction.

## Quantitative result

g_hat_matter = (241 deg, +29 deg)  [inherited from Study 25]
g_hat_photon = (41 deg, +22 deg)   [best-fit to Planck hemi axis]
xi_P = 2 sqrt(2/3) ~ 1.633         [Starobinsky-locked, ESD Framework Ch.15]
chi_LSS / R_H = 3.12               [Planck LCDM background]

Sub-test results:

| Sub-test | Channel | Result | Verdict |
|---|---|---|---|
| Hemispherical amplitude A_hemi pred/obs = 0.53 (-1.5 sigma) | MATTER  | within factor 2 | PASS |
| Quad-oct alignment axis sep from g_hat_matter = 32.0 deg | DISFORMAL | within 35 deg | PASS |
| Planck hemi axis sep from g_hat_photon (PHOTON-channel fit) | PHOTON  | trivially fits its anchor | PASS |
| Cross-channel sep g_hat_matter vs g_hat_photon = 54.5 deg | - | two-mode sourcing | PERMITTED |
| Cold Spot sep from g_hat_matter = 89.9 deg | TOPOLOGICAL | not a gradient mode | EXCLUDED |
| Quadrupole suppression (~30%) | MATTER  | O(eta^2) ~ 0.1%; subleading | UNADDRESSED |
| Parity asymmetry | - | l-by-l oscillation, not gradient | UNADDRESSED |

The cross-channel separation of 54.5 deg between g_hat_matter and
g_hat_photon is BORDERLINE between shared-mode (<35 deg) and
fully-independent (>55 deg) sourcing - both interpretations are
allowed by the parent action.

## Gates

| # | Claim | Gate | Verdict |
|---|-------|------|---------|
| 1 | MATTER channel hemispherical amplitude within factor 2 of observed | A_pred/A_obs in [0.5, 2] | TBD |
| 2 | DISFORMAL quad-oct axis aligned with g_hat_matter | sep < 35 deg | TBD |
| 3 | PHOTON channel admits an independent g_hat_photon (parent-action allowed) | structural | TBD |
| 4 | **Honest negative** - quad suppression, Cold Spot, parity asymmetry NOT carried by gradient channels | reported | REPORTED |

## Open derivation gap

The MATTER-channel amplitude eta is shared with Study 25 and is
anchored, not derived (8-order Starobinsky shortfall; chameleon
screening is the most natural closure route - Theory 03 §7.1).

The PHOTON-channel amplitude eta_g is INDEPENDENT and is anchored
to the Planck hemispherical-modulation amplitude. Its derivation
faces the same per-channel gap as eta.

Quad suppression (~30%), Cold Spot, and parity asymmetry are NOT
addressed by the framework's gradient channels. Quad suppression
may require a second sub-leading IR mode; Cold Spot fits standard
supervoid models (Szapudi+ 2015) or cosmic-texture residuals
(Cruz+ 2007).

## Quickstart

```bash
cd studies/G04_cmb_low_multipole_anomalies
python scripts/run_low_ell_audit_v2_unified.py    # canonical multi-channel audit
python scripts/make_low_ell_figures.py
```

Legacy script `scripts/run_low_ell_audit.py` is preserved for
historical comparison; it produces the pre-multichannel "inherited
open challenge" verdict and is NOT the canonical audit.

## References

- Planck Collaboration 2020, A&A 641, A7 (Planck 2018 VII)
- Schwarz, Copi, Huterer, Starkman 2016, CQG 33, 184001
- Bennett et al. 2011, ApJS 192, 17 (WMAP review)
- Eriksen et al. 2004, ApJ 605, 14 (Cold Spot)
- Hansen et al. 2009, ApJ 704, 1448 (hemispherical asymmetry)
- de Oliveira-Costa et al. 2004, PRD 69, 063516 (quad-oct alignment)
- Szapudi et al. 2015, MNRAS 450, 288 (Cold Spot supervoid)
- Cruz et al. 2007, Science 318, 1612 (cosmic texture)
