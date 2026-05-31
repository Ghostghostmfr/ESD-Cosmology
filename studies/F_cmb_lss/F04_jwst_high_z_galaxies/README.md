# Study 13 — JWST high-z galaxy abundance / Boylan-Kolchin baryon budget

**Status:** 4/4 reproduction claims PASS.

## What this study reproduces

Boylan-Kolchin 2023 ("Stress testing ΛCDM with high-redshift galaxy
candidates", Nat Astron 7, 731) showed that the Labbé+2023 (Nature 616,
266) JWST CEERS detection of six massive (M_*>10^10.5 M☉) galaxy
candidates at z=7-9 implies a cosmic star-formation efficiency

ε* = ρ_*(>M_*, z) / [ (Ω_b/Ω_m) · ρ_m,0 · f_collapse(>M_halo, z) ]
   = ρ_*(>M_*, z) / [ ρ_b,0 · f_collapse(>M_halo, z) ]

that, under standard ΛCDM cosmology and a Sheth-Tormen halo mass
function, exceeds the local-universe universal upper limit
ε*_max ≈ 0.20 (Wechsler & Tinker 2018). The central Labbé value gives
**ε* ≈ 1**, i.e. more stars in massive z=7-9 galaxies than the entire
cosmic baryon budget permits — the headline "impossible early galaxies"
tension.

## What ESD adds

The Hubble-paper Theorem 1 (Higginson 2026) classifies the comoving
baryon mass density ρ_b,0 = Ω_b ρ_crit,0 as a **C1 row** — exactly
h-blind in physical-density (ω_b = Ω_b h²) variables. The ESD-locked
Ω_b = 0.050094 sits 1.6% above the Planck-fit Ω_b = 0.04930, giving
only a 1.6% relaxation of ε* — **not enough to close the JWST tension
on its own**.

A full ESD resolution would require enhanced linear growth at z=7-10
from the closure-pool D-field's screening kernel R(u), which is
deferred to a future study (the screening boost at the collapse
threshold can multiply f_collapse by O(few), lowering ε* into the
plausible regime). This study reproduces the **budget calculation
itself**, not the proposed resolution.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. ρ_b,0 = Ω_b · ρ_crit,0 analytic identity | rel ≤ 1e-10 | 0 | PASS |
| 2. BK 2023 ε* tension reproduced (>0.20) | ε* > 0.20 | **1.033** | PASS |
| 3. h-blindness of ρ_b,0 (Thm 1, C1) | \|dρ/dh\| ≤ 1e-12 | 0 | PASS |
| 4. Locked vs Planck Ω_b: \|Δε*\| small | rel ≤ 2% | 1.59% | PASS |

## Per-sample ε* table

| Survey | z range | ρ_* [M☉/Mpc³] | ε* |
|---|---|---:|---:|
| Labbé+2023 CEERS | 7.0–9.0 | 6.5e6 | **1.033** |
| Casey+2024 COSMOS-Web | 7.5–10.0 | 2.5e6 | 0.397 |
| Xiao+2024 FRESCO | 5.0–9.0 | 1.0e7 | 1.590 |

The Casey+2024 wider-area follow-up reduces but does not eliminate the
tension; the Xiao+2024 ultra-massive sample makes it worse.

## Run

```
make audit       # writes outputs/{claims.csv,summary.json,...}
make figures     # writes figures_generated/{fig_eps_vs_rho,...}.{png,pdf}
make all         # both
```

## Files

- `scripts/esd_jwst.py` — ρ_b,0, ρ_m,0, ε*_min, h-blindness checks
- `scripts/observations.py` — Labbé+2023, Casey+2024, Xiao+2024
- `scripts/run_jwst_audit.py` — 4 gated claims
- `scripts/make_jwst_figures.py` — 3 figures

## Honest limits

- **Not a resolution of the tension.** This is a reproduction of the
  ΛCDM-style budget calculation using ESD-locked Ω_b, Ω_m.
- f_collapse(z) is taken as a tabulated Sheth-Tormen value from
  BK 2023 supplementary, not re-derived from an ESD HMF.
- ~~A future study should compute the closure-pool D-field linear
  growth factor D_+(z; R-kernel) and the resulting boost in
  f_collapse at z=7-10.~~ **Path closed — see addendum.**

## Addendum (2026-05-30): R(u) applicability check

The original README floated a deferred-resolution path: enhance
linear growth at z=7-10 via R(u). That path is **closed** by
Study 19's applicability theorem (axiom A1 fails for linear
perturbations of the same field as the background; no system /
spectator split exists at linear order).

`scripts/esd_jwst_growth.py` carries out the explicit check and
also computes the only ESD-admissible alternative — the in-halo
R(u) dressing of the star-formation-efficiency ceiling ε*_max:

| Quantity | Value |
|---|---:|
| observed ε* (Labbé+2023) | 1.033 |
| standard ε*_max ceiling | 0.20 |
| tension factor | 5.17× |
| z=8, M_halo=10^10.7 M☉ halo r_vir | 12.7 kpc |
| g at r_vir | 4.3×10⁻¹¹ m/s² |
| u = 4g/a₀ | 1.44 |
| R(u) at halo edge | 1.21 |
| in-halo-dressed ε*_max | 0.443 |
| R required to close gap | ≥ 4.17 |

**Verdict: ESD does NOT close the JWST baryon-budget tension via
R(u).** High-z halos are compact, so g ~ a₀ rather than g ≪ a₀; R(u)
is in its modest-amplification regime, not the deep-MOND limit.
Resolution must come from another channel (gas cooling physics,
SFE efficiency, observational systematics in stellar-mass
estimates) — outside ESD's structural prediction set.
