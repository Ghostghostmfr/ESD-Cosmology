"""C09 audit: black-hole tidal Love number k2."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_love as E
import observations as O


def main() -> int:
    print("\n=== Study C09: BH tidal Love number k2 ===")
    M_test = 30.0
    R_u    = E.R_at_horizon(M_test)
    k2_GR  = E.k2_BH_GR()
    k2_ESD = E.k2_BH_ESD(M_test)
    dev    = E.k2_BH_ESD_dev_bound(M_test)
    L_BH   = E.Lambda_BH(k2_ESD)

    # data gate: Lambda_BH = 0 inside every observational tidal bound
    n_inside = 0
    bound_rows = []
    for b in O.TIDAL_BOUNDS:
        inside = 0.0 <= L_BH <= b["Lambda_upper_90CL"]
        bound_rows.append({**b, "Lambda_BH_ESD": L_BH, "inside_90CL": inside})
        if inside:
            n_inside += 1
    all_inside = n_inside == len(O.TIDAL_BOUNDS)

    hb = abs(E.R_at_horizon(M_test, 60.0) - E.R_at_horizon(M_test, 80.0))

    samples = [
        {"obs": "test M (Msun)",        "value": M_test},
        {"obs": "g_horizon (m/s2)",     "value": E.g_horizon(M_test)},
        {"obs": "R(u) at horizon",      "value": R_u},
        {"obs": "k2 GR/Kerr (theorem)", "value": k2_GR},
        {"obs": "k2 ESD (BH)",          "value": k2_ESD},
        {"obs": "|k2 ESD - k2 GR| bound","value": dev},
        {"obs": "Lambda_BH ESD",        "value": L_BH},
        {"obs": "horizon compactness C","value": O.C_SCHWARZSCHILD},
    ]
    claims = [
        {"claim": "1. R(u) at BH horizon (30 Msun) <= 1e-12",
         "value": R_u, "target": 1e-12,
         "verdict": "PASS" if R_u <= 1e-12 else "FAIL"},
        {"claim": "2. ESD inherits Kerr vanishing-Love-number: |k2_ESD| <= 1e-12",
         "value": abs(k2_ESD), "target": 1e-12,
         "verdict": "PASS" if abs(k2_ESD) <= 1e-12 and dev <= 1e-12 else "FAIL"},
        {"claim": "3. Lambda_BH = 0 inside all tidal-deformability 90% CL bounds",
         "value": f"{n_inside}/{len(O.TIDAL_BOUNDS)}",
         "target": f"{len(O.TIDAL_BOUNDS)}/{len(O.TIDAL_BOUNDS)}",
         "verdict": "PASS" if all_inside else "FAIL"},
        {"claim": "4. h-blind |dR| at horizon <= 1e-6",
         "value": hb, "target": 1e-6,
         "verdict": "PASS" if hb <= 1e-6 else "FAIL"},
    ]
    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]
    OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys())); w.writeheader()
        for c in claims: w.writerow(c)
    with open(os.path.join(OUT, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(samples[0].keys())); w.writeheader()
        for s in samples: w.writerow(s)
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": samples,
                   "bounds": bound_rows, "fails": fails}, f, indent=2)
    for s in samples: print(f"  {s['obs']:30s}  {s['value']!r}")
    print()
    for r in bound_rows:
        print(f"  {r['event']:10s} Lambda<= {r['Lambda_upper_90CL']:6.0f}  "
              f"inside={r['inside_90CL']}  ({r['ref']})")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:60s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
