"""Figures for Study 44 - splashback compilation."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from splashback_data import (SPLASHBACK_MEASUREMENTS,
                             ESD_PREDICTED_RSP_R200M,
                             ESD_RSP_THEORY_RANGE)

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)
CHAM_MIN, CHAM_MAX = 0.70, 0.90


def main():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    labels = [r[0] for r in SPLASHBACK_MEASUREMENTS]
    vals   = np.array([r[1] for r in SPLASHBACK_MEASUREMENTS])
    sigs   = np.array([r[2] for r in SPLASHBACK_MEASUREMENTS])
    y      = np.arange(len(vals))
    ax.axvspan(ESD_PREDICTED_RSP_R200M - ESD_RSP_THEORY_RANGE,
               ESD_PREDICTED_RSP_R200M + ESD_RSP_THEORY_RANGE,
               color="green", alpha=0.18,
               label="ESD = $\\Lambda$CDM N-body band")
    ax.axvspan(CHAM_MIN, CHAM_MAX, color="red", alpha=0.12,
               label="Chameleon / fifth-force band (falsified)")
    ax.errorbar(vals, y, xerr=sigs, fmt="o", capsize=4, ms=7,
                color="C0", label="Measurements")
    ax.axvline(ESD_PREDICTED_RSP_R200M, color="green", lw=1.5)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis(); ax.set_xlabel(r"$R_\mathrm{sp}/R_{200m}$")
    ax.set_title("Study 44 — Splashback radius vs ESD and chameleon predictions")
    ax.set_xlim(0.6, 1.2); ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    out = FIG_DIR / "splashback.png"; plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
