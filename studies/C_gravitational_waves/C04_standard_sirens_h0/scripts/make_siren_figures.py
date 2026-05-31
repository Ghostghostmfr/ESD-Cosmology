"""Figures for Study 40 - standard-siren H_0 vs ESD-locked."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from siren_data import SIREN_MEASUREMENTS, H_0_LOCKED

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(9.0, 5.5))
    labels = [m[0] for m in SIREN_MEASUREMENTS]
    H      = np.array([m[1] for m in SIREN_MEASUREMENTS])
    sp     = np.array([m[2] for m in SIREN_MEASUREMENTS])
    sm     = np.array([m[3] for m in SIREN_MEASUREMENTS])
    kinds  = [m[4] for m in SIREN_MEASUREMENTS]
    y = np.arange(len(labels))
    colors = ["C2" if k == "forecast" else "C0" for k in kinds]
    for i, c in enumerate(colors):
        ax.errorbar(H[i], y[i], xerr=[[sm[i]], [sp[i]]], fmt="o",
                    capsize=4, ms=7, color=c)
    ax.axvline(H_0_LOCKED, color="black", lw=2,
               label=f"ESD-locked $H_0 = {H_0_LOCKED}$ km/s/Mpc (Planck CMB)")
    ax.axvspan(67.36 - 0.54, 67.36 + 0.54, color="black", alpha=0.1,
               label="Planck 2018 1$\\sigma$")
    ax.axvline(73.04, color="C3", lw=1.5, ls="--",
               label="SH0ES $H_0 = 73.04$ (for context)")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$]")
    ax.set_xlim(60, 95)
    ax.set_title("Study 40 — standard-siren $H_0$ vs ESD-locked Planck value")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    out = FIG_DIR / "siren_H0.png"
    plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
