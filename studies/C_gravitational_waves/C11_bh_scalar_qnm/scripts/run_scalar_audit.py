"""C11 audit: black-hole scalar quasi-normal modes."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_scalar_qnm as E
import observations as O


def main() -> int:
    print("\n=== Study C11: BH scalar quasi-normal modes ===")
    M_test = 62.0   # GW150914 remnant
    R_u    = E.R_at_horizon(M_test)
    A_sc   = E.scalar_mode_amplitude_ESD(M_test)
    Q_sc   = E.scalar_charge_ESD(M_test)
    dev    = E.scalar_amplitude_dev_bound(M_test)
    f_sc, inv_tau = E.scalar_qnm_frequency_if_radiating(M_test)

    # data gate: ESD scalar amplitude = 0 inside every search's upper bound
    n_inside = 0
    search_rows = []
    for s in O.SCALAR_SEARCHES:
        inside = 0.0 <= A_sc <= s["A_scalar_upper"]
        search_rows.append({**s, "A_scalar_ESD": A_sc, "inside_bound": inside})
        if inside:
            n_inside += 1
    all_inside = n_inside == len(O.SCALAR_SEARCHES)
    # no confirmed (>5 sigma) scalar-mode / non-tensorial detection
    max_sigma = max(s["sigma_claim"] for s in O.SCALAR_SEARCHES)
    no_confirmed = max_sigma < 5.0

    hb = abs(E.R_at_horizon(M_test, 60.0) - E.R_at_horizon(M_test, 80.0))

    samples = [
        {"obs": "test M (Msun)",            "value": M_test},
        {"obs": "g_horizon (m/s2)",         "value": E.g_horizon(M_test)},
        {"obs": "R(u) at horizon",          "value": R_u},
        {"obs": "scalar/tensor amplitude ESD", "value": A_sc},
        {"obs": "remnant scalar charge ESD", "value": Q_sc},
        {"obs": "|A_scalar - 0| bound",     "value": dev},
        {"obs": "scalar ell=0 QNM freq (Hz) [would-be]", "value": f_sc},
        {"obs": "scalar ell=0 1/tau (1/s) [would-be]",   "value": inv_tau},
        {"obs": "max scalar-mode significance (data)",   "value": max_sigma},
    ]
    claims = [
        {"claim": "1. R(u) at BH horizon (62 Msun) <= 1e-12",
         "value": R_u, "target": 1e-12,
         "verdict": "PASS" if R_u <= 1e-12 else "FAIL"},
        {"claim": "2. ESD no-hair: scalar amplitude = scalar charge = 0 (bound <= 1e-12)",
         "value": max(abs(A_sc), abs(Q_sc), dev), "target": 1e-12,
         "verdict": "PASS" if max(abs(A_sc), abs(Q_sc), dev) <= 1e-12 else "FAIL"},
        {"claim": "3. ESD scalar amplitude 0 inside all polarization/mode search bounds",
         "value": f"{n_inside}/{len(O.SCALAR_SEARCHES)}",
         "target": f"{len(O.SCALAR_SEARCHES)}/{len(O.SCALAR_SEARCHES)}",
         "verdict": "PASS" if all_inside else "FAIL"},
        {"claim": "4. no confirmed (>=5 sigma) scalar mode / non-tensorial detection",
         "value": f"{max_sigma} sigma", "target": "< 5 sigma",
         "verdict": "PASS" if no_confirmed else "FAIL"},
        {"claim": "5. h-blind |dR| at horizon <= 1e-6",
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
                   "searches": search_rows, "fails": fails}, f, indent=2)
    for s in samples: print(f"  {s['obs']:42s}  {s['value']!r}")
    print()
    for r in search_rows:
        print(f"  {r['search'][:36]:36s} A<= {r['A_scalar_upper']:.1f}  "
              f"sig={r['sigma_claim']:.1f}  inside={r['inside_bound']}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:66s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
