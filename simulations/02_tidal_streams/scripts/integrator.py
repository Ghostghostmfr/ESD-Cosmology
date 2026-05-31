"""Symplectic leapfrog orbit integrator -- sub-task D.3.

Drift-Kick-Drift leapfrog (2nd order, symplectic, time-reversible):

    x_{n+1/2} = x_n + v_n * dt/2
    v_{n+1}   = v_n + a(x_{n+1/2}) * dt
    x_{n+1}   = x_{n+1/2} + v_{n+1} * dt/2

Symplecticity guarantees a bounded oscillation of the energy around
the shadow Hamiltonian (no secular drift), regardless of which
acceleration field is used (GR or ESD). The self-test verifies:

  * energy conservation under the GR potential to < 1 part in 1e6
    over 5 Gyr at dt = 0.5 Myr (~ 220 steps per disk orbit);
  * z-component of angular momentum is conserved to machine
    precision for any axisymmetric potential (GR and ESD both).

Time unit convention
--------------------
Positions in kpc, velocities in km/s -> the natural time unit is

    T0 = 1 kpc / (1 km/s) = 3.0857e16 s = 0.9779 Gyr.

We expose ``GYR_PER_T0 = 0.9779`` so the user can write physical
times in Gyr without having to think about the conversion.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
from numpy.typing import NDArray

from mw_potential import (
    DEFAULT_MW, MWPotential, R0_KPC, V_CIRC_R0_KMS,
)
from esd_potential import DEFAULT_ESD_MW, ESDMWPotential


GYR_PER_T0: float = 0.9779
MYR_PER_T0: float = GYR_PER_T0 * 1.0e3


# ---------------------------------------------------------------------------
# Integrator
# ---------------------------------------------------------------------------


AccelFn = Callable[[NDArray[np.float64]], NDArray[np.float64]]


def integrate(
    xyz0: NDArray[np.float64],
    v0: NDArray[np.float64],
    accel_fn: AccelFn,
    t_end_gyr: float,
    dt_myr: float,
    record_every: int = 1,
) -> dict:
    """Integrate ``n`` particles (shape ``(n, 3)``) for ``t_end_gyr``.

    Returns a dict with arrays:
        t_gyr      (n_snap,)
        xyz        (n_snap, n, 3)
        v          (n_snap, n, 3)
    """
    if xyz0.ndim != 2 or v0.ndim != 2 or xyz0.shape != v0.shape:
        raise ValueError("xyz0 and v0 must both be (n, 3)")
    dt = dt_myr / MYR_PER_T0
    n_steps = int(round((t_end_gyr / GYR_PER_T0) / dt))
    n_snap = n_steps // record_every + 1

    x = xyz0.copy()
    v = v0.copy()
    xs = np.empty((n_snap, *x.shape))
    vs = np.empty((n_snap, *v.shape))
    ts = np.empty(n_snap)
    xs[0] = x; vs[0] = v; ts[0] = 0.0
    snap_idx = 1

    for step in range(1, n_steps + 1):
        # Drift half
        x_half = x + v * (0.5 * dt)
        # Kick full
        a = accel_fn(x_half)
        v = v + a * dt
        # Drift half
        x = x_half + v * (0.5 * dt)

        if step % record_every == 0 and snap_idx < n_snap:
            xs[snap_idx] = x
            vs[snap_idx] = v
            ts[snap_idx] = step * dt * GYR_PER_T0
            snap_idx += 1

    # Always record the final state (so callers using large record_every
    # to "only get the end" actually receive the evolved state, not the
    # initial condition).
    if snap_idx < n_snap or n_steps % record_every != 0:
        if snap_idx >= xs.shape[0]:
            xs = np.concatenate([xs, x[None, ...]], axis=0)
            vs = np.concatenate([vs, v[None, ...]], axis=0)
            ts = np.concatenate([ts, [n_steps * dt * GYR_PER_T0]])
        else:
            xs[snap_idx] = x
            vs[snap_idx] = v
            ts[snap_idx] = n_steps * dt * GYR_PER_T0
        snap_idx += 1

    return dict(t_gyr=ts[:snap_idx], xyz=xs[:snap_idx], v=vs[:snap_idx])


# ---------------------------------------------------------------------------
# Energy / angular momentum diagnostics (GR potential closed-form)
# ---------------------------------------------------------------------------


def energy_gr(
    mw: MWPotential, xyz: NDArray[np.float64], v: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Specific energy per particle under the GR potential."""
    R = np.sqrt(xyz[..., 0] ** 2 + xyz[..., 1] ** 2)
    z = xyz[..., 2]
    phi = mw.potential(R, z)
    ke = 0.5 * np.sum(v * v, axis=-1)
    return ke + phi


def angular_momentum_z(
    xyz: NDArray[np.float64], v: NDArray[np.float64],
) -> NDArray[np.float64]:
    return xyz[..., 0] * v[..., 1] - xyz[..., 1] * v[..., 0]


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    # Place a particle on a circular orbit at the Sun, plus a slightly
    # tilted one to exercise z motion, plus a halo-scale orbit at 30 kpc.
    R_init = np.array([R0_KPC, R0_KPC, 30.0])
    v_init = np.zeros((3, 3))
    xyz_init = np.zeros((3, 3))
    xyz_init[:, 0] = R_init
    v_circ = DEFAULT_MW.v_circ(R_init)
    v_init[:, 1] = v_circ                # circular orbits in (x, y) plane
    # Add a tiny vertical velocity to particle 2 to make it non-planar.
    v_init[1, 2] = 30.0

    # Integrate under GR for 5 Gyr.
    t_end = 5.0
    dt_myr = 0.5
    res_gr = integrate(
        xyz_init, v_init, DEFAULT_MW.accel_cart,
        t_end_gyr=t_end, dt_myr=dt_myr, record_every=20,
    )
    E0 = energy_gr(DEFAULT_MW, res_gr["xyz"][0], res_gr["v"][0])
    Et = energy_gr(DEFAULT_MW, res_gr["xyz"][-1], res_gr["v"][-1])
    E_all = np.array([
        energy_gr(DEFAULT_MW, res_gr["xyz"][i], res_gr["v"][i])
        for i in range(res_gr["xyz"].shape[0])
    ])
    dE_rel = float(np.max(np.abs((E_all - E0[None, :]) / E0[None, :])))
    Lz0 = angular_momentum_z(res_gr["xyz"][0], res_gr["v"][0])
    Lz_all = angular_momentum_z(res_gr["xyz"], res_gr["v"])
    dLz_rel = float(np.max(np.abs((Lz_all - Lz0[None, :]) / Lz0[None, :])))

    # Same test under ESD (energy not closed-form, but L_z must be
    # conserved to machine precision for an axisymmetric field).
    res_esd = integrate(
        xyz_init, v_init, DEFAULT_ESD_MW.accel_cart,
        t_end_gyr=t_end, dt_myr=dt_myr, record_every=20,
    )
    Lz_esd = angular_momentum_z(res_esd["xyz"], res_esd["v"])
    Lz_esd0 = Lz_esd[0]
    dLz_esd = float(np.max(np.abs((Lz_esd - Lz_esd0[None, :])
                                  / Lz_esd0[None, :])))

    # Radial range stays bounded (no run-away).
    R_t = np.sqrt(res_gr["xyz"][..., 0] ** 2 + res_gr["xyz"][..., 1] ** 2)
    R_range = float(R_t.max() - R_t.min())
    bounded_ok = R_range < 50.0

    e_ok = dE_rel < 1.0e-6
    lz_gr_ok = dLz_rel < 1.0e-10
    lz_esd_ok = dLz_esd < 1.0e-10
    all_ok = e_ok and lz_gr_ok and lz_esd_ok and bounded_ok

    if verbose:
        print(f"[int] dt = {dt_myr} Myr  ->  steps over 5 Gyr = "
              f"{int(round(t_end / GYR_PER_T0 / (dt_myr / MYR_PER_T0)))}")
        print(f"[int] GR  max |dE/E|    = {dE_rel:.3e}  (< 1e-6)")
        print(f"[int] GR  max |dLz/Lz|  = {dLz_rel:.3e}  (< 1e-10)")
        print(f"[int] ESD max |dLz/Lz|  = {dLz_esd:.3e}  (< 1e-10)")
        print(f"[int] radial range      = {R_range:.2f} kpc  (< 50)")
        print(f"[int] {'PASS' if all_ok else 'FAIL'}")

    return dict(
        passed=bool(all_ok), dE_rel=dE_rel,
        dLz_gr=dLz_rel, dLz_esd=dLz_esd, R_range=R_range,
    )


if __name__ == "__main__":
    import sys
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
