"""Phase-1 gate: DISCO-EB LCDM recovery.

Run DISCO-EB with the framework-anchored param dict and ESD cascade knob
set to ZERO. The output must reproduce the vanilla Planck 2018 LCDM matter
power spectrum to within solver tolerance (rtol=1e-3 in DISCO-EB). This is
the LCDM-limit gate that must pass before any ESD-modified run publishes.

Outputs P(k) and a sanity print. The CLASS oracle comparison lives in
class_oracle/compare_disco_vs_class.py and reads this script's output.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
import numpy as np

# JAX must be importable; only required at runtime
import jax
jax.config.update("jax_enable_x64", True)  # required: rtol=1e-5 needs float64
import jax.numpy as jnp

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from esd_background import esd_param_dict, planck2018_param_dict  # noqa: E402

# DISCO-EB API
from discoeb.background import evolve_background
from discoeb.perturbations import evolve_perturbations_batched, get_power


def compute_pk(param: dict, kmin: float = 1e-5, kmax: float = 1e+2,
               nmodes: int = 512, aexp: float = 1.0,
               rtol: float = 1e-5, atol: float = 1e-5,
               max_steps: int = 262144) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run DISCO-EB and return (k, P_m(k), P_cb(k)) in Mpc units.

    Defaults match DISCO-EB's published CLASS comparison notebook
    (nb_discoeb_class_comparison.ipynb): 8 decades in k (1e-5..1e+2 1/Mpc),
    rtol=atol=1e-5. That notebook validates DISCO-EB <0.5% vs CLASS at z=99
    with these settings. We extend max_steps for z=0 runs which integrate
    over a longer conformal time window.
    """
    param = evolve_background(param=param, thermo_module="RECFAST")
    aexp_out = jnp.array([aexp])
    y, kmodes = evolve_perturbations_batched(
        param=param, kmin=kmin, kmax=kmax, num_k=nmodes,
        aexp_out=aexp_out, rtol=rtol, atol=atol,
        lmaxg=31, lmaxgp=31, lmaxr=31, lmaxnu=31, nqmax=5,
        max_steps=max_steps, batch_size=32,
    )
    param['lmaxg'] = 31; param['lmaxgp'] = 31; param['lmaxr'] = 31
    param['lmaxnu'] = 31; param['nqmax'] = 5
    Pkm = get_power(k=kmodes, y=y[:, 0, :], idx=4, param=param)
    Pkcb = get_power(k=kmodes, y=y[:, 0, :], idx=6, param=param)
    return np.asarray(kmodes), np.asarray(Pkm), np.asarray(Pkcb)


def main(z: float = 0.0) -> int:
    aexp = 1.0 / (1.0 + z)
    print("=" * 70)
    print(f"DISCO-EB LCDM Phase-1 recovery gate (z = {z:g}, aexp = {aexp:.6e})")
    print("=" * 70)
    print(f"JAX backend: {jax.default_backend()}")
    print(f"JAX devices: {jax.devices()}")
    print()

    # Two runs: framework-anchored (with n_s = 0.9611 LOCK) and Planck-default.
    # At zero cascade knob, the only delta between them is the n_s value,
    # which should produce a smooth tilt difference in P(k).
    print("[1/2] Framework-anchored (n_s = 0.9611, ESD cascade OFF)")
    t0 = time.perf_counter()
    k_esd, p_esd, p_esd_cb = compute_pk(esd_param_dict(), aexp=aexp)
    print(f"      completed in {time.perf_counter()-t0:.1f} s, {len(k_esd)} k-modes")

    print("[2/2] Planck-default oracle (n_s = 0.96822)")
    t0 = time.perf_counter()
    k_lcdm, p_lcdm, p_lcdm_cb = compute_pk(planck2018_param_dict(), aexp=aexp)
    print(f"      completed in {time.perf_counter()-t0:.1f} s")

    # Sanity: relative difference at a few k-modes (P_m total)
    print()
    print(f"{'k [1/Mpc]':>12s}  {'P_esd_m':>12s}  {'P_lcdm_m':>12s}  {'P_lcdm_cb':>12s}  {'rel diff':>10s}")
    for i in [0, len(k_esd)//4, len(k_esd)//2, 3*len(k_esd)//4, len(k_esd)-1]:
        rd = (p_esd[i] - p_lcdm[i]) / p_lcdm[i]
        print(f"{k_esd[i]:12.4e}  {p_esd[i]:12.4e}  {p_lcdm[i]:12.4e}  {p_lcdm_cb[i]:12.4e}  {rd:+10.3e}")

    # Save for oracle comparison (redshift-tagged)
    out_dir = _HERE / "outputs"
    out_dir.mkdir(exist_ok=True)
    z_tag = f"z{int(round(z))}" if float(z).is_integer() else f"z{z:.3f}"
    fname = out_dir / f"lcdm_baseline_{z_tag}.npz"
    np.savez(fname,
             k=k_esd, p_esd=p_esd, p_esd_cb=p_esd_cb,
             k_lcdm=k_lcdm, p_lcdm=p_lcdm, p_lcdm_cb=p_lcdm_cb,
             z=z, aexp=aexp)
    print(f"\nSaved {fname}")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--z", type=float, default=0.0,
                    help="Output redshift (0 = today, 99 = matches DISCO-EB paper validation point)")
    args = ap.parse_args()
    sys.exit(main(z=args.z))
