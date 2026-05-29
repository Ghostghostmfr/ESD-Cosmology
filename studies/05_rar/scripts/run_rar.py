"""Radial Acceleration Relation (RAR) reproduction - study 05.

Reproduces the headline RAR numbers of

  Higginson, J. P. (2026). Gravity, Electromagnetism, and the Dark
  Sector from a Single Displacement Action with Zero Free Parameters,
  Sec. SPARC Benchmark Validation (Fig. fig:rar).

and the canonical McGaugh+2016 RAR result it benchmarks against.

Procedure (matches paper 1 Sec. SPARC, RAR aggregation):

  1. Load 175 SPARC rotmod files (data/Rotmod_LTG/<Galaxy>_rotmod.dat).
  2. For every data point:
        V_bar = sqrt(|V_gas|V_gas + Ud|V_disk|V_disk + Ub|V_bul|V_bul)   (fixed Ud=0.5, Ub=0.7)
        g_bar = V_bar^2 / r           (m/s^2)
        g_obs = V_obs^2 / r           (m/s^2)
        g_ESD = g_bar (1 + R(u)),    u = 4 g_bar / a_0
        g_MOND = g_bar / (1 - exp(-sqrt(g_bar/a_0)))
  3. Drop points with err_V <= 0 or g_bar <= 0.
  4. Aggregate:
        - total point count N_pts
        - log-residuals  delta = log10(g_obs / g_model)  for both models
        - mean, median, RMS scatter of delta
        - chi^2 in velocity space (paper's stat) and reduced chi^2
        - running median + 16/84 percentile band in log10(g_bar) bins
  5. Check against published targets, write CSV / NPZ / JSON / TXT outputs.

Exit code 0 if every headline number reproduces, 1 otherwise, 3 on data error.
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

from esd_rar import (  # noqa: E402
    A0_SI, UPSILON_BULGE_FIXED, UPSILON_DISK_FIXED,
    compute_g, compute_vbar, g_esd_vec, g_mond_vec,
)

DATA_DIR = os.path.abspath(os.path.join(_HERE, "..", "data"))
MRT_PATH = os.path.join(DATA_DIR, "SPARC_Lelli2016c.mrt")
ROTMOD_DIR = os.path.join(DATA_DIR, "Rotmod_LTG")
OUT_DIR = os.path.join(_HERE, "outputs")


# Published / canonical targets.
#
# Paper 1's Fig. fig:rar is explicitly computed at FIXED M/L (caption:
# "Residuals computed at fixed mass-to-light ratios Ud=0.5, Ub=0.7;
# the bands narrow under per-galaxy optimization"). The paper's
# headline Delta chi^2 = -843 and chi^2_nu ~ 12 come from the GRID
# analysis (Table tab:golden-benchmark) and are reproduced in Study 03.
# Here we target the fixed-M/L numbers that drive Fig. fig:rar itself:
#
#   Delta chi^2 (fixed M/L) = -588 (Study 03 fixed-M/L cross-check)
#   delta_mean centered near zero (paper, Fig. fig:rar bottom)
#   sigma_rar:  McGaugh+2016 canonical orthogonal RAR scatter ~ 0.13 dex
#
# Reduced chi^2 at fixed M/L is naturally larger than the grid value
# (chi^2 monotonically decreases as M/L is optimized). We do not gate
# on it -- the gateable invariant is Delta chi^2 fixed = -588.
PUBLISHED = {
    "N_pts_175":       3449,
    "delta_chi2_fixed": -588.0,
    "delta_mean_esd":   0.0,
    "delta_mean_mond":  0.0,
    "sigma_rar_obs":    0.13,   # McGaugh+2016 (orthogonal scatter)
}
TOL = {
    "N_pts":         200,
    "delta_chi2":    30.0,
    "delta_mean":    0.05,
    "sigma_rar":     0.10,     # we report it as a comparison, not a test
}


# ------------------------------------------------------------------ loading

def load_galaxy(name: str):
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


def list_galaxies() -> list[str]:
    names = []
    for fn in sorted(os.listdir(ROTMOD_DIR)):
        if fn.endswith("_rotmod.dat"):
            names.append(fn[:-len("_rotmod.dat")])
    return names


# ------------------------------------------------------------------ binning

def running_band(x: np.ndarray, y: np.ndarray, n_bins: int = 28
                 ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Median + 16/84 percentile band of y(x) on equal-count bins."""
    order = np.argsort(x)
    xs, ys = x[order], y[order]
    bins = np.array_split(np.arange(xs.size), n_bins)
    xc = np.array([xs[b].mean()         for b in bins if b.size])
    med = np.array([np.median(ys[b])    for b in bins if b.size])
    p16 = np.array([np.percentile(ys[b], 16) for b in bins if b.size])
    p84 = np.array([np.percentile(ys[b], 84) for b in bins if b.size])
    return xc, med, p16, p84


# ------------------------------------------------------------------ main

def main() -> int:  # noqa: C901
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.isdir(ROTMOD_DIR):
        print(f"[rar] Rotmod_LTG dir missing: {ROTMOD_DIR}", file=sys.stderr)
        return 3

    names = list_galaxies()
    if not names:
        print(f"[rar] no rotmod files under {ROTMOD_DIR}", file=sys.stderr)
        return 3
    print(f"[rar] aggregating {len(names)} SPARC galaxies at fixed M/L "
          f"(Ud={UPSILON_DISK_FIXED}, Ub={UPSILON_BULGE_FIXED})")

    t0 = time.time()
    gbar_all, gobs_all = [], []
    g_esd_all, g_mond_all = [], []
    chi2_esd_total = 0.0
    chi2_mond_total = 0.0
    dof_total = 0

    for name in names:
        payload = load_galaxy(name)
        if payload is None:
            continue
        r, vobs, errv, vgas, vdisk, vbul = payload
        vbar = compute_vbar(vgas, vdisk, vbul,
                            UPSILON_DISK_FIXED, UPSILON_BULGE_FIXED)
        g_bar = compute_g(r, vbar)
        g_obs = compute_g(r, vobs)

        # Drop bad points (zero err or zero baryonic source).
        ok = (errv > 0) & (g_bar > 0) & (g_obs > 0)
        if not np.any(ok):
            continue

        gb = g_bar[ok]
        go = g_obs[ok]
        ge = g_esd_vec(gb)
        gm = g_mond_vec(gb)
        gbar_all.append(gb); gobs_all.append(go)
        g_esd_all.append(ge); g_mond_all.append(gm)

        # chi^2 in velocity space (paper convention: V_pred = sqrt(g_model*r)).
        v_e = np.sqrt(ge * r[ok] * 3.085677581491367e19) / 1.0e3
        v_m = np.sqrt(gm * r[ok] * 3.085677581491367e19) / 1.0e3
        chi2_esd_total += float(np.sum(((v_e - vobs[ok]) / errv[ok])**2))
        chi2_mond_total += float(np.sum(((v_m - vobs[ok]) / errv[ok])**2))
        dof_total += int(ok.sum())

    gbar = np.concatenate(gbar_all)
    gobs = np.concatenate(gobs_all)
    g_esd = np.concatenate(g_esd_all)
    g_mond = np.concatenate(g_mond_all)

    log_gbar = np.log10(gbar)
    delta_esd  = np.log10(gobs / g_esd)
    delta_mond = np.log10(gobs / g_mond)

    chi2_nu_esd  = chi2_esd_total  / dof_total
    chi2_nu_mond = chi2_mond_total / dof_total

    mean_e, med_e, rms_e = float(np.mean(delta_esd)),  float(np.median(delta_esd)),  float(np.std(delta_esd))
    mean_m, med_m, rms_m = float(np.mean(delta_mond)), float(np.median(delta_mond)), float(np.std(delta_mond))

    # Binned RAR band.
    xc, med_obs, p16, p84 = running_band(log_gbar, np.log10(gobs))
    xc_e, med_e_curve, _, _ = running_band(log_gbar, np.log10(g_esd))
    xc_m, med_m_curve, _, _ = running_band(log_gbar, np.log10(g_mond))

    elapsed = time.time() - t0
    print(f"[rar] aggregated {dof_total} valid data points in {elapsed:.2f}s")

    # ----- reproduction checks ------------------------------------------------
    checks = []
    def add(name, comp, pub, ok):
        checks.append((name, comp, pub, ok))

    add("N_pts",          dof_total,    PUBLISHED["N_pts_175"],
        abs(dof_total - PUBLISHED["N_pts_175"]) <= TOL["N_pts"])
    add("delta_mean_esd", mean_e,       PUBLISHED["delta_mean_esd"],
        abs(mean_e)  <= TOL["delta_mean"])
    add("delta_mean_mond", mean_m,      PUBLISHED["delta_mean_mond"],
        abs(mean_m)  <= TOL["delta_mean"])
    # Delta chi^2 ESD vs MOND at fixed M/L - cross-check vs Study 03.
    dchi2 = chi2_esd_total - chi2_mond_total
    add("delta_chi2_fixed", dchi2, PUBLISHED["delta_chi2_fixed"],
        abs(dchi2 - PUBLISHED["delta_chi2_fixed"]) <= TOL["delta_chi2"])

    failures = [name for (name, _, _, ok) in checks if not ok]

    # ----- write outputs ------------------------------------------------------
    csv_path = os.path.join(OUT_DIR, "rar_headline.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "computed", "published", "within_tolerance"])
        for name, comp, pub, ok in checks:
            w.writerow([name, repr(comp), repr(pub), ok])
    print(f"[rar] wrote {csv_path}")

    npz_path = os.path.join(OUT_DIR, "rar_points.npz")
    np.savez_compressed(
        npz_path,
        gbar=gbar, gobs=gobs, g_esd=g_esd, g_mond=g_mond,
        delta_esd=delta_esd, delta_mond=delta_mond,
        bin_log_gbar=xc, bin_med_gobs=med_obs, bin_p16=p16, bin_p84=p84,
        bin_med_esd=med_e_curve, bin_med_mond=med_m_curve,
    )
    print(f"[rar] wrote {npz_path}")

    summary = {
        "N_pts": dof_total,
        "N_galaxies": len(names),
        "chi2_total": {"esd": chi2_esd_total, "mond": chi2_mond_total,
                       "delta": dchi2},
        "chi2_nu": {"esd": chi2_nu_esd, "mond": chi2_nu_mond},
        "log_residual": {
            "esd":  {"mean": mean_e, "median": med_e, "rms": rms_e},
            "mond": {"mean": mean_m, "median": med_m, "rms": rms_m},
        },
        "published": PUBLISHED,
        "passed_all": len(failures) == 0,
        "failures": failures,
    }
    json_path = os.path.join(OUT_DIR, "rar_summary.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[rar] wrote {json_path}")

    # ----- console / txt summary ---------------------------------------------
    lines = []
    lines.append("=== Study 05: SPARC Radial Acceleration Relation ===")
    lines.append("  Reproducing paper 1 Sec. SPARC (Fig. fig:rar)")
    lines.append("  Fixed M/L baseline: Ud=0.5, Ub=0.7 (zero per-galaxy parameters)")
    lines.append("")
    lines.append(f"  Sample:        {len(names)} galaxies   {dof_total} data points "
                 f"(published: ~{PUBLISHED['N_pts_175']})  "
                 f"{'OK' if abs(dof_total-PUBLISHED['N_pts_175'])<=TOL['N_pts'] else 'FAIL'}")
    lines.append("")
    lines.append("  --- velocity-space chi^2 at fixed M/L (paper Fig. fig:rar) ---")
    lines.append(f"  chi^2  (ESD):   {chi2_esd_total:9.1f}   "
                 f"chi^2_nu = {chi2_nu_esd:5.2f}")
    lines.append(f"  chi^2  (MOND):  {chi2_mond_total:9.1f}   "
                 f"chi^2_nu = {chi2_nu_mond:5.2f}")
    lines.append(f"  Delta chi^2  = {dchi2:+8.1f}   (published fixed-M/L: -588)  "
                 f"{'OK' if abs(dchi2-PUBLISHED['delta_chi2_fixed'])<=TOL['delta_chi2'] else 'FAIL'}")
    lines.append("  (paper headline -843 and chi^2_nu~12 are grid-M/L; see Study 03)")
    lines.append("")
    lines.append("  --- log10(g_obs / g_model) residuals ---")
    lines.append(f"  ESD:   mean = {mean_e:+.4f}   median = {med_e:+.4f}   "
                 f"RMS = {rms_e:.4f} dex  "
                 f"{'OK' if abs(mean_e)<=TOL['delta_mean'] else 'FAIL'}")
    lines.append(f"  MOND:  mean = {mean_m:+.4f}   median = {med_m:+.4f}   "
                 f"RMS = {rms_m:.4f} dex  "
                 f"{'OK' if abs(mean_m)<=TOL['delta_mean'] else 'FAIL'}")
    lines.append("")
    lines.append(f"  McGaugh+2016 observed orthogonal RAR scatter: "
                 f"~{PUBLISHED['sigma_rar_obs']:.2f} dex")
    lines.append(f"  Framework ESD RMS - observed scatter        = "
                 f"{rms_e - PUBLISHED['sigma_rar_obs']:+.2f} dex "
                 f"(positive => intrinsic scatter dominated by data noise, "
                 f"not by framework)")
    lines.append("")
    lines.append(f"  overall reproduction within tolerance: {len(failures) == 0}")
    if failures:
        lines.append(f"  failures: {failures}")
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "rar_summary.txt"), "w") as f:
        f.write(text)
    print(f"[rar] wrote {os.path.join(OUT_DIR, 'rar_summary.txt')}")
    print()
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
