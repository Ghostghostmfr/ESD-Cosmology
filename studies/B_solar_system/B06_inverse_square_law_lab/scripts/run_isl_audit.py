"""B06 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_isl as E
import observations as O


def main() -> int:
    print("\n=== Study B06: inverse-square-law lab tests ===")
    Ru = E.R_lab()
    rows = []
    max_ratio = 0.0
    n_inside = 0
    for b in O.BOUNDS:
        a_pred = E.alpha_ESD(b["lambda_um"])
        rows.append({**b, "alpha_ESD": a_pred,
                     "inside_bound": abs(a_pred) <= b["alpha_95"]})
        max_ratio = max(max_ratio,
                        abs(a_pred) / b["alpha_95"])
        if abs(a_pred) <= b["alpha_95"]:
            n_inside += 1
    all_inside = n_inside == len(O.BOUNDS)
    hb = abs(E.R_lab(60.0) - E.R_lab(80.0))

    claims = [
        {"claim": "1. R(u) at lab scale <= 1e-15", "value": Ru,
         "target": 1e-15, "verdict": "PASS" if Ru <= 1e-15 else "FAIL"},
        {"claim": "2. predicted |alpha| inside all 5 published bounds",
         "value": f"{n_inside}/{len(O.BOUNDS)}",
         "target": f"{len(O.BOUNDS)}/{len(O.BOUNDS)}",
         "verdict": "PASS" if all_inside else "FAIL"},
        {"claim": "3. max |alpha_ESD|/|alpha_bound| <= 1e-3",
         "value": max_ratio, "target": 1e-3,
         "verdict": "PASS" if max_ratio <= 1e-3 else "FAIL"},
        {"claim": "4. h-blind |dR| <= 1e-6",
         "value": hb, "target": 1e-6,
         "verdict": "PASS" if hb <= 1e-6 else "FAIL"},
    ]
    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]
    OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys())); w.writeheader()
        for c in claims: w.writerow(c)
    with open(os.path.join(OUT, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
        for r in rows: w.writerow(r)
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": rows, "fails": fails}, f, indent=2)
    print(f"  R(u) at lab scale = {Ru:.3e}")
    for r in rows:
        print(f"  {r['experiment']:18s} lam={r['lambda_um']:6.1f} um  "
              f"alpha_bound={r['alpha_95']:.2e}  alpha_pred={r['alpha_ESD']:.2e}  "
              f"inside={r['inside_bound']}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
