"""Study A10 audit driver - UDG broader-sample kinematics.

Sample: pressure-supported UDGs with identified hosts -- DF2, DF4,
NGC 5846-UDG1, Dragonfly 44.

Excluded (with reason in observations.py):
  - AGC 114905: HI rotating disk; Wolf single-component estimator
    structurally inapplicable.
  - DGSAT I: isolated UDG with no host; the EFE-aggregation test
    (the novelty of this study) has nothing to act on.

This study extends A07 (DF2/DF4 only) to the broader UDG demographic
using the same A07 EFE-aggregation predictor. Gates follow the A07
pattern: gate the *EFE reduction factor*, not the absolute match
(which remains a shared MOND-family tension).

Four gated claims:
  1. EFE reduction factor >= 1.3 across {DF2, DF4, NGC 5846-UDG1}
     (extends the A07 reduction claim to the DM-poor demographic).
  2. NGC 5846-UDG1 EFE prediction within 3 sigma of observed.
  3. Dragonfly 44 honest tension reported >= 3 sigma (the DM-rich
     falsifier candidate; EFE here pulls the wrong direction --
     this is the new finding).
  4. h-blindness of sigma_ESD via a_0 (Thm 1, C1).
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_udg_broader as E   # noqa: E402
import observations as O      # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

GATE_EFE_REDUCTION = 1.3
GATE_NGC5846_SIG   = 3.0
GATE_DF44_MIN_SIG  = 3.0
GATE_HBLIND        = 1.0e-20

POOL_REDUCTION = {"NGC 1052-DF2", "NGC 1052-DF4", "NGC 5846-UDG1"}


def main() -> int:
    print("\n=== Study A10: UDG broader kinematics ===")
    print(f"  a_0 (locked) = {E.A0_SI:.4e} m/s^2\n")

    rows = []
    by_label = {}
    for u in O.SAMPLES:
        s_efe = E.sigma_esd_efe(
            u.M_star_msun, u.R_half_kpc, u.M_host_msun, u.r_host_kpc
        ) / E.KM_M
        s_no  = E.sigma_esd_no_efe(u.M_star_msun, u.R_half_kpc) / E.KM_M
        resid_efe = (s_efe - u.sigma_obs_kms) / u.sigma_err_kms
        resid_no  = (s_no  - u.sigma_obs_kms) / u.sigma_err_kms
        # EFE reduction factor: |residual no-EFE| / |residual EFE|; >1 means
        # EFE pulled prediction closer to obs.
        eps = 1.0e-12
        reduction = abs(resid_no) / max(abs(resid_efe), eps)
        row = {
            "label":         u.label,
            "dm_class":      u.dm_class,
            "sigma_obs":     u.sigma_obs_kms,
            "sigma_err":     u.sigma_err_kms,
            "sigma_esd_no_efe": s_no,
            "sigma_esd_efe": s_efe,
            "resid_no_efe":  resid_no,
            "resid_efe":     resid_efe,
            "efe_reduction": reduction,
        }
        rows.append(row)
        by_label[u.label] = row

    pool_min_reduction = min(by_label[k]["efe_reduction"] for k in POOL_REDUCTION)
    ngc_sig  = abs(by_label["NGC 5846-UDG1"]["resid_efe"])
    df44_sig = abs(by_label["Dragonfly 44"]["resid_efe"])
    hb = E.h_blindness_sigma()

    claims = [
        {"claim": "1. EFE reduction factor >= 1.3 across DF2/DF4/NGC5846",
         "value": pool_min_reduction, "target": GATE_EFE_REDUCTION,
         "verdict": "PASS" if pool_min_reduction >= GATE_EFE_REDUCTION else "FAIL"},
        {"claim": "2. NGC 5846-UDG1 EFE within 3 sigma",
         "value": ngc_sig, "target": GATE_NGC5846_SIG,
         "verdict": "PASS" if ngc_sig <= GATE_NGC5846_SIG else "FAIL"},
        {"claim": "3. DF44 honest tension (>= 3 sigma)",
         "value": df44_sig, "target": GATE_DF44_MIN_SIG,
         "verdict": "PASS" if df44_sig >= GATE_DF44_MIN_SIG else "FAIL"},
        {"claim": "4. h-blindness of sigma_ESD (Thm 1, C1)",
         "value": abs(hb["dsigma_dh"]), "target": GATE_HBLIND,
         "verdict": "PASS" if abs(hb["dsigma_dh"]) <= GATE_HBLIND else "FAIL"},
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
        print(f"  [{c['verdict']}] {c['claim']:55s}  -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
