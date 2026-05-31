# Study C08 — BH spin distribution & Kerr extremality

**Status:** 4/4 gates PASS.

Astrophysical black-hole spin measurements come from two independent
channels:
- **X-ray reflection spectroscopy** of stellar-mass BH X-ray binaries
  (Reynolds 2021 ARA&A 59 117) and AGN, where the inner-disk
  truncation at the ISCO sets the Fe Kα line profile;
- **LVK GWTC-3 merger-remnant spin distribution** (Abbott+ 2023
  Phys. Rev. X 13 011048).

The Thorne (1974) bound caps spin at $\chi \le 0.998$ for any
accretion-driven BH. Observed maxima approach this bound (GRS
1915+105 $\chi \gtrsim 0.98$; MCG-6-30-15 $\chi \gtrsim 0.97$).

## ESD prediction

The ESD tensor sector reduces identically to GR (Study 19). The
predicted Kerr ISCO frequency at maximal spin is:

$$
f_{\rm ISCO}(M, \chi) = \frac{c^3}{2\pi G M}\, F(\chi),
$$

with $F(\chi)$ the standard Kerr radial function. At the ISCO,
$g_{\rm ISCO}\sim 10^{12}$–$10^{14}$ m s$^{-2}$, $R(u_{\rm ISCO})
\le 10^{-15}$, so ESD reproduces Kerr to machine precision.

## Anchors

| object | channel | $\chi$ measured | ref |
|---|---|---|---|
| GRS 1915+105       | X-ray reflection | $> 0.98$    | McClintock+ 2006 |
| MCG-6-30-15        | X-ray reflection | $> 0.97$    | Brenneman & Reynolds 2006 |
| GW150914 remnant   | GW ringdown      | $0.67 \pm 0.05$ | Abbott+ 2016 |
| GWTC-3 max remnant | GW ringdown      | $\sim 0.87$ | Abbott+ 2023 |
| Thorne 1974 bound  | theory          | $\le 0.998$ | ApJ 191 507 |

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm ISCO})$ at $\chi=0.998$, $M=10\,M_\odot$ $\le 10^{-15}$ | $\le 10^{-15}$ | PASS |
| 2 | Predicted Thorne bound $\chi_{\max} = 0.998$ | $= 0.998$ | PASS |
| 3 | All 4 observed $\chi$ values $\le \chi_{\max}$ | inside | PASS |
| 4 | h-blindness: $|R(60)-R(80)|$ at ISCO $\le 10^{-6}$ | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/C_gravitational_waves/C08_bh_spin_kerr_extremality
pip install -r requirements.txt
make all
```
