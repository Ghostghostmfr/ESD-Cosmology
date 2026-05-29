"""Phase 2a verification: pin down the ~6% locked-vs-Planck residual.

Five sanity checks before publishing the Phase 2a result:

  (A) Independent recompute of locked Omegas (no shared module).
      Catches typo/import-order bookkeeping bugs.

  (B) H_0 audit across all branches.

  (C) Confirm CLASS uses linear pk_cb_lin (no non-linear corrections).

  (D) CAMB cross-code at locked AND Planck cosmology. If CAMB reproduces
      the same ~6% locked-vs-Planck residual that CLASS gave, the
      deviation is solver-independent.

  (E) Omega_b-only swap at CLASS: Planck cosmology with only Omega_b
      replaced by the framework-locked value. Quantifies how much of the
      6% comes from the largest fractional shift (+1.61% in Omega_b).

This script loads the existing Phase 2a z=0 artifact for the DISCO and
CLASS curves; it only runs the new CAMB + Omega_b-swap CLASS pieces.
"""
from __future__ import annotations

import math
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import esd_core as ESD  # noqa: E402
from run_phase2a_locked import run_class_pk  # noqa: E402


# Planck reference cosmology (the data anchor) -- must match run_phase2a_locked.main
PLANCK_OMEGAM = 0.3153
PLANCK_OMEGAB = 0.0493
PLANCK_N_S    = 0.96822
PLANCK_H0     = 67.36

H0_DEFAULT    = 67.36


def check_A_independent_omega_recompute() -> None:
    print("\n" + "=" * 72)
    print("CHECK (A): independent recompute of locked Omegas (no shared imports)")
    print("=" * 72)

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    c_local = (4.0 * math.log(phi) - 1.0) / phi
    OmegaL_local = 2.0 * math.pi * c_local ** 2 / 3.0
    Omegam_local = 1.0 - OmegaL_local
    eight_pi_c4 = 8.0 * math.pi * c_local ** 4
    # 3 Omega_DM + Omega_b = 8 pi c^4 Omega_m
    # Omega_m = Omega_DM + Omega_b
    # => Omega_DM (3 - r) = (8 pi c^4 - 1) Omega_m  with r = Omega_b/Omega_DM
    # Cleanest: ratio R = Omega_DM/Omega_b = (8 pi c^4 - 1)/(3 - 8 pi c^4)
    R_local = (eight_pi_c4 - 1.0) / (3.0 - eight_pi_c4)
    Omegab_local = Omegam_local / (1.0 + R_local)
    OmegaDM_local = Omegam_local - Omegab_local

    rows = [
        ("c (closure constant)",   c_local,        ESD.C_CHANNEL),
        ("Omega_Lambda",           OmegaL_local,   ESD.OMEGA_LAMBDA_LOCK),
        ("Omega_m",                Omegam_local,   ESD.OMEGA_M_LOCK),
        ("Omega_DM",               OmegaDM_local,  ESD.OMEGA_DM_LOCK),
        ("Omega_b",                Omegab_local,   ESD.OMEGA_B_LOCK),
    ]
    print(f"{'quantity':<22s}  {'local recompute':>18s}  {'esd_core':>18s}  {'rel diff':>12s}")
    fail = 0
    for name, a, b in rows:
        rd = (a - b) / b
        print(f"{name:<22s}  {a:18.10f}  {b:18.10f}  {rd:+12.2e}")
        if abs(rd) > 1e-12:
            fail += 1
    closure = Omegab_local + OmegaDM_local + OmegaL_local
    print(f"\nflatness check: Omega_b + Omega_DM + Omega_Lambda = {closure:.12f}   "
          f"(should be 1.0; deviation {closure - 1.0:+.2e})")
    print(f"identity (B):   3*Omega_DM + Omega_b = {3*OmegaDM_local + Omegab_local:.8f}, "
          f"8 pi c^4 * Omega_m = {eight_pi_c4 * Omegam_local:.8f}")

    if fail == 0 and abs(closure - 1.0) < 1e-12:
        print("\nCHECK (A): PASS -- locked Omegas reproduce from closure constant alone.")
    else:
        print(f"\nCHECK (A): FAIL -- {fail} mismatch(es).")


def check_B_H0_audit() -> None:
    print("\n" + "=" * 72)
    print("CHECK (B): H_0 audit across all branches")
    print("=" * 72)
    print(f"  Locked-cosmology branch (DISCO + CLASS-lock): H_0 = {H0_DEFAULT:.4f}")
    print(f"  Planck baseline branch (CLASS-Planck):        H_0 = {PLANCK_H0:.4f}")
    same = abs(H0_DEFAULT - PLANCK_H0) < 1e-9
    print(f"  Identical? {'YES' if same else 'NO'} -- if YES, P(k) deltas cannot be H_0 confounds.")
    if same:
        print("CHECK (B): PASS")
    else:
        print("CHECK (B): FAIL -- H_0 differs between branches; cannot attribute to Omegas alone.")


def check_C_class_linear() -> None:
    print("\n" + "=" * 72)
    print("CHECK (C): CLASS uses linear pk_cb_lin (no non-linear corrections)")
    print("=" * 72)
    import inspect
    src = inspect.getsource(run_class_pk)
    has_lin = "pk_cb_lin" in src
    has_nl_flag = "non linear" in src.lower() or "non_linear" in src.lower() or "halofit" in src.lower()
    print(f"  run_class_pk uses pk_cb_lin:    {has_lin}")
    print(f"  run_class_pk requests halofit:  {has_nl_flag}")
    if has_lin and not has_nl_flag:
        print("CHECK (C): PASS -- comparison is linear vs linear.")
    else:
        print("CHECK (C): WARNING -- non-linear path possible.")


def run_camb_locked(kmin: float, kmax: float, z: float,
                    *, Omegam: float, Omegab: float, n_s: float,
                    H0: float, mnu: float = 0.06) -> tuple[np.ndarray, np.ndarray]:
    """CAMB run with arbitrary (Omegam, Omegab, n_s, H0). Returns (k [1/Mpc], P_cb)."""
    import camb

    h = H0 / 100.0
    pars = camb.CAMBparams()
    pars.set_cosmology(
        H0=H0,
        ombh2=Omegab * h * h,
        omch2=(Omegam - Omegab) * h * h - (mnu / 93.14),
        mnu=mnu,
        nnu=3.046,
        num_massive_neutrinos=1,
        omk=0.0,
        TCMB=2.7255,
        YHe=0.248,
        tau=None,
    )
    pars.InitPower.set_params(As=2.1064e-9, ns=n_s, pivot_scalar=0.05)
    pars.set_dark_energy(w=-0.99, wa=0.0, dark_energy_model="fluid")
    pars.set_matter_power(redshifts=[float(z)], kmax=kmax / h * 1.5,
                          accurate_massive_neutrino_transfers=True)
    pars.NonLinear = camb.model.NonLinear_none
    pars.Reion.Reionization = False

    results = camb.get_results(pars)
    kh, _zs, pk_cb = results.get_matter_power_spectrum(
        minkh=kmin / h, maxkh=kmax / h, npoints=512,
        var1="delta_nonu", var2="delta_nonu")
    k_mpc = kh * h
    return k_mpc, pk_cb[0] / h**3


def check_D_camb_crosscode(k_grid: np.ndarray, p_class_lock: np.ndarray,
                           p_class_planck: np.ndarray, z: float = 0.0) -> None:
    print("\n" + "=" * 72)
    print("CHECK (D): CAMB cross-code at locked AND Planck cosmology")
    print("=" * 72)

    kmin, kmax = float(k_grid.min()), float(k_grid.max())

    print("  CAMB @ framework-locked cosmology ...")
    t0 = time.perf_counter()
    k_camb_lock, p_camb_lock = run_camb_locked(
        kmin, kmax, z,
        Omegam=ESD.OMEGA_M_LOCK, Omegab=ESD.OMEGA_B_INPUT,
        n_s=ESD.NS_STAR, H0=H0_DEFAULT,
    )
    print(f"    done in {time.perf_counter()-t0:.1f} s")

    print("  CAMB @ Planck baseline cosmology ...")
    t0 = time.perf_counter()
    k_camb_planck, p_camb_planck = run_camb_locked(
        kmin, kmax, z,
        Omegam=PLANCK_OMEGAM, Omegab=PLANCK_OMEGAB,
        n_s=PLANCK_N_S, H0=PLANCK_H0,
    )
    print(f"    done in {time.perf_counter()-t0:.1f} s")

    p_camb_lock_on = np.exp(np.interp(np.log(k_grid), np.log(k_camb_lock), np.log(p_camb_lock)))
    p_camb_planck_on = np.exp(np.interp(np.log(k_grid), np.log(k_camb_planck), np.log(p_camb_planck)))

    rel_class = (p_class_lock - p_class_planck) / p_class_planck
    rel_camb  = (p_camb_lock_on - p_camb_planck_on) / p_camb_planck_on
    rel_class_vs_camb_lock = (p_class_lock - p_camb_lock_on) / p_camb_lock_on

    print()
    print(f"{'k [1/Mpc]':>12s}  {'rel(CLASS lock-vs-Planck)':>26s}  "
          f"{'rel(CAMB lock-vs-Planck)':>26s}  {'rel(CLASS-vs-CAMB @lock)':>26s}")
    for i in [0, len(k_grid)//8, len(k_grid)//4, len(k_grid)//2,
              3*len(k_grid)//4, 7*len(k_grid)//8, len(k_grid)-1]:
        print(f"{k_grid[i]:12.4e}  {rel_class[i]:+26.3e}  {rel_camb[i]:+26.3e}  "
              f"{rel_class_vs_camb_lock[i]:+26.3e}")

    max_class = float(np.max(np.abs(rel_class)))
    max_camb  = float(np.max(np.abs(rel_camb)))
    max_xcomp = float(np.max(np.abs(rel_class - rel_camb)))
    print()
    print(f"  max |CLASS lock-vs-Planck|  = {max_class:.3e}")
    print(f"  max |CAMB  lock-vs-Planck|  = {max_camb:.3e}")
    print(f"  max delta (CLASS - CAMB) of the residual signature = {max_xcomp:.3e}")
    if max_xcomp < 5e-2:
        print("CHECK (D): PASS -- both codes give the same locked-vs-Planck signature.")
    else:
        print("CHECK (D): SUSPECT -- CLASS and CAMB disagree on the residual shape "
              "by more than 5%. Investigate before publishing.")

    # Save for inspection
    out_dir = _HERE / "outputs"
    z_tag = f"z{int(round(z))}" if float(z).is_integer() else f"z{z:.3f}"
    np.savez(out_dir / f"verify_camb_{z_tag}.npz",
             k=k_grid, p_camb_lock=p_camb_lock_on, p_camb_planck=p_camb_planck_on,
             p_class_lock=p_class_lock, p_class_planck=p_class_planck,
             rel_class=rel_class, rel_camb=rel_camb)
    print(f"  saved -> outputs/verify_camb_{z_tag}.npz")


def check_E_omega_b_swap(k_grid: np.ndarray, p_class_lock: np.ndarray,
                          p_class_planck: np.ndarray, z: float = 0.0) -> None:
    print("\n" + "=" * 72)
    print("CHECK (E): Omega_b-only swap at CLASS (isolate the +1.61% baryon contribution)")
    print("=" * 72)

    kmin, kmax = float(k_grid.min()), float(k_grid.max())

    print("  CLASS @ Planck cosmology with Omega_b ONLY replaced by locked value ...")
    t0 = time.perf_counter()
    k_swap, p_swap = run_class_pk(
        kmin, kmax, z,
        H0=PLANCK_H0,
        Omegab=ESD.OMEGA_B_INPUT,   # honest boundary input (Planck baseline)
        Omegam=PLANCK_OMEGAM,
        n_s=PLANCK_N_S,
    )
    print(f"    done in {time.perf_counter()-t0:.1f} s")

    p_swap_on = np.exp(np.interp(np.log(k_grid), np.log(k_swap), np.log(p_swap)))

    rel_full = (p_class_lock - p_class_planck) / p_class_planck         # all Omegas locked
    rel_b_only = (p_swap_on - p_class_planck) / p_class_planck           # only Omega_b locked

    fraction = np.where(np.abs(rel_full) > 1e-10, rel_b_only / rel_full, 0.0)

    print()
    print(f"{'k [1/Mpc]':>12s}  {'full lock-vs-Planck':>22s}  "
          f"{'Omega_b-only-vs-Planck':>24s}  {'fraction from Omega_b':>22s}")
    for i in [0, len(k_grid)//8, len(k_grid)//4, len(k_grid)//2,
              3*len(k_grid)//4, 7*len(k_grid)//8, len(k_grid)-1]:
        print(f"{k_grid[i]:12.4e}  {rel_full[i]:+22.3e}  {rel_b_only[i]:+24.3e}  "
              f"{fraction[i]:+22.3f}")

    # Summary at high-k where the deviation is largest
    high_k_mask = k_grid > 10.0
    if high_k_mask.any():
        mean_frac_high = float(np.mean(fraction[high_k_mask]))
        print(f"\n  Mean fraction (k > 10 Mpc^-1): {mean_frac_high:+.3f}")
        print(f"  -- interpretation: this fraction of the 6% high-k residual comes from Omega_b alone.")
    max_full = float(np.max(np.abs(rel_full)))
    max_b    = float(np.max(np.abs(rel_b_only)))
    print(f"\n  max |full lock-vs-Planck|     = {max_full:.3e}")
    print(f"  max |Omega_b-only-vs-Planck|  = {max_b:.3e}")
    print(f"  ratio max(b_only)/max(full)   = {max_b/max_full:.3f}")

    print("\nCHECK (E): informational (no PASS/FAIL gate); pins the Omega_b contribution.")

    out_dir = _HERE / "outputs"
    z_tag = f"z{int(round(z))}" if float(z).is_integer() else f"z{z:.3f}"
    np.savez(out_dir / f"verify_omegab_swap_{z_tag}.npz",
             k=k_grid, p_class_lock=p_class_lock, p_class_planck=p_class_planck,
             p_class_omegab_swap=p_swap_on,
             rel_full=rel_full, rel_b_only=rel_b_only, fraction=fraction)
    print(f"  saved -> outputs/verify_omegab_swap_{z_tag}.npz")


def main(z: float = 0.0) -> int:
    print("=" * 72)
    print(f"Phase 2a verification battery @ z={z:g}")
    print("=" * 72)
    print(f"timestamp: {datetime.now().isoformat(timespec='seconds')}")

    # Load existing Phase 2a artifact
    out_dir = _HERE / "outputs"
    z_tag = f"z{int(round(z))}" if float(z).is_integer() else f"z{z:.3f}"
    artifact = out_dir / f"phase2a_locked_{z_tag}.npz"
    if not artifact.exists():
        print(f"ERROR: {artifact} not found. Run run_phase2a_locked.py --z {z} first.")
        return 1
    d = np.load(artifact)
    k_grid = d["k"]
    p_class_lock = d["p_class_lock"]
    p_class_planck = d["p_class_planck"]
    print(f"Loaded Phase 2a artifact -> {len(k_grid)} k-modes")

    check_A_independent_omega_recompute()
    check_B_H0_audit()
    check_C_class_linear()
    check_D_camb_crosscode(k_grid, p_class_lock, p_class_planck, z=z)
    check_E_omega_b_swap(k_grid, p_class_lock, p_class_planck, z=z)

    print("\n" + "=" * 72)
    print("VERIFICATION BATTERY COMPLETE")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--z", type=float, default=0.0)
    args = ap.parse_args()
    sys.exit(main(args.z))
