"""Study 33 figures: PPN safety margins and kernel deep-UV behaviour."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from esd_ppn import (
    kernel_R, channel_weights, gamma_minus_1_esd, beta_minus_1_esd,
    u_from_g,
)
from ppn_data import (
    G_EARTH_SURFACE_SI, G_EARTH_ORBIT_SI, G_CASSINI_SI,
    G_NEWTON_SI, M_SUN_KG, R_MERCURY_ORBIT_M,
    GAMMA_MINUS_1_CASSINI, GAMMA_MINUS_1_CASSINI_SIGMA,
    BETA_MINUS_1_LLR, BETA_MINUS_1_LLR_SIGMA,
)

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def fig_kernel_deep_uv():
    u_grid = np.logspace(-6, 14, 400)
    R_arr  = np.array([kernel_R(u) for u in u_grid])
    g_arr  = np.array([gamma_minus_1_esd(u) for u in u_grid])
    b_arr  = np.array([beta_minus_1_esd(u)  for u in u_grid])

    u_pts = {
        "earth surface":   u_from_g(G_EARTH_SURFACE_SI),
        "Earth orbit":     u_from_g(G_EARTH_ORBIT_SI),
        "Mercury orbit":   u_from_g(G_NEWTON_SI * M_SUN_KG / R_MERCURY_ORBIT_M ** 2),
        "Cassini closest": u_from_g(G_CASSINI_SI),
    }

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.loglog(u_grid, np.abs(g_arr), "C0-", lw=1.8, label=r"|$\gamma - 1$| (ESD)")
    ax.loglog(u_grid, np.abs(b_arr), "C2--", lw=1.8, label=r"|$\beta  - 1$| (ESD)")

    # Cassini bound
    ax.axhline(GAMMA_MINUS_1_CASSINI + 2 * GAMMA_MINUS_1_CASSINI_SIGMA,
               color="C3", ls=":", lw=1.4,
               label=r"Cassini 2$\sigma$ bound  |$\gamma-1$|")
    ax.axhline(BETA_MINUS_1_LLR + 2 * BETA_MINUS_1_LLR_SIGMA,
               color="0.4", ls=":", lw=1.4,
               label=r"LLR 2$\sigma$ bound  |$\beta-1$|")

    for label, u in u_pts.items():
        ax.axvline(u, color="0.7", lw=0.6)
        ax.text(u, 1e-30, label, rotation=90, va="bottom",
                ha="right", fontsize=8, color="0.4")

    ax.set_xlabel(r"$u = 4g/a_0$")
    ax.set_ylabel("PPN deviation magnitude")
    ax.set_title("Study 33 - ESD PPN deviations vs Solar-system bounds")
    ax.set_ylim(1e-32, 1e2)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "ppn_kernel_deep_uv.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


def fig_safety_bars():
    from esd_ppn import summary as esd_summary
    s = esd_summary()
    cas = s["cassini_closest"]
    mercury = s["mercury_orbit"]
    earth = s["earth_orbit"]

    labels    = [r"|$\gamma - 1$|", r"|$\beta - 1$|", r"|$\eta_N$|", r"|$\dot G / G$|"]
    predicted = [cas["gamma_minus_1"], mercury["beta_minus_1"],
                 abs(earth["eta_nordtvedt"]), s["gdot_over_g_per_yr"]]
    bounds    = [GAMMA_MINUS_1_CASSINI + 2 * GAMMA_MINUS_1_CASSINI_SIGMA,
                 BETA_MINUS_1_LLR + 2 * BETA_MINUS_1_LLR_SIGMA,
                 7.0e-4 + 2.0 * 7.0e-4,
                 1.0e-13]

    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.bar(x - w/2, predicted, w, color="C2", label="ESD prediction")
    ax.bar(x + w/2, bounds,    w, color="C3", alpha=0.7, label=r"Anchor 2$\sigma$ bound")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("magnitude (log)")
    ax.set_title("Study 33 - ESD PPN safety margins")
    ax.legend(loc="lower left", fontsize=9)
    for xi, v in zip(x, predicted):
        ax.text(xi - w/2, v * 1.4, f"{v:.1e}", ha="center", fontsize=7,
                rotation=90, color="C2")
    for xi, v in zip(x, bounds):
        ax.text(xi + w/2, v * 1.4, f"{v:.1e}", ha="center", fontsize=7,
                rotation=90, color="C3")
    fig.tight_layout()
    out = FIG_DIR / "ppn_safety_bars.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    fig_kernel_deep_uv()
    fig_safety_bars()
