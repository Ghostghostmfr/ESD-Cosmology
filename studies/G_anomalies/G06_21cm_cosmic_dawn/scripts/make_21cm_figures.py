"""Study 32 figures: ESD 21cm prediction vs EDGES / SARAS-3 / LCDM."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from edges_data import (
    Z_COSMIC_DAWN,
    T_B_LCDM_CENTRAL_MK, T_B_LCDM_SIGMA_MK,
    T_B_EDGES_MK, T_B_EDGES_SIGMA_PLUS_MK, T_B_EDGES_SIGMA_MINUS_MK,
    T_B_SARAS3_UPPER_MK, T_B_SARAS3_LOWER_MK,
)
from esd_21cm import T_b_esd_mK, T_gas_adiabatic_K, T_CMB_z_K

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def fig_Tb_anchors():
    tb_fid    = T_b_esd_mK(wf_coupling_fraction=1.0, f_X=1.0)["T_b_mK"]
    tb_deep   = T_b_esd_mK(wf_coupling_fraction=1.0, f_X=0.0)["T_b_mK"]

    labels = ["EDGES\nBowman+18",
              "LCDM std\n(Pritchard-Loeb)",
              "ESD fiducial\n(full WF, X-ray)",
              "ESD max-depth\n(no X-ray)",
              "SARAS-3\n95% envelope"]
    vals = [T_B_EDGES_MK, T_B_LCDM_CENTRAL_MK, tb_fid, tb_deep,
            0.5 * (T_B_SARAS3_LOWER_MK + T_B_SARAS3_UPPER_MK)]
    err_low = [T_B_EDGES_SIGMA_MINUS_MK, T_B_LCDM_SIGMA_MK, 0, 0,
               0.5 * (T_B_SARAS3_UPPER_MK - T_B_SARAS3_LOWER_MK)]
    err_high = [T_B_EDGES_SIGMA_PLUS_MK, T_B_LCDM_SIGMA_MK, 0, 0,
                0.5 * (T_B_SARAS3_UPPER_MK - T_B_SARAS3_LOWER_MK)]
    colors = ["C3", "0.4", "C2", "C2", "C0"]

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    y = np.arange(len(labels))
    for yi, v, lo, hi, c in zip(y, vals, err_low, err_high, colors):
        ax.errorbar([v], [yi], xerr=[[lo], [hi]], fmt="o",
                    color=c, ecolor="0.3", capsize=4, ms=8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.axvspan(T_B_SARAS3_LOWER_MK, T_B_SARAS3_UPPER_MK,
               color="C0", alpha=0.08, label="SARAS-3 envelope")
    ax.axvline(0, color="0.5", lw=0.6)
    ax.set_xlabel(r"$T_b$  at  $z \approx 17$  [mK]")
    ax.set_title("Study 32 - 21cm cosmic-dawn brightness temperature")
    ax.legend(loc="lower left")
    fig.tight_layout()
    out = FIG_DIR / "21cm_Tb_anchors.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


def fig_Tb_vs_z():
    z_grid = np.linspace(8.0, 25.0, 120)
    tb = np.array([T_b_esd_mK(z=zi, wf_coupling_fraction=1.0, f_X=1.0)["T_b_mK"]
                   for zi in z_grid])
    T_gas = np.array([T_gas_adiabatic_K(zi) for zi in z_grid])
    T_cmb = np.array([T_CMB_z_K(zi) for zi in z_grid])

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0))

    axes[0].plot(z_grid, T_cmb, "C0-", lw=1.6, label=r"$T_\mathrm{CMB}(z)$")
    axes[0].plot(z_grid, T_gas, "C3-", lw=1.6, label=r"$T_\mathrm{gas}$ adiabatic")
    axes[0].set_yscale("log")
    axes[0].set_xlabel(r"$z$")
    axes[0].set_ylabel("temperature [K]")
    axes[0].legend()
    axes[0].set_title("IGM temperatures vs $z$")

    axes[1].plot(z_grid, tb, "C2-", lw=2.0, label="ESD T_b (full WF)")
    axes[1].errorbar([17.19], [T_B_EDGES_MK],
                     yerr=[[T_B_EDGES_SIGMA_MINUS_MK],
                           [T_B_EDGES_SIGMA_PLUS_MK]],
                     fmt="s", color="C3", capsize=4, ms=7,
                     label="EDGES Bowman+18")
    axes[1].errorbar([17.19], [T_B_LCDM_CENTRAL_MK],
                     yerr=[[T_B_LCDM_SIGMA_MK], [T_B_LCDM_SIGMA_MK]],
                     fmt="o", color="0.3", capsize=4, ms=7,
                     label="LCDM std")
    axes[1].axhspan(T_B_SARAS3_LOWER_MK, T_B_SARAS3_UPPER_MK,
                    color="C0", alpha=0.08, label="SARAS-3 95%")
    axes[1].axhline(0, color="0.5", lw=0.6)
    axes[1].set_xlabel(r"$z$")
    axes[1].set_ylabel(r"$T_b$  [mK]")
    axes[1].legend(loc="lower right", fontsize=9)
    axes[1].set_title("21cm signal vs $z$")

    fig.tight_layout()
    out = FIG_DIR / "21cm_Tb_vs_z.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    fig_Tb_anchors()
    fig_Tb_vs_z()
