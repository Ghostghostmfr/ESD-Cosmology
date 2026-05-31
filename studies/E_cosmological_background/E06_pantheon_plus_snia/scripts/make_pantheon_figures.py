"""Figures for Study 41 - Pantheon+ binned residuals."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pantheon_data import PANTHEON_BINNED_RESIDUALS

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    z   = np.array([r[0] for r in PANTHEON_BINNED_RESIDUALS])
    res = np.array([r[1] for r in PANTHEON_BINNED_RESIDUALS])
    sig = np.array([r[2] for r in PANTHEON_BINNED_RESIDUALS])
    ax.errorbar(z, res, yerr=sig, fmt="o", capsize=4, ms=7,
                color="C0", label="Pantheon+ binned residuals")
    ax.axhline(0.0, color="black", lw=2,
               label="ESD = $\\Lambda$CDM (Identity B)")
    ax.axhspan(-0.05, 0.05, color="black", alpha=0.05)
    ax.set_xscale("log")
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"$\mu_\mathrm{obs} - \mu_\mathrm{ESD}$ (mag)")
    ax.set_title("Study 41 — Pantheon+ distance-modulus residuals vs ESD background")
    ax.set_xlim(0.005, 2.5); ax.set_ylim(-0.12, 0.12)
    ax.legend(loc="upper right"); ax.grid(True, alpha=0.3, which="both")
    plt.tight_layout()
    out = FIG_DIR / "pantheon_residuals.png"
    plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
