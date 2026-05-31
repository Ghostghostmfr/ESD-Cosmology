"""GR-vs-ESD two-point correlation orchestrator (sub-task 1.6 figure).

Re-uses the same z=0 snapshots that sub-task 1.5 produced (via the
``snapshot`` cache), measures xi(r) via the FFT estimator, and
overlays the linear-theory prediction at the same growth factor.

CLI
---
    python scripts/compare_xi.py --smoke
    python scripts/compare_xi.py --science
"""

from __future__ import annotations

import argparse
import os

import numpy as np

from ic_zeldovich import CosmoParams
from compare_hmf import PROFILE_SMOKE, PROFILE_SCIENCE, RunProfile
from snapshot import get_or_run_snapshot
from two_point import measure_xi_periodic, linear_xi, plot_xi


def _r_bins(box_mpc_h: float, n_grid: int) -> np.ndarray:
    """Sensible radial bins: from 2 cells out to half the box."""
    cell = box_mpc_h / n_grid
    r_min = 2.0 * cell
    r_max = 0.5 * box_mpc_h
    return np.logspace(np.log10(r_min), np.log10(r_max), 16)


def run(profile: RunProfile, gr_only: bool, out_dir: str) -> dict:
    cosmo = CosmoParams()
    print(f"[xi] profile: {profile.label}")

    pos_gr, info_gr = get_or_run_snapshot(profile, esd=False)
    bins = _r_bins(profile.box_mpc_h, profile.n_grid)
    out_gr = measure_xi_periodic(pos_gr, profile.box_mpc_h, profile.n_grid, bins)

    out_esd = None
    if not gr_only:
        pos_esd, info_esd = get_or_run_snapshot(profile, esd=True)
        out_esd = measure_xi_periodic(
            pos_esd, profile.box_mpc_h, profile.n_grid, bins
        )

    # Linear theory at z=0 uses growth_factor=1 since EH98 P(k) is
    # already normalised to sigma_8(z=0).
    r_grid = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), 80)
    xi_lin = linear_xi(r_grid, cosmo, growth_factor=1.0)

    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, f"xi_compare_{profile.name}.png")
    measured = [("GR baseline", out_gr, "C0")]
    if out_esd is not None:
        measured.append(("ESD (gated R(u))", out_esd, "C3"))
    plot_xi(
        out_path=out_png,
        measured=measured,
        theory=(r_grid, xi_lin, "linear theory, z=0"),
        title=f"Two-point correlation -- {profile.label}",
    )
    print(f"[xi] figure : {out_png}")

    # Print a small table of xi values at a few representative scales.
    print("[xi] r [Mpc/h]   GR xi        ESD xi       lin xi")
    for r_pick in (3.0, 8.0, 20.0):
        i = int(np.argmin(np.abs(out_gr["r_centers"] - r_pick)))
        gr_v = out_gr["xi"][i]
        esd_v = out_esd["xi"][i] if out_esd is not None else float("nan")
        lin_v = float(np.interp(out_gr["r_centers"][i], r_grid, xi_lin))
        print(f"   {out_gr['r_centers'][i]:7.2f}   "
              f"{gr_v:+.3e}  {esd_v:+.3e}  {lin_v:+.3e}")

    return dict(
        passed=True,
        figure=out_png,
        n_part=int(pos_gr.shape[0]),
    )


def main() -> None:
    p = argparse.ArgumentParser(
        description="Sub-task 1.6: GR vs ESD two-point correlation."
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
