# Study 09 - GW propagation (disformal photon channel)

Reproduces Channel 1 of Higginson 2026 (Zenodo 10.5281/zenodo.20400097).

| claim | value | target | metric | verdict |
|---|---:|---:|---|---|
| 1. GW170817 |eps_0| bound vs paper 6e-15 | 4.226e-16 | 6e-15 | ratio = 7.044e-02 (naive 1.74s/40Mpc bound) | **PASS** |
| 2. photon-barrier eps_2_max vs paper 5.9e-19 | 5.932e-19 | 5.9e-19 | rel_err = +5.346e-03 | **PASS** |
| 3. saturated Delta H_0 from disformal channel | 0.1141 | 0.12 | DA ratio = 0.998306 | **PASS** |

## Saturated dispersion at the photon-barrier

- eps_0       = 6.000e-15
- eps_2 (max) = 5.932e-19
- D_A ratio   = 0.99830579
- Delta H_0   = +0.1141 km/s/Mpc  (paper cap 0.12)
