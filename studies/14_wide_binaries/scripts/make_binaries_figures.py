"""Study 14 figures: wide-binary γ_g vs separation."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_binaries as B
import observations as O

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name + ".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_gamma_vs_separation():
    s_kAU = np.logspace(np.log10(0.3), np.log10(40.0), 200)
    s_m   = s_kAU * B.KAU_M
    g_esd  = np.array([float(B.gamma_esd(ss, O.M_TOT_MEDIAN_MSUN)) for ss in s_m])
    g_mond = np.array([float(B.gamma_mond_simple(ss, O.M_TOT_MEDIAN_MSUN)) for ss in s_m])

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.semilogx(s_kAU, g_esd,  "k-",  lw=2.0, label=r"ESD $1+R(u)$")
    ax.semilogx(s_kAU, g_mond, "C3--", lw=1.5, label=r"MOND simple-$\nu$")
    ax.axhline(1.0, color="C0", ls=":", label="Newton ($\\gamma=1$)")
    s_mid   = [b.s_kAU_mid for b in O.SAMPLES]
    g_obs   = [b.gamma_g    for b in O.SAMPLES]
    g_err   = [b.gamma_err  for b in O.SAMPLES]
    ax.errorbar(s_mid, g_obs, yerr=g_err, fmt="o", color="C2",
                capsize=3, label="Chae 2023 (Gaia DR3)")
    ax.set_xlabel(r"projected separation $s$ [kAU]")
    ax.set_ylabel(r"$\gamma_g = g_{\rm obs} / g_N$")
    ax.set_title(r"Wide-binary acceleration ratio (M$_{\rm tot}=$1.5 M$_\odot$)")
    ax.legend(fontsize=8, loc="upper left"); ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_gamma_vs_separation")


def fig_residuals():
    s_mid = np.array([b.s_kAU_mid for b in O.SAMPLES])
    g_obs = np.array([b.gamma_g    for b in O.SAMPLES])
    g_err = np.array([b.gamma_err  for b in O.SAMPLES])
    s_m   = s_mid * B.KAU_M
    g_pre = np.array([float(B.gamma_esd(ss, O.M_TOT_MEDIAN_MSUN)) for ss in s_m])
    res_sig = (g_pre - g_obs) / g_err

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    colors = ["C0" if s <= 10 else "C3" for s in s_mid]
    ax.bar(range(len(s_mid)), res_sig, color=colors)
    ax.axhline( 0, color="k", lw=0.8)
    ax.axhline( 3, color="gray", ls="--", lw=0.8, label="3σ")
    ax.axhline(-3, color="gray", ls="--", lw=0.8)
    ax.set_xticks(range(len(s_mid)))
    ax.set_xticklabels([f"{s:.1f}" for s in s_mid])
    ax.set_xlabel(r"$s$ bin center [kAU]")
    ax.set_ylabel(r"$(\gamma_{ESD} - \gamma_{obs})/\sigma$")
    ax.set_title("ESD residuals vs Chae 2023 (blue: intermediate, red: deep)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    _save(fig, "fig_residuals")


def fig_u_vs_R():
    u = np.logspace(-1, 3, 300)
    R = B.S_PHI / (u**B.P_EXP + B.B_PHI * u**B.Q_EXP + B.C_PHI)
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.loglog(u, R, "k-", lw=1.8, label=r"$R(u) = s/[u^p + b u^q + c]$")
    ax.axhline(B.S_PHI/B.C_PHI, color="C2", ls=":", label=r"deep-MOND limit $s/c$")
    # mark the binary u range
    for s_kAU, lbl in [(2, "2 kAU"), (10, "10 kAU"), (20, "20 kAU")]:
        s_m = s_kAU * B.KAU_M
        gN  = B.G_NEWTON * O.M_TOT_MEDIAN_MSUN * B.M_SUN_KG / s_m**2
        u_b = 4 * gN / B.A0_SI
        ax.axvline(u_b, ls="--", alpha=0.5, label=lbl)
    ax.set_xlabel(r"$u = 4 g_N / a_0$")
    ax.set_ylabel(r"$R(u)$")
    ax.set_title(r"Closure-pool kernel $R(u)$ across the binary range")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_u_vs_R")


if __name__ == "__main__":
    fig_gamma_vs_separation()
    fig_residuals()
    fig_u_vs_R()
    print(f"[wide-binaries] figures written to {FIG}")
