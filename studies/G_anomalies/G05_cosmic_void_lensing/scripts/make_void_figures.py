"""Study 30 figures: ESD vs LCDM void density and lensing profiles."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from esd_void import hsw_profile, esd_profile_parameters, R_FLOOR, AMP_FLOOR
from void_data import (
    DES_Y3_DELTA_SIGMA_PEAK, DES_Y3_DELTA_SIGMA_SIGMA,
    DES_Y3_R_OVER_RV_PEAK,
)

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def fig_density_profile():
    p = esd_profile_parameters(delta_c_lcdm=-0.825, wall_amp_lcdm=0.06)
    r = np.linspace(0.05, 2.5, 400)
    lcdm = np.array([hsw_profile(x, p["delta_c_lcdm"], p["wall_amp_lcdm"])
                     for x in r])
    esd = np.array([hsw_profile(x, p["delta_c_esd"], p["wall_amp_esd"])
                    for x in r])

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(r, lcdm, "k--", lw=1.8, label="LCDM (HSW mid-range)")
    ax.plot(r, esd, "C3-", lw=2.2,
            label=f"ESD (amp_D = {p['amp_D_interior']:.2f}, "
                  f"amp_E = {p['amp_E_wall']:.2f}, cap at $\\delta=-1$)")
    ax.axhline(0.0, color="0.5", lw=0.6)
    ax.axvline(1.0, color="0.7", lw=0.6, ls=":")
    ax.set_xlabel(r"$r / R_v$")
    ax.set_ylabel(r"$\delta(r)$")
    ax.set_title("Study 30 - void density profile, ESD vs LCDM")
    ax.legend(loc="lower right")
    ax.set_xlim(0.0, 2.5)
    fig.tight_layout()
    out = FIG_DIR / "void_density_profile.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


def fig_lensing_compare():
    from esd_void import delta_sigma_peak
    p = esd_profile_parameters(delta_c_lcdm=-0.825, wall_amp_lcdm=0.06)
    ds_esd = delta_sigma_peak(p["delta_c_esd"], p["wall_amp_esd"])
    ds_lcdm = delta_sigma_peak(p["delta_c_lcdm"], p["wall_amp_lcdm"])

    labels = ["LCDM (HSW)", "ESD (s/c floor)", "DES Y3"]
    vals = [ds_lcdm, ds_esd, DES_Y3_DELTA_SIGMA_PEAK]
    errs = [0.0, 0.0, DES_Y3_DELTA_SIGMA_SIGMA]

    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    ax.bar(labels, vals, yerr=errs, color=["0.4", "C3", "C0"],
           edgecolor="k", capsize=6)
    ax.axhline(0.0, color="0.5", lw=0.6)
    ax.set_ylabel(r"$\Delta\Sigma_t$  at  $R/R_v \approx 1$  "
                  r"[$h\,M_\odot/\mathrm{pc}^2$]")
    ax.set_title("Study 30 - void tangential shear peak amplitude")
    fig.tight_layout()
    out = FIG_DIR / "void_lensing_compare.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    fig_density_profile()
    fig_lensing_compare()
