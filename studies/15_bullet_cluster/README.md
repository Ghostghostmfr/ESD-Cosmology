# Study 15 — Bullet Cluster + dissociative cluster mergers

**Status:** 4/4 reproduction claims PASS. Bullet East match is **0.4% relative**.

## What this study reproduces

Four iconic merging-cluster systems where weak-lensing total-mass
reconstructions are spatially offset from the X-ray gas (the dominant
baryon component) by 100–500 kpc:

- **1E 0657-56 Bullet Cluster** (Clowe+2006, ApJ 648, L109) — the
  canonical "kill MOND" measurement.
- **MACS J0025.4-1222** (Bradac+2008, ApJ 687, 959).
- **Abell 520 "Train Wreck"** (Jee+2014, ApJ 783, 78).

These offsets falsified pure MOND, which requires lensing convergence
to follow the baryon surface density.

## How ESD passes

ESD has a real dark sector — the closure-pool D-field with locked
Ω_DM = 0.265642 vs Ω_b = 0.050094. The Hubble-paper Theorem 1, row
C4, gives an aperture-mass identity

  M_tot / M_b = (1 + R(u_cl)) + Ω_DM / Ω_b

where R(u_cl) is the closure-pool screening kernel (same one used in
Studies 03, 05, 10, 14) evaluated at cluster densities (u_cl ≫ 1,
so R(u_cl) ≪ 1).

At cluster densities the **5.303 additive term dominates** (>80% of
the total ratio for all four systems). The D-field is collisionless
on dynamical timescales by construction — Theorem 1 row C4 is a
static closure with no momentum transfer between dark and baryon
fluids — so it naturally permits the gas-vs-lensing offset.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---:|---|
| 1. Bullet East M_tot/M_gas | rel ≤ 30% | **0.4%** | PASS |
| 2. Joint 4-merger fit | mean \|resid\|/σ ≤ 2.0 | 0.40σ | PASS |
| 3. h-blindness of M_tot/M_b (Thm 1, C4) | \|dr/dh\| = 0 | 0 | PASS |
| 4. Dark-sector dominance | ≥ 80% | 80.3% | PASS |

## Per-merger table

| System | ratio_obs | ± | ratio_ESD | residual σ | DM % | offset kpc |
|---|---:|---:|---:|---:|---:|---:|
| 1E 0657-56 (Bullet) East | 6.364 | 1.144 | 6.390 | +0.02 | 83.0% | 200 |
| 1E 0657-56 (Bullet) Main | 5.455 | 1.175 | 6.338 | +0.75 | 83.7% | 210 |
| MACS J0025.4-1222 | 6.000 | 1.399 | 6.603 | +0.43 | 80.3% | 150 |
| Abell 520 (Train Wreck) | 7.111 | 1.550 | 6.470 | -0.41 | 82.0% | 480 |

All four within 1σ. **The Bullet test is not a problem for ESD**;
it is structurally resolved by the locked closure-pool dark sector
acting as a collisionless gravitational source.

## What ESD adds beyond ΛCDM

- The 6.4 ratio is **predicted from the locked Ω_DM/Ω_b = 5.30**, not
  fitted — ΛCDM matches the same number by construction but has Ω_DM
  as a free parameter; ESD has it locked by the closure pool.
- The aperture-mass identity is **h-blind in ω-vars** (Theorem 1 C4),
  so the prediction is invariant under Planck-vs-SH0ES H_0 shifts.

## Run

```
make audit       # writes outputs/{claims.csv,summary.json,...}
make figures     # writes figures_generated/{fig_ratio_per_merger,...}
make all         # both
```
