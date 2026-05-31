"""Figures for Study 38 — n_s vs r plane with ESD prediction."""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from r_data import (R_CONSTRAINTS, ESD_R_PREDICTION,
                    ESD_R_RANGE_LOW, ESD_R_RANGE_HIGH, PLANCK_N_S, PLANCK_N_S_SIG)
from esd_inflation import r_predicted, n_s_predicted

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.2))

    # --- Panel A: n_s vs r plane ---
    ax = axes[0]
    N_e_grid = np.linspace(40, 80, 100)
    r_curve   = [r_predicted(N) for N in N_e_grid]
    n_s_curve = [n_s_predicted(N) for N in N_e_grid]
    ax.plot(n_s_curve, r_curve, color="C0", lw=2,
            label="Starobinsky plateau, $N_e \\in [40, 80]$")

    # Mark N_e=50, 60, 70 on curve
    for N in [50, 60, 70]:
        ax.scatter(n_s_predicted(N), r_predicted(N), color="C0", s=50, zorder=4)
        ax.annotate(f"$N_e={N}$", (n_s_predicted(N), r_predicted(N)),
                    xytext=(6, -2), textcoords="offset points", fontsize=8)

    # Planck n_s band (vertical)
    ax.axvspan(PLANCK_N_S - PLANCK_N_S_SIG, PLANCK_N_S + PLANCK_N_S_SIG,
               color="C3", alpha=0.15, label=f"Planck $n_s = {PLANCK_N_S}\\pm{PLANCK_N_S_SIG}$")
    # BK18 upper limit (horizontal)
    ax.axhline(0.036, color="black", lw=1.2, ls="--",
               label=r"BICEP/Keck BK18: $r<0.036$ (95% CL)")
    ax.fill_between([0.93, 1.00], 0.036, 0.2, color="gray", alpha=0.2)

    ax.set_xlabel(r"scalar spectral index $n_s$")
    ax.set_ylabel(r"tensor-to-scalar ratio $r$")
    ax.set_yscale("log")
    ax.set_xlim(0.93, 1.00)
    ax.set_ylim(1e-4, 0.2)
    ax.set_title(r"Panel A — $n_s$ vs $r$ plane")
    ax.legend(loc="lower left", fontsize=9)
    ax.grid(True, alpha=0.3, which="both")

    # --- Panel B: r prediction vs sensitivities ---
    ax = axes[1]
    labels  = [c[0] for c in R_CONSTRAINTS]
    vals    = np.array([c[1] for c in R_CONSTRAINTS])
    kinds   = [c[2] for c in R_CONSTRAINTS]
    y = np.arange(len(labels))
    colors = ["C3" if k == "upper95" else "C2" for k in kinds]
    ax.barh(y, vals, color=colors, alpha=0.7,
            label="upper limit (red) / forecast $\\sigma_r$ (green)")
    ax.axvline(ESD_R_PREDICTION, color="black", lw=2,
               label=f"ESD prediction $r = {ESD_R_PREDICTION:.1e}$ ($N_e=60$)")
    ax.axvspan(ESD_R_RANGE_LOW, ESD_R_RANGE_HIGH, color="black", alpha=0.1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xscale("log")
    ax.set_xlim(1e-5, 1.0)
    ax.set_xlabel(r"$r$  (upper limit or $\sigma_r$)")
    ax.set_title("Panel B — ESD prediction vs current limits and forecasts")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x", which="both")

    plt.tight_layout()
    out = FIG_DIR / "r_ns_plane.png"
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
