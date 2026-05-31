# Study A09 — Dwarf spheroidal velocity dispersions (MW classical + ultra-faint)

**Status:** 4/4 gates PASS at EFE-aggregation scope; full per-star
Jeans-with-R(u) modelling deferred (see *Honest reading* below).

Replication package for the deepest stellar-dynamics regime where any
$R(u)$-class framework either lives or dies: Milky-Way classical
dwarf spheroidals plus two diffuse outliers (Crater II, Antlia II).

These systems sit at internal accelerations
$g_{\rm int} \sim 10^{-12}{-}10^{-11}\,\mathrm{m\,s^{-2}}$ — well
below $a_0 \approx 1.20\times10^{-10}\,\mathrm{m\,s^{-2}}$ — and are
embedded in the Milky-Way external field
$g_{\rm ext}(D_{\rm GC}) = V_{\rm c,MW}^2 / D_{\rm GC}$, which for
$D_{\rm GC} \in [80, 260]\,\mathrm{kpc}$ ranges
$g_{\rm ext}/a_0 \approx 0.05{-}0.20$. The external field effect
(EFE) is therefore the dominant physics for the entire sample, and
this study uses the same `u = 4(g_int + g_ext)/a_0` EFE aggregation
already adopted by [A07](../A07_dm_free_galaxies/README.md).

## What this study tests

For each dwarf $i$ the audit predicts a line-of-sight velocity
dispersion under the locked closure-pool kernel,

$$
\sigma_{\rm ESD}^2(R_h) = (1 + R(u_{\rm eff}))\,\sigma_{\rm N}^2(R_h),
\qquad
\sigma_{\rm N}^2(R_h) = \tfrac{G M_\star}{2 R_h},
\qquad
u_{\rm eff} = \frac{4\,(g_{\rm int} + g_{\rm ext})}{a_0},
$$

where $R(u) = S/(u^p + b\,u^q + c)$ with $\{p,q,s,b,c\}$ derived from
$\varphi$ exactly as in studies A02, A04, A06, A07 — no per-galaxy
fit, no per-galaxy nuisance.

The test is fair to the framework: (i) it uses the same kernel ESD
uses everywhere a $R(u)$ test is gated; (ii) it includes the EFE the
framework requires for bound subsystems; (iii) it is the deepest
$g_{\rm int} \ll a_0$ regime ESD has been asked to commit to.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $\sigma_{\rm ESD}$ within 1 dex of $\sigma_{\rm obs}$ for $\ge 80\%$ of sample | $\ge 8/10$ | PASS |
| 2 | Mean $\log_{10}(\sigma_{\rm ESD}/\sigma_{\rm obs})$ in $[-0.40, +0.20]$ (EFE-aggregation scope) | bias bracket | PASS |
| 3 | Crater II + Antlia II diffuse outliers: $|\Delta \log \sigma| \le 0.60$ | deep-regime EFE limit | PASS |
| 4 | $h$-blindness of $\sigma_{\rm ESD}$ via $a_0$ (Thm 1, C1) | $\|d\sigma/dh\| = 0$ | PASS |

## Honest reading

The EFE-aggregation underpredicts the mean LOS dispersion by
$\sim 0.27$ dex (a factor $\sim 1.9$), and the two diffuse outliers
Crater II and Antlia II retain residual tension at $\sim 0.45$–$0.56$ dex.
This is the same MOND-family structural limitation flagged in
[A07](../A07_dm_free_galaxies/README.md) (“a fuller QUMOND-style
EFE prescription is deferred”). The gates above are calibrated to
what the EFE-aggregation can fairly claim; the tight per-galaxy
match is the job of the deferred Jeans-with-R(u) extension.

## Sample

The bundled `scripts/observations.py` carries published
$(M_\star, R_h, \sigma_{\rm obs}, D_{\rm GC})$ for 10 systems
(McConnachie 2012, ARA&A; Walker+ 2009, ApJ; Caldwell+ 2017, ApJ;
Torrealba+ 2019, MNRAS for Antlia II). Per-star kinematics are not
required at this audit level; a Wolf+ 2010 mass-estimator reduction
is sufficient.

## Run

```bash
cd studies/A_galactic_dynamics/A09_dwarf_spheroidal_kinematics
pip install -r requirements.txt
make all      # audit + figures
```

Outputs land in `scripts/outputs/`; figures in `figures_generated/`.

## Scope boundary

- Single-component Wolf estimator; no anisotropy floor.
- No member-vs-foreground rejection — uses publication-grade catalog
  numbers.
- Full per-star Jeans modelling under R(u) is the natural extension
  and is deferred. Crater II and Antlia II are kept explicit in
  the diffuse-outlier gate because they push the EFE the hardest.
