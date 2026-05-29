"""Study 07 figures:

  fig_desi_y1_distance_ladder  D_M/r_d, D_H/r_d, D_V/r_d versus z
                               with theory curves for each cosmology
                               and DESI Y1 data points with error bars.
  fig_desi_y1_residuals        per-tracer (theory - data)/sigma residuals
                               for PRIMARY vs CLOSURE-POOL vs Planck.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from desi_y1_data import DESI_Y1, DMDH, DV  # noqa: E402
from esd_bao import (  # noqa: E402
    D_H,
    D_M,
    D_V,
    cosmo_esd_closure_pool,
    cosmo_esd_primary,
    cosmo_planck_lcdm,
    r_d_aubourg2015,
)

FIG_DIR = os.path.abspath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG_DIR, exist_ok=True)

COSMOLOGIES = [
    ("ESD PRIMARY",       cosmo_esd_primary(67.36),       "C0", "-"),
    ("ESD CLOSURE-POOL",  cosmo_esd_closure_pool(67.36),  "C1", "--"),
    ("Planck-LCDM",       cosmo_planck_lcdm(67.36),       "k",  ":"),
]


def fig_distance_ladder() -> None:
    z_grid = np.geomspace(0.05, 3.0, 200)
    fig, axes = plt.subplots(3, 1, figsize=(7.5, 8.0), sharex=True)

    for label, c, color, ls in COSMOLOGIES:
        rd = r_d_aubourg2015(c)
        dm = [D_M(c, z) / rd for z in z_grid]
        dh = [D_H(c, z) / rd for z in z_grid]
        dv = [D_V(c, z) / rd for z in z_grid]
        axes[0].plot(z_grid, dm, color=color, ls=ls, lw=1.5, label=label)
        axes[1].plot(z_grid, dh, color=color, ls=ls, lw=1.5, label=label)
        axes[2].plot(z_grid, dv, color=color, ls=ls, lw=1.5, label=label)

    # data
    for t in DESI_Y1:
        if isinstance(t, DV):
            axes[2].errorbar(t.z_eff, t.DV_rd, yerr=t.sigma,
                             fmt="s", color="C3", ms=6, capsize=3, zorder=5,
                             label="DESI Y1" if t.name == "BGS" else None)
        else:
            axes[0].errorbar(t.z_eff, t.DM_rd, yerr=t.DM_sig,
                             fmt="o", color="C3", ms=6, capsize=3, zorder=5,
                             label="DESI Y1" if t.name == "LRG1" else None)
            axes[1].errorbar(t.z_eff, t.DH_rd, yerr=t.DH_sig,
                             fmt="o", color="C3", ms=6, capsize=3, zorder=5,
                             label="DESI Y1" if t.name == "LRG1" else None)

    axes[0].set_ylabel(r"$D_M / r_d$")
    axes[1].set_ylabel(r"$D_H / r_d$")
    axes[2].set_ylabel(r"$D_V / r_d$")
    axes[2].set_xlabel("redshift  $z$")
    for ax in axes:
        ax.set_xscale("log")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)
    axes[0].set_title("Study 07: DESI Y1 BAO vs framework predictions")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_desi_y1_distance_ladder.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


def fig_residuals() -> None:
    rows = []
    for label, c, color, _ in COSMOLOGIES:
        rd = r_d_aubourg2015(c)
        for t in DESI_Y1:
            if isinstance(t, DV):
                th = D_V(c, t.z_eff) / rd
                rows.append((label, color, f"{t.name} ($D_V$)", t.z_eff,
                             (th - t.DV_rd) / t.sigma))
            else:
                th_M = D_M(c, t.z_eff) / rd
                th_H = D_H(c, t.z_eff) / rd
                rows.append((label, color, f"{t.name} ($D_M$)", t.z_eff,
                             (th_M - t.DM_rd) / t.DM_sig))
                rows.append((label, color, f"{t.name} ($D_H$)", t.z_eff,
                             (th_H - t.DH_rd) / t.DH_sig))

    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    # Distinct point label order: tracer/observable order from DESI_Y1
    labels = []
    for t in DESI_Y1:
        if isinstance(t, DV):
            labels.append(f"{t.name} ($D_V$)")
        else:
            labels.append(f"{t.name} ($D_M$)")
            labels.append(f"{t.name} ($D_H$)")
    x = np.arange(len(labels))
    offsets = {"ESD PRIMARY": -0.22, "ESD CLOSURE-POOL": 0.0, "Planck-LCDM": +0.22}
    markers = {"ESD PRIMARY": "o", "ESD CLOSURE-POOL": "s", "Planck-LCDM": "x"}
    for cosmo_label, color, point_label, _z, residual in rows:
        i = labels.index(point_label)
        ax.scatter(x[i] + offsets[cosmo_label], residual,
                   color=color, marker=markers[cosmo_label], s=42,
                   edgecolor="0.2", lw=0.5,
                   label=cosmo_label if i == 0 else None)
    ax.axhline(0,  color="0.4", lw=0.8)
    ax.axhline(+1, color="0.6", lw=0.5, ls=":")
    ax.axhline(-1, color="0.6", lw=0.5, ls=":")
    ax.axhline(+2, color="0.6", lw=0.5, ls="--")
    ax.axhline(-2, color="0.6", lw=0.5, ls="--")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("residual / 1$\\sigma$")
    ax.set_title("Study 07: per-tracer residuals across cosmologies (H$_0$=67.36)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_desi_y1_residuals.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


if __name__ == "__main__":
    fig_distance_ladder()
    fig_residuals()
