"""A12 figure: BTFR with the three sources."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_hi_rotation as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    Mb = np.logspace(6.5, 9.5, 80)
    Vp = [E.V_flat_pred(m) for m in Mb]
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.loglog(Mb, Vp, "k-", lw=1.5, label="ESD deep-MOND closure")
    for s in O.SOURCES:
        marker = "s" if "AGC" in s["name"] else "o"
        ax.errorbar(s["M_b_Msun"], s["V_flat_kms"],
                    xerr=s["M_b_err"], yerr=s["V_err"],
                    fmt=marker, ms=8, capsize=4, label=s["name"])
    ax.set_xlabel(r"$M_b$ ($M_\odot$)")
    ax.set_ylabel(r"$V_{\rm flat}$ (km/s)")
    ax.set_title("A12: BTFR (HI-dominated dwarfs)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_hi_btfr.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[A12] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
