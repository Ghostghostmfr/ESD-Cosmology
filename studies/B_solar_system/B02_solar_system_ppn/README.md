# Study 33 — Solar-system PPN (Cassini Shapiro + LLR)

**Status: PASS (5/5)** — three-channel ESD PPN deviations all lie far
below the Cassini and Lunar Laser Ranging bounds. No screening
mechanism required; the kernel's deep-UV behaviour does all the
work.

## Results

| Quantity | ESD prediction | Anchor 2σ bound | Safety factor |
|---|---|---|---|
| $|\gamma - 1|$ at Cassini geometry ($u = 3.6 \times 10^{12}$) | $1.3 \times 10^{-19}$ | $6.7 \times 10^{-5}$ (Bertotti+ 2003) | $5 \times 10^{14}$ |
| $|\beta - 1|$ at Mercury geometry ($u = 1.3 \times 10^{9}$) | $3.5 \times 10^{-22}$ | $3.3 \times 10^{-4}$ (Williams+ 2009) | $10^{18}$ |
| $|\eta_N|$ at Earth–Moon ($u = 2.0 \times 10^{8}$) | $1.0 \times 10^{-12}$ | $1.6 \times 10^{-3}$ (Williams+ 2012) | $1.6 \times 10^{9}$ |
| $|\dot G / G|$ | $1.4 \times 10^{-19}$ /yr | $1.0 \times 10^{-13}$ /yr (Williams+ 2009) | $10^{6}$ |

## Why ESD passes without screening

At Solar-system scales the gravitational acceleration vastly exceeds
the MOND scale $a_0 = 1.2 \times 10^{-10}$ m/s²:

$$u_\oplus = \frac{4 g_\oplus}{a_0} \sim 2 \times 10^8,\qquad u_\mathrm{Cassini} \sim 4 \times 10^{12}.$$

The closure kernel therefore sits in its deep-UV limit where the
photon-bridge channel dominates,

$$\Sigma(u) \approx u^\phi,\qquad R(u) = \frac{S_\mathrm{NORM}}{\Sigma(u)} \sim u^{-\phi}.$$

For $u \sim 10^{12}$, $R(u) \sim 10^{-19}$, and all three-channel PPN
deviations inherit this algebraic suppression directly from the
parent action. No chameleon, symmetron, or Vainshtein mechanism is
invoked — the suppression is structural.

The $\dot G/G$ prediction comes from cosmological drift of the D-field
background:

$$\dot G/G \sim 2 \beta_m^2 H_0 \sim 2 \times (3.16 \times 10^{-5})^2 \times 6.94 \times 10^{-11}\ /\mathrm{yr} \approx 1.4 \times 10^{-19}\ /\mathrm{yr},$$

six orders of magnitude below the LLR bound.

## Gates

| # | Claim | Verdict |
|---|---|---|
| 1 | $|\gamma - 1| < $ Cassini 2σ bound | PASS |
| 2 | $|\beta - 1| < $ LLR 2σ bound | PASS |
| 3 | $|\eta_N| < $ LLR Nordtvedt bound | PASS |
| 4 | $|\dot G/G| < $ LLR bound | PASS |
| 5 | No new free parameters ($\beta_m$ Cassini-bounded, kernel constants framework-locked) | PASS |

## References

- Bertotti, B., Iess, L., Tortora, P. 2003, *Nature* 425, 374 (Cassini Shapiro $|\gamma - 1| < 2.3 \times 10^{-5}$)
- Williams, J. G., Turyshev, S. G., Boggs, D. H. 2009, *IJMPD* 18, 1129 (LLR $\beta$, $\dot G/G$)
- Williams, J. G., Turyshev, S. G., Boggs, D. H. 2012, *Class. Quantum Grav.* 29, 184004 (LLR Nordtvedt update)
- Park, R. S., et al. 2017, *AJ* 153, 121 (MESSENGER Mercury perihelion)
- Will, C. M. 2014, *Living Rev. Relativity* 17, 4 (PPN review)
- Damour, T., Nordtvedt, K. 1993, *PRD* 48, 3436 (scalar-tensor $\dot G/G$ formula)
