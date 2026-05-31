"""Two-point correlation function xi(r) for a periodic-box particle set.

Sub-task 1.6 of simulation 01. For a periodic box the natural
estimator is via the matter power spectrum and the Wiener-Khinchin
theorem:

    delta_k         = FFT(delta(x))
    P(k)            = |delta_k|^2 / V_box                  [Mpc/h^3]
    xi(x)           = IFFT(P(k))                           (per cell)

which is O(N_grid^3 log N_grid) rather than the O(N_part^2) of
direct pair counting. We CIC the particles to a grid, FFT, take
|delta_k|^2, IFFT back to real space, and bin xi(x) into spherical
radial bins.

Theory comparison uses the analytic linear-theory transform:

    xi_lin(r) = (1 / 2 pi^2) * integral{ k^2 P_lin(k) j_0(k r) dk }

with j_0(x) = sin(x) / x and P_lin from the same EH98 power
spectrum that generated the ICs.

The module is self-testing: a Poisson-random particle distribution
must give xi ~ 0 within shot noise, and a sinusoidal periodic
density perturbation must give xi(r) ~ A^2/2 cos(k0 r) with the
right amplitude and wavelength.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from run_sim import cic_assign
from ic_zeldovich import CosmoParams, linear_power_spectrum


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------


def measure_xi_periodic(
    positions_mpc_h: NDArray[np.float64],
    box_mpc_h: float,
    n_grid: int,
    r_bins_mpc_h: NDArray[np.float64],
) -> dict:
    """Return binned xi(r) for periodic particles via FFT.

    Parameters
    ----------
    positions_mpc_h : (N, 3) particle positions in Mpc/h (will be
                      normalised to [0, 1) for the existing CIC).
    box_mpc_h       : physical box side length.
    n_grid          : mesh size for CIC + FFT.
    r_bins_mpc_h    : monotonic edges of radial bins, in Mpc/h.

    Returns
    -------
    dict with:
        r_centers : (nb,) bin midpoints in Mpc/h
        xi        : (nb,) measured correlation
        n_pairs   : (nb,) cell-pair count contributing to each bin
    """
    pos_code = (positions_mpc_h / box_mpc_h) % 1.0
    rho = cic_assign(pos_code, n_grid)
    delta = rho / rho.mean() - 1.0

    delta_k = np.fft.rfftn(delta, axes=(0, 1, 2))
    power = (np.abs(delta_k) ** 2)
    # Inverse FFT of the power spectrum gives the discrete
    # autocorrelation per cell-shift; divide by N to get the
    # field-averaged xi(displacement).
    xi_grid = np.fft.irfftn(power, s=delta.shape, axes=(0, 1, 2)) / delta.size

    cell = box_mpc_h / n_grid
    ax = np.arange(n_grid)
    ax = np.where(ax > n_grid // 2, ax - n_grid, ax)        # signed offset
    Xs, Ys, Zs = np.meshgrid(ax, ax, ax, indexing="ij")
    r_grid = cell * np.sqrt(Xs * Xs + Ys * Ys + Zs * Zs)
    r_flat = r_grid.ravel()
    xi_flat = xi_grid.ravel()

    nb = len(r_bins_mpc_h) - 1
    xi_binned = np.zeros(nb, dtype=float)
    n_pairs = np.zeros(nb, dtype=np.int64)
    for i in range(nb):
        m = (r_flat >= r_bins_mpc_h[i]) & (r_flat < r_bins_mpc_h[i + 1])
        if m.any():
            xi_binned[i] = float(xi_flat[m].mean())
            n_pairs[i] = int(m.sum())
        else:
            xi_binned[i] = np.nan
    r_centers = 0.5 * (r_bins_mpc_h[1:] + r_bins_mpc_h[:-1])
    return dict(r_centers=r_centers, xi=xi_binned, n_pairs=n_pairs)


# ---------------------------------------------------------------------------
# Linear theory
# ---------------------------------------------------------------------------


def linear_xi(
    r_grid_mpc_h: NDArray[np.float64],
    cosmo: CosmoParams,
    growth_factor: float = 1.0,
    k_min_h_mpc: float = 1.0e-4,
    k_max_h_mpc: float = 1.0e2,
    n_k: int = 4096,
) -> NDArray[np.float64]:
    """Linear xi(r) from the EH98 P(k), at a given growth factor."""
    k_grid = np.logspace(math.log10(k_min_h_mpc), math.log10(k_max_h_mpc), n_k)
    P_grid = (growth_factor ** 2) * linear_power_spectrum(k_grid, cosmo)
    xi = np.empty_like(r_grid_mpc_h)
    for i, r in enumerate(r_grid_mpc_h):
        kr = k_grid * r
        # j_0(kr) = sin(kr)/(kr); use safe handling near 0
        j0 = np.where(kr > 0, np.sin(kr) / np.where(kr > 0, kr, 1.0), 1.0)
        integrand = (k_grid ** 2) * P_grid * j0
        xi[i] = float(np.trapezoid(integrand, k_grid)) / (2.0 * math.pi ** 2)
    return xi


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------


def plot_xi(
    out_path: str,
    measured: Sequence[tuple[str, dict, str]],
    theory: tuple[NDArray, NDArray, str] | None = None,
    title: str = "Two-point correlation",
) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    for label, b, colour in measured:
        r = b["r_centers"]
        xi = b["xi"]
        m = np.isfinite(xi) & (xi > 0)
        ax.plot(r[m], xi[m], "o-", color=colour, label=label, markersize=4)
        m_neg = np.isfinite(xi) & (xi < 0)
        if m_neg.any():
            ax.plot(r[m_neg], np.abs(xi[m_neg]), "x", color=colour,
                    label=f"{label} (xi<0)", markersize=4)
    if theory is not None:
        r, xi_th, lbl = theory
        m = xi_th > 0
        ax.plot(r[m], xi_th[m], "k--", label=lbl, alpha=0.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$r\ [Mpc/h]$")
    ax.set_ylabel(r"$|\xi(r)|$")
    ax.set_title(title)
    ax.legend(frameon=False, fontsize=9)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    """Two checks:
        (a) Poisson-random particles  -> xi ~ 0 within shot noise.
        (b) Planted sinusoidal mode at k0 -> xi(r) = (A^2/2) cos(k0 r).
    """
    rng = np.random.default_rng(20260530)
    box = 100.0
    n_grid = 64
    n_part = n_grid ** 3
    r_bins = np.linspace(2.0, 30.0, 15)

    # (a) Poisson
    pos_random = rng.uniform(0.0, box, size=(n_part, 3))
    out_a = measure_xi_periodic(pos_random, box, n_grid, r_bins)
    # Shot-noise floor for xi at scale r is roughly 1/(N_pairs * n_bar)
    # but in the FFT estimator the dominant noise is just sigma_xi ~ 1/sqrt(N_modes_per_bin).
    # We require |xi| < 0.02 across all bins.
    max_abs_xi_poisson = float(np.nanmax(np.abs(out_a["xi"])))
    poisson_ok = max_abs_xi_poisson < 0.02

    # (b) Planted plane wave with wavevector k0 = (2 pi / L) * (2, 0, 0).
    # Resulting density: delta(x) = A * cos(k0 . x).
    # The 3D autocorrelation is (A^2/2) cos(k0 r_x). Our estimator
    # spherically bins by |r|, so the prediction is the angular
    # average over a sphere:
    #     xi_binned(r) = (A^2/2) * j_0(k0 r) = (A^2/2) sin(k0 r)/(k0 r)
    n_side = n_grid                                  # match grid for clean signal
    lin = (np.arange(n_side) + 0.5) / n_side * box
    X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")
    A = 0.2
    nmode = 2
    k0 = 2.0 * math.pi * nmode / box
    # Displace Lagrangian particles to make delta = A cos(k0 x).
    # Use the Zel'dovich-style relation s = -(A/k0) sin(k0 x) (linear approx).
    disp = -(A / k0) * np.sin(k0 * X)
    pos_wave = np.stack(
        [(X + disp).ravel(), Y.ravel(), Z.ravel()], axis=1
    ) % box
    out_b = measure_xi_periodic(pos_wave, box, n_grid, r_bins)
    r = out_b["r_centers"]
    xi_meas = out_b["xi"]
    kr = k0 * r
    j0 = np.where(kr > 0, np.sin(kr) / np.where(kr > 0, kr, 1.0), 1.0)
    xi_pred = (A ** 2 / 2.0) * j0
    # Compare where the prediction is not too small (avoid divide-by-near-zero).
    finite = np.isfinite(xi_meas) & (np.abs(xi_pred) > 1.0e-4)
    rel_err = (
        float(np.max(np.abs((xi_meas - xi_pred)[finite] / xi_pred[finite])))
        if finite.any() else float("inf")
    )
    wave_ok = rel_err < 0.25

    ok = poisson_ok and wave_ok
    result = dict(
        max_abs_xi_poisson=max_abs_xi_poisson,
        wave_max_rel_err=float(rel_err),
        passed=bool(ok),
    )
    if verbose:
        print(f"[xi] Poisson  max |xi|       = {max_abs_xi_poisson:.3e}"
              f"  (must be < 0.02)")
        print(f"[xi] plane-wave max rel err  = {rel_err:.3e}"
              f"  (must be < 0.25)")
        print(f"[xi] {'PASS' if ok else 'FAIL'}")
    return result


if __name__ == "__main__":
    import sys
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
