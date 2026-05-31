"""C10 audit: black-hole ringdown echoes."""
from __future__ import annotations
import csv, json, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_echoes as E
import observations as O


def main() -> int:
    print("\n=== Study C10: BH ringdown echoes ===")
    M_test = 62.0   # GW150914 remnant
    R_u    = E.R_at_horizon(M_test)
    refl   = E.wall_reflectivity_ESD(M_test)
    A_echo = E.echo_amplitude_ESD(M_test)
    dev    = E.wall_reflectivity_dev_bound(M_test)
    # echo delay a Planck-scale reflective surface WOULD produce
    eps_planck = 1.616e-35 / (E.M_sec(M_test) * O.C_M_S)  # l_pl / (GM/c^2)
    dt_echo = E.echo_delay_if_reflective(M_test, eps_planck)

    # data gate: ESD reflectivity = 0 inside every search's upper bound
    n_inside = 0
    search_rows = []
    for s in O.ECHO_SEARCHES:
        inside = 0.0 <= refl <= s["R_wall_upper"]
        search_rows.append({**s, "R_wall_ESD": refl, "inside_bound": inside})
        if inside:
            n_inside += 1
    all_inside = n_inside == len(O.ECHO_SEARCHES)
    # no confirmed (>5 sigma) echo detection in any search
    max_sigma = max(s["sigma_claim"] for s in O.ECHO_SEARCHES)
    no_confirmed = max_sigma < 5.0

    hb = abs(E.R_at_horizon(M_test, 60.0) - E.R_at_horizon(M_test, 80.0))

    samples = [
        {"obs": "test M (Msun)",          "value": M_test},
        {"obs": "g_horizon (m/s2)",       "value": E.g_horizon(M_test)},
        {"obs": "R(u) at horizon",        "value": R_u},
        {"obs": "wall reflectivity ESD",  "value": refl},
        {"obs": "echo amplitude ESD",     "value": A_echo},
        {"obs": "|R_wall - 0| bound",     "value": dev},
        {"obs": "Planck-surface echo delay (s) [would-be]", "value": dt_echo},
        {"obs": "max echo significance (data)", "value": max_sigma},
    ]
    claims = [
        {"claim": "1. R(u) at BH horizon (62 Msun) <= 1e-12",
         "value": R_u, "target": 1e-12,
         "verdict": "PASS" if R_u <= 1e-12 else "FAIL"},
        {"claim": "2. ESD classical-horizon: reflectivity = echo amp = 0 (bound <= 1e-12)",
         "value": max(abs(refl), abs(A_echo), dev), "target": 1e-12,
         "verdict": "PASS" if max(abs(refl), abs(A_echo), dev) <= 1e-12 else "FAIL"},
        {"claim": "3. ESD reflectivity 0 inside all echo-search upper bounds",
         "value": f"{n_inside}/{len(O.ECHO_SEARCHES)}",
         "target": f"{len(O.ECHO_SEARCHES)}/{len(O.ECHO_SEARCHES)}",
         "verdict": "PASS" if all_inside else "FAIL"},
        {"claim": "4. no confirmed (>=5 sigma) echo detection in data",
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
    for s in samples: print(f"  {s['obs']:38s}  {s['value']!r}")
    print()
    for r in search_rows:
        print(f"  {r['search'][:34]:34s} |R|<= {r['R_wall_upper']:.1f}  "
              f"sig={r['sigma_claim']:.1f}  inside={r['inside_bound']}")
    print()
    for c in claims: print(f"  [{c['verdict']}] {c['claim']:62s} -> {c['value']}")
    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
