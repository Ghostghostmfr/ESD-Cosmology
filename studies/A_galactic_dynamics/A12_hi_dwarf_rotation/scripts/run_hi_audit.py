"""A12 audit."""
from __future__ import annotations
import csv, json, math, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_hi_rotation as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

def main() -> int:
    print("\n=== Study A12: HI-dominated dwarf rotation ===")
    rows = []
    for s in O.SOURCES:
        Vp = E.V_flat_pred(s["M_b_Msun"])
        ratio = Vp / s["V_flat_kms"]
        dex = abs(math.log10(ratio))
        nsigma = abs(Vp - s["V_flat_kms"]) / s["V_err"]
        rows.append({"name": s["name"], "M_b": s["M_b_Msun"],
                     "V_obs": s["V_flat_kms"], "V_pred": Vp,
                     "ratio": ratio, "dex": dex, "nsigma": nsigma})

    ratios = sorted([r["ratio"] for r in rows])
    med_ratio = ratios[len(ratios) // 2]
    max_dex = max(r["dex"] for r in rows)
    max_nsig = max(r["nsigma"] for r in rows)

    # BTFR-scaling check: V_pred should scale as H0^(1/4).
    V60 = E.V_flat_pred(7.4e7, 60.0)
    V80 = E.V_flat_pred(7.4e7, 80.0)
    expected_ratio = (60.0 / 80.0) ** 0.25
    actual_ratio   = V60 / V80
    scale_err = abs(actual_ratio - expected_ratio) / expected_ratio

    claims = [
        {"claim": "1. median V_pred/V_obs in [0.8,1.2]",
         "value": med_ratio, "target": "[0.8, 1.2]",
         "verdict": "PASS" if 0.8 <= med_ratio <= 1.2 else "FAIL"},
        {"claim": "2. both sources within 0.1 dex",
         "value": max_dex, "target": 0.1,
         "verdict": "PASS" if max_dex <= 0.1 else "FAIL"},
        {"claim": "3. both sources within 3 sigma",
         "value": max_nsig, "target": 3.0,
         "verdict": "PASS" if max_nsig <= 3.0 else "FAIL"},
        {"claim": "4. BTFR scaling V_pred ~ H0^(1/4) verified",
         "value": scale_err, "target": 1e-6,
         "verdict": "PASS" if scale_err <= 1e-6 else "FAIL"},
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
        print(f"  {r['name']:14s}  M_b={r['M_b']:.2e}  V_obs={r['V_obs']:.1f}"
              f"  V_pred={r['V_pred']:.2f}  ratio={r['ratio']:.3f}  dex={r['dex']:.3f}  ({r['nsigma']:.2f}s)")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
