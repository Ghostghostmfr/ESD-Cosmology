"""C08 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_spin as E
import observations as O


def main() -> int:
    print("\n=== Study C08: BH spin / Kerr extremality ===")
    chi_test = 0.998
    M_test   = 10.0
    R_isco = E.R_at_ISCO(M_test, chi_test)
    chi_max = E.chi_max_pred()

    rows = []
    n_inside = 0
    for o in O.OBSERVATIONS:
        R_o = E.R_at_ISCO(o["M_Msun"], o["chi"])
        inside = o["chi"] <= chi_max
        rows.append({**o, "R_at_ISCO": R_o, "inside_Thorne": inside})
        if inside: n_inside += 1
    all_inside = n_inside == len(O.OBSERVATIONS)
    hb = abs(E.R_at_ISCO(M_test, chi_test, 60.0) -
             E.R_at_ISCO(M_test, chi_test, 80.0))

    samples = [
        {"obs": "test chi", "value": chi_test},
        {"obs": "test M (Msun)", "value": M_test},
        {"obs": "g_ISCO (m/s2)", "value": E.g_ISCO(M_test, chi_test)},
        {"obs": "R(u) at ISCO",  "value": R_isco},
        {"obs": "chi_max ESD",   "value": chi_max},
    ]
    claims = [
        {"claim": "1. R(u) at ISCO (chi=0.998, 10 Msun) <= 1e-15",
         "value": R_isco, "target": 1e-15,
         "verdict": "PASS" if R_isco <= 1e-15 else "FAIL"},
        {"claim": "2. predicted Thorne bound chi_max = 0.998",
         "value": chi_max, "target": 0.998,
         "verdict": "PASS" if abs(chi_max - 0.998) < 1e-9 else "FAIL"},
        {"claim": "3. all observed chi <= Thorne bound",
         "value": f"{n_inside}/{len(O.OBSERVATIONS)}",
         "target": f"{len(O.OBSERVATIONS)}/{len(O.OBSERVATIONS)}",
         "verdict": "PASS" if all_inside else "FAIL"},
        {"claim": "4. h-blind |dR| at ISCO <= 1e-6",
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
    for s in samples: print(f"  {s['obs']:25s}  {s['value']!r}")
    for r in rows:
        print(f"  {r['object']:18s} chi={r['chi']:.3f}+/-{r['chi_err']:.2f}  "
              f"R_ISCO={r['R_at_ISCO']:.2e}  inside={r['inside_Thorne']}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
