"""B04 figure."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_s2 as E, observations as O
from esd_core import a_zero

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    fsp_pred = E.f_SP_pred()
    xs = ["GR", "ESD pred", "GRAVITY+ 2020"]
    ys = [1.0, fsp_pred, O.F_SP_MEAS]
    errs = [0.0, 0.0, O.F_SP_ERR]
    ax.errorbar(xs, ys, yerr=errs, fmt="o", capsize=5, ms=8, color="#2c6fad")
    ax.axhline(1.0, ls=":", color="gray", lw=0.7)
    ax.set_ylabel("$f_{SP}$ (1 = pure GR)")
    ax.set_title("B04: Schwarzschild precession of S2 / Sgr A*")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_s2_fSP.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[B04] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
