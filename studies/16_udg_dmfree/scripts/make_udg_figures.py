"""Study 16 figures: DM-free UDGs."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_udg as U
import observations as O

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_sigma_compare():
    labels = [u.label for u in O.SAMPLES]
    obs    = [u.sigma_obs_kms for u in O.SAMPLES]
    err    = [u.sigma_obs_err_kms for u in O.SAMPLES]
    pub_N  = [u.sigma_newton_kms for u in O.SAMPLES]
    pub_MN = [u.sigma_mond_noEFE_kms for u in O.SAMPLES]
    pub_ME = [u.sigma_mond_EFE_kms for u in O.SAMPLES]
    esd_N  = [u.sigma_newton_kms * (1 + U.R_of_u(4*U.g_newton(u.M_star_msun,u.R_half_kpc)/U.A0_SI))**0.5 for u in O.SAMPLES]
    esd_E  = []
    for u in O.SAMPLES:
        g_i = U.g_newton(u.M_star_msun, u.R_half_kpc)
        g_e = U.g_newton(u.host_M_msun, u.host_distance_kpc)
        u_ef = 4*(g_i+g_e)/U.A0_SI
        esd_E.append(u.sigma_newton_kms * (1 + U.R_of_u(u_ef))**0.5)
    x = np.arange(len(labels)); w = 0.13
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.errorbar(x, obs, yerr=err, fmt="o", color="k", capsize=4, markersize=10,
                label="observed", zorder=10)
    ax.bar(x-2*w, pub_N,  w, color="C0", label="Newton (pub)")
    ax.bar(x-1*w, pub_MN, w, color="C3", label="MOND no-EFE (pub)")
    ax.bar(x,       esd_N,w, color="C1", label="ESD no-EFE")
    ax.bar(x+1*w, esd_E,  w, color="C2", label="ESD with-EFE")
    ax.bar(x+2*w, pub_ME, w, color="C4", label="MOND with-EFE (pub)")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel(r"$\sigma_{\rm los}$ [km/s]")
    ax.set_title("DM-free UDG velocity dispersions")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")
    _save(fig, "fig_sigma_compare")


def fig_boost_vs_u():
    u = np.logspace(-2, 2, 300)
    R = U.S_NRM/(u**U.P_EXP + U.B_AMP*u**U.Q_EXP + U.C_FLR)
    boost_esd = np.sqrt(1+R)
    boost_mn  = 1.0/np.sqrt(1 - np.exp(-np.sqrt((u*U.A0_SI/4)/U.A0_SI)))
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.loglog(u, boost_esd, "k-",  lw=1.8, label=r"$\sqrt{1+R(u)}$ (ESD)")
    ax.loglog(u, boost_mn,  "C3--", lw=1.5, label=r"simple-$\nu$ MOND")
    for u_ in O.SAMPLES:
        g_i = U.g_newton(u_.M_star_msun, u_.R_half_kpc)
        g_e = U.g_newton(u_.host_M_msun, u_.host_distance_kpc)
        ax.axvline(4*g_i/U.A0_SI,        ls=":", color="C0", alpha=0.6,
                   label=f"{u_.label} no-EFE u")
        ax.axvline(4*(g_i+g_e)/U.A0_SI, ls="--", color="C2", alpha=0.6,
                   label=f"{u_.label} EFE u")
    ax.set_xlabel(r"$u = 4g/a_0$")
    ax.set_ylabel(r"$\sigma$ enhancement factor")
    ax.set_title("ESD vs simple-ν MOND enhancement at UDG accelerations")
    ax.legend(fontsize=7); ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_boost_vs_u")


if __name__ == "__main__":
    fig_sigma_compare()
    fig_boost_vs_u()
    print(f"[udg] figures written to {FIG}")
