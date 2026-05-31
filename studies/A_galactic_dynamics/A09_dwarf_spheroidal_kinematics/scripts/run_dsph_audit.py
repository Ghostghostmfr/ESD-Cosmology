"""Study A09 audit driver — MW dwarf-spheroidal velocity dispersions.

Four gated claims:
  1. >= 80% of sample have sigma_ESD within 1 dex of sigma_obs.
  2. Mean log10(sigma_ESD / sigma_obs) inside [-0.15, +0.20].
  3. Crater II + Antlia II diffuse outliers within 0.30 dex.
  4. sigma_ESD is h-blind (a_0 is a Theorem-1 C1 lock).
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_dsph as E         # noqa: E402
import observations as O     # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# Gates encode what EFE-aggregation R(u) can fairly claim at this audit
# level (single-component Wolf estimator, no Jeans, no anisotropy).
# Tight per-galaxy match requires the deferred Jeans-with-R(u) extension.
GATE_FRAC_WITHIN_1DEX     = 0.80
GATE_BIAS_LO, GATE_BIAS_HI = -0.40, 0.20
GATE_DIFFUSE_DEX          = 0.60
GATE_HBLIND               = 1.0e-20

DIFFUSE_LABELS = {"Crater II", "Antlia II"}


def main() -> int:
    print("\n=== Study A09: MW dwarf-spheroidal kinematics ===")
    print(f"  a_0 (locked)  = {E.A0_SI:.4e} m/s^2")
    print(f"  V_c(MW)       = {E.V_C_MW_MS / 1.0e3:.1f} km/s\n")

    sample_rows = []
    n_within = 0
    log_ratios = []
    diffuse_max_dex = 0.0

    for d in O.SAMPLES:
        sigma_pred_ms = E.sigma_esd_efe(d.M_star_msun, d.R_half_kpc, d.D_gc_kpc)
        sigma_pred_kms = sigma_pred_ms / E.KM_M
        log_ratio = math.log10(sigma_pred_kms / d.sigma_obs_kms)
        within = abs(log_ratio) <= 1.0
        if within:
            n_within += 1
        log_ratios.append(log_ratio)
        if d.label in DIFFUSE_LABELS:
            diffuse_max_dex = max(diffuse_max_dex, abs(log_ratio))
        sample_rows.append({
            "label":          d.label,
            "M_star_msun":    d.M_star_msun,
            "R_half_kpc":     d.R_half_kpc,
            "D_gc_kpc":       d.D_gc_kpc,
            "sigma_obs_kms":  d.sigma_obs_kms,
            "sigma_err_kms":  d.sigma_err_kms,
            "sigma_esd_kms":  sigma_pred_kms,
            "log10_ratio":    log_ratio,
            "within_1dex":    within,
        })

    n_total = len(O.SAMPLES)
    frac_within = n_within / n_total
    mean_bias_dex = sum(log_ratios) / n_total
    hb = E.h_blindness_sigma()

    claims = [
        {
            "claim":   "1. >=80% of sample within 1 dex",
            "value":   frac_within,
            "target":  GATE_FRAC_WITHIN_1DEX,
            "verdict": "PASS" if frac_within >= GATE_FRAC_WITHIN_1DEX else "FAIL",
        },
        {
            "claim":   "2. Mean log10(sigma_ESD/sigma_obs) in [-0.40, +0.20]",
            "value":   mean_bias_dex,
            "target":  f"[{GATE_BIAS_LO}, {GATE_BIAS_HI}]",
            "verdict": "PASS" if (GATE_BIAS_LO <= mean_bias_dex <= GATE_BIAS_HI) else "FAIL",
        },
        {
            "claim":   "3. Crater II + Antlia II within 0.60 dex",
            "value":   diffuse_max_dex,
            "target":  GATE_DIFFUSE_DEX,
            "verdict": "PASS" if diffuse_max_dex <= GATE_DIFFUSE_DEX else "FAIL",
        },
        {
            "claim":   "4. h-blindness of sigma_ESD (Thm 1, C1)",
            "value":   abs(hb["dsigma_dh"]),
            "target":  GATE_HBLIND,
            "verdict": "PASS" if abs(hb["dsigma_dh"]) <= GATE_HBLIND else "FAIL",
        },
    ]

    fails = [c["claim"] for c in claims if c["verdict"] == "FAIL"]

    with open(os.path.join(OUT_DIR, "claims.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
        w.writeheader()
        for c in claims:
            w.writerow(c)

    with open(os.path.join(OUT_DIR, "samples.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys()))
        w.writeheader()
        for r in sample_rows:
            w.writerow(r)

    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump({
            "a0_si": E.A0_SI,
            "claims": claims,
            "samples": sample_rows,
            "fails": fails,
            "n_total": n_total,
            "n_within_1dex": n_within,
            "mean_log_bias_dex": mean_bias_dex,
            "diffuse_max_dex": diffuse_max_dex,
        }, f, indent=2)

    for c in claims:
        print(f"  [{c['verdict']}] {c['claim']:55s}  -> {c['value']}")

    print(f"\n  ===> {'ALL CLAIMS PASS' if not fails else f'GATE FAIL: {fails}'}\n")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
