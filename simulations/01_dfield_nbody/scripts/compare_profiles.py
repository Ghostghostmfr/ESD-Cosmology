"""GR-vs-ESD stacked halo profile orchestrator (sub-task 1.7 figure).

Loads the z=0 snapshots produced by the snapshot cache, runs FOF
on each (GR and ESD) at the science resolution, stacks halo
profiles in mass bins, fits NFW, and produces the side-by-side
figure that is the headline result of sub-task 1.7.
"""

from __future__ import annotations

import argparse
import os

from compare_hmf import PROFILE_SMOKE, PROFILE_SCIENCE, RunProfile
from halo_mass_function import particle_mass_msunh
from halo_profile import stack_profiles, plot_profiles
from snapshot import get_or_run_snapshot


# Mass bins (M_sun / h). At 64^3 / 100 Mpc/h science resolution the
# particle mass is ~ 9.5e10 M_sun/h, so 200 particles ~ 1.9e13 and
# 1000 particles ~ 9.5e13. These bins are chosen accordingly.
MASS_BIN_EDGES_SCIENCE = [1.5e13, 5.0e13, 2.0e14]
MASS_BIN_EDGES_SMOKE = [5.0e12, 5.0e13]


OMEGA_M = 0.31574  # OMEGA_M_LOCK


def run(profile: RunProfile, gr_only: bool, out_dir: str) -> dict:
    print(f"[prof] profile: {profile.label}")
    pmass = particle_mass_msunh(
        OMEGA_M, profile.box_mpc_h, profile.n_part_side ** 3
    )
    print(f"[prof] particle mass = {pmass:.3e} M_sun/h")
    edges = (MASS_BIN_EDGES_SCIENCE if profile.name == "science"
             else MASS_BIN_EDGES_SMOKE)

    pos_gr, _ = get_or_run_snapshot(profile, esd=False)
    profiles_gr = stack_profiles(
        pos_gr, box_mpc_h=profile.box_mpc_h,
        particle_mass_msunh=pmass, mass_bin_edges=edges,
        n_radial_bins=12, r_min_mpc_h=0.05, r_max_mpc_h=3.0,
        min_members=50, b=0.2,
    )

    profiles_esd = None
    if not gr_only:
        pos_esd, _ = get_or_run_snapshot(profile, esd=True)
        profiles_esd = stack_profiles(
            pos_esd, box_mpc_h=profile.box_mpc_h,
            particle_mass_msunh=pmass, mass_bin_edges=edges,
            n_radial_bins=12, r_min_mpc_h=0.05, r_max_mpc_h=3.0,
            min_members=50, b=0.2,
        )

    print("[prof] mass bin              N_GR  r_s_GR     N_ESD  r_s_ESD")
    for k, p_gr in enumerate(profiles_gr):
        p_e = profiles_esd[k] if profiles_esd is not None else None
        rs_gr = f"{p_gr.nfw_r_s:.3f}" if p_gr.nfw_r_s is not None else "  -  "
        if p_e is not None:
            rs_e = f"{p_e.nfw_r_s:.3f}" if p_e.nfw_r_s is not None else "  -  "
            ne = p_e.n_halos_stacked
        else:
            rs_e = "  -  "; ne = 0
        print(
            f"   [{p_gr.mass_bin_lo:.2e},{p_gr.mass_bin_hi:.2e}]   "
            f"{p_gr.n_halos_stacked:4d}  {rs_gr}     {ne:4d}  {rs_e}"
        )

    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, f"profiles_compare_{profile.name}.png")
    plot_profiles(
        out_png, profiles_gr, profiles_esd,
        title=f"Stacked halo profiles -- {profile.label}",
    )
    print(f"[prof] figure : {out_png}")
    return dict(passed=True, figure=out_png)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Sub-task 1.7: GR vs ESD stacked halo profiles."
    )
    grp = p.add_mutually_exclusive_group()
    grp.add_argument("--smoke", action="store_true")
    grp.add_argument("--science", action="store_true")
    p.add_argument("--gr-only", action="store_true")
    p.add_argument("--out-dir", default="figures_generated")
    args = p.parse_args()
    profile = PROFILE_SCIENCE if args.science else PROFILE_SMOKE
    res = run(profile, gr_only=args.gr_only, out_dir=args.out_dir)
    raise SystemExit(0 if res.get("passed") else 1)


if __name__ == "__main__":
    main()
