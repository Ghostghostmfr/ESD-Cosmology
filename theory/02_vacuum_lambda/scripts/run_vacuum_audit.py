"""Theory 02 audit: ESD vacuum / cosmological-constant applicability."""
from __future__ import annotations
import math, os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_vacuum as V

OUTDIR = os.path.join(_HERE, "outputs")
os.makedirs(OUTDIR, exist_ok=True)

# ----------------- locked gates -----------------
GATE_RU_VACUUM             = False        # R(u) must NOT apply
GATE_W_DE                  = 1.0e-12      # |w + 1| <= eps
GATE_F_DE_FLAT             = 1.0e-12      # f_DE(z) = 1 across redshift
GATE_OMEGA_L_VS_PLANCK     = 1.0e-3       # ESD-derived Omega_L vs Planck
GATE_NO_RUNNING            = 1.0e-12      # rho_Lambda(z=1100)/rho_Lambda(0) - 1
GATE_FRIEDMANN_CLOSURE     = 1.0e-12      # 1 - sum should be zero
GATE_HBLIND_W              = 1.0e-15
GATE_HBLIND_RUN            = 1.0e-12

# honesty gates
GATE_PHI_LOCK_THRESHOLD    = 1.0e-2       # under this would mean a "lock"

def fmt(v):
    if isinstance(v, bool):  return str(v).lower()
    if isinstance(v, str):   return v
    if isinstance(v, float):
        if v == 0.0:                       return "0"
        if abs(v) < 1e-3 or abs(v) > 1e3:  return f"{v:.3g}"
        return f"{v:.6g}"
    return str(v)

def row(claim, value, gate_str, ok, sub=""):
    v_print = ("PASS" if ok else "FAIL")
    print(f"  {claim:<74}  {fmt(value):>16}  {gate_str:>16}  {v_print}")
    if sub:
        print(f"    {sub}")

def main():
    print()
    print("=== Theory 02: ESD vacuum / cosmological-constant applicability ===")
    print()
    print("  Apply axioms (A1)-(A3) to Lambda. A1 fails (vacuum is a uniform")
    print("  background, no system/spectator split). A2 fails (no Newtonian g")
    print("  of a bound subsystem; only the de Sitter expansion rate).")
    print("  Therefore R(u) does NOT modify Lambda.")
    print()
    print(f"{'claim':<76}{'value':>18}{'target':>18}{'verdict':>9}")
    print("-" * 123)

    results = {}
    pass_count = 0
    fail_count = 0

    # ---------- A: vacuum applicability ----------
    A = V.applicability_test_vacuum()
    ok_A = (A["Ru_applies"] == GATE_RU_VACUUM)
    row("A. R(u) does NOT apply to the cosmological vacuum",
        A["Ru_applies"], "must_be_false", ok_A,
        sub="(A1) no system/spectator split; (A2) no Newtonian g of a bound mass  [gate: R(u)_applies == False]")
    pass_count += int(ok_A); fail_count += int(not ok_A)
    results["A_vacuum_applicability"] = A

    # ---------- B: w = -1 inheritance ----------
    w = V.w_dark_energy_ESD()
    err_w = abs(w - (-1.0))
    ok_B = (err_w <= GATE_W_DE)
    row("B1. ESD dark-energy equation of state w = -1 exactly",
        err_w, f"<= {GATE_W_DE:g}", ok_B,
        sub=f"w_ESD = {w}")
    pass_count += int(ok_B); fail_count += int(not ok_B)

    # f_DE(z) = 1 across a redshift grid
    f_devs = [abs(V.f_DE(z) - 1.0) for z in [0.0, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0, 1100.0]]
    max_f_dev = max(f_devs)
    ok_B2 = (max_f_dev <= GATE_F_DE_FLAT)
    row("B2. f_DE(z) = 1 across z in [0, 1100]  (no DE evolution)",
        max_f_dev, f"<= {GATE_F_DE_FLAT:g}", ok_B2,
        sub=f"max |f_DE(z) - 1| over z grid [0, 0.1, 0.5, 1, 2, 10, 100, 1100]")
    pass_count += int(ok_B2); fail_count += int(not ok_B2)
    results["B_w_DE"]      = w
    results["B_f_DE_grid"] = f_devs

    # ---------- C: Omega_Lambda inheritance ----------
    OL = V.omega_lambda_ESD(omega_k=0.0)
    OL_target = V.OMEGA_LAMBDA_PLANCK
    err_OL = abs(OL - OL_target)
    ok_C = (err_OL <= GATE_OMEGA_L_VS_PLANCK)
    row("C1. Omega_Lambda_ESD inherited from Friedmann sum",
        OL, f"-> {OL_target:.4f}", ok_C,
        sub=f"|Omega_Lambda_ESD - Omega_Lambda_Planck| = {err_OL:.2e}  [gate: <= {GATE_OMEGA_L_VS_PLANCK:g}]")
    pass_count += int(ok_C); fail_count += int(not ok_C)

    # Friedmann closure: 1 = Om + Or + Ol
    sum_components = V.OMEGA_M_LOCK_VAL + V.omega_r() + OL
    closure_err = abs(1.0 - sum_components)
    ok_C2 = (closure_err <= GATE_FRIEDMANN_CLOSURE)
    row("C2. Friedmann sum closes: Om + Or + Ol = 1",
        sum_components, "1.0", ok_C2,
        sub=f"|1 - (Om + Or + Ol)| = {closure_err:.2e}  [gate: <= {GATE_FRIEDMANN_CLOSURE:g}]")
    pass_count += int(ok_C2); fail_count += int(not ok_C2)
    results["C_Omega_Lambda_ESD"]   = OL
    results["C_Omega_Lambda_Planck"] = OL_target
    results["C_Omega_m_lock"]       = V.OMEGA_M_LOCK_VAL
    results["C_Omega_r"]            = V.omega_r()
    results["C_Omega_gamma"]        = V.omega_gamma()
    results["C_Omega_nu_rel"]       = V.omega_nu_relativistic()

    # ---------- D: no Lambda running ----------
    run_err = abs(V.rho_lambda_running(0.0, 1100.0) - 1.0)
    ok_D = (run_err <= GATE_NO_RUNNING)
    row("D. rho_Lambda(z=0) = rho_Lambda(z=1100)  (no running)",
        run_err, f"<= {GATE_NO_RUNNING:g}", ok_D,
        sub="for w = -1, f_DE(z) = 1 identically  ->  rho_Lambda constant in time")
    pass_count += int(ok_D); fail_count += int(not ok_D)

    # ---------- E: h-blindness ----------
    hb_w   = V.h_blindness_w()
    hb_run = V.h_blindness_running(0.0, 1100.0)
    ok_E1  = (hb_w   <= GATE_HBLIND_W)
    ok_E2  = (hb_run <= GATE_HBLIND_RUN)
    row("E1. h-blindness of w(z)",
        hb_w, f"<= {GATE_HBLIND_W:g}", ok_E1,
        sub="w = -1 trivially H_0-independent")
    pass_count += int(ok_E1); fail_count += int(not ok_E1)
    row("E2. h-blindness of rho_Lambda(z) running",
        hb_run, f"<= {GATE_HBLIND_RUN:g}", ok_E2,
        sub="no-running theorem trivially H_0-independent")
    pass_count += int(ok_E2); fail_count += int(not ok_E2)
    # transparency: Omega_Lambda DOES have ~1e-4 h-dependence via Omega_r
    h_dep_OL = V.h_dependence_OmegaLambda(0.50, 0.80)
    print(f"    [info] Omega_Lambda inherits ~{h_dep_OL:.2e} variation between h=0.50 and h=0.80 via Omega_r")
    print(f"           (standard LambdaCDM h-scaling; NOT an R(u) effect)")
    results["E_h_blindness_w"]       = hb_w
    results["E_h_blindness_running"] = hb_run
    results["E_h_dep_OmegaLambda"]   = h_dep_OL

    # ---------- F: honest phi-lock audit (rigorous) ----------
    audit = V.lambda_phi_lock_audit()
    OL_best_err = audit["Omega_Lambda_audit"]["best_frac_err"]
    OL_expr     = audit["Omega_Lambda_audit"]["best_expr"]
    OL_val      = audit["Omega_Lambda_audit"]["best_value"]
    REAL_LOCK_LINEAR = audit["real_lock_threshold_linear"]   # 5e-3 (5 sig figs)
    TRIV_FLOOR       = audit["trivial_floor_linear"]         # ~ 27%

    # F1: PASSES if NO real lock (best frac err >= real-lock threshold).
    ok_F1 = (OL_best_err >= REAL_LOCK_LINEAR)
    row("F1. honesty: Omega_Lambda is NOT a real phi-power lock",
        OL_best_err, f">= {REAL_LOCK_LINEAR:g}", ok_F1,
        sub=f"best candidate: {OL_expr} = {OL_val:.5f}, frac err {OL_best_err:.2e}  (real-lock requires < 5e-3)")
    pass_count += int(ok_F1); fail_count += int(not ok_F1)

    # F2: Lambda/M_Pl^4, both conventions
    red  = audit["phi_scan_reduced"]
    full = audit["phi_scan_full"]
    # Real lock test: linear frac err < REAL_LOCK_LINEAR
    F2_red_real_lock  = (red["linear_frac_err"]  < REAL_LOCK_LINEAR)
    F2_full_real_lock = (full["linear_frac_err"] < REAL_LOCK_LINEAR)
    real_lock_either  = F2_red_real_lock or F2_full_real_lock
    # PASSES if NO real lock under EITHER convention
    ok_F2 = (not real_lock_either)
    row("F2. honesty: Lambda/M_Pl^4 magnitude is NOT a real phi-power lock",
        max(red["linear_frac_err"], full["linear_frac_err"]),
        f">= {REAL_LOCK_LINEAR:g}", ok_F2,
        sub=f"trivial coincidence floor in linear space ~ {TRIV_FLOOR:.1%}; real lock requires << it")
    print(f"    reduced M_Pl convention:  Lambda/M_Pl^4 = {audit['Lambda_M_Pl4_reduced']:.4e}")
    print(f"      best phi^(-{red['best_N']}) = {red['phi_pow_linear']:.4e}  (linear frac err {red['linear_frac_err']:.2e}, log10 frac err {red['log10_frac_err']:.2e})")
    print(f"    non-reduced M_Pl convention: Lambda/M_Pl^4 = {audit['Lambda_M_Pl4_full']:.4e}")
    print(f"      best phi^(-{full['best_N']}) = {full['phi_pow_linear']:.4e}  (linear frac err {full['linear_frac_err']:.2e}, log10 frac err {full['log10_frac_err']:.2e})")
    pass_count += int(ok_F2); fail_count += int(not ok_F2)
    results["F_phi_lock_audit"] = audit

    # ---------- summary ----------
    print()
    print("  --- Omega-component inheritance (ESD, baseline H_0 = 67.36) ---")
    print(f"  Omega_m   (locked)    = {V.OMEGA_M_LOCK_VAL:.6f}")
    print(f"  Omega_gamma            = {V.omega_gamma():.4e}")
    print(f"  Omega_nu (relativistic) = {V.omega_nu_relativistic():.4e}")
    print(f"  Omega_r   total       = {V.omega_r():.4e}")
    print(f"  Omega_Lambda (ESD)     = {OL:.6f}")
    print(f"  Omega_Lambda (Planck)  = {OL_target:.4f}")
    print()
    print("  --- honest phi-lock scan (rigorous: linear-space 5-sig-fig test) ---")
    print(f"  trivial coincidence floor (linear, near log10 ~ -121): {audit['trivial_floor_linear']:.1%}")
    print(f"  real-lock threshold (linear frac err):                 {audit['real_lock_threshold_linear']:g}")
    print(f"  best Omega_Lambda match:        {audit['Omega_Lambda_audit']['best_expr']:20s} "
          f"= {audit['Omega_Lambda_audit']['best_value']:.5f}  (linear frac err {audit['Omega_Lambda_audit']['best_frac_err']:.2e})")
    rs = audit['phi_scan_reduced']
    print(f"  best Lambda/M_Pl^4 (reduced):   phi^(-{rs['best_N']}) "
          f"= {rs['phi_pow_linear']:.3e}  vs target {rs['target_linear']:.3e}  (linear frac err {rs['linear_frac_err']:.2e})")
    fs = audit['phi_scan_full']
    print(f"  best Lambda/M_Pl^4 (non-red.):  phi^(-{fs['best_N']}) "
          f"= {fs['phi_pow_linear']:.3e}  vs target {fs['target_linear']:.3e}  (linear frac err {fs['linear_frac_err']:.2e})")

    total = pass_count + fail_count
    print()
    if fail_count == 0:
        print(f"  ===> ALL {total} VACUUM-SECTOR CLAIMS PASS")
    else:
        print(f"  ===> {pass_count}/{total} PASS, {fail_count} FAIL")

    print()
    print("  Framework-native statements:")
    print("    * ESD inherits w = -1 exactly (no R(u) on vacuum).")
    print("    * ESD inherits Omega_Lambda from the Friedmann sum given")
    print("      locked Omega_m and observed Omega_r.")
    print("    * No time-evolution of Lambda between recombination and today.")
    print()
    print("  Honest negative result:")
    print("    * ESD does NOT solve the cosmological-constant problem.")
    print("    * Lambda/M_Pl^4 ~ 1e-122 is not predicted by closure pool.")
    print("    * Omega_Lambda value is residual, not an independent phi-lock.")
    print()
    print("  Falsifiers:")
    print("    * w_0 != -1 or w_a != 0 at >= 5sigma from DESI Y3/Y5 + Euclid Y1")
    print("      would falsify Derivation B.")
    print("    * Any detected time-variation of Lambda would falsify D.")

    # ---- write outputs ----
    out_json = os.path.join(OUTDIR, "vacuum_audit.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[vacuum] wrote outputs to {OUTDIR}")

if __name__ == "__main__":
    main()
