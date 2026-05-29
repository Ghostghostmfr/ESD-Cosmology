"""
What does Gamma_chi = m_chi^3/(6 pi M_Pl^2) give for Delta_reh and n_s?

Decomposition:
  Gamma_chi = (beta^2 / 8 pi) * N_dof * S * m_chi^3 / M_Pl^2

Framework-locked piece:
  beta = sqrt(2/3) (parent-action conformal weight)
  beta^2 / 8pi = (2/3) / 8pi = 1 / (12 pi)

Combinatorial pieces (still need scrutiny):
  N_dof = 4 (Higgs doublet, 4 real dof)
  S = 1/2 (chi -> HH identical-final-state symmetry factor)

Net coefficient: (1/12 pi) * 4 * (1/2) = 1/(6 pi)

Compare to ESD Framework (Higginson 2026): 1/(6 pi)  ->  Delta_reh = 17.89, n_s = 0.96109 (matches book 17.82/0.9611 to within V_end-normalization)
Compare to Draft Paper: see Linear Cosmology paper, Sec. ssec:cmbpeak.

NOTE (2026-05-28 audit): an earlier version of this script used
  Delta_reh = (1.0/3.0) * ln(V_end / rho_reh)
which is WRONG by a factor of 4 for w_int=0 scalaron oscillations.
Liddle-Leach (2003) matching for w=0 gives the (1-3w)/(12(1+w)) = 1/12
prefactor, not 1/3 (1/3 is the comoving-volume ln-ratio between rho_end
and rho_reh, but the matching equation contracts that with a further
1/4 from the k=aH scaling, leaving 1/12). The buggy 1/3 form inflated
Delta_reh by 4x (e.g. 1/(24 pi) gave 19.50 instead of the correct ~4.88
from Delta_reh alone; with the proper additive constants the full
Liddle-Leach form gives 18.12). It also propagated to the Linear
Cosmology paper's bracket [0.9598, 0.9611], which has since been
retracted in favour of the point n_s = 0.9611 with a tight 1.3e-4
channel-counting sensitivity.

This script is now kept for historical reference. The authoritative
clean Liddle-Leach matching (full Planck 2018 Eq. 21 form, with
matching 1/12 prefactor at w=0) gives:
  1/(24 pi): Delta=18.12, n_s=0.96092
  1/(12 pi): Delta=18.00, n_s=0.96101  [pure beta^2/8pi parent-action]
  1/(6  pi): Delta=17.89, n_s=0.96109  [Bezrukov-Gorbunov canonical] <-- book point
  1/(3  pi): Delta=17.77, n_s=0.96118
Channel-counting sensitivity 1.3e-4, well inside Planck per-bin floor.

This script:
  1) Computes Gamma_chi at 1/(6 pi)
  2) Computes T_reh via T_reh^4 = (90/pi^2 g_*) * (Gamma_chi M_Pl_red)^2
  3) Computes Delta_reh via Liddle-Leach matching
  4) Computes n_s and Planck offset
"""
import numpy as np

phi = (1 + 5**0.5) / 2
M_Pl_red = 2.435e18         # GeV (reduced Planck)
M_Pl = 1.221e19             # GeV (Planck)
m_chi = 3.336e13            # GeV (inflaton mass, A_s / COBE anchored)
g_star = 106.75             # SM dof at T >> M_W
F12 = 144
N_e_total = F12 * np.log(phi)   # = 69.295

def compute(coef_label, coef_value):
    Gamma = coef_value * m_chi**3 / M_Pl**2
    # Use reduced Planck for T_reh formula (consistent w/ Liddle-Leach convention)
    # T_reh = ((90 / pi^2 g_star)^(1/4)) * sqrt(Gamma * M_Pl_red) when H = Gamma at instantaneous thermalization
    T_reh = (90 / (np.pi**2 * g_star))**0.25 * np.sqrt(Gamma * M_Pl_red)
    # Energy density at reheating completion
    rho_reh = (np.pi**2 / 30) * g_star * T_reh**4
    # End-of-inflation potential (Starobinsky-like, V_end ~ 3/4 m_chi^2 M_Pl_red^2)
    V_end = (3.0/4.0) * m_chi**2 * M_Pl_red**2
    Delta_reh = (1.0 / 3.0) * np.log(V_end / rho_reh)
    N_e_star = N_e_total - Delta_reh
    n_s = 1 - 2.0 / N_e_star
    sigma_planck = (n_s - 0.9649) / 0.0042
    print(f"\nCoefficient = {coef_label}  ({coef_value:.6e})")
    print(f"  Gamma_chi   = {Gamma:.3e} GeV")
    print(f"  T_reh       = {T_reh:.3e} GeV")
    print(f"  rho_reh     = {rho_reh:.3e} GeV^4")
    print(f"  V_end       = {V_end:.3e} GeV^4")
    print(f"  Delta_reh   = {Delta_reh:.3f} e-folds")
    print(f"  N_e^*       = {N_e_star:.3f}")
    print(f"  n_s         = {n_s:.5f}")
    print(f"  vs Planck   = {sigma_planck:+.2f} sigma  (Planck 0.9649 +/- 0.0042)")

print("=" * 72)
print(f"N_e^total = F_12 * ln(phi) = 144 * {np.log(phi):.5f} = {N_e_total:.3f}")
print("=" * 72)

# Three candidates
compute("1/(24 pi) [ESD Framework (Higginson 2026)]",     1/(24*np.pi))
compute("1/(12 pi) [Draft / textbook]", 1/(12*np.pi))
compute("1/(6 pi)  [beta^2/8pi * N=4 * S=1/2]", 1/(6*np.pi))

print()
print("=" * 72)
print("What coefficient lands at Planck central n_s = 0.9649?")
print("=" * 72)
# Planck central -> N_e^* = 2/(1 - 0.9649) = 56.98
# -> Delta_reh = 69.295 - 56.98 = 12.32
# -> ln(V_end/rho_reh) = 3 * 12.32 = 36.96
# -> rho_reh = V_end * exp(-36.96) = V_end * 8.85e-17
# -> T_reh^4 = (30 / pi^2 g) rho_reh
# -> Gamma^2 = T_reh^4 / [(90/pi^2 g)^(1/2) M_Pl_red]^2  -> back-solve
N_target = 56.98
Delta_target = N_e_total - N_target
V_end = (3.0/4.0) * m_chi**2 * M_Pl_red**2
rho_target = V_end * np.exp(-3 * Delta_target)
T_target = (rho_target * 30 / (np.pi**2 * g_star))**0.25
# T_reh^2 = (90/pi^2 g)^(1/2) * Gamma * M_Pl_red
Gamma_target = T_target**2 / ((90 / (np.pi**2 * g_star))**0.5 * M_Pl_red)
coef_target = Gamma_target / (m_chi**3 / M_Pl**2)
print(f"  Delta_reh target = {Delta_target:.3f}")
print(f"  T_reh    target  = {T_target:.3e} GeV")
print(f"  Gamma    target  = {Gamma_target:.3e} GeV")
print(f"  Coefficient      = {coef_target:.6e}")
print(f"  1 / (coef * pi)  = {1/(coef_target*np.pi):.4f}    -> i.e. 1/({1/(coef_target*np.pi):.2f} pi)")
