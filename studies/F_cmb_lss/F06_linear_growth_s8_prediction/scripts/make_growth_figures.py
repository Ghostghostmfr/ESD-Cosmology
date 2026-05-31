"""Study 19 figures."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_growth as G

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_s8_landscape():
    points = [
        ("Planck 2018 (CMB)",   0.832, 0.013, "C0"),
        ("KiDS-1000",           0.766, 0.017, "C3"),
        ("DES-Y3",              0.776, 0.017, "C3"),
        ("HSC-Y3",              0.776, 0.026, "C3"),
        ("WL joint",            0.7719, 0.0109, "C3"),
        ("ESD prediction",      G.S8_ESD(), 0.006*np.sqrt(G.OMEGA_M_LOCK/0.3), "C2"),
    ]
    labels = [p[0] for p in points]
    vals   = [p[1] for p in points]
    errs   = [p[2] for p in points]
    cols   = [p[3] for p in points]
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for vi, yi, ei, ci in zip(vals, y, errs, cols):
        ax.errorbar(vi, yi, xerr=ei, fmt="o", color=ci, capsize=4, markersize=10)
    ax.axvline(G.S8_ESD(), color="C2", lw=1.5, ls="--", alpha=0.6,
               label=f"ESD prediction = {G.S8_ESD():.4f}")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel(r"$S_8 = \sigma_8 \sqrt{\Omega_m/0.3}$")
    ax.set_title(r"ESD predicts $S_8$ = 0.832 (Planck-side) from $\sigma_8$ + locked $\Omega_m$")
    ax.legend(loc="lower right"); ax.grid(alpha=0.3, axis="x")
    ax.invert_yaxis()
    _save(fig, "fig_s8_landscape")


def fig_applicability():
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.axis("off")
    txt = (
        r"$\bf{Applicability\ of\ R(u)\ to\ density\ perturbations}$" + "\n\n"
        r"$\bf{Linear\ regime}\ (\delta \ll 1)$" + "\n"
        r"   $\delta(x,t)$ is a fluctuation of the same field as the background" + "\n"
        r"   No system/spectator split  $\Rightarrow$ axiom (A1) fails" + "\n"
        r"   $\Rightarrow$ R(u) does NOT modify linear growth" + "\n"
        r"   $\Rightarrow$ $\sigma_8^{ESD} = \sigma_8^{\Lambda CDM}$" + "\n\n"
        r"$\bf{Nonlinear\ regime}\ (\delta \gtrsim 1,\ virialized\ halo)$" + "\n"
        r"   Halo is a localized subsystem against a separated background" + "\n"
        r"   Well-defined g, all three axioms hold" + "\n"
        r"   $\Rightarrow$ R(u) applies (Studies 09-16: RAR, SPARC, ...)" + "\n\n"
        r"$\bf{Naive\ alternative\ (ruled\ out)}$" + "\n"
        f"   If (A1) held linearly: u(8 Mpc/h) = 7.4e-3, R(u) = 18.7\n"
        f"   $\\sigma_8$ would be boosted by 4.4x — incompatible with all data"
    )
    ax.text(0.02, 0.97, txt, ha="left", va="top",
            family="monospace", fontsize=10)
    fig.suptitle("Applicability theorem: closes Study 18 OPEN item")
    _save(fig, "fig_applicability_theorem")


if __name__ == "__main__":
    fig_s8_landscape()
    fig_applicability()
    print(f"[growth] figures written to {FIG}")
