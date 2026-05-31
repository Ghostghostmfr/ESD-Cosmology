"""Theory 03 — D-field horizon gradient: unified figure generation.

Produces one standalone figure summarising the η gap-closure derivation
and the observational spread across published dipole analyses.

Run via::

    make figures
    # or
    python scripts/make_unified_figures.py

Output
------
figures_generated/dipole_spread.png
    Horizontal bar chart showing D_excess = D_obs − D_kin for each
    published analysis, with the ESD first-principles σ_η prediction
    marked as a vertical line.  Gap factors (D_excess / σ_η) are
    annotated and match §7.1 of the README exactly.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

_HERE   = Path(__file__).parent
_ROOT   = _HERE.parent
FIG_DIR = _ROOT / "figures_generated"

# ── observational spread — values from §7.1 of the README ─────────────────
# Each entry: (label, D_obs, survey_type)
ANALYSES: list[tuple[str, float, str]] = [
    ("Crawford 2009\n(NVSS, conservative)",     8.0e-3,  "NVSS"),
    ("Rubart & Schwarz 2013\n(NVSS lower)",      1.0e-2,  "NVSS"),
    ("Tiwari & Nusser 2016\n(NVSS)",             1.1e-2,  "NVSS"),
    ("Singal 2011\n(NVSS best)",                 1.4e-2,  "NVSS"),
    ("Secrest+ 2021\n(CatWISE2020)",             1.55e-2, "CatWISE"),
    ("Secrest+ 2022\n(joint NVSS+CatWISE)",      1.45e-2, "joint"),
]

D_KIN      = 4.61e-3   # kinematic-only (CMB v = 369.82 km/s, Ellis-Baldwin)
SIGMA_ETA  = 7.70e-4   # §7.1 ESD prediction: β_m^cosmo × σ_ζ
# gap = D_excess / SIGMA_ETA  (matches §7.1 table exactly)

_C_NVSS    = "#e07b39"
_C_CATWISE = "#6a3d9a"
_C_JOINT   = "#1f7a1f"
_C_ETA     = "#2c6fad"

_COLORS = {"NVSS": _C_NVSS, "CatWISE": _C_CATWISE, "joint": _C_JOINT}


def plot_dipole_spread() -> None:
    fig, ax = plt.subplots(figsize=(9, 5.2))

    labels  = [a[0] for a in ANALYSES]
    d_obs   = np.array([a[1] for a in ANALYSES])
    d_exc   = d_obs - D_KIN                   # what ESD must explain
    gaps    = d_exc / SIGMA_ETA               # matches §7.1 gap column
    colors  = [_COLORS[a[2]] for a in ANALYSES]

    y = np.arange(len(ANALYSES))

    # bars: D_excess from 0 to D_exc
    ax.barh(y, d_exc, color=colors, alpha=0.80, height=0.52, left=0,
            label="_nolegend_")
    # D_exc tip markers
    ax.scatter(d_exc, y, color=colors, s=60, zorder=5)

    # ESD σ_η prediction line
    ax.axvline(SIGMA_ETA, color=_C_ETA, linewidth=2.0, linestyle="--", zorder=3,
               label=rf"ESD $\sigma_\eta$ = {SIGMA_ETA:.2e}  (R(u) + slow-roll)")

    # shade prediction-to-observed range hint
    ax.axvspan(0, SIGMA_ETA, alpha=0.10, color=_C_ETA, zorder=0,
               label="ESD prediction region")

    # gap factor annotations
    for i, (exc, gap, col) in enumerate(zip(d_exc, gaps, colors)):
        ax.text(exc + 1.5e-4, i, f"×{gap:.1f}", va="center", ha="left",
                fontsize=8.5, color=col, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(
        r"$D_{\rm excess} = D_{\rm obs} - D_{\rm kin}$"
        f"   (D_kin = {D_KIN:.4f})",
        fontsize=10,
    )
    ax.set_title(
        "Cosmic radio/IR dipole excess vs ESD first-principles prediction\n"
        r"Gap factor = $D_{\rm excess} \,/\, \sigma_\eta$   "
        "(partial closure: factor 4–13 residual; "
        r"$\sigma_\eta$ is 1$\sigma$ of the η amplitude)",
        fontsize=10,
    )
    ax.set_xlim(-5e-4, max(d_exc) * 1.22)

    # light x-grid
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, linestyle=":", linewidth=0.6, alpha=0.5)
    ax.yaxis.grid(False)

    # colour legend for survey types
    legend_els = [
        Patch(color=_C_NVSS,    alpha=0.80, label="NVSS"),
        Patch(color=_C_CATWISE, alpha=0.80, label="CatWISE"),
        Patch(color=_C_JOINT,   alpha=0.80, label="Joint NVSS+CatWISE"),
    ]
    ax.legend(
        handles=[
            ax.get_lines()[0],           # σ_η line
        ] + legend_els,
        fontsize=8.5, loc="lower right",
    )

    fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "dipole_spread.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[theory03] dipole_spread.png written to {FIG_DIR}/")


def main() -> None:
    plot_dipole_spread()
    d_exc_vals = [a[1] - D_KIN for a in ANALYSES]
    gaps       = [d / SIGMA_ETA for d in d_exc_vals]
    print(
        f"\n[theory03] η closure summary (§7.1):\n"
        f"  σ_η (ESD prediction)  = {SIGMA_ETA:.2e}\n"
        f"  D_kin (kinematic)     = {D_KIN:.4f}\n"
        f"\n  Per-analysis gap (D_excess / σ_η):\n"
        + "\n".join(
            f"    {a[0].split(chr(10))[0]:35s}  ×{g:.1f}"
            for a, g in zip(ANALYSES, gaps)
        )
    )


if __name__ == "__main__":
    main()
