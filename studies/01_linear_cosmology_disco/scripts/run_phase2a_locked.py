"""Phase 2a: framework zero-parameter cosmology vs Planck.

Runs DISCO-EB with the framework-locked param dict (Omega_Lambda, Omega_m,
Omega_DM, Omega_b all derived from the closure constant c) and compares
the resulting P_cb(k) against:

  (i)  CLASS run with the SAME framework-locked Omegas   (oracle sanity)
  (ii) CLASS run with vanilla Planck 2018 Omegas         (prediction vs data)

The (i) gate must pass <1% across 8 decades in k -- this validates that
DISCO-EB handles the framework cosmology correctly. The (ii) residual is
the actual physical distance between the framework's zero-parameter
prediction and the Planck-best-fit cosmology; we expect a few-percent
shape difference (ESD Framework (Higginson 2026) Ch.4 reports 0.06-1.6% deviations in the
scalar Omegas, which translate to ~1-5% shape modulations in P(k)).

H(z) is NOT modified -- the framework's H(z) is identical to LCDM
(Paper 1 Sec.4.3, "LCDM recovery" paragraph). The framework's voice at
background level lives entirely in the LOCKED Omega values.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path
import numpy as np

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: F401

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import esd_core as ESD  # noqa: E402
from esd_background import esd_locked_param_dict  # noqa: E402
from run_lcdm_baseline import compute_pk  # noqa: E402


def run_class_pk(
    kmin: float,
    kmax: float,
    z: float,
    *,
    H0: float,
    Omegab: float,
    Omegam: float,
    n_s: float,
    A_s: float = 2.1064e-9,
    mnu: float = 0.06,
    Neff_total: float = 3.046,
    N_nu_mass: int = 1,
    Tcmb: float = 2.7255,
    YHe: float = 0.248,
    k_pivot: float = 0.05,
) -> tuple[np.ndarray, np.ndarray]:
    """Run CLASS for an arbitrary cosmology. Returns (k, P_cb_lin) in CLASS units."""
    from classy import Class

    h = H0 / 100.0
    Tnu = (4.0 / 11.0) ** (1.0 / 3.0)
    N_nu_rel = Neff_total - N_nu_mass

    cosmo = Class()
    cosmo.set({
        "output": "mPk",
        "P_k_max_1/Mpc": kmax * 1.01,
        "z_max_pk": max(0.5, z + 1.0),
        "h": h,
        "Omega_b": Omegab,
        "Omega_cdm": Omegam - Omegab,   # DISCO-EB notebook convention
        "Omega_k": 0.0,
        "N_ur": N_nu_rel,
        "N_ncdm": N_nu_mass,
        "m_ncdm": mnu,
        "T_ncdm": Tnu,
        "A_s": A_s,
        "n_s": float(n_s),
        "k_pivot": k_pivot,
        "T_cmb": Tcmb,
        "YHe": YHe,
        "gauge": "synchronous",
        "reio_parametrization": "reio_none",
        "k_per_decade_for_pk": 100,
        "k_per_decade_for_bao": 100,
        "recombination": "RECFAST",
        "l_max_g": 31,
        "l_max_pol_g": 31,
        "l_max_ur": 31,
        "l_max_ncdm": 31,
        "Omega_Lambda": 0.0,
        "w0_fld": -0.99,
        "wa_fld": 0.0,
        "cs2_fld": 1.0,
        "use_ppf": "no",
        "radiation_streaming_approximation": 2,
        "ncdm_fluid_approximation": 3,
        "ur_fluid_approximation": 2,
    })
    cosmo.compute()
    k = np.geomspace(kmin, kmax, 512)
    pk_cb = np.array([cosmo.pk_cb_lin(ki, float(z)) for ki in k])
    cosmo.struct_cleanup()
    cosmo.empty()
    return k, pk_cb


def _residuals(p_a: np.ndarray, p_b: np.ndarray) -> tuple[float, float, float]:
    """Return (max_abs_rel, rms_abs_rel, argmax_idx) of (p_a - p_b) / p_b."""
    rel = (p_a - p_b) / p_b
    a = np.abs(rel)
    return float(a.max()), float(np.sqrt(np.mean(a ** 2))), int(a.argmax())


def main(z: float = 0.0, reading: str = "primary") -> int:
    H0 = 67.36   # Planck baseline; framework does NOT lock H_0
    log_lines: list[str] = []

    def log(s: str = "") -> None:
        print(s)
        log_lines.append(s)

    Omegab_use = ESD.omega_b(reading)
    Omegadm_use = ESD.omega_dm(reading)
    is_primary = ESD.Reading.parse(reading) is ESD.Reading.PRIMARY
    omegab_tag = "(BOUNDARY INPUT; Planck)" if is_primary else "(CLOSURE-POOL; derived from c)"

    log("=" * 72)
    log(f"Phase 2a: framework zero-parameter cosmology @ z={z:g}  [reading={reading}]")
    log("=" * 72)
    log(f"timestamp:    {datetime.now().isoformat(timespec='seconds')}")
    log(f"closure c     = {ESD.C_CHANNEL:.8f}   (= (4 ln phi - 1)/phi)")
    log("")
    log("LOCKED density parameters (Ch.4 identities A + B):")
    log(f"  Omega_Lambda = 2 pi c^2 / 3              = {ESD.OMEGA_LAMBDA_LOCK:.6f}")
    log(f"  Omega_m      = 1 - Omega_Lambda          = {ESD.OMEGA_M_LOCK:.6f}")
    log(f"  Omega_DM     (Identity B given Omega_b)  = {Omegadm_use:.6f}")
    log(f"  Omega_b      {omegab_tag:30s} = {Omegab_use:.6f}")
    if is_primary:
        log("  (Ch.4 L91: Omega_b is boundary data set by baryogenesis,")
        log("   not predicted from c-closure. Identity B is a RELATION.)")
    else:
        log("  (Closure-pool route: Identity B closed against matter closure;")
        log("   zero-parameter prediction, +1.6% above Planck baseline.)")
    log("LOCKED primordial:")
    log(f"  n_s          = 1 - 2/N_e_star            = {ESD.NS_STAR:.6f}")
    log(f"  A_s          (Planck COBE anchor, not locked) = {ESD.A_S_PIVOT:.3e}")
    log("Boundary (NOT framework-locked, Planck baseline):")
    log(f"  H_0          = {H0:.3f} km/s/Mpc")
    log("")

    # Planck reference cosmology (the data anchor)
    Planck_Omegam = 0.3153
    Planck_Omegab = 0.0493
    Planck_n_s    = 0.96822
    Planck_H0     = 67.36

    aexp = 1.0 / (1.0 + z)

    # --- (1) DISCO-EB with framework-locked cosmology -------------------------
    log("[1/3] DISCO-EB with framework-locked cosmology")
    t0 = time.perf_counter()
    k_dl, p_dl_m, p_dl_cb = compute_pk(
        esd_locked_param_dict(H0=H0, reading=reading), aexp=aexp
    )
    log(f"      done in {time.perf_counter()-t0:.1f} s   ({len(k_dl)} k-modes)")

    # --- (2) CLASS oracle for the SAME framework-locked cosmology -------------
    log("[2/3] CLASS oracle for framework-locked cosmology (sanity)")
    t0 = time.perf_counter()
    Omegab_used = ESD.omega_b(reading)
    k_co_lock, p_co_lock = run_class_pk(
        k_dl.min(), k_dl.max(), z,
        H0=H0,
        Omegab=Omegab_used,
        Omegam=ESD.OMEGA_M_LOCK,
        n_s=ESD.NS_STAR,
    )
    log(f"      done in {time.perf_counter()-t0:.1f} s")

    # --- (3) CLASS oracle for Planck baseline cosmology (data anchor) ---------
    log("[3/3] CLASS oracle for Planck 2018 baseline cosmology (data anchor)")
    t0 = time.perf_counter()
    k_co_planck, p_co_planck = run_class_pk(
        k_dl.min(), k_dl.max(), z,
        H0=Planck_H0,
        Omegab=Planck_Omegab,
        Omegam=Planck_Omegam,
        n_s=Planck_n_s,
    )
    log(f"      done in {time.perf_counter()-t0:.1f} s")

    # Interpolate CLASS onto DISCO k-grid (log-log)
    p_co_lock_on = np.exp(np.interp(np.log(k_dl), np.log(k_co_lock), np.log(p_co_lock)))
    p_co_planck_on = np.exp(np.interp(np.log(k_dl), np.log(k_co_planck), np.log(p_co_planck)))

    log("")
    log("=" * 72)
    log("RESIDUAL TABLE")
    log("=" * 72)
    log(f"{'k [1/Mpc]':>12s}  {'P_DISCO_lock':>14s}  {'P_CLASS_lock':>14s}  "
        f"{'P_CLASS_Planck':>16s}  {'rel(DvC_lock)':>14s}  {'rel(lock_vs_Planck)':>20s}")
    for i in [0, len(k_dl)//8, len(k_dl)//4, len(k_dl)//2,
              3*len(k_dl)//4, 7*len(k_dl)//8, len(k_dl)-1]:
        rel_oracle = (p_dl_cb[i] - p_co_lock_on[i]) / p_co_lock_on[i]
        rel_predvsdata = (p_co_lock_on[i] - p_co_planck_on[i]) / p_co_planck_on[i]
        log(f"{k_dl[i]:12.4e}  {p_dl_cb[i]:14.4e}  {p_co_lock_on[i]:14.4e}  "
            f"{p_co_planck_on[i]:16.4e}  {rel_oracle:+14.3e}  {rel_predvsdata:+20.3e}")

    # Gates
    max_oracle, rms_oracle, i_oracle = _residuals(p_dl_cb, p_co_lock_on)
    max_predvsdata, rms_predvsdata, i_pd = _residuals(p_co_lock_on, p_co_planck_on)

    log("")
    log(f"Oracle sanity (DISCO_lock vs CLASS_lock):")
    log(f"  max |rel|  = {max_oracle:.4e}  at k = {k_dl[i_oracle]:.4e}")
    log(f"  RMS |rel|  = {rms_oracle:.4e}")
    log(f"  <1% gate:  {'PASS' if max_oracle < 1e-2 else 'FAIL'}")
    log("")
    log(f"Prediction vs Planck data (CLASS_lock vs CLASS_Planck):")
    log(f"  max |rel|  = {max_predvsdata:.4e}  at k = {k_dl[i_pd]:.4e}")
    log(f"  RMS |rel|  = {rms_predvsdata:.4e}")
    log(f"  (Ch.4 reports Omega deviations of 0.06%-1.6% from Planck;")
    log(f"   the P(k) shape difference is the integrated effect of those.)")

    # Save outputs
    out_dir = _HERE / "outputs" / reading
    out_dir.mkdir(parents=True, exist_ok=True)
    z_tag = f"z{int(round(z))}" if float(z).is_integer() else f"z{z:.3f}"
    fname = out_dir / f"phase2a_locked_{z_tag}.npz"
    np.savez(
        fname,
        k=k_dl,
        p_disco_lock_m=p_dl_m,
        p_disco_lock_cb=p_dl_cb,
        p_class_lock=p_co_lock_on,
        p_class_planck=p_co_planck_on,
        Omega_Lambda_lock=ESD.OMEGA_LAMBDA_LOCK,
        Omega_m_lock=ESD.OMEGA_M_LOCK,
        Omega_DM_used=Omegadm_use,
        Omega_b_used=Omegab_use,
        reading=reading,
        # historical (over-lock; kept in npz for diff-vs-prior-runs):
        Omega_DM_overlock=ESD.OMEGA_DM_LOCK,
        Omega_b_overlock=ESD.OMEGA_B_LOCK,
        n_s_lock=ESD.NS_STAR,
        H0=H0,
        z=z,
    )
    log("")
    log(f"Saved arrays -> {fname}")

    log_dir = out_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"phase2a_locked_{z_tag}_{ts}.log"
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    log(f"Saved log    -> {log_path}")
    return 0


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--z", type=float, default=0.0)
    p.add_argument(
        "--reading",
        choices=["primary", "closure-pool"],
        default="primary",
        help="Omega_b reading: 'primary' = Planck anchor (default), "
             "'closure-pool' = derived from c via Identity B.",
    )
    a = p.parse_args()
    sys.exit(main(z=a.z, reading=a.reading))
