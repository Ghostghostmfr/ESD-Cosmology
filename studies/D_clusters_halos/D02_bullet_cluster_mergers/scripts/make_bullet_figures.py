"""Study 15 figures: dissociative cluster mergers."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_bullet as E
import observations as O

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name + ".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_ratio_per_merger():
    labels    = [m.label for m in O.SAMPLES]
    ratio_obs = [m.ratio_obs for m in O.SAMPLES]
    ratio_err = [m.ratio_err for m in O.SAMPLES]
    ratio_pre = []
    for m in O.SAMPLES:
        M_b = m.M_gas * 1e13
        R   = m.aperture_kpc / 1000.0
        ratio_pre.append(E.predict_ratio(M_b, R)["M_tot/M_b"])

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.errorbar(x - 0.12, ratio_obs, yerr=ratio_err, fmt="o", capsize=4,
                color="C2", label="observed (lensing/X-ray)")
    ax.plot(x + 0.12, ratio_pre, "ks", markersize=8, label="ESD (Identity C4)")
    ax.axhline(E.DM_OVER_B, color="C0", ls=":", label=r"$\Omega_{DM}/\Omega_b = 5.30$")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right", fontsize=8)
    ax.set_ylabel(r"$M_{\rm tot}/M_{\rm gas}$")
    ax.set_title("Dissociative cluster mergers: ESD vs observation")
    ax.legend(fontsize=9); ax.grid(alpha=0.3, axis="y")
    _save(fig, "fig_ratio_per_merger")


def fig_dm_dominance():
    M_b_range = np.logspace(12, 15, 60)
    R         = 0.3   # Mpc
    dm_frac = np.array([E.dm_dominance_fraction(M, R) for M in M_b_range])
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.semilogx(M_b_range, dm_frac, "k-", lw=1.8,
                label=r"$\Omega_{DM}/\Omega_b$ / $(M_{tot}/M_b)$")
    ax.axhline(0.80, color="C3", ls=":", label="80% gate")
    for m in O.SAMPLES:
        M_b = m.M_gas * 1e13
        dm  = E.dm_dominance_fraction(M_b, m.aperture_kpc/1000.0)
        ax.plot(M_b, dm, "o", label=m.label)
    ax.set_xlabel(r"$M_{\rm gas}$ [M$_\odot$]")
    ax.set_ylabel("dark-sector dominance fraction")
    ax.set_title(r"Dark-sector dominance: $\Omega_{DM}/\Omega_b$ over $M_{tot}/M_b$")
    ax.legend(fontsize=8, loc="lower right"); ax.grid(alpha=0.3, which="both")
    _save(fig, "fig_dm_dominance")


def fig_residuals():
    labels    = [m.label.split(" (")[0] for m in O.SAMPLES]
    resid_sig = []
    for m in O.SAMPLES:
        M_b = m.M_gas * 1e13
        R   = m.aperture_kpc / 1000.0
        ratio_pre = E.predict_ratio(M_b, R)["M_tot/M_b"]
        resid_sig.append((ratio_pre - m.ratio_obs)/m.ratio_err)
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.bar(range(len(labels)), resid_sig, color="C0")
    ax.axhline(0, color="k", lw=0.8)
    ax.axhline( 2, color="gray", ls="--", lw=0.8, label="2σ")
    ax.axhline(-2, color="gray", ls="--", lw=0.8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=15, ha="right", fontsize=8)
    ax.set_ylabel(r"$(\rm{ratio}_{ESD} - \rm{ratio}_{obs})/\sigma$")
    ax.set_title("Bullet-class residuals (ESD vs measured)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")
    _save(fig, "fig_residuals")


if __name__ == "__main__":
    fig_ratio_per_merger()
    fig_dm_dominance()
    fig_residuals()
    print(f"[bullet] figures written to {FIG}")
