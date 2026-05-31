"""Friends-of-Friends (FOF) halo finder for the ESD N-body sim.

Sub-task 1.4 of simulation 01. The FOF mask produced here is what
gates the R(u) modification in sub-task 1.2b (per Study 19: R(u)
only acts on bound subsystems where axiom A1 holds — a virialised
halo identified by the FOF threshold is the canonical example).

Algorithm
---------
* Compute the mean inter-particle separation
      ell_bar = box / N_particles^(1/3)
* Two particles are "friends" if their periodic separation is less
  than the linking length
      r_link = b * ell_bar      with b = 0.2 (standard cosmological FOF)
* Connected components of the friendship graph are halos.

Implementation uses scipy.spatial.cKDTree (with the ``boxsize`` arg
for native periodic queries) and an explicit union-find. The code
is pure-Python on top of compiled scipy primitives, so it remains
single-threaded — good for the user's "one task at a time" CPU
discipline. For 256^3-particle runs this still completes in seconds.

The output catalog gives, per halo:
    halo_id     : int, sequential 0..N_halos-1
    n_members   : int, particle count
    mass        : float, particle count * particle mass (M_sun/h)
    com_mpc_h   : (3,) float, periodic centre-of-mass
    r_half_mpc_h: float, mass-weighted half-mass radius about the COM
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree


# ---------------------------------------------------------------------------
# Union-find
# ---------------------------------------------------------------------------


class _UnionFind:
    """Union-find with path compression and union by rank."""

    __slots__ = ("parent", "rank")

    def __init__(self, n: int) -> None:
        self.parent = np.arange(n, dtype=np.int64)
        self.rank = np.zeros(n, dtype=np.int32)

    def find(self, i: int) -> int:
        root = i
        while self.parent[root] != root:
            root = int(self.parent[root])
        # path compression
        while self.parent[i] != root:
            nxt = int(self.parent[i])
            self.parent[i] = root
            i = nxt
        return root

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

    def labels(self) -> NDArray[np.int64]:
        # ensure all paths are compressed and produce a dense relabelling.
        roots = np.array([self.find(i) for i in range(len(self.parent))], dtype=np.int64)
        _, inverse = np.unique(roots, return_inverse=True)
        return inverse.astype(np.int64)


# ---------------------------------------------------------------------------
# FOF core
# ---------------------------------------------------------------------------


def mean_interparticle_separation(n_particles: int, box: float) -> float:
    """Mean inter-particle separation = box / N^(1/3)."""
    return float(box) / float(n_particles) ** (1.0 / 3.0)


def fof_labels(
    positions_mpc_h: NDArray[np.float64],
    box_mpc_h: float,
    b: float = 0.2,
) -> NDArray[np.int64]:
    """Run FOF and return one halo label per particle (0..N_halos-1).

    Particles in halos of size 1 are still labelled (every particle
    gets a unique singleton halo). Filtering by ``min_members`` is
    done in :func:`halo_catalog`.
    """
    pos = np.ascontiguousarray(positions_mpc_h, dtype=np.float64)
    n = pos.shape[0]
    ell_bar = mean_interparticle_separation(n, box_mpc_h)
    r_link = b * ell_bar

    tree = cKDTree(pos, boxsize=box_mpc_h)
    pairs = tree.query_pairs(r=r_link, output_type="ndarray")

    uf = _UnionFind(n)
    for i, j in pairs:
        uf.union(int(i), int(j))

    return uf.labels()


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------


@dataclass
class Halo:
    halo_id:      int
    n_members:    int
    mass:         float
    com_mpc_h:    NDArray[np.float64]
    r_half_mpc_h: float


def _periodic_com(
    pos: NDArray[np.float64], box: float
) -> NDArray[np.float64]:
    """Centre of mass on a periodic box via the circular-mean trick."""
    theta = 2.0 * np.pi * pos / box
    xi = np.cos(theta).mean(axis=0)
    zeta = np.sin(theta).mean(axis=0)
    theta_bar = np.arctan2(-zeta, -xi) + np.pi
    return theta_bar * box / (2.0 * np.pi)


def _periodic_delta(
    a: NDArray[np.float64], b: NDArray[np.float64], box: float
) -> NDArray[np.float64]:
    """Minimum-image displacement a - b on a periodic box."""
    d = a - b
    d -= box * np.round(d / box)
    return d


def halo_catalog(
    positions_mpc_h: NDArray[np.float64],
    box_mpc_h: float,
    particle_mass_msun_h: float,
    b: float = 0.2,
    min_members: int = 20,
) -> tuple[list[Halo], NDArray[np.int64]]:
    """Run FOF and build a per-halo catalog above ``min_members``.

    Returns
    -------
    halos : list[Halo]   sorted by descending mass.
    labels: (N,) int     full per-particle labels (-1 for halos that
                         failed the ``min_members`` cut).
    """
    raw_labels = fof_labels(positions_mpc_h, box_mpc_h, b=b)
    n_halos_raw = int(raw_labels.max()) + 1 if raw_labels.size else 0

    # group particle indices by halo id (faster than np.where in a loop)
    order = np.argsort(raw_labels, kind="stable")
    sorted_labels = raw_labels[order]
    boundaries = np.flatnonzero(np.diff(sorted_labels)) + 1
    starts = np.concatenate(([0], boundaries))
    ends = np.concatenate((boundaries, [len(order)]))

    halos: list[Halo] = []
    keep_mask = np.zeros(n_halos_raw, dtype=bool)
    for s, e in zip(starts, ends):
        if e - s < min_members:
            continue
        members = order[s:e]
        keep_mask[int(sorted_labels[s])] = True
        member_pos = positions_mpc_h[members]
        com = _periodic_com(member_pos, box_mpc_h)
        d = _periodic_delta(member_pos, com[None, :], box_mpc_h)
        r = np.linalg.norm(d, axis=1)
        r_sorted = np.sort(r)
        half_idx = max(int(0.5 * len(r_sorted)) - 1, 0)
        halos.append(
            Halo(
                halo_id=-1,                            # reassigned below
                n_members=int(e - s),
                mass=float((e - s) * particle_mass_msun_h),
                com_mpc_h=com,
                r_half_mpc_h=float(r_sorted[half_idx]),
            )
        )

    halos.sort(key=lambda h: -h.n_members)
    for new_id, h in enumerate(halos):
        h.halo_id = new_id

    # Remap labels: kept halos get new_id, dropped particles get -1.
    relabel = np.full(n_halos_raw, -1, dtype=np.int64)
    kept_old_ids = np.flatnonzero(keep_mask)
    # We need to map old_id -> rank-among-kept-sorted-by-mass. Build via halos.
    # Determine each kept halo's particle count, sort by count desc.
    counts = np.zeros(n_halos_raw, dtype=np.int64)
    np.add.at(counts, raw_labels, 1)
    kept_sorted = sorted(kept_old_ids, key=lambda oid: -int(counts[oid]))
    for new_id, oid in enumerate(kept_sorted):
        relabel[oid] = new_id
    labels = relabel[raw_labels]

    return halos, labels


# ---------------------------------------------------------------------------
# Self-test: synthetic clusters + diffuse background
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    """Plant three known compact clusters in a diffuse background and
    verify FOF recovers them with the right multiplicity."""
    rng = np.random.default_rng(20260530)
    box = 100.0  # Mpc/h

    # Diffuse background: 10_000 random particles
    n_bg = 10_000
    bg = rng.uniform(0.0, box, size=(n_bg, 3))

    # Three compact clusters of known size, well separated.
    # Each cluster is tighter than the FOF linking length so it must
    # come back as ONE halo of the planted size.
    planted = [
        ((20.0, 20.0, 20.0), 500),
        ((70.0, 30.0, 50.0), 200),
        ((50.0, 80.0, 60.0), 50),
    ]
    cluster_chunks: list[NDArray[np.float64]] = []
    # cluster radius needs to be << r_link so the cluster collapses
    # to one halo. ell_bar at this density is ~ 100 / (10_000)^(1/3)
    # ~ 4.6 Mpc/h; r_link = 0.2*4.6 ~ 0.93 Mpc/h. Use sigma = 0.1.
    cluster_sigma = 0.1
    for centre, n in planted:
        pts = np.array(centre)[None, :] + cluster_sigma * rng.standard_normal((n, 3))
        cluster_chunks.append(pts % box)
    pos = np.concatenate([bg] + cluster_chunks, axis=0)

    particle_mass = 1.0e10                              # Msun/h, arbitrary
    halos, labels = halo_catalog(
        pos, box_mpc_h=box,
        particle_mass_msun_h=particle_mass,
        b=0.2, min_members=40,
    )

    planted_sizes = sorted([n for _, n in planted], reverse=True)
    recovered_sizes = sorted([h.n_members for h in halos], reverse=True)

    # The first three halos by mass must match the three planted clusters
    # to within stochastic-membership tolerance (no false friends should
    # leak in beyond the linking length).
    top3 = recovered_sizes[:3]
    rel_diffs = [
        abs(t - p) / p for t, p in zip(top3, planted_sizes)
    ] if len(top3) == 3 else [1.0]
    max_rel_diff = max(rel_diffs)

    # Background should produce no halos above min_members=40 at this
    # density (mean separation 4.6 Mpc/h vs linking 0.93 Mpc/h -- well
    # below the FOF percolation threshold).
    expected_background_halos = 0
    # halos beyond the top 3 are spurious background groups
    bg_halo_count = max(len(halos) - 3, 0)

    result = {
        "n_halos_total": len(halos),
        "planted_sizes": planted_sizes,
        "recovered_top3": top3,
        "max_rel_diff_top3": max_rel_diff,
        "background_halo_count": bg_halo_count,
        "expected_background_halos": expected_background_halos,
        "labels_shape": labels.shape,
    }
    ok = (
        len(top3) == 3
        and max_rel_diff < 0.05
        and bg_halo_count == 0
        and labels.shape == (pos.shape[0],)
    )

    if verbose:
        print(f"[fof] particles total       = {pos.shape[0]}")
        print(f"[fof] planted cluster sizes = {planted_sizes}")
        print(f"[fof] recovered top-3 sizes = {top3}")
        print(f"[fof] max |rec - plant|/plant = {max_rel_diff:.3e}")
        print(f"[fof] background halos      = {bg_halo_count}"
              f"  (expected {expected_background_halos})")
        print(f"[fof] total halos returned  = {len(halos)}")
        print(f"[fof] {'PASS' if ok else 'FAIL'}")

    result["passed"] = ok
    return result


if __name__ == "__main__":
    import sys

    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
