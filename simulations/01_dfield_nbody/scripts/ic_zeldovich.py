"""Zel'dovich-approximation initial conditions for the ESD N-body sim.

Sub-task 1.3 of simulation 01. Generates a Gaussian random matter
realization from the Eisenstein-Hu '98 no-wiggle linear transfer
function (the canonical analytic baseline for cosmological N-body
IC generators like NGENIC, MUSIC, and 2LPTic), normalized to the
Planck sigma_8.

All cosmological constants come from ``esd_core``:
    Omega_m = OMEGA_M_LOCK        (Identity-B locked, Paper 1)
    Omega_b = OMEGA_B_LOCK        (closure-pool)
    n_s     = NS_STAR             (primordial tilt)
The Hubble parameter, sigma_8, and T_CMB are SM inputs taken at
their Planck 2018 baseline values.

Per Study 19, the linear growth at IC time is *identical* to LCDM
(R(u) does not modify linear growth). So a standard EH98-based IC
is the correct framework-faithful starting point — the ESD signal
only appears later, after virialization, gated by Study 1.2a.

Code-unit convention (matches run_sim.py)
-----------------------------------------
* Positions in [0, 1) (periodic box of side L_box_mpc_h Mpc/h)
* Canonical momentum p = a^2 dx/dt with H0 = 1 (so time has units
  of inverse Hubble); only ratios H(a)/H0 ever appear.

The PM solver's Poisson source ``-1.5 * omega_m * delta / a`` is
written in these same code units, so positions/momenta produced
here drop in directly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from esd_core import NS_STAR, OMEGA_B_LOCK, OMEGA_M_LOCK


# ---------------------------------------------------------------------------
# Cosmology container
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CosmoParams:
    """Cosmological parameters for IC generation (Planck 2018 baseline)."""

    omega_m: float = float(OMEGA_M_LOCK)
    omega_b: float = float(OMEGA_B_LOCK)
    h:       float = 0.6736             # H0 = 100 h km/s/Mpc
    n_s:     float = float(NS_STAR)
    sigma_8: float = 0.8111             # Planck 2018 baseline; matches Study 24
    T_cmb:   float = 2.7255             # K


# ---------------------------------------------------------------------------
# Eisenstein & Hu 1998 no-wiggle transfer function
# ---------------------------------------------------------------------------


def eh98_nowiggle_transfer(
    k_h_per_mpc: NDArray[np.float64], cosmo: CosmoParams
) -> NDArray[np.float64]:
    """Linear matter transfer T(k), Eisenstein & Hu 1998 no-wiggle form.

    Input k in h/Mpc. Returns T(k), dimensionless, normalised to 1 at k -> 0.

    Reference: Eisenstein & Hu 1998 ApJ 496, 605, Eqs. (28)-(31)
    (the "no baryon acoustic oscillations" approximation; the BAO
    wiggles are a sub-percent perturbation that we'll fold in only
    if/when a future sub-task needs explicit BAO in the IC).
    """
    # Convert k to Mpc^-1 (EH98 internal units).
    k = k_h_per_mpc * cosmo.h

    om = cosmo.omega_m
    ob = cosmo.omega_b
    h = cosmo.h
    theta = cosmo.T_cmb / 2.7

    om_h2 = om * h * h
    ob_h2 = ob * h * h
    fb = ob / om

    # Eq. (26): sound horizon at drag epoch
    s = 44.5 * np.log(9.83 / om_h2) / np.sqrt(1.0 + 10.0 * ob_h2**0.75)

    # Eq. (31): no-wiggle alpha
    alpha_gamma = (
        1.0
        - 0.328 * np.log(431.0 * om_h2) * fb
        + 0.38 * np.log(22.3 * om_h2) * fb**2
    )

    # Eq. (30): Gamma_eff(k)
    ks = k * s / h                        # k * (s in Mpc), with k in Mpc^-1
    gamma_eff = om * h * (
        alpha_gamma + (1.0 - alpha_gamma) / (1.0 + (0.43 * ks) ** 4)
    )

    # Eq. (28)-(29): q and T0
    q = k * theta * theta / gamma_eff     # k in Mpc^-1
    L0 = np.log(2.0 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    T = L0 / (L0 + C0 * q * q)
    return T


def linear_power_spectrum(
    k_h_per_mpc: NDArray[np.float64], cosmo: CosmoParams
) -> NDArray[np.float64]:
    """Linear matter power spectrum P(k) in (Mpc/h)^3, sigma_8 normalised.

    P(k) = A * k^n_s * T(k)^2 with the amplitude A fixed by sigma_8.
    """
    T = eh98_nowiggle_transfer(k_h_per_mpc, cosmo)
    P_unnormalised = k_h_per_mpc**cosmo.n_s * T * T
    norm = _sigma_R_squared_unnormalised(8.0, cosmo) ** -1 * cosmo.sigma_8**2
    return norm * P_unnormalised


def _W_top_hat(kR: NDArray[np.float64]) -> NDArray[np.float64]:
    """Top-hat window function in Fourier space."""
    x = np.where(kR < 1e-6, 1e-6, kR)
    return 3.0 * (np.sin(x) - x * np.cos(x)) / (x * x * x)


def _sigma_R_squared_unnormalised(R_mpc_h: float, cosmo: CosmoParams) -> float:
    """Unnormalised sigma^2(R) integrated on a log-k grid.

    sigma^2 = (1 / 2 pi^2) integral k^2 P(k) W(kR)^2 dk
    with P(k) = k^n_s T(k)^2 (the un-amplitude-normalised P).
    """
    k = np.logspace(-5.0, 3.0, 4096)     # h/Mpc
    T = eh98_nowiggle_transfer(k, cosmo)
    Pk = k**cosmo.n_s * T * T
    W = _W_top_hat(k * R_mpc_h)
    integrand = k * k * Pk * W * W
    # log integration: integral f(k) dk = integral k f(k) d ln k
    return float(np.trapezoid(integrand * k, np.log(k)) / (2.0 * np.pi**2))


# ---------------------------------------------------------------------------
# Linear growth factor D(a) (delegate to run_sim.py to keep a single source)
# ---------------------------------------------------------------------------


def growth_factor_normalised(a: float, omega_m: float) -> float:
    """D(a) normalised so D(a=1) == 1. Used to scale the z=0 IC to a_init."""
    from run_sim import linear_growth_factor

    a_grid = np.linspace(min(1e-3, a / 10.0), 1.0, 1024)
    D = linear_growth_factor(a_grid, omega_m)
    D /= D[-1]                            # D(a=1) = 1
    return float(np.interp(a, a_grid, D))


# ---------------------------------------------------------------------------
# Zel'dovich initial conditions
# ---------------------------------------------------------------------------


def _k_grid_physical(
    n_grid: int, box_mpc_h: float
) -> tuple[NDArray, NDArray, NDArray, NDArray]:
    """rfft k-grid in physical units of h/Mpc plus its squared magnitude."""
    k_fund = 2.0 * np.pi / box_mpc_h                 # h/Mpc
    kx = k_fund * np.fft.fftfreq(n_grid, d=1.0 / n_grid)
    ky = kx.copy()
    kz = k_fund * np.fft.rfftfreq(n_grid, d=1.0 / n_grid)
    kx3, ky3, kz3 = np.meshgrid(kx, ky, kz, indexing="ij")
    k2 = kx3 * kx3 + ky3 * ky3 + kz3 * kz3
    return kx3, ky3, kz3, k2


def _gaussian_delta_field(
    n_grid: int, box_mpc_h: float, cosmo: CosmoParams, seed: int
) -> NDArray[np.float64]:
    """Generate a Gaussian random delta(x) field with the linear P(k).

    Discrete Fourier convention:
        delta(x) = (1/V) sum_k delta_k exp(i k . x)
    so the variance of delta_k on a periodic grid satisfies
        <|delta_k|^2> = P(k) * V                            (1)
    Equivalently, with numpy's unnormalised rfftn,
        var( rfftn(delta) at mode k ) = P(k) * N_cells^2 / V
                                      = P(k) * N_cells / dV.
    We seed the Fourier modes directly to enforce hermitian symmetry
    cleanly via irfftn.
    """
    rng = np.random.default_rng(seed)
    kx, ky, kz, k2 = _k_grid_physical(n_grid, box_mpc_h)
    k_mag = np.sqrt(k2)
    k_mag_safe = np.where(k_mag == 0.0, 1.0, k_mag)
    Pk = linear_power_spectrum(k_mag_safe, cosmo)
    Pk[0, 0, 0] = 0.0                                # remove DC mode

    V = box_mpc_h**3
    N = n_grid**3

    # Variance of each complex Fourier coefficient (rfftn unnormalised):
    #   <|delta_k|^2> = P(k) * V  in continuum
    #   discrete rfftn coefficient sigma^2 = P(k) * N^2 / V
    sigma = np.sqrt(0.5 * Pk * N * N / V)            # 1/sqrt(2) per Re/Im
    real = rng.standard_normal(k_mag.shape) * sigma
    imag = rng.standard_normal(k_mag.shape) * sigma
    delta_k = real + 1j * imag
    delta_k[0, 0, 0] = 0.0

    # Enforce hermitian symmetry on the Nyquist planes (kz=0 and kz=Nyq).
    # irfftn handles the bulk; the kz=0 plane needs explicit symmetrisation.
    for kz_idx in (0, n_grid // 2):
        plane = delta_k[:, :, kz_idx]
        plane_sym = np.conj(plane[::-1, ::-1])
        # roll by 1 so the (0,0) corner stays fixed
        plane_sym = np.roll(np.roll(plane_sym, 1, axis=0), 1, axis=1)
        delta_k[:, :, kz_idx] = 0.5 * (plane + plane_sym)

    delta = np.fft.irfftn(delta_k, s=(n_grid, n_grid, n_grid), axes=(0, 1, 2))
    return delta


def zeldovich_ic(
    n_part_side: int,
    box_mpc_h: float,
    z_init: float,
    cosmo: CosmoParams,
    seed: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64], dict]:
    """Generate Zel'dovich-approximation initial conditions.

    Returns
    -------
    positions : (N, 3) float, in code units [0, 1).
    momenta   : (N, 3) float, canonical p = a^2 dx/dt in code units.
    info      : dict with the realisation diagnostics (sigma_8 measured
                from the delta grid, displacement RMS, etc.).

    Linear-theory recipe:
        delta_k(z_init)        = D(a_init) * delta_k(z=0)
        psi_k                  = i k delta_k / k^2        (displacement)
        x = q + psi                                       (positions)
        p = a^2 * (f H) * psi                             (momenta)
    """
    a_init = 1.0 / (1.0 + z_init)
    D_init = growth_factor_normalised(a_init, cosmo.omega_m)

    n_grid = n_part_side                              # one particle per cell
    delta_z0 = _gaussian_delta_field(n_grid, box_mpc_h, cosmo, seed)
    delta_init = D_init * delta_z0

    # Displacement field psi from delta on the grid.
    kx, ky, kz, k2 = _k_grid_physical(n_grid, box_mpc_h)
    k2_safe = np.where(k2 == 0.0, 1.0, k2)
    delta_k = np.fft.rfftn(delta_init, axes=(0, 1, 2))
    delta_k[0, 0, 0] = 0.0
    psi_x_k = 1j * kx * delta_k / k2_safe
    psi_y_k = 1j * ky * delta_k / k2_safe
    psi_z_k = 1j * kz * delta_k / k2_safe
    psi_x_k[0, 0, 0] = 0.0
    psi_y_k[0, 0, 0] = 0.0
    psi_z_k[0, 0, 0] = 0.0
    psi_x = np.fft.irfftn(psi_x_k, s=(n_grid, n_grid, n_grid), axes=(0, 1, 2))
    psi_y = np.fft.irfftn(psi_y_k, s=(n_grid, n_grid, n_grid), axes=(0, 1, 2))
    psi_z = np.fft.irfftn(psi_z_k, s=(n_grid, n_grid, n_grid), axes=(0, 1, 2))

    # Particle Lagrangian coords on a cubic grid (cell centres in
    # PHYSICAL units, Mpc/h), then displaced.
    cell = box_mpc_h / n_grid
    lin = (np.arange(n_grid) + 0.5) * cell
    Q1, Q2, Q3 = np.meshgrid(lin, lin, lin, indexing="ij")
    x_phys = (Q1 + psi_x).reshape(-1)
    y_phys = (Q2 + psi_y).reshape(-1)
    z_phys = (Q3 + psi_z).reshape(-1)

    # Convert to code units [0, 1).
    positions = np.column_stack([x_phys, y_phys, z_phys]) / box_mpc_h
    positions %= 1.0

    # Linear-theory peculiar velocity at a_init:
    #     dx/dt = (f H) psi   with f = dlnD/dlna, H in 1/Hubble units
    # Convert psi to code-unit displacement (divide by L_box).
    from run_sim import hubble, omega_m_of_a

    f_growth = omega_m_of_a(a_init, cosmo.omega_m) ** 0.55
    H_init = hubble(a_init, cosmo.omega_m)
    coef = (a_init**2) * f_growth * H_init / box_mpc_h
    momenta = coef * np.column_stack(
        [psi_x.reshape(-1), psi_y.reshape(-1), psi_z.reshape(-1)]
    )

    info = {
        "a_init": a_init,
        "z_init": z_init,
        "D_init": D_init,
        "sigma_delta_init": float(np.std(delta_init)),
        "displacement_rms_mpc_h": float(
            np.sqrt(np.mean(psi_x**2 + psi_y**2 + psi_z**2))
        ),
    }
    return positions, momenta, info


# ---------------------------------------------------------------------------
# Round-trip self-test: measure P(k) on the realised grid
# ---------------------------------------------------------------------------


def measure_pk(
    delta: NDArray[np.float64], box_mpc_h: float, n_bins: int = 20
) -> tuple[NDArray, NDArray, NDArray]:
    """Spherically average |delta_k|^2 -> P(k_phys) on a 3D grid."""
    n_grid = delta.shape[0]
    kx, ky, kz, k2 = _k_grid_physical(n_grid, box_mpc_h)
    k_mag = np.sqrt(k2)
    V = box_mpc_h**3
    N = n_grid**3
    delta_k = np.fft.rfftn(delta, axes=(0, 1, 2))
    # convert rfftn coefficient to physical P(k):  P = |delta_k|^2 * V / N^2
    Pk_grid = (np.abs(delta_k) ** 2) * V / (N * N)

    k_min = 2.0 * np.pi / box_mpc_h
    k_max = np.pi * n_grid / box_mpc_h                # Nyquist
    bin_edges = np.logspace(np.log10(k_min), np.log10(k_max), n_bins + 1)
    bin_centres = np.sqrt(bin_edges[:-1] * bin_edges[1:])

    # rfftn modes need a weight: kz != 0 and kz != Nyquist counted twice
    # (they represent the dropped negative-kz half), kz == 0 and kz == Nyq
    # counted once. Express as a weight array.
    weight = np.ones_like(k_mag)
    weight[..., 1:-1] = 2.0

    k_flat = k_mag.flatten()
    P_flat = Pk_grid.flatten()
    w_flat = weight.flatten()
    Pk_mean = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(n_bins):
        sel = (k_flat >= bin_edges[i]) & (k_flat < bin_edges[i + 1])
        wsel = w_flat[sel]
        if wsel.sum() == 0:
            Pk_mean[i] = np.nan
            counts[i] = 0
            continue
        Pk_mean[i] = float(np.average(P_flat[sel], weights=wsel))
        counts[i] = float(wsel.sum())
    return bin_centres, Pk_mean, counts


def self_test(verbose: bool = True) -> dict:
    """Round-trip: input P(k) -> IC realisation -> measured P(k)."""
    cosmo = CosmoParams()
    n_grid = 64
    box = 200.0                                       # Mpc/h
    z_init = 49.0
    seed = 20260530

    pos, mom, info = zeldovich_ic(n_grid, box, z_init, cosmo, seed)

    # rebuild the delta grid AT Z=0 directly to check the input P(k),
    # since the IC's delta_init is suppressed by D(a_init).
    delta_z0 = _gaussian_delta_field(n_grid, box, cosmo, seed)
    k_centres, Pk_meas, counts = measure_pk(delta_z0, box, n_bins=15)

    Pk_in = linear_power_spectrum(k_centres, cosmo)
    ratio = Pk_meas / Pk_in

    # Skip very-low-k bins (one or two modes -> huge sample variance)
    # and Nyquist-adjacent bins (CIC-style aliasing not present here,
    # but bin width gets cramped). Quote the central range.
    mask = (counts >= 8) & (k_centres > 4.0 * 2.0 * np.pi / box) & (
        k_centres < 0.4 * np.pi * n_grid / box
    )
    central_ratio = ratio[mask]
    median_ratio = float(np.median(central_ratio))
    rms_log_ratio = float(np.std(np.log(central_ratio)))

    # Empirical sigma_8 from the realised delta at z=0
    # (integrate top-hat over the measured grid).
    sigma8_meas = _sigma8_from_delta(delta_z0, box)

    result = {
        "n_grid": n_grid,
        "box_mpc_h": box,
        "z_init": z_init,
        "D_init": info["D_init"],
        "displacement_rms_mpc_h": info["displacement_rms_mpc_h"],
        "sigma8_input": cosmo.sigma_8,
        "sigma8_measured": sigma8_meas,
        "median_Pk_ratio": median_ratio,
        "rms_log_Pk_ratio": rms_log_ratio,
        "n_central_bins": int(mask.sum()),
        "k_centres": k_centres,
        "Pk_input": Pk_in,
        "Pk_measured": Pk_meas,
        "Pk_ratio": ratio,
    }

    ok = (
        abs(median_ratio - 1.0) < 0.10
        and rms_log_ratio < 0.35
        and abs(sigma8_meas / cosmo.sigma_8 - 1.0) < 0.20
        and info["displacement_rms_mpc_h"] > 0.0
        and info["displacement_rms_mpc_h"] < 0.3 * box
    )

    if verbose:
        print(f"[ic] n_grid={n_grid}, box={box} Mpc/h, z_init={z_init}")
        print(f"[ic] D(z=49)/D(z=0)             = {info['D_init']:.4f}")
        print(f"[ic] displacement RMS           = {info['displacement_rms_mpc_h']:.3f} Mpc/h"
              f"  (~{info['displacement_rms_mpc_h']/(box/n_grid):.2f} cells)")
        print(f"[ic] sigma_8 input              = {cosmo.sigma_8:.4f}")
        print(f"[ic] sigma_8 from realised dz=0 = {sigma8_meas:.4f}")
        print(f"[ic] median P_meas/P_in (central {int(mask.sum())} bins)"
              f"  = {median_ratio:.4f}")
        print(f"[ic] rms log(P_meas/P_in)       = {rms_log_ratio:.4f}")
        print(f"[ic] {'PASS' if ok else 'FAIL'}")

    result["passed"] = ok
    return result


def _sigma8_from_delta(delta: NDArray, box_mpc_h: float) -> float:
    """Measure sigma_8 from a delta grid by Fourier-space top-hat."""
    n = delta.shape[0]
    kx, ky, kz, k2 = _k_grid_physical(n, box_mpc_h)
    k = np.sqrt(k2)
    W = _W_top_hat(k * 8.0)
    delta_k = np.fft.rfftn(delta, axes=(0, 1, 2))
    weight = np.ones_like(k); weight[..., 1:-1] = 2.0
    V = box_mpc_h**3
    N = n**3
    Pk = (np.abs(delta_k) ** 2) * V / (N * N)
    # variance = (1/V) sum_k |W|^2 P(k)  -> approximate via weighted sum
    # over the rfftn half-grid with the Hermitian doubling.
    sigma2 = float((Pk * W * W * weight).sum() / V)
    return float(np.sqrt(sigma2))


if __name__ == "__main__":
    import sys

    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
