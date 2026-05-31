"""Study 08 figures.

  fig_anchor_distribution -- H_0 number-line by anchor family
  fig_channel_budget      -- log-scale bar of max |Delta H_0| per channel vs gap
  fig_h0_vs_h_blindness   -- relative dR_i/dh per ESD-distinctive child
"""
from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import anchors as A           # noqa: E402
import channels as CH         # noqa: E402
import esd_h0 as H            # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(_HERE), "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)

FAM_COLOR = {
    "cmb":      "tab:blue",
    "bao_bbn":  "tab:cyan",
    "trgb":     "tab:olive",
    "lensing":  "tab:purple",
    "masers":   "tab:brown",
    "gw":       "tab:gray",
    "distance": "tab:red",
}


def _save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), dpi=160,
                bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"),
                bbox_inches="tight")
    plt.close(fig)


def fig_anchor_distribution():
    H0_esd = H.bridge_inversion_H0()
    H0_paper = 67.28
    n = len(A.ANCHORS)
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    for i, a in enumerate(A.ANCHORS):
        c = FAM_COLOR.get(a.family, "k")
        ax.errorbar(a.H0, n - i, xerr=a.sigma, fmt="o",
                    color=c, capsize=3, ms=6)
        ax.text(a.H0 + a.sigma + 0.2, n - i, a.name,
                fontsize=8, va="center")
    ax.axvspan(H0_esd - 0.05, H0_esd + 0.05, color="green", alpha=0.25,
               label=f"ESD bridge prediction = {H0_esd:.2f} km/s/Mpc")
    ax.axvline(H0_paper, color="green", lw=0.8, ls=":",
               label=f"hubble paper quote = {H0_paper:.2f}")
    ax.set_xlim(60, 80)
    ax.set_ylim(0, n + 1)
    ax.set_yticks([])
    ax.set_xlabel("$H_0$  [km / s / Mpc]")
    ax.set_title("Multi-anchor $H_0$ vs ESD bridge prediction")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, "fig_anchor_distribution")


def fig_channel_budget():
    names = [f"C{c.idx}" for c in CH.CHANNELS]
    caps  = [c.deltaH0_max if np.isfinite(c.deltaH0_max) else 10.0
             for c in CH.CHANNELS]  # show 'ruled out' as 10 km/s/Mpc top
    caps_for_log = [max(v, 1e-13) for v in caps]
    colors = ["tab:blue" if c.status == "active" else
              ("tab:gray" if c.status == "structurally absent" else "tab:red")
              for c in CH.CHANNELS]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(names, caps_for_log, color=colors)
    ax.set_yscale("log")
    ax.axhline(CH.SHOES_GAP_KM_S_MPC, color="red", ls="--",
               label=f"SH0ES gap = {CH.SHOES_GAP_KM_S_MPC:.2f} km/s/Mpc")
    ax.axhline(CH.combined_budget(), color="green", ls=":",
               label=f"combined ESD budget = {CH.combined_budget():.2f}")
    ax.set_ylabel("max $|\\Delta H_0|$  [km / s / Mpc]")
    ax.set_title("ESD 6-channel drift budget vs SH0ES gap "
                 f"(shortfall {CH.budget_vs_gap_ratio():.0f}x)")
    ax.legend(loc="upper right", fontsize=9)
    _save(fig, "fig_channel_budget")


def fig_h_blindness():
    """Bar plot of |dR_i/dh|/|R_i| for ESD-distinctive vs non-distinctive."""
    J_dist = H.numerical_jacobian(
        children=(H.child_C1, H.child_C4, H.child_C7))
    J_nond = H.numerical_jacobian(children=(H.child_C2,))
    names = ["C1 bridge", "C4 cluster", "C7 Lya Jeans", "C2 theta_*"]
    vals  = list(np.abs(J_dist[:, 0])) + list(np.abs(J_nond[:, 0]))
    colors = ["tab:blue", "tab:blue", "tab:blue", "tab:red"]
    floor = 1e-18
    vals_plot = [max(v, floor) for v in vals]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.bar(names, vals_plot, color=colors)
    ax.set_yscale("log")
    ax.axhline(1e-9, color="k", ls="--",
               label="Thm 1 gate $|\\partial R_i / \\partial h| < 10^{-9}$")
    ax.set_ylabel("$|\\partial R_i / \\partial h| \\,/\\, |R_i|$")
    ax.set_title("h-blindness theorem (ESD-distinctive children, blue)")
    ax.legend(fontsize=9)
    _save(fig, "fig_h_blindness")


def main():
    fig_anchor_distribution()
    fig_channel_budget()
    fig_h_blindness()
    print(f"[hubble] figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()
