# Paper notes - Study 09

Primary reference:

> James P. Higginson, *ESD Framework: The Hubble Tension as a Structural
> h-Blindness Boundary and Mirror-Identity Classification of Dark Energy*
> (2026). Zenodo DOI: [10.5281/zenodo.20400097](https://doi.org/10.5281/zenodo.20400097).
> Local source: `Research/ESD_Supporting_Papers/hubble_tension/hubble_paper_v2.tex`.

Study 09 reproduces Channel 1 of that paper's Sec. "Closure of
internal channels":

| § in paper                              | claim                                 | study artifact                                  |
|-----------------------------------------|---------------------------------------|-------------------------------------------------|
| Channel 1 -- "disformal photons"        | `|eps_0| < 6e-15` from GW170817       | `scripts/esd_gw.py::gw170817_eps0_bound`        |
| Channel 1 -- "photon-barrier condition" | `eps_2 <= 5.9e-19` from `c_gamma^2 >= 0` | `scripts/esd_gw.py::eps2_max_from_barrier`     |
| Table 1                                 | `max |Delta H_0| ~ 0.12 km/s/Mpc`     | `scripts/esd_gw.py::delta_H0_from_dispersion`   |

Each is checked against a publishable gate in `run_gw_audit.py`.
Exit code 0 iff all 3 claims reproduce.

The companion file used by the published paper for the full
disformal-disformal calculation is
`Research/ESD_Supporting_Papers/hubble_tension/lambda_bridge_reflection13.py`;
Study 09 only needs the saturated-dispersion subset, so it does not
import that file.
