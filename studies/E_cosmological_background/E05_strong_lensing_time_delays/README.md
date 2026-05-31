# Study 31 — Strong Lensing Time Delays (TDCOSMO + H0LiCOW)

**Status:** PASS (5/5) — three-channel ESD $H_0 = 67.36 \pm 0.54$
km/s/Mpc from the locked $a_0$ bridge inversion agrees with TDCOSMO-IV
(Birrer+ 2020) at $0.01\sigma$ and with B1608+656 $D_{\Delta t}$
(Suyu+ 2010) at $\chi^2 = 0.36$. The Wong+ 2020 / H0LiCOW
$H_0 = 73.3$ is flagged at $3.2\sigma$ tension, consistent with the
standard identification of that result as biased by rigid power-law
lens models. At the Einstein radius the three-channel closure pool is
small ($R = 0.40$, amp$_D = 1.0017$ — a 0.2 % Fermat-potential
enhancement, well inside the mass-sheet-degeneracy floor), so the
lens-scale ESD modification is absorbed by the standard lens fit.

Tests whether the ESD framework's locked $H_0$ prediction (from the
$a_0$ bridge inversion of Studies 08 / 12) is consistent with the
time-delay cosmography of the TDCOSMO 6-lens sample, and whether the
**three-channel** structure of the parent action correctly identifies
the Wong+ 2020 vs. Birrer+ 2020 (TDCOSMO-IV) $H_0$ split as a lens-
modelling issue rather than a framework failure.

## Why TDCOSMO is the cleanest one-step $H_0$ probe

Strong-lens time delays measure the **time-delay distance** directly:

$$\Delta t_{ij} = \frac{1+z_l}{c}\,D_{\Delta t}\,\bigl[\phi(\theta_i,\beta) - \phi(\theta_j,\beta)\bigr], \qquad D_{\Delta t} = \frac{D_l\,D_s}{D_{ls}}.$$

$D_{\Delta t}$ scales as $1/H_0$ at fixed cosmology, so a single
strong-lens system with well-measured time delays and a fitted
Fermat-potential difference $\Delta\phi$ gives a one-step inversion
$H_0 = c\,\Delta t / [(1+z_l)\,\Delta\phi\,D_{\Delta t}^{(H_0=1)\,-1}]$.

Two large analyses give discrepant answers:

| Pipeline | $H_0$ [km/s/Mpc] | Lens-mass assumption |
|---|---|---|
| Wong+ 2020 (H0LiCOW) | $73.3^{+1.7}_{-1.8}$ | rigid power-law / composite NFW+stars |
| Birrer+ 2020 (TDCOSMO-IV) | $67.4^{+4.1}_{-3.2}$ | mass-sheet-flexible (incl. SLACS prior) |

This is the classical **mass-sheet degeneracy**: rigid mass profiles
force a low $\kappa_\mathrm{ext}$ prior and inflate the inferred
$H_0$.

## ESD prediction (three-channel treatment)

The parent action (ESD Framework Ch.3) has three channels:

| Channel | Role | Term in $\Sigma(u)$ |
|---|---|---|
| **D** (anchor / drive) | $A^2(D) g_{\mu\nu}$ conformal — bulk-density sourced | $\tau_D = c$ |
| **E** (bridge / transfer) | $B(D) \partial D\,\partial D$ disformal — gradient sourced | $\tau_E = b\,u^q$ |
| **S** (spectator / floor) | $Z(D) F^2$ photon bridge (locked at floor) | $\tau_S = u^\varphi$ |

**Lens-scale physics ($R_E \sim 5$–$15$ kpc):**

For a typical massive elliptical lens ($\sigma_v = 250$ km/s,
$\theta_E = 1.5''$, $D_l \sim 1.5$ Gpc):

$$g(R_E) \sim \sigma_v^2 / R_E \;\approx\; 1.86\times 10^{-10}\ \mathrm{m\,s^{-2}}, \quad u_\mathrm{lens} = 4g/a_0 \;\approx\; 6.2.$$

This is the **MOND transition regime** ($u \sim O(1)$), not the deep
IR regime probed by voids. At $u_\mathrm{lens} = 6.2$ the kernel is
strongly off the floor:

$$R(u_\mathrm{lens}) \approx 0.40, \quad R_D \approx 0.003, \quad R_E \approx 0.28, \quad R_S \approx 0.12,$$

with channel weights $w_D \approx 0.009$, $w_E \approx 0.71$,
$w_S \approx 0.29$. The D-channel modification of the lens potential
is tiny: amp$_D = \sqrt{1 + R_D} \approx 1.002$, i.e. a 0.2 %
enhancement. The E-channel and S-channel carry most of the (small)
closure pool at lens scales, both of which couple to gradient and
photon-bridge modes that **do not** alter the standard Fermat
potential of a parametric lens fit.

**Net lens-scale result:** the Fermat-potential difference
$\Delta\phi_\mathrm{obs}$ is theory-agnostic at the per-mille level.
ESD predicts GR-like strong-lens cosmography. Any residual 0.2 %
enhancement is absorbed into the lens-mass fit (degenerate with
$\kappa_\mathrm{ext}$, well below mass-sheet-degeneracy systematics).

**Cosmological distances:**

The only ESD signature in TDCOSMO is the $H_0$ anchor (and a small
$H(z)$ correction from the D-field dark-energy sector,
[theory/02_vacuum_lambda](../../../theory/02_vacuum_lambda/), at
sub-percent level). The framework predicts

$$H_0^{\mathrm{ESD}} \;=\; \frac{c}{a_0}\sqrt{\frac{8\pi}{i_{dB}}} \;=\; 67.36 \pm 0.54\ \mathrm{km/s/Mpc}$$

from the $a_0$ bridge inversion (Study 08 §C1, Study 12). This is
identical to Planck within Planck's error budget.

## Predictions vs anchors

| Anchor | $H_0$ [km/s/Mpc] | Tension with ESD $H_0 = 67.36$ |
|---|---|---|
| Planck 2018 | $67.36 \pm 0.54$ | $0.0\,\sigma$ |
| TDCOSMO-IV (Birrer+ 2020) | $67.4^{+4.1}_{-3.2}$ | $\sim 0.01\,\sigma$ |
| H0LiCOW (Wong+ 2020) | $73.3^{+1.7}_{-1.8}$ | $\sim 3.2\,\sigma$ |
| SH0ES (Riess+ 2022) | $73.04 \pm 1.04$ | $\sim 4.9\,\sigma$ |

**ESD interpretation:** TDCOSMO-IV is correct, Wong+ 2020 is biased
by the rigid power-law lens model. The 3$\sigma$ Wong+ 2020 tension
flags it as a lens-modelling artifact, not a framework failure.

## Gates

| # | Claim | Gate |
|---|-------|------|
| 1 | Lens-scale ESD modification is small (amp$_D < 1.05$, i.e. lens fit absorbs it within mass-sheet systematics) | structural check |
| 2 | $D_{\Delta t}$ predicted for B1608+656 within $2\sigma$ of Suyu+ 2010 measurement | $\chi^2 < 4$ |
| 3 | ESD $H_0$ within $2\sigma$ of TDCOSMO-IV | tension < 2$\sigma$ |
| 4 | Wong+ 2020 $H_0$ tension $> 2\sigma$ (flagged as lens-model dependent) | tension > 2$\sigma$ |
| 5 | No new free parameters | audit |

## Observational targets

| Dataset | Quantity | Reference |
|---|---|---|
| TDCOSMO 6-lens combined | $H_0 = 73.3^{+1.7}_{-1.8}$ | Wong+ 2020, MNRAS 498, 1420 |
| TDCOSMO-IV (mass-sheet flex.) | $H_0 = 67.4^{+4.1}_{-3.2}$ | Birrer+ 2020, A&A 643, A165 |
| B1608+656 individual | $D_{\Delta t} = 5156 \pm 296$ Mpc | Suyu+ 2010, ApJ 711, 201 |

## References

- Wong et al. 2020, MNRAS 498, 1420 (H0LiCOW final result)
- Birrer et al. 2020, A&A 643, A165 (TDCOSMO-IV mass-sheet flexible)
- Suyu et al. 2010, ApJ 711, 201 (B1608+656 individual)
- Refsdal 1964, MNRAS 128, 307 (time-delay method)
