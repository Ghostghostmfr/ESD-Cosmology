"""B06 figure: ISL alpha vs lambda bound."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_isl as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    lams = [b["lambda_um"] for b in O.BOUNDS]
    bnds = [b["alpha_95"] for b in O.BOUNDS]
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.loglog(lams, bnds, "o-", color="#888", lw=1.5, ms=7,
              label="Lab 95% upper bound on |α|")
    ax.axhline(1e-15, color="#d62728", lw=2, ls="--",
               label=r"ESD predicted $|\alpha| \approx R_{\rm lab} \sim 10^{-19}$")
    ax.set_xlabel(r"$\lambda$ (μm)")
    ax.set_ylabel(r"$|\alpha|$")
    ax.set_title("B06: inverse-square-law bounds")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig_isl_alpha.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[B06] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
