"""Theory 01 figures."""
from __future__ import annotations
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_bh as B

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)

def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)

def fig_R_of_u_kernel():
    u = np.logspace(-12, 22, 800)
    R = np.array([B.R_of_u(float(x)) for x in u])
    asy_UV = B.S_NRM / u**B.P_EXP
    cap_IR = B.S_NRM / B.C_FLR
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.loglog(u, R, lw=2, label=r"$R(u) = s/\Sigma(u)$")
    ax.loglog(u, asy_UV, ls="--", lw=1, color="C3",
              label=r"UV asymptote $s/u^p$")
    ax.axhline(cap_IR, ls=":", lw=1, color="C2",
               label=fr"IR cap $s/c \approx {cap_IR:.2f}$")
    ax.set_xlabel(r"$u = 4g/a_0$")
    ax.set_ylabel(r"$R(u)$")
    ax.set_title("ESD closure-pool kernel: regular everywhere, UV-finite, no pole")
    ax.legend()
    ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_R_of_u_kernel")

def fig_horizon_landscape():
    rows = B.horizon_u_table()
    rows2 = B.relational_boundary_table()
    M  = np.array([r["M_solar"] for r in rows])
    u_h = np.array([r["u_h"] for r in rows])
    R_h = np.array([r["R_h"] for r in rows])
    r_s = np.array([r["r_s_m"] for r in rows])
    r_u1 = np.array([r["r_u1_m"] for r in rows2])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax1.loglog(M, u_h, "o-", color="C0", label=r"$u(r_s) = 4g_h/a_0$")
    ax1.axhline(1.0, ls=":", color="C3", label=r"MOND scale $u = 1$")
    ax1.set_xlabel(r"$M$ [$M_\odot$]")
    ax1.set_ylabel(r"$u$ at horizon")
    ax1.set_title("Horizons live in the deep strong-field cone")
    ax1.grid(alpha=0.3, which="both"); ax1.legend()

    ax2.loglog(M, r_s,  "s-", color="C0", label=r"$r_s = 2GM/c^2$")
    ax2.loglog(M, r_u1, "o-", color="C2", label=r"$r(u=1)$  (MOND shell)")
    ax2.set_xlabel(r"$M$ [$M_\odot$]")
    ax2.set_ylabel(r"radius [m]")
    ax2.set_title("MOND-scale shell sits FAR outside the horizon")
    ax2.grid(alpha=0.3, which="both"); ax2.legend()
    _save(fig, "fig_horizon_landscape")

def fig_SBH_T_Hawking():
    M = np.logspace(0, 11, 200)
    S = np.array([B.S_BH(float(m)) for m in M])
    T = np.array([B.T_Hawking(float(m)) for m in M])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax1.loglog(M, S, lw=2, color="C0")
    ax1.set_xlabel(r"$M$ [$M_\odot$]")
    ax1.set_ylabel(r"$S_{BH}/k_B$")
    ax1.set_title(r"$S_{BH} = A/(4 l_P^2)$ — inherited from GR (R(u) inactive)")
    ax1.grid(alpha=0.3, which="both")
    ax2.loglog(M, T, lw=2, color="C3")
    ax2.set_xlabel(r"$M$ [$M_\odot$]")
    ax2.set_ylabel(r"$T_H$ [K]")
    ax2.set_title(r"$T_H = \hbar c^3 / (8\pi G M k_B)$ — same")
    ax2.grid(alpha=0.3, which="both")
    _save(fig, "fig_SBH_T_Hawking")

if __name__ == "__main__":
    fig_R_of_u_kernel()
    fig_horizon_landscape()
    fig_SBH_T_Hawking()
    print(f"[bh] figures written to {FIG}")
