# Paper notes - Study 10

Primary reference:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).

Study 10 reproduces child C4 from that paper's "Children list" and
"h-blindness theorem" sections:

| § in paper                                | claim                                | study artifact                              |
|-------------------------------------------|--------------------------------------|---------------------------------------------|
| Children list, item C4                    | `M_tot/M_b = (1 + R(u_cl)) + Om_DM/Om_b` | `scripts/esd_cluster.py::M_tot_over_M_b`    |
| Theorem 1 (h-blindness) -- C4 entry       | `d R_4 / d h = 0` at fixed (M, R, omegas) | `scripts/esd_cluster.py::h_blindness_C4`    |
| Closure of internal channels (asymptote)  | deep-Newton recovers cosmic f_b      | claim 3 in `run_cluster_audit.py`           |

The screening function `Sigma(u) = u^p + b u^q + c` is the same one
defined throughout the ESD framework (parent action). Constants
(`p = phi`, `q = 2 ln(phi)/phi`, `b = phi^6 - 2`,
`c = (4 ln(phi) - 1)/phi`, `s = 16 phi + 1`) are locked by the
closure pool with no continuous free parameters.
