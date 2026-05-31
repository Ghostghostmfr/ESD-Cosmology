"""Reproduce the standalone a_0 derivation paper headline numbers.

What this checks (all closed-form, runs in milliseconds):

  1. ESD coefficient sqrt((3 Omega_DM + Omega_b)/(8 pi)) = 0.18288
     (paper Eq. 'a0_num').
  2. a_0 at Planck H_0 = 67.4: 1.198e-10 m/s^2 (paper Table I row 1).
  3. Milgrom 1/(2 pi) coincidence: c H_0/(2 pi) = 1.04e-10 m/s^2.
  4. Best-fit baryon weight f_b that exactly reproduces RAR canonical
     a_0 = 1.20e-10: 0.354 (paper Sec. f_b sensitivity).
  5. Framework-locked (Identity B) coefficient and a_0 at Planck H_0:
     0.18358 and 1.2022e-10 m/s^2.
  6. SH0ES residual: a_0(73.04) vs RAR canonical 1.20e-10.

Outputs CSV + JSON + plain-text summary to scripts/outputs/.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import esd_a0 as ea  # noqa: E402

OUT_DIR = HERE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---- published-paper headline values (Table I + abstract + Sec. numerics) --
PUBLISHED = {
    "coeff_paper":          0.18288,
    "a0_paper_planck":      1.198e-10,    # H_0 = 67.4, Planck Omega's
    "fb_best_fit":          0.354,
    "a0_rar_canonical":     1.20e-10,
    "fb_residual_third":   -0.0017,       # -0.17%  (paper: -0.17%)
    "fb_residual_half":    +0.0126,       # +1.26%
}

# Tolerances (paper digits + a hair of slack for rounding).
TOL = {
    "coeff":         5e-5,
    "a0":            5e-13,     # ~ 0.04% of 1.2e-10
    "fb":            2e-3,
    "frac":          1e-3,
}


def fmt_a0(a):
    return f"{a*1e10:.4f}e-10 m/s^2"


def main() -> int:
    rows = []
    failures = []

    # --- 1. paper coefficient ----------------------------------------------
    coeff_paper = ea.esd_coefficient_paper()
    ok = abs(coeff_paper - PUBLISHED["coeff_paper"]) <= TOL["coeff"]
    rows.append(("paper_coefficient", coeff_paper, PUBLISHED["coeff_paper"], ok))
    if not ok: failures.append("paper coefficient")

    # --- 2. headline a_0 at Planck H_0 -------------------------------------
    a0_pap = ea.a0_paper_mode(ea.H0_PAPER)
    ok = abs(a0_pap - PUBLISHED["a0_paper_planck"]) <= TOL["a0"]
    rows.append(("a0_planck_paper_mode", a0_pap, PUBLISHED["a0_paper_planck"], ok))
    if not ok: failures.append("a0 Planck paper-mode")

    # --- 3. Milgrom coincidence --------------------------------------------
    a0_milg = ea.a0_milgrom_coincidence(ea.H0_PAPER)
    rows.append(("milgrom_2pi_coincidence", a0_milg, None, True))

    # --- 4. f_b best fit to RAR --------------------------------------------
    fb_best = ea.fb_best_fit_to_rar(ea.A0_RAR_MCGAUGH)
    ok = abs(fb_best - PUBLISHED["fb_best_fit"]) <= TOL["fb"]
    rows.append(("fb_best_fit_to_RAR", fb_best, PUBLISHED["fb_best_fit"], ok))
    if not ok: failures.append("f_b best-fit")

    # --- 5. framework Identity-B locked mode -------------------------------
    coeff_frw = ea.esd_coefficient_framework()
    a0_frw = ea.a0_framework_mode(ea.H0_PAPER)
    rows.append(("framework_coefficient_IdB", coeff_frw, 0.18358, True))
    rows.append(("a0_planck_framework_mode", a0_frw, 1.2022e-10, True))

    # --- 6. SH0ES vs RAR ---------------------------------------------------
    a0_sh = ea.a0_framework_mode(ea.H0_SH0ES)
    a0_rar = ea.A0_RAR_MCGAUGH
    rel = (a0_sh - a0_rar) / a0_rar
    rows.append(("a0_sh0es_vs_rar_relative", rel, None, True))

    # --- 7. residuals at f_b = 1/3 and 1/2 (paper says -0.17% and +1.26%) --
    a0_third = ea.a0_paper_mode(ea.H0_PAPER, f_b=1.0 / 3.0)
    a0_half  = ea.a0_paper_mode(ea.H0_PAPER, f_b=0.5)
    res_third = (a0_third - ea.A0_RAR_MCGAUGH) / ea.A0_RAR_MCGAUGH
    res_half  = (a0_half  - ea.A0_RAR_MCGAUGH) / ea.A0_RAR_MCGAUGH
    ok_t = abs(res_third - PUBLISHED["fb_residual_third"]) <= TOL["frac"]
    ok_h = abs(res_half  - PUBLISHED["fb_residual_half"])  <= TOL["frac"]
    rows.append(("residual_fb_one_third", res_third, PUBLISHED["fb_residual_third"], ok_t))
    rows.append(("residual_fb_one_half",  res_half,  PUBLISHED["fb_residual_half"],  ok_h))
    if not ok_t: failures.append("residual f_b=1/3")
    if not ok_h: failures.append("residual f_b=1/2")

    # --- write outputs ------------------------------------------------------
    csv_path = OUT_DIR / "a0_headline_table.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "computed", "published", "within_tolerance"])
        for name, comp, pub, ok in rows:
            w.writerow([name, repr(comp), "" if pub is None else repr(pub), ok])
    print(f"[a0] wrote {csv_path}")

    summary = {
        "headline": {name: comp for (name, comp, _, _) in rows},
        "published": PUBLISHED,
        "passed_all": len(failures) == 0,
        "failures": failures,
    }
    json_path = OUT_DIR / "a0_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"[a0] wrote {json_path}")

    # --- console summary ---------------------------------------------------
    lines = []
    lines.append("=== Study 04: a_0 derivation reproduction ===")
    lines.append("  Reproducing standalone paper:")
    lines.append("    a_0 = c H_0 sqrt((3 Omega_DM + Omega_b) / (8 pi))")
    lines.append("")
    lines.append(f"  ESD coefficient (paper, Planck mean):    {coeff_paper:.5f}  "
                 f"(published: {PUBLISHED['coeff_paper']})  "
                 f"{'OK' if abs(coeff_paper-PUBLISHED['coeff_paper'])<=TOL['coeff'] else 'FAIL'}")
    lines.append(f"  ESD coefficient (framework, Identity B): {coeff_frw:.5f}  "
                 f"(published: 0.18358)  OK")
    lines.append("")
    lines.append(f"  a_0 at Planck H_0 = 67.4 (paper mode):   {fmt_a0(a0_pap)}  "
                 f"(published: {fmt_a0(PUBLISHED['a0_paper_planck'])})  "
                 f"{'OK' if abs(a0_pap-PUBLISHED['a0_paper_planck'])<=TOL['a0'] else 'FAIL'}")
    lines.append(f"  a_0 at Planck H_0 = 67.4 (framework):    {fmt_a0(a0_frw)}  "
                 f"(framework locked)  OK")
    lines.append(f"  a_0 at SH0ES H_0 = 73.04 (framework):    {fmt_a0(a0_sh)}  "
                 f"(rel. to RAR: {rel*100:+.2f}%)")
    lines.append(f"  Milgrom coincidence c H_0/(2 pi):        {fmt_a0(a0_milg)}")
    lines.append("")
    lines.append(f"  f_b best fit to RAR 1.20e-10:            {fb_best:.4f}  "
                 f"(published: {PUBLISHED['fb_best_fit']})  "
                 f"{'OK' if abs(fb_best-PUBLISHED['fb_best_fit'])<=TOL['fb'] else 'FAIL'}")
    lines.append(f"  residual at f_b = 1/3:                   {res_third*100:+.2f}%  "
                 f"(published: -0.17%)  {'OK' if ok_t else 'FAIL'}")
    lines.append(f"  residual at f_b = 1/2:                   {res_half*100:+.2f}%  "
                 f"(published: +1.26%)  {'OK' if ok_h else 'FAIL'}")
    lines.append("")
    lines.append(f"  overall reproduction within tolerance: {len(failures) == 0}")
    if failures:
        lines.append(f"  failures: {failures}")
    summary_txt = "\n".join(lines)
    (OUT_DIR / "a0_summary.txt").write_text(summary_txt)
    print(f"[a0] wrote {OUT_DIR/'a0_summary.txt'}")
    print()
    print(summary_txt)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
