"""Phase 2b: F_12 cascade ridden on the framework-locked cosmology.

Computes P_m(k) with DISCO-EB using the LOCKED density parameters
(Ch.4 identities A + B) and then applies the F_12 cascade
modulation multiplicatively:

    P_m^Phase2b(k) = (1 + delta_cascade(k)) * P_m^locked(k)

Provenance: the LOCKED cosmology factor is LOCK class. The cascade
modulation is SCAFFOLD class (parent-action derivation incomplete)
and must be reported as "candidate signature" until promoted.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import io
import sys
import time
from pathlib import Path

import jax  # noqa: E402
jax.config.update("jax_enable_x64", True)

import numpy as np  # noqa: E402

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from esd_background import esd_locked_param_dict  # noqa: E402
from esd_primordial import apply_cascade, cascade_modulation, k_end_mpc_inverse  # noqa: E402
from run_lcdm_baseline import compute_pk  # noqa: E402


class _Tee(io.TextIOBase):
    def __init__(self, *streams):
        self._streams = streams

    def write(self, s):
        for st in self._streams:
            st.write(s)
            st.flush()
        return len(s)


def main(z: float, knob_amplitude: float, reading: str = "primary") -> int:
    out_dir = _HERE / "outputs"
    log_dir = out_dir / "logs"
    out_dir.mkdir(exist_ok=True)
    log_dir.mkdir(exist_ok=True)

    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"phase2b_cascade_locked_z{int(z)}_{stamp}.log"
    log_fh = open(log_path, "w", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, log_fh)

    print("=" * 72)
    print(f"Phase 2b: cascade x locked cosmology @ z={z}")
    print("=" * 72)
    print(f"timestamp:        {_dt.datetime.now().isoformat(timespec='seconds')}")
    print(f"knob_amplitude:   {knob_amplitude}")
    print(f"k_end (cascade):  {k_end_mpc_inverse():.3e} 1/Mpc")
    print()

    param = esd_locked_param_dict(reading=reading)
    print("LOCKED cosmology in use (Ch.4 identities A + B):")
    print(f"  Omega_m  = {param['Omegam']:.6f}")
    print(f"  Omega_b  = {param['Omegab']:.6f}")
    print(f"  H_0      = {param['H0']:.3f} km/s/Mpc (Planck boundary, not locked)")
    print(f"  n_s      = {param['n_s']:.6f}")
    print()

    aexp = 1.0 / (1.0 + z)
    t0 = time.perf_counter()
    k, p_locked, _p_locked_cb = compute_pk(param, aexp=aexp)
    print(f"DISCO-EB locked-cosmology run: {time.perf_counter()-t0:.1f} s   ({len(k)} k-modes)")

    delta = cascade_modulation(k, knob_amplitude=knob_amplitude)
    p_2b = apply_cascade(p_locked, k, knob_amplitude=knob_amplitude)

    print()
    print("=" * 72)
    print("RESIDUAL TABLE")
    print("=" * 72)
    head = f"{'k [1/Mpc]':>12s}  {'P_locked':>13s}  {'delta':>13s}  {'P_2b':>13s}"
    print(head)
    idxs = [0, len(k)//6, len(k)//3, len(k)//2, 2*len(k)//3, 5*len(k)//6, len(k)-1]
    for i in idxs:
        print(f"{k[i]:12.4e}  {p_locked[i]:13.4e}  {delta[i]:+13.4e}  {p_2b[i]:13.4e}")

    max_abs = float(np.max(np.abs(delta)))
    rms = float(np.sqrt(np.mean(delta**2)))
    ceiling = 1.0 / 51.4745  # 1 / N_e_star
    print()
    print(f"Max |delta_cascade|:  {max_abs:.4e}")
    print(f"RMS |delta_cascade|:  {rms:.4e}")
    print(f"Analytic ceiling 1/N_e_star: {ceiling:.4e}")
    print(f"Ceiling match:        {abs(max_abs - ceiling)/ceiling:.2e} (relative)")
    print()
    print("Provenance: cascade is SCAFFOLD; parent-action derivation incomplete.")
    print("Report any Phase 2b deviation as 'candidate signature'.")

    npz_path = out_dir / f"phase2b_cascade_locked_z{int(z)}.npz"
    np.savez(npz_path,
             k=k, p_locked=p_locked, p_phase2b=p_2b, delta=delta,
             knob_amplitude=knob_amplitude,
             Omegam=param["Omegam"], Omegab=param["Omegab"],
             H0=param["H0"], n_s=param["n_s"], z=z)
    print(f"\nSaved arrays -> {npz_path}")
    print(f"Saved log    -> {log_path}")

    sys.stdout = sys.__stdout__
    log_fh.close()
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--z", type=float, default=0.0)
    ap.add_argument("--knob", type=float, default=1.0)
    ap.add_argument(
        "--reading",
        choices=["primary", "closure-pool"],
        default="primary",
        help="Omega_b reading: 'primary' = Planck anchor (default), "
             "'closure-pool' = derived from c via Identity B.",
    )
    args = ap.parse_args()
    sys.exit(main(args.z, args.knob, reading=args.reading))
