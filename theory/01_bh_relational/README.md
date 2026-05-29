# Theory 01 — ESD relational view of black holes

**Status:** 8/8 theory claims PASS. First entry in the
`theory/` track, separate from the reproduction-track `studies/`.

## What this folder does

Three independent theory derivations built on Paper 1's axioms
(A1)–(A3), applied to the strong-field regime around black holes.

| | Derivation | Result |
|---|---|---|
| **A** | Bekenstein–Hawking entropy applicability | R(u) does NOT dress the horizon area; ESD inherits S_BH = A/(4 l_P²) from GR |
| **B** | Singularity-resolution theorem | R(u) = s/Σ(u) is regular for all u ≥ 0; R(u) → 0 in the UV (r → 0) |
| **C** | Horizon as the relational boundary of R(u) | Every astrophysical horizon has u ≫ 1 and R(u) ≪ 1; the MOND-scale shell sits *far outside* the horizon |

## Derivation A — S_BH applicability theorem

The Schwarzschild horizon is a vacuum geometric property of the
spacetime, not a localized massive subsystem.

- **(A1) fails**: no system/spectator split internal to the horizon area itself.
- **(A2) fails**: the horizon is not a bound test mass whose g can be dressed.

Therefore R(u) does NOT modify S_BH. ESD inherits the
Bekenstein–Hawking law exactly:

$$S_{BH} = \frac{A}{4 l_P^2}, \qquad T_H = \frac{\hbar c^3}{8\pi G M k_B}.$$

For M = 1 M_⊙: S_BH/k_B ≈ 1.05 × 10⁷⁷, T_H ≈ 6.2 × 10⁻⁸ K.
For M87*: S_BH/k_B ≈ 4.4 × 10⁹⁶.

## Derivation B — Singularity-resolution theorem

The closure-pool kernel is

$$R(u) = \frac{s}{\Sigma(u)}, \qquad \Sigma(u) = u^p + b\,u^q + c,$$

with p = φ, q = 2 ln φ / φ, c = (4 ln φ − 1)/φ, b = φ⁶ − 2, s = 16φ + 1.

**Theorem (UV-finiteness).** Σ(u) > 0 for all u ≥ 0 (each term is
positive). R(u) is therefore regular on the entire half-line
[0, ∞). As u → ∞ (r → 0), Σ(u) → u^p, so

$$R(u) \to \frac{s}{u^p} \to 0.$$

The kernel has **no UV pole** and **vanishes** at the would-be
classical singularity. R(u_IR_cap) = s/c ≈ 47.04 sets the IR
ceiling, R → 0 sets the UV floor. ESD's classical singularity is
dressed away by the kernel itself — no separate "Planck-scale
mechanism" is invoked.

Numerical check: at u = 10²⁰, R(u) = 1.17 × 10⁻³¹ matches the
asymptote s/u^p to machine precision.

## Derivation C — Horizon as relational boundary

For a Schwarzschild horizon at r_s = 2GM/c², the Newtonian
acceleration at the horizon is g_h = c⁴/(4GM). The framework input is
u = 4g/a₀.

| BH | M [M_⊙] | r_s [m] | u(r_s) | R(u_h) |
|---|---:|---:|---:|---:|
| 10 M_⊙ stellar | 10 | 2.95×10⁴ | 5.07×10²² | 4.93×10⁻³⁶ |
| 30 M_⊙ stellar | 30 | 8.86×10⁴ | 1.69×10²² | 2.92×10⁻³⁵ |
| 10³ M_⊙ IMBH | 10³ | 2.95×10⁶ | 5.07×10²⁰ | 8.49×10⁻³³ |
| 10⁵ M_⊙ IMBH | 10⁵ | 2.95×10⁸ | 5.07×10¹⁸ | 1.46×10⁻²⁹ |
| Sgr A* | 4.15×10⁶ | 1.23×10¹⁰ | 1.22×10¹⁷ | 6.08×10⁻²⁷ |
| M87* | 6.5×10⁹ | 1.92×10¹³ | 7.79×10¹³ | 8.96×10⁻²² |
| TON 618 | 6.6×10¹⁰ | 1.95×10¹⁴ | 7.67×10¹² | 3.81×10⁻²⁰ |

The MOND-scale shell r(u=1) (where R(u) becomes O(1)) sits
**far outside** every horizon:

| BH | r_s [m] | r(u=1) [m] | r(u=1)/r_s |
|---|---:|---:|---:|
| 10 M_⊙ | 2.95×10⁴ | 6.65×10¹⁵ | 2.25×10¹¹ |
| Sgr A* | 1.23×10¹⁰ | 4.29×10¹⁸ | 3.49×10⁸ |
| M87* | 1.92×10¹³ | 1.70×10²⁰ | 8.83×10⁶ |
| TON 618 | 1.95×10¹⁴ | 5.40×10²⁰ | 2.77×10⁶ |

For TON 618 (the most massive known BH) the MOND-scale shell is
still nearly 3 × 10⁶ horizon radii outside. The R(u) ~ O(1)
regime can never reach an astrophysical horizon. **Horizons are the
deep-relational-floor boundary of the R(u) channel.**

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---|---|
| A1. R(u) does NOT apply to horizon entropy | must_be_false | False | PASS |
| A2. h-blindness of S_BH | ≤ 1e-15 | 0 | PASS |
| B1. R(u) → s/u^p as u → ∞ (no UV pole) | ≤ 1e-6 | 0 | PASS |
| B2. Σ(u) > 0 for all u ≥ 0 (regular) | True | True | PASS |
| B3. no zeros on test grid | True | True | PASS |
| C1. u ≫ 1 at every astrophysical horizon | ≥ 1e8 | 7.67e12 | PASS |
| C2. R(u) ≪ 1 at every astrophysical horizon | ≤ 1e-10 | 3.81e-20 | PASS |
| C3. r(u=1)/r_s ≫ 1 (MOND shell outside horizon) | ≥ 1e3 | 2.77e6 | PASS |

## Framework-native predictions and falsifiers

- **Hawking spectrum**: unchanged from GR. Any ESD-specific
  modification of the Hawking radiation spectrum at fixed M would
  falsify Derivation A.
- **Photon-ring / shadow**: unchanged from GR (already confirmed
  in Study 17 for M87* and Sgr A* to 0.77σ and 0.13σ).
- **Singularity behaviour**: ESD predicts no UV singularity in the
  kernel response. A detection of any Planck-scale R(u) feature
  (e.g. resonance, pole) would falsify Derivation B.
- **No anomalous MOND-shell physics at horizons**: the deep-strong-field
  cone is R(u) ≈ 0 to many orders. Any MOND-like deviation observed
  at r ~ r_s would falsify Derivation C.

## Run

```
make audit
make figures
make all
```
