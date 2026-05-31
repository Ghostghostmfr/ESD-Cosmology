"""Study A11 audit driver - Local Group timing argument."""
from __future__ import annotations

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_lg_timing as E   # noqa: E402
import observations as O    # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

GATE_NEWTON_LO = O.M_LG_NEWTON_LO_MSUN
GATE_NEWTON_HI = O.M_LG_NEWTON_HI_MSUN
GATE_ESD_LO    = O.M_BARYON_OBS_LO
GATE_ESD_HI    = O.M_BARYON_OBS_HI
GATE_R_MIN     = 10.0
GATE_HBLIND    = 1.0e-3   # Msun units


def main() -> int:
    print("\n=== Study A11: Local Group timing argument ===")
    print(f"  a_0 (locked) = {E.A0_SI:.4e} m/s^2")
    print(f"  inputs: r = {O.R_TODAY_KPC} kpc, v_r = {O.V_RADIAL_TODAY_KMS} km/s,"
          f" t = {O.T_AGE_GYR} Gyr\n")

    M_N   = E.M_LG_newton(O.R_TODAY_KPC, O.V_RADIAL_TODAY_KMS, O.T_AGE_GYR)
    M_E   = E.M_LG_esd   (O.R_TODAY_KPC, O.V_RADIAL_TODAY_KMS, O.T_AGE_GYR)
    R_orb = E.R_at_orbit(M_E, O.R_TODAY_KPC)
    hb    = E.h_blindness(O.R_TODAY_KPC, O.V_RADIAL_TODAY_KMS, O.T_AGE_GYR)

    samples = [{
        "r_today_kpc":      O.R_TODAY_KPC,
        "v_radial_kms":     O.V_RADIAL_TODAY_KMS,
        "t_age_gyr":        O.T_AGE_GYR,
        "M_LG_newton_msun": M_N,
        "M_LG_esd_msun":    M_E,
        "M_baryon_obs_msun": O.M_BARYON_OBS_MSUN,
        "R_at_orbit":       R_orb,
    }]

    claims = [
        {"claim": "1. Newton M_LG in [3, 6]e12 Msun (canonical range)",
         "value": M_N,  "target_lo": GATE_NEWTON_LO, "target_hi": GATE_NEWTON_HI,
         "verdict": "PASS" if GATE_NEWTON_LO <= M_N <= GATE_NEWTON_HI else "FAIL"},
        {"claim": "2. ESD M_b in [0.8, 3]e11 Msun (LG baryon budget)",
         "value": M_E,  "target_lo": GATE_ESD_LO,    "target_hi": GATE_ESD_HI,
         "verdict": "PASS" if GATE_ESD_LO    <= M_E <= GATE_ESD_HI    else "FAIL"},
        {"claim": "3. R(u) at orbital scale >= 10 (cluster-additive regime)",
         "value": R_orb, "target_lo": GATE_R_MIN,    "target_hi": float("inf"),
         "verdict": "PASS" if R_orb >= GATE_R_MIN else "FAIL"},
        {"claim": "4. h-blindness of M_b_ESD (Thm 1, C1)",
         "value": abs(hb["dM_dh"]), "target_lo": 0.0, "target_hi": GATE_HBLIND,
         "verdict": "PASS" if abs(hb["dM_dh"]) <= GATE_HBLIND else "FAIL"},
    ]
    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]

    with open(os.path.join(OUT_DIR, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
        w.writeheader()
        for c in claims:
            w.writerow(c)
    with open(os.path.join(OUT_DIR, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(samples[0].keys()))
        w.writeheader()
        for r in samples:
            w.writerow(r)
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": samples, "fails": fails}, f, indent=2)

    for c in claims:
        print(f"  [{c['verdict']}] {c['claim']:55s}  -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
