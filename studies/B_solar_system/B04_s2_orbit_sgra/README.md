# Study B04 — S2 stellar orbit at Sgr A*

**Status:** 4/4 gates PASS.

The S-cluster star S2/S0-2 completes a 16-yr orbit around Sgr A*
with periastron 120 AU = 1400 $r_s$ (GRAVITY Collaboration 2018,
A&A 615, L15; 2020, A&A 636, L5; Do+ 2019, Science 365, 664).
The Schwarzschild precession of the orbit is measured at

$$
f_{\rm SP} = 1.10 \pm 0.19\quad\text{(GRAVITY+ 2020, A\&A 636, L5)}
$$

(1 = full GR; 0 = pure Newton). This is the only stellar-orbit
strong-field GR test at galactic-center scales.

## Framework expectation

At S2 periastron, $g \sim G M_\bullet / r_p^2 \sim 5\times 10^{-2}$
m/s², so $u = g/a_0 \sim 4\times 10^8 \gg 1$. The closure-pool
kernel $R(u) \ll 10^{-10}$, well below the GRAVITY precession
fractional uncertainty (17%). ESD reduces to GR identically here.

The fair test is therefore:

1. Kernel suppression at S2 periastron: $R(u_p) \le 10^{-6}$.
2. The framework's predicted $f_{\rm SP}$ (= 1 to machine precision)
   is consistent with the GRAVITY+ 2020 measurement at $\le 1\sigma$.
3. Kernel suppression even at S2 *apoapsis* (the lowest-$g$ point
   on the orbit): $R(u_a) \le 10^{-4}$.
4. h-blindness: framework $f_{\rm SP}$ does not depend on $H_0$.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm peri}) \le 10^{-6}$ | $\le 10^{-6}$ | PASS |
| 2 | $f_{\rm SP}^{\rm pred} = 1$ within $1\sigma$ of GRAVITY+ 2020 | $\le 1\sigma$ | PASS |
| 3 | $R(u_{\rm apo}) \le 10^{-4}$ | $\le 10^{-4}$ | PASS |
| 4 | h-blind ($|f_{\rm SP}(60)-f_{\rm SP}(80)| \le 10^{-6}$) | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/B_solar_system/B04_s2_orbit_sgra
pip install -r requirements.txt
make all
```
