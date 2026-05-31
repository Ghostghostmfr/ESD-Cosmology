"""GR-vs-ESD halo-mass-function orchestrator (sub-task 1.5 figure).

End-to-end pipeline:

    Zel'dovich IC (ic_zeldovich)
        --> PM evolution (run_sim, GR baseline)
        --> FOF (find_halos)
        --> binned dn/dlnM

    same IC --> PM evolution (run_sim, ESD enabled)
        --> FOF (find_halos)
        --> binned dn/dlnM

    overlay both against Press-Schechter analytic curve.

The same realisation seed is used for both runs so any difference in
the recovered halo population is *directly* the effect of the gated
R(u) modification -- cosmic-variance is differenced out cleanly.

CLI
---
    python scripts/compare_hmf.py --smoke
        32^3 / 50 Mpc/h / 100 steps, runs in ~minutes on one CPU.
        Verifies the pipeline end-to-end; not a science figure.

    python scripts/compare_hmf.py --science
        64^3 / 100 Mpc/h / 400 steps. Produces the comparison figure
        used in the paper/figures slot.

    python scripts/compare_hmf.py --gr-only --smoke
        Skip the ESD leg (faster sanity check of the GR baseline + PS).
"""

from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass

import numpy as np

from ic_zeldovich import CosmoParams, zeldovich_ic
from run_sim import SimConfig, ESDRunConfig, run_pm
from find_halos import halo_catalog
from halo_mass_function import (
    binned_dn_dlnm,
    particle_mass_msunh,
    press_schechter_dn_dlnm,
    plot_hmf,
)


# ---------------------------------------------------------------------------
# Run profile
# ---------------------------------------------------------------------------


@dataclass
class RunProfile:
    name: str
    n_part_side: int
    n_grid: int
    box_mpc_h: float
    z_init: float
    n_steps: int
    seed: int

    @property
    def label(self) -> str:
        return (
            f"{self.name}: N={self.n_part_side}^3, "
            f"L={self.box_mpc_h:.0f} Mpc/h, "
            f"n_steps={self.n_steps}"
        )


PROFILE_SMOKE = RunProfile(
    name="smoke",
    n_part_side=32, n_grid=32, box_mpc_h=50.0,
    z_init=49.0, n_steps=100, seed=20260530,
)

PROFILE_SCIENCE = RunProfile(
    name="science",
    n_part_side=64, n_grid=64, box_mpc_h=100.0,
    z_init=49.0, n_steps=400, seed=20260530,
)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def _run_one(
    profile: RunProfile, cosmo: CosmoParams, esd: bool,
) -> tuple[np.ndarray, dict]:
    """Generate IC, evolve to z=0, return final positions in Mpc/h."""
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
        ESDRunConfig(box_mpc_h=profile.box_mpc_h, h=cosmo.h)
        if esd else None
    )
    t0 = time.time()
    _ = run_pm(pos, mom, sim_cfg, esd_cfg=esd_cfg)
    elapsed = time.time() - t0

    # pos was modified in place by run_pm; convert to Mpc/h.
    pos_phys = pos * profile.box_mpc_h
    info = dict(ic=ic_info, elapsed_s=elapsed)
    return pos_phys, info


def _halos_from_positions(
    positions_mpc_h: np.ndarray,
    box_mpc_h: float,
    particle_mass: float,
    min_members: int,
) -> np.ndarray:
    halos, _ = halo_catalog(
        positions_mpc_h, box_mpc_h=box_mpc_h,
        particle_mass_msun_h=particle_mass,
        b=0.2, min_members=min_members,
    )
    return np.array([h.mass for h in halos], dtype=float)


def run(profile: RunProfile, gr_only: bool, out_dir: str) -> dict:
    cosmo = CosmoParams()
    n_part = profile.n_part_side ** 3
    m_p = particle_mass_msunh(cosmo.omega_m, profile.box_mpc_h, n_part)

    # FOF min_members: 32 is the conventional lower bound for a
    # resolved halo in pure-PM runs; below this the dynamical
    # state is unreliable.
    min_members = 32

    print(f"[hmf] profile        : {profile.label}")
    print(f"[hmf] particle mass  : {m_p:.3e} M_sun/h")
    print(f"[hmf] min halo mass  : {min_members * m_p:.3e} M_sun/h")
    print(f"[hmf] cosmology      : Omega_m={cosmo.omega_m:.5f},"
          f" h={cosmo.h:.4f}, sigma_8={cosmo.sigma_8:.4f}")

    print(f"[hmf] running GR baseline ...")
    pos_gr, info_gr = _run_one(profile, cosmo, esd=False)
    masses_gr = _halos_from_positions(pos_gr, profile.box_mpc_h, m_p, min_members)
    print(f"[hmf]   GR  elapsed = {info_gr['elapsed_s']:.1f} s,"
          f" halos = {len(masses_gr)}")

    masses_esd: np.ndarray = np.array([])
    info_esd: dict = {}
    if not gr_only:
        print(f"[hmf] running ESD-modified ...")
        pos_esd, info_esd = _run_one(profile, cosmo, esd=True)
        masses_esd = _halos_from_positions(
            pos_esd, profile.box_mpc_h, m_p, min_members
        )
        print(f"[hmf]   ESD elapsed = {info_esd['elapsed_s']:.1f} s,"
              f" halos = {len(masses_esd)}")

    # Shared log10-mass bins covering the union of both populations.
    all_masses = np.concatenate([masses_gr, masses_esd])
    if all_masses.size == 0:
        print("[hmf] FAIL: zero halos resolved -- box may be too small"
              " or evolution too short")
        return dict(passed=False)
    lo = np.log10(all_masses.min()) - 0.01
    hi = np.log10(all_masses.max()) + 0.01
    edges = np.linspace(lo, hi, 8 + 1)

    bin_gr = binned_dn_dlnm(masses_gr, profile.box_mpc_h, log10_bins=edges)
    bin_esd = (
        binned_dn_dlnm(masses_esd, profile.box_mpc_h, log10_bins=edges)
        if masses_esd.size else None
    )

    # Press-Schechter on a smoothly-sampled grid covering the bins.
    M_grid = np.logspace(lo, hi, 80)
    dn_PS = press_schechter_dn_dlnm(M_grid, cosmo)

    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, f"hmf_compare_{profile.name}.png")
    measured = [("GR baseline", bin_gr, "C0")]
    if bin_esd is not None:
        measured.append(("ESD (gated R(u))", bin_esd, "C3"))
    plot_hmf(
        out_path=out_png,
        measured=measured,
        theory=(M_grid, dn_PS, "Press-Schechter, z=0"),
        title=(
            f"Halo mass function -- {profile.label}\n"
            f"min halo = {min_members} particles"
        ),
    )
    print(f"[hmf] figure        : {out_png}")

    # Quick sanity: PS curve should be within an order of magnitude of
    # the GR baseline in the mass range where both have counts.
    if bin_gr["counts"].sum() > 0:
        # compare on the bin centres
        from numpy import interp
        ps_at_centres = interp(
            np.log10(bin_gr["M_centers"]), np.log10(M_grid), np.log10(dn_PS),
        )
        meas_log = np.log10(np.maximum(bin_gr["dn_dlnM"], 1e-30))
        ok_bins = bin_gr["counts"] > 0
        if ok_bins.any():
            diff = np.abs(meas_log[ok_bins] - ps_at_centres[ok_bins])
            print(f"[hmf] |log10(GR / PS)|  median = {np.median(diff):.2f},"
                  f" max = {diff.max():.2f}")

    return dict(
        passed=True,
        profile=profile,
        n_halos_gr=int(len(masses_gr)),
        n_halos_esd=int(len(masses_esd)),
        elapsed_gr_s=float(info_gr["elapsed_s"]),
        elapsed_esd_s=float(info_esd.get("elapsed_s", 0.0)),
        figure=out_png,
    )


def main() -> None:
    p = argparse.ArgumentParser(
        description="Sub-task 1.5: GR vs ESD halo mass function comparison."
    )
    grp = p.add_mutually_exclusive_group()
    grp.add_argument("--smoke", action="store_true",
                     help="32^3 / 50 Mpc/h fast pipeline check (default).")
    grp.add_argument("--science", action="store_true",
                     help="64^3 / 100 Mpc/h science-figure run.")
    p.add_argument("--gr-only", action="store_true",
                   help="Skip the ESD leg (faster sanity check).")
    p.add_argument("--out-dir", default="figures_generated",
                   help="Directory for output PNG.")
    args = p.parse_args()

    profile = PROFILE_SCIENCE if args.science else PROFILE_SMOKE
    res = run(profile, gr_only=args.gr_only, out_dir=args.out_dir)
    raise SystemExit(0 if res.get("passed") else 1)


if __name__ == "__main__":
    main()
