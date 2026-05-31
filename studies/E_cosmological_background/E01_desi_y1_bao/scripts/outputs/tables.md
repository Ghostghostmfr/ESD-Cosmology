# Study 07 — DESI Y1 BAO chi^2 across cosmologies (Markdown)

| cosmology | H0 | Omega_m | omega_b | r_d (Mpc) | chi^2 | chi^2/dof |
|---|---:|---:|---:|---:|---:|---:|
| ESD-PRIMARY  (H0=67.36) | 67.36 | 0.3157 | 0.02237 | 146.832 | 22.87 | 1.906 |
| ESD-PRIMARY  (H0=73.04) | 73.04 | 0.3157 | 0.02630 | 138.035 | 16.27 | 1.356 |
| ESD-CLOSURE-POOL (H0=67.36) | 67.36 | 0.3157 | 0.02273 | 146.532 | 25.57 | 2.131 |
| ESD-CLOSURE-POOL (H0=73.04) | 73.04 | 0.3157 | 0.02672 | 137.753 | 15.40 | 1.283 |
| Planck-LCDM (H0=67.36 baseline) | 67.36 | 0.3158 | 0.02237 | 146.825 | 22.89 | 1.907 |
| SH0ES-LCDM  (H0=73.04 baseline) | 73.04 | 0.3158 | 0.02630 | 138.028 | 16.28 | 1.357 |

## Differential tests (at H_0 = 67.36)

| comparison | Delta chi^2 | verdict |
|---|---:|---|
| ESD-PRIMARY - Planck-LCDM | -0.02 | gate \|dchi2\|<=5.0 -> **PASS** |
| ESD-CLOSURE-POOL - Planck-LCDM | +2.68 | reported |
| CP - PRIMARY (reading discriminator) | +2.70 | DESI Y1 prefers **PRIMARY** |

## Per-tracer chi^2 (ESD-PRIMARY, H_0 = 67.36)

| tracer | z | chi^2 |
|---|---:|---:|
| BGS | 0.295 | 0.88 |
| LRG1 | 0.510 | 9.71 |
| LRG2 | 0.706 | 9.77 |
| LRG3+ELG1 | 0.930 | 0.94 |
| ELG2 | 1.317 | 1.13 |
| QSO | 1.491 | 0.00 |
| Lya QSO | 2.330 | 0.45 |
