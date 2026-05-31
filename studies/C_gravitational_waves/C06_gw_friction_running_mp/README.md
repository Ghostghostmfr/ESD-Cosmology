# Study C06 — GW friction / running Planck mass

**Status:** 4/4 gates PASS.

Modified-gravity theories with a time-varying effective Planck mass
predict a GW luminosity-distance distinct from the EM one:

$$
\frac{d_L^{\rm GW}(z)}{d_L^{\rm EM}(z)} =
\exp\!\left[-\tfrac{1}{2}\int_0^z\frac{\alpha_M(z')}{1+z'}\,dz'\right].
$$

A non-zero $\alpha_M$ (running Planck mass) would show up as a
mismatch between the GW-inferred distance and the host-galaxy EM
distance. LVK GWTC-3 + GW170817 bound $\alpha_M$ near zero
(Mukherjee+ 2021, MNRAS 502 1136; Lagos+ 2019, PRD 99 083504).

## ESD prediction

The ESD parent action puts the metric, the displacement scalar $D$,
and $A_\mu$ in one Lagrangian. The tensor (graviton) sector reduces
identically to GR (see `theory/02_vacuum_lambda` and Study 19): no
running Planck mass, $\alpha_M = 0$, no extra GW friction. The
predicted ratio is $d_L^{\rm GW}/d_L^{\rm EM} = 1$ identically.

## Anchors

| source | $d_L^{\rm EM}$ (Mpc) | $d_L^{\rm GW}$ (Mpc) | ref |
|---|---|---|---|
| GW170817 / NGC 4993 | 40.7 ± 2.4 | 43.8 +2.9 −6.9 | Abbott+ 2017 PRL 119 161101 |

| LVK + GWTC-3 dark-siren bound | value | ref |
|---|---|---|
| $\alpha_M$ (90% CL, Mukherjee+ 2021) | $-3.2^{+3.4}_{-3.4}$ | MNRAS 502 1136 |

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | Predicted $\alpha_M = 0$ (structural; tensor sector ≡ GR) | $|\alpha_M| \le 10^{-12}$ | PASS |
| 2 | $d_L^{\rm GW}/d_L^{\rm EM}$ at GW170817 within 1σ of 1 | $\le 1$ σ | PASS |
| 3 | Predicted $\alpha_M$ inside LVK O3 90% CL | $|\alpha_M^{\rm pred}| \le 6.6$ | PASS |
| 4 | h-blindness: $\alpha_M$ at $H_0 \in \{60,80\}$ identical | $\le 10^{-12}$ | PASS |

## Run

```bash
cd studies/C_gravitational_waves/C06_gw_friction_running_mp
pip install -r requirements.txt
make all
```
