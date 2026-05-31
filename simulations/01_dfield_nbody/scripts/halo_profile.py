"""Stacked halo density profiles + NFW fit (sub-task 1.7).

For each halo above the resolved-mass threshold:
    * find the periodic centre-of-mass (re-using find_halos helpers),
    * bin member particles in radial shells about the COM,
    * stack into mass bins.

Then fit each stacked profile to NFW

    rho(r) = rho_s / [ (r/r_s) (1 + r/r_s)^2 ]

and report (rho_s, r_s, c = r_vir / r_s) per mass bin.

For the GR baseline we expect NFW to fit well at large c. ESD
modifies the per-particle acceleration inside halos (the gate fires
at delta > 200 rho-bar), so the ESD profile should DEVIATE from NFW
in a systematic way -- this is the headline science figure of
sub-task 1.7 and the place where Study 19 says the framework's
internal structure of halos must depart from LambdaCDM.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import curve_fit

from find_halos import halo_catalog, _periodic_delta


# Cosmology helpers (kept local to avoid cross-module coupling).
RHO_CRIT_0_MSUNH_MPCH3: float = 2.775e11


# ---------------------------------------------------------------------------
# NFW
# ---------------------------------------------------------------------------


def nfw_rho(r: NDArray[np.float64], rho_s: float, r_s: float) -> NDArray[np.float64]:
    x = r / r_s
    return rho_s / (x * (1.0 + x) ** 2)


def fit_nfw(
    r: NDArray[np.float64], rho: NDArray[np.float64], rho_err: NDArray[np.float64],
) -> tuple[float, float] | None:
    """Fit NFW (rho_s, r_s) in log-space; return None on failure."""
    mask = np.isfinite(rho) & (rho > 0)
    if mask.sum() < 4:
        return None
    log_rho = np.log10(rho[mask])
    log_err = (rho_err[mask] / rho[mask]) / math.log(10.0)
    log_err = np.maximum(log_err, 0.05)

    def model(r, log_rho_s, log_r_s):
        return np.log10(nfw_rho(r, 10.0 ** log_rho_s, 10.0 ** log_r_s))

    try:
        popt, _ = curve_fit(
            model, r[mask], log_rho,
            p0=[6.0, 0.0],                # rho_s ~ 1e6, r_s ~ 1 Mpc/h
            sigma=log_err, maxfev=8000,
        )
    except Exception:
        return None
    return float(10.0 ** popt[0]), float(10.0 ** popt[1])


# ---------------------------------------------------------------------------
# Profile measurement
# ---------------------------------------------------------------------------


@dataclass
class StackedProfile:
    mass_bin_lo: float
    mass_bin_hi: float
    n_halos_stacked: int
    r_centers_mpc_h: NDArray[np.float64]
    rho_msunh_per_mpch3: NDArray[np.float64]
    rho_err: NDArray[np.float64]
    nfw_rho_s: float | None
    nfw_r_s: float | None


def stack_profiles(
    positions_mpc_h: NDArray[np.float64],
    box_mpc_h: float,
    particle_mass_msunh: float,
    mass_bin_edges: Sequence[float],
    n_radial_bins: int = 12,
    r_min_mpc_h: float = 0.05,
    r_max_mpc_h: float = 3.0,
    min_members: int = 50,
    b: float = 0.2,
) -> list[StackedProfile]:
    """Run FOF on ``positions_mpc_h`` and stack profiles per mass bin.

    For each halo (>= ``min_members``) we sum particle counts in
    log-spaced radial shells about the periodic centre-of-mass, then
    convert to rho [M_sun/h / (Mpc/h)^3] and stack within each mass
    bin. The stack adds particle counts per shell across all halos
    in the bin, then divides by the total shell volume contributed.
    """
    halos, _ = halo_catalog(
        positions_mpc_h, box_mpc_h=box_mpc_h,
        particle_mass_msun_h=particle_mass_msunh,
        b=b, min_members=min_members,
    )
    r_edges = np.logspace(
        math.log10(r_min_mpc_h), math.log10(r_max_mpc_h), n_radial_bins + 1
    )
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    shell_vol = (4.0 / 3.0) * math.pi * (r_edges[1:] ** 3 - r_edges[:-1] ** 3)

    out: list[StackedProfile] = []
    edges = list(mass_bin_edges)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mass_mask = [(h.mass >= lo) and (h.mass < hi) for h in halos]
        if not any(mass_mask):
            out.append(StackedProfile(
                lo, hi, 0, r_centers,
                np.full_like(r_centers, np.nan),
                np.full_like(r_centers, np.nan),
                None, None,
            ))
            continue

        # Use a KDTree-free per-halo loop: each halo is at most a few
        # thousand particles. We still need the full particle list,
        # not the halo's own membership (otherwise the outskirts of
        # massive halos that overlap into other FOF objects get cut).
        # However, with FOF defined by b=0.2 the linking already
        # bounds the halo. We use ALL particles (full snapshot) and
        # take only those within r_max_mpc_h of the COM.
        # That picks up infalling particles that should still count
        # toward the halo's outer profile.
        counts_total = np.zeros_like(r_centers, dtype=np.int64)
        n_stacked = 0
        for h, in_bin in zip(halos, mass_mask):
            if not in_bin:
                continue
            d = _periodic_delta(positions_mpc_h, h.com_mpc_h[None, :], box_mpc_h)
            r = np.linalg.norm(d, axis=1)
            sel = r < r_max_mpc_h
            if not sel.any():
                continue
            counts, _ = np.histogram(r[sel], bins=r_edges)
            counts_total += counts.astype(np.int64)
            n_stacked += 1

        total_vol = n_stacked * shell_vol
        with np.errstate(divide="ignore", invalid="ignore"):
            rho = particle_mass_msunh * counts_total / total_vol
            rho_err = (
                particle_mass_msunh * np.sqrt(np.maximum(counts_total, 1))
                / total_vol
            )

        nfw_rho_s = nfw_r_s = None
        fit = fit_nfw(r_centers, rho, rho_err)
        if fit is not None:
            nfw_rho_s, nfw_r_s = fit

        out.append(StackedProfile(
            lo, hi, n_stacked, r_centers, rho, rho_err, nfw_rho_s, nfw_r_s,
        ))
    return out


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------


def plot_profiles(
    out_path: str,
    profiles_gr: list[StackedProfile],
    profiles_esd: list[StackedProfile] | None,
    title: str = "Stacked halo profiles",
) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n_bins = len(profiles_gr)
    if n_bins == 0:
        return
    fig, axes = plt.subplots(
        1, n_bins, figsize=(4.2 * n_bins, 4.0), sharey=True, squeeze=False,
    )
    axes = axes[0]
    for k, p_gr in enumerate(profiles_gr):
        ax = axes[k]
        good = np.isfinite(p_gr.rho_msunh_per_mpch3) & (p_gr.rho_msunh_per_mpch3 > 0)
        if good.any():
            ax.errorbar(
                p_gr.r_centers_mpc_h[good],
                p_gr.rho_msunh_per_mpch3[good],
                yerr=p_gr.rho_err[good],
                fmt="o", color="C0", label=f"GR  (N={p_gr.n_halos_stacked})",
                capsize=2, markersize=4,
            )
            if p_gr.nfw_rho_s is not None:
                rr = np.logspace(
                    np.log10(p_gr.r_centers_mpc_h.min()),
                    np.log10(p_gr.r_centers_mpc_h.max()), 60,
                )
                ax.plot(
                    rr, nfw_rho(rr, p_gr.nfw_rho_s, p_gr.nfw_r_s),
                    "C0--", alpha=0.7,
                    label=f"NFW fit (r_s={p_gr.nfw_r_s:.2f} Mpc/h)",
                )
        if profiles_esd is not None:
            p_e = profiles_esd[k]
            good_e = np.isfinite(p_e.rho_msunh_per_mpch3) & (p_e.rho_msunh_per_mpch3 > 0)
            if good_e.any():
                ax.errorbar(
                    p_e.r_centers_mpc_h[good_e],
                    p_e.rho_msunh_per_mpch3[good_e],
                    yerr=p_e.rho_err[good_e],
                    fmt="s", color="C3",
                    label=f"ESD (N={p_e.n_halos_stacked})",
                    capsize=2, markersize=4,
                )
                if p_e.nfw_rho_s is not None:
                    rr = np.logspace(
                        np.log10(p_e.r_centers_mpc_h.min()),
                        np.log10(p_e.r_centers_mpc_h.max()), 60,
                    )
                    ax.plot(
                        rr, nfw_rho(rr, p_e.nfw_rho_s, p_e.nfw_r_s),
                        "C3--", alpha=0.7,
                        label=f"NFW fit ESD (r_s={p_e.nfw_r_s:.2f} Mpc/h)",
                    )
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel(r"$r\ [Mpc/h]$")
        if k == 0:
            ax.set_ylabel(r"$\rho(r)\ [M_\odot/h\ /\ (Mpc/h)^3]$")
        ax.set_title(
            f"M in [{p_gr.mass_bin_lo:.1e}, {p_gr.mass_bin_hi:.1e}]"
        )
        ax.legend(frameon=False, fontsize=8)
        ax.grid(True, which="both", ls=":", alpha=0.4)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Self-test: plant a known NFW halo and recover (rho_s, r_s).
# ---------------------------------------------------------------------------


def _sample_nfw_radii(
    n: int, r_s: float, r_vir: float, rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Inverse-CDF sampling of r for the NFW radial distribution.

    Mass enclosed: M(<r) = 4 pi rho_s r_s^3 [ ln(1+x) - x/(1+x) ],  x = r/r_s.
    """
    c = r_vir / r_s

    def m_of_x(x): return np.log(1.0 + x) - x / (1.0 + x)
    m_tot = m_of_x(c)
    u = rng.uniform(0.0, 1.0, size=n)
    # solve m(x)/m_tot = u for x via bisection on a log-spaced grid
    x_grid = np.logspace(-3.0, math.log10(c), 4096)
    m_grid = m_of_x(x_grid) / m_tot
    return r_s * np.interp(u, m_grid, x_grid)


def self_test(verbose: bool = True) -> dict:
    rng = np.random.default_rng(20260530)
    box = 50.0
    n_particles = 2000
    r_s_true = 0.3
    r_vir = 2.0
    m_per_part = 1.0e10              # M_sun/h, arbitrary

    # Place an NFW halo at the box centre + a uniform background.
    centre = np.array([box / 2.0, box / 2.0, box / 2.0])
    r = _sample_nfw_radii(n_particles, r_s_true, r_vir, rng)
    theta = np.arccos(2.0 * rng.uniform(size=n_particles) - 1.0)
    phi = 2.0 * math.pi * rng.uniform(size=n_particles)
    halo_pos = centre + np.stack([
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta),
    ], axis=1)
    halo_pos = halo_pos % box
    n_bg = 6000
    bg = rng.uniform(0.0, box, size=(n_bg, 3))
    positions = np.concatenate([halo_pos, bg], axis=0)

    # Mass bin chosen to catch a halo of ~2000 particles. The halo's
    # FOF mass is approximately 2000 * m_per_part = 2e13.
    edges = [1.0e13, 1.0e14]
    profiles = stack_profiles(
        positions, box_mpc_h=box,
        particle_mass_msunh=m_per_part,
        mass_bin_edges=edges,
        n_radial_bins=12,
        r_min_mpc_h=0.05, r_max_mpc_h=2.0,
        min_members=200,
    )
    assert len(profiles) == 1
    p = profiles[0]

    fit_ok = p.nfw_r_s is not None
    # Recovery: r_s within 30 % (limited by background contamination,
    # finite sampling, and FOF-stripped outer particles).
    if fit_ok:
        r_s_recovered = float(p.nfw_r_s)
        rel = abs(r_s_recovered - r_s_true) / r_s_true
    else:
        r_s_recovered = float("nan")
        rel = 1.0
    ok = fit_ok and rel < 0.3 and p.n_halos_stacked >= 1
    if verbose:
        print(f"[prof] halos stacked in bin = {p.n_halos_stacked}")
        print(f"[prof] r_s true             = {r_s_true:.3f} Mpc/h")
        print(f"[prof] r_s recovered        = {r_s_recovered:.3f} Mpc/h")
        print(f"[prof] relative error       = {rel:.3e}  (must be < 0.30)")
        print(f"[prof] {'PASS' if ok else 'FAIL'}")
    return dict(passed=bool(ok), r_s_true=r_s_true, r_s_recovered=r_s_recovered,
                rel_err=rel, n_stacked=p.n_halos_stacked)


if __name__ == "__main__":
    import sys
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
