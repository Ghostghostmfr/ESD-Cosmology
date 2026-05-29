"""Study 06 figures: (S_8, Omega_m) tension + pull-bar across all observables.

Generates (under figures_generated/):
  fig_S8_Om_tension      S_8 vs Omega_m plane with Planck / KiDS-1000 / DES Y3
                         1-sigma ellipses + framework lock point.
  fig_pull_bars          signed pulls (lock - mean)/sigma across all
                         (survey, observable) pairs, primary reading.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_locks as L  # noqa: E402
import observations as O  # noqa: E402
from run_cmb_lss_audit import iter_pulls, lock_value  # noqa: E402

FIG_DIR = os.path.abspath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG_DIR, exist_ok=True)


# Lit (S_8, Omega_m) ellipses (1-sigma marginal; sigma_Om approximated
# from each survey's reported chain).  Values per the cited papers.
S8_OM_PROBES = [
    # name,           S_8,   sig_S8,  Omega_m, sig_Om, color
    ("Planck 2018",   0.834, 0.016,   0.3158, 0.0073, "C0"),
    ("KiDS-1000",     0.759, 0.024,   0.290,  0.040,  "C2"),
    ("DES Y3",        0.772, 0.017,   0.290,  0.030,  "C3"),
]


def fig_s8_om_tension() -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    for name, s8, sS8, om, sOm, color in S8_OM_PROBES:
        e = Ellipse((om, s8), width=2*sOm, height=2*sS8,
                    edgecolor=color, facecolor=color, alpha=0.18, lw=1.4,
                    label=f"{name}  $S_8={s8:.3f}\\pm{sS8:.3f}$")
        ax.add_patch(e)
        ax.plot(om, s8, "o", color=color, ms=4)

    # Framework lock
    ax.plot(L.OMEGA_M, L.S_8_LOCK, "*", color="black", ms=18,
            label=(f"ESD locked: $\\Omega_m={L.OMEGA_M:.4f}$, "
                   f"$S_8={L.S_8_LOCK:.4f}$"))

    ax.set_xlabel(r"$\Omega_m$")
    ax.set_ylabel(r"$S_8 \;=\; \sigma_8\sqrt{\Omega_m/0.3}$")
    ax.set_title("Study 06: ESD locked $(S_8,\\,\\Omega_m)$ vs major surveys")
    ax.set_xlim(0.22, 0.36)
    ax.set_ylim(0.70, 0.88)
    ax.legend(loc="lower right", fontsize=8, framealpha=0.97)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_S8_Om_tension.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


def fig_pull_bars() -> None:
    rows = list(iter_pulls("primary"))
    rows.sort(key=lambda r: (r["survey"], r["observable"]))
    labels = [f"{r['survey']}/{r['observable']}" for r in rows]
    pulls  = [r["pull"] for r in rows]
    colors = ["C0" if abs(p) < 1 else ("C1" if abs(p) < 2 else "C3") for p in pulls]

    fig, ax = plt.subplots(figsize=(8.5, 0.32 * len(rows) + 1.2))
    y = np.arange(len(rows))
    ax.barh(y, pulls, color=colors, edgecolor="0.3", lw=0.5)
    ax.axvline(0, color="0.3", lw=0.8)
    for s, ls in ((1, ":"), (2, "--")):
        ax.axvline(+s, color="0.5", lw=0.6, ls=ls)
        ax.axvline(-s, color="0.5", lw=0.6, ls=ls)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel(r"signed pull  $(lock - measured) / \sigma$")
    ax.set_title("Study 06: framework lock vs every survey constraint  "
                 "(primary reading)")
    pmax = max(3.5, np.abs(pulls).max() * 1.15)
    ax.set_xlim(-pmax, pmax)
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_pull_bars.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


if __name__ == "__main__":
    fig_s8_om_tension()
    fig_pull_bars()
