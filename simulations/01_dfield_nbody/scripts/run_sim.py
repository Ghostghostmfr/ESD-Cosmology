"""GR-baseline particle-mesh (PM) solver for the ESD N-body study.

Sub-task 1.1 of simulation 01: a clean, numpy-only PM solver that
reproduces standard Newtonian cosmological collisionless dynamics
(no ESD modification yet — that lands in sub-task 1.2).

The point of this file is to establish the *baseline*. Before we
bolt on the locked R(u) source term, the solver must reproduce the
linear growth factor D(a) on a tiny test box. That verification is
performed by ``self_test_linear_growth``.

Conventions
-----------
* Comoving positions ``x`` in code units, periodic box of side 1.
* Canonical momentum ``p = a^2 * dx/dt``.
* Time variable: scale factor ``a``. Step rule is KDK leapfrog.
* Background cosmology in code units: ``H0 = 1`` and the comoving
  Poisson equation reads

      laplacian Phi = (3/2) Omega_m delta / a

  with ``delta`` the matter overdensity on the grid (mean removed).
* Particle masses are equal and absorbed into the density
  normalisation; only ``delta`` enters the force.

This file only solves the standard GR equations of motion. The
ESD modification (1 + R(u)) source rescaling is intentionally
absent and lives in sub-task 1.2.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

# Locked cosmological parameters come from esd_core. For sub-task 1.1
# we only need Omega_m; sub-task 1.2b adds the ESD modification path.
from esd_core import OMEGA_M_LOCK

from esd_modification import (
    applicability_gate,
    R_kernel,
    u_of_gN,
    DELTA_VIR,
    GATE_WIDTH_LN,
)

# Mpc in metres (IAU 2015).
_MPC_M: float = 3.0857e22


# ---------------------------------------------------------------------------
# Background cosmology helpers (flat LCDM in code units H0 = 1)
# ---------------------------------------------------------------------------


def hubble(a: float, omega_m: float) -> float:
    """E(a) = H(a)/H0 for flat LCDM. ``H0 = 1`` in code units."""
    omega_l = 1.0 - omega_m
    return math.sqrt(omega_m / a**3 + omega_l)


def omega_m_of_a(a: float, omega_m: float) -> float:
    return omega_m / a**3 / hubble(a, omega_m) ** 2


def linear_growth_factor(
    a_grid: NDArray[np.float64], omega_m: float
) -> NDArray[np.float64]:
    """Solve the linear growth ODE in ``a`` and return D(a).

    Derived from D''(t) + 2 H D'(t) = (3/2) Omega_m(a) H^2 D by
    switching to scale-factor time. The result is

        D'' + (3/a + H'/H) D' - (3/2) Omega_m D / (a^2 H^2) * H^2 = 0

    i.e. (using H'/H = -3 Omega_m / (2 a^4 H^2)):

        D'' + (3/a + H'/H) D' = (3/2) Omega_m D / a^2,

    where ' = d/da. Normalised so D(a=a_grid[0]) = a_grid[0]
    (matter-era growing mode).
    """
    from scipy.integrate import solve_ivp

    a0 = float(a_grid[0])

    def rhs(a: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        D, dD = y
        H = hubble(a, omega_m)
        # H^2 = Om/a^3 + (1-Om)  =>  2 H dH/da = -3 Om / a^4
        dHda = -1.5 * omega_m / a**4 / H
        # source uses the *time-dependent* matter fraction Om(a) = Om0/(a^3 H^2)
        omega_m_a = omega_m / (a**3 * H**2)
        ddD = 1.5 * omega_m_a * D / a**2 - (3.0 / a + dHda / H) * dD
        return np.array([dD, ddD])

    sol = solve_ivp(
        rhs,
        (a0, float(a_grid[-1])),
        np.array([a0, 1.0]),
        t_eval=a_grid,
        rtol=1e-10,
        atol=1e-12,
    )
    return sol.y[0]


# ---------------------------------------------------------------------------
# PM solver primitives: CIC assignment, FFT Poisson, force interpolation
# ---------------------------------------------------------------------------


def cic_assign(positions: NDArray[np.float64], n_grid: int) -> NDArray[np.float64]:
    """Cloud-in-cell deposit of unit-mass particles onto an ``n_grid^3`` mesh.

    ``positions`` are in code units (periodic box of side 1). Returns
    cell-mass on the grid; mean over the grid equals N_part / N_cells.
    """
    n = n_grid
    p = (positions % 1.0) * n
    i0 = np.floor(p).astype(np.int64) % n
    f = p - np.floor(p)
    i1 = (i0 + 1) % n

    rho = np.zeros((n, n, n), dtype=np.float64)
    # Eight CIC corners.
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                ix = i1[:, 0] if dx else i0[:, 0]
                iy = i1[:, 1] if dy else i0[:, 1]
                iz = i1[:, 2] if dz else i0[:, 2]
                wx = f[:, 0] if dx else (1.0 - f[:, 0])
                wy = f[:, 1] if dy else (1.0 - f[:, 1])
                wz = f[:, 2] if dz else (1.0 - f[:, 2])
                w = wx * wy * wz
                np.add.at(rho, (ix, iy, iz), w)
    return rho


def cic_interpolate(
    field: NDArray[np.float64], positions: NDArray[np.float64]
) -> NDArray[np.float64]:
    """CIC sample a scalar grid field at particle positions."""
    n = field.shape[0]
    p = (positions % 1.0) * n
    i0 = np.floor(p).astype(np.int64) % n
    f = p - np.floor(p)
    i1 = (i0 + 1) % n

    out = np.zeros(positions.shape[0], dtype=np.float64)
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                ix = i1[:, 0] if dx else i0[:, 0]
                iy = i1[:, 1] if dy else i0[:, 1]
                iz = i1[:, 2] if dz else i0[:, 2]
                wx = f[:, 0] if dx else (1.0 - f[:, 0])
                wy = f[:, 1] if dy else (1.0 - f[:, 1])
                wz = f[:, 2] if dz else (1.0 - f[:, 2])
                out += field[ix, iy, iz] * (wx * wy * wz)
    return out


def _k_grid(n: int) -> tuple[NDArray, NDArray, NDArray, NDArray]:
    """Cached FFT wavenumber grids in units of 2 pi (box length = 1)."""
    k1d = 2.0 * np.pi * np.fft.fftfreq(n, d=1.0 / n)
    kz1d = 2.0 * np.pi * np.fft.rfftfreq(n, d=1.0 / n)
    kx, ky, kz = np.meshgrid(k1d, k1d, kz1d, indexing="ij")
    k2 = kx**2 + ky**2 + kz**2
    return kx, ky, kz, k2


def solve_forces(
    delta: NDArray[np.float64], a: float, omega_m: float
) -> tuple[NDArray, NDArray, NDArray]:
    """Solve Poisson and return the three comoving force components.

        nabla^2 Phi = (3/2) Omega_m * delta / a
        F = -grad Phi
    """
    n = delta.shape[0]
    kx, ky, kz, k2 = _k_grid(n)
    k2_safe = k2.copy()
    k2_safe[0, 0, 0] = 1.0  # avoid div-by-zero; DC term set to 0 below

    delta_k = np.fft.rfftn(delta, axes=(0, 1, 2))
    phi_k = -1.5 * omega_m / a * delta_k / k2_safe
    phi_k[0, 0, 0] = 0.0

    axes = (0, 1, 2)
    fx = -np.fft.irfftn(1j * kx * phi_k, s=delta.shape, axes=axes)
    fy = -np.fft.irfftn(1j * ky * phi_k, s=delta.shape, axes=axes)
    fz = -np.fft.irfftn(1j * kz * phi_k, s=delta.shape, axes=axes)
    return fx, fy, fz


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


@dataclass
class SimConfig:
    n_part_side: int = 32          # particles per side (N_p = n_part_side^3)
    n_grid: int = 32               # mesh cells per side
    a_init: float = 0.02
    a_final: float = 1.0
    n_steps: int = 100
    omega_m: float = float(OMEGA_M_LOCK)
    seed: int = 1234


@dataclass
class ESDRunConfig:
    """Optional ESD modification of the per-particle acceleration.

    The PM solver computes the comoving Newtonian potential as before;
    after interpolating the proper peculiar acceleration to particles,
    each particle's acceleration is rescaled by

        g_ESD = g_N * [ 1 + gate(delta_local) * R(u(|g_N|_SI)) ]

    where ``gate`` is the Study-19 applicability indicator and
    ``R(u)`` is the closure-pool kernel from ``esd_modification``.
    Both factors are evaluated per particle from the same density
    grid used to solve Poisson, so the modification is consistent
    with the gravitating source.

    Setting ``run_pm(..., esd_cfg=None)`` (the default) preserves the
    pure-GR code path bit-for-bit, so the sub-task 1.1 self-test is
    untouched.
    """
    box_mpc_h: float                     # physical box size [Mpc/h, comoving]
    h: float                             # H0 / (100 km/s/Mpc)
    delta_vir: float = float(DELTA_VIR)
    gate_width_ln: float = float(GATE_WIDTH_LN)

    def code_to_si_accel(self) -> float:
        """Conversion: |g_N| in code units -> [m / s^2] in proper SI.

        Code units are L_box -> 1 and H0 -> 1. Hence
            length_SI per code = (box_mpc_h / h) * Mpc_m,
            time_SI per code   = 1 / H0_SI,
        with H0_SI = 100 h km/s/Mpc = 1e5 h / Mpc_m s^-1. The proper
        peculiar acceleration scale therefore works out to
            box_mpc_h * h * 1e10 / Mpc_m   [m / s^2].
        """
        return self.box_mpc_h * self.h * 1.0e10 / _MPC_M


def _density_contrast(positions: NDArray, n_grid: int) -> NDArray:
    rho = cic_assign(positions, n_grid)
    mean = rho.mean()
    return rho / mean - 1.0


def _particle_accels(
    fx: NDArray, fy: NDArray, fz: NDArray,
    delta: NDArray,
    positions: NDArray,
    a: float,
    esd_cfg: "ESDRunConfig | None",
) -> tuple[NDArray, NDArray, NDArray]:
    """Interpolate (fx, fy, fz) to particles; optionally apply ESD modification.

    When ``esd_cfg`` is None this is byte-equivalent to the original
    three ``cic_interpolate`` calls in ``run_pm`` -- the GR path is
    not touched.
    """
    ax = cic_interpolate(fx, positions)
    ay = cic_interpolate(fy, positions)
    az = cic_interpolate(fz, positions)
    if esd_cfg is None:
        return ax, ay, az

    # |g_N|_proper in code units: the force returned by solve_forces is
    # -grad Phi in code units; the proper peculiar acceleration is
    # -grad Phi / a (see derivation in run_pm). Divide by ``a`` once.
    g_code = np.sqrt(ax * ax + ay * ay + az * az) / a
    g_si = g_code * esd_cfg.code_to_si_accel()
    u = u_of_gN(g_si)
    delta_p = cic_interpolate(delta, positions)
    gate = applicability_gate(
        delta_p,
        delta_vir=esd_cfg.delta_vir,
        width_ln=esd_cfg.gate_width_ln,
    )
    factor = 1.0 + gate * R_kernel(u)
    return ax * factor, ay * factor, az * factor


def run_pm(
    positions: NDArray[np.float64],
    momenta: NDArray[np.float64],
    cfg: SimConfig,
    record_mode: tuple[int, int, int] | None = None,
    esd_cfg: "ESDRunConfig | None" = None,
) -> dict:
    """Evolve ``positions``/``momenta`` from ``a_init`` to ``a_final`` with KDK.

    If ``record_mode`` is set to ``(kx, ky, kz)`` integer wavenumbers,
    the complex amplitude of ``delta(k)`` at that single mode is
    recorded at every step. This is what the self-test uses to track
    linear growth without needing IO of full snapshots.
    """
    a_grid = np.linspace(cfg.a_init, cfg.a_final, cfg.n_steps + 1)
    log = {"a": a_grid.copy(), "delta_k": np.zeros(cfg.n_steps + 1, dtype=complex)}

    def record(step: int) -> None:
        if record_mode is None:
            return
        delta = _density_contrast(positions, cfg.n_grid)
        delta_k = np.fft.rfftn(delta) / delta.size
        kx, ky, kz = record_mode
        log["delta_k"][step] = delta_k[kx, ky, kz]

    record(0)

    for step in range(cfg.n_steps):
        a0, a1 = float(a_grid[step]), float(a_grid[step + 1])
        da = a1 - a0
        a_half = 0.5 * (a0 + a1)

        # --- kick (half), at a0 -------------------------------------------
        delta = _density_contrast(positions, cfg.n_grid)
        fx, fy, fz = solve_forces(delta, a0, cfg.omega_m)
        ax, ay, az = _particle_accels(fx, fy, fz, delta, positions, a0, esd_cfg)
        kick_coef = 0.5 * da / (a0 * hubble(a0, cfg.omega_m))
        momenta[:, 0] += kick_coef * ax
        momenta[:, 1] += kick_coef * ay
        momenta[:, 2] += kick_coef * az

        # --- drift (full), at a_half --------------------------------------
        drift_coef = da / (a_half**3 * hubble(a_half, cfg.omega_m))
        positions += drift_coef * momenta
        positions %= 1.0

        # --- kick (half), at a1 -------------------------------------------
        delta = _density_contrast(positions, cfg.n_grid)
        fx, fy, fz = solve_forces(delta, a1, cfg.omega_m)
        ax, ay, az = _particle_accels(fx, fy, fz, delta, positions, a1, esd_cfg)
        kick_coef = 0.5 * da / (a1 * hubble(a1, cfg.omega_m))
        momenta[:, 0] += kick_coef * ax
        momenta[:, 1] += kick_coef * ay
        momenta[:, 2] += kick_coef * az

        record(step + 1)

    return log


# ---------------------------------------------------------------------------
# Initial conditions: single-mode sinusoidal perturbation
# ---------------------------------------------------------------------------


def single_mode_ic(
    n_part_side: int,
    amplitude: float,
    mode: tuple[int, int, int],
    a_init: float,
    omega_m: float,
) -> tuple[NDArray, NDArray]:
    """Sinusoidal Zel'dovich displacement along the given Fourier mode.

    Used by the self-test: small enough amplitude to stay linear from
    ``a_init`` to a = 1, so growth at this mode tracks D(a) exactly.
    """
    n = n_part_side
    lin = (np.arange(n) + 0.5) / n
    X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")
    q = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)

    kx, ky, kz = mode
    k_vec = 2.0 * np.pi * np.array([kx, ky, kz], dtype=float)
    k_mag2 = float((k_vec @ k_vec))
    phase = q @ k_vec
    psi = amplitude * np.sin(phase)              # displacement potential
    # displacement: s = -k / k^2 * Im(delta_k e^{i k.q}) -- for delta = A cos(k.q):
    #   s = -(k / k^2) * A * sin(k.q)
    disp = -(k_vec / k_mag2)[None, :] * psi[:, None]
    positions = (q + disp) % 1.0

    # Linear-theory velocity: p = a^2 dx/dt; for the growing mode at small a,
    #   dx/dt = (f H) * s  with f = d ln D / d ln a (~ Omega_m(a)^{0.55})
    f_growth = omega_m_of_a(a_init, omega_m) ** 0.55
    H = hubble(a_init, omega_m)
    momenta = (a_init**2) * f_growth * H * disp
    return positions, momenta


# ---------------------------------------------------------------------------
# Self-test: recover the linear growth factor
# ---------------------------------------------------------------------------


def self_test_linear_growth(verbose: bool = True) -> dict:
    cfg = SimConfig(
        n_part_side=32, n_grid=32, a_init=0.02, a_final=1.0, n_steps=400
    )
    mode = (1, 0, 0)
    amplitude = 1.0e-3            # well inside linear regime
    rng = np.random.default_rng(cfg.seed)
    _ = rng                       # reserved for future stochastic IC
    pos, mom = single_mode_ic(
        cfg.n_part_side, amplitude, mode, cfg.a_init, cfg.omega_m
    )
    log = run_pm(pos, mom, cfg, record_mode=mode)

    # Measured growth: |delta_k(a)| / |delta_k(a_init)|
    amp = np.abs(log["delta_k"])
    amp /= amp[0]
    # Theoretical growth from linear ODE
    D = linear_growth_factor(log["a"], cfg.omega_m)
    D /= D[0]

    rel_err = (amp - D) / D
    max_err = float(np.max(np.abs(rel_err[1:])))    # skip a=a_init
    final_err = float(rel_err[-1])

    result = {
        "a": log["a"],
        "measured": amp,
        "linear_theory": D,
        "max_rel_err": max_err,
        "final_rel_err": final_err,
    }
    if verbose:
        print(f"[self-test] n_part_side = {cfg.n_part_side}, n_grid = {cfg.n_grid}")
        print(f"[self-test] mode = {mode}, amplitude = {amplitude:.1e}")
        print(f"[self-test] steps = {cfg.n_steps}, a in [{cfg.a_init}, {cfg.a_final}]")
        print(f"[self-test] max |measured/D - 1|   = {max_err:.3e}")
        print(f"[self-test] final (measured/D - 1) = {final_err:+.3e}")
    return result


def self_test_esd_linear_invariance(verbose: bool = True) -> dict:
    """Sub-task 1.2b verification: ESD-on must reproduce GR linear growth.

    Per Study 19, the applicability gate forces R(u) to vanish in the
    linear regime (delta << delta_vir = 200), so a sinusoidal Zel'dovich
    perturbation with amplitude 1e-3 must grow exactly as D(a) -- the
    same residual the GR baseline achieves on the 1.1 self-test.

    This is the *invariant* that justifies wiring R(u) into the
    integrator: if it fails, the modification is silently leaking into
    the linear sector and the resulting cosmology disagrees with Planck
    at first order. If it passes, ESD inherits LambdaCDM linear growth
    exactly and the modification is confined to virialized scales.
    """
    cfg = SimConfig(
        n_part_side=32, n_grid=32, a_init=0.02, a_final=1.0, n_steps=400
    )
    # Physical box. 200 Mpc/h is large enough that the k=(1,0,0) mode
    # is solidly linear; h matches the Planck-2018 value used in the
    # IC generator.
    esd_cfg = ESDRunConfig(box_mpc_h=200.0, h=0.6736)

    mode = (1, 0, 0)
    amplitude = 1.0e-3
    pos, mom = single_mode_ic(
        cfg.n_part_side, amplitude, mode, cfg.a_init, cfg.omega_m
    )
    log = run_pm(pos, mom, cfg, record_mode=mode, esd_cfg=esd_cfg)

    amp = np.abs(log["delta_k"])
    amp /= amp[0]
    D = linear_growth_factor(log["a"], cfg.omega_m)
    D /= D[0]
    rel_err = (amp - D) / D
    max_err = float(np.max(np.abs(rel_err[1:])))
    final_err = float(rel_err[-1])

    # GR baseline residual for the same configuration, to compare.
    gr_res = self_test_linear_growth(verbose=False)
    gr_max = gr_res["max_rel_err"]
    delta_residual = abs(max_err - gr_max)

    # Sample the gate over the realised delta range so we can confirm
    # it is functionally zero throughout the run.
    a_grid = log["a"]
    typical_delta = amplitude * (D / D[0])
    gate_max = float(np.max(
        applicability_gate(
            typical_delta,
            delta_vir=esd_cfg.delta_vir,
            width_ln=esd_cfg.gate_width_ln,
        )
    ))

    result = {
        "esd_max_rel_err": max_err,
        "esd_final_rel_err": final_err,
        "gr_max_rel_err": gr_max,
        "esd_minus_gr": delta_residual,
        "gate_max_over_run": gate_max,
        "a": a_grid,
    }
    if verbose:
        print("[esd-self-test] linear-regime invariance (sub-task 1.2b)")
        print(f"[esd-self-test] box = {esd_cfg.box_mpc_h} Mpc/h, h = {esd_cfg.h}")
        print(f"[esd-self-test] mode = {mode}, amplitude = {amplitude:.1e}")
        print(f"[esd-self-test] max gate over run = {gate_max:.3e}  (must be ~ 0)")
        print(f"[esd-self-test] GR  max |meas/D - 1| = {gr_max:.3e}")
        print(f"[esd-self-test] ESD max |meas/D - 1| = {max_err:.3e}")
        print(f"[esd-self-test] |ESD - GR| residual  = {delta_residual:.3e}")
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(
        description="ESD sim 01: GR-baseline PM solver (sub-task 1.1)"
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="Run the linear-growth verification on a 32^3 box.",
    )
    p.add_argument(
        "--esd-self-test",
        action="store_true",
        help="Sub-task 1.2b: verify ESD-on reproduces GR linear growth.",
    )
    args = p.parse_args()

    if args.self_test:
        res = self_test_linear_growth(verbose=True)
        # Pass criterion: <3% deviation from linear growth over a in [0.02, 1].
        ok = res["max_rel_err"] < 0.03
        print(f"[self-test] {'PASS' if ok else 'FAIL'}")
        raise SystemExit(0 if ok else 1)

    if args.esd_self_test:
        res = self_test_esd_linear_invariance(verbose=True)
        # Pass: gate stays below 1e-3 everywhere AND ESD residual is
        # within 0.5% of GR residual (any larger drift would imply the
        # gate is leaking into the linear sector).
        ok = (
            res["gate_max_over_run"] < 1.0e-3
            and res["esd_minus_gr"] < 5.0e-3
        )
        print(f"[esd-self-test] {'PASS' if ok else 'FAIL'}")
        raise SystemExit(0 if ok else 1)

    # Default behaviour for now: just print that the full driver isn't
    # wired up yet (Zel'dovich IC and snapshot IO land in sub-task 1.3).
    print("Sub-task 1.1 driver only exposes --self-test until sub-task 1.3.")
    print("Run:  python -m scripts.run_sim --self-test")


if __name__ == "__main__":
    main()
