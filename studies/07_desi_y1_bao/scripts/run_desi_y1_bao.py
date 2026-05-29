"""Study 07: DESI Y1 BAO chi^2 reproduction.

For each candidate cosmology compute the theoretical
(D_M/r_d, D_H/r_d, D_V/r_d) at every DESI Y1 tracer, then a chi^2 with
each tracer's 2x2 (or scalar) within-tracer covariance:

    chi^2 = sum_tracers  d^T C^{-1} d,    d = (theory - data)

Acceptance:
  * |Delta chi^2 (ESD - Planck-LCDM)| <= 5  for the PRIMARY reading.
    DESI Y1 reports chi^2/dof ~ 1 for the best-fit flat LCDM
    (arXiv:2404.03002 Sec. 4.1); any framework whose locked
    (Omega_m, Omega_b, h) sits within ~1 sigma of Planck must
    reproduce this to within a handful of chi^2 units, regardless
    of the precise r_d calibration constant.

Discriminator reported (not gated): chi^2(CLOSURE-POOL) - chi^2(PRIMARY).
DESI Y1 prefers the lower-omega_b reading iff this is positive.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from typing import Dict, List

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from desi_y1_data import DESI_Y1, DMDH, DV, N_MEAS  # noqa: E402
from esd_bao import (  # noqa: E402
    Cosmo,
    D_H,
    D_M,
    D_V,
    cosmo_esd_closure_pool,
    cosmo_esd_primary,
    cosmo_planck_lcdm,
    r_d_aubourg2015,
)

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

DELTA_CHI2_GATE = 5.0   # PRIMARY reading vs Planck-LCDM baseline


def theory_row(c: Cosmo, z: float, kind: str, rd: float) -> Dict[str, float]:
    if kind == "DV":
        return {"DV_rd": D_V(c, z) / rd}
    return {
        "DM_rd": D_M(c, z) / rd,
        "DH_rd": D_H(c, z) / rd,
    }


def chi2_single(c: Cosmo) -> Dict[str, object]:
    rd = r_d_aubourg2015(c)
    chi2 = 0.0
    per_tracer: List[dict] = []
    for t in DESI_Y1:
        if isinstance(t, DV):
            th = D_V(c, t.z_eff) / rd
            d  = th - t.DV_rd
            tx = (d / t.sigma) ** 2
            chi2 += tx
            per_tracer.append({
                "name":   t.name, "z": t.z_eff,
                "th_DV":  th,    "data_DV": t.DV_rd,
                "sigma":  t.sigma, "chi2_tracer": tx,
            })
        else:
            th_M = D_M(c, t.z_eff) / rd
            th_H = D_H(c, t.z_eff) / rd
            dM = th_M - t.DM_rd
            dH = th_H - t.DH_rd
            cov = np.array([
                [t.DM_sig ** 2,           t.rho * t.DM_sig * t.DH_sig],
                [t.rho * t.DM_sig * t.DH_sig, t.DH_sig ** 2],
            ])
            cinv = np.linalg.inv(cov)
            d = np.array([dM, dH])
            tx = float(d @ cinv @ d)
            chi2 += tx
            per_tracer.append({
                "name":   t.name, "z": t.z_eff,
                "th_DM":  th_M,  "data_DM": t.DM_rd, "sigma_DM": t.DM_sig,
                "th_DH":  th_H,  "data_DH": t.DH_rd, "sigma_DH": t.DH_sig,
                "rho":    t.rho, "chi2_tracer": tx,
            })
    return {
        "H0":          c.H0,
        "Omega_m":     c.Omega_m,
        "Omega_b":     c.Omega_b,
        "omega_m":     c.omega_m,
        "omega_b":     c.omega_b,
        "r_d_Mpc":     rd,
        "chi2":        chi2,
        "dof":         N_MEAS,
        "chi2_per_dof":chi2 / N_MEAS,
        "per_tracer":  per_tracer,
    }


def main() -> int:
    cases: List[tuple[str, Cosmo]] = [
        ("ESD-PRIMARY  (H0=67.36)",        cosmo_esd_primary(67.36)),
        ("ESD-PRIMARY  (H0=73.04)",        cosmo_esd_primary(73.04)),
        ("ESD-CLOSURE-POOL (H0=67.36)",    cosmo_esd_closure_pool(67.36)),
        ("ESD-CLOSURE-POOL (H0=73.04)",    cosmo_esd_closure_pool(73.04)),
        ("Planck-LCDM (H0=67.36 baseline)",cosmo_planck_lcdm(67.36)),
        ("SH0ES-LCDM  (H0=73.04 baseline)",cosmo_planck_lcdm(73.04)),
    ]
    results = []
    for label, c in cases:
        r = chi2_single(c)
        r["label"] = label
        results.append(r)

    baseline = next(r for r in results if r["label"].startswith("Planck-LCDM"))
    chi2_base = baseline["chi2"]
    primary   = next(r for r in results if r["label"] == "ESD-PRIMARY  (H0=67.36)")
    cp_67     = next(r for r in results if r["label"] == "ESD-CLOSURE-POOL (H0=67.36)")
    dchi2_primary = primary["chi2"]   - chi2_base
    dchi2_cp      = cp_67["chi2"]     - chi2_base
    dchi2_reading = cp_67["chi2"]     - primary["chi2"]

    # --- write per-tracer CSV --------------------------------------------
    csv_path = os.path.join(OUT_DIR, "per_tracer.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "tracer", "z", "kind",
                    "theory_a", "data_a", "sigma_a",
                    "theory_b", "data_b", "sigma_b",
                    "rho", "chi2_tracer"])
        for r in results:
            for t in r["per_tracer"]:
                if "th_DV" in t:
                    w.writerow([r["label"], t["name"], t["z"], "DV",
                                t["th_DV"], t["data_DV"], t["sigma"],
                                "", "", "", "", t["chi2_tracer"]])
                else:
                    w.writerow([r["label"], t["name"], t["z"], "DM,DH",
                                t["th_DM"], t["data_DM"], t["sigma_DM"],
                                t["th_DH"], t["data_DH"], t["sigma_DH"],
                                t["rho"], t["chi2_tracer"]])
    print(f"[bao] wrote {csv_path}")

    # --- summary JSON ----------------------------------------------------
    summary = {
        "delta_chi2_gate":          DELTA_CHI2_GATE,
        "chi2_planck_lcdm":         chi2_base,
        "delta_chi2_esd_primary":   dchi2_primary,
        "delta_chi2_esd_cp":        dchi2_cp,
        "delta_chi2_reading":       dchi2_reading,
        "summary": [
            {k: r[k] for k in ("label", "H0", "Omega_m", "Omega_b",
                               "omega_m", "omega_b", "r_d_Mpc",
                               "chi2", "dof", "chi2_per_dof")}
            for r in results
        ],
    }
    json_path = os.path.join(OUT_DIR, "summary.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[bao] wrote {json_path}")

    # --- console / txt summary -------------------------------------------
    lines = []
    lines.append("=== Study 07: DESI Y1 BAO chi^2 across cosmologies ===")
    lines.append("")
    lines.append(f"  N_meas = {N_MEAS}   (BGS DV; LRG1/2/3+ELG1/ELG2/LyaQSO DM+DH; QSO DV)")
    lines.append("")
    header = (f"  {'label':<34}{'H0':>7}{'Om':>9}{'omega_b':>10}"
              f"{'r_d/Mpc':>10}{'chi^2':>9}{'chi^2/dof':>11}")
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for r in results:
        lines.append(f"  {r['label']:<34}{r['H0']:>7.2f}"
                     f"{r['Omega_m']:>9.4f}{r['omega_b']:>10.5f}"
                     f"{r['r_d_Mpc']:>10.3f}{r['chi2']:>9.2f}"
                     f"{r['chi2_per_dof']:>11.3f}")
    lines.append("")
    lines.append(f"  Delta chi^2 (ESD-PRIMARY    - Planck-LCDM, H0=67.36) = {dchi2_primary:+.3f}")
    lines.append(f"  Delta chi^2 (ESD-CLOSURE-PL - Planck-LCDM, H0=67.36) = {dchi2_cp:+.3f}")
    lines.append(f"  Reading discriminator (CP - PRIMARY at H0=67.36)     = {dchi2_reading:+.3f}")
    lines.append(f"  Gate: |Delta chi^2 (PRIMARY)| <= {DELTA_CHI2_GATE}")
    if abs(dchi2_primary) <= DELTA_CHI2_GATE:
        lines.append("  ===> GATE PASS")
        rc = 0
    else:
        lines.append("  ===> GATE FAIL")
        rc = 1
    lines.append("")
    if dchi2_reading > 0:
        lines.append("  -> DESI Y1 prefers the PRIMARY reading "
                     f"(Delta chi^2 = {dchi2_reading:+.2f}).")
    elif dchi2_reading < 0:
        lines.append("  -> DESI Y1 prefers the CLOSURE-POOL reading "
                     f"(Delta chi^2 = {dchi2_reading:+.2f}).")
    else:
        lines.append("  -> DESI Y1 is indifferent between the two readings.")
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "summary.txt"), "w") as f:
        f.write(text)
    print(f"[bao] wrote {os.path.join(OUT_DIR, 'summary.txt')}")

    # --- Markdown table (paper / README friendly) ------------------------
    md = []
    md.append("# Study 07 — DESI Y1 BAO chi^2 across cosmologies (Markdown)\n")
    md.append("| cosmology | H0 | Omega_m | omega_b | r_d (Mpc) | chi^2 | chi^2/dof |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in results:
        md.append(f"| {r['label']} | {r['H0']:.2f} | {r['Omega_m']:.4f} | "
                  f"{r['omega_b']:.5f} | {r['r_d_Mpc']:.3f} | "
                  f"{r['chi2']:.2f} | {r['chi2_per_dof']:.3f} |")
    md.append("")
    md.append("## Differential tests (at H_0 = 67.36)\n")
    md.append("| comparison | Delta chi^2 | verdict |")
    md.append("|---|---:|---|")
    verdict_primary = "PASS" if abs(dchi2_primary) <= DELTA_CHI2_GATE else "FAIL"
    md.append(f"| ESD-PRIMARY - Planck-LCDM | {dchi2_primary:+.2f} | gate \\|dchi2\\|<={DELTA_CHI2_GATE} -> **{verdict_primary}** |")
    md.append(f"| ESD-CLOSURE-POOL - Planck-LCDM | {dchi2_cp:+.2f} | reported |")
    reading_pref = ("PRIMARY" if dchi2_reading > 0
                    else ("CLOSURE-POOL" if dchi2_reading < 0 else "(tie)"))
    md.append(f"| CP - PRIMARY (reading discriminator) | {dchi2_reading:+.2f} | DESI Y1 prefers **{reading_pref}** |")
    md.append("")
    md.append("## Per-tracer chi^2 (ESD-PRIMARY, H_0 = 67.36)\n")
    md.append("| tracer | z | chi^2 |")
    md.append("|---|---:|---:|")
    primary_run = next(r for r in results if r["label"] == "ESD-PRIMARY  (H0=67.36)")
    for t in primary_run["per_tracer"]:
        md.append(f"| {t['name']} | {t['z']:.3f} | {t['chi2_tracer']:.2f} |")
    md_path = os.path.join(OUT_DIR, "tables.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"[bao] wrote {md_path}")

    print()
    print(text)
    return rc


if __name__ == "__main__":
    sys.exit(main())
