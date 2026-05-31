"""Study D07 figure builder."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_slacs_einstein as E   # noqa: E402
import observations as O         # noqa: E402

FIG_DIR = os.path.join(_HERE, "..", "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def main() -> int:
    obs   = [L.theta_E_obs for L in O.SAMPLES]
    pred  = [E.theta_E_pred_arcsec(L.M_star_msun, L.R_E_kpc,
                                   L.z_lens, L.z_source) for L in O.SAMPLES]

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.plot([0.3, 2.5], [0.3, 2.5], "k--", lw=1, alpha=0.5, label="1:1")
    for L, t_obs, t_pred in zip(O.SAMPLES, obs, pred):
        ax.plot(t_obs, t_pred, "o", color="#d62728")
        ax.annotate(L.label.replace("SDSS", ""),
                    (t_obs, t_pred), fontsize=6,
                    xytext=(4, 4), textcoords="offset points")
    ax.set_xlim(0.3, 2.5)
    ax.set_ylim(0.3, 2.5)
    ax.set_xlabel(r"$\theta_{E,\rm obs}$ [arcsec]")
    ax.set_ylabel(r"$\theta_{E,\rm ESD}$ [arcsec]")
    ax.set_title("Study D07: SLACS Einstein radius (ESD SIS)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig_theta_E_slacs.png")
    fig.savefig(out, dpi=150)
    fig.savefig(out.replace(".png", ".pdf"))
    plt.close(fig)
    print(f"[D07] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
