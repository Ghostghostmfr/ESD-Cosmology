# Study 24 — ACT DR6 CMB lensing vs ESD's locked $S_8^{\mathrm{CMBL}}$

**Status:** PASS (audit complete)
**Datasets:** ACT DR6 lensing (Madhavacheril et al. 2024, ApJ 962, 113)
**ESD inputs (locked):** Paper 1 Identity B locks $\Omega_m = 0.31574$; Study 19
shows the linear growth equation is unmodified, so $\sigma_8^{\mathrm{ESD}} =
\sigma_8^{\Lambda\mathrm{CDM}} = 0.8111$ (Planck 2018).

## What this study tests

ACT DR6 reconstructs the CMB lensing convergence on a sky fraction
$f_{\rm sky} \approx 0.23$ and reports a high-precision measurement of
the structure-growth amplitude in the **CMB-lensing combination**

$$
S_8^{\mathrm{CMBL}} \equiv \sigma_8 \left(\frac{\Omega_m}{0.3}\right)^{0.25}
$$

(note the exponent $0.25$, not the cosmic-shear $0.5$). Headline values
from Madhavacheril et al. 2024:

| analysis            | $S_8^{\mathrm{CMBL}}$  |
|---------------------|------------------------|
| ACT DR6 only        | $0.818 \pm 0.022$      |
| ACT DR6 + Planck NPIPE | $0.840 \pm 0.018$  |

The ACT lensing kernel peaks at $z \sim 1\text{-}2$ and $k \sim 0.1\,h/$Mpc,
firmly in the **linear** regime, so Study 19's conclusion applies: ESD does
not modify the predicted $\sigma_8$. The ESD prediction is therefore

$$
S_8^{\mathrm{CMBL,\,ESD}}
= \sigma_8^{\mathrm{Planck}} \left(\frac{\Omega_m^{\mathrm{lock}}}{0.3}\right)^{0.25}
= 0.8111 \cdot (1.05247)^{0.25}
\approx 0.8216 .
$$

This is a **closure-pool prediction**: no per-survey free parameters.

## What this study does not do

- It does not re-run the lensing reconstruction pipeline (that requires
  the full 6 TB ACT DR6 maps + the NPIPE NERSC pipeline).
- It does not fit a cosmology to the bandpowers. It compares the
  closure-pool-locked headline $S_8^{\mathrm{CMBL}}$ against the
  collaboration's published headline posterior.
- It does not test nonlinear scales; those belong to Studies 18 and 19.

## Pass criterion

A standard 3-σ compatibility threshold (the same threshold used in
Study 23). The audit script prints both the ACT-only and ACT+NPIPE
tensions; the headline ACT-only number is used for the gate.

## Files

- `scripts/observations.py` — published ACT DR6 lensing values.
- `scripts/esd_lensing.py` — ESD's $S_8^{\mathrm{CMBL}}$ prediction.
- `scripts/run_act_lensing_audit.py` — pass/fail audit gate.
- `scripts/make_act_lensing_figures.py` — figures.
- `paper/README.md` — write-up placeholder.

## Reproduction

```bash
cd studies/F07_act_dr6_cmb_lensing
pip install -r requirements.txt
make all
```
