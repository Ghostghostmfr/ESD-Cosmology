# SPARC data (shipped self-contained)

These files are the public SPARC galaxy rotation-curve database,
included verbatim so that this study reproduces end-to-end without
any network access.

## Files

| File                                  | Source / origin |
|---------------------------------------|-----------------|
| `SPARC_Lelli2016c.mrt`                | Lelli, McGaugh & Schombert 2016, AJ 152 157.  Mirror: http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt |
| `Rotmod_LTG/<Galaxy>_rotmod.dat` (175 files) | SPARC mass-model decomposition (one file per galaxy).  Mirror: http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip |

Total size on disk: ~0.21 MB.

## Refetch

The data files here are sufficient — `make residuals` runs offline.
If you want to refresh them anyway,

```bash
python scripts/fetch_sparc_rotmod.py --force
```

will attempt (in order) the CWRU mirror, then a VizieR fallback for
the master table.  The repo's `scripts/fetch_sparc_rotmod.py` also
checks an optional local development mirror at
`../../../../../repro/data/`, which exists only in the larger UTF
workspace and is silently skipped in a standalone deployment.

## Citation

If you use the SPARC data in derived work, please cite:

> Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016).
> *SPARC: Mass models for 175 disk galaxies with Spitzer photometry
> and accurate rotation curves.*
> The Astronomical Journal, 152, 157.
> [DOI: 10.3847/0004-6256/152/6/157](https://doi.org/10.3847/0004-6256/152/6/157)
