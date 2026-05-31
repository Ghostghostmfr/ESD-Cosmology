"""Study B03 audit - pulsar timing strong-field consistency."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_pulsar as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

def main() -> int:
    print("\n=== Study B03: pulsar timing (J0737 + J0337) ===")
    R_orb = E.predict_orbital_R()
    R_surf = E.predict_surface_R()
    omdot_frac = E.gr_omdot_recovery_frac()
    hb = E.h_blindness()

    samples = [
        {"system": "J0737 orbital", "g_m_s2": O.G_ORBITAL_PSR, "R_u": R_orb},
        {"system": "J0737 NS surface", "g_m_s2": O.G_NS_SURFACE, "R_u": R_surf},
        {"system": "J0737 omdot_pred (deg/yr)", "g_m_s2": float("nan"),
         "R_u": O.post_keplerian_GR()["omdot_deg_yr"]},
        {"system": "J0337 SEP |Delta| 95% CL", "g_m_s2": float("nan"),
         "R_u": O.J0337["Delta_95CL"]},
    ]
    claims = [
        {"claim": "1. R(u) at orbital scale <= 1e-6", "value": R_orb,
         "target": 1.0e-6, "verdict": "PASS" if R_orb <= 1e-6 else "FAIL"},
        {"claim": "2. R(u) at NS surface <= 1e-9", "value": R_surf,
         "target": 1.0e-9, "verdict": "PASS" if R_surf <= 1e-9 else "FAIL"},
        {"claim": "3. GR omdot recovery <= 1e-3", "value": omdot_frac,
         "target": 1.0e-3, "verdict": "PASS" if omdot_frac <= 1e-3 else "FAIL"},
        {"claim": "4. h-blind verdict (|dR| << test threshold)", "value": hb,
         "target": 1.0e-6, "verdict": "PASS" if hb <= 1.0e-6 else "FAIL"},
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

    for s in samples: print(f"  {s['system']:35s}  {s['R_u']!r}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
