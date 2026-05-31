"""Study 22: DESI Y1 BAO + Planck 2018 CMB distance prior joint w0-wa test.

Computes a profiled chi^2 landscape in the (w0, wa) plane using:
  - DESI Y1 BAO (7 tracers, arXiv:2404.03002 Table 1)
  - Planck 2018 CMB compressed distance prior (Chen+2019, arXiv:1902.09081)
  - Pantheon+ SN Ia 20-bin (Brout+2022, approximate) — if enabled

At each (w0, wa) grid point the chi^2 is minimised over H0 in [55, 85].
The ESD framework prediction w0=-1, wa=0 is evaluated at its natural
anchor H0=67.36.

Gates:
  1. |Delta_chi2_BAO(ESD - Planck-LCDM)| <= 5    (BAO-only, inherits Std 07)
  2. Delta_chi2_2D(ESD vs best-fit CPL, BAO+CMB) < 11.83  (< 3sigma in 2D)

Gate 3 (reported, not gated): tension sigma level is always printed and
written to the summary JSON as an honest negative.  The published DESI Y1
+ Planck CMB result places the CPL best-fit at ~2.3 sigma from LCDM
(arXiv:2404.03002 Table 4); ESD's w0=-1,wa=0 prediction lies at
approximately the same offset, so Gate 2 is expected to pass at DESI Y1
precision.  This gate is the leading falsifier candidate for DESI Y3/Y5.

Outputs (written to scripts/outputs/):
  summary.json    gate verdicts, key chi^2 values, tension sigma
  chi2_grid.npz   2D profiled chi^2 arrays for figure generation
  per_tracer.csv  per-tracer residuals for ESD and Planck-LCDM
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
from typing import List

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2 as chi2_dist

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from cmb_prior_data import chi2_cmb  # noqa: E402
from desi_bao_data import DESI_Y1, DMDH, DV, N_MEAS  # noqa: E402
from esd_w0wa import (  # noqa: E402
    Cosmo,
    D_H,
    D_M,
    D_V,
    cmb_acoustic_l_A,
    cmb_shift_R,
    cosmo_esd_primary,
    cosmo_planck_lcdm,
    mu_sn,
    r_d_aubourg2015,
)
from pantheon_plus_data import PANTHEON_PLUS, SNBin  # noqa: E402

import esd_core as ESD  # noqa: E402

OUT_DIR = os.path.join(_HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Gate thresholds
# ---------------------------------------------------------------------------
GATE1_DCHI2_BAO:   float = 5.0      # |Delta chi^2_BAO(ESD - Planck)| <= this
GATE2_DCHI2_2D:    float = 11.83    # Delta chi^2_2D < this (3-sigma in 2D)

# Two-sigma and three-sigma Δchi^2 thresholds for a 2-parameter chi^2.
DCHI2_1SIGMA: float = 2.30
DCHI2_2SIGMA: float = 6.18
DCHI2_3SIGMA: float = 11.83

# w0-wa grid parameters for the profiled chi^2 scan.
W0_MIN, W0_MAX, NW0 = -2.0, 0.2, 121
WA_MIN, WA_MAX, NWA = -3.5, 1.5, 121


# ---------------------------------------------------------------------------
# BAO chi^2
# ---------------------------------------------------------------------------
def chi2_bao_single(c: Cosmo) -> float:
    """BAO chi^2 summed over all DESI Y1 tracers."""
    rd = r_d_aubourg2015(c)
    total = 0.0
    for t in DESI_Y1:
        if isinstance(t, DV):
            th = D_V(c, t.z_eff) / rd
            total += ((th - t.DV_rd) / t.sigma) ** 2
        else:
            th_M = D_M(c, t.z_eff) / rd
            th_H = D_H(c, t.z_eff) / rd
            dM, dH = th_M - t.DM_rd, th_H - t.DH_rd
            cov = np.array([
                [t.DM_sig ** 2,                t.rho * t.DM_sig * t.DH_sig],
                [t.rho * t.DM_sig * t.DH_sig,  t.DH_sig ** 2],
            ])
            d = np.array([dM, dH])
            total += float(d @ np.linalg.inv(cov) @ d)
    return total


# ---------------------------------------------------------------------------
# CMB chi^2
# ---------------------------------------------------------------------------
def chi2_cmb_single(c: Cosmo) -> float:
    """CMB chi^2 from the 3-parameter Planck 2018 compressed distance prior."""
    R    = cmb_shift_R(c)
    l_A  = cmb_acoustic_l_A(c)
    obh2 = c.omega_b
    return chi2_cmb(R, l_A, obh2)


# ---------------------------------------------------------------------------
# SN chi^2 (marginalised over M_B / H0 offset)
# ---------------------------------------------------------------------------
def chi2_sn_marginal(c: Cosmo, sn_bins: list[SNBin]) -> float:
    """SN chi^2 analytically marginalised over the magnitude offset M.

    Only the SHAPE of the Hubble diagram constrains (w0, wa, Omega_m).
    The optimal offset M_opt is computed analytically and removed.
    """
    if not sn_bins:
        return 0.0
    mu_th  = np.array([mu_sn(c, b.z) for b in sn_bins])
    mu_dat = np.array([b.mu for b in sn_bins])
    sigma  = np.array([b.sigma for b in sn_bins])
    w      = 1.0 / sigma ** 2
    delta  = mu_th - mu_dat
    M_opt  = np.sum(w * delta) / np.sum(w)
    residual = delta - M_opt
    return float(np.sum(w * residual ** 2))


# ---------------------------------------------------------------------------
# Combined chi^2 for a given Cosmo object
# ---------------------------------------------------------------------------
def chi2_total(c: Cosmo, use_sn: bool = True) -> float:
    c2  = chi2_bao_single(c)
    c2 += chi2_cmb_single(c)
    if use_sn and PANTHEON_PLUS:
        c2 += chi2_sn_marginal(c, PANTHEON_PLUS)
    return c2


# ---------------------------------------------------------------------------
# w0-wa profiled chi^2 grid scan
# ---------------------------------------------------------------------------
def scan_w0wa_grid(
    Omega_m: float,
    Omega_b: float,
    use_sn: bool = True,
) -> dict:
    """Scan (w0, wa) grid, profiling over H0 at each point.

    Returns a dict with keys:
      w0_grid, wa_grid, chi2_map, H0_map, w0_bf, wa_bf, H0_bf, chi2_min
    """
    w0_arr = np.linspace(W0_MIN, W0_MAX, NW0)
    wa_arr = np.linspace(WA_MIN, WA_MAX, NWA)
    chi2_map = np.full((NW0, NWA), np.nan)
    H0_map   = np.full((NW0, NWA), np.nan)

    for i, w0 in enumerate(w0_arr):
        for j, wa in enumerate(wa_arr):
            def _obj(H0: float) -> float:
                c = Cosmo(H0=H0, Omega_m=Omega_m, Omega_b=Omega_b,
                          w0=w0, wa=wa)
                return chi2_total(c, use_sn=use_sn)

            res = minimize_scalar(_obj, bounds=(55.0, 85.0), method="bounded",
                                  options={"xatol": 0.05})
            chi2_map[i, j] = res.fun
            H0_map[i, j]   = res.x

    idx_flat = int(np.nanargmin(chi2_map))
    i_bf, j_bf = np.unravel_index(idx_flat, chi2_map.shape)
    return {
        "w0_arr":   w0_arr,
        "wa_arr":   wa_arr,
        "chi2_map": chi2_map,
        "H0_map":   H0_map,
        "w0_bf":    float(w0_arr[i_bf]),
        "wa_bf":    float(wa_arr[j_bf]),
        "H0_bf":    float(H0_map[i_bf, j_bf]),
        "chi2_min": float(chi2_map[i_bf, j_bf]),
    }


# ---------------------------------------------------------------------------
# Per-tracer residual table
# ---------------------------------------------------------------------------
def per_tracer_residuals(cosmologies: list[tuple[str, Cosmo]]) -> list[dict]:
    rows = []
    for label, c in cosmologies:
        rd = r_d_aubourg2015(c)
        for t in DESI_Y1:
            if isinstance(t, DV):
                th = D_V(c, t.z_eff) / rd
                rows.append({
                    "label": label, "tracer": t.name, "z": t.z_eff,
                    "kind": "DV",
                    "theory": th, "data": t.DV_rd, "sigma": t.sigma,
                    "residual": (th - t.DV_rd) / t.sigma,
                    "chi2_tracer": ((th - t.DV_rd) / t.sigma) ** 2,
                })
            else:
                th_M = D_M(c, t.z_eff) / rd
                th_H = D_H(c, t.z_eff) / rd
                rows.append({
                    "label": label, "tracer": t.name, "z": t.z_eff,
                    "kind": "DM",
                    "theory": th_M, "data": t.DM_rd, "sigma": t.DM_sig,
                    "residual": (th_M - t.DM_rd) / t.DM_sig,
                    "chi2_tracer": None,
                })
                rows.append({
                    "label": label, "tracer": t.name, "z": t.z_eff,
                    "kind": "DH",
                    "theory": th_H, "data": t.DH_rd, "sigma": t.DH_sig,
                    "residual": (th_H - t.DH_rd) / t.DH_sig,
                    "chi2_tracer": None,
                })
    return rows


# ---------------------------------------------------------------------------
# Sigma conversion for 2D chi^2
# ---------------------------------------------------------------------------
def dchi2_to_sigma_2d(dchi2: float) -> float:
    """Convert Δchi^2 to sigma for a 2D constraint (chi^2 with 2 dof)."""
    if dchi2 <= 0.0:
        return 0.0
    p_value = 1.0 - chi2_dist.cdf(dchi2, df=2)
    # Convert p-value to equivalent 1D sigma via inverse normal CDF.
    from scipy.special import erfinv
    return math.sqrt(2.0) * float(erfinv(1.0 - p_value))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    use_sn = bool(PANTHEON_PLUS)
    print(f"[w0wa] SN arm: {'ACTIVE' if use_sn else 'DISABLED'} "
          f"({len(PANTHEON_PLUS)} bins)")
    print(f"[w0wa] w0 grid: {NW0} points in [{W0_MIN}, {W0_MAX}]")
    print(f"[w0wa] wa grid: {NWA} points in [{WA_MIN}, {WA_MAX}]")
    print(f"[w0wa] total grid points: {NW0 * NWA} — scanning now ...")

    Om = ESD.OMEGA_M_LOCK
    Ob = ESD.OMEGA_B_INPUT   # PRIMARY reading

    # ---- Gate 1: BAO-only chi^2 (same criterion as Study 07) ---------------
    c_esd  = cosmo_esd_primary(67.36)
    c_pla  = cosmo_planck_lcdm(67.36)
    chi2_bao_esd   = chi2_bao_single(c_esd)
    chi2_bao_planck = chi2_bao_single(c_pla)
    dchi2_bao = chi2_bao_esd - chi2_bao_planck
    gate1_pass = abs(dchi2_bao) <= GATE1_DCHI2_BAO

    # ---- w0-wa grid scan (BAO + CMB [+ SN]) --------------------------------
    grid = scan_w0wa_grid(Om, Ob, use_sn=use_sn)
    print(f"[w0wa] grid scan done.  Best-fit: w0={grid['w0_bf']:.3f}, "
          f"wa={grid['wa_bf']:.3f}, H0={grid['H0_bf']:.2f}, "
          f"chi2_min={grid['chi2_min']:.3f}")

    # ---- ESD chi^2 at its natural H0 anchor --------------------------------
    chi2_esd_full = chi2_total(c_esd, use_sn=use_sn)
    dchi2_2d_esd  = chi2_esd_full - grid["chi2_min"]
    tension_sigma = dchi2_to_sigma_2d(dchi2_2d_esd)
    gate2_pass    = dchi2_2d_esd < GATE2_DCHI2_2D

    # Also compute CMB observables for ESD to report
    R_esd   = cmb_shift_R(c_esd)
    lA_esd  = cmb_acoustic_l_A(c_esd)
    obh2_esd = c_esd.omega_b

    # ---- Per-tracer residuals for CSV output --------------------------------
    residuals = per_tracer_residuals([
        ("ESD-PRIMARY (H0=67.36)",  c_esd),
        ("Planck-LCDM (H0=67.36)", c_pla),
    ])
    csv_path = os.path.join(OUT_DIR, "per_tracer.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "label", "tracer", "z", "kind",
            "theory", "data", "sigma", "residual", "chi2_tracer",
        ])
        w.writeheader()
        w.writerows(residuals)
    print(f"[w0wa] wrote {csv_path}")

    # ---- Save chi^2 grid as .npz for figures --------------------------------
    npz_path = os.path.join(OUT_DIR, "chi2_grid.npz")
    np.savez_compressed(
        npz_path,
        w0_arr=grid["w0_arr"],
        wa_arr=grid["wa_arr"],
        chi2_map=grid["chi2_map"],
        H0_map=grid["H0_map"],
        chi2_min=grid["chi2_min"],
        w0_bf=grid["w0_bf"],
        wa_bf=grid["wa_bf"],
        H0_bf=grid["H0_bf"],
    )
    print(f"[w0wa] wrote {npz_path}")

    # ---- Summary lines ------------------------------------------------------
    lines = []
    lines.append("=== Study 22: DESI Y1 BAO + Planck CMB w0-wa joint test ===")
    lines.append("")
    lines.append("ESD framework prediction: w0 = -1, wa = 0 (theorem, not fit)")
    lines.append(f"ESD cosmology: Omega_m={Om:.5f}, Omega_b={Ob:.5f}, H0=67.36")
    lines.append("")
    lines.append(f"  SN arm: {'ACTIVE (' + str(len(PANTHEON_PLUS)) + ' bins, approx)' if use_sn else 'DISABLED'}")
    lines.append(f"  N_BAO = {N_MEAS},  N_SN = {len(PANTHEON_PLUS)},  N_CMB = 3")
    lines.append("")
    lines.append("--- Gate 1: BAO-only chi^2 ---")
    lines.append(f"  chi^2_BAO(ESD-PRIMARY)  = {chi2_bao_esd:.3f}")
    lines.append(f"  chi^2_BAO(Planck-LCDM)  = {chi2_bao_planck:.3f}")
    lines.append(f"  Delta chi^2_BAO          = {dchi2_bao:+.3f}")
    lines.append(f"  Gate: |Delta chi^2| <= {GATE1_DCHI2_BAO}")
    lines.append(f"  ===> Gate 1 {'PASS' if gate1_pass else 'FAIL'}")
    lines.append("")
    lines.append("--- CMB observables (ESD at H0=67.36) ---")
    lines.append(f"  R_model    = {R_esd:.4f}  (Planck: 1.7492 +/- 0.0044)")
    lines.append(f"  l_A_model  = {lA_esd:.3f} (Planck: 301.80 +/- 0.14)")
    lines.append(f"  omega_b    = {obh2_esd:.5f}  (Planck: 0.02237 +/- 0.00015)")
    lines.append(f"  chi^2_CMB(ESD) = {chi2_cmb_single(c_esd):.3f}")
    lines.append("")
    lines.append("--- Gate 2: BAO + CMB (+ SN) joint w0-wa ---")
    lines.append(f"  Best-fit CPL: w0={grid['w0_bf']:.3f}, wa={grid['wa_bf']:.3f}, "
                 f"H0={grid['H0_bf']:.2f}, chi^2={grid['chi2_min']:.3f}")
    lines.append(f"  ESD (w0=-1, wa=0, H0=67.36): chi^2={chi2_esd_full:.3f}")
    lines.append(f"  Delta chi^2_2D(ESD vs best-fit CPL) = {dchi2_2d_esd:.3f}")
    lines.append(f"  Tension: {tension_sigma:.2f} sigma  "
                 f"[2D: 1s={DCHI2_1SIGMA}, 2s={DCHI2_2SIGMA}, "
                 f"3s={DCHI2_3SIGMA}]")
    lines.append(f"  Gate: Delta chi^2_2D < {GATE2_DCHI2_2D}")
    lines.append(f"  ===> Gate 2 {'PASS' if gate2_pass else 'FAIL'}")
    lines.append("")
    lines.append("--- Gate 3: Honest negative (ALWAYS REPORTED) ---")
    if tension_sigma < 2.0:
        lines.append(f"  Tension: {tension_sigma:.2f} sigma — ESD consistent with DESI+CMB joint.")
    elif tension_sigma < 3.0:
        lines.append(f"  TENSION FLAG ({tension_sigma:.2f} sigma): DESI+CMB prefer w0 != -1, wa != 0.")
        lines.append("  This is a potential falsifier. Verdict deferred to DESI Y3/Y5 + Euclid Y1.")
    else:
        lines.append(f"  FALSIFIER FLAG ({tension_sigma:.2f} sigma >= 3 sigma): "
                     "DESI+CMB data strongly disfavour ESD's w0=-1, wa=0 prediction.")
        lines.append("  Framework vacuum-applicability theorem (theory/02) is in tension.")
    lines.append("")
    lines.append("Published DESI Y1 + Planck CMB reference: ~2.3 sigma from LCDM")
    lines.append("(arXiv:2404.03002 Table 4, BAO + CMB combination).")
    lines.append("ESD prediction coincides with LCDM for (w0, wa), so the")
    lines.append("same ~2.3 sigma offset is expected at DESI Y1 precision.")

    # Write text summary
    txt_path = os.path.join(OUT_DIR, "summary.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # Print to console
    for line in lines:
        print(line)

    # Write JSON summary
    summary = {
        "gate1_criterion": f"|Delta_chi2_BAO| <= {GATE1_DCHI2_BAO}",
        "gate1_delta_chi2_bao": dchi2_bao,
        "gate1_verdict": "PASS" if gate1_pass else "FAIL",
        "gate2_criterion": f"Delta_chi2_2D < {GATE2_DCHI2_2D}",
        "gate2_delta_chi2_2d": dchi2_2d_esd,
        "gate2_tension_sigma": tension_sigma,
        "gate2_verdict": "PASS" if gate2_pass else "FAIL",
        "sn_arm_active": use_sn,
        "n_sn_bins": len(PANTHEON_PLUS),
        "esd_primary": {
            "H0": 67.36,
            "Omega_m": Om,
            "Omega_b": Ob,
            "w0": -1.0,
            "wa":  0.0,
            "chi2_bao": chi2_bao_esd,
            "chi2_cmb": chi2_cmb_single(c_esd),
            "chi2_total": chi2_esd_full,
            "R_model":    R_esd,
            "l_A_model":  lA_esd,
            "omega_b_model": obh2_esd,
        },
        "planck_lcdm_bao_chi2": chi2_bao_planck,
        "best_fit_cpl": {
            "w0": grid["w0_bf"],
            "wa": grid["wa_bf"],
            "H0": grid["H0_bf"],
            "chi2_min": grid["chi2_min"],
        },
        "grid": {
            "w0_min": W0_MIN, "w0_max": W0_MAX, "nw0": NW0,
            "wa_min": WA_MIN, "wa_max": WA_MAX, "nwa": NWA,
        },
        "honest_negative": {
            "tension_sigma": tension_sigma,
            "reference_desi_y1_cmb_tension_sigma": 2.3,
            "note": (
                "DESI Y1 + Planck CMB prefer CPL over LCDM at ~2.3 sigma "
                "(arXiv:2404.03002 Table 4). ESD predicts w0=-1, wa=0 "
                "(same as LCDM for this sector). Decisive test: DESI Y3/Y5 "
                "+ Euclid Y1 (expected ~5x improvement in w0-wa precision)."
            ),
        },
    }
    json_path = os.path.join(OUT_DIR, "summary.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[w0wa] wrote {json_path}")

    both_pass = gate1_pass and gate2_pass
    print(f"\n[w0wa] OVERALL: {'PASS' if both_pass else 'FAIL'} "
          f"(gate1={'PASS' if gate1_pass else 'FAIL'}, "
          f"gate2={'PASS' if gate2_pass else 'FAIL'})")
    return 0 if both_pass else 1


if __name__ == "__main__":
    sys.exit(main())
