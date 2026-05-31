"""Study 17 figures: EHT shadows."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_eht as E
import observations as O

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_ring_compare():
    labels = [s.label for s in O.SOURCES]
    obs    = [s.theta_obs_rad/E.MUAS for s in O.SOURCES]
    err    = [s.theta_err_rad/E.MUAS for s in O.SOURCES]
    gr     = [E.theta_ring_GR(s.M_solar, s.D_m)/E.MUAS for s in O.SOURCES]
    es     = [E.theta_ring_ESD(s.M_solar, s.D_m)[0]/E.MUAS for s in O.SOURCES]
    x = np.arange(len(labels)); w = 0.25
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.errorbar(x, obs, yerr=err, fmt="o", color="k", markersize=10, capsize=4,
                label="EHT observed", zorder=10)
    ax.bar(x-w, gr, w, color="C0", label="GR (Schwarzschild)")
    ax.bar(x,   es, w, color="C1", label="ESD R(u) → 0")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel(r"Photon-ring $\theta_d$ [$\mu$as]")
    ax.set_title("Strong-field test: ESD reproduces GR shadow exactly")
    ax.legend(); ax.grid(alpha=0.3, axis="y")
    _save(fig, "fig_ring_compare")


def fig_R_vs_u():
    u = np.logspace(-2, 25, 600)
    R = E.S_NRM/(u**E.P_EXP + E.B_AMP*u**E.Q_EXP + E.C_FLR)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.loglog(u, R, "k-", lw=1.8, label=r"$R(u) = s/\Sigma(u)$")
    for s in O.SOURCES:
        u_ps = 4.0*E.g_at_photon_sphere(s.M_solar)/E.A0_SI
        ax.axvline(u_ps, ls="--", alpha=0.7, label=f"{s.label}: u_ps = {u_ps:.2e}")
    ax.axhline(1e-10, color="grey", ls=":", alpha=0.5)
    ax.set_xlabel(r"$u = 4 g / a_0$")
    ax.set_ylabel(r"closure-pool correction $R(u)$")
    ax.set_title("Closure correction vanishes at black-hole photon spheres")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_R_vs_u")


if __name__ == "__main__":
    fig_ring_compare()
    fig_R_vs_u()
    print(f"[eht] figures written to {FIG}")
