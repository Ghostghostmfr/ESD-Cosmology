"""
Figures for Study 23: NANOGrav 15-yr stochastic GW background audit.

Generates two figures using only the published headline values from
Agazie et al. 2023 (ApJL 951 L8) and the ESD GW-sector predictions
(see `esd_gw.py`):

  fig_hellings_downs.png
    Theoretical Hellings-Downs ORF (ESD = GR tensor) versus the
    monopole (scalar-breathing-like) and dipole (vector-like)
    overlap reduction functions, demonstrating that the HD pattern
    that NANOGrav reports is the unique tensor signature.

  fig_spectral_consistency.png
    Gaussian approximation to the published HD-correlated posterior
    on the spectral index gamma, overlaid with the GW-driven SMBHB
    theoretical value gamma = 13/3 and the +/-1, +/-3 sigma bands.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow `python scripts/make_nanograv_figures.py` from the study root.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.esd_gw import SMBHB_EXPECTED_GAMMA, hellings_downs_tensor  # noqa: E402
from scripts.observations import NANOGRAV_15YR_SPECTRAL  # noqa: E402

FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures_generated"


def _monopole_orf(theta_rad: np.ndarray) -> np.ndarray:
    """Overlap reduction function for an isotropic monopole-correlated
    process: constant 0.5 (matches the HD self-correlation normalization
    at zero separation when pulsar term is excluded)."""
    return 0.5 * np.ones_like(theta_rad)


def _dipole_orf(theta_rad: np.ndarray) -> np.ndarray:
    """Overlap reduction function for a dipole-correlated process:
    proportional to cos(theta)."""
    return 0.5 * np.cos(theta_rad)


def make_hellings_downs_figure() -> Path:
    theta_deg = np.linspace(1.0, 179.0, 400)
    theta_rad = np.deg2rad(theta_deg)

    hd = hellings_downs_tensor(theta_rad)
    mono = _monopole_orf(theta_rad)
    dipo = _dipole_orf(theta_rad)

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.axhline(0.0, color="0.7", lw=0.8)
    ax.plot(theta_deg, hd, color="C0", lw=2.2,
            label="Hellings-Downs (tensor; ESD = GR)")
    ax.plot(theta_deg, mono, color="C3", lw=1.4, ls="--",
            label="Monopole-correlated")
    ax.plot(theta_deg, dipo, color="C2", lw=1.4, ls=":",
            label="Dipole-correlated")

    ax.set_xlabel("Pulsar pair angular separation  $\\theta$  [deg]")
    ax.set_ylabel("Overlap reduction function  $\\Gamma(\\theta)$")
    ax.set_xlim(0, 180)
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180])
    ax.set_title("Study 23 - ORF predictions: tensor vs alternatives")
    ax.legend(loc="lower left", frameon=False)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()

    out = FIGURES_DIR / "fig_hellings_downs.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def make_spectral_consistency_figure() -> Path:
    obs = NANOGRAV_15YR_SPECTRAL
    theory = SMBHB_EXPECTED_GAMMA

    gamma_grid = np.linspace(0.5, 7.0, 600)
    # Gaussian approximation to the published 1-D marginal posterior.
    posterior = np.exp(
        -0.5 * ((gamma_grid - obs.gamma_median) / obs.gamma_sigma) ** 2
    ) / (obs.gamma_sigma * np.sqrt(2.0 * np.pi))

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.fill_between(gamma_grid, 0, posterior, color="C0", alpha=0.25,
                    label="NANOGrav 15-yr posterior\n(Gaussian approx.)")
    ax.plot(gamma_grid, posterior, color="C0", lw=1.8)

    # 1-sigma and 3-sigma bands around the observation.
    for n_sig, alpha in ((1, 0.28), (3, 0.12)):
        ax.axvspan(obs.gamma_median - n_sig * obs.gamma_sigma,
                   obs.gamma_median + n_sig * obs.gamma_sigma,
                   color="C0", alpha=alpha, lw=0,
                   label=f"+/- {n_sig}$\\sigma$ band" if n_sig in (1, 3) else None)

    ax.axvline(theory, color="C3", lw=2.0,
               label=f"SMBHB theory  $\\gamma = 13/3 \\approx {theory:.3f}$")
    ax.axvline(obs.gamma_median, color="C0", lw=1.2, ls="--",
               label=f"observed median = {obs.gamma_median:.2f}")

    tension = abs(obs.gamma_median - theory) / obs.gamma_sigma
    ax.set_title(
        f"Study 23 - spectral index consistency  "
        f"(tension = {tension:.2f}$\\sigma$)"
    )
    ax.set_xlabel("Spectral index  $\\gamma$  "
                  "(with $h_c^2(f) \\propto f^{-\\gamma}$)")
    ax.set_ylabel("Posterior density")
    ax.set_xlim(gamma_grid.min(), gamma_grid.max())
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()

    out = FIGURES_DIR / "fig_spectral_consistency.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def main() -> int:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    hd_path = make_hellings_downs_figure()
    sp_path = make_spectral_consistency_figure()
    print(f"wrote {hd_path}")
    print(f"wrote {sp_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
