"""Reproduce the rotation-curve paper's figure set from outputs/.

Three figures:
  fig_gallery.png          12-galaxy gallery (4 ESD wins, 4 ties, 4 MOND wins).
  fig_delta_hist.png       Distribution of grid-search Delta chi^2 = chi^2_ESD - chi^2_MOND.
  fig_rchi2_scatter.png    Per-galaxy ESD vs MOND reduced chi^2 (fixed M/L).
"""

from __future__ import annotations

import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
NPZ_PATH = os.path.join(_HERE, "outputs", "all_curves.npz")
CSV_PATH = os.path.join(_HERE, "outputs", "galaxy_results.csv")
FIG_DIR = os.path.abspath(os.path.join(_HERE, "..", "figures_generated"))


def _load_rows() -> list[dict]:
    rows: list[dict] = []
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in ("N", "T", "Q"):
                row[key] = int(row[key])
            for key in ("chi2_ESD_fix", "chi2_MOND_fix", "delta_fix",
                        "rchi2_ESD_fix", "rchi2_MOND_fix",
                        "chi2_ESD_grid", "chi2_MOND_grid", "delta_grid",
                        "rchi2_ESD_grid", "rchi2_MOND_grid"):
                row[key] = float(row[key])
            rows.append(row)
    return rows


def _gallery_fig(rows: list[dict], npz) -> None:
    wins = sorted([r for r in rows if r["WTL"] == "W"], key=lambda r: r["delta_grid"])[:4]
    ties = [r for r in rows if r["WTL"] == "T"]
    if len(ties) >= 4:
        ties_sel = [ties[len(ties)//8], ties[3*len(ties)//8],
                    ties[5*len(ties)//8], ties[7*len(ties)//8]]
    else:
        ties_sel = ties
    losses = sorted([r for r in rows if r["WTL"] == "L"],
                    key=lambda r: r["delta_grid"], reverse=True)[:4]
    picks = [("ESD wins", wins, "#0d3b66"),
             ("Ties",     ties_sel, "#114b5f"),
             ("MOND wins", losses, "#d7263d")]

    fig, axes = plt.subplots(3, 4, figsize=(15.5, 9.2), sharex=False, sharey=False)
    for row_idx, (label, picks_row, color) in enumerate(picks):
        for col_idx in range(4):
            ax = axes[row_idx, col_idx]
            if col_idx >= len(picks_row):
                ax.axis("off")
                continue
            row = picks_row[col_idx]
            name = row["Galaxy"]
            try:
                r = npz[f"{name}__r"]
                vobs = npz[f"{name}__vobs"]
                errv = npz[f"{name}__errv"]
                v_esd = npz[f"{name}__v_esd_best"]
                v_mond = npz[f"{name}__v_mond_best"]
                vbar = npz[f"{name}__vbar_best_esd"]
            except KeyError:
                ax.text(0.5, 0.5, f"(no data for {name})",
                        transform=ax.transAxes, ha="center")
                continue
            ax.errorbar(r, vobs, yerr=errv, fmt="o", ms=2.6, color="black",
                        ecolor="0.55", lw=0.5, alpha=0.8, label="SPARC")
            ax.plot(r, vbar, "--", color="#888", lw=1.0, label=r"$V_{\rm bar}$")
            ax.plot(r, v_mond, ":", color="#d7263d", lw=1.4,
                    label=f"MOND (rchi2={row['rchi2_MOND_grid']:.2f})")
            ax.plot(r, v_esd, "-", color="#0d3b66", lw=1.6,
                    label=f"ESD (rchi2={row['rchi2_ESD_grid']:.2f})")
            ax.set_title(name, fontsize=10)
            ax.grid(True, alpha=0.3)
            if col_idx == 0:
                ax.set_ylabel(f"{label}\nV [km/s]", fontsize=10, color=color)
            if row_idx == 2:
                ax.set_xlabel("r [kpc]", fontsize=10)
            if row_idx == 0 and col_idx == 0:
                ax.legend(fontsize=7, loc="lower right")
    fig.suptitle("SPARC rotation-curve gallery: ESD vs MOND (best-fit M/L)",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out_png = os.path.join(FIG_DIR, "fig_gallery.png")
    out_pdf = os.path.join(FIG_DIR, "fig_gallery.pdf")
    fig.savefig(out_png, dpi=160)
    fig.savefig(out_pdf)
    plt.close(fig)
    print(f"[fig] wrote {out_png}")
    print(f"[fig] wrote {out_pdf}")


def _delta_hist_fig(rows: list[dict]) -> None:
    delta_grid = np.array([r["delta_grid"] for r in rows])
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    bins = np.linspace(-60, 60, 41)
    ax.hist(np.clip(delta_grid, bins[0], bins[-1]), bins=bins,
            color="#0d3b66", alpha=0.85, edgecolor="white")
    ax.axvline(0, color="k", lw=1.0)
    ax.axvspan(-1, 1, color="0.85", alpha=0.6, label="tie margin")
    ax.set_xlabel(r"$\Delta\chi^2 = \chi^2_{\rm ESD} - \chi^2_{\rm MOND}$ "
                  "(best-fit M/L grid, clipped to $\\pm 60$)")
    ax.set_ylabel("Number of galaxies")
    ax.set_title("Per-galaxy $\\Delta\\chi^2$ distribution "
                 f"(N={len(delta_grid)}, $\\sum\\Delta\\chi^2 = {delta_grid.sum():+.0f}$)")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_png = os.path.join(FIG_DIR, "fig_delta_hist.png")
    out_pdf = os.path.join(FIG_DIR, "fig_delta_hist.pdf")
    fig.savefig(out_png, dpi=160)
    fig.savefig(out_pdf)
    plt.close(fig)
    print(f"[fig] wrote {out_png}")
    print(f"[fig] wrote {out_pdf}")


def _rchi2_scatter_fig(rows: list[dict]) -> None:
    r_esd = np.array([r["rchi2_ESD_fix"] for r in rows])
    r_mond = np.array([r["rchi2_MOND_fix"] for r in rows])
    wtl = np.array([r["WTL"] for r in rows])
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    diag = np.array([1e-2, 1e3])
    ax.plot(diag, diag, "k--", lw=1.0, alpha=0.7, label="equal $\\chi^2_\\nu$")
    masks = [(wtl == "W", "ESD better (W)", "#0d3b66"),
             (wtl == "T", "Tie",             "#888888"),
             (wtl == "L", "MOND better (L)", "#d7263d")]
    for m, lab, col in masks:
        ax.scatter(r_mond[m], r_esd[m], s=18, alpha=0.75, color=col,
                   edgecolor="white", linewidth=0.4, label=lab)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.05, 200)
    ax.set_ylim(0.05, 200)
    ax.set_xlabel(r"MOND reduced $\chi^2$ (fixed $\Upsilon_d=0.5,\Upsilon_b=0.7$)")
    ax.set_ylabel(r"ESD reduced $\chi^2$ (fixed $\Upsilon_d=0.5,\Upsilon_b=0.7$)")
    ax.set_title(f"Per-galaxy reduced $\\chi^2$: ESD vs MOND (N={len(r_esd)})")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    out_png = os.path.join(FIG_DIR, "fig_rchi2_scatter.png")
    out_pdf = os.path.join(FIG_DIR, "fig_rchi2_scatter.pdf")
    fig.savefig(out_png, dpi=160)
    fig.savefig(out_pdf)
    plt.close(fig)
    print(f"[fig] wrote {out_png}")
    print(f"[fig] wrote {out_pdf}")


def main() -> int:
    if not os.path.exists(NPZ_PATH) or not os.path.exists(CSV_PATH):
        print("[fig] outputs missing; run `python run_rotation_curves.py` first.",
              file=sys.stderr)
        return 1
    os.makedirs(FIG_DIR, exist_ok=True)
    rows = _load_rows()
    npz = np.load(NPZ_PATH, allow_pickle=True)
    _gallery_fig(rows, npz)
    _delta_hist_fig(rows)
    _rchi2_scatter_fig(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
