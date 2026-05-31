# Study 27 — MICROSCOPE Weak Equivalence Principle (Touboul+ 2022)

**Status:** GATES PENDING — run `make all` to evaluate.

Lifts the ESD Framework Book Ch. 4 WEP-violation prediction into a self-contained
audit against the MICROSCOPE final-data bound

$$|\eta_\mathrm{Pt-Ti}| < 2.7 \times 10^{-15} \quad (95\%\ \text{CL,
Touboul et al.\ 2022, PRL 129, 121102}).$$

## ESD prediction (ESD Framework Book Ch. 4 §4.7)

The parent action couples matter through two scalar channels:

1. **Universal conformal map** $\tilde g_{\mu\nu} = A^2(D)\,g_{\mu\nu}$ with
   coupling strength $\beta_m$. This piece is **species-independent** —
   it renormalises Newton's constant but produces **no** fifth force
   visible to the EP.
2. **Gauge bridge** through $Z(D) F^2$ with coupling strength
   $\beta_Z(u)$. This piece couples to the EM binding fraction
   $f_{\mathrm{EM},A} = E_\mathrm{EM} / (m_A c^2)$, which **is**
   species-dependent.

The species-resolved effective scalar charge is

$$\alpha_A(u) \;=\; \beta_m + \beta_Z(u)\, f_{\mathrm{EM},A}.$$

The Eötvös ratio between two test masses A, B in a common potential
sourced by an unscreened mass M is

$$\eta_{A,B}(u) \;=\; \beta_m^2(u)\,
  \bigl(\beta_Z/\beta_m\bigr)(u)\, |\Delta f_\mathrm{EM}|,$$

where the universal $\beta_m^2$ piece is the *screening factor*
inherited from the Cassini PPN bound, and $\beta_Z/\beta_m$ is the
*channel ratio* set by the framework's gauge-cascade.

## Numerical inputs (all framework-derived, no fits)

| Quantity | Value at Earth | Source |
|---|---|---|
| $\beta_m^2(u_\oplus)$ | $\sim 10^{-9}$ | ESD Framework Ch. 4 Cassini-anchored PPN |
| $(\beta_Z/\beta_m)(u_\oplus)$ | $\simeq 2.6 \times 10^{-11}$ | ESD Framework Ch. 4 channel-ratio running |
| $\Delta f_\mathrm{EM}^\mathrm{Pt-Ti}$ | $\sim 10^{-3}$ | nuclear EM binding tables |

## Predicted signal

$$\eta_\mathrm{Pt-Ti}^\mathrm{ESD} \;\sim\; 10^{-9} \cdot 2.6\!\times\!10^{-11}
   \cdot 10^{-3} \;\sim\; 2.6 \times 10^{-23},$$

**eight orders of magnitude below the MICROSCOPE bound** and **six
orders below the projected MICROSCOPE-2 sensitivity** $(\sim 10^{-17})$.
The same $\beta_m^2$ screening that delivers GR recovery in the
gravity sector therefore delivers EP safety automatically. This is the
structural reason ESD is not in tension with MICROSCOPE.

## Gates

| # | Claim | Gate | Verdict |
|---|-------|------|---------|
| 1 | $|\eta_\mathrm{ESD}|$ below MICROSCOPE 2022 bound $2.7\!\times\!10^{-15}$ | $|\eta_\mathrm{ESD}/\eta_\mathrm{bound}| < 1$ | TBD |
| 2 | $|\eta_\mathrm{ESD}|$ below MICROSCOPE-2 forecast $\sim 10^{-17}$ | $|\eta_\mathrm{ESD}|/10^{-17} < 1$ | TBD |
| 3 | $\beta_m^2$ screening factor consistent with Cassini PPN | $\beta_m^2(u_\oplus) \le 10^{-8}$ | TBD |
| 4 | Headroom reported (orders of magnitude below each bound) | report | REPORTED |

Gates 1, 2, 3 are expected to **PASS** by 8, 6, and 1 orders respectively.

## References

- Touboul et al.\ 2022, PRL 129, 121102 (MICROSCOPE final result)
- Bergé et al.\ 2018, PRL 120, 141101 (MICROSCOPE-2 forecast)
- ESD Framework Book Ch. 4 §4.7 (Higginson 2026, channel-ratio derivation)
- ESD Framework Book Ch. 16 Prediction 2 (MAGIS / Sr–Yb optical clock parallel)
- Bertotti, Iess, Tortora 2003, Nature 425, 374 (Cassini PPN γ-1)

## Quickstart

```bash
cd studies/B01_equivalence_principle_microscope
python scripts/run_wep_audit.py
python scripts/make_wep_figures.py
```
