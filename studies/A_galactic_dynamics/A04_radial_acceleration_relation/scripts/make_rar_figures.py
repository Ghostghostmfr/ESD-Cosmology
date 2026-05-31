"""RAR figures - study 05.

Generates (under figures_generated/):
  fig_rar           top: g_obs vs g_bar density with ESD/MOND/Newton curves
                     bottom: running median + 16/84 band of log(g_obs/g_model)
  fig_rar_residual  zoomed residual band only (useful as a thumbnail)
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from esd_rar import (  # noqa: E402
    A0_SI, g_esd_vec, g_mond_vec,
)

NPZ_PATH = os.path.join(HERE, "outputs", "rar_points.npz")
FIG_DIR = os.path.abspath(os.path.join(HERE, "..", "figures_generated"))
os.makedirs(FIG_DIR, exist_ok=True)


def _running_band(x: np.ndarray, y: np.ndarray, n_bins: int = 28):
    order = np.argsort(x)
    xs, ys = x[order], y[order]
    bins = np.array_split(np.arange(xs.size), n_bins)
    xc = np.array([xs[b].mean()         for b in bins if b.size])
    med = np.array([np.median(ys[b])    for b in bins if b.size])
    p16 = np.array([np.percentile(ys[b], 16) for b in bins if b.size])
    p84 = np.array([np.percentile(ys[b], 84) for b in bins if b.size])
    return xc, med, p16, p84


def main() -> int:
    if not os.path.exists(NPZ_PATH):
        print(f"[fig] missing {NPZ_PATH}. Run scripts/run_rar.py first.",
              file=sys.stderr)
        return 1

    d = np.load(NPZ_PATH)
    gbar = d["gbar"]; gobs = d["gobs"]
    delta_esd = d["delta_esd"]; delta_mond = d["delta_mond"]

    # Smooth model curves on a dense g_bar grid.
    g_axis = np.logspace(np.log10(gbar.min() * 0.9),
                         np.log10(gbar.max() * 1.1), 400)
    g_esd_curve  = g_esd_vec(g_axis)
    g_mond_curve = g_mond_vec(g_axis)

    # --- fig_rar (2-panel) ---------------------------------------------------
    fig, (axA, axB) = plt.subplots(
        2, 1, figsize=(7.5, 8.5), sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.0], "hspace": 0.07},
        constrained_layout=False,
    )

    # Top: g_obs vs g_bar
    axA.hexbin(np.log10(gbar), np.log10(gobs), gridsize=70,
               cmap="Greys", bins="log", mincnt=1)
    axA.plot(np.log10(g_axis), np.log10(g_esd_curve), color="C3", lw=2.2,
             label="ESD (locked, zero free parameters)")
    axA.plot(np.log10(g_axis), np.log10(g_mond_curve), color="C0", lw=2.0, ls="--",
             label=r"MOND simple $\nu(x)=1/(1-e^{-\sqrt{x}})$")
    diag = np.linspace(min(np.log10(g_axis)), max(np.log10(g_axis)), 50)
    axA.plot(diag, diag, color="0.4", lw=1.0, ls=":",
             label=r"Newtonian $g_{\rm obs}=g_{\rm bar}$")
    axA.axvline(np.log10(A0_SI), color="0.6", lw=0.8, alpha=0.7)
    axA.text(np.log10(A0_SI), axA.get_ylim()[1] - 0.4, r" $a_0$",
             color="0.4", fontsize=9, va="top")
    axA.set_ylabel(r"$\log_{10}\,g_{\rm obs}$  [m s$^{-2}$]")
    axA.set_title("Study 05: SPARC Radial Acceleration Relation "
                  "(175 galaxies, fixed M/L)")
    axA.legend(loc="upper left", fontsize=9, framealpha=0.95)
    axA.grid(True, alpha=0.3)

    # Bottom: residual bands
    x_e, med_e, p16e, p84e = _running_band(np.log10(gbar), delta_esd)
    x_m, med_m, p16m, p84m = _running_band(np.log10(gbar), delta_mond)
    axB.fill_between(x_e, p16e, p84e, color="C3", alpha=0.20)
    axB.plot(x_e, med_e, color="C3", lw=2.0,
             label=r"ESD median $\pm$ 16/84")
    axB.fill_between(x_m, p16m, p84m, color="C0", alpha=0.15)
    axB.plot(x_m, med_m, color="C0", lw=2.0, ls="--",
             label="MOND median $\\pm$ 16/84")
    axB.axhline(0.0, color="0.3", lw=0.8)
    axB.set_xlabel(r"$\log_{10}\,g_{\rm bar}$  [m s$^{-2}$]")
    axB.set_ylabel(r"$\log_{10}(g_{\rm obs}/g_{\rm model})$ [dex]")
    axB.set_ylim(-0.55, 0.55)
    axB.legend(loc="upper right", fontsize=9, framealpha=0.95)
    axB.grid(True, alpha=0.3)

    fig.subplots_adjust(left=0.10, right=0.97, top=0.94, bottom=0.08)
    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_rar.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)

    # --- fig_rar_residual (single band, thumbnail) ---------------------------
    fig2, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.fill_between(x_e, p16e, p84e, color="C3", alpha=0.20)
    ax.plot(x_e, med_e, color="C3", lw=2.0, label="ESD")
    ax.fill_between(x_m, p16m, p84m, color="C0", alpha=0.15)
    ax.plot(x_m, med_m, color="C0", lw=2.0, ls="--", label="MOND")
    ax.axhline(0.0, color="0.3", lw=0.8)
    ax.set_xlabel(r"$\log_{10}\,g_{\rm bar}$  [m s$^{-2}$]")
    ax.set_ylabel(r"$\log_{10}(g_{\rm obs}/g_{\rm model})$ [dex]")
    ax.set_title("Study 05: RAR log-residuals "
                 "(median + 16/84 percentile band)")
    ax.set_ylim(-0.55, 0.55)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig2.tight_layout()
    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_rar_residual.{ext}")
        fig2.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
