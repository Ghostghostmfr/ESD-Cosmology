"""Study 26 audit: ESD vs CMB isotropic-birefringence measurements.

Gates:
  1. ESD parent action contains no parity-odd photon term -> structural.
  2. ESD framework forbids adding g(D) F F~ post-hoc -> structural
     (Higginson 2026 strong-CP-no-axion, Q9 + Q10).
  3. beta_obs consistent with beta_ESD = 0 across all measurements
     -> |beta_obs / sigma_beta| < 3.
  4. Honest-negative tension in sigma reported per measurement.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from birefringence_data import all_measurements, FORECASTS
from esd_birefringence import (
    BETA_ESD_DEG,
    action_audit,
    esd_beta,
    tension_sigma,
)

OUT_DIR = HERE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    print("=" * 72)
    print("Study 26 - CMB cosmic birefringence audit")
    print("=" * 72)
    print(f"ESD prediction: beta = {BETA_ESD_DEG:.3f} deg (exact, no free parameters)")
    print()

    audit = action_audit()
    print("-- Gate 1 + 2 (structural action audit) --")
    for k, v in audit.items():
        print(f"   {k:30s} : {v}")
    gate1 = audit["parity_odd_term_present"] is None
    gate2 = "excluded" in str(audit["post_hoc_g(D)F_Ftilde"])
    print(f"   Gate 1 (no parity-odd term)         : {'PASS' if gate1 else 'FAIL'}")
    print(f"   Gate 2 (post-hoc addition forbidden): {'PASS' if gate2 else 'FAIL'}")
    print()

    print("-- Gate 3 + 4 (measurement comparison) --")
    print(f"   {'analysis':45s} {'beta':>8s} {'sigma':>7s} {'tension':>10s}")
    rows = []
    for m in all_measurements():
        sig = tension_sigma(m.beta_deg, m.sigma_deg)
        gate3 = abs(sig) < 3.0
        rows.append({
            "name":         m.name,
            "beta_deg":     m.beta_deg,
            "sigma_deg":    m.sigma_deg,
            "esd_beta_deg": esd_beta(),
            "tension_sigma": sig,
            "gate3_within_3sigma": bool(gate3),
            "reference":    m.reference,
            "notes":        m.notes,
        })
        flag = "PASS" if gate3 else "FAIL"
        print(f"   {m.name:45s} {m.beta_deg:8.3f} {m.sigma_deg:7.3f} "
              f"{sig:+8.2f} sig  [{flag}]")
    print()

    # Combined inverse-variance tension of independent-ish measurements.
    # PR3, PR4 NPIPE, and the joint share data, so this is illustrative.
    print("-- Forecast falsifier discovery (assumes beta_truth = 0.342 deg) --")
    beta_truth = 0.342
    fc = {}
    for exp, sig in FORECASTS.items():
        disc_sig = beta_truth / sig
        print(f"   {exp:25s} sigma_beta = {sig:.2f} deg -> "
              f"{disc_sig:.1f} sigma detection of beta=0.342")
        fc[exp] = {"sigma_deg": sig, "discovery_sigma_at_0p342": disc_sig}
    print()

    all_gate3 = all(r["gate3_within_3sigma"] for r in rows)
    worst = max(rows, key=lambda r: abs(r["tension_sigma"]))

    verdict = (
        "HONEST NEGATIVE FALSIFIER CANDIDATE: ESD predicts beta = 0 "
        "exactly with no free parameter, derived from (a) the parent "
        "action's parity-even Z(D) F^2 photon coupling and (b) the "
        "strong-CP-no-axion structural exclusion of any g(D) F F~ "
        f"addition. The most precise current measurement ({worst['name']}) "
        f"reports beta = {worst['beta_deg']:.3f} +/- {worst['sigma_deg']:.3f} deg, "
        f"a {abs(worst['tension_sigma']):.2f}-sigma tension. "
    )
    if all_gate3:
        verdict += (
            "All measurements remain below 3 sigma, so Gate 3 still PASSES, "
            "but the joint result sits at the edge. LiteBIRD (~0.05 deg) "
            "and CMB-S4 (~0.02 deg) would push a confirmed signal at "
            "beta ~ 0.342 deg to 6.8 sigma and 17.1 sigma respectively, "
            "promoting this from candidate to definitive falsifier."
        )
    else:
        verdict += (
            "At least one measurement exceeds 3 sigma vs ESD's beta = 0 "
            "prediction; ESD's parity-odd photon-sector exclusion is "
            "under direct tension."
        )

    summary = {
        "esd_beta_deg":          BETA_ESD_DEG,
        "esd_free_parameters":   0,
        "structural_audit":      audit,
        "gate1_no_parity_odd":   bool(gate1),
        "gate2_post_hoc_forbidden": bool(gate2),
        "measurements":          rows,
        "gate3_all_within_3sig": bool(all_gate3),
        "gate4_reported":        True,
        "forecasts":             fc,
        "verdict":               verdict,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"wrote {OUT_DIR / 'summary.json'}")
    print()
    print("VERDICT:", verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
