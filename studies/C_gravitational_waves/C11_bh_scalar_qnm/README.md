# C11 --- Black-hole scalar quasi-normal modes

**Question.** Does the ESD D-field (the framework's scalar degree of
freedom) excite an *extra* spin-0 ringdown branch on top of GR's tensor
quasi-normal-mode (QNM) spectrum? Study C05 covers the standard tensor
220 mode; this study is the distinct test for a scalar (spin-0) mode.

**ESD prediction (zero free parameters).** By the GW-sector
applicability theorem (Study C02) the ESD tensor sector reduces to GR,
and near the horizon `u = 4 g / a0` is deep in the high-`u` regime where
the locked closure kernel `R(u) -> 0`. The D-field therefore decouples
from the radiative dynamics: the remnant carries no scalar charge and
the scalar QNM amplitude vanishes,

```
A_scalar^ESD = 0 ,   Q_scalar^ESD = 0 ,   |A_scalar^ESD - 0| <= R(u_horizon).
```

ESD inherits GR's purely tensorial, no-hair ringdown. The module also
reports the scalar `ell=0` QNM frequency a radiating D-field *would*
produce (`M*omega ~ 0.1105 - 0.1049 i`), so the null is explicit and
falsifiable: a confirmed scalar/non-tensorial mode would break it.

**Data.** No statistically significant scalar component is found in
GW polarization or ringdown-spectroscopy searches (GW170814
polarization, Abbott+ 2017; Isi+ 2019 ringdown spectroscopy; GWTC-3
tests of GR, Abbott+ 2021). The null discriminates against
scalar-tensor / Brans-Dicke, Einstein-dilaton-Gauss-Bonnet, and hairy
(massive-scalar) black holes.

## Run

```
pip install -r requirements.txt
make            # audit + figure
```

`from esd_core import a_zero` supplies the locked `a0(H0)`; sibling
modules are imported via a local `sys.path` insert, so the study is
fully self-contained and uses only relative paths.

## Gates (all PASS)

1. `R(u)` at the BH horizon (62 Msun) `<= 1e-12`.
2. No-hair: scalar amplitude `=` scalar charge `= 0` (bound `<= 1e-12`).
3. ESD scalar amplitude `0` inside every polarization/mode search bound.
4. No confirmed (`>= 5 sigma`) scalar-mode / non-tensorial detection.
5. `H0`-blindness: `|dR|` across `H0 in [60,80]` `<= 1e-6`.
