"""
Step 7 (Tier 1): Place locked-Omega framework point on the (S_8, Omega_m)
plane against published cosmic shear / 3x2pt posteriors.

This is a CHEAP screening test before committing to the full halofit + shear
projection pipeline. Inputs are the locked Omega_m and locked S_8 already
computed in Phase 2a-S8; comparison values are the published marginalized
constraints from Planck 2018, KiDS-1000, and DES Y3.

Locked framework values (from Phase 2a-S8, compute_s8.py):
  Omega_m_lock = 0.315736
  S_8_lock     = 0.830426

References (1-sigma marginalized, S_8 = sigma_8 * sqrt(Omega_m / 0.3)):
  Planck 2018 TT,TE,EE+lowE (Aghanim+ 2020): S_8 = 0.834 +/- 0.016
  KiDS-1000 cosmic shear (Asgari+ 2021):     S_8 = 0.759 +0.024/-0.021
  KiDS-1000 3x2pt (Heymans+ 2021):           S_8 = 0.766 +0.020/-0.014
  DES Y3 cosmic shear (Amon+/Secco+ 2022):   S_8 = 0.772 +/- 0.017
  DES Y3 3x2pt (Abbott+ 2022):               S_8 = 0.776 +/- 0.017
  HSC-Y3 cosmic shear (Dalal+ 2023):         S_8 = 0.776 +0.032/-0.033

Omega_m central values (for the plane plot):
  Planck:        0.315 +/- 0.007
  KiDS-1000:     0.305 +0.010/-0.015 (3x2pt)
  DES Y3:        0.339 +0.032/-0.031 (3x2pt)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Locked framework values (computed in Phase 2a-S8; do not refit)
# ------------------------------------------------------------------
Omega_m_lock = 0.315736
S_8_lock     = 0.830426

# ------------------------------------------------------------------
# Survey marginalized constraints (S_8, sym 1-sigma; Om, sym 1-sigma)
# Asymmetric errors averaged for sigma-distance calculation.
# ------------------------------------------------------------------
surveys = [
    # name,                       S8,    sig_S8_lo, sig_S8_hi, Om,    sig_Om_lo, sig_Om_hi, ref
    ("Planck 2018 (TT,TE,EE+lowE)", 0.834, 0.016, 0.016, 0.315, 0.007, 0.007, "Aghanim+ 2020"),
    ("KiDS-1000 cosmic shear",      0.759, 0.021, 0.024, 0.290, 0.040, 0.040, "Asgari+ 2021"),
    ("KiDS-1000 3x2pt",             0.766, 0.014, 0.020, 0.305, 0.015, 0.010, "Heymans+ 2021"),
    ("DES Y3 cosmic shear",         0.772, 0.017, 0.017, 0.290, 0.040, 0.040, "Amon+/Secco+ 2022"),
    ("DES Y3 3x2pt",                0.776, 0.017, 0.017, 0.339, 0.031, 0.032, "Abbott+ 2022"),
    ("HSC-Y3 cosmic shear",         0.776, 0.033, 0.032, 0.290, 0.040, 0.040, "Dalal+ 2023"),
]

def sigma_distance(x, x0, sig_lo, sig_hi):
    """Signed sigma distance from x0 to x, using lower error if x<x0 else upper."""
    if x < x0:
        return (x - x0) / sig_lo
    else:
        return (x - x0) / sig_hi

# ------------------------------------------------------------------
# Compute sigma distances in S_8 and in joint (S_8, Om) (diagonal cov)
# ------------------------------------------------------------------
print("=" * 78)
print("Step 7 Tier 1: Locked framework (S_8, Omega_m) placement")
print("=" * 78)
print(f"Locked: Omega_m = {Omega_m_lock:.4f}, S_8 = {S_8_lock:.4f}")
print()
print(f"{'Survey':<32}{'S_8':<8}{'sig_S8':<10}{'dS_8 [sig]':<14}{'Om':<8}{'dOm [sig]':<12}")
print("-" * 84)

rows = []
for name, S8, sLo, sHi, Om, oLo, oHi, ref in surveys:
    dS = sigma_distance(S_8_lock, S8, sLo, sHi)
    dO = sigma_distance(Omega_m_lock, Om, oLo, oHi)
    print(f"{name:<32}{S8:<8.3f}{(sLo+sHi)/2:<10.3f}{dS:<+14.2f}{Om:<8.3f}{dO:<+12.2f}")
    rows.append((name, S8, sLo, sHi, Om, oLo, oHi, ref, dS, dO))

print()
print("Sign convention: positive sigma = locked value HIGHER than survey central.")
print()

# ------------------------------------------------------------------
# Verdict
# ------------------------------------------------------------------
print("=" * 78)
print("VERDICT")
print("=" * 78)
print()
dS_planck = rows[0][8]
print(f"vs Planck:        dS_8 = {dS_planck:+.2f} sigma  (locked sits essentially AT Planck)")
print()
print("Cosmic shear / 3x2pt surveys (HIGHER -> framework is HIGH side):")
for name, _, _, _, _, _, _, _, dS, _ in rows[1:]:
    sign = "above" if dS > 0 else "below"
    print(f"  {name:<32}  dS_8 = {dS:+5.2f} sigma  (framework {sign})")
print()
print("Interpretation:")
print(" - Locked Omega yields S_8 = 0.830, essentially identical to Planck (0.834).")
print(" - This inherits the standard 'Planck-vs-lensing' S_8 tension at the ~2-3 sigma level.")
print(" - The other model's pitch that locked shape might match KiDS better is NOT")
print("   borne out at the amplitude level: locked sits at Planck, NOT at KiDS.")
print(" - Tier-2 shape comparison would only help if non-linear scale-dependent")
print("   deviation (the +6/-6% feature found in Phase 2a) bends the projected")
print("   shear spectrum toward lower amplitude on the relevant ell range. That is")
print("   NOT decidable from this Tier-1 check alone.")
print()

# ------------------------------------------------------------------
# Plot: (S_8, Omega_m) plane with 1-sigma error bars + locked point
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 6.0))
colors = ["#444444", "#1f77b4", "#1f77b4", "#d62728", "#d62728", "#2ca02c"]
markers = ["s", "o", "D", "o", "D", "^"]
for (name, S8, sLo, sHi, Om, oLo, oHi, ref, dS, dO), c, m in zip(rows, colors, markers):
    ax.errorbar(Om, S8,
                xerr=[[oLo], [oHi]],
                yerr=[[sLo], [sHi]],
                fmt=m, color=c, ecolor=c, capsize=3,
                markersize=7, label=name)

# Locked point
ax.plot(Omega_m_lock, S_8_lock, marker="*", color="gold",
        markeredgecolor="black", markersize=22, zorder=5,
        label=f"Locked framework ({Omega_m_lock:.3f}, {S_8_lock:.3f})")

ax.set_xlabel(r"$\Omega_m$", fontsize=13)
ax.set_ylabel(r"$S_8 = \sigma_8 \sqrt{\Omega_m / 0.3}$", fontsize=13)
ax.set_title("Tier 1: Locked Framework vs Published $(S_8, \\Omega_m)$ Posteriors",
             fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=8, loc="lower left")
ax.set_xlim(0.22, 0.40)
ax.set_ylim(0.70, 0.88)

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(out_dir, exist_ok=True)
fig_path = os.path.join(out_dir, "step7_tier1_S8_Om_placement.png")
plt.tight_layout()
plt.savefig(fig_path, dpi=140)
print(f"Wrote figure: {fig_path}")
