# Study C05 — Black-hole ringdown QNM spectroscopy

**Status:** 4/4 gates PASS.

Following a binary BH merger, the remnant settles into a Kerr BH by
emitting a superposition of quasi-normal modes (QNMs). Each mode
$(\ell, m, n)$ is fully fixed by the final mass $M_f$ and spin
$\chi_f$ in pure GR (no-hair theorem). Deviations from the GR QNM
spectrum directly bound any modification of the strong-field
metric near the horizon.

LVK has reported high-confidence QNM detections for several O3/O4
events; the headline events used here are:

- **GW150914** (Abbott+ 2016, PRL 116, 061102 + Isi+ 2019,
  PRL 123, 111102): $f_{220} = 251.5^{+9.2}_{-12.6}$ Hz,
  $\tau_{220} = 4.0^{+1.7}_{-2.5}$ ms.
- **GW190521** (Abbott+ 2020, PRL 125, 101102): final
  $M_f = 142^{+28}_{-16}\,M_\odot$, $\chi_f = 0.72^{+0.09}_{-0.12}$.
- **GW200129** (Capano+ 2023, Nat. Astron. 7, 1185): high-SNR
  220 + 221 detection.

## Framework expectation

At the photon sphere $r = 3GM_f/c^2$, $g \sim c^2/(3GM_f)\cdot c^2/r$
is enormous; $u \gg 10^{30}$ for stellar-mass BHs. Closure-pool
kernel $R(u)$ vanishes far below current LVK uncertainty
($\sim 5\%$). ESD predicts the Kerr QNM spectrum identically.

The fair tests:

1. $R(u_{\rm photon})$ at GW150914's photon sphere $\le 10^{-12}$.
2. Predicted $f_{220}$ for GW150914 from Berti–Cardoso–Will fits
   within 1$\sigma$ of Isi+ 2019.
3. Predicted $\tau_{220}$ within $1\sigma$.
4. h-blindness.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm photon}) \le 10^{-12}$ | $\le 10^{-12}$ | PASS |
| 2 | $f_{220}$ within $1\sigma$ of Isi+ 2019 | $\le 1\sigma$ | PASS |
| 3 | $\tau_{220}$ within $1\sigma$ of Isi+ 2019 | $\le 1\sigma$ | PASS |
| 4 | h-blind | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/C_gravitational_waves/C05_bh_ringdown_qnm
pip install -r requirements.txt
make all
```
