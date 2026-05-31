"""Single-target stream simulation orchestrator -- sub-tasks D.5/D.6/D.7.

Workflow for each ``StreamTarget``:

  1. Take the published present-day galactocentric phase-space.
  2. Integrate the progenitor backward by ``target.age_gyr`` (no spray)
     under the GR potential to find an "ancestor" location.
  3. Restart at the ancestor and forward-integrate with particle spray
     under BOTH the GR and ESD potentials, in turn.
  4. Project both stream realisations into a stream-aligned frame
     defined by the GR present-day progenitor's own orbit (so that
     phi1=phi2=0 sits at the progenitor and the two branches are
     compared on the same axes).
  5. Plot (phi1, phi2) for both branches with the progenitor marked.

This is **not** a chi-square fit against Gaia data — that would
require downloading the Gaia member catalogue and an MCMC over the
progenitor's initial phase space (Bowden+ 2015 prescription). The
present orchestrator instead produces the *predicted* track in each
gravity model and lets a side-by-side visual comparison expose any
systematic difference. A future D.5b would close the loop with data.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from mw_potential import DEFAULT_MW, MWPotential
from esd_potential import DEFAULT_ESD_MW, ESDMWPotential
from integrator import integrate
from stream import integrate_stream, StreamConfig
from stream_data import (
    StreamTarget, ALL_TARGETS, GD1, PAL5, SGR,
    stream_frame_from_orbit, to_stream_coords,
)


# ---------------------------------------------------------------------------
# Backward-integrate a single tracer (no spray, no extra particles).
# ---------------------------------------------------------------------------


def backward_progenitor(
    target: StreamTarget, accel_fn, dt_myr: float = 0.5,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return (x_ancestor, v_ancestor) ``target.age_gyr`` ago.

    We integrate forward with ``-v0`` and then negate the final
    velocity (time-reversal symmetry of conservative dynamics).
    The same accel_fn used here MUST be used for the forward run
    so the present-day endpoint matches the observed phase space.
    """
    x0 = target.x0[None, :]
    v0_neg = -target.v0[None, :]
    res = integrate(
        x0, v0_neg, accel_fn,
        t_end_gyr=target.age_gyr, dt_myr=dt_myr,
        record_every=10_000_000,                # only the last snapshot
    )
    x_anc = res["xyz"][-1, 0]
    v_anc = -res["v"][-1, 0]
    return x_anc, v_anc


# ---------------------------------------------------------------------------
# Run one target, both branches.
# ---------------------------------------------------------------------------


@dataclass
class StreamRun:
    name: str
    branch: str                       # "GR" or "ESD"
    prog_xyz_final: NDArray[np.float64]
    prog_v_final: NDArray[np.float64]
    stream_xyz_final: NDArray[np.float64]    # (n_active, 3)
    release_side: NDArray[np.int8]            # (n_active,)
    cfg: StreamConfig


def run_target(
    target: StreamTarget,
    release_every_myr: float = 5.0,
    dt_myr: float = 1.0,
) -> dict[str, StreamRun]:
    """Run both GR and ESD branches for one target.

    Returns ``{"GR": StreamRun, "ESD": StreamRun}``.
    """
    print(f"[run] target = {target.name}  ({target.M_prog_describe})")
    print(f"[run]   age_gyr = {target.age_gyr},  M_prog = {target.M_prog_msun:.2e}")

    # Per-branch backward integration so each forward run ends at the
    # observed present-day phase space (the orbit family differs
    # between potentials, so a shared ancestor would put the two
    # streams in different places today and confound the comparison).
    cfg = StreamConfig(
        M_prog_msun=target.M_prog_msun,
        release_every_myr=release_every_myr,
        dt_myr=dt_myr,
        t_end_gyr=target.age_gyr,
    )

    runs: dict[str, StreamRun] = {}
    for label, mw in (("GR", DEFAULT_MW), ("ESD", DEFAULT_ESD_MW)):
        x_anc, v_anc = backward_progenitor(
            target, mw.accel_cart, dt_myr=dt_myr,
        )
        print(f"[run]   [{label}] ancestor at -{target.age_gyr:.1f} Gyr: "
              f"|x|={np.linalg.norm(x_anc):.2f} kpc, "
              f"|v|={np.linalg.norm(v_anc):.2f} km/s")
        print(f"[run]   [{label}] integrating forward with spray ...")
        out = integrate_stream(
            x_anc, v_anc, mw.accel_cart, DEFAULT_MW, cfg,
            record_every=200, verbose=False,
        )
        n_last = int(out["n_active"][-1])
        runs[label] = StreamRun(
            name=target.name, branch=label,
            prog_xyz_final=out["prog_xyz"][-1],
            prog_v_final=out["prog_v"][-1],
            stream_xyz_final=out["stream_xyz"][-1, :n_last],
            release_side=out["release_side"][:n_last],
            cfg=cfg,
        )
        d_prog = np.linalg.norm(runs[label].prog_xyz_final - target.x0)
        print(f"[run]     n_particles = {n_last},  "
              f"|prog_now - observed|  = {d_prog:.2f} kpc")
    return runs


# ---------------------------------------------------------------------------
# Plotting (GR vs ESD on shared stream-frame axes per target).
# ---------------------------------------------------------------------------


def plot_target(
    runs: dict[str, StreamRun], out_path: str,
) -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Use the GR present-day progenitor's orbit to set the stream frame.
    gr = runs["GR"]; esd = runs["ESD"]
    e1, e2, e3 = stream_frame_from_orbit(gr.prog_xyz_final, gr.prog_v_final)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    metrics: dict[str, dict] = {}
    for ax, run, colour in zip(axes, (gr, esd), ("C0", "C3")):
        phi1, phi2 = to_stream_coords(run.stream_xyz_final, e1, e2, e3)
        # Unwrap phi1 so the stream is a continuous arc on the plot.
        phi1u = np.degrees(np.unwrap(np.radians(phi1)))
        leading = run.release_side == +1
        trailing = run.release_side == -1
        ax.scatter(
            phi1u[leading], phi2[leading], s=4, alpha=0.5,
            color=colour, label="leading (L2)",
        )
        ax.scatter(
            phi1u[trailing], phi2[trailing], s=4, alpha=0.5,
            color=colour, marker="x", label="trailing (L1)",
        )
        ax.axhline(0.0, color="grey", lw=0.5, ls=":")
        ax.axvline(0.0, color="grey", lw=0.5, ls=":")
        ax.scatter([0.0], [0.0], color="black", s=40, marker="*",
                   label="progenitor (today)")
        ax.set_xlabel(r"$\phi_1$ along stream [deg]")
        if ax is axes[0]:
            ax.set_ylabel(r"$\phi_2$ across stream [deg]")
        ax.set_title(f"{run.name} -- {run.branch}")
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=False, fontsize=8, loc="best")
        metrics[run.branch] = dict(
            phi1_span=float(np.nanmax(phi1u) - np.nanmin(phi1u)),
            phi2_rms=float(np.sqrt(np.nanmean(phi2 ** 2))),
            phi2_max=float(np.nanmax(np.abs(phi2))),
        )

    fig.suptitle(f"{gr.name}: predicted stream track, GR vs ESD")
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    return metrics


# ---------------------------------------------------------------------------
# CLI / batch driver.
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--target", default="all",
                   choices=("all", "gd1", "pal5", "sgr"))
    p.add_argument("--out-dir", default="figures_generated")
    p.add_argument("--release-every-myr", type=float, default=5.0)
    p.add_argument("--dt-myr", type=float, default=1.0)
    args = p.parse_args()

    table = {"gd1": GD1, "pal5": PAL5, "sgr": SGR}
    if args.target == "all":
        targets = ALL_TARGETS
    else:
        targets = (table[args.target],)

    summary: list[tuple[str, dict]] = []
    for tgt in targets:
        runs = run_target(
            tgt, release_every_myr=args.release_every_myr,
            dt_myr=args.dt_myr,
        )
        slug = tgt.name.lower().replace(" ", "").replace("-", "")
        out_path = os.path.join(args.out_dir, f"stream_{slug}_compare.png")
        m = plot_target(runs, out_path)
        print(f"[run]   figure -> {out_path}")
        summary.append((tgt.name, m))

    print("\n[summary] target          GR phi1 span / phi2 rms     ESD phi1 span / phi2 rms")
    for name, m in summary:
        gr = m["GR"]; esd = m["ESD"]
        print(f"   {name:15s}  {gr['phi1_span']:7.2f} / {gr['phi2_rms']:5.2f}  deg     "
              f"{esd['phi1_span']:7.2f} / {esd['phi2_rms']:5.2f}  deg")


if __name__ == "__main__":
    main()
