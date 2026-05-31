"""Figures for Study 47 - z~0 fsigma_8 compilation."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pv_data import PECULIAR_VEL_MEASUREMENTS, ESD_FSIGMA8_Z0

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(9, 5))
    labels = [r[0] for r in PECULIAR_VEL_MEASUREMENTS]
    vals   = np.array([r[1] for r in PECULIAR_VEL_MEASUREMENTS])
    sigs   = np.array([r[2] for r in PECULIAR_VEL_MEASUREMENTS])
    y      = np.arange(len(vals))
    ax.axvline(ESD_FSIGMA8_Z0, color="green", lw=2,
               label=f"ESD locked: $f\\sigma_8(0) = {ESD_FSIGMA8_Z0:.3f}$")
    ax.errorbar(vals, y, xerr=sigs, fmt="o", capsize=4, ms=7,
                color="C0", label="Peculiar-velocity measurements")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis(); ax.set_xlabel(r"$f\sigma_8(z \approx 0)$")
    ax.set_title("Study 47 — Peculiar-velocity $f\\sigma_8(z{\\approx}0)$ vs ESD-locked")
    ax.set_xlim(0.25, 0.65); ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    out = FIG_DIR / "pv_fsigma8.png"; plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
