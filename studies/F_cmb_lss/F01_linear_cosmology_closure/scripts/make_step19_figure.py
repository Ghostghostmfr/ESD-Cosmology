"""
Generate CMB residual plot for the linear cosmology paper.
Reads step19_cmb_residual.npz and produces a 2-panel figure:
  (top) TT spectrum overlay framework vs Planck-best
  (bottom) Residual (ESD/Planck - 1) for TT, TE, EE
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIGDIR = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(_FIGDIR, exist_ok=True)

data = np.load(os.path.join(_HERE, "step19_cmb_residual.npz"))
l   = data["l"]
TTP = data["TT_planck"]
TTF = data["TT_esd"]
TEP = data["TE_planck"]
TEF = data["TE_esd"]
EEP = data["EE_planck"]
EEF = data["EE_esd"]

# Use l >= 2
mask = (l >= 2) & (l <= 2500)
l  = l[mask]
TTP, TTF = TTP[mask], TTF[mask]
TEP, TEF = TEP[mask], TEF[mask]
EEP, EEF = EEP[mask], EEF[mask]

# Compute residuals (avoid div-by-zero in TE which can cross 0)
def safe_ratio(a, b):
    return np.where(np.abs(b) > 1e-3 * np.max(np.abs(b)), a/b - 1.0, np.nan)

resTT = safe_ratio(TTF, TTP) * 100
resTE = safe_ratio(TEF, TEP) * 100
resEE = safe_ratio(EEF, EEP) * 100

fig, axes = plt.subplots(2, 1, figsize=(7.0, 6.0), sharex=True,
                         gridspec_kw={"height_ratios": [2, 1.4], "hspace": 0.05})

# Top: TT spectrum overlay
ax0 = axes[0]
ax0.plot(l, TTP, color="black", lw=1.2, label=r"Planck-best $\Lambda$CDM ($n_s=0.9649$)")
ax0.plot(l, TTF, color="C3",   lw=1.2, ls="--",
         label=r"ESD prediction ($n_s=0.9611$)")
ax0.set_ylabel(r"$\mathcal{D}_\ell^{TT}\ [\mu\mathrm{K}^2]$")
ax0.set_xscale("log")
ax0.set_xlim(2, 2500)
ax0.set_ylim(0, 6500)
ax0.legend(loc="upper right", fontsize=9, frameon=False)
ax0.grid(alpha=0.3)
ax0.set_title(r"Framework vs Planck-best CMB anisotropy spectra",
              fontsize=10)

# Annotate first three peaks
peak_ls = [220, 540, 815]
for pl in peak_ls:
    i = np.argmin(np.abs(l - pl))
    ax0.annotate("", xy=(pl, TTP[i] + 100), xytext=(pl, TTP[i] + 400),
                 arrowprops=dict(arrowstyle="->", color="gray", lw=0.6))
ax0.text(220, 6100, r"$\ell_1\!\sim\!220$", ha="center", fontsize=8, color="gray")
ax0.text(540, 3200, r"$\ell_2\!\sim\!537$", ha="center", fontsize=8, color="gray")
ax0.text(815, 3100, r"$\ell_3\!\sim\!813$", ha="center", fontsize=8, color="gray")

# Bottom: residuals (TT + EE only; TE zero-crossings make ratio singular)
ax1 = axes[1]
ax1.axhline(0, color="black", lw=0.6, alpha=0.5)
ax1.fill_between([2, 2500], -0.5, 0.5, color="gray", alpha=0.15,
                 label=r"Planck per-bin systematic floor ($\pm 0.5\%$)")
ax1.plot(l, resTT, color="C0", lw=1.3, label="TT")
# Smooth EE residual by masking near zero-crossings of EE itself
EE_threshold = 0.05 * np.max(np.abs(EEP))
resEE_clean = np.where(np.abs(EEP) > EE_threshold, resEE, np.nan)
ax1.plot(l, resEE_clean, color="C2", lw=1.0, label="EE", alpha=0.75)
ax1.set_xlabel(r"Multipole $\ell$")
ax1.set_ylabel(r"$\mathcal{D}_\ell^{\rm ESD}/\mathcal{D}_\ell^{\rm Planck}-1\ [\%]$")
ax1.set_xscale("log")
ax1.set_xlim(2, 2500)
ax1.set_ylim(-1.5, 2.5)
ax1.legend(loc="upper right", fontsize=8, frameon=False)
ax1.grid(alpha=0.3)

plt.tight_layout()
out = os.path.join(_FIGDIR, "step19_cmb_peak_residual.png")
plt.savefig(out, dpi=180, bbox_inches="tight")
plt.savefig(out.replace(".png", ".pdf"), bbox_inches="tight")
print(f"Saved: {out} and .pdf")

# Print summary stats for the figure caption
print("\nFigure caption inputs:")
print(f"  TT peak-1 offset: {resTT[np.argmin(np.abs(l-220))]:+.2f}%")
print(f"  TT peak-2 offset: {resTT[np.argmin(np.abs(l-537))]:+.2f}%")
print(f"  TT at l=2000   : {resTT[np.argmin(np.abs(l-2000))]:+.2f}%")
print(f"  TT max |dev|   : {np.nanmax(np.abs(resTT)):.2f}%")
print(f"  EE at l=1000   : {resEE[np.argmin(np.abs(l-1000))]:+.2f}%")
