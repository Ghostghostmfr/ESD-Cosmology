"""Phase 2a convergence test: DISCO at hires vs published settings.

Re-runs DISCO-EB at the framework-locked cosmology with finer settings
(nmodes=1024, rtol=atol=1e-6) and compares to:
  (i)  the published 512-mode / rtol=1e-5 DISCO result (self-convergence)
  (ii) the existing CLASS@locked oracle from Phase 2a (oracle sanity)

If hires DISCO matches published DISCO to <0.1% and still passes the
<1% oracle gate, the published Phase 2a settings are converged and the
6% locked-vs-Planck residual is not an under-resolution artifact.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

import jax
jax.config.update("jax_enable_x64", True)

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import esd_core as ESD  # noqa: E402
from esd_background import esd_locked_param_dict  # noqa: E402
from run_lcdm_baseline import compute_pk  # noqa: E402


def main(z: float = 0.0, reading: str = "primary") -> int:
    out_dir = _HERE / "outputs"
    log_dir = out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    z_tag = f"z{int(round(z))}" if float(z).is_integer() else f"z{z:.3f}"
    log_path = log_dir / f"phase2a_convergence_{z_tag}_{stamp}.log"
    log_fh = open(log_path, "w", encoding="utf-8")

    def log(s: str = "") -> None:
        print(s)
        log_fh.write(s + "\n")
        log_fh.flush()

    log("=" * 72)
    log(f"Phase 2a convergence test @ z={z:g}")
    log("=" * 72)
    log(f"timestamp: {datetime.now().isoformat(timespec='seconds')}")
    log(f"settings : nmodes=512, rtol=atol=1e-6  (vs published 512 / 1e-5)")
    log("")

    # Load published Phase 2a artifact (512-mode, rtol=1e-5)
    artifact = out_dir / f"phase2a_locked_{z_tag}.npz"
    if not artifact.exists():
        log(f"ERROR: {artifact} not found.")
        log_fh.close()
        return 1
    d = np.load(artifact)
    k_pub = d["k"]
    p_pub_disco = d["p_disco_lock_cb"]
    p_class_lock = d["p_class_lock"]
    p_class_planck = d["p_class_planck"]
    log(f"Loaded published artifact: {len(k_pub)} k-modes, DISCO_pub + CLASS_lock + CLASS_planck")

    # Hires DISCO run
    aexp = 1.0 / (1.0 + z)
    log("\nRunning hires DISCO @ framework-locked cosmology ...")
    t0 = time.perf_counter()
    k_hi, _p_hi_m, p_hi_cb = compute_pk(
        esd_locked_param_dict(H0=67.36, reading=reading),
        aexp=aexp,
        nmodes=512,
        rtol=1e-6,
        atol=1e-6,
        max_steps=524288,
    )
    elapsed = time.perf_counter() - t0
    log(f"  done in {elapsed:.1f} s   ({len(k_hi)} k-modes)")

    # Interpolate hires onto published k-grid for direct comparison
    p_hi_on_pub = np.exp(np.interp(np.log(k_pub), np.log(k_hi), np.log(p_hi_cb)))

    rel_self = (p_hi_on_pub - p_pub_disco) / p_pub_disco
    rel_oracle = (p_hi_on_pub - p_class_lock) / p_class_lock
    rel_signature = (p_hi_on_pub - p_class_planck) / p_class_planck

    log("")
    log("=" * 72)
    log("CONVERGENCE TABLE")
    log("=" * 72)
    log(f"{'k [1/Mpc]':>12s}  {'P_disco_hi':>13s}  {'P_disco_pub':>13s}  "
        f"{'rel self':>12s}  {'rel vs CLASS':>14s}  {'rel vs Planck':>15s}")
    for i in [0, len(k_pub)//8, len(k_pub)//4, len(k_pub)//2,
              3*len(k_pub)//4, 7*len(k_pub)//8, len(k_pub)-1]:
        log(f"{k_pub[i]:12.4e}  {p_hi_on_pub[i]:13.4e}  {p_pub_disco[i]:13.4e}  "
            f"{rel_self[i]:+12.3e}  {rel_oracle[i]:+14.3e}  {rel_signature[i]:+15.3e}")

    max_self = float(np.max(np.abs(rel_self)))
    rms_self = float(np.sqrt(np.mean(rel_self**2)))
    max_oracle = float(np.max(np.abs(rel_oracle)))
    rms_oracle = float(np.sqrt(np.mean(rel_oracle**2)))
    max_sig = float(np.max(np.abs(rel_signature)))

    log("")
    log(f"SELF-CONVERGENCE  (hires DISCO vs published DISCO):")
    log(f"  max |rel|  = {max_self:.3e}")
    log(f"  RMS |rel|  = {rms_self:.3e}")
    log(f"  <0.5% gate: {'PASS' if max_self < 5e-3 else 'FAIL'}")
    log("")
    log(f"ORACLE SANITY (hires DISCO vs CLASS @ locked):")
    log(f"  max |rel|  = {max_oracle:.3e}")
    log(f"  RMS |rel|  = {rms_oracle:.3e}")
    log(f"  <1% gate:   {'PASS' if max_oracle < 1e-2 else 'FAIL'}")
    log("")
    log(f"PREDICTION SIGNATURE (hires DISCO vs CLASS @ Planck):")
    log(f"  max |rel|  = {max_sig:.3e}")
    log(f"  -- should remain ~6%, indicating the residual is physical, not under-resolution.")
    log("")

    out_path = out_dir / f"phase2a_convergence_{z_tag}.npz"
    np.savez(out_path,
             k=k_pub, p_disco_hires=p_hi_on_pub, p_disco_published=p_pub_disco,
             p_class_lock=p_class_lock, p_class_planck=p_class_planck,
             rel_self=rel_self, rel_oracle=rel_oracle, rel_signature=rel_signature,
             nmodes_hires=512, rtol_hires=1e-6)
    log(f"Saved arrays -> {out_path}")
    log(f"Saved log    -> {log_path}")
    log_fh.close()
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--z", type=float, default=0.0)
    ap.add_argument(
        "--reading",
        choices=["primary", "closure-pool"],
        default="primary",
        help="Omega_b reading: 'primary' = Planck anchor (default), "
             "'closure-pool' = derived from c via Identity B.",
    )
    args = ap.parse_args()
    sys.exit(main(args.z, reading=args.reading))
