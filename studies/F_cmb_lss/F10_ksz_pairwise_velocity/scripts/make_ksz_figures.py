"""Figures for Study 37 — kSZ pairwise-velocity amplitude."""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ksz_data import KSZ_MEASUREMENTS
from esd_ksz import A_ksz_esd

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    A_pred = A_ksz_esd()
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    labels = [m[0] for m in KSZ_MEASUREMENTS]
    A      = np.array([m[1] for m in KSZ_MEASUREMENTS])
    sig    = np.array([m[2] for m in KSZ_MEASUREMENTS])
    snr    = np.array([m[3] for m in KSZ_MEASUREMENTS])
    y = np.arange(len(labels))

    ax.errorbar(A, y, xerr=sig, fmt="o", capsize=4, ms=7, color="C0",
                label="kSZ pairwise-velocity measurements")
    for yi, s in zip(y, snr):
        ax.annotate(f"{s:.1f}σ", (1.55, yi), fontsize=8,
                    ha="left", va="center", color="gray")
    ax.axvline(A_pred, color="black", lw=2,
               label=f"ESD prediction $A_{{kSZ}} = {A_pred:.2f}$ (= ΛCDM, Study 19)")
    ax.axvspan(0.9, 1.1, color="black", alpha=0.08)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(r"$A_{kSZ} = (f \sigma_8 \bar\tau)_{\rm obs}\,/\,(f \sigma_8 \bar\tau)_{\Lambda\rm CDM}$")
    ax.set_title("Study 37 — kSZ pairwise-velocity amplitude vs ESD/ΛCDM prediction\n"
                 "(detection SNR in gray)")
    ax.set_xlim(0.0, 1.8)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()

    out = FIG_DIR / "ksz_amplitude.png"
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
