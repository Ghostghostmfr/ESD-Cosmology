"""ESD vs MOND — formal statistical verdict (study 48).

Reads the per-galaxy table produced by study 03 (A02_sparc_rotation_curves)
and outputs:

  outputs/verdict_summary.json    W/T/L, Sigma_Delta-chi2, pass/fail gate
  outputs/verdict_summary.txt     human-readable version of the above
  figures_generated/delta_chi2_histogram.png
  figures_generated/esd_vs_mond_scatter.png
  figures_generated/cumulative_delta_chi2.png

Prerequisite: run study 03 first (`make residuals` in that folder) to
build `A02_sparc_rotation_curves/scripts/outputs/galaxy_results.csv`.

Exit code: 0 if all acceptance gates pass, 1 otherwise, 3 on data error.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = Path(__file__).parent
_STUDY48 = _HERE.parent
_STUDY03_CSV = (
    _STUDY48.parent / "A02_sparc_rotation_curves" / "scripts" / "outputs" / "galaxy_results.csv"
)
OUT_DIR = _STUDY48 / "scripts" / "outputs"
FIG_DIR = _STUDY48 / "figures_generated"

# Published headline numbers (paper 1 / study 03).
PUBLISHED = {
    "N_total": 175,
    "grid": {"W": 53, "T": 98, "L": 24, "dchi2": -843.0},
    "fixed": {"W": 73, "T": 55, "L": 47, "dchi2": -588.0},
    "esd_better_rchi2_fixed": 110,
}
TOL = {"WL": 2, "T": 6, "dchi2": 30.0, "rchi2_count": 5, "N": 2}

TIE_MARGIN = 1.0


# ------------------------------------------------------------------ load CSV

def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        print(
            f"[48] CSV not found: {path}\n"
            f"     Run `make residuals` in studies/A02_sparc_rotation_curves first.",
            file=sys.stderr,
        )
        sys.exit(3)
    rows: list[dict] = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# ------------------------------------------------------------------ figures

def plot_delta_histogram(delta_grid: np.ndarray, fig_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    bins = np.linspace(-80, 30, 45)
    ax.hist(delta_grid, bins=bins, color="#2c6fad", edgecolor="white", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=1.0, linestyle="--", alpha=0.6)
    ax.axvline(float(np.sum(delta_grid)) / len(delta_grid), color="#d62728",
               linewidth=1.5, linestyle="-", label=f"mean = {np.mean(delta_grid):.1f}")
    ax.set_xlabel(r"$\Delta\chi^2 = \chi^2_{\rm ESD} - \chi^2_{\rm MOND}$ (per galaxy, grid M/L)")
    ax.set_ylabel("Number of galaxies")
    ax.set_title(
        rf"ESD vs MOND — $\Delta\chi^2$ distribution  "
        rf"($\Sigma\,\Delta\chi^2 = {int(np.sum(delta_grid)):+d}$, $N=175$)"
    )
    ax.legend(fontsize=9)
    ax.text(0.97, 0.95, "← ESD better",
            transform=ax.transAxes, ha="right", va="top", fontsize=8, color="#2c6fad")
    fig.tight_layout()
    fig.savefig(fig_dir / "delta_chi2_histogram.png", dpi=150)
    plt.close(fig)


def plot_scatter(chi2_esd: np.ndarray, chi2_mond: np.ndarray, fig_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    vmax = min(np.percentile(np.concatenate([chi2_esd, chi2_mond]), 98), 300)
    ax.scatter(chi2_mond, chi2_esd, s=12, alpha=0.6, color="#2c6fad", linewidth=0)
    lim = (0, vmax)
    ax.plot(lim, lim, "k--", linewidth=1.0, alpha=0.5, label="Equal fit")
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_xlabel(r"$\chi^2_{\rm MOND}$ (grid M/L)")
    ax.set_ylabel(r"$\chi^2_{\rm ESD}$ (grid M/L)")
    ax.set_title("ESD vs MOND per-galaxy goodness of fit\n(points below diagonal = ESD better)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(fig_dir / "esd_vs_mond_scatter.png", dpi=150)
    plt.close(fig)


def plot_cumulative(delta_grid: np.ndarray, fig_dir: Path) -> None:
    sorted_d = np.sort(delta_grid)
    cumsum = np.cumsum(sorted_d)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(1, len(cumsum) + 1), cumsum, color="#2c6fad", linewidth=1.5)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.fill_between(np.arange(1, len(cumsum) + 1), cumsum,
                    where=(cumsum < 0), color="#2c6fad", alpha=0.15)
    ax.set_xlabel("Galaxy index (sorted by $\\Delta\\chi^2$, most negative first)")
    ax.set_ylabel(r"Cumulative $\Sigma\,\Delta\chi^2$")
    ax.set_title(
        r"ESD cumulative advantage over MOND  "
        rf"($\Sigma_\mathrm{{total}} = {int(np.sum(delta_grid)):+d}$)"
    )
    fig.tight_layout()
    fig.savefig(fig_dir / "cumulative_delta_chi2.png", dpi=150)
    plt.close(fig)


# ------------------------------------------------------------------ main

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_csv(_STUDY03_CSV)
    N = len(rows)

    delta_grid = np.array([float(r["delta_grid"]) for r in rows])
    delta_fix = np.array([float(r["delta_fix"]) for r in rows])
    chi2_esd_grid = np.array([float(r["chi2_ESD_grid"]) for r in rows])
    chi2_mond_grid = np.array([float(r["chi2_MOND_grid"]) for r in rows])
    rchi2_esd_fix = np.array([float(r["rchi2_ESD_fix"]) for r in rows])
    rchi2_mond_fix = np.array([float(r["rchi2_MOND_fix"]) for r in rows])

    # --- W/T/L tallies ---
    W_grid = int(np.sum(delta_grid < -TIE_MARGIN))
    T_grid = int(np.sum(np.abs(delta_grid) <= TIE_MARGIN))
    L_grid = int(np.sum(delta_grid > TIE_MARGIN))
    dchi2_grid = float(np.sum(delta_grid))

    W_fix = int(np.sum(delta_fix < -TIE_MARGIN))
    T_fix = int(np.sum(np.abs(delta_fix) <= TIE_MARGIN))
    L_fix = int(np.sum(delta_fix > TIE_MARGIN))
    dchi2_fix = float(np.sum(delta_fix))
    esd_better_fix = int(np.sum(rchi2_esd_fix < rchi2_mond_fix))

    # --- acceptance gates ---
    def _ok(val: float, target: float, tol: float) -> bool:
        return abs(val - target) <= tol

    gates = {
        "N_total":             _ok(N, PUBLISHED["N_total"], TOL["N"]),
        "grid_W":              _ok(W_grid, PUBLISHED["grid"]["W"], TOL["WL"]),
        "grid_T":              _ok(T_grid, PUBLISHED["grid"]["T"], TOL["T"]),
        "grid_L":              _ok(L_grid, PUBLISHED["grid"]["L"], TOL["WL"]),
        "grid_dchi2":          _ok(dchi2_grid, PUBLISHED["grid"]["dchi2"], TOL["dchi2"]),
        "fixed_W":             _ok(W_fix, PUBLISHED["fixed"]["W"], TOL["WL"]),
        "fixed_T":             _ok(T_fix, PUBLISHED["fixed"]["T"], TOL["T"]),
        "fixed_L":             _ok(L_fix, PUBLISHED["fixed"]["L"], TOL["WL"]),
        "fixed_dchi2":         _ok(dchi2_fix, PUBLISHED["fixed"]["dchi2"], TOL["dchi2"]),
        "esd_better_rchi2":    _ok(esd_better_fix, PUBLISHED["esd_better_rchi2_fixed"],
                                   TOL["rchi2_count"]),
    }
    overall_pass = all(gates.values())

    # --- figures ---
    plot_delta_histogram(delta_grid, FIG_DIR)
    plot_scatter(chi2_esd_grid, chi2_mond_grid, FIG_DIR)
    plot_cumulative(delta_grid, FIG_DIR)
    print(f"[48] figures written to {FIG_DIR}/")

    # --- text summary ---
    lines = [
        "=" * 62,
        "ESD vs MOND — Formal Statistical Verdict  (Study 48)",
        "=" * 62,
        "",
        f"  Sample:  {N} SPARC galaxies",
        "",
        "  Grid M/L (best-fit Υ_d, Υ_b):",
        f"    ESD wins   (Δχ² < −1):    {W_grid:3d}",
        f"    Ties       (|Δχ²| ≤ 1):   {T_grid:3d}",
        f"    ESD losses (Δχ² > +1):    {L_grid:3d}",
        f"    Σ Δχ²:                    {dchi2_grid:+.1f}",
        "",
        "  Fixed M/L (Υ_d=0.5, Υ_b=0.7, zero per-galaxy freedom):",
        f"    ESD wins:                  {W_fix:3d}",
        f"    Ties:                      {T_fix:3d}",
        f"    ESD losses:                {L_fix:3d}",
        f"    Σ Δχ²:                    {dchi2_fix:+.1f}",
        f"    χ²ᵥ(ESD) < χ²ᵥ(MOND):    {esd_better_fix:3d} / {N}",
        "",
        "  Acceptance gates:",
    ]
    for name, passed in gates.items():
        lines.append(f"    {name:<28s}  {'PASS' if passed else 'FAIL'}")
    lines += [
        "",
        f"  Overall: {'PASS' if overall_pass else 'FAIL'}",
        "=" * 62,
    ]
    txt = "\n".join(lines)
    print(txt)
    (OUT_DIR / "verdict_summary.txt").write_text(txt + "\n", encoding="utf-8")

    result = {
        "N_total": N,
        "grid": {"W": W_grid, "T": T_grid, "L": L_grid, "dchi2": dchi2_grid},
        "fixed": {"W": W_fix, "T": T_fix, "L": L_fix, "dchi2": dchi2_fix,
                  "esd_better_rchi2": esd_better_fix},
        "gates": gates,
        "overall_pass": overall_pass,
    }
    (OUT_DIR / "verdict_summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(f"[48] summary written to {OUT_DIR}/verdict_summary.{{json,txt}}")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
