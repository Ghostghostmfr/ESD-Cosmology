"""Study 09 figures."""
from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_gw as G   # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(_HERE), "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), dpi=160,
                bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"),
                bbox_inches="tight")
    plt.close(fig)


def fig_cgamma_vs_z():
    """c_gamma^2(z) saturated against the photon barrier at z = z_LSS."""
    eps0 = G.EPS0_PAPER_BOUND
    eps2 = G.eps2_max_from_barrier(eps0)
    z = np.logspace(0, np.log10(G.Z_LSS * 1.05), 600)
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.semilogx(1 + z, G.c_gamma_sq(z, eps0, eps2),
                color="tab:blue",
                label=f"saturated: eps0={eps0:.1e}, eps2={eps2:.2e}")
    ax.semilogx(1 + z, G.c_gamma_sq(z, eps0, 0.0),
                color="tab:gray", ls="--",
                label="eps2 = 0 (GW-only bound)")
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(1 + G.Z_LSS, color="red", ls=":",
               label=f"z_LSS = {G.Z_LSS:.0f}")
    ax.set_xlabel("1 + z")
    ax.set_ylabel("$c_\\gamma^2(z) \\,/\\, c^2$")
    ax.set_title("Disformal photon dispersion saturated at the photon barrier")
    ax.legend(loc="lower left", fontsize=9)
    _save(fig, "fig_cgamma_vs_z")


def fig_delta_H0_vs_eps2():
    """Delta H_0 contribution as eps_2 sweeps up to its barrier cap."""
    eps0 = G.EPS0_PAPER_BOUND
    eps2_max = G.eps2_max_from_barrier(eps0)
    grid = np.linspace(0.0, eps2_max, 25)
    dH0 = []
    for e2 in grid:
        dH0.append(G.delta_H0_from_dispersion(eps0=eps0, eps2=e2)["delta_H0"])
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.plot(grid / eps2_max, dH0, color="tab:blue", marker="o", ms=4)
    ax.axhline(G.DELTA_H0_PAPER, color="red", ls="--",
               label=f"paper cap = {G.DELTA_H0_PAPER:.2f} km/s/Mpc")
    ax.set_xlabel("eps_2 / eps_2_max")
    ax.set_ylabel("$\\Delta H_0$  [km / s / Mpc]")
    ax.set_title("Disformal channel contribution to $H_0$ shift")
    ax.legend()
    _save(fig, "fig_delta_H0_vs_eps2")


def main():
    fig_cgamma_vs_z()
    fig_delta_H0_vs_eps2()
    print(f"[gw] figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()
