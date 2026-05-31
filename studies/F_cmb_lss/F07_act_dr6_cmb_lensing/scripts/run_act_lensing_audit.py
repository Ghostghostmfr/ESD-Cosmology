"""
Study 24 audit: ACT DR6 CMB lensing versus ESD's locked S_8^{CMBL}.

The ESD prediction is fixed by:
  - Identity B (Paper 1 C2):  Omega_m = 0.31574  (locked)
  - Study 19:                 sigma_8 unchanged from Planck on linear scales

giving  S_8^{CMBL,ESD} = sigma_8 * (Omega_m / 0.3)^0.25  with no free
parameters. The audit compares this against the headline ACT DR6 lensing
posterior on the same combination.

A 3-sigma compatibility threshold is used (same as Study 23). The audit
also reports the tension against the tighter ACT DR6 + Planck NPIPE
combined posterior, but the headline ACT-only value is used for the
pass/fail gate.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.esd_lensing import (  # noqa: E402
    OMEGA_M_LOCK,
    SIGMA8_PLANCK,
    s8_cmbl_esd,
    s8_cmbl_esd_sigma,
)
from scripts.observations import ACT_DR6_ONLY, ACT_DR6_PLUS_NPIPE  # noqa: E402

TENSION_PASS_THRESHOLD_SIGMA = 3.0


def _tension(obs_median: float, obs_sigma: float,
             theory: float, theory_sigma: float) -> float:
    """Tension in units of the joint 1-sigma (independent Gaussians)."""
    return abs(obs_median - theory) / math.hypot(obs_sigma, theory_sigma)


def main() -> int:
    theory = s8_cmbl_esd()
    theory_sigma = s8_cmbl_esd_sigma()

    print("=" * 64)
    print(" ESD Study 24 audit: ACT DR6 CMB lensing")
    print("=" * 64)
    print(f"  Locked inputs:")
    print(f"    sigma_8 (Planck 2018)  = {SIGMA8_PLANCK:.4f}")
    print(f"    Omega_m (Identity B)   = {OMEGA_M_LOCK:.5f}")
    print(f"  ESD prediction:")
    print(f"    S_8^CMBL = sigma_8 * (Omega_m/0.3)^0.25 = "
          f"{theory:.4f} +/- {theory_sigma:.4f}")
    print()

    passed = True
    for obs in (ACT_DR6_ONLY, ACT_DR6_PLUS_NPIPE):
        tension = _tension(obs.median, obs.sigma, theory, theory_sigma)
        gate = obs is ACT_DR6_ONLY  # only the headline ACT-only gate counts
        verdict = "PASS" if tension < TENSION_PASS_THRESHOLD_SIGMA else "FAIL"
        marker = "  (PASS/FAIL gate)" if gate else "  (informational only)"
        print(f"--- {obs.label} ---")
        print(f"    observed S_8^CMBL = {obs.median:.3f} +/- {obs.sigma:.3f}")
        print(f"    tension vs ESD    = {tension:.2f} sigma   -> {verdict}{marker}")
        print(f"    source            : {obs.source}")
        print()
        if gate and verdict == "FAIL":
            passed = False

    print("--- Summary ---")
    print(f"  pass threshold : < {TENSION_PASS_THRESHOLD_SIGMA:.1f} sigma")
    if passed:
        print("[OVERALL PASS] ACT DR6 lensing is consistent with ESD's locked")
        print("               S_8^CMBL (Planck sigma_8 + Identity B Omega_m).")
    else:
        print("[OVERALL FAIL] ACT DR6 lensing is in tension with ESD's locked")
        print("               S_8^CMBL.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
