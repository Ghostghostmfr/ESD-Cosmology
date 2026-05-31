"""Figures for Study 26 cosmic-birefringence audit."""
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

from birefringence_data import all_measurements, FORECASTS

OUT_DIR = HERE / "outputs"
FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig, stem: str) -> None:
    for ext in ("png", "pdf"):
        path = FIG_DIR / f"{stem}.{ext}"
        fig.savefig(path, dpi=160, bbox_inches="tight")
        print(f"wrote {path}")
    plt.close(fig)


def fig_measurements() -> None:
    summary = json.loads((OUT_DIR / "summary.json").read_text())
    rows = summary["measurements"]
    labels = [r["name"].split("(")[0].strip() for r in rows]
    betas = np.array([r["beta_deg"] for r in rows])
    sigs = np.array([r["sigma_deg"] for r in rows])
    tens = np.array([r["tension_sigma"] for r in rows])
    y = np.arange(len(labels))[::-1]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.errorbar(betas, y, xerr=sigs, fmt="o", color="#2a7fbf",
                ecolor="#2a7fbf", capsize=4, markersize=8,
                label="measurement")
    ax.axvline(0.0, color="black", lw=2, ls="--",
               label=r"ESD prediction $\beta=0$")
    for yi, ti in zip(y, tens):
        ax.text(0.55, yi, f"{abs(ti):.2f}$\\sigma$ tension",
                va="center", fontsize=10, color="#a01818", fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel(r"isotropic birefringence angle $\beta$ (deg)")
    ax.set_xlim(-0.2, 0.85)
    ax.set_title("Study 26 - CMB cosmic birefringence vs ESD prediction "
                 r"($\beta = 0$)")
    ax.grid(axis="x", alpha=0.3)
    ax.legend(loc="lower right")
    _save(fig, "fig_beta_measurements")


def fig_forecast() -> None:
    beta_truth = 0.342
    fig, ax = plt.subplots(figsize=(8, 4.5))
    exps = list(FORECASTS.keys())
    sigs = np.array([FORECASTS[e] for e in exps])
    disc = beta_truth / sigs
    x = np.arange(len(exps))
    bars = ax.bar(x, disc, color=["#2a7fbf", "#6aa84f", "#d96b1f"])
    for xi, di in zip(x, disc):
        ax.text(xi, di + 0.4, f"{di:.1f}$\\sigma$",
                ha="center", fontsize=10, fontweight="bold")
    ax.axhline(5.0, color="black", ls="--", lw=1.5,
               label=r"$5\sigma$ discovery threshold")
    ax.axhline(3.64, color="#a01818", ls=":", lw=1.5,
               label=r"current joint $3.64\sigma$ (E&K 2023)")
    ax.set_xticks(x)
    ax.set_xticklabels(exps, rotation=15, ha="right")
    ax.set_ylabel(r"forecast significance of $\beta = 0.342^\circ$ detection")
    ax.set_title("Study 26 - Falsifier forecast for ESD's "
                 r"$\beta = 0$ prediction")
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    _save(fig, "fig_falsifier_forecast")


def main() -> int:
    fig_measurements()
    fig_forecast()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
