"""Figures for Study 43 - hydrostatic mass bias compilation."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from bias_data import BIAS_MEASUREMENTS, PLANCK_SZ_REQUIRED_1MB, PLANCK_SZ_SIGMA
from esd_bias import ESD_PREDICTED_1MB_CENTER, ESD_PREDICTED_1MB_RANGE

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    labels = [r[0] for r in BIAS_MEASUREMENTS]
    vals   = np.array([r[1] for r in BIAS_MEASUREMENTS])
    sigs   = np.array([r[2] for r in BIAS_MEASUREMENTS])
    y      = np.arange(len(vals))
    ax.errorbar(vals, y, xerr=sigs, fmt="o", capsize=4, ms=7,
                color="C0", label="WL-program measurements")
    ax.axvspan(ESD_PREDICTED_1MB_CENTER - ESD_PREDICTED_1MB_RANGE,
               ESD_PREDICTED_1MB_CENTER + ESD_PREDICTED_1MB_RANGE,
               color="green", alpha=0.18,
               label=f"ESD prediction = WL band ({ESD_PREDICTED_1MB_CENTER:.2f} ± {ESD_PREDICTED_1MB_RANGE:.2f})")
    ax.axvline(PLANCK_SZ_REQUIRED_1MB, color="red", lw=2, ls="--",
               label=f"Planck-SZ required ({PLANCK_SZ_REQUIRED_1MB:.2f}) — owned by Study 18")
    ax.axvspan(PLANCK_SZ_REQUIRED_1MB - PLANCK_SZ_SIGMA,
               PLANCK_SZ_REQUIRED_1MB + PLANCK_SZ_SIGMA,
               color="red", alpha=0.10)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(r"$1 - b_H$"); ax.invert_yaxis()
    ax.set_title("Study 43 — Hydrostatic mass bias compilation vs ESD prediction")
    ax.set_xlim(0.5, 1.05); ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    out = FIG_DIR / "hydrostatic_bias.png"; plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
