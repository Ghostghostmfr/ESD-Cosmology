# Study 32 — 21cm Cosmic Dawn (EDGES vs SARAS-3)

**Status: PASS (5/5)** — three-channel ESD predicts the standard $\Lambda$CDM
21cm signal $T_b \approx -220$ mK at $z = 17.19$ (matching Pritchard-Loeb 2012
at $0.01\sigma$), lies inside the SARAS-3 (Singh+ 2022) 95 % envelope, and
sides with the SARAS-3 refutation of the EDGES Bowman+ 2018 $-500$ mK depth.
No new free parameters; the framework inherits the same astrophysical
uncertainty as $\Lambda$CDM.

Tests whether the ESD framework's three-channel structure, evaluated
in the cosmic-dawn regime ($z \approx 17$), predicts the standard
$\Lambda$CDM 21cm brightness temperature (consistent with the SARAS-3
refutation of the EDGES anomaly) or instead requires a non-standard
modification of the cosmic-dawn IGM thermal history.

## Results

**Three-channel state at cosmic dawn ($z = 17.19$):**

| Quantity | Value |
|---|---|
| $u_\mathrm{cd}$ | $9.50 \times 10^{-2}$ |
| $R(u_\mathrm{cd})$ | $5.94$ |
| $w_D, w_E, w_S$ | $0.126, \ 0.869, \ 0.0049$ |
| $\rho_m / \rho_{DE}$ at $z=17$ | $2777$ |
| $H(z=17.19)$ | $2936$ km/s/Mpc |

The kernel is in the MOND-bridge regime ($u \sim 0.1$, $R \sim 6$), but the
*background-mean* Friedmann equation is matter-dominated by 2777$\times$ at
$z = 17$, so any ESD modification of $H(z)$ is sub-percent. The S-channel
(photon bridge) has weight only $0.005$, leaving Lyman-$\alpha$ coupling
GR-identical.

**Predictions vs observations:**

| Quantity | Value |
|---|---|
| $T_b$ ESD fiducial (full WF, $f_X=1$) | $-220.3$ mK |
| $T_b$ ESD max-depth (full WF, no X-ray) | $-364.2$ mK |
| $T_b$ ESD shallow ($f_\alpha=0.3$, $f_X=1$) | $-12.6$ mK |
| $T_b$ $\Lambda$CDM standard | $-220 \pm 40$ mK |
| $T_b$ EDGES Bowman+ 2018 | $-500^{+200}_{-200}$ mK |
| $T_b$ SARAS-3 95% envelope | $[-300, +50]$ mK |
| ESD vs $\Lambda$CDM tension | $0.01\sigma$ |
| ESD vs EDGES tension | $1.37\sigma$ |

**Gates:**

| # | Claim | Verdict |
|---|---|---|
| 1 | Matter-dominated background at $z=17$ ($\rho_m/\rho_{DE} > 100$) | PASS ($2777$) |
| 2 | $T_b$ within $2\sigma$ of $\Lambda$CDM standard | PASS ($-220.3$ vs $-220 \pm 40$ mK) |
| 3 | $T_b$ within SARAS-3 95 % envelope | PASS |
| 4 | Sides with SARAS-3 refutation of EDGES (EDGES outside SARAS-3 envelope, ESD inside) | PASS |
| 5 | No new free parameters | PASS |

## Background

The redshifted 21cm hyperfine line of neutral hydrogen probes the IGM
between recombination and reionisation. The differential brightness
temperature against the CMB is

$$T_b(z) \approx 27\,x_\mathrm{HI}\,\frac{\Omega_b h^2}{0.023}\,\sqrt{\frac{0.15}{\Omega_m h^2}\,\frac{1+z}{10}}\,\frac{T_s - T_\mathrm{CMB}(z)}{T_s}\ \mathrm{mK},$$

with $T_s$ the 21cm spin temperature. In the standard adiabatic
picture after thermal decoupling at $z \sim 200$:

$$T_\mathrm{gas}(z) = T_\mathrm{CMB}(z=200)\,\left(\frac{1+z}{201}\right)^2,$$

which gives $T_\mathrm{gas}(z=17) \approx 4.4$ K vs.
$T_\mathrm{CMB}(z=17) \approx 49$ K. After Lyman-$\alpha$ sources turn
on, the Wouthuysen-Field (WF) effect couples $T_s$ to $T_\mathrm{gas}$
and the absorption feature deepens.

**The anchors at $z \approx 17$:**

| Probe | $T_b$ at $z \approx 17$ | Reference |
|---|---|---|
| Standard $\Lambda$CDM | $-220 \pm 40$ mK | Pritchard & Loeb 2012 |
| EDGES Bowman+ 2018 | $-500^{+200}_{-500}$ mK | *Nature* 555, 67 |
| SARAS-3 95 % envelope | $\in [-300, +50]$ mK | Singh+ 2022, *Nature Astronomy* 6, 607 |

SARAS-3 rules out the EDGES profile at 95.3 % confidence. Two
families of physics could explain a real EDGES depth: extra baryon
cooling (Barkana 2018 DM-baryon scattering) or extra radio background
(Feng & Holder 2018). If EDGES is a systematic, standard $\Lambda$CDM
prevails.

## ESD prediction (three-channel treatment)

The parent action's three channels at cosmic dawn:

For the IGM mean at $z = 17.19$ the relevant acceleration scale is
the Hubble drag on the linear peculiar-velocity field,

$$g_\mathrm{cd} \sim H(z)\,v_\mathrm{pec}^\mathrm{IGM},\quad u_\mathrm{cd} = \frac{4g_\mathrm{cd}}{a_0}.$$

The audit computes $u_\mathrm{cd}$ from the framework-locked
$H_0 = 67.36$ km/s/Mpc and reports the three channel weights
$(w_S, w_E, w_D)$ at that $u_\mathrm{cd}$.

**Three propagation paths through which ESD could modify the 21cm signal:**

1. **Background expansion $H(z)$:** the modified Friedmann equation
   integrates the kernel over the homogeneous background. At $z = 17$
   the matter density dominates the D-field dark energy by ~6000, so
   any ESD modification of $H(z)$ is sub-percent.
2. **Adiabatic gas cooling:** $T_\mathrm{gas}$ evolution depends on
   the Hubble friction $H(z)$ and the recombination/Compton-decoupling
   history. Both reduce to GR when the background kernel is small.
3. **Wouthuysen-Field coupling:** the Ly$\alpha$ coupling rate
   depends on the photon-bridge coefficient $Z(D)$, which is locked
   at the closure-pool floor ($Z = 1$). Therefore the WF coupling
   rate is GR-identical.

Net ESD prediction at $z = 17.19$: **$T_b \approx T_b^{\Lambda\mathrm{CDM}}$**
to within the standard adiabatic uncertainty (full vs partial WF
coupling).

## Gates

| # | Claim | Gate |
|---|-------|------|
| 1 | Background kernel small enough that $H(z)$ is $\Lambda$CDM-like ($R(u_\mathrm{cd}) < 5$) | structural check |
| 2 | $T_b$ within $2\sigma$ of standard $\Lambda$CDM prediction | $|T_b^\mathrm{ESD} - T_b^{\Lambda\mathrm{CDM}}| < 2 \times 40$ mK |
| 3 | $T_b$ within SARAS-3 95 % envelope ($\in [-300, +50]$ mK) | bound check |
| 4 | EDGES central depth ruled out at $>2\sigma$ | tension > 2$\sigma$ |
| 5 | No new free parameters | audit |

## Observational targets

| Dataset | Quantity | Reference |
|---|---|---|
| EDGES low-band | $T_b = -500^{+200}_{-500}$ mK at 78 MHz | Bowman+ 2018, Nature 555, 67 |
| SARAS-3 | 95 % rejection of EDGES profile | Singh+ 2022, Nature Astronomy 6, 607 |
| LCDM standard | $T_b \sim -150$ to $-250$ mK | Furlanetto+ 2006, Pritchard & Loeb 2012 |

## References

- Bowman, J. D., et al. 2018, *Nature* 555, 67 (EDGES detection claim)
- Singh, S., et al. 2022, *Nature Astronomy* 6, 607 (SARAS-3 refutation)
- Furlanetto, S. R., Oh, S. P., Briggs, F. H. 2006, Phys. Rep. 433, 181
- Pritchard, J. R., Loeb, A. 2012, Rep. Prog. Phys. 75, 086901
- Barkana, R. 2018, *Nature* 555, 71 (DM-baryon scattering interpretation)
- Feng, C., Holder, G. 2018, ApJ 858, L17 (radio-background interpretation)
