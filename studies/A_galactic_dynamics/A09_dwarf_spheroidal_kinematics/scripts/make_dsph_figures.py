"""Study A09 figure builder — sigma_ESD vs sigma_obs for MW dSph sample."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_dsph as E       # noqa: E402
import observations as O   # noqa: E402

FIG_DIR = os.path.join(_HERE, "..", "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def main() -> int:
    labels = [d.label for d in O.SAMPLES]
    obs    = [d.sigma_obs_kms for d in O.SAMPLES]
    err    = [d.sigma_err_kms for d in O.SAMPLES]
    pred   = [E.sigma_esd_efe(d.M_star_msun, d.R_half_kpc, d.D_gc_kpc) / E.KM_M
              for d in O.SAMPLES]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.errorbar(obs, pred, xerr=err, fmt="o", color="#2c6fad",
                ecolor="#888", capsize=2, label="ESD with EFE")
    lo, hi = 1.0, 25.0
    ax.plot([lo, hi], [lo, hi], "k--", lw=1, alpha=0.6, label="1:1")
    for x, y, lab in zip(obs, pred, labels):
        ax.annotate(lab, (x, y), fontsize=7, alpha=0.7,
                    xytext=(3, 3), textcoords="offset points")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel(r"$\sigma_{\rm obs}$ [km/s]")
    ax.set_ylabel(r"$\sigma_{\rm ESD}$ [km/s]")
    ax.set_title("Study A09: MW dwarf-spheroidal LOS dispersions (ESD + EFE)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig_sigma_dsph.png")
    fig.savefig(out, dpi=150)
    fig.savefig(out.replace(".png", ".pdf"))
    plt.close(fig)
    print(f"[A09] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
