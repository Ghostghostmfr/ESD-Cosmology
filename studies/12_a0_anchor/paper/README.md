# Paper notes - Study 12

Primary reference:

> James P. Higginson, *ESD Framework: The Hubble Tension as a
> Structural h-Blindness Boundary and Mirror-Identity Classification
> of Dark Energy* (2026). Zenodo DOI:
> [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

Study 12 is a cross-anchor consistency audit linking the C1 bridge
of the Hubble paper to every other study in the suite that uses `a_0`:

| § in paper                          | claim                                      | study artifact                              |
|-------------------------------------|--------------------------------------------|---------------------------------------------|
| Children list, item C1              | `a_0 = c H_0 sqrt((3 Om_DM + Om_b)/(8 pi))`| `esd_core.cosmology.a_zero`                 |
| Theorem 1 (h-blindness), C1 row     | `d a_0 / d h = 0` in omega-vars            | `scripts/esd_anchor.py::a0_h_blindness`     |
| Bridge inversion (Study 08, C1)     | `H_0 = a_0 / (c sqrt(idB/8pi))`            | `scripts/esd_anchor.py::bridge_inversion_H0`|
| McGaugh+2016 RAR anchor (Study 05)  | `a_0 = 1.20 +/- 0.02 x 10^-10 m/s^2`       | claim 2 in `run_anchor_audit.py`            |

This study quantifies how the local-vs-CMB `H_0` tension manifests
as a ~9% mismatch in the inferred `a_0` anchor; Theorem 1 implies
that mismatch cannot be moved internally without violating one of
the ESD-distinctive children.
