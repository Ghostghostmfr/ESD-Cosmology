"""D08 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_ns as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

def main() -> int:
    print("\n=== Study D08: NICER NS mass-radius ===")
    rows = []
    R_caps, sigs, R_us = [], [], []
    for s in O.SOURCES:
        R_p = E.R_pred_km(s["M"])
        R_err = O.R_symm_err(s)
        nsig = abs(R_p - s["R_km"]) / R_err
        R_u  = E.R_at_surface(s["M"], s["R_km"])
        frac = abs(R_p - s["R_km"]) / s["R_km"]
        rows.append({"name": s["name"], "M_Msun": s["M"], "R_obs": s["R_km"],
                     "R_err": R_err, "R_pred": R_p,
                     "nsigma": nsig, "frac": frac, "R_u": R_u})
        R_us.append(R_u); sigs.append(nsig); R_caps.append(frac)

    med_frac = sorted(R_caps)[len(R_caps) // 2]
    max_nsig = max(sigs)
    max_R_u  = max(R_us)
    hb = abs(E.R_at_surface(1.4, 12.5, 60.0) - E.R_at_surface(1.4, 12.5, 80.0))

    claims = [
        {"claim": "1. max R(u) at NS surface <= 1e-15", "value": max_R_u,
         "target": 1e-15, "verdict": "PASS" if max_R_u <= 1e-15 else "FAIL"},
        {"claim": "2. median |dR|/R <= 0.15", "value": med_frac,
         "target": 0.15, "verdict": "PASS" if med_frac <= 0.15 else "FAIL"},
        {"claim": "3. max nsigma on R <= 2", "value": max_nsig,
         "target": 2.0, "verdict": "PASS" if max_nsig <= 2.0 else "FAIL"},
        {"claim": "4. h-blind |dR(u)| <= 1e-6", "value": hb,
         "target": 1e-6, "verdict": "PASS" if hb <= 1e-6 else "FAIL"},
    ]
    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]

    with open(os.path.join(OUT, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys())); w.writeheader()
        for c in claims: w.writerow(c)
    with open(os.path.join(OUT, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
        for r in rows: w.writerow(r)
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": rows, "fails": fails}, f, indent=2)
    for r in rows:
        print(f"  {r['name']:14s}  M={r['M_Msun']:.3f}  R_obs={r['R_obs']:.2f}+/-{r['R_err']:.2f}"
              f"   R_pred={r['R_pred']:.2f}  ({r['nsigma']:.2f}s, frac={r['frac']:.3f}, R_u={r['R_u']:.2e})")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:50s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
