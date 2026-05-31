"""B04 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_s2 as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

def main() -> int:
    print("\n=== Study B04: S2 orbit at Sgr A* ===")
    R_peri = E.R_at_g(O.G_PERI)
    R_apo  = E.R_at_g(O.G_APO)
    nsig   = E.n_sigma_fSP()
    hb = abs(E.f_SP_pred(60.0) - E.f_SP_pred(80.0))

    samples = [
        {"point": "periastron g (m/s2)",  "value": O.G_PERI},
        {"point": "apoastron g (m/s2)",   "value": O.G_APO},
        {"point": "R(u) at periastron",   "value": R_peri},
        {"point": "R(u) at apoastron",    "value": R_apo},
        {"point": "f_SP_pred",            "value": E.f_SP_pred()},
        {"point": "f_SP_obs (GRAVITY+20)","value": O.F_SP_MEAS},
    ]
    claims = [
        {"claim": "1. R(u_peri) <= 1e-6", "value": R_peri, "target": 1e-6,
         "verdict": "PASS" if R_peri <= 1e-6 else "FAIL"},
        {"claim": "2. f_SP within 1 sigma of GRAVITY+ 2020", "value": nsig,
         "target": 1.0, "verdict": "PASS" if nsig <= 1.0 else "FAIL"},
        {"claim": "3. R(u_apo) <= 1e-4", "value": R_apo, "target": 1e-4,
         "verdict": "PASS" if R_apo <= 1e-4 else "FAIL"},
        {"claim": "4. h-blind |df_SP| <= 1e-6", "value": hb,
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
    for s in samples: print(f"  {s['point']:35s}  {s['value']!r}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
