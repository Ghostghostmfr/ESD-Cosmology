"""
Phase-2a residual decomposition: WHAT is the 6% P(k) bump made of?

We have CLASS-lock (primary reading, Omega_b=0.0493 input) vs CLASS-Planck.
Both share H0=67.36, A_s=2.1e-9. They differ in:
  Omega_m   : 0.315736  vs 0.31530   (+0.14%)
  Omega_DM  : 0.265907  vs 0.26446   (+0.55%)   <-- from Identity B
  Omega_b   : 0.04930   vs 0.04930   ( 0%)      <-- matched
  n_s       : 0.961146  vs 0.96822   (-0.731%)  <-- framework: 1 - 2/N_e* = 0.961

We do NOT re-run Boltzmann. We use the existing CLASS-lock and CLASS-Planck
P(k) arrays from outputs/phase2a_locked_z0.npz to:

  (1) Strip the pure-tilt factor (k/k_pivot)^(Delta n_s) from the residual
      and see how much of the +6%/-5% is left.
  (2) Quote what fraction of the residual is "n_s tilt" vs "broadband transfer
      function shift from Omega_DM h^2 / Omega_m h^2".
"""
import os

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
d = np.load(os.path.join(_HERE, 'outputs', 'phase2a_locked_z0.npz'))
k = d['k']                # h/Mpc actually... let's check
P_lock = d['p_class_lock']
P_planck = d['p_class_planck']

# Pivot scale in Planck/CLASS is k_pivot = 0.05 / Mpc (NOT h/Mpc)
# Our k-grid in DISCO/CLASS run_phase2a_locked is built in 1/Mpc.
# Check by inspection of run_phase2a script.
n_s_lock   = 0.961146
n_s_planck = 0.96822
delta_n    = n_s_lock - n_s_planck
k_pivot    = 0.05   # 1/Mpc

r_observed = P_lock / P_planck - 1
tilt       = (k / k_pivot) ** delta_n
r_tilt     = tilt - 1
P_planck_with_tilt = P_planck * tilt
r_after_tilt = P_lock / P_planck_with_tilt - 1

# Window-binned decomposition
windows = [
    (1e-5, 5e-3, "large-scale equality"),
    (5e-3, 0.15, "cosmic-shear node"),
    (0.15, 1e2,  "small-scale Silk")
]

print("=" * 80)
print("PHASE 2A RESIDUAL DECOMPOSITION (PRIMARY reading, Omega_b=0.0493 input)")
print("=" * 80)
print(f"n_s lock   = {n_s_lock}")
print(f"n_s Planck = {n_s_planck}")
print(f"Delta n_s  = {delta_n:+.6f}   (framework prediction n_s = 1 - 2/N_e*)")
print(f"k_pivot    = {k_pivot} 1/Mpc")
print()
print(f"{'window':<26}{'max|r| obs %':<16}{'max|r| tilt %':<16}{'max|r| after-tilt %':<22}")
for lo, hi, name in windows:
    m = (k >= lo) & (k <= hi)
    obs_max = np.max(np.abs(r_observed[m])) * 100
    tilt_max = np.max(np.abs(r_tilt[m])) * 100
    after_max = np.max(np.abs(r_after_tilt[m])) * 100
    print(f"  {name:<24}{obs_max:<16.3f}{tilt_max:<16.3f}{after_max:<22.3f}")

print()
print(f"FULL RANGE:")
print(f"  observed       : max {np.max(np.abs(r_observed))*100:.3f}%  RMS {np.sqrt(np.mean(r_observed**2))*100:.3f}%")
print(f"  pure n_s tilt  : max {np.max(np.abs(r_tilt))*100:.3f}%  RMS {np.sqrt(np.mean(r_tilt**2))*100:.3f}%")
print(f"  AFTER stripping tilt: max {np.max(np.abs(r_after_tilt))*100:.3f}%  RMS {np.sqrt(np.mean(r_after_tilt**2))*100:.3f}%")
print()

# Point-by-point sanity
print("Spot checks:")
for k_target in [1e-5, 1e-3, 1e-2, 0.05, 1.0, 10.0, 100.0]:
    i = int(np.argmin(np.abs(k - k_target)))
    print(f"  k = {k[i]:.3e} 1/Mpc:  observed {r_observed[i]*100:+.3f}%   "
          f"tilt {r_tilt[i]*100:+.3f}%   after-tilt {r_after_tilt[i]*100:+.3f}%")
print()
print("INTERPRETATION:")
print("If 'after-tilt' is small everywhere, the 6% residual IS the framework's")
print("locked n_s = 1 - 2/N_e* prediction (Paper 1 / Ch.3 inflation slow-roll),")
print("NOT the Identity-B Omega_b derivation. Under PRIMARY reading the Omega_b")
print("plumbing contributes essentially zero to the residual.")
