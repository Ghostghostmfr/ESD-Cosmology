"""Study 10 figures."""
from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_cluster as C            # noqa: E402
import observations as OBS         # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(_HERE), "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), dpi=160,
                bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"),
                bbox_inches="tight")
    plt.close(fig)


def fig_R_vs_u():
    """Locked R(u) = s/Sigma(u) over five decades in u."""
    u = np.logspace(-2, 4, 400)
    R = C.R_of_u(u)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.loglog(u, R, color="tab:blue", lw=2,
              label="$R(u) = s/\\Sigma(u)$")
    ax.axhline(C.DM_OVER_B, color="tab:red", ls="--",
               label=f"$\\Omega_{{DM}}/\\Omega_b = {C.DM_OVER_B:.2f}$")
    ax.axvspan(0.5, 3.0, color="gold", alpha=0.18,
               label="typical cluster $u_{cl}$")
    ax.set_xlabel("$u = 4 g_N / a_0$")
    ax.set_ylabel("$R(u)$  (screening response)")
    ax.set_title("Locked ESD screening response $R(u)$")
    ax.legend(loc="lower left", fontsize=9)
    _save(fig, "fig_R_vs_u")


def fig_fb_predictions():
    """Cluster f_b predictions vs published measurements."""
    fig, ax = plt.subplots(figsize=(8.2, 5.0))

    # Theory curve: f_b(u) for u in cluster range
    u = np.logspace(-1.5, 2.5, 200)
    fb_theory = 1.0 / ((1.0 + C.R_of_u(u)) + C.DM_OVER_B)
    ax.semilogx(u, fb_theory, color="tab:blue", lw=2,
                label="ESD C4 prediction")

    ax.axhline(C.OMEGA_B_LOCK / (C.OMEGA_B_LOCK + C.OMEGA_DM_LOCK),
               color="tab:red", ls="--",
               label=f"cosmic $f_b = {C.OMEGA_B_LOCK / (C.OMEGA_B_LOCK + C.OMEGA_DM_LOCK):.4f}$")

    color_map = {"R_500c": "tab:green", "R_200c": "tab:orange"}
    for s in OBS.SAMPLES:
        if s.radius_def == "R_inf":
            continue
        u_s = C.u_cluster(s.M_500_solar, s.R_def_mpc)
        c   = color_map.get(s.radius_def, "k")
        ax.errorbar(u_s, s.f_b, yerr=s.sigma, fmt="o",
                    color=c, capsize=3, ms=8)
        ax.text(u_s, s.f_b - s.sigma - 0.0035, s.name.split("(")[0].strip(),
                fontsize=7, ha="center", va="top")

    # Manual legend entries
    ax.plot([], [], "o", color="tab:green", label="$R_{500c}$ direct")
    ax.plot([], [], "o", color="tab:orange", label="$R_{200c}$ extrap.")

    ax.set_xlabel("$u_{cl} = 4 g_N(R) / a_0$")
    ax.set_ylabel("$f_b = M_b / M_{tot}$")
    ax.set_ylim(0.10, 0.18)
    ax.set_title("ESD child C4: cluster baryon fraction vs $u_{cl}$")
    ax.legend(loc="lower right", fontsize=9)
    _save(fig, "fig_fb_predictions")


def fig_sample_pulls():
    """Bar plot of per-sample pulls."""
    names = []; pulls = []; colors = []
    for s in OBS.SAMPLES:
        if s.radius_def == "R_inf":
            continue
        u  = C.u_cluster(s.M_500_solar, s.R_def_mpc)
        fb = C.baryon_fraction(u)
        p  = (s.f_b - fb) / s.sigma
        names.append(s.name.split("(")[0].strip())
        pulls.append(p)
        colors.append("tab:green" if s.radius_def == "R_500c" else "tab:orange")
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.barh(names, pulls, color=colors)
    ax.axvline(0, color="k", lw=0.7)
    ax.axvspan(-2, 2, color="gray", alpha=0.12, label="$\\pm 2\\sigma$")
    ax.set_xlabel("pull = (obs - pred) / sigma")
    ax.set_title("Per-sample pull, child C4")
    ax.legend(loc="lower right", fontsize=9)
    _save(fig, "fig_sample_pulls")


def main():
    fig_R_vs_u()
    fig_fb_predictions()
    fig_sample_pulls()
    print(f"[cluster] figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()
