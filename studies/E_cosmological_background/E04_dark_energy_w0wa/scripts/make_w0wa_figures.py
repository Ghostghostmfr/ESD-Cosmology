"""Study 22 figures:

  fig_w0wa_contours   chi^2 contours in the w0-wa plane.
                      1-, 2-, 3-sigma levels shown; ESD prediction
                      at (w0=-1, wa=0) marked; best-fit CPL marked.

  fig_bao_residuals   per-tracer (theory - data)/sigma residuals for
                      ESD-PRIMARY vs Planck-LCDM, matching Study 07 style.
"""

from __future__ import annotations

import json
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from desi_bao_data import DESI_Y1, DMDH, DV  # noqa: E402
from esd_w0wa import (  # noqa: E402
    D_H,
    D_M,
    D_V,
    cosmo_esd_primary,
    cosmo_planck_lcdm,
    r_d_aubourg2015,
    Cosmo,
)

OUT_DIR = os.path.join(_HERE, "outputs")
FIG_DIR = os.path.abspath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG_DIR, exist_ok=True)

# 2D chi^2 thresholds (2 dof) for sigma contours.
DCHI2_1S = 2.30
DCHI2_2S = 6.18
DCHI2_3S = 11.83


# ---------------------------------------------------------------------------
# Figure 1: w0-wa chi^2 contour plot
# ---------------------------------------------------------------------------
def fig_w0wa_contours() -> None:
    npz_path = os.path.join(OUT_DIR, "chi2_grid.npz")
    if not os.path.exists(npz_path):
        print(f"[fig] {npz_path} not found — run make audit first.")
        return

    data     = np.load(npz_path)
    w0_arr   = data["w0_arr"]
    wa_arr   = data["wa_arr"]
    chi2_map = data["chi2_map"]
    chi2_min = float(data["chi2_min"])
    w0_bf    = float(data["w0_bf"])
    wa_bf    = float(data["wa_bf"])

    # Profiled delta-chi^2 (profile over H0, which is already done in the grid)
    dchi2 = chi2_map - chi2_min
    W0, WA = np.meshgrid(w0_arr, wa_arr, indexing="ij")

    fig, ax = plt.subplots(figsize=(7.0, 5.5))

    # Filled contours for background (no alpha — keeps PDF rendering clean).
    levels_fill = [0.0, DCHI2_1S, DCHI2_2S, DCHI2_3S, dchi2.max() + 1.0]
    ax.contourf(W0, WA, dchi2, levels=levels_fill,
                colors=["#2166ac", "#74add1", "#abd9e9", "#f7fbff"])

    # Sigma contour lines
    cs = ax.contour(W0, WA, dchi2,
                    levels=[DCHI2_1S, DCHI2_2S, DCHI2_3S],
                    colors=["#1a1a2e", "#1a1a2e", "#1a1a2e"],
                    linewidths=[1.2, 1.6, 2.0],
                    linestyles=["-", "-", "-"])
    ax.clabel(cs, fmt={DCHI2_1S: "1σ", DCHI2_2S: "2σ", DCHI2_3S: "3σ"},
              fontsize=9, inline=True)

    # Best-fit CPL marker
    ax.plot(w0_bf, wa_bf, "s", color="#d7191c", ms=9, zorder=6,
            label=f"Best-fit CPL: $w_0$={w0_bf:.2f}, $w_a$={wa_bf:.2f}")

    # ESD prediction: w0=-1, wa=0 (exact)
    ax.plot(-1.0, 0.0, "*", color="#fdae61", ms=16, markeredgecolor="0.2",
            markeredgewidth=0.8, zorder=7, label="ESD: $w_0=-1$, $w_a=0$ (theorem)")

    # ΛCDM reference line
    ax.axvline(-1.0, color="0.5", lw=0.8, ls="--", zorder=3, label="$w_0=-1$ (ΛCDM)")
    ax.axhline(0.0,  color="0.5", lw=0.8, ls=":",  zorder=3)

    ax.set_xlabel("$w_0$", fontsize=13)
    ax.set_ylabel("$w_a$", fontsize=13)
    ax.set_xlim(w0_arr[0], w0_arr[-1])
    ax.set_ylim(wa_arr[0], wa_arr[-1])
    ax.set_title(
        "Study 22: DESI Y1 BAO + Planck 2018 CMB\n$w_0$-$w_a$ profiled $\\Delta\\chi^2$ contours",
        fontsize=10,
    )
    ax.legend(loc="upper left", fontsize=8, framealpha=0.85)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()

    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_w0wa_contours.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: per-tracer BAO residuals (same style as Study 07)
# ---------------------------------------------------------------------------
def fig_bao_residuals() -> None:
    json_path = os.path.join(OUT_DIR, "summary.json")
    if not os.path.exists(json_path):
        print(f"[fig] {json_path} not found — run make audit first.")
        return

    with open(json_path) as f:
        summary = json.load(f)

    bf = summary["best_fit_cpl"]
    c_esd  = cosmo_esd_primary(67.36)
    c_pla  = cosmo_planck_lcdm(67.36)
    c_cpl  = Cosmo(
        H0=bf["H0"],
        Omega_m=c_esd.Omega_m,
        Omega_b=c_esd.Omega_b,
        w0=bf["w0"],
        wa=bf["wa"],
    )

    cosmologies = [
        ("ESD (w₀=−1, wₐ=0)", c_esd,  "C0",  "o"),
        ("Best-fit CPL",       c_cpl,  "C1",  "s"),
        ("Planck-ΛCDM",        c_pla,  "k",   "x"),
    ]

    # Build label list in DESI Y1 tracer order
    labels = []
    for t in DESI_Y1:
        if isinstance(t, DV):
            labels.append(f"{t.name} ($D_V$)")
        else:
            labels.append(f"{t.name} ($D_M$)")
            labels.append(f"{t.name} ($D_H$)")

    x = np.arange(len(labels))
    offsets = {"ESD (w₀=−1, wₐ=0)": -0.22,
               "Best-fit CPL":        0.0,
               "Planck-ΛCDM":        +0.22}

    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    for cosmo_label, c, color, marker in cosmologies:
        rd = r_d_aubourg2015(c)
        scatter_kwargs = {
            "color": color,
            "marker": marker,
            "s": 45,
            "lw": 0.5,
            "zorder": 5,
        }
        if marker != "x":
            scatter_kwargs["edgecolor"] = "0.2"
        for t in DESI_Y1:
            if isinstance(t, DV):
                th = D_V(c, t.z_eff) / rd
                res = (th - t.DV_rd) / t.sigma
                lbl = f"{t.name} ($D_V$)"
                i = labels.index(lbl)
                ax.scatter(x[i] + offsets[cosmo_label], res,
                           **scatter_kwargs,
                           label=cosmo_label if t.name == "BGS" else None)
            else:
                th_M = D_M(c, t.z_eff) / rd
                th_H = D_H(c, t.z_eff) / rd
                for lbl_sfx, th_val, dat_val, sig_val in [
                    (f"($D_M$)", th_M, t.DM_rd, t.DM_sig),
                    (f"($D_H$)", th_H, t.DH_rd, t.DH_sig),
                ]:
                    lbl = f"{t.name} {lbl_sfx}"
                    i = labels.index(lbl)
                    res = (th_val - dat_val) / sig_val
                    ax.scatter(x[i] + offsets[cosmo_label], res,
                               **scatter_kwargs,
                               label=None)

    ax.axhline(0,  color="0.4", lw=0.8)
    ax.axhline(+1, color="0.6", lw=0.5, ls=":")
    ax.axhline(-1, color="0.6", lw=0.5, ls=":")
    ax.axhline(+2, color="0.6", lw=0.5, ls="--")
    ax.axhline(-2, color="0.6", lw=0.5, ls="--")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("residual / 1$\\sigma$")
    ax.set_title(
        "Study 22: DESI Y1 BAO per-tracer residuals\n"
        "ESD (w₀=−1, wₐ=0) vs best-fit CPL vs Planck-ΛCDM"
    )
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()

    for ext in ("png", "pdf"):
        p = os.path.join(FIG_DIR, f"fig_bao_residuals.{ext}")
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


if __name__ == "__main__":
    fig_w0wa_contours()
    fig_bao_residuals()
