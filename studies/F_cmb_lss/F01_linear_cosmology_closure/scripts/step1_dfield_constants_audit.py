"""
Phase 3 Step 1: D-field perturbation constants audit.

ESD Framework (Higginson 2026) Ch.4 reference values (LOCKED):
  - a_0 = c_closure^2 * c_light * H_0 * sqrt(Omega_m)     [Eq. gravity-a0-image-master]
  - a_0 = c_light * H_0 * sqrt((3*Omega_DM + Omega_b)/(8 pi))   [Eq. gravity-a0-cosmo-master]
  - m_D * c^2 = a_0 * phi / sqrt(8 pi)  [Eq. gravity-mD-master, natural-unit form]
  - lambda_D = c^2 / (a_0 * phi) * sqrt(8 pi)            [inverse of above]
  - beta_Z / beta_m = b = phi^6 - 2  at  u = 1            [Eq. gravity-channel-ratio]

ESD Framework (Higginson 2026) Ch.4 L57 (CRITICAL): "the same canonical normalization that
locked the golden-ratio response eliminates the remaining action-side
ratio beta_m^2/alpha".  -> beta_m^2/alpha is NOT a free closure-locked
number; it is structurally absorbed into a_0 itself.

This script:
  1. Computes the locked closure constants numerically.
  2. Computes m_D and lambda_D in SI.
  3. Computes lambda_D / R_H (Hubble radius ratio) -- decides whether the
     Compton scale is sub- or super-horizon.
  4. Computes (k / m_D)^2 for the observable k-window of Phase 2a
     (kmin=1e-5, kmax=1e+2 1/Mpc) -- this is the Yukawa enhancement
     suppression factor W(k, m_D) = k^2 / (k^2 + m_D^2).
"""
from __future__ import annotations
import math
import numpy as np

# --- Master closure pool ---
PHI = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI = math.log(PHI)
C_CLOSURE = (4.0 * LN_PHI - 1.0) / PHI            # ~ 0.57158707
S_CLOSURE = 16.0 * PHI + 1.0                       # ~ 26.8885
B_CLOSURE = PHI**6 - 2.0                            # ~ 15.9443

# --- SI / cosmology ---
C_LIGHT = 2.99792458e8                              # m/s
H0_KMSMPC = 67.36                                   # Planck-2018, framework boundary
MPC_M = 3.0857e22
H0_SI = H0_KMSMPC * 1.0e3 / MPC_M                   # ~ 2.184e-18 s^-1

OMEGA_M = 0.315736   # framework lock (Ch.4 identities A+B)
OMEGA_DM = 0.265642
OMEGA_B = 0.050094

print("=" * 68)
print("Phase 3 Step 1: D-field Compton scale & Yukawa-window audit")
print("=" * 68)

# --- closure pool ---
print("\n[1] Closure constants (Ch.2 L33)")
print(f"    phi      = {PHI:.10f}")
print(f"    ln(phi)  = {LN_PHI:.10f}")
print(f"    c (closure) = (4 ln phi - 1)/phi = {C_CLOSURE:.10f}")
print(f"    s = 16 phi + 1 = {S_CLOSURE:.10f}")
print(f"    b = phi^6 - 2  = {B_CLOSURE:.10f}")

# --- a_0 derivation, two routes (Ch.4) ---
print("\n[2] a_0 derivation (Ch.4 cosmological reduction)")
a0_route1 = C_CLOSURE**2 * C_LIGHT * H0_SI * math.sqrt(OMEGA_M)
a0_route2 = C_LIGHT * H0_SI * math.sqrt((3.0*OMEGA_DM + OMEGA_B) / (8.0 * math.pi))
print(f"    Route 1: a_0 = c^2 * c_light * H_0 * sqrt(Om)   = {a0_route1:.4e} m/s^2")
print(f"    Route 2: a_0 = c_light * H_0 * sqrt((3OmDM+Omb)/8pi) = {a0_route2:.4e} m/s^2")
print(f"    Consistency check (relative): {abs(a0_route1-a0_route2)/a0_route2:.3e}")
print(f"    MOND-fit reference   a_0_obs = 1.20e-10 m/s^2")
A0 = a0_route2

# --- m_D & Compton scale ---
print("\n[3] m_D from Ch.4 Eq. gravity-mD-master")
print("    m_D * c^2 = a_0 * phi / sqrt(8 pi)  [natural-unit form]")
print("    => lambda_D = c^2 * sqrt(8 pi) / (a_0 * phi)")
LAMBDA_D = C_LIGHT**2 * math.sqrt(8.0 * math.pi) / (A0 * PHI)
print(f"    lambda_D = {LAMBDA_D:.4e} m")
# inverse length
mD_inv_m = 1.0 / LAMBDA_D
print(f"    m_D (as 1/lambda_D) = {mD_inv_m:.4e} m^-1")
# in 1/Mpc
mD_invMpc = mD_inv_m * MPC_M
print(f"    m_D = {mD_invMpc:.4e} 1/Mpc")

# Hubble radius
R_H = C_LIGHT / H0_SI
R_H_Mpc = R_H / MPC_M
print(f"\n    Hubble radius R_H = c/H_0 = {R_H:.4e} m  = {R_H_Mpc:.4e} Mpc")
print(f"    lambda_D / R_H    = {LAMBDA_D/R_H:.4f}")
if LAMBDA_D > R_H:
    print("    >>> SUPER-HORIZON: D-field Compton scale exceeds the Hubble radius.")
else:
    print("    >>> SUB-HORIZON: D-field Compton scale fits inside the Hubble radius.")

# --- Yukawa window for Phase 2a k-range ---
print("\n[4] Yukawa suppression W(k, m_D) = k^2 / (k^2 + m_D^2)")
print("    Phase 2a k-window: 1e-5 to 1e+2  1/Mpc, 7 sample modes")
k_grid = np.logspace(-5, 2, 8)  # 1/Mpc
W = k_grid**2 / (k_grid**2 + mD_invMpc**2)
print(f"    {'k [1/Mpc]':>12}  {'W(k,m_D)':>14}  {'k/m_D':>14}")
for k, w in zip(k_grid, W):
    print(f"    {k:12.4e}  {w:14.6e}  {k/mD_invMpc:14.4e}")

print("\n[5] Verdict")
if mD_invMpc < k_grid.min() / 1e3:
    print("    m_D << k for ALL observable modes.")
    print("    -> Yukawa factor W ~ 1 across the entire window.")
    print("    -> Fifth-force is SCALE-INDEPENDENT inside observable cosmology.")
    print("    -> Any matter-side coupling renormalizes Newton's constant uniformly")
    print("       and is degenerate with G itself at the linear-perturbation level.")
elif mD_invMpc > k_grid.max() * 1e3:
    print("    m_D >> k for ALL observable modes.")
    print("    -> Yukawa factor W ~ 0 across the entire window.")
    print("    -> Fifth-force is fully screened on all observable scales.")
else:
    print("    m_D lies within (or near) the observable k-window.")
    print("    -> Scale-dependent fifth-force signature is observable.")
    print("    -> Modified-growth f sigma_8(z) is a clean discriminator.")

print("\n[6] beta_m^2 / alpha status (Ch.4 L57)")
print("    NOT a free closure-locked number.")
print("    The action-side ratio is structurally eliminated by the same")
print("    canonical normalization that locks the golden-ratio response.")
print("    -> action-level couplings enter observables only through (a_0, m_D).")

print("\n[7] beta_Z / beta_m  (Ch.4 Eq. gravity-channel-ratio)")
print(f"    beta_Z / beta_m  |_(u=1)  =  b  =  phi^6 - 2  =  {B_CLOSURE:.6f}")
print("    -> EM-side channel ratio is closure-locked (no free dial).")
print("    -> relevant for disformal / clock-frequency observables, NOT linear growth.")

print("\n" + "=" * 68)
print("Summary saved -> step1_audit_summary.txt")
print("=" * 68)

with open("step1_audit_summary.txt", "w") as f:
    f.write(
        f"phi = {PHI:.10f}\n"
        f"c (closure) = {C_CLOSURE:.10f}\n"
        f"s = {S_CLOSURE:.10f}\n"
        f"b = {B_CLOSURE:.10f}\n"
        f"a_0 (Route 2) = {A0:.6e} m/s^2\n"
        f"lambda_D = {LAMBDA_D:.6e} m\n"
        f"m_D = {mD_invMpc:.6e} 1/Mpc\n"
        f"R_H = {R_H:.6e} m\n"
        f"lambda_D / R_H = {LAMBDA_D/R_H:.4f}\n"
        f"k-window min k/m_D = {k_grid.min()/mD_invMpc:.3e}\n"
        f"k-window max k/m_D = {k_grid.max()/mD_invMpc:.3e}\n"
    )
