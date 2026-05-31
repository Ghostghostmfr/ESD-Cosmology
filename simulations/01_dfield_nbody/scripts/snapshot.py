"""Snapshot cache for Study A reuse across analysis scripts.

Sub-tasks 1.6 (xi(r)) and 1.7 (density profiles) both want the same
z=0 particle distribution produced by sub-task 1.5's PM evolution.
Re-evolving from z=49 every time is wasteful (~ 200 s per leg), so
this module saves and reloads the final positions.

Cache file naming
-----------------
    snapshots/science_{tag}_{esd_flag}_z0.npz

with ``tag`` = profile name (e.g. ``science``) and ``esd_flag`` =
``gr`` or ``esd``. The contents are positions in Mpc/h (shape (N,3))
plus the profile metadata needed for downstream analysis.

A snapshot is considered valid if the profile parameters in the
loaded file match the requested ``RunProfile``. Mismatch -> rerun.
"""

from __future__ import annotations

import os
import time

import numpy as np

from ic_zeldovich import CosmoParams, zeldovich_ic
from run_sim import SimConfig, ESDRunConfig, run_pm
from compare_hmf import RunProfile


SNAPSHOT_DIR_DEFAULT = "snapshots"


def _snapshot_path(profile: RunProfile, esd: bool, snap_dir: str) -> str:
    tag = "esd" if esd else "gr"
    return os.path.join(snap_dir, f"science_{profile.name}_{tag}_z0.npz")


def _profile_matches(npz: np.lib.npyio.NpzFile, profile: RunProfile) -> bool:
    try:
        return (
            int(npz["n_part_side"]) == profile.n_part_side
            and int(npz["n_grid"]) == profile.n_grid
            and abs(float(npz["box_mpc_h"]) - profile.box_mpc_h) < 1e-9
            and abs(float(npz["z_init"]) - profile.z_init) < 1e-9
            and int(npz["n_steps"]) == profile.n_steps
            and int(npz["seed"]) == profile.seed
        )
    except KeyError:
        return False


def get_or_run_snapshot(
    profile: RunProfile,
    esd: bool,
    snap_dir: str = SNAPSHOT_DIR_DEFAULT,
    force: bool = False,
    verbose: bool = True,
) -> tuple[np.ndarray, dict]:
    """Return final z=0 positions in Mpc/h. Cached on disk by profile.

    If a matching snapshot already exists and ``force`` is False, the
    cached positions are loaded -- this is the fast path for re-using
    the same evolved field across the HMF / xi(r) / profile analyses.
    """
    cosmo = CosmoParams()
    os.makedirs(snap_dir, exist_ok=True)
    path = _snapshot_path(profile, esd, snap_dir)

    if not force and os.path.exists(path):
        with np.load(path, allow_pickle=False) as npz:
            if _profile_matches(npz, profile):
                if verbose:
                    print(f"[snap] cached  : {path}")
                return npz["positions_mpc_h"].copy(), dict(
                    cached=True,
                    box_mpc_h=float(npz["box_mpc_h"]),
                    n_particles=int(npz["positions_mpc_h"].shape[0]),
                )
            elif verbose:
                print(f"[snap] mismatch: {path} -> rerunning")

    if verbose:
        print(f"[snap] evolving: {profile.label}, esd={esd}")
    pos, mom, ic_info = zeldovich_ic(
        n_part_side=profile.n_part_side,
        box_mpc_h=profile.box_mpc_h,
        z_init=profile.z_init,
        cosmo=cosmo,
        seed=profile.seed,
    )
    sim_cfg = SimConfig(
        n_part_side=profile.n_part_side,
        n_grid=profile.n_grid,
        a_init=1.0 / (1.0 + profile.z_init),
        a_final=1.0,
        n_steps=profile.n_steps,
        omega_m=cosmo.omega_m,
        seed=profile.seed,
    )
    esd_cfg = (
        ESDRunConfig(box_mpc_h=profile.box_mpc_h, h=cosmo.h) if esd else None
    )
    t0 = time.time()
    _ = run_pm(pos, mom, sim_cfg, esd_cfg=esd_cfg)
    elapsed = time.time() - t0

    pos_phys = (pos * profile.box_mpc_h).astype(np.float64)

    np.savez(
        path,
        positions_mpc_h=pos_phys,
        n_part_side=profile.n_part_side,
        n_grid=profile.n_grid,
        box_mpc_h=profile.box_mpc_h,
        z_init=profile.z_init,
        n_steps=profile.n_steps,
        seed=profile.seed,
        omega_m=cosmo.omega_m,
        h=cosmo.h,
        sigma_8=cosmo.sigma_8,
    )
    if verbose:
        print(f"[snap] wrote   : {path}  ({elapsed:.1f} s)")
    return pos_phys, dict(
        cached=False,
        box_mpc_h=profile.box_mpc_h,
        n_particles=pos_phys.shape[0],
        elapsed_s=elapsed,
    )
