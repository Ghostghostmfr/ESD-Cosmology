"""C07 figure: Lambda(M) with LVC bound."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_tidal as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    Ms = np.linspace(1.1, 2.0, 40)
    Ls = [E.Lambda_GR_APR(M) for M in Ms]
    g = O.GW170817
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.axhspan(g["Lambda_tilde_lo"], g["Lambda_tilde_hi"],
               color="#bbb", alpha=0.5, label="GW170817 90% CL")
    ax.plot(Ms, Ls, "k-", lw=2, label="ESD = GR (APR-class)")
    ax.axvline(g["M_NS_Msun"], color="#d62728", ls="--", lw=1)
    ax.set_xlabel(r"$M_{\rm NS}$ ($M_\odot$)")
    ax.set_ylabel(r"$\Lambda$")
    ax.set_yscale("log"); ax.set_title("C07: NS tidal deformability")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig_lambda_M.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C07] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
