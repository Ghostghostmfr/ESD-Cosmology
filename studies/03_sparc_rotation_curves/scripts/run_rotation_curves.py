"""Full SPARC rotation-curve analysis (study 03 paper-grade runner).

Reproduces the headline numbers of

  Higginson, J. P. (2026).  Gravity, Electromagnetism, and the Dark
  Sector from a Single Displacement Action with Zero Free Parameters,
  Sec. "SPARC Benchmark Validation".

and of the companion paper

  Higginson, J. P. (2026).  Rotation Curve Predictions for 175 SPARC
  Galaxies from the Golden-Ratio Gravitational Closure.

Procedure (matches paper 1 Sec. SPARC):

  1. Load SPARC master table (data/SPARC_Lelli2016c.mrt) and
     all rotation-curve files (data/Rotmod_LTG/<Galaxy>_rotmod.dat).
     Run `python fetch_sparc_rotmod.py` once to populate the cache;
     the data is shipped with the repo so this is normally a no-op.
  2. For every galaxy, at every measured radius r:
        V_bar^2 = |V_gas|V_gas + Ud|V_disk|V_disk + Ub|V_bul|V_bul
        g_N    = V_bar^2 / r
        V_pred = sqrt( g_N * (1 + R(u)) * r ),  u = 4 g_N / a_0
        V_MOND = sqrt( g_MOND(g_N) * r )
  3. Compute chi^2 against V_obs at both
        (A) fixed M/L  Ud=0.5, Ub=0.7   (zero per-galaxy parameters)
        (B) best-fit Ud, Ub from the published 13x9 grid
            (only Ud, Ub vary; ESD constants stay locked).
  4. Classify each galaxy:
        W if Delta chi^2 = chi^2_ESD - chi^2_MOND < -1,
        L if > 1, otherwise T.
  5. Aggregate W / T / L counts and Sum Delta chi^2.

Outputs:
  outputs/galaxy_results.csv             per-galaxy table
  outputs/rotation_curves_summary.json   headline numbers + reproduction status
  outputs/rotation_curves_summary.txt    human-readable summary
  outputs/all_curves.npz                 V(r) arrays for the figure stage

Exit code: 0 if the published headline numbers reproduce within
tolerance, 1 otherwise, 3 on data error.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from esd_rotation import (  # noqa: E402
    UPS_B_GRID, UPS_D_GRID, UPSILON_BULGE_FIXED, UPSILON_DISK_FIXED,
    chi2, compute_gN, compute_vbar, g_esd_vec, g_mond_vec, vel_from_g,
)

DATA_DIR = os.path.abspath(os.path.join(_HERE, "..", "data"))
MRT_PATH = os.path.join(DATA_DIR, "SPARC_Lelli2016c.mrt")
ROTMOD_DIR = os.path.join(DATA_DIR, "Rotmod_LTG")
OUT_DIR = os.path.join(_HERE, "outputs")

CSV_PATH = os.path.join(OUT_DIR, "galaxy_results.csv")
JSON_PATH = os.path.join(OUT_DIR, "rotation_curves_summary.json")
TXT_PATH = os.path.join(OUT_DIR, "rotation_curves_summary.txt")
NPZ_PATH = os.path.join(OUT_DIR, "all_curves.npz")

TIE_MARGIN: float = 1.0

# Published headline numbers (paper 1 SPARC section).
PUBLISHED = {
    "N_total":        175,
    "grid": {"W": 53, "T": 94, "L": 24, "dchi2_total": -843.0},
    "fixed": {"W": 73, "T": 55, "L": 47, "dchi2_total": -588.0},
    "esd_better_rchi2_fixed": 110,
}
# Tolerances.  W and L are demanding (Delta = +/- 2); T is loosened
# because paper 1 reports the head-to-head on 171 late-type galaxies
# (4 early-type excluded by hand), whereas we run on the full 175 -
# the extra 4 galaxies always land as ties and inflate T by ~4.
TOL = {"wtl_WL": 2, "wtl_T": 6, "dchi2": 30.0, "rchi2_count": 5, "N": 2}


# ------------------------------------------------------------------ loading

def load_galaxy(name: str) -> tuple[np.ndarray, ...] | None:
    fpath = os.path.join(ROTMOD_DIR, f"{name}_rotmod.dat")
    if not os.path.exists(fpath):
        return None
    r, vobs, errv, vgas, vdisk, vbul = [], [], [], [], [], []
    with open(fpath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            try:
                r.append(float(parts[0]))
                vobs.append(float(parts[1]))
                errv.append(float(parts[2]))
                vgas.append(float(parts[3]))
                vdisk.append(float(parts[4]))
                vbul.append(float(parts[5]))
            except ValueError:
                continue
    if not r:
        return None
    return (np.asarray(r), np.asarray(vobs), np.asarray(errv),
            np.asarray(vgas), np.asarray(vdisk), np.asarray(vbul))


def parse_master_table(path: str) -> dict[str, dict]:
    meta: dict[str, dict] = {}
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    data_start = 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith("---"):
            data_start = i + 1
    for ln in lines[data_start:]:
        parts = ln.split()
        if len(parts) < 5:
            continue
        try:
            T = int(parts[1])
        except ValueError:
            continue
        # Q field is one of the last two tokens, depending on the line
        Q = -1
        for tok in parts[-3:]:
            if tok.isdigit():
                Q = int(tok)
                break
        meta[parts[0]] = {"T": T, "Q": Q}
    return meta


# ------------------------------------------------------------------ fitting

def fit_galaxy(payload) -> dict:
    r, vobs, errv, vgas, vdisk, vbul = payload
    N = len(r)

    # (A) fixed M/L
    vbar_fix = compute_vbar(vgas, vdisk, vbul,
                            UPSILON_DISK_FIXED, UPSILON_BULGE_FIXED)
    gN_fix = compute_gN(r, vbar_fix)
    v_esd_fix = vel_from_g(r, g_esd_vec(gN_fix))
    v_mond_fix = vel_from_g(r, g_mond_vec(gN_fix))
    chi2_esd_fix = chi2(v_esd_fix, vobs, errv)
    chi2_mond_fix = chi2(v_mond_fix, vobs, errv)

    # (B) grid search
    best_esd = (UPSILON_DISK_FIXED, UPSILON_BULGE_FIXED, chi2_esd_fix)
    best_mond = (UPSILON_DISK_FIXED, UPSILON_BULGE_FIXED, chi2_mond_fix)
    for ud in UPS_D_GRID:
        for ub in UPS_B_GRID:
            vbar = compute_vbar(vgas, vdisk, vbul, ud, ub)
            gN = compute_gN(r, vbar)
            c2_e = chi2(vel_from_g(r, g_esd_vec(gN)), vobs, errv)
            c2_m = chi2(vel_from_g(r, g_mond_vec(gN)), vobs, errv)
            if c2_e < best_esd[2]:
                best_esd = (ud, ub, c2_e)
            if c2_m < best_mond[2]:
                best_mond = (ud, ub, c2_m)

    vbar_best_esd = compute_vbar(vgas, vdisk, vbul, best_esd[0], best_esd[1])
    v_esd_best = vel_from_g(r, g_esd_vec(compute_gN(r, vbar_best_esd)))
    vbar_best_mond = compute_vbar(vgas, vdisk, vbul, best_mond[0], best_mond[1])
    v_mond_best = vel_from_g(r, g_mond_vec(compute_gN(r, vbar_best_mond)))

    return {
        "N": N,
        "r": r, "vobs": vobs, "errv": errv,
        "vbar_fix": vbar_fix, "vbar_best_esd": vbar_best_esd,
        "v_esd_fix": v_esd_fix, "v_mond_fix": v_mond_fix,
        "v_esd_best": v_esd_best, "v_mond_best": v_mond_best,
        "chi2_esd_fix": chi2_esd_fix, "chi2_mond_fix": chi2_mond_fix,
        "ud_esd": best_esd[0], "ub_esd": best_esd[1], "chi2_esd_grid": best_esd[2],
        "ud_mond": best_mond[0], "ub_mond": best_mond[1], "chi2_mond_grid": best_mond[2],
    }


# ------------------------------------------------------------------ main

def main() -> int:  # noqa: C901
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(MRT_PATH):
        print(f"[rc] master table missing: {MRT_PATH}\n"
              f"     run `python fetch_sparc_rotmod.py` first.", file=sys.stderr)
        return 3
    if not os.path.isdir(ROTMOD_DIR):
        print(f"[rc] Rotmod_LTG dir missing: {ROTMOD_DIR}", file=sys.stderr)
        return 3

    meta = parse_master_table(MRT_PATH)
    names = sorted(f[: -len("_rotmod.dat")]
                   for f in os.listdir(ROTMOD_DIR)
                   if f.endswith("_rotmod.dat"))
    print(f"[rc] analyzing {len(names)} SPARC galaxies "
          f"(grid {len(UPS_D_GRID)}x{len(UPS_B_GRID)}={len(UPS_D_GRID)*len(UPS_B_GRID)})")

    rows: list[dict] = []
    curves: dict[str, np.ndarray] = {}
    t0 = time.time()
    for i, name in enumerate(names):
        payload = load_galaxy(name)
        if payload is None:
            continue
        res = fit_galaxy(payload)
        T = meta.get(name, {}).get("T", -1)
        Q = meta.get(name, {}).get("Q", -1)

        delta_fix = res["chi2_esd_fix"] - res["chi2_mond_fix"]
        delta_grid = res["chi2_esd_grid"] - res["chi2_mond_grid"]
        if delta_grid < -TIE_MARGIN:
            wtl = "W"
        elif delta_grid > TIE_MARGIN:
            wtl = "L"
        else:
            wtl = "T"

        rows.append({
            "name": name, "T": T, "Q": Q, "N": res["N"],
            "chi2_esd_fix": res["chi2_esd_fix"],
            "chi2_mond_fix": res["chi2_mond_fix"],
            "delta_fix": delta_fix,
            "rchi2_esd_fix": res["chi2_esd_fix"] / max(res["N"], 1),
            "rchi2_mond_fix": res["chi2_mond_fix"] / max(res["N"], 1),
            "ud_esd": res["ud_esd"], "ub_esd": res["ub_esd"],
            "chi2_esd_grid": res["chi2_esd_grid"],
            "ud_mond": res["ud_mond"], "ub_mond": res["ub_mond"],
            "chi2_mond_grid": res["chi2_mond_grid"],
            "delta_grid": delta_grid,
            "rchi2_esd_grid": res["chi2_esd_grid"] / max(res["N"] - 1, 1),
            "rchi2_mond_grid": res["chi2_mond_grid"] / max(res["N"] - 1, 1),
            "wtl": wtl,
        })
        for key in ("r", "vobs", "errv",
                    "v_esd_fix", "v_mond_fix",
                    "v_esd_best", "v_mond_best",
                    "vbar_fix", "vbar_best_esd"):
            curves[f"{name}__{key}"] = res[key]

        if (i + 1) % 25 == 0:
            print(f"  [{i+1:3d}/{len(names)}]  elapsed {time.time()-t0:.1f}s")

    print(f"[rc] done in {time.time()-t0:.1f}s ({len(rows)} galaxies)")
    if not rows:
        print("[rc] no galaxies processed.", file=sys.stderr)
        return 3

    # CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Galaxy", "T", "Q", "N",
                    "chi2_ESD_fix", "chi2_MOND_fix", "delta_fix",
                    "rchi2_ESD_fix", "rchi2_MOND_fix",
                    "Ud_ESD", "Ub_ESD", "chi2_ESD_grid",
                    "Ud_MOND", "Ub_MOND", "chi2_MOND_grid",
                    "delta_grid", "rchi2_ESD_grid", "rchi2_MOND_grid", "WTL"])
        for r in rows:
            w.writerow([
                r["name"], r["T"], r["Q"], r["N"],
                f"{r['chi2_esd_fix']:.2f}", f"{r['chi2_mond_fix']:.2f}",
                f"{r['delta_fix']:.2f}",
                f"{r['rchi2_esd_fix']:.3f}", f"{r['rchi2_mond_fix']:.3f}",
                r["ud_esd"], r["ub_esd"], f"{r['chi2_esd_grid']:.2f}",
                r["ud_mond"], r["ub_mond"], f"{r['chi2_mond_grid']:.2f}",
                f"{r['delta_grid']:.2f}",
                f"{r['rchi2_esd_grid']:.3f}", f"{r['rchi2_mond_grid']:.3f}",
                r["wtl"],
            ])
    print(f"[rc] wrote {CSV_PATH}")

    np.savez_compressed(NPZ_PATH, **curves)
    print(f"[rc] wrote {NPZ_PATH}")

    # aggregate
    N_total = len(rows)
    W_grid = sum(1 for r in rows if r["wtl"] == "W")
    T_grid = sum(1 for r in rows if r["wtl"] == "T")
    L_grid = sum(1 for r in rows if r["wtl"] == "L")
    dchi2_grid_total = float(sum(r["delta_grid"] for r in rows))

    W_fix = sum(1 for r in rows if r["delta_fix"] < -TIE_MARGIN)
    T_fix = sum(1 for r in rows if abs(r["delta_fix"]) <= TIE_MARGIN)
    L_fix = sum(1 for r in rows if r["delta_fix"] > TIE_MARGIN)
    dchi2_fix_total = float(sum(r["delta_fix"] for r in rows))
    esd_better_fix = sum(1 for r in rows
                         if r["rchi2_esd_fix"] < r["rchi2_mond_fix"])

    # reproduction check
    def _within(value: float, target: float, tol: float) -> bool:
        return abs(value - target) <= tol

    repro = {
        "N":          _within(N_total, PUBLISHED["N_total"], TOL["N"]),
        "grid_W":     _within(W_grid, PUBLISHED["grid"]["W"], TOL["wtl_WL"]),
        "grid_T":     _within(T_grid, PUBLISHED["grid"]["T"], TOL["wtl_T"]),
        "grid_L":     _within(L_grid, PUBLISHED["grid"]["L"], TOL["wtl_WL"]),
        "grid_dchi2": _within(dchi2_grid_total, PUBLISHED["grid"]["dchi2_total"], TOL["dchi2"]),
        "fixed_W":    _within(W_fix, PUBLISHED["fixed"]["W"], TOL["wtl_WL"]),
        "fixed_T":    _within(T_fix, PUBLISHED["fixed"]["T"], TOL["wtl_T"]),
        "fixed_L":    _within(L_fix, PUBLISHED["fixed"]["L"], TOL["wtl_WL"]),
        "fixed_dchi2": _within(dchi2_fix_total, PUBLISHED["fixed"]["dchi2_total"], TOL["dchi2"]),
        "esd_better_rchi2_fixed": _within(esd_better_fix,
                                          PUBLISHED["esd_better_rchi2_fixed"],
                                          TOL["rchi2_count"]),
    }
    overall_ok = all(repro.values())

    summary = {
        "N_total": N_total,
        "grid": {"W": W_grid, "T": T_grid, "L": L_grid,
                 "dchi2_total": dchi2_grid_total},
        "fixed": {"W": W_fix, "T": T_fix, "L": L_fix,
                  "dchi2_total": dchi2_fix_total,
                  "esd_better_rchi2": esd_better_fix},
        "tie_margin": TIE_MARGIN,
        "published": PUBLISHED,
        "tolerance": TOL,
        "reproduction": repro,
        "overall_reproduction": overall_ok,
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[rc] wrote {JSON_PATH}")

    def _ok(b: bool) -> str:
        return "OK " if b else "OFF"
    lines = [
        "=== Study 03: SPARC rotation-curve analysis ===",
        "  Reproducing Higginson 2026 paper 1 Sec. SPARC + companion paper",
        "",
        f"  Sample:    N = {N_total}   (published: {PUBLISHED['N_total']})  {_ok(repro['N'])}",
        f"  Tie margin: |Delta chi^2| <= {TIE_MARGIN}",
        "",
        "  --- Best-fit M/L from 13x9 grid (paper 1 baseline) ---",
        f"    W / T / L = {W_grid} / {T_grid} / {L_grid}   "
        f"(published: 53 / 94 / 24)  {_ok(repro['grid_W'] and repro['grid_T'] and repro['grid_L'])}",
        f"    Sum Delta chi^2 = {dchi2_grid_total:+.1f}   "
        f"(published: -843)  {_ok(repro['grid_dchi2'])}",
        "",
        "  --- Fixed M/L  (Ud=0.5, Ub=0.7; zero per-galaxy parameters) ---",
        f"    W / T / L = {W_fix} / {T_fix} / {L_fix}   "
        f"(published: 73 / 55 / 47)  {_ok(repro['fixed_W'] and repro['fixed_T'] and repro['fixed_L'])}",
        f"    Sum Delta chi^2 = {dchi2_fix_total:+.1f}   "
        f"(published: -588)  {_ok(repro['fixed_dchi2'])}",
        f"    ESD < MOND on reduced chi^2: {esd_better_fix} galaxies   "
        f"(published: 110)  {_ok(repro['esd_better_rchi2_fixed'])}",
        "",
        f"  overall reproduction within tolerance: {overall_ok}",
    ]
    text = "\n".join(lines) + "\n"
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[rc] wrote {TXT_PATH}\n")
    print(text)
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
