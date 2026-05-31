# Study 20 — Redshift derivation (null-geodesic applicability theorem)

**Status:** 4/4 derivation claims PASS. Companion to Study 19.

## What this study does

Theory work. Same axiomatic framework as Study 19, applied to
**photons** instead of linear density perturbations. The result rules
out — structurally, from Paper 1's spectator-relational axioms — any
anomalous-redshift mechanism in ESD.

## The applicability theorem (for photons)

R(u) is the closure-pool dressing of the gravitational interaction
between a localized massive subsystem and a separated spectator
background. Three axioms govern its applicability:

- **(A1) Bound-system locality** — requires a localized massive subsystem.
- **(A2) Acceleration definedness** — requires a well-defined gravitational acceleration g, since u = 4g/a₀.
- **(A3) Closure universality** — when (A1) and (A2) hold, R(u) is unique.

A **photon** is massless and follows a null geodesic of the background
metric with zero proper acceleration. It is not a localized massive
subsystem, and there is no g to feed into u. **Both axioms (A1) and
(A2) fail identically.**

Therefore R(u) does NOT modify photon propagation.

## Consequences

1. **Cosmological redshift unmodified:** 1+z = a(t_obs) / a(t_emit)
2. **All distance measures inherit ΛCDM forms** with ESD's locked Ω_m:
   $$H(z) = H_0\sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}, \quad D_L = (1+z)\,c\int_0^z dz'/H(z')$$
3. **µ(z) curve identical** to ΛCDM-Planck to <0.0001 mag (the only
   difference is the 0.02% Ω_m gap from Study 18).
4. **Sandage redshift-drift** dz/dt_obs unmodified.
5. **CMB z_* = 1089.92** unmodified (recombination physics is photon-
   based; no R(u) handle).
6. **No tired-light, no Arp-style discordant-redshift** mechanism.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---|---|
| 1. R(u) does NOT apply to null geodesics | A1,A2 fail | False | PASS |
| 2. µ(z) identity: ESD = ΛCDM-Planck | ≤ 5 mmag | 0.1 mmag | PASS |
| 3. CMB z_* inherited exactly | structural | 1089.92 | PASS |
| 4. h-blindness of dimensionless z | ≤ 1e-10 | 1.5e-16 | PASS |

## Sandage drift prediction (ELT / SKA observable)

| z | dz/dt_obs (10⁻¹⁰ /yr) |
|---:|---:|
| 0.5 | +0.122 |
| 1.0 | +0.144 |
| 2.0 | −0.024 |
| 4.0 | −0.921 |

## Framework-native statement

ESD predicts **no anomalous redshift component**, **no tired light**,
**no Arp-style discordant-redshift mechanism**, and **no modification
of the cosmological distance-redshift relation** at any z. Every
redshift observable inherits its ΛCDM form with ESD's locked Ω_m.

This is a **strong falsifier**: any detection of an anomalous redshift
component would falsify ESD.

## Run

```
make audit
make figures
make all
```
