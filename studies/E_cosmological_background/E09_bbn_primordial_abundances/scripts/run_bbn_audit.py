"""Study E09 audit driver - BBN under PRIMARY and CLOSURE-POOL readings."""
from __future__ import annotations

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_bbn as E       # noqa: E402
import observations as O  # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

GATE_NSIGMA      = 2.0
GATE_OMEGA_B_TOL = 0.03      # |Omega_b_CP - Omega_b_PRIMARY| / Omega_b_PRIMARY


def n_sigma(pred: float, obs: float, err: float) -> float:
    return abs(pred - obs) / err


def main() -> int:
    print("\n=== Study E09: BBN primordial abundances ===")

    rows = []
    for reading in ("primary", "closure-pool"):
        p = E.predictions(reading)
        rows.append({
            "reading":     p["reading"],
            "eta10":       p["eta10"],
            "DH_pred":     p["DH"],
            "Yp_pred":     p["Yp"],
            "DH_obs":      O.DH_OBS,
            "Yp_obs":      O.YP_OBS,
            "DH_nsigma":   n_sigma(p["DH"], O.DH_OBS, O.DH_OBS_ERR),
            "Yp_nsigma":   n_sigma(p["Yp"], O.YP_OBS, O.YP_OBS_ERR),
        })

    from esd_core import omega_b as _ob
    Ob_pri = _ob("primary")
    Ob_clo = _ob("closure-pool")
    ob_gap = abs(Ob_clo - Ob_pri) / Ob_pri

    primary = next(r for r in rows if r["reading"] == "primary")
    closure = next(r for r in rows if r["reading"] == "closure-pool")
    yp_max_n = max(primary["Yp_nsigma"], closure["Yp_nsigma"])

    claims = [
        {"claim": "1. PRIMARY D/H within 2 sigma of Cooke+ 2018",
         "value": primary["DH_nsigma"], "target": GATE_NSIGMA,
         "verdict": "PASS" if primary["DH_nsigma"] <= GATE_NSIGMA else "FAIL"},
        {"claim": "2. CLOSURE-POOL D/H within 2 sigma of Cooke+ 2018",
         "value": closure["DH_nsigma"], "target": GATE_NSIGMA,
         "verdict": "PASS" if closure["DH_nsigma"] <= GATE_NSIGMA else "FAIL"},
        {"claim": "3. Both readings Yp within 2 sigma of Aver+ 2021",
         "value": yp_max_n, "target": GATE_NSIGMA,
         "verdict": "PASS" if yp_max_n <= GATE_NSIGMA else "FAIL"},
        {"claim": "4. Identity B internal consistency: |Omega_b_CP - Omega_b_PRI| / Omega_b_PRI <= 3%",
         "value": ob_gap, "target": GATE_OMEGA_B_TOL,
         "verdict": "PASS" if ob_gap <= GATE_OMEGA_B_TOL else "FAIL"},
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

    for r in rows:
        print(f"  {r['reading']:14s}  eta_10 = {r['eta10']:.4f}"
              f"   D/H = {r['DH_pred']:.3e}"
              f" ({r['DH_nsigma']:.2f} sigma)"
              f"   Yp = {r['Yp_pred']:.4f}"
              f" ({r['Yp_nsigma']:.2f} sigma)")
    print()
    for c in claims:
        print(f"  [{c['verdict']}] {c['claim']:55s}  -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
