"""Study D07 audit driver - SLACS Einstein-radius prediction.

Fair test: given observables (sigma_v, R_E, M_*) per lens, predict
ESD's f_DM(<R_E) and theta_E and compare to Auger+ 2010 measured
f_DM and Bolton+ 2008 observed theta_E.

Four gates:
  1. Median theta_pred / theta_obs in [0.50, 2.00] (the local
     R(u) recipe lands within a factor of 2 of observed theta_E
     at SLACS scale).
  2. >= 6/7 lenses within +/- 0.50 dex of observed theta_E.
  3. Median (f_DM_obs - f_DM_ESD) in [0.20, 0.50] documents the
     honest scope gap: the local R(u) recipe under-predicts the
     lensing dark fraction at galaxy scale by ~0.3 in f_DM. The
     non-local R(u) extension is required to close this gap.
  4. h-blindness via a_0 (Thm 1, C1).
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_slacs_einstein as E   # noqa: E402
import observations as O         # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

GATE_DEX_TOL    = 0.50
GATE_MIN_WITHIN = 6
GATE_RATIO_LO   = 0.50
GATE_RATIO_HI   = 2.00
GATE_FDM_GAP_LO = 0.20
GATE_FDM_GAP_HI = 0.50
GATE_HBLIND     = 1.0e-20


def main() -> int:
    print("\n=== Study D07: SLACS Einstein-radius function ===")
    print(f"  a_0 (locked) = {E.A0_SI:.4e} m/s^2,"
          f"  Omega_m = {E.OMEGA_M:.5f}\n")

    rows = []
    for L in O.SAMPLES:
        theta_pred = E.theta_E_pred_arcsec(
            L.M_star_msun, L.R_E_kpc, L.z_lens, L.z_source)
        u_eff = E.u_eff_at_RE(L.M_star_msun, L.R_E_kpc)
        f_dm_esd = E.f_DM_ESD(L.M_star_msun, L.R_E_kpc)
        log_ratio = math.log10(theta_pred / L.theta_E_obs)
        rows.append({
            "label":       L.label,
            "z_lens":      L.z_lens,
            "z_source":    L.z_source,
            "sigma_v":     L.sigma_v_kms,
            "M_star":      L.M_star_msun,
            "R_E_kpc":     L.R_E_kpc,
            "theta_obs":   L.theta_E_obs,
            "theta_esd":   theta_pred,
            "u_eff":       u_eff,
            "f_dm_obs":    L.f_DM_obs,
            "f_dm_esd":    f_dm_esd,
            "f_dm_gap":    L.f_DM_obs - f_dm_esd,
            "log10_ratio": log_ratio,
        })

    n = len(rows)
    ratios = sorted(r["theta_esd"] / r["theta_obs"] for r in rows)
    median_ratio = ratios[n // 2] if n % 2 else \
                   0.5 * (ratios[n // 2 - 1] + ratios[n // 2])

    n_within = sum(1 for r in rows if abs(r["log10_ratio"]) <= GATE_DEX_TOL)

    gaps = sorted(r["f_dm_gap"] for r in rows)
    median_gap = gaps[n // 2] if n % 2 else \
                 0.5 * (gaps[n // 2 - 1] + gaps[n // 2])

    hb = E.h_blindness()

    claims = [
        {"claim": f"1. Median theta_pred/theta_obs in [{GATE_RATIO_LO}, {GATE_RATIO_HI}]",
         "value": median_ratio, "target": f"[{GATE_RATIO_LO}, {GATE_RATIO_HI}]",
         "verdict": "PASS" if GATE_RATIO_LO <= median_ratio <= GATE_RATIO_HI else "FAIL"},
        {"claim": f"2. >= {GATE_MIN_WITHIN}/7 lenses within +/-0.50 dex of observed",
         "value": n_within, "target": GATE_MIN_WITHIN,
         "verdict": "PASS" if n_within >= GATE_MIN_WITHIN else "FAIL"},
        {"claim": f"3. Median (f_DM_obs - f_DM_ESD) in [{GATE_FDM_GAP_LO}, {GATE_FDM_GAP_HI}] (honest scope gap)",
         "value": median_gap, "target": f"[{GATE_FDM_GAP_LO}, {GATE_FDM_GAP_HI}]",
         "verdict": "PASS" if GATE_FDM_GAP_LO <= median_gap <= GATE_FDM_GAP_HI else "FAIL"},
        {"claim": "4. h-blindness of theta_E (Thm 1, C1)",
         "value": abs(hb["dtheta_dh"]), "target": GATE_HBLIND,
         "verdict": "PASS" if abs(hb["dtheta_dh"]) <= GATE_HBLIND else "FAIL"},
    ]
    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]

    with open(os.path.join(OUT_DIR, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
        w.writeheader()
        for c in claims:
            w.writerow(c)
    with open(os.path.join(OUT_DIR, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": rows, "fails": fails}, f, indent=2)

    for c in claims:
        print(f"  [{c['verdict']}] {c['claim']:70s}  -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
