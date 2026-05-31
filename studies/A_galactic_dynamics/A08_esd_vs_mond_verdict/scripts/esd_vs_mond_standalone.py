"""ESD vs MOND — standalone verdict figures (study 48).

Generates figures from the published headline numbers embedded in this
module.  No dependency on study 03; works on a fresh clone.

Run via::

    make summary
    # or
    python scripts/esd_vs_mond_standalone.py

Outputs
-------
figures_generated/wtl_comparison.png
    Side-by-side W/T/L bar chart for grid M/L and fixed M/L scenarios.
figures_generated/delta_chi2_summary.png
    Σ Δχ² bar chart with both scenarios, annotated with a benchmark
    bar for "random-split expected Δχ² = 0".
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = Path(__file__).parent
_STUDY48 = _HERE.parent
FIG_DIR = _STUDY48 / "figures_generated"

# ── published headline numbers ─────────────────────────────────────────────
# Source: study 03 (A02_sparc_rotation_curves) + paper 1 statistical verdict.
PUB = {
    "N": 175,
    "grid": {
        "label": "Grid M/L\n(best-fit Υ_d, Υ_b per galaxy)",
        "W": 53,
        "T": 98,
        "L": 24,
        "dchi2": -843.0,
    },
    "fixed": {
        "label": "Fixed M/L\n(Υ_d = 0.5, Υ_b = 0.7)",
        "W": 73,
        "T": 55,
        "L": 47,
        "dchi2": -588.0,
    },
}

_C_ESD  = "#2c6fad"   # ESD blue
_C_TIE  = "#888888"   # tie grey
_C_MOND = "#d62728"   # MOND red
_C_ZERO = "#333333"   # zero line


def _bar_positions(centre: float, n: int = 3, width: float = 0.22) -> list[float]:
    """Return x-positions for n side-by-side bars centred on `centre`."""
    half = (n - 1) / 2
    return [centre + (i - half) * width for i in range(n)]


# ── figure 1: W/T/L comparison ─────────────────────────────────────────────

def plot_wtl(pub: dict) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))

    scenarios = [pub["grid"], pub["fixed"]]
    x_centres = np.array([0.5, 1.5])
    width = 0.22

    for cx, sc in zip(x_centres, scenarios):
        xW, xT, xL = _bar_positions(cx, 3, width)
        ax.bar(xW, sc["W"], width, color=_C_ESD,  label="ESD wins"  if cx == x_centres[0] else "")
        ax.bar(xT, sc["T"], width, color=_C_TIE,  label="Tie"       if cx == x_centres[0] else "")
        ax.bar(xL, sc["L"], width, color=_C_MOND, label="ESD loses" if cx == x_centres[0] else "")
        # annotate totals on top of bars
        for xpos, val in ((xW, sc["W"]), (xT, sc["T"]), (xL, sc["L"])):
            ax.text(xpos, val + 1.5, str(val), ha="center", va="bottom",
                    fontsize=9, fontweight="bold")

    ax.set_xticks(x_centres)
    ax.set_xticklabels([sc["label"] for sc in scenarios], fontsize=10)
    ax.set_ylabel("Number of galaxies  (N = 175 SPARC)", fontsize=10)
    ax.set_title(
        "ESD vs MOND — Win / Tie / Loss by stellar mass-to-light scenario\n"
        r"$\Delta\chi^2 < -1$ → ESD wins,  $|\Delta\chi^2| \leq 1$ → Tie,  $\Delta\chi^2 > +1$ → ESD loses",
        fontsize=10,
    )
    ax.set_xlim(0, 2)
    ax.set_ylim(0, max(sc["T"] for sc in scenarios) * 1.18)
    ax.legend(fontsize=9, loc="upper right")
    ax.axhline(pub["N"] / 3, color=_C_ZERO, linewidth=0.8, linestyle=":",
               alpha=0.5, label="N/3 random baseline")
    ax.text(0.02, 0.97, f"N = {pub['N']} SPARC galaxies",
            transform=ax.transAxes, va="top", ha="left", fontsize=8, color="#555")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "wtl_comparison.png", dpi=150)
    plt.close(fig)
    print(f"[48-standalone] wtl_comparison.png written")


# ── figure 2: Σ Δχ² summary ────────────────────────────────────────────────

def plot_dchi2_summary(pub: dict) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))

    scenarios = [pub["grid"], pub["fixed"]]
    x = np.array([0.6, 1.4])
    width = 0.35

    bars = ax.bar(x, [sc["dchi2"] for sc in scenarios], width,
                  color=[_C_ESD, "#4a9e6b"], zorder=3)
    ax.axhline(0, color=_C_ZERO, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)

    for xi, sc, bar in zip(x, scenarios, bars):
        ax.text(xi, sc["dchi2"] - 25, f'{sc["dchi2"]:+.0f}',
                ha="center", va="top", fontsize=11, fontweight="bold",
                color="white")

    ax.set_xticks(x)
    ax.set_xticklabels([sc["label"] for sc in scenarios], fontsize=10)
    ax.set_ylabel(r"$\Sigma\,\Delta\chi^2 = \Sigma(\chi^2_{\rm ESD} - \chi^2_{\rm MOND})$",
                  fontsize=10)
    ax.set_title(
        "ESD vs MOND — total $\\chi^2$ advantage across 175 SPARC galaxies\n"
        "(negative = ESD better overall)",
        fontsize=10,
    )
    ax.set_xlim(0.1, 1.9)
    ax.text(0.98, 0.97, "← ESD better", transform=ax.transAxes,
            ha="right", va="top", fontsize=9, color=_C_ESD)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "delta_chi2_summary.png", dpi=150)
    plt.close(fig)
    print(f"[48-standalone] delta_chi2_summary.png written")


# ── main ───────────────────────────────────────────────────────────────────

def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plot_wtl(PUB)
    plot_dchi2_summary(PUB)
    print(
        "\n[48-standalone] Verdict summary (from published headline numbers):\n"
        f"  Grid M/L  — W={PUB['grid']['W']}  T={PUB['grid']['T']}  "
        f"L={PUB['grid']['L']}  Σ Δχ²={PUB['grid']['dchi2']:+.0f}\n"
        f"  Fixed M/L — W={PUB['fixed']['W']}  T={PUB['fixed']['T']}  "
        f"L={PUB['fixed']['L']}  Σ Δχ²={PUB['fixed']['dchi2']:+.0f}\n"
        f"  N = {PUB['N']} SPARC galaxies\n"
        "\n  To reproduce from per-galaxy data: run `make residuals` in "
        "studies/A_galactic_dynamics/A02_sparc_rotation_curves first,\n"
        "  then `make all` here."
    )


if __name__ == "__main__":
    main()
