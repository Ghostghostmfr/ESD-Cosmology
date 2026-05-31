"""Figures for Study 36: HMF lift and cluster-cosmology S_8 panel."""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cluster_data import (
    CLUSTER_COSMOLOGY, SIGMA_8_LOCKED, S_8_LOCKED,
    PLANCK_S_8, PLANCK_S_8_SIG, OMEGA_M0_LOCKED,
)
from esd_cluster_hmf import hmf_lift_factor, G_eff_over_G_N, delta_c_esd, kernel_R
from esd_cluster_hmf import channel_weights
from cluster_data import u_vir_cluster, CLUSTER_PROBE_SCALES

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.0))

    # --- Panel 1: HMF lift vs cluster mass ---
    M_grid = np.logspace(13, 15.3, 50)
    R_typical = lambda M: 1.0 * (M / 2e14) ** (1.0 / 3.0)
    lifts = [hmf_lift_factor(M, R_typical(M)) for M in M_grid]
    geffs = [G_eff_over_G_N(u_vir_cluster(M, R_typical(M))) for M in M_grid]

    ax = axes[0]
    ax.semilogx(M_grid, lifts, color="C0", lw=2,
                label=r"$n_\mathrm{ESD}/n_{\Lambda\mathrm{CDM}}$ (HMF lift)")
    ax.semilogx(M_grid, geffs, color="C3", lw=1.5, ls="--",
                label=r"$G_\mathrm{eff}/G_N$ (conformal enhancement)")
    ax.axhline(1.0, color="gray", lw=1, alpha=0.5)
    for label, M, R in CLUSTER_PROBE_SCALES:
        ax.axvline(M, color="gray", lw=0.5, alpha=0.3)
    ax.set_xlabel(r"halo mass $M_{200}$ [$M_\odot$]")
    ax.set_ylabel("ESD / $\\Lambda$CDM ratio")
    ax.set_title(r"Panel A — ESD HMF lift and $G_\mathrm{eff}/G_N$")
    ax.set_ylim(0.95, 1.5)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # --- Panel 2: cluster-cosmology S_8 ---
    ax = axes[1]
    surveys = [entry[0] for entry in CLUSTER_COSMOLOGY]
    S8s     = [entry[7] for entry in CLUSTER_COSMOLOGY]
    sigs    = [0.5 * (entry[8] + entry[9]) for entry in CLUSTER_COSMOLOGY]
    y = np.arange(len(surveys))
    ax.errorbar(S8s, y, xerr=sigs, fmt="o", capsize=4, ms=7, color="C0",
                label="cluster cosmology surveys")
    ax.axvline(S_8_LOCKED, color="black", lw=2,
               label=r"ESD-locked $S_8 = 0.832$")
    ax.axvline(PLANCK_S_8, color="C3", lw=1.5, ls="--",
               label=r"Planck CMB $S_8 = 0.832$")
    ax.axvspan(PLANCK_S_8 - PLANCK_S_8_SIG, PLANCK_S_8 + PLANCK_S_8_SIG,
               color="C3", alpha=0.15)
    ax.set_yticks(y)
    ax.set_yticklabels(surveys, fontsize=9)
    ax.set_xlabel(r"$S_8 = \sigma_8\sqrt{\Omega_m/0.3}$")
    ax.set_title(r"Panel B — Cluster-cosmology $S_8$ vs Planck CMB")
    ax.legend(loc="lower left", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    ax.set_xlim(0.72, 0.92)

    plt.tight_layout()
    out = FIG_DIR / "cluster_hmf_S8.png"
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
