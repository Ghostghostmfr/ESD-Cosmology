"""C08 figure: chi distribution vs Thorne bound."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_spin as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    names = [o["object"] for o in O.OBSERVATIONS]
    chis  = [o["chi"]    for o in O.OBSERVATIONS]
    errs  = [o["chi_err"] for o in O.OBSERVATIONS]
    ys = list(range(len(names)))
    ax.errorbar(chis, ys, xerr=errs, fmt="o", color="#2c6fad",
                ms=8, capsize=4)
    ax.axvline(E.chi_max_pred(), color="#d62728", lw=2, ls="--",
               label=r"ESD = Kerr Thorne bound $\chi=0.998$")
    ax.set_yticks(ys); ax.set_yticklabels(names)
    ax.set_xlabel(r"$\chi$")
    ax.set_title("C08: BH spin distribution")
    ax.set_xlim(0.5, 1.05); ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig_chi_dist.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C08] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
