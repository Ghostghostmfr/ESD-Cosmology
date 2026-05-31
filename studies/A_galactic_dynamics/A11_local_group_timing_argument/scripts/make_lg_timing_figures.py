"""Study A11 figure builder."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_lg_timing as E   # noqa: E402
import observations as O    # noqa: E402

FIG_DIR = os.path.join(_HERE, "..", "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def main() -> int:
    M_N = E.M_LG_newton(O.R_TODAY_KPC, O.V_RADIAL_TODAY_KMS, O.T_AGE_GYR)
    M_E = E.M_LG_esd   (O.R_TODAY_KPC, O.V_RADIAL_TODAY_KMS, O.T_AGE_GYR)

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    bars = ["Newton TA\n(dynamical)", "ESD TA\n(baryonic)", "Observed LG\nbaryons"]
    vals = [M_N, M_E, O.M_BARYON_OBS_MSUN]
    errs = [[0, 0, O.M_BARYON_OBS_MSUN - O.M_BARYON_OBS_LO],
            [0, 0, O.M_BARYON_OBS_HI  - O.M_BARYON_OBS_MSUN]]
    colors = ["#2c6fad", "#d62728", "#888888"]
    ax.bar(bars, vals, color=colors, yerr=errs, capsize=6)
    ax.set_yscale("log")
    ax.set_ylabel(r"$M_{\rm LG}$ [$M_\odot$]")
    ax.set_title("Study A11: Local Group timing argument")
    for i, v in enumerate(vals):
        ax.text(i, v * 1.3, f"{v:.2e}", ha="center", fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig_lg_timing.png")
    fig.savefig(out, dpi=150)
    fig.savefig(out.replace(".png", ".pdf"))
    plt.close(fig)
    print(f"[A11] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
