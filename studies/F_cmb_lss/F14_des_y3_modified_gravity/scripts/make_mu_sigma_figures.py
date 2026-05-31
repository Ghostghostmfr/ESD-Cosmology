"""Figures for Study 46 - (mu_0, Sigma_0) compilation."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mu_sigma_data import PHENO_MG_MEASUREMENTS

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(7.5, 7))
    colors = ["C0","C1","C2","C3","C4"]
    for (surv, mu, smu, S, sS, _), col in zip(PHENO_MG_MEASUREMENTS, colors):
        ax.errorbar([mu], [S], xerr=[smu], yerr=[sS], fmt="o", ms=8,
                    capsize=4, color=col, label=surv)
    ax.scatter([0],[0], marker="*", s=350, color="green",
               edgecolor="black", zorder=5,
               label="ESD = $\\Lambda$CDM (mu_0=Sigma_0=0)")
    ax.axhline(0, color="gray", lw=0.7); ax.axvline(0, color="gray", lw=0.7)
    ax.set_xlabel(r"$\mu_0$"); ax.set_ylabel(r"$\Sigma_0$")
    ax.set_title("Study 46 — Phenomenological MG ($\\mu_0$, $\\Sigma_0$) vs ESD")
    ax.set_xlim(-1.0, 0.8); ax.set_ylim(-0.4, 0.4)
    ax.legend(loc="lower right", fontsize=8); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    out = FIG_DIR / "mu_sigma_plane.png"; plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
