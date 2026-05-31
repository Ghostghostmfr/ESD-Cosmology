# Study D — Tidal streams as gravity probes (sim 02)

ESD vs GR discrimination using the morphology of cold stellar streams
in the Milky Way halo (GD-1, Sagittarius, Pal 5).

## Sub-tasks

| # | Sub-task | Self-test |
|---|----------|-----------|
| D.1 | MW potential (Hernquist bulge + MN disk + NFW halo) | v_circ(8.122 kpc) in [225, 235] km/s |
| D.2 | ESD-modified potential (D-field correction in outer halo) | Recovers GR at small r |
| D.3 | Symplectic leapfrog integrator with adaptive step | E + L_z conservation < 1e-6 over 5 Gyr |
| D.4 | Particle-spray stream model (Fardal+ 2015) | Reproduce a published GD-1 mock track to ~0.1° |
| D.5 | GD-1 fit (GR vs ESD) | chi^2 comparison vs Gaia DR3 |
| D.6 | Sagittarius fit (outer-halo regime) | chi^2 comparison |
| D.7 | Pal 5 fit (optional) | chi^2 comparison |

## Folder layout

```
02_tidal_streams/
    scripts/        modules + self-tests + orchestrators
    data/           public stream catalogs (gitignored)
    figures_generated/   intermediate figures (gitignored)
    paper/figures/  promoted figures (committed)
```

## Constants

- R0_KPC = 8.122 (GRAVITY 2019)
- V_CIRC_R0 = 229.0 km/s (Eilers+ 2019)
- G_GAL = 4.302e-6 kpc (km/s)^2 / M_sun
