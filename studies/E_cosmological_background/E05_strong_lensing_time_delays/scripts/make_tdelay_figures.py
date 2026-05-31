"""Study 31 figures: H_0 anchor comparison and D_dt cosmology curve."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from tdcosmo_data import (
    H0_ESD, H0_ESD_SIGMA,
    H0_PLANCK, H0_PLANCK_SIGMA,
    H0_SH0ES, H0_SH0ES_SIGMA,
    H0_TDCOSMO_WONG2020, H0_TDCOSMO_WONG2020_SIGMA_PLUS,
    H0_TDCOSMO_WONG2020_SIGMA_MINUS,
    H0_TDCOSMO_IV, H0_TDCOSMO_IV_SIGMA_PLUS, H0_TDCOSMO_IV_SIGMA_MINUS,
    D_DT_B1608_MPC, D_DT_B1608_SIGMA, TDCOSMO_LENSES,
)
from esd_tdelay import time_delay_distance_mpc

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def fig_H0_anchors():
    labels = ["TDCOSMO-IV\nBirrer+20",
              "TDCOSMO/H0LiCOW\nWong+20",
              "SH0ES\nRiess+22",
              "Planck\n2018",
              "ESD\n(Studies 08/12)"]
    vals = [H0_TDCOSMO_IV, H0_TDCOSMO_WONG2020, H0_SH0ES, H0_PLANCK, H0_ESD]
    err_minus = [H0_TDCOSMO_IV_SIGMA_MINUS, H0_TDCOSMO_WONG2020_SIGMA_MINUS,
                 H0_SH0ES_SIGMA, H0_PLANCK_SIGMA, H0_ESD_SIGMA]
    err_plus  = [H0_TDCOSMO_IV_SIGMA_PLUS,  H0_TDCOSMO_WONG2020_SIGMA_PLUS,
                 H0_SH0ES_SIGMA, H0_PLANCK_SIGMA, H0_ESD_SIGMA]
    colors = ["C0", "C3", "C3", "C0", "C2"]

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    y = np.arange(len(labels))
    ax.errorbar(vals, y, xerr=[err_minus, err_plus], fmt="o",
                ecolor="0.3", capsize=4, ms=7,
                mfc="white", mec="k")
    for yi, c, v in zip(y, colors, vals):
        ax.plot(v, yi, "o", color=c, ms=8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.axvspan(H0_ESD - H0_ESD_SIGMA, H0_ESD + H0_ESD_SIGMA,
               color="C2", alpha=0.15, label="ESD 1$\\sigma$")
    ax.set_xlabel(r"$H_0$  [km/s/Mpc]")
    ax.set_title("Study 31 - $H_0$ anchors vs ESD prediction")
    ax.legend(loc="lower right")
    ax.set_xlim(63, 78)
    fig.tight_layout()
    out = FIG_DIR / "tdelay_H0_anchors.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


def fig_D_dt_vs_zl():
    """D_dt(z_l, z_s) for ESD H_0 and Wong+ 2020 H_0, overlaid on the
    6-lens TDCOSMO sample."""
    z_l_grid = np.linspace(0.1, 1.0, 60)
    z_s_fid = 1.7
    D_dt_esd  = [time_delay_distance_mpc(z, z_s_fid, H0_ESD)
                 for z in z_l_grid]
    D_dt_wong = [time_delay_distance_mpc(z, z_s_fid, H0_TDCOSMO_WONG2020)
                 for z in z_l_grid]

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(z_l_grid, D_dt_esd, "C2-", lw=2.0,
            label=f"ESD ($H_0={H0_ESD:.2f}$)")
    ax.plot(z_l_grid, D_dt_wong, "C3--", lw=2.0,
            label=f"Wong+ 2020 ($H_0={H0_TDCOSMO_WONG2020:.1f}$)")
    # B1608 point
    z_l_b = TDCOSMO_LENSES["B1608+656"]["z_lens"]
    ax.errorbar([z_l_b], [D_DT_B1608_MPC], yerr=[D_DT_B1608_SIGMA],
                fmt="o", color="k", ms=7, capsize=4,
                label="B1608+656 (Suyu+ 2010)")
    ax.set_xlabel(r"$z_\mathrm{lens}$")
    ax.set_ylabel(r"$D_{\Delta t}$  [Mpc]   (at $z_\mathrm{src}=1.7$)")
    ax.set_title("Study 31 - time-delay distance vs $z_\\mathrm{lens}$")
    ax.legend()
    fig.tight_layout()
    out = FIG_DIR / "tdelay_D_dt_vs_zl.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    fig_H0_anchors()
    fig_D_dt_vs_zl()
