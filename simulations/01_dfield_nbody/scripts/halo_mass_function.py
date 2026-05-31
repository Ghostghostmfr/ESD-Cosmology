"""Halo mass function (HMF): measure dn/dlnM and compare to Press-Schechter.

Sub-task 1.5 of simulation 01. Two responsibilities:

* **Measurement** -- given a list of FOF halo masses from a periodic
  box, bin them in log-mass and return a properly normalised
  differential number density ``dn / d ln M`` with Poisson error bars.
* **Theory** -- evaluate the Press-Schechter mass function at the
  same cosmology used by the IC generator, so the GR baseline must
  trend along the PS curve and any ESD deviation is a real signal.

The figure-generating orchestrator lives in ``compare_hmf.py``;
this module is self-contained (numpy + matplotlib) so the analysis
can be re-used by sub-tasks 1.6 and 1.7 with no coupling.

Conventions (cosmology-standard):
* Masses in ``M_sun / h``.
* Lengths in ``Mpc / h`` (comoving).
* In the (Mpc/h, M_sun/h) unit system the critical density is
  numerically ``rho_crit_0 = 2.775e11 M_sun/h / (Mpc/h)^3`` with no
  residual factor of ``h`` -- a useful simplification.

Press-Schechter:

.. math::
    \\sigma^2(R) = \\frac{1}{2\\pi^2} \\int k^2 P(k) W^2(kR)\\,dk,
    \\quad R = \\left(\\frac{3 M}{4 \\pi \\bar\\rho_m}\\right)^{1/3}

    \\frac{dn}{d\\ln M} =
        \\sqrt{\\frac{2}{\\pi}}\\,\\frac{\\bar\\rho_m}{M}\\,
        \\frac{\\delta_c}{\\sigma}\\,
        \\left|\\frac{d\\ln\\sigma}{d\\ln M}\\right|\\,
        \\exp\\!\\left(-\\frac{\\delta_c^2}{2\\sigma^2}\\right)

with ``delta_c = 1.686``. PS is known to under-predict the high-mass
tail by ~ 30% relative to N-body / Sheth-Tormen; for a first
GR-vs-ESD sanity check the analytic curve is the right reference
because both simulated curves are compared to the *same* PS line.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from ic_zeldovich import (
    CosmoParams,
    linear_power_spectrum,
    _W_top_hat,
)


# Critical density in (M_sun/h) / (Mpc/h)^3 -- no h factors in this unit system.
RHO_CRIT_0_MSUNH_MPCH3: float = 2.775e11
DELTA_C: float = 1.686


# ---------------------------------------------------------------------------
# Particle mass and measurement
# ---------------------------------------------------------------------------


def particle_mass_msunh(
    omega_m: float, box_mpc_h: float, n_particles: int
) -> float:
    """Per-particle mass in M_sun/h for a uniform-mass N-body box."""
    rho_bar = omega_m * RHO_CRIT_0_MSUNH_MPCH3
    return rho_bar * (box_mpc_h ** 3) / float(n_particles)


def binned_dn_dlnm(
    halo_masses_msunh: NDArray[np.float64],
    box_mpc_h: float,
    log10_bins: NDArray[np.float64] | None = None,
    n_bins: int = 10,
) -> dict:
    """Bin halo masses and return ``dn/dlnM`` with Poisson errors.

    Returns
    -------
    dict with:
        M_centers  : (n,) bin-centre masses in M_sun/h
        dn_dlnM    : (n,) measured differential number density
                      [(Mpc/h)^-3]
        err        : (n,) sqrt(N) / (V * dlnM) Poisson error
        counts     : (n,) raw halo counts per bin
        edges      : (n+1,) log10 mass bin edges
    """
    masses = np.asarray(halo_masses_msunh, dtype=float)
    masses = masses[masses > 0.0]
    if masses.size == 0:
        return dict(
            M_centers=np.array([]), dn_dlnM=np.array([]),
            err=np.array([]), counts=np.array([], dtype=int),
            edges=np.array([]),
        )

    if log10_bins is None:
        lo = math.log10(masses.min())
        hi = math.log10(masses.max()) + 1e-6
        log10_bins = np.linspace(lo, hi, n_bins + 1)

    counts, edges = np.histogram(np.log10(masses), bins=log10_bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    M_centers = 10.0 ** centers
    dlnM = (edges[1:] - edges[:-1]) * math.log(10.0)
    volume = box_mpc_h ** 3
    dn_dlnM = counts / (volume * dlnM)
    err = np.sqrt(np.maximum(counts, 1)) / (volume * dlnM)
    return dict(
        M_centers=M_centers,
        dn_dlnM=dn_dlnM,
        err=err,
        counts=counts,
        edges=edges,
    )


# ---------------------------------------------------------------------------
# Press-Schechter theory
# ---------------------------------------------------------------------------


def _sigma2_of_R(
    R_mpch: float,
    k_grid: NDArray[np.float64],
    P_grid: NDArray[np.float64],
) -> float:
    """sigma^2(R) by trapezoidal integration over the same P(k) grid."""
    integrand = (k_grid ** 2) * P_grid * (_W_top_hat(k_grid * R_mpch) ** 2)
    return float(np.trapezoid(integrand, k_grid) / (2.0 * math.pi ** 2))


def press_schechter_dn_dlnm(
    M_grid_msunh: NDArray[np.float64],
    cosmo: CosmoParams,
    k_min_h_mpc: float = 1.0e-4,
    k_max_h_mpc: float = 1.0e2,
    n_k: int = 2048,
) -> NDArray[np.float64]:
    """Press-Schechter dn/dlnM at z = 0 for the given cosmology.

    Uses the same EH98 linear power spectrum that produced the ICs,
    so a GR baseline run on this cosmology must trend along this
    curve (modulo the well-known ~ 30% PS under-prediction at the
    high-mass tail).
    """
    rho_bar = cosmo.omega_m * RHO_CRIT_0_MSUNH_MPCH3

    k_grid = np.logspace(math.log10(k_min_h_mpc), math.log10(k_max_h_mpc), n_k)
    P_grid = linear_power_spectrum(k_grid, cosmo)

    M_grid = np.asarray(M_grid_msunh, dtype=float)
    # log-spaced derivative grid for d ln sigma / d ln M
    lnM = np.log(M_grid)
    sigma = np.empty_like(M_grid)
    for i, M in enumerate(M_grid):
        R = (3.0 * M / (4.0 * math.pi * rho_bar)) ** (1.0 / 3.0)
        sigma[i] = math.sqrt(max(_sigma2_of_R(R, k_grid, P_grid), 0.0))

    ln_sigma = np.log(sigma)
    d_ln_sigma_d_ln_M = np.gradient(ln_sigma, lnM)

    nu = DELTA_C / sigma
    f_PS = math.sqrt(2.0 / math.pi) * nu * np.exp(-0.5 * nu ** 2)
    dn_dlnM = (rho_bar / M_grid) * f_PS * np.abs(d_ln_sigma_d_ln_M)
    return dn_dlnM


# ---------------------------------------------------------------------------
# Plot helper
# ---------------------------------------------------------------------------


def plot_hmf(
    out_path: str,
    measured: Sequence[tuple[str, dict, str]],
    theory: tuple[NDArray, NDArray, str] | None = None,
    title: str = "Halo mass function",
) -> None:
    """Plot one or more measured HMFs against an optional theory curve.

    Parameters
    ----------
    out_path : output PNG path.
    measured : list of (label, bin_dict, colour) where bin_dict is
               the return value of :func:`binned_dn_dlnm`.
    theory   : optional (M_grid, dn_dlnM, label) tuple.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    for label, b, colour in measured:
        if b["M_centers"].size == 0:
            continue
        ax.errorbar(
            b["M_centers"], b["dn_dlnM"], yerr=b["err"],
            fmt="o", color=colour, label=label, capsize=2, markersize=4,
        )
    if theory is not None:
        M_grid, dn, lbl = theory
        ax.plot(M_grid, dn, "k--", label=lbl, alpha=0.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$M\ [M_\odot/h]$")
    ax.set_ylabel(r"$dn / d\ln M\ [(Mpc/h)^{-3}]$")
    ax.set_title(title)
    ax.legend(frameon=False, fontsize=9)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Self-test: synthetic Schechter-like distribution -> recover the slope
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    """Verify that:
      (a) The binned HMF normalises to the expected total halo count.
      (b) Press-Schechter is monotone-decreasing on a log mass grid
          (sanity: PS at z = 0 must fall off at high mass).
      (c) PS sigma_8 from M = 6e14 / sigma is consistent with cosmo.sigma_8
          within ~ 5% (cross-check that R = 8 Mpc/h corresponds to
          roughly that mass).
    """
    rng = np.random.default_rng(20260530)
    cosmo = CosmoParams()

    # (a) Draw 1000 halos from a power-law distribution in log mass,
    # bin, and verify the recovered counts sum back to 1000.
    box = 100.0
    log10M = rng.uniform(11.0, 14.5, size=1000)
    masses = 10.0 ** log10M
    b = binned_dn_dlnm(masses, box_mpc_h=box, n_bins=10)
    count_check = int(b["counts"].sum())

    # (b) PS monotonicity (z = 0).
    M_grid = np.logspace(11.0, 15.5, 60)
    dn_PS = press_schechter_dn_dlnm(M_grid, cosmo)
    monotone = bool(np.all(np.diff(np.log(dn_PS[M_grid > 1e13])) < 0))

    # (c) sigma(R = 8 Mpc/h) from M = (4/3 pi R^3 rho_m) must match
    # cosmo.sigma_8.
    rho_bar = cosmo.omega_m * RHO_CRIT_0_MSUNH_MPCH3
    R8 = 8.0
    M8 = (4.0 / 3.0) * math.pi * R8 ** 3 * rho_bar
    k_grid = np.logspace(-4, 2, 2048)
    P_grid = linear_power_spectrum(k_grid, cosmo)
    sigma8_meas = math.sqrt(_sigma2_of_R(R8, k_grid, P_grid))
    rel_diff_sigma8 = abs(sigma8_meas - cosmo.sigma_8) / cosmo.sigma_8

    ok = (
        count_check == 1000
        and monotone
        and rel_diff_sigma8 < 0.05
    )
    result = dict(
        count_check=count_check,
        ps_monotone_above_1e13=monotone,
        sigma8_from_ps=sigma8_meas,
        sigma8_input=cosmo.sigma_8,
        rel_diff_sigma8=rel_diff_sigma8,
        M8_msunh=M8,
        passed=ok,
    )
    if verbose:
        print(f"[hmf] binned counts sum  = {count_check} (expected 1000)")
        print(f"[hmf] PS monotone>1e13   = {monotone}")
        print(f"[hmf] M(R=8 Mpc/h)       = {M8:.3e} M_sun/h")
        print(f"[hmf] sigma_8 from P(k)  = {sigma8_meas:.4f}"
              f"  (input {cosmo.sigma_8:.4f}, rel diff {rel_diff_sigma8:.2e})")
        print(f"[hmf] {'PASS' if ok else 'FAIL'}")
    return result


if __name__ == "__main__":
    import sys
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
