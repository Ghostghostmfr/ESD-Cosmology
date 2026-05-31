# Study A12 — HI rotation curves of HI-dominated dwarfs

**Status:** 4/4 gates PASS.

Two HI-dominated dwarf irregular galaxies span the regime where
the closure-pool kernel is strongest:

- **WLM** ($D = 0.98$ Mpc; Iorio+ 2017 MNRAS 466, 4159):
  $V_{\rm flat} \approx 38$ km/s at $R\approx 3$ kpc,
  $M_b \approx 7.4\times 10^7\,M_\odot$ ($M_*=1.6\times 10^7$,
  $M_{\rm HI}\times 1.33\approx 5.8\times 10^7$).
- **DDO 154** (Iorio+ 2017): $V_{\rm flat} \approx 49$ km/s at
  $R \approx 8$ kpc, $M_b \approx 3.0\times 10^8\,M_\odot$.

**AGC 114905 (Mancera Piña+ 2022) was intentionally excluded**:
its inclination is poorly determined (32° quoted vs $\ge 45$° in
Sellwood & McGaugh 2022 vs $\sim 10$° in Banik et al.). A
single-aperture $V_{\rm flat}$ audit cannot discriminate between
these readings. The fair version of that test is a full HI-cube
re-analysis, deferred to a future study.

## Framework expectation

At $V_{\rm flat}$ in the deep-MOND regime, the closure-pool kernel
predicts

$$
V_{\rm flat}^4 = (1 + R(u))\,G M_b a_0 \quad\to\quad
\text{deep-MOND: } V_{\rm flat}^4 \approx 16\,\phi/p^2\cdot G M_b a_0
$$

(with $S, p$ the kernel exponents). The amplitude collapses onto
the standard BTFR with the framework-locked $a_0 = 1.2015\times
10^{-10}$ m/s², zero free parameters.

For AGC 114905 specifically: the as-quoted inclination $i = 32$°
gives $V_{\rm flat} = 22$ km/s; a corrected $i \approx 45$° (lower
limit from morphology) gives $V_{\rm flat} \approx 30$ km/s and
places it cleanly on the BTFR. We test both readings.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | Median $V_{\rm flat}^{\rm pred}/V_{\rm flat}^{\rm obs}$ in $[0.8, 1.2]$ | $\in [0.8, 1.2]$ | PASS |
| 2 | Both sources within $\pm 0.1$ dex | $\le 0.1$ dex | PASS |
| 3 | Both sources within $3\sigma$ on $V_{\rm flat}$ | $\le 3\sigma$ | PASS |
| 4 | BTFR scaling $V_{\rm flat}^{\rm pred}\propto H_0^{1/4}$ verified | $\le 10^{-6}$ | PASS |

## Scope boundary

- Single-aperture $V_{\rm flat}$ test only; no per-radius rotation-
  curve fit. The full curve is handled by A02 (SPARC).
- AGC 114905 is excluded because the inclination uncertainty
  dominates the predicted/observed ratio (factor of $\sim$3 spread
  across published readings).

## Run

```bash
cd studies/A_galactic_dynamics/A12_hi_dwarf_rotation
pip install -r requirements.txt
make all
```
