# Paper / data references

Study 06 is a closed-form audit -- not a paper reproduction in the
sense of Studies 02-05. Its purpose is to take every reading-independent
lock the ESD framework already commits to and confront it with the
published constraints from the canonical CMB / LSS / BBN / weak-lensing
surveys.

## Framework reference

> Higginson, J. P. (2026). *Gravity, Electromagnetism, and the Dark
> Sector from a Single Displacement Action with Zero Free Parameters.*
> Zenodo. DOI: [10.5281/zenodo.19283596](https://doi.org/10.5281/zenodo.19283596).
> Chs. 4, 14, 15 (Identities A, B; primordial locks; reheating chain).

## Survey constraints used in the audit

| Tag             | Reference |
|-----------------|-----------|
| Planck 2018     | Aghanim et al., *Planck 2018 results. VI. Cosmological parameters*, A&A 641, A6 (2020) -- TT,TE,EE+lowE+lensing baseline. |
| KiDS-1000       | Asgari et al., *KiDS-1000 cosmology: Cosmic shear constraints*, A&A 645, A104 (2021). |
| DES Y3          | Amon et al. PRD 105, 023514 (2022); Secco et al. PRD 105, 023515 (2022). |
| SH0ES           | Riess et al., *A Comprehensive Measurement of the Local Value of the Hubble Constant*, ApJL 934, L7 (2022). |
| BBN (Cooke+2018)| Cooke, Pettini & Steidel, *One Percent Determination of the Primordial Deuterium Abundance*, ApJ 855, 102 (2018). |
| BICEP/Keck-21   | BICEP/Keck Collaboration, *Improved Constraints on Primordial Gravitational Waves...*, PRL 127, 151301 (2021).  95% upper limit $r_{0.05} < 0.036$. |
| McGaugh+2016    | McGaugh, Lelli & Schombert, *Radial Acceleration Relation in Rotationally Supported Galaxies*, PRL 117, 201101 (2016). |

## What the framework commits to

Every number on the *lock* side of the audit table is derived in
closed form from the locked golden-ratio constants ($\varphi$,
$c = c_{\rm channel}$, $N_*$), with no per-observable tuning:

- $\Omega_\Lambda = 2\pi c^2 / 3$, $\Omega_m = 1 - \Omega_\Lambda$ (Identity A)
- $3\Omega_{DM} + \Omega_b = 8\pi c^4 \Omega_m$ (Identity B)
- $n_s = 1 - 2/N_*$, $r = 12/N_*^2$, $\alpha_s = -2/N_*^2$ (Starobinsky slow-roll at $N_*$)
- $a_0 = c H_0 \sqrt{(3\Omega_{DM} + \Omega_b)/(8\pi)}$ (Study 04)
- $S_8 = 0.830426$ via CLASS at the locked $(\Omega_m,\Omega_b,n_s,A_s,H_0)$ (Study 01)

## Two readings of Identity B

The framework admits two operational readings -- they differ only on
$\Omega_b$, $\Omega_{DM}$, and the derived $\omega_b h^2$:

- **Primary** (boundary-input): $\Omega_b$ is taken from observation
  (Planck 2018: 0.0493), and $\Omega_{DM}$ is solved from Identity B.
- **Closure-pool** (zero-parameter): $\Omega_b$ is derived from $c$
  alone using Identity B closed against matter closure
  ($\Omega_m = \Omega_b + \Omega_{DM}$). Gives $\Omega_b = 0.050094$.

Every other observable in this audit is reading-independent.
