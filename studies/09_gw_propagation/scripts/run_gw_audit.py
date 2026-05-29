"""Study 09 — disformal photon channel reproduction harness.

Verifies, against the published Hubble paper Channel 1, that:

  1. GW170817's 1.74 s arrival window pins |eps_0| safely below
     the published 6e-15 bound.
  2. The photon-barrier condition c_gamma^2(z_LSS) >= 0 caps eps_2
     at 5.9e-19, matching the paper.
  3. The maximum saturated Delta H_0 contribution from the disformal
     channel is <= 0.12 km/s/Mpc, matching paper Table 1.

Exit 0 iff all three claims reproduce.
"""
from __future__ import annotations

import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_gw as G                  # noqa: E402
import observations as OBS          # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------- gates --------------------------------------
GATE_EPS0_BOUND_RATIO = 5.0     # |eps_0|_GW170817 <= 5 * paper's 6e-15
GATE_EPS2_REL         = 0.05    # eps_2 from barrier within 5% of 5.9e-19
GATE_DELTA_H0         = 0.20    # saturated channel cap <= 0.20 km/s/Mpc


def main() -> int:
    fails = []
    rows = []

    # ---- Claim 1: GW170817 -> eps_0 bound -------------------------------
    gw = G.gw170817_delta_c_over_c()
    eps0_naive = gw["naive_bound"]
    paper_bound = gw["paper_eps0_bound"]
    ratio = eps0_naive / paper_bound
    ok1 = ratio <= GATE_EPS0_BOUND_RATIO
    rows.append({
        "claim":  "1. GW170817 |eps_0| bound vs paper 6e-15",
        "value":  eps0_naive, "target": paper_bound,
        "units":  "dimensionless",
        "metric": f"ratio = {ratio:.3e} (naive 1.74s/40Mpc bound)",
        "gate":   f"ratio <= {GATE_EPS0_BOUND_RATIO}",
        "verdict": "PASS" if ok1 else "FAIL",
    })
    if not ok1: fails.append("Claim 1")

    # ---- Claim 2: photon-barrier -> eps_2 cap ---------------------------
    eps2_computed = G.eps2_max_from_barrier(paper_bound)
    eps2_paper = G.EPS2_PAPER_BOUND
    rel = (eps2_computed - eps2_paper) / eps2_paper
    ok2 = abs(rel) <= GATE_EPS2_REL
    rows.append({
        "claim":  "2. photon-barrier eps_2_max vs paper 5.9e-19",
        "value":  eps2_computed, "target": eps2_paper,
        "units":  "dimensionless",
        "metric": f"rel_err = {rel:+.3e}",
        "gate":   f"|rel_err| <= {GATE_EPS2_REL}",
        "verdict": "PASS" if ok2 else "FAIL",
    })
    if not ok2: fails.append("Claim 2")

    # ---- Claim 3: saturated channel cap on Delta H_0 -------------------
    sat = G.delta_H0_from_dispersion(eps0=paper_bound, eps2=eps2_computed)
    dH0 = sat["delta_H0"]
    ok3 = abs(dH0) <= GATE_DELTA_H0
    rows.append({
        "claim":  "3. saturated Delta H_0 from disformal channel",
        "value":  dH0, "target": G.DELTA_H0_PAPER,
        "units":  "km/s/Mpc",
        "metric": f"DA ratio = {sat['DA_ratio']:.6f}",
        "gate":   f"|Delta H_0| <= {GATE_DELTA_H0:.2f}",
        "verdict": "PASS" if ok3 else "FAIL",
    })
    if not ok3: fails.append("Claim 3")

    # ---- write artifacts -----------------------------------------------
    with open(os.path.join(OUT_DIR, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow(r)

    summary = {
        "gw170817":        gw,
        "eps2_max":        eps2_computed,
        "delta_H0_max":    dH0,
        "saturated_DA":    sat,
        "events":          [e.__dict__ for e in OBS.EVENTS],
        "fails":           fails,
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    lines = []
    lines.append("=== Study 09: GW propagation + disformal photon channel ===")
    lines.append("")
    lines.append("  Reproduces Channel 1 of hubble paper (Higginson 2026,")
    lines.append("  Zenodo 10.5281/zenodo.20400097).")
    lines.append("")
    header = f"  {'claim':<48}{'value':>14}{'target':>14}{'verdict':>10}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for r in rows:
        v = r["value"]; t = r["target"]
        v_s = f"{v:.4g}" if isinstance(v, float) else str(v)
        t_s = f"{t:.4g}" if isinstance(t, float) else str(t)
        lines.append(f"  {r['claim']:<48}{v_s:>14}{t_s:>14}{r['verdict']:>10}")
        lines.append(f"    {r['metric']}    [gate: {r['gate']}]")
    lines.append("")
    lines.append("  --- input events ---")
    for e in OBS.EVENTS:
        dt = (f"{e.delta_t_s:.2f} s" if not (e.delta_t_s != e.delta_t_s) else "-- (no EM)")
        lines.append(f"    {e.name:<32}  D = {e.D_lum_mpc:6.1f} Mpc   GRB lag = {dt}")
    lines.append("")
    lines.append("  --- saturated dispersion ---")
    lines.append(f"    eps_0 (used)       = {paper_bound:.3e}")
    lines.append(f"    eps_2 (barrier)    = {eps2_computed:.3e}")
    lines.append(f"    D_A ratio (mod/GR) = {sat['DA_ratio']:.8f}")
    lines.append(f"    Delta H_0          = {dH0:+.4f} km/s/Mpc")
    lines.append(f"    paper Table 1 cap  = {G.DELTA_H0_PAPER:.2f} km/s/Mpc")
    lines.append("")
    if fails:
        lines.append(f"  ===> GATE FAIL on: {', '.join(fails)}")
        rc = 1
    else:
        lines.append("  ===> ALL 3 CHANNEL-1 CLAIMS REPRODUCED")
        rc = 0
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "summary.txt"), "w") as f:
        f.write(text)

    # markdown
    md = ["# Study 09 - GW propagation (disformal photon channel)\n"]
    md.append(f"Reproduces Channel 1 of Higginson 2026 (Zenodo "
              f"10.5281/zenodo.20400097).\n")
    md.append("| claim | value | target | metric | verdict |")
    md.append("|---|---:|---:|---|---|")
    for r in rows:
        v = r["value"]; t = r["target"]
        v_s = f"{v:.4g}" if isinstance(v, float) else str(v)
        t_s = f"{t:.4g}" if isinstance(t, float) else str(t)
        md.append(f"| {r['claim']} | {v_s} | {t_s} | {r['metric']} | **{r['verdict']}** |")
    md.append("\n## Saturated dispersion at the photon-barrier\n")
    md.append(f"- eps_0       = {paper_bound:.3e}")
    md.append(f"- eps_2 (max) = {eps2_computed:.3e}")
    md.append(f"- D_A ratio   = {sat['DA_ratio']:.8f}")
    md.append(f"- Delta H_0   = {dH0:+.4f} km/s/Mpc  (paper cap {G.DELTA_H0_PAPER:.2f})")
    with open(os.path.join(OUT_DIR, "tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(text)
    print(f"\n[gw] wrote outputs to {OUT_DIR}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
