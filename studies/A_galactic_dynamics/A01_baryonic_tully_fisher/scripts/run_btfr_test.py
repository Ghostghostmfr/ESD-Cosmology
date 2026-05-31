"""SPARC BTFR low-acceleration slope test (Study 02 runner).

Procedure (as in the paper):

  1. Load cached SPARC Table 1 from `../data/sparc_table1.dat`
     (run `python fetch_sparc.py` once to populate the cache).
  2. Filter Q == 1 (highest-quality galaxies).
  3. For each galaxy compute g_char = V_f^2 / R_eff [m/s^2] and
     M_b = 0.5 * L_3.6 + 1.33 * M_HI.
  4. Keep galaxies with g_char < 0.5 * a_0 (locked a_0 from esd_core).
  5. OLS regress log10(V_f) ~ log10(M_b); report slope, stderr,
     95% CI, R^2.
  6. Compare against the locked prediction slope = 1/4 = 0.250 using
     the standard physics-paper tension criterion:
        |slope - 0.250| / stderr  ->  consistent / tension / inconsistent
  7. Cut-sensitivity scan across {0.25, 0.5, 1.0, 2.0, 10.0} * a_0;
     every cut gets the same tension grade so the verdict is not
     dominated by sample-size starvation of the deepest cut.

Outputs:
  outputs/btfr_results.npz   - all numerical results, sample arrays.
  outputs/btfr_summary.txt   - human-readable summary, paper-ready.

Exit code:
  0 every cut consistent (<=2 sigma), 1 any cut in 2-3 sigma tension,
  2 any cut inconsistent (>3 sigma), 3 data / fit error.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from esd_btfr import a_zero_SI, baryonic_mass_solar, predicted_btfr_slope  # noqa: E402

DATA_PATH = os.path.abspath(os.path.join(_HERE, "..", "data", "sparc_table1.dat"))
OUT_DIR = os.path.join(_HERE, "outputs")
NPZ_PATH = os.path.join(OUT_DIR, "btfr_results.npz")
TXT_PATH = os.path.join(OUT_DIR, "btfr_summary.txt")
JSON_PATH = os.path.join(OUT_DIR, "btfr_summary.json")

# Unit conversions.
KPC_TO_M = 3.0857e19
KMS_TO_MS = 1.0e3


# ----------------------------------------------------------------------- parsing

def parse_sparc_table1(path: str) -> list[dict]:
    """Parse SPARC Table 1 (VizieR J/AJ/152/157, machine-readable).

    Column layout (0-indexed, per the .ReadMe):
       0 Galaxy   1 T   2 D[Mpc]   3 e_D   4 f_D
       5 Inc[deg] 6 e_Inc
       7 L36[1e9 Lsun]  8 e_L36
       9 Reff[kpc]  10 SBeff
      11 Rdisk[kpc] 12 SBdisk
      13 MHI[1e9 Msun]  14 RHI[kpc]
      15 Vflat[km/s] 16 e_Vflat
      17 Q  18 Ref
    """
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if not ln.strip() or ln.startswith("#"):
                continue
            parts = ln.split()
            if len(parts) < 18:
                continue
            try:
                name = parts[0]
                L36 = float(parts[7])
                R_eff = float(parts[9])
                MHI = float(parts[13])
                Vflat = float(parts[15])
                Q = int(parts[17])
            except (ValueError, IndexError):
                continue
            if Vflat <= 0.0 or R_eff <= 0.0 or L36 <= 0.0:
                continue
            rows.append(
                {"name": name, "L36": L36, "R_eff": R_eff,
                 "MHI": MHI, "Vflat": Vflat, "Q": Q}
            )
    return rows


def g_char_si(Vflat_kms: float, R_eff_kpc: float) -> float:
    """Characteristic centripetal acceleration V^2/R [m/s^2]."""
    V = Vflat_kms * KMS_TO_MS
    R = R_eff_kpc * KPC_TO_M
    return V * V / R


# ----------------------------------------------------------------------- regression

def ols_slope(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, float]:
    """Plain OLS y = a + b*x.  Returns (slope, stderr_slope, R^2, intercept)."""
    n = x.size
    xbar = float(x.mean())
    ybar = float(y.mean())
    Sxx = float(np.sum((x - xbar) ** 2))
    Sxy = float(np.sum((x - xbar) * (y - ybar)))
    b = Sxy / Sxx
    a = ybar - b * xbar
    yhat = a + b * x
    SSE = float(np.sum((y - yhat) ** 2))
    SST = float(np.sum((y - ybar) ** 2))
    R2 = 1.0 - SSE / SST
    sigma2 = SSE / (n - 2)
    se_b = float(np.sqrt(sigma2 / Sxx))
    return b, se_b, R2, a


# ----------------------------------------------------------------------- main

def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(DATA_PATH):
        print(
            f"[btfr] cached SPARC table not found at {DATA_PATH}\n"
            f"       run `python fetch_sparc.py` first.",
            file=sys.stderr,
        )
        return 3

    rows_all = parse_sparc_table1(DATA_PATH)
    print(f"[btfr] parsed {len(rows_all)} galaxy rows from SPARC.")

    rows_q1 = [r for r in rows_all if r["Q"] == 1]
    print(f"[btfr] after Q==1 filter: {len(rows_q1)}")

    a0 = a_zero_SI()
    threshold = 0.5 * a0
    print(f"[btfr] locked a_0 from esd_core = {a0:.4e} m/s^2")
    print(f"[btfr] deep-regime cut: g_char < 0.5*a_0 = {threshold:.4e} m/s^2")

    kept: list[dict] = []
    for r in rows_q1:
        g = g_char_si(r["Vflat"], r["R_eff"])
        if g < threshold:
            r2 = dict(r)
            r2["g_char"] = g
            r2["M_b"] = baryonic_mass_solar(r["L36"], r["MHI"])
            kept.append(r2)
    print(f"[btfr] after deep-regime cut: {len(kept)} galaxies")

    if len(kept) < 5:
        print("[btfr] sample too small to fit.", file=sys.stderr)
        return 3

    logV = np.array([np.log10(r["Vflat"]) for r in kept])
    logM = np.array([np.log10(r["M_b"]) for r in kept])
    M_b = np.array([r["M_b"] for r in kept])
    Vflat = np.array([r["Vflat"] for r in kept])
    g_arr = np.array([r["g_char"] for r in kept])

    slope, se, R2, intercept = ols_slope(logM, logV)
    t95 = 1.96
    ci_lo = slope - t95 * se
    ci_hi = slope + t95 * se

    pred = predicted_btfr_slope()

    def grade(slope_v: float, se_v: float) -> tuple[float, str]:
        """Standard physics-paper tension grading.

        Returns (n_sigma, label) where label is one of
        CONSISTENT / TENSION / INCONSISTENT.
        """
        n = abs(slope_v - pred) / se_v if se_v > 0 else float("inf")
        if n <= 2.0:
            return n, "CONSISTENT"
        if n <= 3.0:
            return n, "TENSION"
        return n, "INCONSISTENT"

    n_sigma, verdict = grade(slope, se)
    in_2sigma = n_sigma <= 2.0

    # cut sensitivity ----------------------------------------------------------
    cuts: list[dict] = []
    for frac in (0.25, 0.5, 1.0, 2.0, 10.0):
        sub = [r for r in rows_q1 if g_char_si(r["Vflat"], r["R_eff"]) < frac * a0]
        if len(sub) < 5:
            cuts.append({"frac": frac, "N": len(sub), "slope": None,
                         "stderr": None, "R2": None,
                         "n_sigma": None, "verdict": "INSUFFICIENT_N"})
            continue
        lV = np.array([np.log10(r["Vflat"]) for r in sub])
        lM = np.array([np.log10(baryonic_mass_solar(r["L36"], r["MHI"])) for r in sub])
        s, ses, r2v, _ = ols_slope(lM, lV)
        ns, vd = grade(s, ses)
        cuts.append({"frac": frac, "N": len(sub), "slope": s,
                     "stderr": ses, "R2": r2v,
                     "n_sigma": ns, "verdict": vd})

    # roll-up exit code over all cuts that produced a fit
    fit_verdicts = [c["verdict"] for c in cuts if c["slope"] is not None]
    if any(v == "INCONSISTENT" for v in fit_verdicts):
        exit_code = 2
    elif any(v == "TENSION" for v in fit_verdicts):
        exit_code = 1
    else:
        exit_code = 0

    # write outputs ------------------------------------------------------------
    np.savez(
        NPZ_PATH,
        # main fit
        slope=slope, stderr=se, R2=R2, intercept=intercept,
        ci_lo=ci_lo, ci_hi=ci_hi,
        predicted_slope=pred, a_zero_SI=a0, threshold=threshold,
        N_kept=len(kept), N_q1=len(rows_q1), N_all=len(rows_all),
        n_sigma=n_sigma, verdict=verdict,
        # sample arrays
        logM=logM, logV=logV, M_b=M_b, Vflat=Vflat, g_char=g_arr,
        names=np.array([r["name"] for r in kept]),
        # cut sweep (parallel arrays)
        cut_frac=np.array([c["frac"] for c in cuts]),
        cut_N=np.array([c["N"] for c in cuts]),
        cut_slope=np.array([np.nan if c["slope"] is None else c["slope"] for c in cuts]),
        cut_stderr=np.array([np.nan if c["stderr"] is None else c["stderr"] for c in cuts]),
        cut_R2=np.array([np.nan if c["R2"] is None else c["R2"] for c in cuts]),
        cut_n_sigma=np.array([np.nan if c["n_sigma"] is None else c["n_sigma"] for c in cuts]),
        cut_verdict=np.array([c["verdict"] for c in cuts]),
    )
    print(f"[btfr] wrote {NPZ_PATH}")

    summary_lines = [
        "=== Study 02: SPARC BTFR low-acceleration slope ===",
        f"  N (all SPARC)         : {len(rows_all)}",
        f"  N (Q==1)              : {len(rows_q1)}",
        f"  N (deep regime kept)  : {len(kept)}",
        f"  Locked a_0 [m/s^2]    : {a0:.4e}",
        f"  Cut threshold [m/s^2] : {threshold:.4e}",
        "",
        "  --- deep-regime regression (g < 0.5 * a_0) ---",
        f"  slope        : {slope:.4f}",
        f"  stderr       : {se:.4f}",
        f"  95% CI       : [{ci_lo:.4f}, {ci_hi:.4f}]",
        f"  R^2          : {R2:.4f}",
        f"  intercept    : {intercept:.4f}",
        "",
        "  --- acceptance (standard tension grading) ---",
        f"  predicted slope         : {pred:.3f}",
        f"  tension                 : {n_sigma:.2f} sigma",
        f"  predicted in 95% CI     : {in_2sigma}",
        f"  verdict (deep cut)      : {verdict}",
        "",
        "  --- cut sensitivity (g < frac * a_0) ---",
        "    grading: CONSISTENT (<=2 sigma) | TENSION (2-3) | INCONSISTENT (>3)",
    ]
    for c in cuts:
        if c["slope"] is None:
            summary_lines.append(
                f"    frac={c['frac']:>5}  N={c['N']:3d}  (insufficient N)"
            )
        else:
            summary_lines.append(
                f"    frac={c['frac']:>5}  N={c['N']:3d}  "
                f"slope={c['slope']:.3f} +/- {c['stderr']:.3f}  R^2={c['R2']:.3f}  "
                f"tension={c['n_sigma']:.2f} sigma  -> {c['verdict']}"
            )
    summary_lines.append("")
    summary_lines.append(
        f"  Overall verdict (worst across all fit cuts): "
        f"{['CONSISTENT', 'TENSION', 'INCONSISTENT'][exit_code]}"
    )
    summary_text = "\n".join(summary_lines) + "\n"
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write(summary_text)
    print(f"[btfr] wrote {TXT_PATH}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "slope": slope, "stderr": se, "R2": R2, "intercept": intercept,
            "ci_lo": ci_lo, "ci_hi": ci_hi,
            "predicted_slope": pred, "a_zero_SI": a0, "threshold": threshold,
            "N_all": len(rows_all), "N_q1": len(rows_q1), "N_kept": len(kept),
            "n_sigma": n_sigma, "verdict": verdict,
            "predicted_in_CI95": in_2sigma,
            "cuts": cuts,
            "overall_verdict": ["CONSISTENT", "TENSION", "INCONSISTENT"][exit_code],
        }, f, indent=2)
    print(f"[btfr] wrote {JSON_PATH}")

    print()
    print(summary_text)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
