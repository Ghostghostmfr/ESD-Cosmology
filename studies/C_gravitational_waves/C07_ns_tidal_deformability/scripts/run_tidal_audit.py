"""C07 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_tidal as E
import observations as O


def main() -> int:
    print("\n=== Study C07: NS tidal deformability ===")
    g = O.GW170817
    M, R = g["M_NS_Msun"], g["R_NS_km"]
    R_u = E.R_at_NS(M, R)
    L_ESD = E.Lambda_ESD(M, R)
    L_GR  = E.Lambda_GR_APR(M)
    inside = g["Lambda_tilde_lo"] <= L_ESD <= g["Lambda_tilde_hi"]
    ratio_ESD_GR = L_ESD / L_GR - 1.0
    hb = abs(E.R_at_NS(M, R, 60.0) - E.R_at_NS(M, R, 80.0))

    samples = [
        {"obs": "g_NS surface (m/s2)", "value": E.g_NS_surface(M, R)},
        {"obs": "R(u) at NS",          "value": R_u},
        {"obs": "Lambda GR (APR)",     "value": L_GR},
        {"obs": "Lambda ESD",          "value": L_ESD},
        {"obs": "LVC band [lo, hi]",
         "value": f"[{g['Lambda_tilde_lo']}, {g['Lambda_tilde_hi']}]"},
    ]
    claims = [
        {"claim": "1. R(u) at NS surface <= 1e-15", "value": R_u,
         "target": 1e-15, "verdict": "PASS" if R_u <= 1e-15 else "FAIL"},
        {"claim": "2. Lambda_ESD inside LVC 90% CL [70, 720]",
         "value": L_ESD, "target": "inside",
         "verdict": "PASS" if inside else "FAIL"},
        {"claim": "3. ESD/GR ratio (1+R-1) <= 1e-15",
         "value": ratio_ESD_GR, "target": 1e-15,
         "verdict": "PASS" if abs(ratio_ESD_GR) <= 1e-15 else "FAIL"},
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
        w = csv.DictWriter(f, fieldnames=list(samples[0].keys())); w.writeheader()
        for s in samples: w.writerow(s)
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump({"claims": claims, "samples": samples, "fails": fails}, f, indent=2)
    for s in samples: print(f"  {s['obs']:30s}  {s['value']!r}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
