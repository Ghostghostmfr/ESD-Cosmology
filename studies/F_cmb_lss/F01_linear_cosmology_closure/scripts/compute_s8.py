"""Phase 2a S8 calculation: framework cosmology vs Planck vs KiDS-1000.

S8 = sigma8 * sqrt(Omega_m / 0.3) is the standard scalar that
summarises the lensing-vs-CMB "S8 tension":

  Planck-LCDM:   S8 ~ 0.832 +/- 0.013   (CMB-inferred)
  KiDS-1000:     S8 ~ 0.766 +/- 0.020   (lensing-measured, ~2-3 sigma low)

This script computes S8 from the framework-locked P(k) and compares to
Planck (computed the same way for apples-to-apples) and to the
published KiDS-1000 value. If the framework's locked cosmology sits
meaningfully below Planck S8 and toward KiDS, the +/- 6% P(k)
deviation translates into a real, headline-grade tension-easing signal
with no extra parameters.

sigma8 is computed two ways:
  (a) numerical quadrature of our DISCO P(k) array (with R=8 Mpc/h
      tophat window) -- our own independent number
  (b) CLASS internal cosmo.sigma8() -- gold-standard cross-check

S8 caveat: Planck-published S8=0.832 is on TOTAL matter (incl. massive
neutrinos). Our arrays are CB. With mnu=0.06 eV the CB-vs-total
sigma8 differs by ~0.5%. We compute both branches the same way
(CB-only) so the internal comparison is consistent; we also run the
CLASS cross-check to anchor the absolute scale.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import esd_core as ESD  # noqa: E402


# Planck reference cosmology (matches run_phase2a_locked main())
PLANCK_OMEGAM = 0.3153
PLANCK_OMEGAB = 0.0493
PLANCK_N_S    = 0.96822
PLANCK_H0     = 67.36

H0_LOCKED     = 67.36   # framework boundary value (= Planck)

# Published external numbers (with 1-sigma uncertainties)
PLANCK_S8_PUBLISHED   = 0.832
PLANCK_S8_ERR         = 0.013
KIDS1000_S8_PUBLISHED = 0.766
KIDS1000_S8_ERR       = 0.020


def tophat_W(x: np.ndarray) -> np.ndarray:
    """Fourier transform of a real-space tophat: 3 (sin x - x cos x) / x^3.
    Series expansion near x=0 to avoid catastrophic cancellation."""
    out = np.empty_like(x)
    small = np.abs(x) < 1e-3
    if small.any():
        xs = x[small]
        out[small] = 1.0 - xs**2/10.0 + xs**4/280.0
    big = ~small
    xb = x[big]
    out[big] = 3.0 * (np.sin(xb) - xb*np.cos(xb)) / xb**3
    return out


def sigma_R(k: np.ndarray, P: np.ndarray, R: float) -> float:
    """sigma(R)^2 = (1/2pi^2) integral k^2 P(k) W(kR)^2 dk
    Computed via log-k trapezoid for numerical stability."""
    lnk = np.log(k)
    integrand = k**3 * P * tophat_W(k * R)**2 / (2.0 * np.pi**2)
    # d(integral over k) = integrand * d(ln k)  since k dk = k * d(ln k)? no -- careful:
    # integral I = int f(k) dk = int f(k) * k * d(ln k) = int [f(k) * k] d(ln k)
    # here f(k) = (1/2pi^2) k^2 P(k) W(kR)^2
    # so [f(k) * k] = k^3 P(k) W^2 / (2 pi^2)  -- matches `integrand` above.
    return float(np.trapezoid(integrand, lnk))


def class_sigma8(*, H0: float, Omegab: float, Omegam: float,
                 n_s: float, A_s: float = 2.1064e-9, mnu: float = 0.06,
                 Neff_total: float = 3.046, N_nu_mass: int = 1,
                 Tcmb: float = 2.7255, YHe: float = 0.248) -> float:
    """Independent CLASS-internal sigma8 (gold-standard cross-check)."""
    from classy import Class

    h = H0 / 100.0
    Tnu = (4.0 / 11.0) ** (1.0 / 3.0)
    N_nu_rel = Neff_total - N_nu_mass

    cosmo = Class()
    cosmo.set({
        "output": "mPk",
        "P_k_max_1/Mpc": 100.0,
        "z_max_pk": 1.5,
        "h": h,
        "Omega_b": Omegab,
        "Omega_cdm": Omegam - Omegab,
        "Omega_k": 0.0,
        "N_ur": N_nu_rel,
        "N_ncdm": N_nu_mass,
        "m_ncdm": mnu,
        "T_ncdm": Tnu,
        "A_s": A_s,
        "n_s": float(n_s),
        "k_pivot": 0.05,
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
    s8 = cosmo.sigma8()
    cosmo.struct_cleanup()
    cosmo.empty()
    return float(s8)


def main() -> int:
    out_dir = _HERE / "outputs"
    log_dir = out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"phase2a_s8_z0_{stamp}.log"
    log_fh = open(log_path, "w", encoding="utf-8")

    def log(s: str = "") -> None:
        print(s)
        log_fh.write(s + "\n")
        log_fh.flush()

    log("=" * 72)
    log("Phase 2a: S8 from locked cosmology vs Planck vs KiDS-1000")
    log("=" * 72)
    log(f"timestamp: {datetime.now().isoformat(timespec='seconds')}")
    log("")

    # Load Phase 2a artifact
    artifact = out_dir / "phase2a_locked_z0.npz"
    if not artifact.exists():
        log(f"ERROR: {artifact} not found.")
        log_fh.close()
        return 1
    d = np.load(artifact)
    k = d["k"]
    p_disco_lock = d["p_disco_lock_cb"]   # CB matter (matches CLASS branches)
    p_class_lock = d["p_class_lock"]
    p_class_planck = d["p_class_planck"]

    # ---------------- (a) quadrature on our P(k) arrays --------------------
    log("(a) sigma8 by quadrature on our P(k) arrays (CB matter, R=8 Mpc/h tophat)")
    log("")

    # R in Mpc (not Mpc/h). Both branches use h=0.6736 (H_0=67.36).
    h_lock   = H0_LOCKED   / 100.0
    h_planck = PLANCK_H0   / 100.0
    R_lock   = 8.0 / h_lock      # ~ 11.876 Mpc
    R_planck = 8.0 / h_planck

    sig8_disco_lock  = np.sqrt(sigma_R(k, p_disco_lock,  R_lock))
    sig8_class_lock  = np.sqrt(sigma_R(k, p_class_lock,  R_lock))
    sig8_class_planck = np.sqrt(sigma_R(k, p_class_planck, R_planck))

    log(f"  R_8 (Mpc)            = {R_lock:.4f}  (= 8 / h, h={h_lock:.4f})")
    log(f"  sigma8 (DISCO@lock)  = {sig8_disco_lock:.5f}   [quadrature]")
    log(f"  sigma8 (CLASS@lock)  = {sig8_class_lock:.5f}   [quadrature]")
    log(f"  sigma8 (CLASS@Planck)= {sig8_class_planck:.5f}   [quadrature]")
    log(f"  DISCO-vs-CLASS at lock: {(sig8_disco_lock-sig8_class_lock)/sig8_class_lock:+.3e}")
    log("")

    # ---------------- (b) CLASS internal cosmo.sigma8 cross-check ----------
    log("(b) CLASS internal cosmo.sigma8() cross-check (gold-standard)")
    log("    (this is the CLASS-internal total-matter sigma8; quadrature above is CB)")
    log("")
    try:
        sig8_class_lock_internal   = class_sigma8(
            H0=H0_LOCKED, Omegab=ESD.OMEGA_B_INPUT,
            Omegam=ESD.OMEGA_M_LOCK, n_s=ESD.NS_STAR)
        sig8_class_planck_internal = class_sigma8(
            H0=PLANCK_H0, Omegab=PLANCK_OMEGAB,
            Omegam=PLANCK_OMEGAM, n_s=PLANCK_N_S)
        class_available = True
    except ModuleNotFoundError:
        log("  classy not installed -> using CB-quadrature sigma8 for S8 headline.")
        log("  (CLASS cross-check is optional; install `classy` to enable.)")
        sig8_class_lock_internal   = sig8_class_lock
        sig8_class_planck_internal = sig8_class_planck
        class_available = False
    log(f"  sigma8 CLASS@lock   (cosmo.sigma8 internal) = {sig8_class_lock_internal:.5f}")
    log(f"  sigma8 CLASS@Planck (cosmo.sigma8 internal) = {sig8_class_planck_internal:.5f}")
    if class_available:
        quad_vs_int_lock   = (sig8_class_lock   - sig8_class_lock_internal)   / sig8_class_lock_internal
        quad_vs_int_planck = (sig8_class_planck - sig8_class_planck_internal) / sig8_class_planck_internal
        log(f"  CB-quadrature vs total-matter internal: lock {quad_vs_int_lock:+.3e}, "
            f"planck {quad_vs_int_planck:+.3e}")
        log(f"  (small offset expected: massive-neutrino contribution to total matter)")
    log("")

    # ---------------- S8 = sigma8 * sqrt(Omega_m / 0.3) --------------------
    log("S8 = sigma8 * sqrt(Omega_m / 0.3)")
    log("")

    # Use CLASS-internal (total-matter) sigma8 for the headline numbers,
    # since that matches the convention Planck/KiDS quote S8 in.
    def s8(sigma8: float, Omegam: float) -> float:
        return sigma8 * np.sqrt(Omegam / 0.3)

    S8_lock   = s8(sig8_class_lock_internal,   ESD.OMEGA_M_LOCK)
    S8_planck = s8(sig8_class_planck_internal, PLANCK_OMEGAM)
    S8_lock_quad   = s8(sig8_disco_lock,  ESD.OMEGA_M_LOCK)   # DISCO quadrature for posterity
    S8_planck_quad = s8(sig8_class_planck, PLANCK_OMEGAM)

    log(f"  S8 (framework lock, CLASS-internal sigma8)  = {S8_lock:.5f}")
    log(f"  S8 (Planck baseline, CLASS-internal sigma8) = {S8_planck:.5f}")
    log(f"  S8 (framework lock, DISCO quadrature on CB) = {S8_lock_quad:.5f}")
    log(f"  S8 (Planck, CLASS quadrature on CB)         = {S8_planck_quad:.5f}")
    log("")
    log(f"  S8 (Planck-LCDM published) = {PLANCK_S8_PUBLISHED:.3f} +/- {PLANCK_S8_ERR:.3f}")
    log(f"  S8 (KiDS-1000 measured)    = {KIDS1000_S8_PUBLISHED:.3f} +/- {KIDS1000_S8_ERR:.3f}")
    log("")

    # ---------------- TENSION ANALYSIS -------------------------------------
    log("=" * 72)
    log("TENSION ANALYSIS")
    log("=" * 72)

    # Use CLASS-internal numbers for direct comparison with published S8.
    # Combined uncertainty assumed dominated by published error bars.
    def tension(value: float, mean: float, err: float) -> float:
        return (value - mean) / err

    t_lock_vs_planck   = tension(S8_lock,   PLANCK_S8_PUBLISHED,   PLANCK_S8_ERR)
    t_lock_vs_kids     = tension(S8_lock,   KIDS1000_S8_PUBLISHED, KIDS1000_S8_ERR)
    t_planck_vs_kids   = tension(PLANCK_S8_PUBLISHED, KIDS1000_S8_PUBLISHED, KIDS1000_S8_ERR)
    t_our_planck_vs_pub= tension(S8_planck, PLANCK_S8_PUBLISHED,   PLANCK_S8_ERR)

    log(f"  Our Planck-baseline S8 vs Planck-published:  {t_our_planck_vs_pub:+.2f} sigma "
        f"(sanity: should be near 0; offset = our A_s vs theirs etc.)")
    log(f"  Planck-published vs KiDS-1000:               {t_planck_vs_kids:+.2f} sigma "
        f"(the famous tension)")
    log("")
    log(f"  Framework-locked S8 vs Planck-published:     {t_lock_vs_planck:+.2f} sigma")
    log(f"  Framework-locked S8 vs KiDS-1000:            {t_lock_vs_kids:+.2f} sigma")
    log("")

    delta_S8 = S8_lock - S8_planck
    log(f"  delta S8 (locked - Planck-baseline, both internal) = {delta_S8:+.5f}")
    log(f"  -- positive = framework predicts MORE clustering than Planck-LCDM at the")
    log(f"     same H_0; negative = LESS, easing the S8 tension toward KiDS.")
    log("")

    if delta_S8 < -0.005:
        log("VERDICT: framework predicts LOWER S8 than Planck-LCDM. Direction is")
        log("         consistent with easing the S8 tension. Magnitude tells you")
        log("         whether the relief is partial or full.")
    elif delta_S8 > 0.005:
        log("VERDICT: framework predicts HIGHER S8 than Planck-LCDM. Direction is")
        log("         AGAINST the S8 tension -- the locked cosmology would worsen")
        log("         lensing-vs-CMB disagreement, not ease it.")
    else:
        log("VERDICT: framework S8 is essentially indistinguishable from Planck-LCDM.")
        log("         The +/-6% P(k) deviation produces near-cancellation in the")
        log("         R=8 Mpc/h weighted integral. S8 alone is not a clean")
        log("         discriminator for this cosmology.")
    log("")

    # ---------------- save --------------------------------------------------
    out_npz = out_dir / "phase2a_s8_z0.npz"
    np.savez(out_npz,
             sig8_disco_lock_quad=sig8_disco_lock,
             sig8_class_lock_quad=sig8_class_lock,
             sig8_class_planck_quad=sig8_class_planck,
             sig8_class_lock_internal=sig8_class_lock_internal,
             sig8_class_planck_internal=sig8_class_planck_internal,
             S8_lock=S8_lock, S8_planck=S8_planck,
             S8_lock_quad=S8_lock_quad, S8_planck_quad=S8_planck_quad,
             Omega_m_lock=ESD.OMEGA_M_LOCK, Omega_m_planck=PLANCK_OMEGAM,
             H0=H0_LOCKED,
             tension_lock_vs_planck_published=t_lock_vs_planck,
             tension_lock_vs_kids=t_lock_vs_kids)
    log(f"Saved arrays -> {out_npz}")
    log(f"Saved log    -> {log_path}")
    log_fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
