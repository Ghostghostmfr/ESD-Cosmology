# Study 21 — Gravitational-wave applicability theorem

**Status:** 4/4 derivation claims PASS. Second companion to Study 19 (after Study 20 on photons).

## What this study does

Theory work. Applies Paper 1's spectator-relational axioms (A1)–(A3)
to **gravitational waves** to determine whether R(u) modifies GW
propagation.

## The applicability theorem (for GWs)

A gravitational wave is a tensor perturbation h_{μν} of the
background metric, propagating at c in vacuum via the linearized
Einstein equations.

- **(A1) fails**: GW is a vacuum perturbation of the background,
  not a localized massive subsystem.
- **(A2) fails**: GW has no proper acceleration of an associated mass.
  u = 4g/a₀ has no defined value because there is no subsystem g.

R(u) does NOT modify GW propagation.

## Consequences

1. **c_GW = c exactly** — falsifiable. GW170817 already constrains
   |c_GW − c|/c < 3 × 10⁻¹⁵.
2. **Two tensor polarizations only** (h_+, h_×) — no scalar/vector
   modes from R(u).
3. **GW amplitude h ~ 1/D_L** inherits ΛCDM distance from Study 20.
4. **Standard-siren H_0** inherits ΛCDM analysis; ESD-locked
   H_0 = 67.36 km/s/Mpc is consistent with LIGO GW170817 SS
   (70 +12/−8) at 0.22σ.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---|---|
| 1. R(u) does NOT apply to GW propagation | A1,A2 fail | False | PASS |
| 2. c_GW = c (GW170817) | ≤ 3e-15 | 0 | PASS |
| 3. LIGO SS H_0 consistent with ESD H_0 | ≤ 2σ | 0.22σ | PASS |
| 4. h-blindness of GW observables | ≤ 1e-15 | 0 | PASS |

## GW170817 multimessenger summary

| Quantity | Value |
|---|---|
| Observed GW-GRB delay | 1.74 ± 0.05 s |
| ESD propagation contribution | 0 s (predicted) |
| Source-side delay attribution | 1.74 s (GRB jet) |
| Speed bound | \|c_GW − c\|/c < 3 × 10⁻¹⁵ |
| GW170817 D_L | 40 +8/−14 Mpc |
| LIGO standard-siren H_0 | 70 +12/−8 km/s/Mpc |
| ESD-locked H_0 (Planck mode) | 67.36 km/s/Mpc |

## Framework-native statement

ESD predicts:
- **c_GW = c** at all frequencies and redshifts.
- **Two tensor polarizations only** (h_+, h_×).
- **Standard ΛCDM scaling** of h ~ 1/D_L.

**Strong falsifiers:**
- Any measured GW-EM speed difference would falsify ESD.
- Any detected scalar/vector GW polarization (LISA, Cosmic Explorer)
  would falsify ESD.

## Run

```
make audit
make figures
make all
```
