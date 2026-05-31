"""
Figures for Study 24: ACT DR6 CMB lensing vs ESD's locked S_8^{CMBL}.

  fig_s8_cmbl_landscape.png
    A horizontal "landscape" plot showing ESD's locked prediction
    against the ACT DR6 only and ACT DR6 + Planck NPIPE posteriors.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.esd_lensing import s8_cmbl_esd, s8_cmbl_esd_sigma  # noqa: E402
from scripts.observations import ACT_DR6_ONLY, ACT_DR6_PLUS_NPIPE  # noqa: E402

FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures_generated"


def make_landscape_figure() -> Path:
    theory = s8_cmbl_esd()
    theory_sigma = s8_cmbl_esd_sigma()

    rows = [
        (ACT_DR6_ONLY.label, ACT_DR6_ONLY.median, ACT_DR6_ONLY.sigma, "C0"),
        (ACT_DR6_PLUS_NPIPE.label, ACT_DR6_PLUS_NPIPE.median,
         ACT_DR6_PLUS_NPIPE.sigma, "C3"),
        ("ESD locked prediction", theory, theory_sigma, "C2"),
    ]

    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    y = np.arange(len(rows))
    for i, (label, m, s, color) in enumerate(rows):
        ax.errorbar(m, i, xerr=s, fmt="o", color=color, capsize=4, lw=1.6,
                    markersize=7, label=f"{label} = {m:.3f} +/- {s:.3f}")

    ax.axvline(theory, color="C2", lw=1.0, ls="--", alpha=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlabel(r"$S_8^{\mathrm{CMBL}} = \sigma_8 (\Omega_m/0.3)^{0.25}$")
    ax.set_title("Study 24 - ACT DR6 lensing vs ESD locked prediction")
    ax.grid(True, axis="x", alpha=0.25)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    fig.tight_layout()

    out = FIGURES_DIR / "fig_s8_cmbl_landscape.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def main() -> int:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out = make_landscape_figure()
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
