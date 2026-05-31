"""B05 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_stellar as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

def main() -> int:
    print("\n=== Study B05: stellar interior NULL ===")
    R_int = E.R_at_g(O.G_STELLAR_INTERIOR)
    dnu_pred = E.delta_nu_pred()
    vgr_pred = E.sirius_b_vgr_pred()

    nsig_dnu = abs(dnu_pred - O.DELTA_NU_SUN_MEAS_UHZ) / O.DELTA_NU_SUN_MESA_ERR
    nsig_vgr = abs(vgr_pred - O.SIRIUS_B_VGR_KMS) / O.SIRIUS_B_VGR_ERR
    hb = abs(E.delta_nu_pred(60.0) - E.delta_nu_pred(80.0))

    samples = [
        {"obs": "stellar interior g (m/s2)", "value": O.G_STELLAR_INTERIOR},
        {"obs": "R(u) interior",             "value": R_int},
        {"obs": "Delta_nu pred (uHz)",       "value": dnu_pred},
        {"obs": "Delta_nu meas (uHz)",       "value": O.DELTA_NU_SUN_MEAS_UHZ},
        {"obs": "Sirius B vgr pred (km/s)",  "value": vgr_pred},
        {"obs": "Sirius B vgr meas (km/s)",  "value": O.SIRIUS_B_VGR_KMS},
    ]
    claims = [
        {"claim": "1. R(u) at stellar interior <= 1e-12", "value": R_int,
         "target": 1e-12, "verdict": "PASS" if R_int <= 1e-12 else "FAIL"},
        {"claim": "2. Solar Delta_nu within 5 sigma", "value": nsig_dnu,
         "target": 5.0, "verdict": "PASS" if nsig_dnu <= 5.0 else "FAIL"},
        {"claim": "3. Sirius B v_gr within 1 sigma", "value": nsig_vgr,
         "target": 1.0, "verdict": "PASS" if nsig_vgr <= 1.0 else "FAIL"},
        {"claim": "4. h-blind |dDelta_nu| <= 1e-6", "value": hb,
         "target": 1e-6, "verdict": "PASS" if hb <= 1e-6 else "FAIL"},
    ]
    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]

    with open(os.path.join(OUT, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys())); w.writeheader()
        for c in claims: w.writerow(c)
    with open(os.path.join(OUT, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(samples[0].keys())); w.writeheader()
        for s in samples: w.writerow(s)
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": samples, "fails": fails}, f, indent=2)
    for s in samples: print(f"  {s['obs']:35s}  {s['value']!r}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
