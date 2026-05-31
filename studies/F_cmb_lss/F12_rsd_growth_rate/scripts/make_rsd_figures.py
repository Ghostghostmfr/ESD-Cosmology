"""Figures for Study 39 - RSD f*sigma_8(z) compilation."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from rsd_data import FSIGMA8_MEASUREMENTS
from esd_rsd import fsigma8_predicted

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    z_grid = np.linspace(0.0, 2.0, 100)
    pred   = [fsigma8_predicted(z) for z in z_grid]

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    ax.plot(z_grid, pred, color="black", lw=2,
            label=r"ESD = $\Lambda$CDM (locked $\Omega_m=0.31574$, $\sigma_8=0.8111$)")

    zs   = np.array([m[1] for m in FSIGMA8_MEASUREMENTS])
    fss  = np.array([m[2] for m in FSIGMA8_MEASUREMENTS])
    sigs = np.array([m[3] for m in FSIGMA8_MEASUREMENTS])
    ax.errorbar(zs, fss, yerr=sigs, fmt="o", capsize=4, ms=6,
                color="C0", label="RSD measurements (17 surveys)")
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"$f(z)\,\sigma_8(z)$")
    ax.set_title("Study 39 - RSD growth-rate compilation vs ESD prediction")
    ax.set_xlim(0, 2.0); ax.set_ylim(0.1, 0.7)
    ax.legend(loc="lower left"); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    out = FIG_DIR / "fsigma8_compilation.png"
    plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
