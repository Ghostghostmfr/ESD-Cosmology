"""D08 figure: APR-surrogate M-R with NICER ellipses."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_ns as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    Ms = np.linspace(1.0, 2.3, 80)
    Rs = [E.R_pred_km(m) for m in Ms]
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.plot(Rs, Ms, "k-", lw=1.5, label="ESD = GR + APR-surrogate")
    for s in O.SOURCES:
        ax.errorbar(s["R_km"], s["M"],
                    xerr=O.R_symm_err(s), yerr=s["M_err"], fmt="o",
                    ms=8, capsize=4, label=s["name"])
    ax.set_xlabel("R (km)"); ax.set_ylabel(r"M ($M_\odot$)")
    ax.set_title("D08: NICER NS mass-radius vs ESD = GR")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig_nicer_MR.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[D08] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
