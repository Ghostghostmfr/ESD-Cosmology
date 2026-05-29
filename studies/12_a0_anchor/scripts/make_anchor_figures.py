"""Study 12 figures."""
from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_anchor as A           # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(_HERE), "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), dpi=160,
                bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"),
                bbox_inches="tight")
    plt.close(fig)


def fig_bridge_curve():
    """a_0 vs H_0 along the locked bridge, with anchors highlighted."""
    H = np.linspace(60, 80, 200)
    a0 = np.array([A.a_zero(h) for h in H])
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(H, a0 * 1e10, color="tab:blue", lw=2,
            label="$a_0 = c H_0\\sqrt{(3\\Omega_{DM}+\\Omega_b)/(8\\pi)}$")
    ax.axhline(A.A0_MCGAUGH_MS2 * 1e10, color="tab:green", ls="--",
               label=f"McGaugh+2016 anchor: $a_0={A.A0_MCGAUGH_MS2*1e10:.2f}\\times 10^{{-10}}$ m/s$^2$")
    ax.axvspan(A.H0_PLANCK_KMS - 0.5, A.H0_PLANCK_KMS + 0.5,
               color="tab:blue", alpha=0.18, label=f"Planck: $H_0={A.H0_PLANCK_KMS}$")
    ax.axvspan(A.H0_SH0ES_KMS - 1.0, A.H0_SH0ES_KMS + 1.0,
               color="tab:red", alpha=0.18, label=f"SH0ES: $H_0={A.H0_SH0ES_KMS}$")
    ax.scatter([A.H0_PLANCK_KMS], [A.a_zero(A.H0_PLANCK_KMS)*1e10],
               s=80, color="tab:blue", zorder=5)
    ax.scatter([A.H0_SH0ES_KMS], [A.a_zero(A.H0_SH0ES_KMS)*1e10],
               s=80, color="tab:red", zorder=5)
    ax.set_xlabel("$H_0$  (km/s/Mpc)")
    ax.set_ylabel("$a_0$  ($10^{-10}$ m/s$^2$)")
    ax.set_title("Closure-pool bridge $a_0(H_0)$ and the Hubble tension")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, alpha=0.3)
    _save(fig, "fig_bridge_a0_vs_H0")


def fig_cross_study():
    """Bar chart of a_0 values across studies + McGaugh anchor."""
    labels = [
        "esd_core\n(Planck mode)",
        "esd_core\n(SH0ES mode)",
        "McGaugh+2016\nRAR fit",
    ]
    values = [
        A.a_zero(A.H0_PLANCK_KMS),
        A.a_zero(A.H0_SH0ES_KMS),
        A.A0_MCGAUGH_MS2,
    ]
    colors = ["tab:blue", "tab:red", "tab:green"]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    bars = ax.bar(labels, np.array(values)*1e10, color=colors,
                   edgecolor="k", alpha=0.85)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width()/2, v*1e10 + 0.01,
                f"{v*1e10:.3f}", ha="center", va="bottom", fontsize=10)
    ax.set_ylabel("$a_0$  ($10^{-10}$ m/s$^2$)")
    ax.axhline(A.A0_MCGAUGH_MS2 * 1e10, color="tab:green", ls=":",
               alpha=0.6)
    ax.set_title("Cross-study $a_0$ values: Planck mode matches RAR to 0.12%")
    ax.set_ylim(1.1, 1.4)
    ax.grid(True, axis="y", alpha=0.3)
    _save(fig, "fig_cross_study_a0")


def fig_h_blindness():
    """Show a_0 vs h at fixed omega-densities: horizontal line."""
    h_grid = np.linspace(0.55, 0.80, 30)
    a0_omega = np.array([A.a0_h_blindness(h0=h)["a0"] for h in h_grid])
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(h_grid, a0_omega * 1e10, "o-", color="tab:blue",
            label="$a_0(h\\,|\\,\\omega_i\\,\\text{fixed})$  (omega-form)")
    ax.axhline(A.A0_MCGAUGH_MS2 * 1e10, color="tab:green", ls="--",
               label=f"McGaugh $a_0 = {A.A0_MCGAUGH_MS2*1e10:.2f}\\times 10^{{-10}}$ m/s$^2$")
    ax.set_xlabel("$h$")
    ax.set_ylabel("$a_0$  ($10^{-10}$ m/s$^2$)")
    ax.set_title("h-blindness of $a_0$ in physical-density (omega) variables")
    ax.set_ylim(1.15, 1.25)
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, alpha=0.3)
    _save(fig, "fig_a0_h_blindness")


def main():
    fig_bridge_curve()
    fig_cross_study()
    fig_h_blindness()
    print(f"[a0-anchor] figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()
