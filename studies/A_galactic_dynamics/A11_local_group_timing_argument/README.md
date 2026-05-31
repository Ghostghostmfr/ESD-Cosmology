# Study A11 — Local Group timing argument

**Status:** 4/4 gates PASS at radial-orbit scope.

The Kahn & Woltjer (1959) timing argument fixes the total Local Group
mass from the radial orbit of M31 about MW. Under Newton, requiring
$r = 770$ kpc, $\dot r = -110$ km/s today at $t_0 = 13.7$ Gyr gives
$M_{\rm LG}^{\rm Newton} \simeq 4.5 \times 10^{12}\,M_\odot$, well in
excess of the directly observed baryonic mass of the Local Group
$M_{\rm LG}^{\rm baryon} \simeq 1.5 \times 10^{11}\,M_\odot$. The
"missing" factor $\sim 30$ is the dark-matter halo content under
$\Lambda$CDM.

ESD's closure kernel acts at $u = 4 g_N / a_0$. At LG separations,
$g_N \sim G M_b / r^2 \sim 10^{-12}\,{\rm m/s}^2$ for baryon-only
mass, giving $u \sim 0.04$ and $R(u) \sim O(40)$. The radial
equation under ESD becomes

$$
\ddot r = -\frac{G M_b}{r^2}\,(1 + R(u(r))),\qquad u(r) = \frac{4 G M_b}{a_0 r^2},
$$

which is nonlinear in $M_b$ through $R(u)$. We integrate this
equation backwards in time from today's $(r, \dot r)$ and solve by
shooting for the baryonic mass $M_b$ that lands $r = 0$ at $t = 0$.

## What this study tests

The fair ESD prediction is **not** that $M_{\rm LG}^{\rm Newton}$
agrees with anything — it doesn't, by construction. The fair
prediction is:

> Under ESD's local $R(u)$ boost, the *baryonic* mass required by
> the timing argument should agree with the directly measured Local
> Group baryonic mass.

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | Newton timing-argument mass reproduces canonical value | $M_{\rm LG}^N \in [3, 6]\times 10^{12}\,M_\odot$ | PASS |
| 2 | ESD baryonic timing-argument mass agrees with observed Local Group baryons | $M_{\rm LG}^{\rm ESD} \in [0.8, 3]\times 10^{11}\,M_\odot$ | PASS |
| 3 | ESD R(u) boost at the orbital scale is in the cluster-additive regime | $R(u_{\rm orbit}) \ge 10$ | PASS |
| 4 | $h$-blindness of the ESD mass (Thm 1, C1) | $\|dM/dh\| = 0$ | PASS |

## Run

```bash
cd studies/A_galactic_dynamics/A11_local_group_timing_argument
pip install -r requirements.txt
make all
```

## Scope boundary

- Two-body radial-orbit timing argument (Kahn & Woltjer 1959 form).
  Tangential motion of M31 (van der Marel+ 2012), cosmological
  expansion drag (Partridge+ 2013), and LMC infall (Peñarrubia+ 2016)
  not included; each shifts $M^N$ by $\sim 10$–30%.
- $R(u)$ treated as a local boost on the instantaneous radial
  Newtonian force. The full $R(u)$-curved orbit (with angular
  momentum and time-dependent EFE from external structures) is
  deferred to the binary-orbit extension.
- Observed Local Group baryonic mass adopted from
  McMillan 2017 (MW) + Tamm+ 2012 (M31) + dwarf-gas catalogues.
