"""Figures for Study 34: E_G(z) prediction vs measurements."""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from eg_data import EG_MEASUREMENTS
from esd_eg import E_G_esd_linear, E_G_esd_with_halo_correction

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    z_grid = np.linspace(0.0, 1.2, 200)
    eg_lin = np.array([E_G_esd_linear(z) for z in z_grid])
    eg_k10 = np.array([E_G_esd_with_halo_correction(z, 0.10) for z in z_grid])
    eg_k30 = np.array([E_G_esd_with_halo_correction(z, 0.30) for z in z_grid])

    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    ax.plot(z_grid, eg_lin, color="black", lw=2,
            label=r"ESD = $\Lambda$CDM (linear): $\Omega_m/f(z)$")
    ax.plot(z_grid, eg_k10, color="C0", lw=1.2, ls="--",
            label=r"ESD with halo correction at $k = 0.10\,h/$Mpc")
    ax.plot(z_grid, eg_k30, color="C3", lw=1.2, ls=":",
            label=r"ESD with halo correction at $k = 0.30\,h/$Mpc")

    for z, eg, sig, label, _cite in EG_MEASUREMENTS:
        ax.errorbar(z, eg, yerr=sig, fmt="o", capsize=3, ms=5,
                    label=label)
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"$E_G(z)$")
    ax.set_title(r"Study 34 — $E_G(z)$: ESD prediction vs published measurements")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=8, ncol=2)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 0.7)
    plt.tight_layout()
    out = FIG_DIR / "eg_vs_z.png"
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
