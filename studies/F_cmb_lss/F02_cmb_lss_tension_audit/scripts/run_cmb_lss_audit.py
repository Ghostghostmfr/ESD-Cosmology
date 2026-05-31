"""Study 06: CMB & LSS lock audit.

For every framework lock (Omega_m, Omega_b, Omega_DM, Omega_Lambda,
n_s, r, alpha_s, A_s, a_0, S_8, sigma_8, omega_b h^2) compare against
every survey constraint that measures the same observable and report
the signed pull

    pull = (lock - measured_central) / measured_sigma

The acceptance gate is: every reading-independent lock must be within
TIER_GATE sigma of the central CMB result (Planck 2018). Tension
surveys (KiDS-1000, DES Y3) are reported for transparency but do not
trigger a FAIL -- they ARE the S_8 tension that any cosmological
framework must contend with.

Outputs (in scripts/outputs/):
  pulls.csv               flat (survey, observable, lock, mean, sigma, pull)
  audit_summary.json      reading-by-reading aggregate
  audit_summary.txt       human-readable summary
"""

from __future__ import annotations

import csv
import json
import os
import sys
from typing import Iterable

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_locks as L  # noqa: E402
import observations as O  # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)


TIER_GATE = 2.0  # sigma; reading-independent locks must clear this vs Planck

def lock_value(name: str, reading: str = "primary") -> float | None:
    """Map observable name -> framework lock value at the requested reading."""
    omega_b   = L.OMEGA_B_PRIMARY  if reading == "primary" else L.OMEGA_B_CLOSURE_POOL
    omega_dm  = L.OMEGA_DM_PRIMARY if reading == "primary" else L.OMEGA_DM_CLOSURE_POOL
    h         = 0.6736
    table = {
        "Omega_m":       L.OMEGA_M,
        "Omega_Lambda":  L.OMEGA_LAMBDA,
        "Omega_b":       omega_b,
        "Omega_DM":      omega_dm,
        "n_s":           L.NS_STAR,
        "alpha_s":       L.ALPHA_S_STAR,
        "A_s":           L.A_S_PIVOT,
        "r":             L.R_TENSOR,
        "H_0":           67.36,                   # Planck-anchored
        "S_8":           L.S_8_LOCK,
        "sigma_8":       L.S_8_LOCK / (L.OMEGA_M / 0.3) ** 0.5,
        "omega_b_h2":    omega_b * h * h,
        "a_0":           L.a0_si(67.36),
    }
    return table.get(name)


def iter_pulls(reading: str = "primary",
               surveys: dict | None = None) -> Iterable[dict]:
    if surveys is None:
        surveys = O.SURVEYS
    for survey_name, cat in surveys.items():
        for obs_name, obs in cat.items():
            lk = lock_value(obs_name, reading=reading)
            if lk is None:
                continue
            pull = (lk - obs.central) / obs.sigma
            yield {
                "survey":   survey_name,
                "observable": obs_name,
                "lock":     lk,
                "mean":     obs.central,
                "sigma":    obs.sigma,
                "pull":     pull,
                "tag":      obs.tag,
                "reading":  reading,
            }


def fmt(v: float, width: int = 11) -> str:
    av = abs(v)
    if av == 0 or (av >= 1e-3 and av < 1e6):
        return f"{v:>{width}.5g}"
    return f"{v:>{width}.3e}"


def main() -> int:
    rows_primary = list(iter_pulls("primary"))
    rows_cp      = list(iter_pulls("closure-pool"))
    all_rows     = rows_primary + rows_cp

    # --- write CSV ---------------------------------------------------------
    csv_path = os.path.join(OUT_DIR, "pulls.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reading", "survey", "observable", "lock", "mean", "sigma", "pull", "tag"])
        for r in all_rows:
            w.writerow([r["reading"], r["survey"], r["observable"],
                        r["lock"], r["mean"], r["sigma"], r["pull"], r["tag"]])
    print(f"[audit] wrote {csv_path}")

    # --- Tier-1 (CMB-only) gate: Planck 2018 reading-independent observables
    READ_INDEP = {"Omega_m", "Omega_Lambda", "n_s", "alpha_s", "A_s", "r",
                  "S_8", "sigma_8", "Omega_DM", "a_0"}
    fails = []
    for r in rows_primary:
        if r["survey"] != "Planck 2018" or r["observable"] not in READ_INDEP:
            continue
        if abs(r["pull"]) > TIER_GATE:
            fails.append((r["observable"], r["pull"]))

    summary = {
        "tier_gate_sigma": TIER_GATE,
        "n_pulls":         len(all_rows),
        "fails_planck":    fails,
        "by_reading": {
            "primary":      {r["survey"] + "/" + r["observable"]: r["pull"] for r in rows_primary},
            "closure-pool": {r["survey"] + "/" + r["observable"]: r["pull"] for r in rows_cp},
        },
    }
    json_path = os.path.join(OUT_DIR, "audit_summary.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[audit] wrote {json_path}")

    # --- console / txt summary -------------------------------------------
    lines = []
    lines.append("=== Study 06: ESD framework cosmological lock audit ===")
    lines.append("")
    lines.append("All numbers below are signed pulls  (lock - measured) / sigma.")
    lines.append("Reading: PRIMARY  (Omega_b matched to Planck; Omega_DM from Identity B)")
    lines.append("")
    header = (f"  {'observable':<14}{'lock':>12}{'measured':>14}"
              f"{'sigma':>11}{'pull':>9}   survey")
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for r in rows_primary:
        flag = "  " if abs(r["pull"]) < 1 else ("* " if abs(r["pull"]) < 2 else "**")
        lines.append(f"  {r['observable']:<14}{fmt(r['lock'])}"
                     f"{fmt(r['mean'],14)}{fmt(r['sigma'],11)}"
                     f"  {r['pull']:>+6.2f}   {flag}{r['survey']}")
    lines.append("")
    lines.append("Reading: CLOSURE-POOL  (Omega_b derived from c alone)")
    lines.append("  (differs only in Omega_b, Omega_DM, omega_b h^2; everything else identical)")
    lines.append("")
    for r in rows_cp:
        if r["observable"] not in ("Omega_b", "Omega_DM", "omega_b_h2"):
            continue
        flag = "  " if abs(r["pull"]) < 1 else ("* " if abs(r["pull"]) < 2 else "**")
        lines.append(f"  {r['observable']:<14}{fmt(r['lock'])}"
                     f"{fmt(r['mean'],14)}{fmt(r['sigma'],11)}"
                     f"  {r['pull']:>+6.2f}   {flag}{r['survey']}")
    lines.append("")
    if fails:
        lines.append(f"GATE FAIL: {len(fails)} Planck pulls exceed {TIER_GATE} sigma:")
        for obs, p in fails:
            lines.append(f"    {obs}: pull = {p:+.2f}")
    else:
        lines.append(f"GATE PASS: every reading-independent Planck pull within {TIER_GATE} sigma.")
    lines.append("")
    lines.append("S_8 tension (reported, not gated):")
    s8_pulls = [r for r in rows_primary if r["observable"] == "S_8"]
    for r in s8_pulls:
        lines.append(f"  framework S_8 = {r['lock']:.4f} vs {r['survey']:<14}"
                     f"  {r['mean']:.3f} +/- {r['sigma']:.3f}   pull = {r['pull']:+.2f}")

    # --- BBN omega_b h^2 decomposition (post-LUNA vs pre-LUNA Cooke) -----
    lines.append("")
    lines.append("omega_b h^2 BBN decomposition (post-LUNA is the headline; pre-LUNA")
    lines.append("Cooke+2018 retained for historical-tension breakdown only):")
    o_planck = O.PLANCK["omega_b_h2"].central
    sig      = O.PLANCK["omega_b_h2"].sigma
    o_luna   = O.BBN_LUNA["omega_b_h2"].central
    o_cooke  = O.BBN_COOKE["omega_b_h2"].central
    o_prim   = lock_value("omega_b_h2", reading="primary")
    o_cp     = lock_value("omega_b_h2", reading="closure-pool")
    lines.append(f"  Planck CMB             omega_b h^2 = {o_planck:.5f} +/- {sig:.5f}")
    lines.append(f"  BBN post-LUNA           omega_b h^2 = {o_luna:.5f} +/- {sig:.5f}  (Pisanti+/Yeh+ 2021)")
    lines.append(f"  BBN Cooke+2018 (pre-LUNA)         = {o_cooke:.5f} +/- {sig:.5f}  (historical)")
    lines.append(f"  ESD PRIMARY                         = {o_prim:.5f}  (= Planck input)")
    lines.append(f"  ESD CLOSURE-POOL                    = {o_cp:.5f}")
    lines.append("")
    lines.append("  CLOSURE-POOL tension breakdown:")
    lines.append(f"    Planck - BBN-LUNA   = {(o_planck-o_luna)/sig:+5.2f} sigma   (1.0 sigma; gap mostly closed)")
    lines.append(f"    CP     - Planck     = {(o_cp-o_planck)/sig:+5.2f} sigma   (framework-specific)")
    lines.append(f"    CP     - BBN-LUNA   = {(o_cp-o_luna)/sig:+5.2f} sigma   <-- headline framework stress")
    lines.append("")
    lines.append("  For reference (do NOT cite as the framework's stress):")
    lines.append(f"    Planck - BBN-Cooke  = {(o_planck-o_cooke)/sig:+5.2f} sigma   (pre-LUNA shared CMB-BBN tension)")
    lines.append(f"    CP     - BBN-Cooke  = {(o_cp-o_cooke)/sig:+5.2f} sigma   (= sum: shared + framework piece)")
    text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "audit_summary.txt"), "w") as f:
        f.write(text)
    print(f"[audit] wrote {os.path.join(OUT_DIR, 'audit_summary.txt')}")

    # --- Markdown table (paper / README friendly) ------------------------
    md = []
    md.append("# Study 06 — ESD framework cosmological lock audit (Markdown)\n")
    md.append("Signed pulls $(lock - measured)/\\sigma$. PRIMARY reading.\n")
    md.append("| observable | lock | measured | sigma | pull | survey |")
    md.append("|---|---:|---:|---:|---:|---|")
    for r in rows_primary:
        md.append(f"| {r['observable']} | {r['lock']:.5g} | {r['mean']:.5g} | "
                  f"{r['sigma']:.3g} | {r['pull']:+.2f} | {r['survey']} |")
    md.append("\n## CLOSURE-POOL reading (Omega_b, Omega_DM, omega_b h^2 only)\n")
    md.append("| observable | lock | measured | sigma | pull | survey |")
    md.append("|---|---:|---:|---:|---:|---|")
    for r in rows_cp:
        if r["observable"] not in ("Omega_b", "Omega_DM", "omega_b_h2"):
            continue
        md.append(f"| {r['observable']} | {r['lock']:.5g} | {r['mean']:.5g} | "
                  f"{r['sigma']:.3g} | {r['pull']:+.2f} | {r['survey']} |")
    md.append("\n## BBN omega_b h^2 decomposition (post-LUNA headline)\n")
    md.append("| comparison | sigma | note |")
    md.append("|---|---:|---|")
    md.append(f"| Planck - BBN-LUNA | {(o_planck-o_luna)/sig:+.2f} | gap mostly closed |")
    md.append(f"| CP - Planck | {(o_cp-o_planck)/sig:+.2f} | framework-specific |")
    md.append(f"| **CP - BBN-LUNA** | **{(o_cp-o_luna)/sig:+.2f}** | **headline framework stress** |")
    md.append(f"| Planck - BBN-Cooke (pre-LUNA) | {(o_planck-o_cooke)/sig:+.2f} | historical, not the framework's |")
    md.append(f"| CP - BBN-Cooke (pre-LUNA) | {(o_cp-o_cooke)/sig:+.2f} | sum of the two above |")
    md_path = os.path.join(OUT_DIR, "tables.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"[audit] wrote {md_path}")

    print()
    print(text)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
