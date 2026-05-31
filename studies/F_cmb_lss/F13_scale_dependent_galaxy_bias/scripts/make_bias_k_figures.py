"""Figures for Study 45 - b(k) deviations."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from bias_k_data import BIAS_K_MEASUREMENTS

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(9, 5))
    labels = [r[0] for r in BIAS_K_MEASUREMENTS]
    vals   = np.array([r[1] for r in BIAS_K_MEASUREMENTS])
    sigs   = np.array([r[2] for r in BIAS_K_MEASUREMENTS])
    y      = np.arange(len(vals))
    ax.axvline(0.0, color="black", lw=2, label=r"ESD: $db/d\ln k = 0$")
    ax.axvspan(-0.05, 0.05, color="green", alpha=0.10,
               label=r"Observational $\sim 5\%$ tolerance band")
    ax.errorbar(vals, y, xerr=sigs, fmt="o", capsize=4, ms=7,
                color="C0", label="Measured deviation")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(r"max $|b(k_i) - \langle b\rangle|\,/\,\langle b\rangle$")
    ax.set_title("Study 45 — Linear bias k-dependence vs ESD constant-$b$ prediction")
    ax.set_xlim(-0.08, 0.10); ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    out = FIG_DIR / "bias_k.png"; plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
