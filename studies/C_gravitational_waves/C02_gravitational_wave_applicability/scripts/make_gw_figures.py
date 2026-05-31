"""Study 21 figures."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "..", "E03_cosmological_redshift_derivation", "scripts")))
import esd_gw as W

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_speed_constraints():
    """Visualize the GW170817 multimessenger speed bound vs alternative theories."""
    theories = [
        ("ESD prediction",     0.0,         0.0,        "C2"),
        ("GR",                 0.0,         0.0,        "C0"),
        ("Generic Horndeski",  3e-15,       1e-2,       "C3"),
        ("Scalar-tensor (TeVeS)", 0.0,      1e-3,       "C1"),
        ("Massive graviton (m=1e-22 eV)", 1e-16, 1e-15, "C4"),
    ]
    bound_observed = 3e-15
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for label, lo, hi, c in theories:
        if hi > 0:
            ax.barh(label, hi-lo, left=lo, color=c, alpha=0.7, edgecolor="k")
        else:
            ax.plot(lo, label, "o", color=c, markersize=12)
    ax.axvline(bound_observed, color="r", lw=1.5, ls="--",
               label=f"GW170817 bound: |c_GW-c|/c < {bound_observed:g}")
    ax.set_xscale("symlog", linthresh=1e-16)
    ax.set_xlabel(r"$|c_{GW} - c| / c$")
    ax.set_title("GW propagation speed: ESD predicts identity, GW170817 confirms < 3e-15")
    ax.legend()
    ax.grid(alpha=0.3, axis="x")
    _save(fig, "fig_gw_speed_constraints")


def fig_h0_landscape():
    """Standard-siren GW H_0 vs Planck CMB vs SH0ES."""
    items = [
        ("Planck CMB",                   67.36, 0.54, 0.54, "C0"),
        ("SH0ES (Cepheids+SNe)",          73.04, 1.04, 1.04, "C3"),
        ("LIGO GW170817 SS",             70.0, 12.0, 8.0,  "C2"),
        ("ESD-locked (Planck mode)",     67.36, 0.0, 0.0,  "C2"),
    ]
    labels = [i[0] for i in items]
    vals   = [i[1] for i in items]
    errp   = [i[2] for i in items]
    errm   = [i[3] for i in items]
    cols   = [i[4] for i in items]
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    for vi, yi, ep, em, ci in zip(vals, y, errp, errm, cols):
        ax.errorbar(vi, yi, xerr=[[em],[ep]], fmt="o", color=ci, capsize=4, markersize=10)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel(r"$H_0$ [km/s/Mpc]")
    ax.set_title("Standard-siren $H_0$ from GW170817 is consistent with ESD-locked $H_0$")
    ax.grid(alpha=0.3, axis="x")
    ax.invert_yaxis()
    _save(fig, "fig_h0_landscape")


if __name__ == "__main__":
    fig_speed_constraints()
    fig_h0_landscape()
    print(f"[gw] figures written to {FIG}")
