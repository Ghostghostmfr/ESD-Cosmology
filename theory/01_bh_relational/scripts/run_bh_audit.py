"""Theory 01 audit: ESD relational view of black holes.

Three derivations, with explicit gates:

  A. S_BH applicability:  R(u) does NOT apply to the horizon
                          entropy area-law.  Inherit S_BH from GR.
  B. Singularity resolution:  R(u) -> 0 as u -> infinity, Sigma(u)
                              never vanishes.  No UV pole.
  C. Horizon-as-boundary:  for every astrophysical BH, u >> 1 at
                           r_s and r(u=1) << r_s -- the MOND-scale
                           regime never reaches the horizon.
"""
from __future__ import annotations
import math, os, sys, json, csv

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_bh as B

OUTDIR = os.path.join(_HERE, "outputs")
os.makedirs(OUTDIR, exist_ok=True)

# ----------------- locked gates -----------------
GATE_RU_APPLIES_HORIZON   = False
GATE_KERNEL_UV_REL_ERR    = 1.0e-6      # rel err of R(u_large) ~ s/u^p
GATE_KERNEL_REGULAR       = True
GATE_HORIZON_U_MIN        = 1.0e8       # u at horizon for all BH must exceed
GATE_HORIZON_R_MAX        = 1.0e-10     # R(u) at horizon for all BH must lie below
GATE_RU1_OVER_RS_MIN      = 1.0e3       # r(u=1)/r_s must be >> 1 (MOND scale sits OUTSIDE horizon)
GATE_HBLIND               = 1.0e-15

def fmt(v):
    if isinstance(v, bool):  return str(v).lower()
    if isinstance(v, str):   return v
    if isinstance(v, float):
        if v == 0.0:                       return "0"
        if abs(v) < 1e-3 or abs(v) > 1e3:  return f"{v:.3g}"
        return f"{v:.4g}"
    return str(v)

def row(claim, value, gate_str, ok, sub=""):
    v_print = ("PASS" if ok else "FAIL")
    print(f"  {claim:<74}  {fmt(value):>12}  {gate_str:>12}  {v_print}")
    if sub:
        print(f"    {sub}")

def main():
    print()
    print("=== Theory 01: ESD relational black holes ===")
    print()
    print("  Three theory derivations from Paper 1's axioms (A1)-(A3):")
    print("    A. S_BH applicability (horizon entropy area-law)")
    print("    B. Singularity resolution (kernel UV-finiteness)")
    print("    C. Horizon as the relational boundary of R(u)")
    print()
    print(f"{'claim':<76}{'value':>14}{'target':>14}{'verdict':>9}")
    print("-" * 114)

    results = {}
    pass_count = 0
    fail_count = 0

    # ---------- Derivation A: S_BH applicability ----------
    A_test = B.applicability_test_horizon_entropy()
    ok_A1 = (A_test["Ru_applies"] == GATE_RU_APPLIES_HORIZON)
    row(
        "A1. R(u) does NOT apply to horizon entropy area-law",
        A_test["Ru_applies"], "must_be_false", ok_A1,
        sub="(A1) horizon is vacuum geometry; (A2) no bound test mass to dress  [gate: R(u)_applies == False]",
    )
    pass_count += int(ok_A1); fail_count += int(not ok_A1)
    results["A1_Ru_applies"] = A_test

    # numerical check: S_BH for a 1 Msun BH ~ 1.05e54 k_B
    sbh_1msun = B.S_BH(1.0)
    th_1msun  = B.T_Hawking(1.0)
    print(f"    [info] M=1 Msun: r_s = {B.r_schwarzschild(1.0):.3e} m, "
          f"S_BH/k_B = {sbh_1msun:.3e}, T_H = {th_1msun:.3e} K")
    sbh_m87   = B.S_BH(6.5e9)
    print(f"    [info] M87*:    r_s = {B.r_schwarzschild(6.5e9):.3e} m, "
          f"S_BH/k_B = {sbh_m87:.3e}")
    results["A_SBH_1Msun_kB"] = sbh_1msun
    results["A_SBH_M87_kB"]   = sbh_m87

    hblind_A = B.h_blindness_SBH(1.0e6)
    ok_A2 = (hblind_A <= GATE_HBLIND)
    row("A2. h-blindness of S_BH (Thm 1)",
        hblind_A, f"<= {GATE_HBLIND:g}", ok_A2,
        sub="S_BH depends only on G, M, c, hbar  [gate: <= 1e-15]")
    pass_count += int(ok_A2); fail_count += int(not ok_A2)
    results["A2_h_blindness_SBH"] = hblind_A

    # ---------- Derivation B: singularity resolution ----------
    uv = B.kernel_UV_limit(1.0e20)
    ok_B1 = (uv["rel_err"] <= GATE_KERNEL_UV_REL_ERR) and (uv["R_of_u"] > 0.0)
    row("B1. R(u) -> s / u^p as u -> infinity (no UV pole)",
        uv["rel_err"], f"<= {GATE_KERNEL_UV_REL_ERR:g}", ok_B1,
        sub=f"R(1e20) = {uv['R_of_u']:.3e}, asymptote s/u^p = {uv['R_asymptote']:.3e}")
    pass_count += int(ok_B1); fail_count += int(not ok_B1)
    results["B1_kernel_UV"] = uv

    cap = B.kernel_minimum()
    ok_B2 = bool(cap["regular"])
    row("B2. Sigma(u) > 0 for all u >= 0 (kernel regular)",
        cap["regular"], "True", ok_B2,
        sub=f"R IR cap = s/c = {cap['R_IR_cap']:.3f}, R UV limit = 0.0")
    pass_count += int(ok_B2); fail_count += int(not ok_B2)
    results["B2_kernel_regularity"] = cap

    # explicit grid sanity
    grid = [1e-12, 1e-6, 1e-3, 1.0, 10.0, 1e3, 1e9, 1e18]
    ok_B3 = B.no_UV_pole(grid)
    row("B3. no zeros of Sigma(u) on test grid",
        ok_B3, "True", ok_B3,
        sub=f"u-grid = {grid}")
    pass_count += int(ok_B3); fail_count += int(not ok_B3)
    results["B3_grid_no_zero"] = {"grid": grid, "ok": ok_B3}

    # ---------- Derivation C: horizon as relational boundary ----------
    table_h  = B.horizon_u_table()
    table_r1 = B.relational_boundary_table()
    u_min   = min(r["u_h"] for r in table_h)
    R_max   = max(r["R_h"] for r in table_h)
    ratio_min = min(r["r_u1_over_rs"] for r in table_r1)

    ok_C1 = (u_min >= GATE_HORIZON_U_MIN)
    row("C1. every astrophysical horizon has u >> 1",
        u_min, f">= {GATE_HORIZON_U_MIN:g}", ok_C1,
        sub=f"min u at horizon across catalog (largest = TON618)")
    pass_count += int(ok_C1); fail_count += int(not ok_C1)

    ok_C2 = (R_max <= GATE_HORIZON_R_MAX)
    row("C2. every astrophysical horizon has R(u) << 1",
        R_max, f"<= {GATE_HORIZON_R_MAX:g}", ok_C2,
        sub=f"max R(u) at horizon across catalog")
    pass_count += int(ok_C2); fail_count += int(not ok_C2)

    ok_C3 = (ratio_min >= GATE_RU1_OVER_RS_MIN)
    row("C3. r(u=1) / r_s >> 1 (MOND-scale shell sits OUTSIDE horizon)",
        ratio_min, f">= {GATE_RU1_OVER_RS_MIN:g}", ok_C3,
        sub="min ratio across catalog; horizons live deep in u >> 1")
    pass_count += int(ok_C3); fail_count += int(not ok_C3)

    results["C_horizon_table"]  = table_h
    results["C_boundary_table"] = table_r1

    # ---------- summary ----------
    print()
    print("  --- BH-catalog horizon table (u, R(u)) ---")
    print(f"  {'BH':<24}{'M [Msun]':>12}{'r_s [m]':>14}{'u(r_s)':>14}{'R(u_h)':>14}")
    for r in table_h:
        print(f"  {r['name']:<24}{r['M_solar']:>12.3e}{r['r_s_m']:>14.3e}"
              f"{r['u_h']:>14.3e}{r['R_h']:>14.3e}")

    print()
    print("  --- BH-catalog relational-boundary table ---")
    print(f"  {'BH':<24}{'r_s [m]':>14}{'r(u=1) [m]':>16}{'r(u=1)/r_s':>16}")
    for r in table_r1:
        print(f"  {r['name']:<24}{r['r_s_m']:>14.3e}{r['r_u1_m']:>16.3e}"
              f"{r['r_u1_over_rs']:>16.3e}")

    total = pass_count + fail_count
    print()
    if fail_count == 0:
        print(f"  ===> ALL {total} BH-THEORY CLAIMS PASS")
    else:
        print(f"  ===> {pass_count}/{total} PASS, {fail_count} FAIL")
    print()
    print("  Framework-native statements:")
    print("    A. S_BH = A / (4 l_P^2) inherited from GR; R(u) cannot")
    print("       dress a vacuum horizon area.")
    print("    B. The closure-pool kernel R(u) is regular for all u in")
    print("       [0, infinity).  Sigma(u) > 0 always; R(u) -> 0 in the")
    print("       UV (r -> 0).  The classical singularity is dressed away")
    print("       by the kernel itself, not by a separate mechanism.")
    print("    C. Every astrophysical horizon sits in u >> 1, R(u) << 1.")
    print("       The MOND-scale (R(u) ~ O(1)) regime is at r ~ AU and")
    print("       beyond -- it can never reach the horizon for any")
    print("       astrophysical BH mass.  Horizons are the deep-")
    print("       relational-floor boundary of the R(u) channel.")

    # ----------- write outputs -----------
    out_json = os.path.join(OUTDIR, "bh_audit.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    out_csv = os.path.join(OUTDIR, "bh_horizon_table.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table_h[0].keys()))
        w.writeheader();  [w.writerow(r) for r in table_h]
    out_csv2 = os.path.join(OUTDIR, "bh_boundary_table.csv")
    with open(out_csv2, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table_r1[0].keys()))
        w.writeheader();  [w.writerow(r) for r in table_r1]
    print(f"\n[bh] wrote outputs to {OUTDIR}")

if __name__ == "__main__":
    main()
