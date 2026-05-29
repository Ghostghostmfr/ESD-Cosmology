"""Study 11 figures."""
from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_jeans as J            # noqa: E402
import observations as OBS       # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(_HERE), "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), dpi=160,
                bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"),
                bbox_inches="tight")
    plt.close(fig)


def fig_lambda_vs_m22():
    m22 = np.logspace(-1, 2, 200)
    lam = np.array([J.lambda_J_kpc(comoving=True, m_D_eV=1e-22 * m)
                    for m in m22])
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.loglog(m22, lam, color="tab:blue", lw=2,
              label="HBG quantum Jeans (this study)")
    ax.axhline(J.LAMBDA_J_PAPER, color="tab:red", ls="--",
               label=f"paper $\\lambda_J = {J.LAMBDA_J_PAPER:.0f}$ kpc")
    ax.scatter([1.0], [J.lambda_J_kpc(comoving=True)], s=80,
               color="tab:green", zorder=5,
               label=f"$m_{{22}}=1$ fiducial: {J.lambda_J_kpc(comoving=True):.1f} kpc")
    ax.set_xlabel("$m_D / 10^{-22}\\,\\mathrm{eV}$")
    ax.set_ylabel("$\\lambda_J$ (comoving, kpc, z=3)")
    ax.set_title("ESD child C7: Jeans cutoff vs ultralight scalar mass")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    _save(fig, "fig_lambda_vs_m22")


def fig_k_cut_vs_lya():
    m22 = np.logspace(-1, 2, 200)
    k_cut = np.array([J.k_cut_comoving_mpc_inv(m_D_eV=1e-22 * m) for m in m22])
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.loglog(m22, k_cut, color="tab:blue", lw=2,
              label="ESD C7 cutoff $k_J(m_D)$")
    for s in OBS.SAMPLES:
        ax.axhline(s.k_max_Mpc, ls=":", alpha=0.7,
                   label=f"{s.name.split('(')[0].strip()}: $k_{{\\max}}={s.k_max_Mpc:.1f}$ Mpc$^{{-1}}$")
        ax.axvline(s.m22_bound, ls="-.", color="tab:gray", alpha=0.4)
    ax.scatter([1.0], [J.k_cut_comoving_mpc_inv()],
               s=80, color="tab:green", zorder=5,
               label=f"$m_{{22}}=1$: $k={J.k_cut_comoving_mpc_inv():.1f}$ Mpc$^{{-1}}$")
    ax.set_xlabel("$m_D / 10^{-22}\\,\\mathrm{eV}$")
    ax.set_ylabel("$k_J$ (comoving, Mpc$^{-1}$, z=3)")
    ax.set_title("Lyman-$\\alpha$ probe range vs framework cutoff")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, which="both", alpha=0.3)
    _save(fig, "fig_k_cut_vs_lya")


def fig_h_blindness():
    """Show lambda_J vs h at fixed omega_m_h2 -- horizontal line."""
    h_grid = np.linspace(0.55, 0.80, 30)
    lam    = np.array([J.lambda_J_kpc(comoving=True) for _ in h_grid])
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(h_grid, lam, "o-", color="tab:blue",
            label="$\\lambda_J(h\\,|\\, \\omega_m\\,\\text{fixed})$")
    ax.axhline(J.LAMBDA_J_PAPER, ls="--", color="tab:red",
               label="paper $\\lambda_J = 94$ kpc")
    ax.set_xlabel("$h$")
    ax.set_ylabel("$\\lambda_J$ (comoving, kpc)")
    ax.set_title("h-blindness of C7 (Theorem 1)")
    ax.set_ylim(0, 110)
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, alpha=0.3)
    _save(fig, "fig_h_blindness")


def main():
    fig_lambda_vs_m22()
    fig_k_cut_vs_lya()
    fig_h_blindness()
    print(f"[lya-jeans] figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()
