"""Figures for Study 35: ISW amplitude across surveys."""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from isw_data import ISW_MEASUREMENTS

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    labels = [m[0] for m in ISW_MEASUREMENTS]
    z_med  = [m[5] for m in ISW_MEASUREMENTS]
    A_obs  = [m[1] for m in ISW_MEASUREMENTS]
    sig    = [m[2] for m in ISW_MEASUREMENTS]

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.axhline(1.0, color="black", lw=2, label=r"ESD = $\Lambda$CDM ($A = 1$)")
    ax.axhspan(0.85, 1.15, color="gray", alpha=0.15, label=r"$\pm 15\%$ band")
    for label, z, A, s in zip(labels, z_med, A_obs, sig):
        ax.errorbar(z, A, yerr=s, fmt="o", capsize=3, ms=6, label=label)
    ax.set_xlabel(r"survey median redshift $z_\mathrm{med}$")
    ax.set_ylabel(r"ISW amplitude $A_\mathrm{obs}/A_\mathrm{LCDM}$")
    ax.set_title("Study 35 — ISW × galaxy cross-correlation amplitude")
    ax.set_xlim(0.0, 1.5)
    ax.set_ylim(0.0, 2.2)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    plt.tight_layout()
    out = FIG_DIR / "isw_amplitude_vs_z.png"
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
