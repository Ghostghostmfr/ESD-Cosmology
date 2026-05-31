"""Study 18 figures: S_8 tension."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_s8 as S
import observations as O

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_s8_compare():
    ms = O.MEASUREMENTS
    labels = [m.label for m in ms]
    vals   = [m.S8 for m in ms]
    errs   = [m.S8_err for m in ms]
    colors = ["C0" if m.probe == "CMB" else "C3" for m in ms]
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7, 4.0))
    ax.errorbar(vals, y, xerr=errs, fmt="o", color="k", capsize=4, markersize=8)
    for vi, yi, ci in zip(vals, y, colors):
        ax.plot(vi, yi, "o", color=ci, markersize=10, zorder=3)
    wl = O.weak_lensing()
    joint, joint_err = S.inverse_variance_combine([m.S8 for m in wl], [m.S8_err for m in wl])
    ax.axvspan(joint - joint_err, joint + joint_err, color="C3", alpha=0.18,
               label=f"WL joint = {joint:.3f} ± {joint_err:.3f}")
    pl = O.planck()
    ax.axvspan(pl.S8 - pl.S8_err, pl.S8 + pl.S8_err, color="C0", alpha=0.18,
               label=f"Planck = {pl.S8} ± {pl.S8_err}")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel(r"$S_8 = \sigma_8 \sqrt{\Omega_m/0.3}$")
    ax.set_title(r"$S_8$ tension: 3.54$\sigma$ between Planck CMB and weak lensing")
    ax.legend(loc="lower right"); ax.grid(alpha=0.3, axis="x")
    ax.invert_yaxis()
    _save(fig, "fig_s8_compare")


def fig_omega_m_match():
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ms = O.MEASUREMENTS
    labels = [m.label for m in ms]
    vals   = [m.Omega_m for m in ms]
    errs   = [m.Omega_m_err for m in ms]
    y = np.arange(len(labels))
    ax.errorbar(vals, y, xerr=errs, fmt="o", color="k", capsize=4, markersize=8)
    ax.axvline(S.OMEGA_M_LOCK, color="C2", lw=2.0,
               label=fr"ESD-locked $\Omega_m$ = {S.OMEGA_M_LOCK:.4f}")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel(r"$\Omega_m$")
    ax.set_title(r"ESD-locked $\Omega_m$ matches Planck to << 1%")
    ax.legend(); ax.grid(alpha=0.3, axis="x")
    ax.invert_yaxis()
    _save(fig, "fig_omega_m_match")


if __name__ == "__main__":
    fig_s8_compare()
    fig_omega_m_match()
    print(f"[s8] figures written to {FIG}")
