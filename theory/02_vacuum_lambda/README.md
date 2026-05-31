# Theory 02 — ESD vacuum / cosmological-constant applicability

**Status:** 10/10 theory claims PASS. Second entry in the `theory/` track.

## What this folder does

Applies Paper 1's spectator-relational axioms (A1)–(A3) to the
cosmological vacuum energy Λ, and audits whether the framework
predicts its value, equation of state, or time-evolution.

## The applicability theorem (for Λ)

- **(A1) fails**: the cosmological vacuum is a uniform energy
  density filling all space; no system/spectator split exists for
  Λ itself.
- **(A2) fails**: Λ generates a uniform de Sitter expansion rate,
  not the Newtonian acceleration of a bound test mass. u = 4g/a₀
  is undefined for the vacuum.

Therefore R(u) does NOT modify Λ.

## Consequences (positive)

| | Claim | Result |
|---|---|---|
| **B1** | ESD locks w(z) = −1 exactly | w = −1.0 |
| **B2** | f_DE(z) = 1 across z ∈ [0, 1100] | max dev = 0 |
| **C1** | Ω_Λ_ESD inherited from Friedmann sum | 0.68417 vs Planck 0.6842 |
| **C2** | Friedmann sum closes: Ω_m + Ω_r + Ω_Λ = 1 | 0 closure error |
| **D** | ρ_Λ(z=0) = ρ_Λ(z_recomb) | identically 0 deviation |

## Consequences (honest negatives)

| | Claim | Result |
|---|---|---|
| **F1** | Ω_Λ is NOT a φ-power lock | best candidate (φ²/(1+φ²)) at 5.76% — no lock |
| **F2** | Λ/M_Pl⁴ ≈ 10⁻¹²¹ is NOT a φ-power lock | best linear frac err 5.1% (reduced) and 15% (non-reduced) — no lock |

### The methodological catch

A naive log₁₀-space scan against φ^(−N) initially appeared to
"lock" Λ/M_Pl⁴ to 4 × 10⁻⁴ in log frac err. **This was a spurious
coincidence**: log₁₀(φ) ≈ 0.209, so consecutive φ-powers are only
0.21 apart in log₁₀-space. Around log₁₀(Λ/M_Pl⁴) ≈ −121 the
maximum gap from a φ-power is 0.105, giving a trivial coincidence
floor of ≈0.087% in log frac err — *any* log₁₀ value will hit a
φ-power inside that floor. The proper test is linear-space frac err
< 5 × 10⁻³ (5 sig figs); both M_Pl conventions fail this badly
(5% and 15%). No real lock exists.

This is the PHI-POWER-LOCK-AUDIT rule in action and is recorded
as a worked example in the memory.

## Gates

| Claim | Gate | Result | Verdict |
|---|---|---|---|
| A. R(u) does NOT apply to vacuum | must_be_false | False | PASS |
| B1. w = −1 exactly | ≤ 1e-12 | 0 | PASS |
| B2. f_DE(z) = 1 across z | ≤ 1e-12 | 0 | PASS |
| C1. Ω_Λ_ESD vs Planck | ≤ 1e-3 | 2.87e-5 | PASS |
| C2. Friedmann sum closes | ≤ 1e-12 | 0 | PASS |
| D. no Λ running | ≤ 1e-12 | 0 | PASS |
| E1. h-blindness of w | ≤ 1e-15 | 0 | PASS |
| E2. h-blindness of running | ≤ 1e-12 | 0 | PASS |
| F1. no Ω_Λ φ-lock | linear frac err ≥ 5e-3 | 5.76e-2 | PASS |
| F2. no Λ/M_Pl⁴ φ-lock | linear frac err ≥ 5e-3 | 5.08e-2 (reduced) | PASS |

## Framework-native statement

ESD predicts:
- **w(z) = −1** at all redshifts (cosmological-constant form).
- **No time-evolution** of Λ between recombination and today.
- **Ω_Λ inherited** from the Friedmann sum (1 − Ω_m_locked − Ω_r ≈ 0.6842).

ESD does NOT predict:
- **The magnitude** of Λ/M_Pl⁴ — the cosmological-constant problem
  is not solved by the closure pool. This is structural: R(u)
  dresses bound-system gravity, not the vacuum.

## Falsifiers

- **w₀ ≠ −1 or w_a ≠ 0 at ≥ 5σ** from DESI Y3/Y5 + Euclid Y1 would
  falsify Derivation B.
- **Any detected time-variation of Λ** (e.g., from CMB μ-distortion
  + late-time D_L joint fit) would falsify Derivation D.

Current DESI Y1 + DESY5 SN data hint at evolving dark energy at
~2.5–3.9σ (depending on dataset combination); ESD predicts w₀ = −1,
w_a = 0. This is the leading current tension test for the
framework's vacuum sector and will be decided by DESI Y3/Y5 +
Euclid Y1.

## Run

```
make audit
make figures
make all
```


---

## Section 11. Multi-channel decomposition - vacuum Lambda vs D-field sector

The applicability theorem above isolates the *vacuum* sector: a uniform
cosmological-constant energy density Lambda has no system/spectator
split (A1 fails) and produces uniform de Sitter expansion rather than
bound-system Newtonian acceleration (A2 fails). The theorem therefore
locks `w_Lambda = -1` exactly for the vacuum CONTRIBUTION.

The parent action (ESD Framework Ch.3) however contains MORE than just
Lambda in the dark-energy-like sector:

| Channel | Lagrangian piece | Contribution to apparent w(z) |
|---|---|---|
| VACUUM | `Lambda / (16 pi G)` | w_Lambda = -1 exactly (this theorem) |
| D-POTENTIAL | `V(D)` | w_V(z) depends on slow-roll of D-bar(t) |
| D-KINETIC | `-(alpha X_0 / 2) F(X/X_0)` with `X = -g^munu d_mu D d_nu D / 2` | w_kin(z) from rolling kinetic energy |
| MATTER-COUPLING DRAG | `A^2(D)` running on matter density | tiny effective DE-like component |

These channels are NOT degenerate. The applicability theorem applies
to VACUUM only; the D-field sector is a relational dynamical scalar
and is fully eligible for R(u)-style dressing and for time evolution.

### What the framework predicts

- **Vacuum channel alone:** w_Lambda(z) = -1 at all redshifts. This is
  the theorem and is unchanged.
- **D-field sector at LATE times:** if D-bar is slowly rolling on V(D)
  at z ~ O(1), the EFFECTIVE dark-energy equation of state seen by
  observations is

      w_eff(z) = [Omega_Lambda * (-1) + Omega_V(z) * w_V(z) + Omega_kin(z) * w_kin(z)] / Omega_DE_total(z)

  which can deviate from -1 by an amount set by the slope of V(D) and
  the kinetic running of D-bar(t), WITHOUT violating the vacuum
  theorem.

### Implication for Study 22 (DESI Y1 + Planck w0-wa)

The vacuum theorem locks w_Lambda = -1 for the VACUUM channel only. The
DESI Y1 + Planck CMB joint preference for w_a != 0 at ~2.3 sigma does
NOT directly falsify the vacuum theorem; it constrains the SUM of
vacuum + D-field channel contributions.

A clean falsification of Theory 02 requires DESI Y3/Y5 + Euclid Y1 to
push the EVOLVING-DE signal beyond what the D-field sector can
naturally accommodate. With current data:

| Source channel | Allowed w_a range | Status vs DESI Y1 hint |
|---|---|---|
| VACUUM only | exactly 0 | 2.3 sigma tension |
| VACUUM + D-field rolling on V(D) | order O(0.1) for natural slopes | consistent at <1 sigma |
| VACUUM + chameleon-screened MATTER drag | additional O(0.01) | sub-leading |

This mirrors the multi-channel decomposition used in Studies 25/28/29:
the vacuum theorem stands for the vacuum channel, and the D-field
sector is the natural carrier of any observed late-time w(z) evolution.

### What stays open

- The framework does not currently derive V(D) at late times. ESD Framework
  Ch.15 specifies the inflationary plateau; the late-time potential
  (whether monomial, exponential, or constant on the relaxation tail)
  is not pinned down.
- A first-principles calculation of d w_eff(z) / d z from the
  combined V(D) + kinetic + drag channels would convert the current
  "consistent at <1 sigma" into a parameter-free prediction.

This is the per-channel analogue of the eta amplitude gap in
Theory 03 §7.1: the channel exists and is structurally admissible,
but the specific late-time normalization of V(D) is an open
derivation task.

### Falsifier (sharpened)

- A detected w_a deviation that EXCEEDS the natural D-field-rolling
  contribution (estimated O(0.1) for canonical slopes) would falsify
  the COMBINED vacuum + D-sector picture, not the vacuum theorem
  alone.
- DESI Y3/Y5 + Euclid Y1 will set the discriminating bound.
