# Study B03 — Double + triple pulsar strong-field timing

**Status:** 4/4 gates PASS at the closure-pool kernel level.

Pulsars in compact relativistic binaries are the cleanest strong-field
GR laboratories outside black-hole horizons. Two systems matter here:

- **J0737-3039A/B** — the double pulsar (Kramer+ 2021, PRX 11, 041050).
  Eight post-Keplerian parameters measured at $\sim 10^{-4}$
  fractional precision; relativistic mass measurement at the 0.013%
  level on the pulsar mass.
- **J0337+1715** — the millisecond pulsar in a triple system with two
  white dwarfs (Ransom+ 2014, Nature 505; Archibald+ 2018,
  Nature 559, 73; Voisin+ 2020, A&A 638, A24). Provides the strongest
  strong-field equivalence-principle test ever performed:
  $|\Delta| < 1.8\times 10^{-6}$ (95% CL).

## Framework expectation

At pulsar-binary accelerations $g \sim 10$ m/s² (compact orbit) and
internal NS surface $g \sim 10^{12}$ m/s², $u = g/a_0 \gg 10^{10}$,
so the closure-pool kernel $R(u) \to S/u^p \to 0$ to far below current
measurement precision. ESD reduces *identically* to GR in this regime
(Study 19 applicability theorem).

The fair tests here are therefore:

1. The kernel really does deliver $R(u) < 10^{-6}$ at orbital scale.
2. The kernel really does deliver $R(u_\star) < 10^{-9}$ at NS surface
   scale (so that the strong-EP test of J0337 is honored).
3. The predicted post-Keplerian parameters of J0737 agree with GR
   (and therefore observation) to within their measurement errors.
4. h-blindness: the prediction is independent of $H_0$.

This is a structural-consistency test of the *limit* of the closure-
pool kernel, not a fit. Any nonzero $R(u)$ at these accelerations
would have produced a measurable strong-EP violation or a deviation
in J0737's post-Keplerian closure long ago.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | Kernel suppression at J0737 orbital scale, $R(u_{\rm orb}) \le 10^{-6}$ | $\le 10^{-6}$ | PASS |
| 2 | Kernel suppression at NS surface, $R(u_\star) \le 10^{-9}$ | $\le 10^{-9}$ | PASS |
| 3 | Predicted GR post-Keplerian closure consistent with Kramer+ 2021 to 0.1% | $\le 10^{-3}$ | PASS |
| 4 | h-blindness: $|R(u; H_0{=}60) - R(u; H_0{=}80)|$ well below test threshold | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/B_solar_system/B03_pulsar_timing_double_triple
pip install -r requirements.txt
make all
```

## Scope boundary

- Post-Keplerian closure is computed at the 1PN-with-GR-2PN-mass
  level using the Damour–Deruelle parameterization, not a full
  TEMPO2/Enterprise fit.
- This study certifies that ESD does not break a strong-field test
  it cannot improve. The non-trivial science is the *value* of
  $R(u)$ at $u\gg 10^{10}$, which is reported.
