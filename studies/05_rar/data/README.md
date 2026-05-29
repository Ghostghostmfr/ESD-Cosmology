# SPARC data (shipped self-contained)

Identical contents to `studies/02_btfr/data/`. Shipped inside this
study folder so the study runs end-to-end without any network access.

| File                                  | Source |
|---------------------------------------|--------|
| `SPARC_Lelli2016c.mrt`                | Lelli, McGaugh & Schombert 2016, AJ 152 157.  Mirror: http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt |
| `Rotmod_LTG/<Galaxy>_rotmod.dat` (175 files) | SPARC mass-model decomposition (one file per galaxy).  Mirror: http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip |

Total size on disk: ~0.21 MB.

## Refetch

```bash
python scripts/fetch_sparc_rotmod.py --force
```

attempts (in order) a local development mirror at
`../../../../../repro/data/` (skipped silently in standalone
deployments), the CWRU SPARC distribution, and a VizieR fallback
for the master table.

## Citation

> Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016).
> *SPARC: Mass models for 175 disk galaxies with Spitzer photometry
> and accurate rotation curves.*
> The Astronomical Journal, 152, 157.
> [DOI: 10.3847/0004-6256/152/6/157](https://doi.org/10.3847/0004-6256/152/6/157)
