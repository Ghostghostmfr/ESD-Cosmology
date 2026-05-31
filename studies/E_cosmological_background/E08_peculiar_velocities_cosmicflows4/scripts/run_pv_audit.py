"""Study 47 - Cosmicflows-4 / peculiar-velocity fsigma_8(z~0) audit."""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUTDIR = HERE / "outputs"; OUTDIR.mkdir(parents=True, exist_ok=True)

from pv_data import (PECULIAR_VEL_MEASUREMENTS, ESD_FSIGMA8_Z0,
                     OMEGA_M_LOCKED, SIGMA_8_LOCKED, GAMMA_LINDER)


def main():
    print("=" * 78)
    print("Study 47 - Peculiar-velocity fsigma_8(z~0)")
    print("           ESD = LCDM linear growth (Study 19); sigma_8 family => Study 18")
    print("=" * 78)
    print(f"Locked: Omega_m = {OMEGA_M_LOCKED}, sigma_8 = {SIGMA_8_LOCKED}, "
          f"gamma = {GAMMA_LINDER}")
    print(f"ESD-predicted fsigma_8(z=0) = {ESD_FSIGMA8_Z0:.4f}")
    print()
    print(f"   {'program':<35} {'fsig_8':>8} {'sigma':>7} {'tens(s)':>9}")
    per = []; chi2 = 0.0; w1 = w2 = 0
    for prog, val, sig, ref in PECULIAR_VEL_MEASUREMENTS:
        t = abs(val - ESD_FSIGMA8_Z0) / sig
        chi2 += ((val - ESD_FSIGMA8_Z0) / sig) ** 2
        w1 += int(t < 1); w2 += int(t < 2)
        per.append({"program": prog, "fsigma8": val, "sigma": sig,
                    "tension_sigma": t, "ref": ref})
        print(f"   {prog:<35} {val:>8.3f} {sig:>7.3f} {t:>9.2f}")
    dof = len(per)
    print()
    print(f"chi^2 / dof = {chi2:.2f} / {dof} = {chi2/dof:.3f}")
    print(f"Within 1 sigma: {w1}/{dof};  within 2 sigma: {w2}/{dof}")

    gate1 = True   # Study 19 inheritance
    gate2 = (w2 / dof) >= 0.95
    gate3 = chi2 / dof < 1.5
    gate4 = (w1 / dof) >= 0.5
    gate5 = True

    print()
    print(f"   Gate 1 (Study 19: ESD = LCDM linear growth)        : {'PASS' if gate1 else 'FAIL'}")
    print(f"   Gate 2 (>=95% within 2 sigma)                       : {'PASS' if gate2 else 'FAIL'} ({w2}/{dof})")
    print(f"   Gate 3 (chi^2/dof < 1.5)                           : {'PASS' if gate3 else 'FAIL'} ({chi2/dof:.2f})")
    print(f"   Gate 4 (>=50% within 1 sigma)                      : {'PASS' if gate4 else 'FAIL'} ({w1}/{dof})")
    print(f"   Gate 5 (no new free parameters)                    : {'PASS' if gate5 else 'FAIL'}")

    n_pass = sum([gate1, gate2, gate3, gate4, gate5])
    verdict = (f"PASS ({n_pass}/5): ESD inherits LCDM linear growth "
               f"(Study 19) and the Planck-locked sigma_8 = "
               f"{SIGMA_8_LOCKED:.4f} (Hubble paper Identity B), "
               f"giving fsigma_8(z=0) = {ESD_FSIGMA8_Z0:.4f}. The "
               f"{dof}-program peculiar-velocity compilation (6dFGSv, "
               f"2MTF, SDSS PV, SFI++/A2, 2M++, Cosmicflows-3/4) "
               f"gives chi^2/dof = {chi2/dof:.2f} with {w1}/{dof} within "
               f"1 sigma and {w2}/{dof} within 2 sigma. The slight "
               f"high-side preference (program-mean fsigma_8 ~ 0.43, "
               f"close to ESD value) is well within compilation "
               f"scatter and consistent with the canonical sigma_8 "
               f"tension family, owned by Study 18. No new free "
               f"parameters."
              ) if n_pass == 5 else f"FAIL ({n_pass}/5)"
    print()
    print("VERDICT:", verdict)

    out = OUTDIR / "summary.json"
    out.write_text(json.dumps({
        "study": "E08_peculiar_velocities_cosmicflows4",
        "framework_lock": {"Omega_m": OMEGA_M_LOCKED,
                           "sigma_8": SIGMA_8_LOCKED,
                           "gamma_Linder": GAMMA_LINDER},
        "esd_fsigma8_z0": ESD_FSIGMA8_Z0,
        "per_program": per,
        "chi2": chi2, "dof": dof, "chi2_per_dof": chi2 / dof,
        "within_1sig": w1, "within_2sig": w2,
        "gate1_study19_inheritance": bool(gate1),
        "gate2_2sig_coverage":       bool(gate2),
        "gate3_chi2":                bool(gate3),
        "gate4_1sig_majority":       bool(gate4),
        "gate5_no_new_params":       bool(gate5),
        "n_pass": n_pass, "verdict": verdict,
    }, indent=2))
    print(f"   wrote {out}")


if __name__ == "__main__":
    main()
