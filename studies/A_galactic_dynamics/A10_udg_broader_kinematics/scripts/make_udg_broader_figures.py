"""Study A10 figure builder."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_udg_broader as E   # noqa: E402
import observations as O      # noqa: E402

FIG_DIR = os.path.join(_HERE, "..", "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)

CLASS_COLOR = {"DM-free": "#2c6fad", "DM-poor": "#888888", "DM-rich": "#d62728"}


def main() -> int:
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for u in O.SAMPLES:
        sp = E.sigma_esd_efe(u.M_star_msun, u.R_half_kpc,
                             u.M_host_msun, u.r_host_kpc) / E.KM_M
        c = CLASS_COLOR.get(u.dm_class, "k")
        ax.errorbar(u.sigma_obs_kms, sp, xerr=u.sigma_err_kms,
                    fmt="o", color=c, ecolor=c, alpha=0.85)
        ax.annotate(u.label, (u.sigma_obs_kms, sp),
                    fontsize=7, xytext=(4, 4), textcoords="offset points")
    lo, hi = 1.0, 60.0
    ax.plot([lo, hi], [lo, hi], "k--", lw=1, alpha=0.5, label="1:1")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel(r"$\sigma_{\rm obs}$ [km/s]")
    ax.set_ylabel(r"$\sigma_{\rm ESD}$ [km/s]")
    ax.set_title("Study A10: UDG broader sample (ESD + EFE)")
    for cls, col in CLASS_COLOR.items():
        ax.plot([], [], "o", color=col, label=cls)
    ax.legend(fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig_sigma_udg_broader.png")
    fig.savefig(out, dpi=150)
    fig.savefig(out.replace(".png", ".pdf"))
    plt.close(fig)
    print(f"[A10] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
