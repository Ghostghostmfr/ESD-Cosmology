# Study 10 - ESD cluster ratio C4 audit (Markdown)

Reproduces child C4 of Higginson 2026 (Zenodo 10.5281/zenodo.20400097).

## Claims

| claim | value | target | metric | verdict |
|---|---:|---:|---|---|
| 1a. C4 vs direct R_500c f_b (max pull) | 0.8146 | 0 | 3 R_500c samples (X-COP, Planck-SZ, CHEX-MATE) | **PASS** |
| 1b. C4 vs R_200c extrapolations (max pull) | 2.515 | 0 | 2 R_200c samples (model-dependent extrap.) | **PASS** |
| 2. h-blindness of C4 (Thm 1) | 0 | 0 | M_tot/M_b = 7.4878 | **PASS** |
| 3. cosmic asymptote f_b(u->inf) = Omega_b/Omega_m | 0.1587 | 0.1587 | rel_err = -8.353e-10 | **PASS** |

## Per-sample comparison

| sample | radius | u_cl | R(u) | f_b pred | f_b obs | pull | reference |
|---|---|---:|---:|---:|---:|---:|---|
| X-COP (12 nearby clusters) | R_500c | 1.61 | 1.123 | 0.1347 | 0.1310 | -0.73 | Eckert+ 2019, A&A 621, A40 |
| X-COP extrapolated to R_200c | R_200c | 0.68 | 1.953 | 0.1211 | 0.1460 | +2.49 | Eckert+ 2019, A&A 621, A40 |
| Planck SZ baryon census | R_500c | 1.65 | 1.107 | 0.1350 | 0.1260 | -0.81 | Planck 2015 XXIV, A&A 594, A24 |
| CHEX-MATE relaxed subset | R_500c | 1.65 | 1.107 | 0.1350 | 0.1350 | +0.00 | CHEX-MATE Collaboration 2024, A&A 686, A185 |
| XMM Cluster Outskirts Project (XCOP-extreme) | R_200c | 0.84 | 1.709 | 0.1248 | 0.1550 | +2.52 | Ettori+ 2019, A&A 621, A39 |
