"""Figures for Study 25 - Cosmic dipole audit (MATTER channel)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from dipole_data import (  # noqa: E402
    NVSS, CATWISE, JOINT, DIR_CMB_LDEG, DIR_CMB_BDEG,
)

OUT_DIR = HERE / "outputs"
FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig, stem: str) -> None:
    for ext in ("png", "pdf"):
        path = FIG_DIR / f"{stem}.{ext}"
        fig.savefig(path, dpi=160, bbox_inches="tight")
        print(f"wrote {path}")
    plt.close(fig)


def _ll_to_rad(l_deg: float, b_deg: float) -> tuple[float, float]:
    l = np.deg2rad(((l_deg + 180.0) % 360.0) - 180.0)
    b = np.deg2rad(b_deg)
    return l, b


def fig_amplitudes() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    a = s["anchor"]
    surveys = [NVSS, CATWISE, JOINT]
    names = [sv.name for sv in surveys]
    D_obs = np.array([sv.D_obs for sv in surveys]) * 1e3
    D_err = np.array([sv.D_err for sv in surveys]) * 1e3
    D_kin = a["D_kin_NVSS_alpha0p75"] * 1e3
    D_total_pred = (a["D_kin_NVSS_alpha0p75"] + a["D_excess"]) * 1e3

    x = np.arange(len(names))
    w = 0.32
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.bar(x - w, [D_kin] * len(names), w, color="#9aa0a6",
           edgecolor="black", linewidth=0.4,
           label=f"Ellis-Baldwin kinematic from CMB v ({D_kin:.2f})")
    ax.bar(x, D_obs, w, yerr=D_err, color="#d96b1f",
           ecolor="black", capsize=4, edgecolor="black", linewidth=0.4,
           label="Observed dipole")
    ax.bar(x + w, [D_total_pred] * len(names), w, color="#2a7fbf",
           edgecolor="black", linewidth=0.4,
           label=(f"ESD: kinematic + MATTER A$^2$(D) excess "
                  f"(eta={a['eta_best']:.2e})"))

    for xi, do, de in zip(x, D_obs, D_err):
        ax.text(xi, do + de + 0.4, f"{do:.1f}", ha="center",
                fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel(r"Dipole amplitude $D \times 10^{3}$")
    ax.set_title("Study 25 - Cosmic dipole: MATTER A$^2$(D) channel "
                 f"reproduces the excess at {a['eta_significance']:.1f}$\\sigma$")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    _save(fig, "fig_dipole_amplitudes")


def fig_directions() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    g_l, g_b = s["g_hat_matter_lb"]

    fig = plt.figure(figsize=(10, 5.5))
    ax = fig.add_subplot(111, projection="mollweide")

    l, b = _ll_to_rad(DIR_CMB_LDEG, DIR_CMB_BDEG)
    ax.scatter([l], [b], s=200, marker="*", color="black", zorder=5,
               label=f"CMB kinematic ({DIR_CMB_LDEG:.0f}, {DIR_CMB_BDEG:.0f})")

    l, b = _ll_to_rad(g_l, g_b)
    ax.scatter([l], [b], s=220, marker="X", color="#2a7fbf", zorder=6,
               edgecolor="black", linewidths=1.2,
               label=fr"$\hat g_{{\rm matter}}$ ({g_l:.0f}, {g_b:+.0f})")

    surveys_dir = [NVSS, CATWISE, JOINT]
    colors = ["#d96b1f", "#6aa84f", "#a01818"]
    for sv, c in zip(surveys_dir, colors):
        if sv.dir_l_deg is None:
            continue
        l, b = _ll_to_rad(sv.dir_l_deg, sv.dir_b_deg)
        ax.scatter([l], [b], s=110, color=c, edgecolor="black", zorder=4,
                   label=f"{sv.name} ({sv.dir_l_deg:.0f}, {sv.dir_b_deg:.0f})")

    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=2,
              fontsize=9)
    ax.set_title("Cosmic dipole axes vs MATTER-channel $\\hat g$ "
                 "(galactic)", pad=20)
    _save(fig, "fig_dipole_directions")


def fig_cross_observable_alignment() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    seps = s["cross_observable_separations_deg"]
    names = list(seps.keys())
    vals = np.array(list(seps.values()))
    pass_mask = vals < 35.0
    colors = ["#2a7fbf" if ok else "#a01818" for ok in pass_mask]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    y = np.arange(len(names))[::-1]
    ax.barh(y, vals, color=colors, edgecolor="black", linewidth=0.4)
    for yi, v in zip(y, vals):
        ax.text(v + 0.6, yi, f"{v:.1f} deg",
                va="center", fontsize=9, fontweight="bold")
    ax.axvline(35.0, color="black", ls="--", lw=1,
               label=r"gate: 35 deg")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel(r"separation from $\hat g_{\rm matter}$ [deg]")
    ax.set_title(f"Study 25 - MATTER channel cross-observable alignment "
                 f"({s['n_pass']}/{s['n_total']} PASS)")
    ax.set_xlim(0, max(vals) * 1.25 + 5)
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.3)
    _save(fig, "fig_cross_observable_alignment")


def main() -> int:
    fig_amplitudes()
    fig_directions()
    fig_cross_observable_alignment()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
