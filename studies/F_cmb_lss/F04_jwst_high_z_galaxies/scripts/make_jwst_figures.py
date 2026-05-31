"""Study 13 figures: JWST high-z baryon budget tension."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_jwst as J
import observations as O

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name + ".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_epsilon_vs_rho():
    rho = np.logspace(5.5, 7.5, 60)
    eps = [J.epsilon_star_min(r) for r in rho]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.loglog(rho, eps, "k-", lw=1.8, label=r"$\varepsilon_\star = \rho_\star / (\rho_b f_{coll})$")
    ax.axhline(0.20, color="C2", ls=":", label="universal SFE upper limit (BK23)")
    ax.axhline(1.00, color="C3", ls="--", label=r"$\varepsilon_\star = 1$ (impossible)")
    for s in O.SAMPLES:
        e = J.epsilon_star_min(s.rho_star)
        ax.errorbar(s.rho_star, e,
                    xerr=s.rho_err, fmt="o", capsize=3, label=s.label)
    ax.set_xlabel(r"$\rho_\star$ [M$_\odot$/Mpc$^3$]")
    ax.set_ylabel(r"$\varepsilon_\star$")
    ax.set_title("JWST high-z cosmic star-formation efficiency (BK23)")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_eps_vs_rho")


def fig_eps_vs_z():
    zs = np.linspace(4.0, 14.0, 40)
    out = J.epsilon_vs_z_curve(zs)
    z_arr   = [r[0] for r in out]
    eps_arr = [r[2] for r in out]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.semilogy(z_arr, eps_arr, "k-", lw=1.8, label=r"$\varepsilon_\star(z)$ for $\rho_\star=$ Labbé")
    ax.axhline(0.20, color="C2", ls=":", label="universal SFE upper limit")
    ax.axhline(1.00, color="C3", ls="--", label=r"$\varepsilon_\star=1$ floor")
    ax.set_xlabel(r"$z$")
    ax.set_ylabel(r"$\varepsilon_{\star,\min}(z)$")
    ax.set_title("ε*_min vs z with toy f_collapse(z) (BK23 normalization)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_eps_vs_z")


def fig_h_blindness():
    h_arr = np.linspace(0.55, 0.85, 41)
    rho_b_omega_form = [J.OMEGA_B_LOCK * J.H_FID**2 * (J.MPC_M**3 / J.M_SUN_KG)
                         * 3 * J.H100_SI**2 / (8 * np.pi * J.G_NEWTON) for _ in h_arr]
    rho_b_omega_form = np.array(rho_b_omega_form)
    rho_b_lock = np.array([J.rho_baryon_0(h=h) for h in h_arr])
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(h_arr, rho_b_omega_form, "k-", lw=2.0, label=r"$\omega_b$-form (h-blind)")
    ax.plot(h_arr, rho_b_lock,      "C1--", lw=1.6, label=r"$\Omega_b$-form (h$^2$ scaling)")
    ax.axvline(J.H_FID, color="C0", ls=":", alpha=0.5)
    ax.set_xlabel(r"$h$")
    ax.set_ylabel(r"$\rho_{b,0}$ [M$_\odot$/Mpc$^3$]")
    ax.set_title(r"h-blindness of $\rho_{b,0}$ in $\omega_b$ variables (Thm 1, C1)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    _save(fig, "fig_h_blindness")


if __name__ == "__main__":
    fig_epsilon_vs_rho()
    fig_eps_vs_z()
    fig_h_blindness()
    print(f"[jwst-highz] figures written to {FIG}")
