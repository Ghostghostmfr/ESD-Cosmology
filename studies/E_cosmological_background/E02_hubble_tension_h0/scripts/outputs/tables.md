# Study 08 - ESD Hubble-tension paper reproduction (Markdown)

## Quantitative claims of `hubble_paper_v2`

| claim | value | target | metric | verdict |
|---|---:|---:|---|---|
| 1. bridge inversion a0 -> H0 | 67.28 | 67.28 | rel_err = -4.717e-06 | **PASS** |
| 2. Identity (C): 3 Om_DM+Om_b = (18/pi) Om_L^2 Om_m | 0.847 | 0.847 | rel_diff = +1.311e-16 | **PASS** |
| 3. h-blindness Thm 1 on {C1, C4, C7} | 1.079e-11 | 0 | per-child = ['+1.08e-11', '+0.00e+00', '+0.00e+00'] | **PASS** |
| 4. combined 6-channel drift budget | 0.12 | 0.12 | gap_ratio = 47.3x required | **PASS** |
| 5. predicted SH0ES Delta mu_host | 0.1859 | 0.17 | abs_err = +0.016 | **PASS** |

## 6-channel drift budget (paper Table 1)

| ch | mechanism | max \|ΔH_0\| (km/s/Mpc) | status |
|---:|---|---:|---|
| 1 | Disformal photons | 1.20e-01 | active |
| 2 | Running alpha at recombination | 7.00e-09 | active |
| 3 | Newton constant drift | 1.40e-06 | active |
| 4 | N_eff / r_s / w / Omega_K | 0.00e+00 | structurally absent |
| 5 | Bridge x local void | ruled out | ruled out by SPARC |
| 6 | EFE on Cepheid stellar structure | 1.00e-12 | active |
| | **combined finite caps** | **1.200e-01** | dominated by Ch1 |
| | required SH0ES gap | 5.68 | shortfall 47.3x |

## Multi-anchor H_0 table

ESD bridge prediction: **H_0 = 67.28 km/s/Mpc**

| family | anchor | H_0 | sigma | pull vs ESD | reference |
|---|---|---:|---:|---:|---|
| cmb | Planck 2018 (TT,TE,EE+lowE+lensing) | 67.36 | 0.54 | +0.15 | Aghanim+ 2020, A&A 641, A6 |
| cmb | ACT-DR4 + WMAP | 67.60 | 1.10 | +0.29 | Aiola+ 2020, JCAP 12 047 |
| cmb | ACT-DR6 (lensing combined) | 68.10 | 0.90 | +0.91 | Madhavacheril+ 2024, ApJ 962, 113 |
| cmb | SPT-3G TT/TE/EE | 68.30 | 1.50 | +0.68 | Balkenhol+ 2023, PRD 108, 023510 |
| bao_bbn | DESI Y1 BAO + BBN | 68.50 | 0.80 | +1.53 | DESI 2024 VI, arXiv:2404.03002 |
| bao_bbn | BOSS+eBOSS BAO + BBN | 67.40 | 1.10 | +0.11 | Alam+ 2021, PRD 103, 083533 |
| trgb | CCHP TRGB-JWST | 69.85 | 1.95 | +1.32 | Freedman+ 2024, arXiv:2408.06153 |
| trgb | EDD TRGB | 71.50 | 1.80 | +2.34 | Anand+ 2022, ApJ 932, 15 |
| lensing | H0LiCOW (TDCOSMO IV) | 73.30 | 1.80 | +3.34 | Wong+ 2020, MNRAS 498, 1420 |
| lensing | TDCOSMO + ext (hierarchical) | 67.40 | 3.50 | +0.03 | Birrer+ 2020, A&A 643, A165 |
| masers | Megamaser Cosmology Project | 73.90 | 3.00 | +2.21 | Pesce+ 2020, ApJL 891, L1 |
| gw | GW170817 + EM counterpart | 70.00 | 12.00 | +0.23 | Abbott+ 2017, Nature 551, 85 |
| distance | SH0ES 2022 (Cepheid-SN1a) | 73.04 | 1.04 | +5.54 | Riess+ 2022, ApJL 934, L7 |
| distance | SH0ES JWST + HST 2024 | 72.60 | 2.00 | +2.66 | Riess+ 2024, ApJL 962, L17 |
