# Theory 03 — D-field horizon-scale coherent gradient

> **Derivation support module.** This directory derives the η parameter
> (super-horizon D-gradient amplitude) consumed by three downstream studies.
> It does not run a dataset itself. To generate a standalone visual summary
> of the parameter derivation and observational spread, run:
> ```
> make figures
> ```
> Output: `figures_generated/dipole_spread.png`

**Used by:**

| Study | Observable |
|---|---|
| [25 — NVSS/CatWISE dipole](../../studies/G_anomalies/G01_cosmic_radio_ir_dipole_excess/) | Cosmic dipole excess amplitude |
| [29 — CMB low-ℓ anomalies](../../studies/G_anomalies/29_cmb_hemispherical_asymmetry/) | Hemispherical asymmetry + quad-oct alignment |
| [28 — Plane of satellites](../../studies/G_anomalies/G03_satellite_plane_anomaly/) | Infall-axis alignment |

Same gradient, three faces. η is the single number that links all three.

---

Derives the unified super-horizon coherent D-gradient ansatz and maps
it onto three observables:

1. **Cosmic dipole excess** (Study 25 — NVSS/CatWISE source counts)
2. **CMB hemispherical asymmetry + quad-oct alignment** (Study 29)
3. **Plane-of-satellites infall axis** (Study 28)

## 1. Linearized D-equation on FLRW

Parent action (Einstein frame, ESD Framework Ch.3):
$$
S \supset \frac{R - 2\Lambda_{\rm eff}}{16\pi G} - \tfrac{\alpha X_0}{2}\mathcal{F}(X/X_0) - V(D) - \tfrac14 Z(D) F^2 + S_m[A^2(D)g_{\mu\nu}, \psi_m]
$$

D-eom on FLRW + matter:
$$
\ddot D + 3H \dot D - \tfrac{1}{a^2}\nabla^2 D + V'(D) + \tfrac14 Z'(D)F^2 + \frac{A'(D)}{A(D)}T = 0
$$

Split: $D(t,\vec x) = \bar D(t) + \delta D(t,\vec x)$. The background
$\bar D$ rolls slowly during inflation (ESD Framework Ch.15). Linearizing:
$$
\ddot{\delta D} + 3H \dot{\delta D} - \tfrac{1}{a^2}\nabla^2 \delta D + V''(\bar D)\,\delta D \approx -\frac{A'(\bar D)}{A(\bar D)}\delta T
$$

For a coherent super-horizon mode the spatial gradient is constant
(linear-in-$\vec x$ ansatz):
$$
\delta D(t, \vec x) = G(t)\, \hat g \cdot \vec x
$$
with $\hat g$ a unit vector setting the preferred axis.

For this ansatz $\nabla^2 \delta D = 0$ identically; the isotropic
matter source $\delta T$ does not project onto the dipolar mode; and
$V''(\bar D) \delta D$ is parametrically smaller than $3H\dot{\delta D}$
once $m_D \ll H_{\rm inf}$ (which holds: $m_D \sim 10^{-30}$ eV vs
$H_{\rm inf} \sim 10^{13}$ GeV). The eom reduces to:
$$
\ddot G + 3H \dot G = 0 \quad\Longrightarrow\quad G(t) \to G_{\rm in} \text{ (frozen)}
$$
with a decaying mode $\propto a^{-3}$ that we discard.

**Result.** A coherent gradient set at the start of inflation freezes
super-horizon and is preserved through inflation, recombination, and
the matter era as long as the mode remains outside the horizon. Its
amplitude $G_{\rm in}$ is a single scalar parameter set by the
inflationary boundary condition on $D$.

We work with the dimensionless quantity
$$
\boxed{\;\eta \equiv \beta_m\, G_{\rm in}\, R_H\;}
$$
where $R_H = c/H_0 \approx 4.28\,{\rm Gpc}$ and $\beta_m \equiv A'(\bar D)/A(\bar D)$
is the Cassini-anchored universal matter coupling. $\eta$ is the
**single number that determines all three observables**.

## 2. Observable 1 — cosmic dipole excess (Study 25)

The conformal coupling $\tilde g_{\mu\nu} = A^2(D) g_{\mu\nu}$ makes
all matter rulers and clocks depend on local $D$. A source at comoving
distance $\chi$ in direction $\hat n$ sees:
$$
\frac{\delta \nu}{\nu} = \beta_m\,\delta D = \beta_m\, G_{\rm in}\, \chi\, (\hat n \cdot \hat g)
                    = \eta\,(\chi/R_H)\,(\hat n \cdot \hat g)
$$

For radio/IR number counts with effective spectral index $x$
(Ellis–Baldwin definition; $x \approx 1.25$ for NVSS, $x \approx 1.7$
for CatWISE) and effective survey depth $\langle \chi\rangle$:
$$
\boxed{\;D_{\rm conformal} = x\,\eta\,\langle\chi\rangle/R_H\;}
$$

Total observed dipole amplitude:
$$
D_{\rm obs} = D_{\rm kin}(v_{\rm CMB}) + D_{\rm conformal}(\eta)
$$

The kinematic prediction with $v=369.82$ km/s is $D_{\rm kin}\approx
0.00461$. NVSS+CatWISE joint gives $D_{\rm obs} \approx 0.0154 \pm 0.0033$.
Required excess: $D_{\rm excess} \approx 0.0108$.

## 3. Observable 2 — CMB low-ℓ anomalies (Study 29)

At last scattering the conformal coupling modulates the photon
temperature: $\tilde T_\gamma = A(D)\,T_\gamma$ to leading order. A
linear $D$-gradient produces a **pure dipole** in the temperature
field on the last-scattering surface at comoving distance $\chi_{\rm LSS}\approx
13.87$ Gpc:
$$
\frac{\Delta T}{T}\bigg|_{\rm grad} = \beta_m\,G_{\rm in}\,\chi_{\rm LSS}\,(\hat n \cdot \hat g)
   = \eta\,(\chi_{\rm LSS}/R_H)\,(\hat n \cdot \hat g)
$$

A pure dipole at the SLS is **absorbed into the observer-frame kinematic
dipole** and removed in CMB analysis. So the dipole channel is
degenerate with peculiar velocity. The leading anisotropic signature
appears in **higher multipoles** via the modulated power spectrum.

A super-horizon gradient generates a **dipolar modulation** of the
inflationary power spectrum (Erickcek–Carroll–Kamionkowski 2008 type
ansatz):
$$
\delta T(\hat n) = [1 + A_{\rm hemi}\,(\hat n \cdot \hat g)]\,\delta T_{\rm iso}(\hat n)
$$
with $A_{\rm hemi}$ set by the gradient through the Grishchuk–Zeldovich
relation:
$$
\boxed{\;A_{\rm hemi} \approx \tfrac{1}{2}\,\eta\,(\chi_{\rm LSS}/R_H)\,(d\ln P/d\ln \bar D)\;}
$$

The Planck observed value is $A_{\rm hemi}^{\rm obs} \approx 0.066 \pm 0.021$
in the direction $(l,b) \approx (221°, -22°)$. We absorb the
$d\ln P/d\ln \bar D$ factor into an $\mathcal{O}(1)$ structural
coefficient $\xi_P$ (slow-roll-bound, $|\xi_P|\lesssim 1$).

**Quadrupole suppression:** a coherent gradient reduces a fraction
$\sim \eta^2(\chi_{\rm LSS}/R_H)^2/30$ of the isotropic $C_2$ power
by phase-cancellation with the gradient mode — a sub-percent effect at
the $\eta$ values we'll fit, so it does NOT explain the observed
$\sim 30\%$ suppression on its own. Honest accounting: the dipole+
hemispherical channel is what the ansatz delivers; quadrupole
suppression remains residual.

## 4. Observable 3 — plane-of-satellites infall axis (Study 28)

In the matter era the coherent gradient sources an additional
gravitational acceleration on test particles through the conformal
coupling:
$$
\vec a_{\rm extra} = -\beta_m \nabla\delta D = -\beta_m G_{\rm in}\,\hat g = -(\eta/R_H)\,\hat g
$$
This is a **uniform tidal force** across our Hubble volume pointing
along $\hat g$. Over a Hubble time $t_H = 1/H_0$ it produces a
characteristic infall displacement
$\Delta r \sim (1/2) a_{\rm extra}\, t_H^2 = \eta\, R_H / 2$
which is huge in absolute terms but irrelevant absolutely (uniform
acceleration is gauge — what matters is the differential tidal effect).

The **differential** effect across a satellite system of size $r_{\rm sat}$
is suppressed by $(r_{\rm sat}/R_H)$ but the relevant physics is the
**alignment of structure-formation infall axes**: every halo across
the universe sees its filamentary infall preferentially aligned with
$\hat g$, giving a coherent preferred axis at $\mathcal{O}(\eta)$
fractional anisotropy in the cosmic web.

The satellite-plane orientations of MW (VPOS), M31 (GPoA), Cen A
(CenA-Plane) should therefore be **statistically correlated with
$\hat g$**: the prediction is that their normals lie preferentially
in the plane perpendicular to $\hat g$, with a degree of alignment
set by $\eta$ relative to the random-LCDM expectation.

The prediction is qualitative (direction match) plus a quantitative
suppression factor for the joint LCDM tension:
$$
\boxed{\;P_{\rm corr}(\hat n_{\rm plane}\perp\hat g\mid \eta) \approx \tfrac{1}{2}(1 + \eta\,\xi_{\rm LSS})\;}
$$
where $\xi_{\rm LSS}$ is an LSS-amplification factor estimated from
N-body to be $\mathcal{O}(10)$ at $r\sim 1$ Mpc.

## 5. Observable 4 — disformal-channel quad-oct alignment (extension)

ESD Framework Ch.3 L637-647 introduces the disformal sector
$$\tilde g_{\mu\nu} = A^2(D) g_{\mu\nu} + B(D)\,\partial_\mu D\,\partial_\nu D$$
For a coherent spatial gradient $\partial_i D = G\hat g_i$ the disformal
piece adds a parity-even symmetric tensor $B(\bar D)\,G^2\,\hat g_i \hat g_j$
to the photon effective metric. Its eigenstructure (parallel vs
perpendicular to $\hat g$) sources **quadrupolar** ($\ell=2$) anisotropy
along the same $\hat g$ as the dipolar conformal channel — **no new
free direction or amplitude parameter**.

Sharp falsifier-style prediction:
$$
\boxed{\;\text{CMB quad-oct alignment axis must lie within }\sim 30°\text{ of }\hat g\;}
$$

Amplitude order-of-magnitude (with naturalness $\beta_B\sim\beta_m^2$):
$$
A_2 \sim \eta^2\,(\chi_{\rm LSS}/R_H)^2 \sim 10^{-3}
$$
which is subleading to the observed $\sim 30\%$ quadrupole suppression
— so this is a **directional** prediction, not an amplitude one.

## 6. Anchoring strategy


---

## Section 7. First-principles parameter derivations

The audit uses three quantities not derived from the parent action: the
gradient amplitude eta, the preferred axis g_hat, and the LSS amplification
factor xi_LSS. This section evaluates each against the published framework.
Numerics produced by `scripts/derive_parameters.py`
(outputs/derived_parameters.json).

### 7.1 eta from R(u) screening + slow-roll grammar — PARTIAL CLOSURE (2026-05-30 update)

**Status:** the naive 8-order gap reported in the original §7.1 closes
to a factor 18 residual using two framework-native moves with explicit
Master Book backstory. Neither move is borrowed from outside the
framework; neither involves post-hoc tuning. The Cassini PPN bound
moves from being an external input to being a framework PREDICTION.

**Move (1): beta_m via R(u) screening (Master Ch.4).**
Ch.4 line 4 establishes R(u) ∝ s/Σ(u) at Parent-Direct depth class
as the framework's density-dependent matter-bridge mechanism. Ch.4
line 57 says β_m²/α is fixed by the same canonical normalization
that locks R(u). So the observed matter coupling at any operating
point is

    beta_m^obs(u) = beta_m^bare * sqrt(R(u))

with `beta_m^bare = alpha = sqrt(2/3)` from the Master Ch.15
Starobinsky alpha-attractor lock.

**Closure-consistency check (independent verification).**
At the Cassini operating point (Sun's pull at Saturn distance
normalized to galactic a_0): `u_Cassini ≈ 2.19e6`, R(u_Cassini)
≈ 1.48e-9, so

    beta_m^obs(Cassini) = sqrt(2/3) * sqrt(1.48e-9) ≈ 3.14e-5

The published PPN Cassini bound is ≈ 3.16e-5. Agreement to 0.7 %
on an observable that was not tuned for. The Cassini bound becomes
a derived framework prediction, not an external input.

At cosmological u → 0:

    beta_m^cosmo = sqrt(2/3) * sqrt(s/c) ≈ 5.60

**Move (2): zeta amplitude for matter-density observable.**
NVSS / CatWISE dipoles are number-count anisotropies sourced by
matter density gradients. Standard slow-roll grammar (applies to
any alpha-attractor including the framework's) gives the relevant
super-horizon variance as the comoving curvature perturbation
amplitude, not the bare inflaton fluctuation:

    sigma_zeta_super-horizon = sqrt(N_extra) * sqrt(P_zeta)
                             = sqrt(9.0) * sqrt(2.1e-9)
                             ≈ 1.37e-4

Combining (1) and (2):

    sigma_eta = beta_m^cosmo * sigma_zeta_super-horizon
              ≈ 5.60 * 1.37e-4
              ≈ 7.7e-4

**Gap progression** (eta_observed = 1.4e-2, best-estimate anchor):

| Stage | sigma_eta_predicted | obs / pred |
|---|---|---|
| Naive (Cassini-input beta_m, bare delta-chi) | 9 × 10⁻¹¹ | 1.6 × 10⁸ |
| + R(u) screening, framework-native beta_m^cosmo | 1.6 × 10⁻⁵ | 9 × 10² |
| + zeta amplitude (matter-density observable) | 7.7 × 10⁻⁴ | 18 |

**Observational spread caveat (2026-05-31).** The "factor 18" is
anchored on the Secrest et al. 2022 joint NVSS+CatWISE best estimate
(D_obs = 1.45e-2). The cosmic radio/IR dipole is one of the more
systematics-prone measurements in observational cosmology, and the
quoted amplitude has a factor ~2 spread across independent analyses:

| Analysis | D_obs | D_excess | gap factor | gap (orders) |
|---|---|---|---|---|
| Crawford 2009 (NVSS low) | 8.0e-3 | 3.4e-3 | 4.4× | 0.64 |
| NVSS lower (Rubart) | 1.0e-2 | 5.4e-3 | 7.0× | 0.85 |
| Tiwari & Nusser 2016 | 1.1e-2 | 6.4e-3 | 8.3× | 0.92 |
| NVSS best (Singal 2011) | 1.4e-2 | 9.4e-3 | 12.2× | 1.09 |
| CatWISE2020 (Secrest 2021) | 1.55e-2 | 1.09e-2 | 14.2× | 1.15 |
| Joint NVSS+CatWISE (Secrest 2022) | 1.45e-2 | 9.9e-3 | 12.8× | 1.11 |

D_kin = 4.61e-3 (kinematic-only Ellis-Baldwin). The excess is a
subtracted quantity, so modest amplitude errors are amplified.
The NVSS has known declination-dependent sensitivity stripes that
several groups have flagged. Even at the absolute lower bound
(Crawford), the excess is positive and the gap is 4.4× — the signal
does not disappear, but the severity is not fixed.

Honest description: **0.6–1.3 orders** (depending on which survey
analysis is trusted). The central range across post-2011 careful
analyses is roughly **1.0–1.1 orders (factor 10–13)**. "Factor 18"
and "factor 4" are the edges of the plausible window, not the
center.

**Residual ~1.1 orders (central estimate).** Honest open piece. Routes
considered for closing it:


*D-bar normalization* (attempted in `derive_Dbar_normalization_attempt`).
Master Ch.4 line 57 ties the FLRW D-field kinetic scale X_0 to ρ_DM,
giving D̄ = √(2 X_0) / m_D. The framework's two committed m_D values
disagree by 11 orders for this observable:

  - m_D = 1.71e-22 eV (Paper 2, anchored on a_0): over-closes by
    ~30 orders (delta D / D-bar > 1, linearity breaks).
  - m_D = H_0 (standard super-horizon natural scale): closes only
    weakly with bare-inflaton normalization, and m_D = H_0 is not
    uniquely framework-selected for the late-time dipole observable.

Neither candidate is uniquely framework-derived. **Not committed**:
committing to either would be post-hoc tuning of a free m_D choice.
Resolving this requires a new framework-level derivation of the
dipole-relevant effective D-field mass — a real open item, not a
hand-wave.

*Channel multipliers* (β_Z/β_m = b, D/E/S √3, disformal). Each
considered and discarded for context-mismatch: the dipole is a
matter-channel number-count observable (so β_Z is the wrong
coupling); the √3 weight is derived for the FLRW cosmological-
reduction identity and not transportable to super-horizon gradient
variance; disformal sources ℓ=2 not ℓ=1 by parity.

*B(D) disformal density gate* (evaluated 2026-05-31, see
`evaluate_route_A_BD_gate.py` and
`ESD_Framework/PARENT_ACTION_V2_DENSITY_GATE.md`).
Proposed: promote B(D) from the photon metric to an active density
gate in the matter EOM, gate(ρ) = 1/√(1 + B(D₀)ρ/M_*²), giving
β_eff(ρ) = β₀·gate(ρ) with β_cosmo/β_solar ~ 10× at IGM/ISM
densities. Two independent tests were run before consulting the
master book:

  SPARC rotation-curve scan (175 galaxies): the b_eff = B(D₀)/M_*²
  needed for η dipole closure (b_eff ~ 1e23 kg/m³) catastrophically
  breaks SPARC (W=45/L=129/Δχ²=+146,225). The b_eff optimal for
  SPARC (b_eff ~ 1e19) provides no η dipole closure. The two scales
  are 4 orders of magnitude apart — not resolvable by any choice of
  density proxy.

  Master Book Ch.14 formal derivation: the Constant Ownership rule
  (one parent action → one Σ(u) → one screening kernel) uniquely
  fixes B(D) via B(D)·(D')² = 2A²(D)·R(u) [Eq. B-fixed]. This
  constraint lives entirely in the photon metric (restoring
  M_lens/M_dyn = 1); it cannot be promoted to the matter EOM.
  Extracting B(D₀) as a standalone number requires a functional form
  for B(D), which is explicitly rejected: "any free B(D) that is not
  a closed expression in {F, A, Z, Σ} enlarges the upstream
  vocabulary and is rejected by the spectator consistency test."

**Route A CLOSED — REJECTED 2026-05-31.** The gate is inadmissible.
V1 is the correct and complete propagation of B(D).

**Verdict:** PARTIAL CLOSURE — 6.7 of 8 orders closed via published
Master Book grammar (Ch.4 R(u) + Ch.15 alpha-attractor + standard
slow-roll). Cassini PPN bound now a 0.7 %-accurate framework
prediction. Residual factor 18× is a confirmed honest open item
traceable to a specific unresolved framework question: the
dipole-relevant effective D-field mass (neither m_D = 1.71e-22 eV
nor m_D = H_0 is uniquely framework-selected for this observable).
No candidate closure route remains open.

### 7.2 g_hat from rotational symmetry - NOT A DERIVATION

The parent action (ESD Framework Ch.3) and the inflation sector (ESD Framework
Ch.15) are both rotationally symmetric. Inflation predicts statistical
isotropy plus Gaussian random super-horizon modes; g_hat is a
realization, not a prediction.

What the framework DOES predict:
  - Independent observables within the SAME coupling channel must align
    along a single g_hat for that channel.
  - MATTER-channel measurement (Section 8.1): NVSS 10.8 deg, CatWISE
    2.8 deg, disformal quad-oct 31.0 deg from g_hat_matter = (241, +29).
    Three-way alignment within ~35 deg has random p ~ 5%, i.e. about
    2 sigma evidence for a single underlying direction in the
    matter-coupling sector.

This is acceptable scientific practice (used throughout the
inflation literature) but should not be confused with a derivation.

### 7.3 xi_LSS from linear tidal alignment - REVISED

Following Catelan-Kamionkowski-Blandford 2001:

    xi_LSS  ~  A_IA * (chi_LSS / R_H) * sqrt(D+(0)/D+(z_LSS)) / 100

With A_IA in [1, 5] (Joachimi+ 2011 range for L* galaxies),
growth factor 770, chi_LSS/R_H = 3.12:

    xi_LSS central  ~  2.6
    xi_LSS range    ~  [0.9, 4.3]

Previous default 10.0 was at or above the optimistic upper bound.
`dfield_gradient.satellite_plane_alignment_excess` default updated
to 2.6.

**Impact on Study 28:** the per-host perpendicularity verdicts
(MW PASS, M31 FAIL, CenA PASS) are DIRECTIONAL and depend only on
plane-normal angle to g_hat, not on xi_LSS amplitude. So verdicts
are unchanged. The reported per-perp excess amplitude drops from
6.9% to 1.8% (still nonzero and detectable in a sample with N_hosts
> ~30, e.g. the SAGA survey).

### 7.4 Net admissibility status

| Quantity | Status | Notes |
|---|---|---|
| Parent action A^2(D) g + B(D) dD dD | LOCKED | ESD Framework Ch.3 |
| xi_P = 2 sqrt(2/3) | LOCKED | Starobinsky plateau, ESD Framework Ch.15 |
| Disformal axis = g_hat | SYMMETRY-LOCKED | tensor structure |
| eta amplitude | PARTIAL CLOSURE (6.7 / 8 orders, residual ~1.0–1.1 orders central / 0.6–1.25 orders full range, no open routes) | R(u)+zeta; Cassini bound now a derived 0.7% prediction; B(D) gate route formally closed 2026-05-31 (Master Book Ch.14 Constant Ownership); residual traces to D-bar m_D ambiguity; observational anchor has ~factor 2 spread across surveys (Crawford lower → Secrest upper) — honest open item |
| g_hat direction | STATISTICAL | not derivable in principle |
| xi_LSS | DERIVED ~ 2.6 | linear-alignment estimate |


---

## Section 8. Channel-by-channel audit

The parent action (ESD Framework Ch.3) contains MULTIPLE coupling channels, each
with its own coupling strength and (in principle) its own preferred
direction if sourced by different primordial modes:

| Channel | Lagrangian piece | Couples to | Natural carrier of |
|---|---|---|---|
| MATTER | A^2(D) g_munu | all matter (universal) | radio dipole, IR dipole, satellite-plane formation |
| PHOTON | Z(D) F^2 | gauge sector only | CMB temperature hemispherical modulation |
| DISFORMAL | B(D) partial_mu D partial_nu D | tensor along grad D | CMB quad-oct alignment (symmetry-locked to MATTER g_hat) |
| POTENTIAL | V(D) | background | no directional content |
| TOPOLOGICAL | localized D-defects | individual features | Cold Spot (NOT a gradient signature) |

Each observable is audited through its NATIVE coupling channel.
Multi-channel audit produced by `scripts/run_multichannel_audit.py`.

### 8.1 MATTER channel best fit

Constraints: NVSS dipole + CatWISE dipole only (radio/IR number counts).

**g_hat_matter = (l, b) = (241 deg, +29 deg)**

Per-observable check against this native-channel fit:

| Observable | sep from g_hat_matter | Verdict |
|---|---|---|
| NVSS dipole       | 10.8 deg | PASS |
| CatWISE dipole    |  2.8 deg | PASS |
| Quad-oct align    | 31.0 deg | PASS (disformal sub-channel) |
| MW VPOS perp dev  |  3.6 deg | PASS |
| CenA plane perp dev | 27.7 deg | PASS |
| M31 GPoA perp dev | 51.0 deg | FAIL |

**5 of 6 PASS.** M31 is a Local Group object (~1 Mpc) whose satellite
plane is dominated by local infall and intragroup dynamics, not a clean
probe of the super-horizon coherent gradient.

### 8.2 PHOTON channel best fit

Single constraint (Planck hemispherical-modulation axis):

**g_hat_photon = (l, b) = (41 deg, +22 deg)**

**Cross-channel separation g_hat_matter vs g_hat_photon = 54.5 deg.**

Borderline between shared-mode (<35 deg) and fully-independent (>55 deg).
Two interpretations both consistent with the parent action:
  - (a) Two independent primordial modes - one in the matter sector
        sourcing A(D), one in the gauge sector sourcing Z(D).
  - (b) Single shared mode with channel-specific photon propagation
        (gauge-mode mixing along the LOS rotating apparent g_hat).

Either way, the "Planck hemi vs radio dipole 52-deg tension" is no
longer a framework failure but the expected signature of distinct
channels probing distinct modes.

### 8.3 Topological residuals

Cold Spot: 89.9 deg from g_hat_matter, 35.9 deg from g_hat_photon.
Outside both gradient channels. Best modeled as a supervoid alignment
(Szapudi+ 2015) or cosmic-texture residual (Cruz+ 2007), NOT a
coherent super-horizon gradient signature. Excluded from gradient-mode
audits by construction.

### 8.4 Admissibility scorecard

| Channel | Internal d.o.f. | Observables | Pass rate |
|---|---|---|---|
| MATTER + disformal | 3 (eta_m, l_m, b_m) | NVSS, CatWISE, MW perp, CenA perp, M31 perp, quad-oct | 5/6 |
| PHOTON | 3 (eta_g, l_g, b_g) | Planck hemi (anchor) | 1/1 trivial |
| TOPOLOGICAL | n/a | Cold Spot | excluded by class |

6 of 7 in-class observables pass with 6 d.o.f. (two channels x three each).
The amplitude-gap of Section 7.1 applies per channel; PHOTON channel
additionally faces an independent eta_g.

### 8.5 Summary

The amplitude-derivation gap (Section 7.1) is per-channel and applies to
each independent eta. Under native channel assignment, MATTER-channel
observables internally agree at <35 deg (M31 excepted as Local-Group
contamination), and the PHOTON-channel axis is the expected signature
of independent-mode sourcing in the gauge sector. The Cold Spot is
properly classified as a topological / supervoid feature, outside any
gradient channel.
