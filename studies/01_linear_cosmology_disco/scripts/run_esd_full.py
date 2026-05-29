"""Full ESD-modified DISCO-EB run.

Computes the LCDM-limit P_m(k) from DISCO-EB with framework-anchored
params, then applies the F_12 cascade modulation as a multiplicative
factor: P_m^ESD(k) = (1 + delta_cascade(k)) * P_m^LCDM(k).

Only run AFTER run_lcdm_baseline.py + compare_disco_vs_class.py
have demonstrated <0.1 percent recovery vs the CLASS oracle.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from esd_background import esd_param_dict  # noqa: E402
from esd_primordial import apply_cascade, cascade_modulation, k_end_mpc_inverse  # noqa: E402
from run_lcdm_baseline import compute_pk  # noqa: E402


def main(knob_amplitude: float = 1.0) -> int:
    print("=" * 70)
    print(f"DISCO-EB ESD full run (cascade knob = {knob_amplitude})")
    print("=" * 70)
    print(f"k_end = {k_end_mpc_inverse():.3e} 1/Mpc")
    print()

    t0 = time.perf_counter()
    k, p_lcdm, _p_lcdm_cb = compute_pk(esd_param_dict())
    print(f"DISCO-EB LCDM-limit run: {time.perf_counter()-t0:.1f} s")

    delta = cascade_modulation(k, knob_amplitude=knob_amplitude)
    p_esd = apply_cascade(p_lcdm, k, knob_amplitude=knob_amplitude)

    print(f"\n{'k [1/Mpc]':>12s}  {'P_lcdm':>12s}  {'delta':>12s}  {'P_esd':>12s}")
    for i in [0, len(k)//4, len(k)//2, 3*len(k)//4, len(k)-1]:
        print(f"{k[i]:12.4e}  {p_lcdm[i]:12.4e}  {delta[i]:+12.4e}  {p_esd[i]:12.4e}")

    print(f"\nMax |delta_cascade| across k-range: {np.max(np.abs(delta)):.4e}")
    print(f"Expected ceiling 1/N_e_star = {1/51.4745:.4e}")

    out_dir = _HERE / "outputs"
    out_dir.mkdir(exist_ok=True)
    np.savez(out_dir / "esd_full.npz",
             k=k, p_lcdm=p_lcdm, p_esd=p_esd, delta=delta,
             knob_amplitude=knob_amplitude)
    print(f"\nSaved {out_dir / 'esd_full.npz'}")
    return 0


if __name__ == "__main__":
    knob = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    sys.exit(main(knob))
