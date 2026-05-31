"""C06 figure: alpha_M bound."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_friction as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    lvk = O.LVK_O3
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.axhspan(lvk["alpha_M_med"] - lvk["alpha_M_errm"],
               lvk["alpha_M_med"] + lvk["alpha_M_errp"],
               color="#bbb", alpha=0.5, label="LVK O3 90% CL")
    ax.axhline(lvk["alpha_M_med"], color="#666", lw=1, ls="--",
               label=f"LVK median = {lvk['alpha_M_med']}")
    ax.axhline(E.alpha_M_ESD(), color="#d62728", lw=2,
               label="ESD prediction = 0")
    ax.set_ylabel(r"$\alpha_M$ (running Planck-mass)")
    ax.set_xticks([])
    ax.set_title("C06: GW friction bound")
    ax.legend(loc="upper right")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_alpha_M.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C06] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
