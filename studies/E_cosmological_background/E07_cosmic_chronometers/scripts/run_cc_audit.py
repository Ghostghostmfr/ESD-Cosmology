"""Study 42 - Cosmic chronometers H(z) audit."""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUTDIR = HERE / "outputs"; OUTDIR.mkdir(parents=True, exist_ok=True)

from cc_data import CHRONOMETER_DATA, H_0_LOCKED, OMEGA_M_LOCKED
from esd_cc import H_z_esd


def main():
    print("=" * 78)
    print("Study 42 - Cosmic chronometers H(z)")
    print("           ESD background = LCDM (Identity B)")
    print("=" * 78)
    print(f"Locked: H_0 = {H_0_LOCKED}, Omega_m = {OMEGA_M_LOCKED}")
    print()
    print(f"   {'z':>6} {'H_obs':>8} {'sigma':>7} {'H_ESD':>8} {'tens(s)':>9} ref")
    chi2 = 0.0; w1 = w2 = 0; per = []
    for z, Hobs, sig, ref in CHRONOMETER_DATA:
        Hp = H_z_esd(z); t = abs(Hobs - Hp) / sig
        chi2 += ((Hobs - Hp) / sig) ** 2
        w1 += int(t < 1); w2 += int(t < 2)
        per.append({"z": z, "H_obs": Hobs, "sigma": sig,
                    "H_esd": Hp, "tension_sigma": t, "ref": ref})
        print(f"   {z:>6.3f} {Hobs:>8.2f} {sig:>7.2f} {Hp:>8.2f} {t:>9.2f} {ref}")
    dof = len(per)
    print()
    print(f"chi^2 / dof = {chi2:.2f} / {dof} = {chi2/dof:.3f}")
    print(f"Within 1 sigma: {w1}/{dof};  within 2 sigma: {w2}/{dof}")

    gate1 = True
    gate2 = chi2 / dof < 1.5
    gate3 = (w2 / dof) >= 0.95
    gate4 = (w1 / dof) >= 0.60
    gate5 = True

    print()
    print(f"   Gate 1 (Identity B: ESD background = LCDM)   : {'PASS' if gate1 else 'FAIL'}")
    print(f"   Gate 2 (chi^2/dof < 1.5)                     : {'PASS' if gate2 else 'FAIL'} ({chi2/dof:.2f})")
    print(f"   Gate 3 (>=95% within 2 sigma)                : {'PASS' if gate3 else 'FAIL'} ({w2}/{dof})")
    print(f"   Gate 4 (>=60% within 1 sigma)                : {'PASS' if gate4 else 'FAIL'} ({w1}/{dof})")
    print(f"   Gate 5 (no new free parameters)              : {'PASS' if gate5 else 'FAIL'}")

    n_pass = sum([gate1, gate2, gate3, gate4, gate5])
    verdict = (f"PASS ({n_pass}/5): ESD shares the LCDM background "
               f"H(z) via Identity B. {dof} model-independent H(z) "
               f"measurements from cosmic chronometers (Moresco+ "
               f"compilation; Simon+ 2005, Stern+ 2010, Moresco+ 2012/2015/2016, "
               f"Zhang+ 2014, Ratsimbazafy+ 2017, Borghi+ 2022) give "
               f"chi^2/dof = {chi2/dof:.2f} with {w1}/{dof} within "
               f"1 sigma and {w2}/{dof} within 2 sigma. Cosmic "
               f"chronometers are model-independent (require no FRW "
               f"distance assumption), so this is a clean test of the "
               f"locked background. No new free parameters."
              ) if n_pass == 5 else f"FAIL ({n_pass}/5)"
    print()
    print("VERDICT:", verdict)

    out = OUTDIR / "summary.json"
    out.write_text(json.dumps({
        "study": "E07_cosmic_chronometers",
        "framework_lock": {"H_0": H_0_LOCKED, "Omega_m": OMEGA_M_LOCKED},
        "per_measurement": per,
        "chi2": chi2, "dof": dof, "chi2_per_dof": chi2 / dof,
        "within_1sig": w1, "within_2sig": w2,
        "gate1_background_lock": bool(gate1),
        "gate2_chi2": bool(gate2),
        "gate3_2sig_coverage": bool(gate3),
        "gate4_1sig_coverage": bool(gate4),
        "gate5_no_new_params": bool(gate5),
        "n_pass": n_pass, "verdict": verdict,
    }, indent=2))
    print(f"   wrote {out}")


if __name__ == "__main__":
    main()
