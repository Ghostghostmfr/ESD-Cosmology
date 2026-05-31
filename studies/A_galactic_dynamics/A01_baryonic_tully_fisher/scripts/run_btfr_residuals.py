"""Full BTFR residual analysis (Study 02 paper-grade runner).

Reproduces the headline numbers of

  Higginson, J. P. (2026).  A Zero-Parameter Prediction for the
  Baryonic Tully-Fisher Relation from the Golden-Ratio Gravitational
  Closure.  DOI 10.5281/zenodo.20400008.

Procedure (matches Sec.~3-4 of the paper):

  1. Load SPARC master table (data/SPARC_Lelli2016c.mrt) and
     rotation curves (data/Rotmod_LTG/<Galaxy>_rotmod.dat).
     Run `python fetch_sparc_rotmod.py` once to populate the cache.
  2. Filter Q <= 2.
  3. Compute baryonic mass:
        M_b = 0.5 * L_3.6 + 1.33 * M_HI.
  4. For each galaxy compute g_N at the flat-rotation radius from
     the SPARC mass-model components:
        V_bar^2 = 0.5 * V_disk^2 + 0.7 * V_bul^2 + |V_gas| * V_gas,
     evaluated as the median over the outer 20% of radial bins
     (minimum 2 points); g_N = V_bar^2 / r_out.
     Fallback: point-mass g_N = G M_b / (2.2 * R_disk)^2 if no
     rotmod file is available.
  5. Form u = 4 g_N / a_0 and G(u) = u(1 + R(u))^2 / 4.
  6. ESD prediction:  V_f^4_pred = G(u) * G * M_b * a_0.
     MOND prediction: V_f^4_pred = G * M_b * a_0  (G(u) -> 1).
  7. Residuals delta = log10(V_f^4_obs) - log10(V_f^4_pred).
  8. Report mean, RMS, effective slope for both predictions.

Outputs:
  outputs/btfr_residuals.npz   - all per-galaxy arrays + summary scalars.
  outputs/btfr_residuals.json  - paper-ready headline numbers.
  outputs/btfr_residuals.txt   - human-readable summary table.

Exit code:
  0 if the published headline numbers reproduce within tolerance,
  1 otherwise,
  3 on data/fit error.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from esd_btfr import (  # noqa: E402
    G_btfr, G_SI, MSUN_KG, UPSILON_BULGE, UPSILON_DISK,
    a_zero_SI, baryonic_mass_solar,
)

DATA_DIR = os.path.abspath(os.path.join(_HERE, "..", "data"))
MRT_PATH = os.path.join(DATA_DIR, "SPARC_Lelli2016c.mrt")
ROTMOD_DIR = os.path.join(DATA_DIR, "Rotmod_LTG")
OUT_DIR = os.path.join(_HERE, "outputs")
NPZ_PATH = os.path.join(OUT_DIR, "btfr_residuals.npz")
TXT_PATH = os.path.join(OUT_DIR, "btfr_residuals.txt")
JSON_PATH = os.path.join(OUT_DIR, "btfr_residuals.json")

# (km/s)^2 / kpc -> m/s^2
KMS2_PER_KPC_TO_MS2: float = 1.0e6 / 3.086e19
# kpc * (km/s)^2 / Msun
G_KPC_KMS2_MSUN: float = 4.3009e-6

# Published headline numbers (Tab. btfr-stats of the paper).  We treat
# these as the regression target; tolerance is loose enough to allow
# for differences in a_0 (1.198e-10 published vs 1.2015e-10 from
# esd_core / current Planck inputs).
PUBLISHED = {
    "N": 129,
    "esd_rms_dex": 0.268,
    "mond_rms_dex": 0.283,
    "esd_mean_dex": -0.017,
    "mond_mean_dex": 0.103,
    "alpha_eff_esd": 3.84,
}
TOL = {"rms": 0.01, "mean": 0.02, "alpha": 0.05, "N": 5}


# ----------------------------------------------------------------------- parsing

def parse_sparc_master(path: str) -> list[dict]:
    """Parse SPARC Lelli+2016 master MRT table."""
    galaxies: list[dict] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    data_start = 0
    for i, ln in enumerate(lines):
        if ln.startswith("-----"):
            data_start = i + 1
    for ln in lines[data_start:]:
        parts = ln.split()
        if len(parts) < 18:
            continue
        try:
            galaxies.append({
                "name": parts[0],
                "T": int(parts[1]),
                "D": float(parts[2]),
                "L36": float(parts[7]),
                "Rdisk": float(parts[11]),
                "MHI": float(parts[13]),
                "Vflat": float(parts[15]),
                "e_Vflat": float(parts[16]),
                "Q": int(parts[17]),
            })
        except (ValueError, IndexError):
            continue
    return galaxies


def read_rotation_curve(galaxy_name: str) -> dict | None:
    """Read SPARC `<name>_rotmod.dat`.

    Columns (per SPARC README):
      Rad[kpc]  Vobs  errV  Vgas  Vdisk  Vbul  SBdisk  SBbul
    """
    path = os.path.join(ROTMOD_DIR, f"{galaxy_name}_rotmod.dat")
    if not os.path.exists(path):
        return None
    rad, vgas, vdisk, vbul = [], [], [], []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip():
                continue
            parts = ln.split()
            if len(parts) < 6:
                continue
            try:
                rad.append(float(parts[0]))
                vgas.append(float(parts[3]))
                vdisk.append(float(parts[4]))
                vbul.append(float(parts[5]))
            except ValueError:
                continue
    if not rad:
        return None
    return {
        "Rad": np.array(rad), "Vgas": np.array(vgas),
        "Vdisk": np.array(vdisk), "Vbul": np.array(vbul),
    }


def outer_gN_from_rotmod(rc: dict) -> float | None:
    """Compute g_N at the outer rotation-curve radius from the SPARC
    mass-model decomposition.  Returns m/s^2 or None on failure."""
    n = len(rc["Rad"])
    n_outer = max(2, n // 5)
    sl = slice(n - n_outer, n)
    rad = rc["Rad"][sl]
    vgas = rc["Vgas"][sl]
    vdisk = rc["Vdisk"][sl]
    vbul = rc["Vbul"][sl]
    Vbar2 = (UPSILON_DISK * vdisk**2
             + UPSILON_BULGE * vbul**2
             + np.abs(vgas) * vgas)
    if np.median(Vbar2) <= 0:
        return None
    r_out = float(np.median(rad))
    if r_out <= 0:
        return None
    g_N_kpc = float(np.median(Vbar2)) / r_out
    return g_N_kpc * KMS2_PER_KPC_TO_MS2


def pointmass_gN(M_b_msun: float, Rdisk_kpc: float) -> float | None:
    """Fallback g_N = G * M_b / (2.2 * R_disk)^2 (kpc -> m/s^2)."""
    if Rdisk_kpc <= 0:
        return None
    r_char = 2.2 * Rdisk_kpc
    g_N_kpc = G_KPC_KMS2_MSUN * M_b_msun / r_char**2
    return g_N_kpc * KMS2_PER_KPC_TO_MS2


# ----------------------------------------------------------------------- main

def main() -> int:  # noqa: C901  (single straight-line procedure)
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(MRT_PATH):
        print(f"[btfr] master table missing: {MRT_PATH}\n"
              f"       run `python fetch_sparc_rotmod.py` first.",
              file=sys.stderr)
        return 3
    if not os.path.isdir(ROTMOD_DIR):
        print(f"[btfr] Rotmod_LTG dir missing: {ROTMOD_DIR}\n"
              f"       run `python fetch_sparc_rotmod.py` first.",
              file=sys.stderr)
        return 3

    galaxies = parse_sparc_master(MRT_PATH)
    print(f"[btfr] parsed {len(galaxies)} galaxies from SPARC master table")

    good = [g for g in galaxies
            if g["Q"] <= 2 and g["Vflat"] > 0 and g["e_Vflat"] > 0]
    print(f"[btfr] after Q<=2 quality cut: {len(good)} galaxies")

    a0 = a_zero_SI()
    print(f"[btfr] locked a_0 = {a0:.4e} m/s^2 (esd_core.a_zero)")

    names: list[str] = []
    log_Mb, log_Vf = [], []
    log_Vf4_obs, log_Vf4_esd, log_Vf4_mond = [], [], []
    G_vals, u_vals = [], []
    methods = {"rotcurve": 0, "pointmass": 0, "skipped": 0}

    for gal in good:
        Mb = baryonic_mass_solar(gal["L36"], gal["MHI"])
        Vf = gal["Vflat"]
        if Mb <= 0 or Vf <= 0:
            methods["skipped"] += 1
            continue

        g_N: float | None = None
        rc = read_rotation_curve(gal["name"])
        if rc is not None:
            g_N = outer_gN_from_rotmod(rc)
            if g_N is not None and g_N > 0:
                methods["rotcurve"] += 1
            else:
                g_N = None
        if g_N is None:
            g_N = pointmass_gN(Mb, gal["Rdisk"])
            if g_N is not None and g_N > 0:
                methods["pointmass"] += 1
            else:
                methods["skipped"] += 1
                continue

        u = 4.0 * g_N / a0
        Gu = G_btfr(u)
        # G * M_b * a_0 in m^4/s^4 -> (km/s)^4 via 1e12
        GMba0_kms4 = G_SI * (Mb * MSUN_KG) * a0 / 1.0e12
        Vf4_obs = Vf**4
        Vf4_esd = Gu * GMba0_kms4
        Vf4_mond = GMba0_kms4   # G(u) = 1

        names.append(gal["name"])
        log_Mb.append(np.log10(Mb))
        log_Vf.append(np.log10(Vf))
        log_Vf4_obs.append(np.log10(Vf4_obs))
        log_Vf4_esd.append(np.log10(Vf4_esd))
        log_Vf4_mond.append(np.log10(Vf4_mond))
        G_vals.append(Gu)
        u_vals.append(u)

    log_Mb_arr = np.array(log_Mb)
    log_Vf_arr = np.array(log_Vf)
    log_Vf4_obs_arr = np.array(log_Vf4_obs)
    log_Vf4_esd_arr = np.array(log_Vf4_esd)
    log_Vf4_mond_arr = np.array(log_Vf4_mond)
    G_vals_arr = np.array(G_vals)
    u_vals_arr = np.array(u_vals)
    N = len(log_Mb_arr)
    print(f"[btfr] analyzed {N} galaxies "
          f"(rotcurve={methods['rotcurve']}, pointmass={methods['pointmass']}, "
          f"skipped={methods['skipped']})")

    if N < 50:
        print("[btfr] sample too small for residual analysis.", file=sys.stderr)
        return 3

    # observed best-fit slope (M_b vs V_f^4)
    obs_coeffs = np.polyfit(log_Mb_arr, 4.0 * log_Vf_arr, 1)
    obs_slope = float(obs_coeffs[0])
    alpha_obs = 4.0 / obs_slope

    # ESD effective slope
    esd_coeffs = np.polyfit(log_Mb_arr, log_Vf4_esd_arr, 1)
    esd_slope = float(esd_coeffs[0])
    alpha_eff_esd = 4.0 / esd_slope

    res_esd = log_Vf4_obs_arr - log_Vf4_esd_arr
    res_mond = log_Vf4_obs_arr - log_Vf4_mond_arr
    esd_mean = float(np.mean(res_esd))
    esd_rms = float(np.std(res_esd))
    mond_mean = float(np.mean(res_mond))
    mond_rms = float(np.std(res_mond))

    # tolerance check vs published headline numbers
    repro = {
        "N":          abs(N - PUBLISHED["N"]) <= TOL["N"],
        "esd_rms":    abs(esd_rms - PUBLISHED["esd_rms_dex"]) <= TOL["rms"],
        "mond_rms":   abs(mond_rms - PUBLISHED["mond_rms_dex"]) <= TOL["rms"],
        "esd_mean":   abs(esd_mean - PUBLISHED["esd_mean_dex"]) <= TOL["mean"],
        "mond_mean":  abs(mond_mean - PUBLISHED["mond_mean_dex"]) <= TOL["mean"],
        "alpha_esd":  abs(alpha_eff_esd - PUBLISHED["alpha_eff_esd"]) <= TOL["alpha"],
    }
    overall_ok = all(repro.values())

    # write npz
    np.savez(
        NPZ_PATH,
        a_zero_SI=a0, N=N,
        names=np.array(names),
        log_Mb=log_Mb_arr, log_Vf=log_Vf_arr,
        log_Vf4_obs=log_Vf4_obs_arr,
        log_Vf4_esd=log_Vf4_esd_arr,
        log_Vf4_mond=log_Vf4_mond_arr,
        G_values=G_vals_arr, u_values=u_vals_arr,
        residuals_esd=res_esd, residuals_mond=res_mond,
        esd_mean=esd_mean, esd_rms=esd_rms,
        mond_mean=mond_mean, mond_rms=mond_rms,
        obs_slope=obs_slope, alpha_obs=alpha_obs,
        esd_slope=esd_slope, alpha_eff_esd=alpha_eff_esd,
        n_rotcurve=methods["rotcurve"], n_pointmass=methods["pointmass"],
    )
    print(f"[btfr] wrote {NPZ_PATH}")

    # JSON summary
    summary = {
        "N": N,
        "a_zero_SI": a0,
        "esd": {"mean_residual_dex": esd_mean, "rms_residual_dex": esd_rms,
                "effective_alpha": alpha_eff_esd},
        "mond": {"mean_residual_dex": mond_mean, "rms_residual_dex": mond_rms,
                 "effective_alpha": 4.0},
        "observed_alpha": alpha_obs,
        "g_N_methods": methods,
        "u_range": [float(u_vals_arr.min()), float(u_vals_arr.max())],
        "G_range": [float(G_vals_arr.min()), float(G_vals_arr.max())],
        "published": PUBLISHED,
        "tolerance": TOL,
        "reproduction": repro,
        "overall_reproduction": overall_ok,
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[btfr] wrote {JSON_PATH}")

    # human-readable
    def _ok(b: bool) -> str:
        return "OK " if b else "OFF"
    lines = [
        "=== Study 02: Full BTFR residual analysis ===",
        "  Reproducing Higginson 2026 (DOI 10.5281/zenodo.20400008)",
        "",
        f"  Sample:   N = {N}    (published: {PUBLISHED['N']})  {_ok(repro['N'])}",
        f"  Locked a_0 = {a0:.4e} m/s^2",
        f"  g_N source: rotation-curve {methods['rotcurve']}, "
        f"point-mass {methods['pointmass']}, skipped {methods['skipped']}",
        f"  u range: [{u_vals_arr.min():.3f}, {u_vals_arr.max():.3f}]",
        f"  G(u) range: [{G_vals_arr.min():.3f}, {G_vals_arr.max():.3f}]",
        "",
        "  --- ESD closure (zero free parameters) ---",
        f"  mean residual : {esd_mean:+.3f} dex   (published: {PUBLISHED['esd_mean_dex']:+.3f})  {_ok(repro['esd_mean'])}",
        f"  RMS residual  : {esd_rms:.3f} dex    (published: {PUBLISHED['esd_rms_dex']:.3f})    {_ok(repro['esd_rms'])}",
        f"  effective alpha: {alpha_eff_esd:.2f}        (published: {PUBLISHED['alpha_eff_esd']:.2f})         {_ok(repro['alpha_esd'])}",
        "",
        "  --- MOND deep limit (G(u) = 1) ---",
        f"  mean residual : {mond_mean:+.3f} dex   (published: {PUBLISHED['mond_mean_dex']:+.3f})  {_ok(repro['mond_mean'])}",
        f"  RMS residual  : {mond_rms:.3f} dex    (published: {PUBLISHED['mond_rms_dex']:.3f})    {_ok(repro['mond_rms'])}",
        "",
        f"  observed best-fit alpha: {alpha_obs:.2f}",
        "",
        f"  overall reproduction within tolerance: {overall_ok}",
    ]
    text = "\n".join(lines) + "\n"
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[btfr] wrote {TXT_PATH}")
    print()
    print(text)

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
