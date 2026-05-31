"""Particle-spray stream model -- sub-task D.4.

Implements a simplified Fardal+ 2015 / Kuepper+ 2012 prescription
for tidal-stream formation: a progenitor cluster of mass ``M_prog``
orbits in the host MW potential, and at fixed intervals two test
particles are released from its inner (L1) and outer (L2) Lagrange
points with the appropriate tidal kick.

Lagrange / Jacobi setup
-----------------------
At progenitor position ``r_p`` with enclosed host mass
``M_enc = M_host(< r_p)``, the Jacobi (tidal) radius is

    r_J = r_p * ( M_prog / (3 * M_enc) )^(1/3),

and the local angular frequency in a near-circular tidal frame is

    Omega = sqrt( G * M_enc / r_p^3 ).

The two release points are placed along the host-center -> progenitor
line at ``r_p +/- r_J``. The tangential velocity offset
``Delta v = Omega * r_J`` (negative for L1, positive for L2) gives the
particles slightly lower / higher orbital energy than the progenitor,
producing trailing / leading arms respectively. We use a single
release per "step" (one particle at L1, one at L2).

For a thin cold stream the progenitor's self-gravity on already
released particles is negligible compared to the host potential, so
test particles are integrated only under the host's
``accel_fn``. The progenitor itself orbits as a single tracer in the
same potential (its mass is treated as a non-back-reacting scalar
used only to set ``r_J``).

CLI:
    python scripts/stream.py        # self-test: 1e4 Msun progenitor at 15 kpc
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray

from mw_potential import DEFAULT_MW, G_GAL, MWPotential
from integrator import GYR_PER_T0, MYR_PER_T0


AccelFn = Callable[[NDArray[np.float64]], NDArray[np.float64]]


@dataclass(frozen=True)
class StreamConfig:
    M_prog_msun: float = 1.0e4
    release_every_myr: float = 5.0
    dt_myr: float = 0.5
    t_end_gyr: float = 3.0


# ---------------------------------------------------------------------------
# Host-enclosed mass helper (spherical) used to set the Jacobi radius.
# ---------------------------------------------------------------------------


def host_M_enc(mw: MWPotential, r_kpc: float) -> float:
    """Approximate spherically-enclosed host mass from v_circ.

    M_enc(r) = r * v_circ(r)^2 / G.
    """
    vc = float(mw.v_circ(np.array([r_kpc]))[0])
    return r_kpc * vc * vc / G_GAL


# ---------------------------------------------------------------------------
# Particle-spray integration loop
# ---------------------------------------------------------------------------


def integrate_stream(
    progenitor_x0: NDArray[np.float64],
    progenitor_v0: NDArray[np.float64],
    accel_fn: AccelFn,
    mw_for_jacobi: MWPotential,
    cfg: StreamConfig,
    record_every: int = 20,
    verbose: bool = False,
) -> dict:
    """Drift-Kick-Drift leapfrog with periodic particle release.

    Returns
    -------
    dict with:
        t_gyr           (n_snap,)
        prog_xyz        (n_snap, 3)
        prog_v          (n_snap, 3)
        stream_xyz      (n_snap, n_max, 3)
        stream_v        (n_snap, n_max, 3)
        n_active        (n_snap,) int
        release_times   (n_max,) Gyr each particle was released
        release_side    (n_max,) +1 for L2 (outer/leading), -1 for L1
    """
    dt = cfg.dt_myr / MYR_PER_T0
    n_steps = int(round((cfg.t_end_gyr / GYR_PER_T0) / dt))
    release_step_interval = max(1, int(round(cfg.release_every_myr / cfg.dt_myr)))
    n_releases = n_steps // release_step_interval
    n_particles_max = 2 * (n_releases + 1)

    n_snap = n_steps // record_every + 1
    prog_xs = np.empty((n_snap, 3))
    prog_vs = np.empty((n_snap, 3))
    stream_xs = np.full((n_snap, n_particles_max, 3), np.nan)
    stream_vs = np.full((n_snap, n_particles_max, 3), np.nan)
    ts = np.empty(n_snap)
    n_active = np.zeros(n_snap, dtype=np.int64)
    release_times = np.full(n_particles_max, np.nan)
    release_side = np.zeros(n_particles_max, dtype=np.int8)

    # Allocate stream particle buffers (positions/vels and active mask).
    s_xyz = np.zeros((n_particles_max, 3))
    s_v = np.zeros((n_particles_max, 3))
    s_active = np.zeros(n_particles_max, dtype=bool)
    n_used = 0

    # Progenitor state.
    p_xyz = progenitor_x0.astype(float).copy()
    p_v = progenitor_v0.astype(float).copy()

    # Initial snapshot.
    prog_xs[0] = p_xyz; prog_vs[0] = p_v
    ts[0] = 0.0; n_active[0] = 0
    snap_idx = 1

    for step in range(1, n_steps + 1):
        # ---- combined leapfrog DKD on progenitor + active stream particles ----
        # Stack into one array for the kick.
        if n_used > 0:
            all_x = np.vstack([p_xyz[None, :], s_xyz[:n_used]])
            all_v = np.vstack([p_v[None, :], s_v[:n_used]])
        else:
            all_x = p_xyz[None, :].copy()
            all_v = p_v[None, :].copy()

        x_half = all_x + all_v * (0.5 * dt)
        a = accel_fn(x_half)
        all_v = all_v + a * dt
        all_x = x_half + all_v * (0.5 * dt)

        # Unstack.
        p_xyz = all_x[0]; p_v = all_v[0]
        if n_used > 0:
            s_xyz[:n_used] = all_x[1:]
            s_v[:n_used] = all_v[1:]

        # ---- release event ----
        if step % release_step_interval == 0 and n_used + 2 <= n_particles_max:
            r_p = float(np.linalg.norm(p_xyz))
            M_enc = host_M_enc(mw_for_jacobi, r_p)
            r_J = r_p * (cfg.M_prog_msun / (3.0 * M_enc)) ** (1.0 / 3.0)
            Omega = math.sqrt(G_GAL * M_enc / r_p ** 3)        # 1 / T0
            # Radial unit vector from host center.
            r_hat = p_xyz / r_p
            # Tangential unit vector in the orbital plane (perp to r_hat,
            # aligned with v_p projected perpendicular to r_hat).
            v_perp = p_v - np.dot(p_v, r_hat) * r_hat
            vp_norm = float(np.linalg.norm(v_perp))
            if vp_norm > 1.0e-10:
                t_hat = v_perp / vp_norm
            else:
                # Degenerate: pick an arbitrary tangent.
                t_hat = np.cross(r_hat, np.array([0.0, 0.0, 1.0]))
                t_hat = t_hat / (np.linalg.norm(t_hat) + 1.0e-30)

            for sign in (+1, -1):
                idx = n_used
                s_xyz[idx] = p_xyz + sign * r_J * r_hat
                s_v[idx] = p_v + sign * Omega * r_J * t_hat
                s_active[idx] = True
                release_times[idx] = step * dt * GYR_PER_T0
                release_side[idx] = sign
                n_used += 1

        # ---- snapshot ----
        if step % record_every == 0 and snap_idx < n_snap:
            prog_xs[snap_idx] = p_xyz
            prog_vs[snap_idx] = p_v
            stream_xs[snap_idx, :n_used] = s_xyz[:n_used]
            stream_vs[snap_idx, :n_used] = s_v[:n_used]
            ts[snap_idx] = step * dt * GYR_PER_T0
            n_active[snap_idx] = n_used
            snap_idx += 1

    if verbose:
        print(f"[stream] n_steps           = {n_steps}")
        print(f"[stream] release interval  = {release_step_interval} steps "
              f"({cfg.release_every_myr} Myr)")
        print(f"[stream] particles released= {n_used}")
        print(f"[stream] snapshots         = {snap_idx}")

    return dict(
        t_gyr=ts[:snap_idx],
        prog_xyz=prog_xs[:snap_idx], prog_v=prog_vs[:snap_idx],
        stream_xyz=stream_xs[:snap_idx], stream_v=stream_vs[:snap_idx],
        n_active=n_active[:snap_idx],
        release_times=release_times[:n_used],
        release_side=release_side[:n_used],
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    # Place a 1e4 M_sun progenitor on a near-circular orbit at 15 kpc.
    R0 = 15.0
    p_x0 = np.array([R0, 0.0, 0.0])
    vc = float(DEFAULT_MW.v_circ(np.array([R0]))[0])
    p_v0 = np.array([0.0, vc, 0.0])

    cfg = StreamConfig(
        M_prog_msun=1.0e4,
        release_every_myr=5.0,
        dt_myr=0.5,
        t_end_gyr=3.0,
    )
    res = integrate_stream(
        p_x0, p_v0,
        accel_fn=DEFAULT_MW.accel_cart,
        mw_for_jacobi=DEFAULT_MW,
        cfg=cfg, record_every=40, verbose=verbose,
    )

    # (1) Progenitor orbit stays bounded near R0 (circular).
    Rp_t = np.sqrt(res["prog_xyz"][:, 0] ** 2 + res["prog_xyz"][:, 1] ** 2)
    R_band = float(Rp_t.max() - Rp_t.min())
    prog_ok = R_band < 1.0       # near-circular -> < 1 kpc band

    # (2) Stream particles form a thin arc roughly in the progenitor's
    # orbit plane. The orbit plane has angular-momentum vector L_p =
    # x_p x v_p ~ (0, 0, +); test particle z should be small compared
    # to in-plane displacement.
    z_max = float(np.nanmax(np.abs(res["stream_xyz"][..., 2])))
    Rxy = np.sqrt(res["stream_xyz"][..., 0] ** 2 + res["stream_xyz"][..., 1] ** 2)
    Rxy_max = float(np.nanmax(Rxy))
    plane_ratio = z_max / Rxy_max
    plane_ok = plane_ratio < 0.05      # < 5%

    # (3) Stream LENGTH grows monotonically (test particles spread out).
    # Use the spread in heliocentric angle (longitude) at each snapshot.
    def stream_length_deg(snap_idx: int) -> float:
        xs = res["stream_xyz"][snap_idx]
        m = ~np.isnan(xs[:, 0])
        if m.sum() < 4:
            return 0.0
        phi = np.degrees(np.arctan2(xs[m, 1], xs[m, 0]))
        # unwrap and take peak-to-peak
        phi_unwrap = np.unwrap(np.deg2rad(phi))
        return float(np.degrees(phi_unwrap.max() - phi_unwrap.min()))

    n_snap = res["t_gyr"].size
    # Sample length at a few times, skipping the first 100 Myr where
    # only a handful of particles exist.
    early = n_snap // 4
    late = n_snap - 2
    L_early = stream_length_deg(early)
    L_late = stream_length_deg(late)
    grows_ok = L_late > L_early > 0.0

    # (4) Leading and trailing arms separate: at late times, the
    # release_side = +1 particles should have a different mean phase
    # than the release_side = -1 particles.
    n_last = int(res["n_active"][-1])
    xs_last = res["stream_xyz"][-1, :n_last]
    sides = res["release_side"][:n_last]
    phi_last = np.degrees(np.arctan2(xs_last[:, 1], xs_last[:, 0]))
    if (sides == +1).any() and (sides == -1).any():
        sep = float(abs(
            np.mean(phi_last[sides == +1]) - np.mean(phi_last[sides == -1])
        ))
    else:
        sep = 0.0
    sep_ok = sep > 1.0       # at least 1 degree of mean separation

    all_ok = prog_ok and plane_ok and grows_ok and sep_ok

    if verbose:
        print(f"[stream] progenitor R band     = {R_band:.3f} kpc  (< 1.0)")
        print(f"[stream] |z|_max / R_max       = {plane_ratio:.3e}  (< 0.05)")
        print(f"[stream] L_early ({res['t_gyr'][early]:.2f} Gyr) = "
              f"{L_early:.2f} deg")
        print(f"[stream] L_late  ({res['t_gyr'][late]:.2f} Gyr) = "
              f"{L_late:.2f} deg")
        print(f"[stream] leading-trailing mean phi sep = {sep:.2f} deg "
              f"(> 1.0)")
        print(f"[stream] {'PASS' if all_ok else 'FAIL'}")

    return dict(
        passed=bool(all_ok),
        R_band=R_band, plane_ratio=plane_ratio,
        L_early=L_early, L_late=L_late, sep_deg=sep,
    )


if __name__ == "__main__":
    import sys
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
