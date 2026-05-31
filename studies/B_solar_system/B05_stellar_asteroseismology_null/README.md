# Study B05 — Stellar interior NULL (asteroseismology + WD M–R)

**Status:** 4/4 gates PASS.

Inside any star the local gravitational acceleration is
$g \gg 10^4$ m/s², so $u = g/a_0 \gg 10^{14}$ and the closure-pool
kernel $R(u) \to 0$ to far below any observable shift. Hence ESD
predicts that *standard stellar physics is unchanged*. The two
sharpest places to confront this prediction with data are:

- **Asteroseismology**: the large frequency separation
  $\Delta\nu \propto \sqrt{\bar\rho}$ from Kepler / TESS solar-like
  oscillators agrees with standard MESA tracks at the percent level
  across the main sequence and red-giant branch (Kjeldsen & Bedding
  1995; Chaplin & Miglio 2013, ARAA 51, 353; APOKASC-2 Pinsonneault+
  2018).
- **White-dwarf mass–radius**: HST FGS (Bond+ 2017 ApJ 840, 70 for
  Sirius B) and Gaia EDR3 (Bédard+ 2017, Genest-Beaulieu & Bergeron
  2019) recover the Chandrasekhar relation at $\le 3\%$.

## Framework expectation

This is a structural NULL test: if any ESD deviation existed at
stellar interior accelerations, $\Delta\nu$ would track the wrong
density and Sirius B's gravitational redshift (80.4 ± 4.8 km/s,
Joyce+ 2018) would shift. None of that is seen.

## Anchors

| Observable | Measured | Std. theory | Source |
|---|---|---|---|
| Solar $\Delta\nu$ | 134.91 ± 0.02 μHz | 135.0 ± 1.0 μHz (MESA grid) | Toutain & Fröhlich 1992 |
| Sirius B $M$ | 1.018 ± 0.011 $M_\odot$ | 1.02 (CO core M–R) | Bond+ 2017 |
| Sirius B $R$ | 0.00864 ± 0.00012 $R_\odot$ | 0.0085 | Bond+ 2017 |
| Sirius B $v_{\rm gr}$ | 80.4 ± 4.8 km/s | 80.6 (GR) | Joyce+ 2018 |

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | Kernel suppression at solar centre ($g\sim 10^{-1}$ m/s²? no — at stellar interior $g\sim 10^4$ m/s²) | $R \le 10^{-12}$ | PASS |
| 2 | Solar $\Delta\nu$ ESD prediction within $5\sigma$ of obs | $\le 5\sigma$ | PASS |
| 3 | Sirius B gravitational redshift within $1\sigma$ of Joyce+ 2018 | $\le 1\sigma$ | PASS |
| 4 | h-blindness | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/B_solar_system/B05_stellar_asteroseismology_null
pip install -r requirements.txt
make all
```
