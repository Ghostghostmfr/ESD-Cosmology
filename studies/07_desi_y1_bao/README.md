# Study 07 — DESI Y1 BAO χ² reproduction (PRIMARY vs CLOSURE-POOL discriminator)

Closed-form BAO reproduction: for every framework cosmology (and a
Planck-ΛCDM baseline) we compute $(D_M/r_d,\,D_H/r_d,\,D_V/r_d)$ at
every DESI Y1 tracer (BGS, LRG1, LRG2, LRG3+ELG1, ELG2, QSO, Ly-α QSO),
then a χ² with each tracer's within-tracer 2×2 covariance.

The strongest live test this enables: **does DESI Y1 prefer the
PRIMARY reading (Ω_b = 0.0493) or the CLOSURE-POOL reading
(Ω_b = 0.0500) of Identity B?**

See [paper/README.md](paper/README.md) for the data citation
(Adame et al. 2404.03002 Table 1) and the Aubourg+2015 sound-horizon
fitting formula used in lieu of CAMB.

## Quickstart

```bash
# from the repo root, with esd_core installed (pip install -e .)
cd studies/07_desi_y1_bao
pip install -r requirements.txt
make all      # chi^2 + figures
```

Outputs land in [scripts/outputs/](scripts/outputs/);
figures in [figures_generated/](figures_generated/).

## Acceptance gate

`run_desi_y1_bao.py` returns exit 0 iff

$$|\Delta\chi^2(\text{ESD-PRIMARY} - \text{Planck-}\Lambda\text{CDM})| \leq 5$$

at $H_0 = 67.36$. The differential is the right gate, because the
**absolute** χ²/dof depends on the r_d normalization (Aubourg+2015 vs
CAMB) and on whether full cross-tracer covariance is used — neither
of which the framework controls. The differential between two
cosmologies evaluated through the *same* pipeline is unambiguous.

## Reading discriminator

The two readings of Identity B differ only on $\Omega_b$ (and
therefore on $\omega_b = \Omega_b h^2$, which sets the sound horizon
through the baryon loading $\propto \omega_b^{-0.128}$). They are
identical on $\Omega_m$, so the *distances* are identical and only
$r_d$ moves:

| Reading        | $\Omega_b$ | $\omega_b\;(h{=}0.6736)$ | $r_d$ (Mpc) |
|----------------|-----------:|-------------------------:|------------:|
| PRIMARY        |    0.04930 |                  0.02237 |     146.83  |
| CLOSURE-POOL   |    0.05009 |                  0.02273 |     146.53  |

The 0.2 % shift in $r_d$ propagates to ~0.2 % shifts in every BAO
ratio, which is detectable at DESI Y1 precision and recorded by
`run_desi_y1_bao.py` as a $\Delta\chi^2$ in the summary block.

## Two figures

- [`fig_desi_y1_distance_ladder`](figures_generated/fig_desi_y1_distance_ladder.pdf) —
  $D_M/r_d$, $D_H/r_d$, $D_V/r_d$ vs $z$ with theory curves (ESD
  PRIMARY, ESD CLOSURE-POOL, Planck-ΛCDM) and DESI Y1 points with
  error bars.
- [`fig_desi_y1_residuals`](figures_generated/fig_desi_y1_residuals.pdf) —
  per-tracer $(theory - data)/\sigma$ for all three cosmologies.

## Notes

- $H_0$ is **not** locked by the framework (Identity A fixes only the
  $\Omega_\Lambda/\Omega_m$ split). We report results at both Planck
  ($H_0 = 67.36$) and SH0ES ($H_0 = 73.04$) anchors.
- The absolute $\chi^2 \approx 22.9$ ($\chi^2/\text{dof}\approx 1.9$)
  at the Planck-ΛCDM baseline is higher than DESI's reported $\sim
  12$ because we use the Aubourg+2015 fitting formula instead of CAMB
  for $r_d$ and we ignore cross-tracer covariance. Both effects
  cancel in the differential ESD-vs-Planck gate.
