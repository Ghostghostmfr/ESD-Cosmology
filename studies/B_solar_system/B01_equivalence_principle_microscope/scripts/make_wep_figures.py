"""Figures for Study 27 MICROSCOPE WEP audit."""
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

OUT_DIR = HERE / "outputs"
FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig, stem: str) -> None:
    for ext in ("png", "pdf"):
        path = FIG_DIR / f"{stem}.{ext}"
        fig.savefig(path, dpi=160, bbox_inches="tight")
        print(f"wrote {path}")
    plt.close(fig)


def fig_headroom() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    labels = ["Eot-Wash\n(1999)", "MICROSCOPE\n(2017 first)",
              "MICROSCOPE\n(2022 final)", "MICROSCOPE-2\n(forecast)",
              "ESD\nprediction"]
    eta = [1e-13, 1.3e-14, s["experiment_bound"],
           s["experiment_forecast_m2"], s["eta_esd_pt_ti"]]
    colors = ["#888888", "#888888", "#a01818", "#d96b1f", "#2a7fbf"]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(x, eta, color=colors, log=True, edgecolor="black", linewidth=0.5)
    for xi, ei in zip(x, eta):
        ax.text(xi, ei * 1.5, f"{ei:.1e}", ha="center", fontsize=9)
    ax.set_yscale("log")
    ax.set_ylim(1e-25, 1e-11)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(r"Eötvös ratio $|\eta|$")
    ax.set_title("Study 27 - WEP bounds vs ESD prediction")
    ax.grid(axis="y", alpha=0.3, which="both")

    # Annotate ESD prediction's headroom
    ax.annotate(
        f"{s['orders_below_2022']:.0f} orders below\nMICROSCOPE 2022",
        xy=(4, s["eta_esd_pt_ti"]), xytext=(2.4, 1e-20),
        fontsize=10, color="#2a7fbf", ha="left",
        arrowprops=dict(arrowstyle="->", color="#2a7fbf"))
    _save(fig, "fig_wep_headroom")


def fig_channel_ratio() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    bd = s["esd_inputs"]
    # Decomposition: eta = beta_m^2 * (beta_Z/beta_m) * |Delta f_EM|
    factors = [bd["beta_m_sq_screening"], bd["beta_Z_over_beta_m"],
               bd["delta_f_em_pt_ti"]]
    names = [r"$\beta_m^2$ screening" + "\n(Cassini PPN)",
             r"$\beta_Z/\beta_m$" + "\n(channel ratio)",
             r"$\Delta f_{\rm EM}$" + "\n(Pt-Ti)"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(factors))
    ax.bar(x, factors, color=["#2a7fbf", "#6aa84f", "#d96b1f"],
           log=True, edgecolor="black", linewidth=0.5)
    for xi, fi in zip(x, factors):
        ax.text(xi, fi * 1.6, f"{fi:.1e}", ha="center", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylabel("factor")
    ax.set_yscale("log")
    ax.set_ylim(1e-13, 1e-2)
    ax.set_title(r"Study 27 - $|\eta_{\rm Pt-Ti}| = \beta_m^2 \cdot"
                 r"(\beta_Z/\beta_m) \cdot |\Delta f_{\rm EM}|$"
                 f"\n  product = {bd['eta_pt_ti_esd']:.2e}")
    ax.grid(axis="y", alpha=0.3, which="both")
    _save(fig, "fig_wep_channel_breakdown")


def main() -> int:
    fig_headroom()
    fig_channel_ratio()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
