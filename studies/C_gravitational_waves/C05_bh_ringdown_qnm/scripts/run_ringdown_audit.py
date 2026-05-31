"""C05 audit."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_ringdown as E
import observations as O

OUT = os.path.join(_HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

def main() -> int:
    print("\n=== Study C05: BH ringdown QNM ===")
    g = O.GW150914
    Mf, chi, z = g["Mf_Msun"], g["chi_f"], g["redshift"]
    R_ph = E.R_photon(Mf)
    f_pred  = E.f220_ESD(Mf, chi, z=z)
    t_pred  = E.tau220_ESD(Mf, chi, z=z)
    f_obs, f_err = g["f220_Hz"], O.f220_symm_err()
    t_obs, t_err = g["tau220_ms"], O.tau220_symm_err()
    nsig_f = abs(f_pred - f_obs) / f_err
    nsig_t = abs(t_pred - t_obs) / t_err
    hb = abs(E.f220_ESD(Mf, chi, 60.0, z=z) - E.f220_ESD(Mf, chi, 80.0, z=z))

    samples = [
        {"obs": "g_photon (m/s2)", "value": E.g_photon_sphere(Mf)},
        {"obs": "R(u) photon",     "value": R_ph},
        {"obs": "f220 pred (Hz)",  "value": f_pred},
        {"obs": "f220 obs (Hz)",   "value": f_obs},
        {"obs": "tau220 pred (ms)","value": t_pred},
        {"obs": "tau220 obs (ms)", "value": t_obs},
    ]
    claims = [
        {"claim": "1. R(u) at photon sphere <= 1e-12", "value": R_ph,
         "target": 1e-12, "verdict": "PASS" if R_ph <= 1e-12 else "FAIL"},
        {"claim": "2. f220 within 1 sigma", "value": nsig_f,
         "target": 1.0, "verdict": "PASS" if nsig_f <= 1.0 else "FAIL"},
        {"claim": "3. tau220 within 1 sigma", "value": nsig_t,
         "target": 1.0, "verdict": "PASS" if nsig_t <= 1.0 else "FAIL"},
        {"claim": "4. h-blind |df220| <= 1e-6 Hz", "value": hb,
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
    for s in samples: print(f"  {s['obs']:28s}  {s['value']!r}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:50s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
