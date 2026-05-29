# Paper notes - Study 11

Primary reference:

> James P. Higginson, *ESD Framework: The Hubble Tension as a
> Structural h-Blindness Boundary and Mirror-Identity Classification
> of Dark Energy* (2026). Zenodo DOI:
> [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

Study 11 reproduces child C7 from the paper's "Children list" and
Theorem 1:

| § in paper                       | claim                                | study artifact                              |
|----------------------------------|--------------------------------------|---------------------------------------------|
| Children list, item C7           | `lambda_J ~ 94 kpc`, set by `m_D`    | `scripts/esd_jeans.py::lambda_J_comoving_m` |
| Theorem 1 (h-blindness), C7 row  | `d lambda_J / d h = 0` at fixed `omega_m` | `scripts/esd_jeans.py::h_blindness_C7`    |
| (parametric)                     | `lambda_J ~ m_D^{-1/2}` ultralight   | claim 3 in `run_jeans_audit.py`             |

The paper's symbolic expression
`lambda_J = (pi/m_D) sqrt(c_s^2 / (G rho_m a^3))` is implemented
through the unit-clean Hu-Barkana-Gruzinov 2000 quantum-Jeans
length, which agrees to within a factor of 2 (order-unity convention).
The Theorem 1 structural content -- h-independence in
physical-density variables -- is identically satisfied.
