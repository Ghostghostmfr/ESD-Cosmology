"""C06 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_friction as E
import observations as O


def main() -> int:
    print("\n=== Study C06: GW friction / running Planck mass ===")
    alpha_pred = E.alpha_M_ESD()
    g = O.GW170817
    ratio_pred = E.distance_ratio(g["z"])
    ratio_obs = g["dL_GW_Mpc"] / g["dL_EM_Mpc"]
    # 1-sigma on ratio: combine errors in quadrature
    rel_em = g["dL_EM_err"] / g["dL_EM_Mpc"]
    dL_GW_err = 0.5 * (g["dL_GW_errp"] + g["dL_GW_errm"])
    rel_gw = dL_GW_err / g["dL_GW_Mpc"]
    ratio_err = ratio_obs * (rel_em ** 2 + rel_gw ** 2) ** 0.5
    nsig_ratio = abs(ratio_pred - ratio_obs) / ratio_err

    lvk = O.LVK_O3
    bound = lvk["bound_90pct"]
    inside = abs(alpha_pred) <= bound

    hb = abs(E.alpha_M_ESD(60.0) - E.alpha_M_ESD(80.0))

    samples = [
        {"obs": "alpha_M ESD",                "value": alpha_pred},
        {"obs": "ratio dL_GW/dL_EM ESD",      "value": ratio_pred},
        {"obs": "ratio dL_GW/dL_EM obs",      "value": ratio_obs},
        {"obs": "ratio 1-sigma",              "value": ratio_err},
        {"obs": "LVK alpha_M 90% bound",      "value": bound},
    ]
    claims = [
        {"claim": "1. predicted |alpha_M| <= 1e-12 (tensor = GR)",
         "value": abs(alpha_pred), "target": 1e-12,
         "verdict": "PASS" if abs(alpha_pred) <= 1e-12 else "FAIL"},
        {"claim": "2. dL_GW/dL_EM at GW170817 within 1 sigma of 1",
         "value": nsig_ratio, "target": 1.0,
         "verdict": "PASS" if nsig_ratio <= 1.0 else "FAIL"},
        {"claim": "3. predicted alpha_M inside LVK O3 90% CL",
         "value": abs(alpha_pred), "target": bound,
         "verdict": "PASS" if inside else "FAIL"},
        {"claim": "4. h-blind |d alpha_M| <= 1e-12",
         "value": hb, "target": 1e-12,
         "verdict": "PASS" if hb <= 1e-12 else "FAIL"},
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
    for s in samples: print(f"  {s['obs']:32s}  {s['value']!r}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:55s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
