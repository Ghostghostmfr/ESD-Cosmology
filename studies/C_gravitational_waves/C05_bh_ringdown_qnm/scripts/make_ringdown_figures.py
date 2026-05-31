"""C05 figure: f220 and tau220 pred vs obs for GW150914."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_ringdown as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    g = O.GW150914
    Mf, chi, z = g["Mf_Msun"], g["chi_f"], g["redshift"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2))
    ax1.errorbar(["Isi+ 2019", "ESD pred"],
                 [g["f220_Hz"], E.f220_ESD(Mf, chi, z=z)],
                 yerr=[O.f220_symm_err(), 0.0], fmt="o", ms=8,
                 capsize=5, color="#2c6fad")
    ax1.set_ylabel(r"$f_{220}$ (Hz)")
    ax1.set_title("GW150914 220-mode frequency")
    ax2.errorbar(["Isi+ 2019", "ESD pred"],
                 [g["tau220_ms"], E.tau220_ESD(Mf, chi, z=z)],
                 yerr=[O.tau220_symm_err(), 0.0], fmt="o", ms=8,
                 capsize=5, color="#d62728")
    ax2.set_ylabel(r"$\tau_{220}$ (ms)")
    ax2.set_title("GW150914 220-mode damping time")
    fig.suptitle("C05: BH ringdown QNM consistency")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_ringdown.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C05] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
