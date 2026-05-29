# Paper notes — Study 08

Primary reference:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).
> Local source: `Research/ESD_Supporting_Papers/hubble_tension/hubble_paper_v2.tex`.

Study 08 reproduces the five quantitative claims of that paper:

| § in paper                        | claim                            | study artifact                |
|-----------------------------------|----------------------------------|-------------------------------|
| Eq. bridge-published / abstract   | H_0 = 67.28 from a_0             | `scripts/esd_h0.py::bridge_inversion_H0` |
| Reflection-19, Eq. (C)            | 3 Ω_DM + Ω_b = (18/π) Ω_Λ² Ω_m   | `scripts/esd_h0.py::identity_C_residual` |
| Theorem 1                         | h-blindness on {C1,C4,C7}        | `scripts/esd_h0.py::h_blindness_check`   |
| Table 1                           | 6-channel drift budget ≤ 0.12    | `scripts/channels.py`                    |
| Sec. *calibration_bias*           | predicted Δμ_host = 0.17 mag     | `scripts/esd_h0.py::shoes_calibration_bias_mag` |

Each is checked against a publishable gate in `run_hubble_audit.py`.
Exit code 0 iff all 5 claims reproduce.
