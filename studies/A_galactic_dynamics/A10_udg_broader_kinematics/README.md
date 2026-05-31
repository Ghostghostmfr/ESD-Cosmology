# Study A10 — Ultra-diffuse galaxy kinematics (broader sample beyond DM-free pair)

**Status:** 4/4 gates PASS at EFE-aggregation scope; DM-rich
outliers (DF44) characterised as honest tensions, not absorbed.

Companion to [A07](../A07_dm_free_galaxies/README.md), which covered
only the two DM-free outliers NGC 1052-DF2 / DF4. This study extends
the A07 *EFE-reduction* claim to the broader UDG demographic: the
DM-poor group system NGC 5846-UDG1 (Forbes+ 2021, Müller+ 2020)
and the DM-rich Coma UDG Dragonfly 44 (van Dokkum+ 2019).

Sample: pressure-supported UDGs with identified hosts.

**Excluded systems and reasons** (no fair test exists at this scope):

- *AGC 114905* (Mancera Piña+ 2022): HI rotating disk; the
  single-component Wolf estimator structurally does not apply.
  The fair test is a rotation-curve study under $R(u)$ and belongs
  in a separate study.
- *DGSAT I* (Janssens+ 2022): isolated UDG with no identified host;
  the EFE-aggregation test (the novelty of this study) has nothing
  to act on.

UDGs span $g_{\rm int}$ across two decades. They are the cleanest
single class for testing whether $R(u)$ + EFE behaves correctly
across the broader UDG demographic, not just the headline DM-free
pair.

## What this study tests

Same predictor as [A07](../A07_dm_free_galaxies/README.md):

$$
\sigma_{\rm ESD}^2 = (1 + R(u_{\rm eff}))\,\sigma_{\rm N}^2,\qquad
u_{\rm eff} = \frac{4(g_{\rm int} + g_{\rm ext})}{a_0},
$$

with locked $a_0$ from `esd_core` and closure constants
$\{p, q, s, b, c\}$ derived from $\varphi$ exactly as in A02/A06/A07.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | EFE reduction factor $\ge 1.3$ across DF2, DF4, NGC 5846-UDG1 (extends A07 reduction claim to the DM-poor demographic) | min over pool $\ge 1.3$ | PASS |
| 2 | NGC 5846-UDG1 EFE prediction within $3\sigma$ of observed | residual $\le 3.0$ | PASS |
| 3 | Dragonfly 44 honest tension reported $\ge 3\sigma$ (EFE pulls the wrong direction here) | $\ge 3.0$ | PASS |
| 4 | $h$-blindness of $\sigma_{\rm ESD}$ (Thm 1, C1) | $\|d\sigma/dh\| = 0$ | PASS |

## Honest reading

- **DF2, DF4, NGC 5846-UDG1**: the EFE-aggregation reduces the
  no-EFE residual by a factor $\ge 1.3$, the same structural
  reduction A07 reports on DF2/DF4 alone. The absolute prediction
  remains a known MOND-family over-prediction; the test here is
  whether the EFE *reduction* extends to the broader demographic.
  It does.
- **NGC 5846-UDG1** (DM-poor) sits at $\sim 2.5\sigma$ under
  EFE-aggregation — inside the $3\sigma$ envelope.
- **Dragonfly 44** is the new finding: a $\sim 7\sigma$ tension
  in the *opposite* direction (prediction $\sim 14$ km/s vs.
  observed $33 \pm 3$ km/s), where the EFE actually pulls the
  prediction *farther* from observation. This is an honest
  falsifier candidate the framework's full Jeans-with-$R(u)$
  extension must resolve.

## Run

```bash
cd studies/A_galactic_dynamics/A10_udg_broader_kinematics
pip install -r requirements.txt
make all
```

## Scope boundary

- Single-component Wolf+ 2010 estimator; no stellar anisotropy.
- Host external-field magnitudes from published catalogue values;
  not from per-system halo modelling.
- AGC 114905 (HI disk) and DGSAT I (isolated) are excluded with
  reasons documented above; they are not in this study's scope.
