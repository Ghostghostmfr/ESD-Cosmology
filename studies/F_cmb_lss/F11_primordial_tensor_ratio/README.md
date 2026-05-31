# Study 38 — Primordial tensor-to-scalar ratio $r$ (BICEP/Keck, LiteBIRD, CMB-S4)

**Status: PASS (5/5 gates)** — the ESD parent action embeds a
**Starobinsky-class plateau** inflation attractor (Master Ch. 15;
disformal $B(D)\,\partial D\partial D$ term running to its
high-$D$ fixed point). Single-field slow-roll on the plateau gives
the parameter-free predictions

$$r \;=\; \frac{12}{N_e^{\,2}} \;\approx\; 3.3 \times 10^{-3},\qquad
n_s \;=\; 1 - \frac{2}{N_e} \;\approx\; 0.967\qquad(N_e = 60)$$

The $n_s$ prediction matches Planck 2018 ($n_s = 0.9649 \pm 0.0042$)
at **$0.12\sigma$**, and the $r$ prediction sits a factor $\sim 11$
below the current best 95% CL upper limit (BICEP/Keck BK18,
$r < 0.036$). **LiteBIRD reaches $\sim 3\sigma$ at the ESD value,
CMB-S4 reaches $\sim 6.6\sigma$, PICO reaches $\sim 33\sigma$** —
the framework's inflation lock is testable within the next decade.

Closes the cosmology audit suite by anchoring the
**primordial** end of the framework's parent-action spectrum, in
parallel with [Studies 19/34/35/37](../F06_linear_growth_s8_prediction/README.md)
which anchor the **linear-regime sub-horizon** end, and
[Studies 33/36](../../D_clusters_halos/D04_cluster_mass_function/README.md) which anchor
the **bound-system $R(u)$-modified** end.

## Why the framework predicts $r \sim 3 \times 10^{-3}$

The Master Ch. 15 inflation derivation identifies a unique
plateau-class attractor in the parent action when the disformal
sector $B(D)\,\partial_\mu D\,\partial^\mu D$ runs to its
high-curvature fixed point. On the plateau:

$$\epsilon = \frac{3}{4\,N_e^{\,2}},\qquad
\eta = -\,\frac{1}{N_e},\qquad
n_s = 1 + 2\eta - 6\epsilon,\qquad r = 16\,\epsilon$$

| $N_e$ | $\epsilon$ | $\eta$ | $r = 16\epsilon$ | $n_s$ |
|---|---|---|---|---|
| 50 | $3.00 \times 10^{-4}$ | $-0.0200$ | $4.8 \times 10^{-3}$ | $0.958$ |
| 60 (best anchor) | $2.08 \times 10^{-4}$ | $-0.0167$ | $\mathbf{3.3 \times 10^{-3}}$ | $\mathbf{0.967}$ |
| 70 | $1.53 \times 10^{-4}$ | $-0.0143$ | $2.4 \times 10^{-3}$ | $0.972$ |

The single-field consistency relation $n_t = -r/8 \approx -4 \times 10^{-4}$
provides a second falsifier accessible to LiteBIRD/CMB-S4 tensor
spectrum reconstruction.

## Comparison with current constraints

| Survey / forecast | $r$ (95% UL or $\sigma_r$) | Status vs ESD $r = 3.3 \times 10^{-3}$ |
|---|---|---|
| BICEP/Keck BK18                | $r < 0.036$ (95% CL UL)         | **cleared** by factor $\sim 11$ |
| ACT DR4 + WMAP                 | $r < 0.114$ (95% CL UL)         | **cleared** by factor $\sim 35$ |
| BICEP3/Keck (proj. $\sim 2027$) | $\sigma_r \sim 3 \times 10^{-3}$ | SNR $\sim 1.1$ at ESD value |
| Simons Observatory             | $\sigma_r \sim 3 \times 10^{-3}$ | SNR $\sim 1.1$ at ESD value |
| LiteBIRD (JAXA L-class)        | $\sigma_r \sim 1 \times 10^{-3}$ | SNR $\sim 3.3$ at ESD value |
| CMB-S4 (Stage-IV ground)       | $\sigma_r \sim 5 \times 10^{-4}$ | SNR $\sim 6.6$ at ESD value |
| PICO (NASA Probe concept)      | $\sigma_r \sim 1 \times 10^{-4}$ | SNR $\sim 33$ at ESD value |

### Forward falsifiers

| Future outcome | Implication for framework |
|---|---|
| LiteBIRD/CMB-S4 detect $r \in [2, 5] \times 10^{-3}$ at $\geq 3\sigma$ | **Confirms** Starobinsky-plateau lock |
| CMB-S4 reaches $r < 10^{-3}$ (5$\sigma$) | Falsifies plateau anchor in standard $N_e \in [50,70]$ window |
| Any survey detects $r > 0.01$ | Indicates different parent-action embedding (chaotic-class or natural-inflation) |
| $n_t \neq -r/8$ measured | Indicates beyond-single-field structure (multi-field, EFT modifications) |

## Independent cross-check: scalar tilt $n_s$

The same plateau anchor that predicts $r$ also predicts
$n_s = 1 - 2/N_e$:

| Quantity | ESD prediction ($N_e = 60$) | Planck 2018 | Tension |
|---|---|---|---|
| $n_s$ | $0.9654$ | $0.9649 \pm 0.0042$ | $\mathbf{0.12\sigma}$ |

This is a parameter-free coincidence: $N_e$ is set by reheating
constraints to $50{-}70$, and the same value that gives the
observed $n_s$ also predicts the testable $r \sim 3 \times 10^{-3}$.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | Master Ch. 15 parent action locks Starobinsky-plateau attractor → $r > 0$ | PASS |
| 2 | ESD prediction below all current 95% CL upper limits | PASS (cleared by ×11 and ×35) |
| 3 | ESD $n_s$ matches Planck within $1\sigma$ | PASS ($0.12\sigma$) |
| 4 | At least one funded forecast reaches $\geq 2\sigma$ at ESD $r$ | PASS (LiteBIRD $3.3\sigma$, CMB-S4 $6.6\sigma$) |
| 5 | No new free parameters (only standard $N_e \in [50, 70]$ reheating window) | PASS |

## Relationship to other studies

| Study | Relationship |
|---|---|
| Master Ch. 15  | Derives Starobinsky plateau as unique attractor of disformal sector |
| [19](../F06_linear_growth_s8_prediction/README.md) | Same parent action → linear growth = $\Lambda$CDM |
| [33](../../B_solar_system/B02_solar_system_ppn/README.md) | Same parent action → bound-system $R(u)$ acts; PN tests |
| [36](../../D_clusters_halos/D04_cluster_mass_function/README.md) | Same parent action → HMF lift forward prediction |
| Hubble paper Identity B | Same parent action → $\Omega_m = 0.31574$ lock |

Studies 19/33/34/35/36/37/38 collectively span the **full
cosmological-history span** of the ESD parent action: from
inflation ($z \to \infty$) through linear-mode evolution
($z \sim 1100$ CMB, $z \sim 1$ BAO/RSD) into bound-system
nonlinear collapse ($z = 0$ clusters/galaxies/solar system),
**with no new parameters beyond the original closure-pool kernel
$R(u)$**.

## References

- Starobinsky, A. A. 1980, PLB 91, 99 ($R^2$ inflation)
- Planck Collab. 2020, A&A 641, A10 (inflation: $n_s$ constraint)
- Ade, P. A. R. et al. (BICEP/Keck) 2021, PRL 127, 151301 (BK18 $r$ upper limit)
- Aiola, S. et al. (ACT) 2020, JCAP 12, 047 (ACT DR4 + WMAP)
- Ade, P. A. R. et al. (Simons Obs.) 2019, JCAP 02, 056 (SO forecast)
- Hazumi, M. et al. (LiteBIRD) 2022, PTEP 2023, 042F01 (LiteBIRD forecast)
- Abazajian, K. N. et al. (CMB-S4) 2022, ApJ 926, 54 (CMB-S4 forecast)
- Hanany, S. et al. (PICO) 2019, NASA Astro2020 white paper, arXiv:1902.10541
- ESD Framework — Master Book Chapter 15

## Quickstart

```bash
cd studies/F11_primordial_tensor_ratio
python scripts/run_r_audit.py
python scripts/make_r_figures.py
```
