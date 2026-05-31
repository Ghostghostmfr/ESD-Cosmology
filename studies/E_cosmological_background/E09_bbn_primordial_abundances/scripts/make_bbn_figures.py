"""Study E09 figure builder."""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import esd_bbn as E       # noqa: E402
import observations as O  # noqa: E402

FIG_DIR = os.path.join(_HERE, "..", "figures_generated")
os.makedirs(FIG_DIR, exist_ok=True)


def main() -> int:
    etas = np.linspace(5.5, 6.8, 200)
    dh   = [E.DH_pred(e) for e in etas]

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(etas, [d * 1.0e5 for d in dh], "k-", lw=1.5,
            label="Pitrou+ 2018 fit")
    ax.axhspan((O.DH_OBS - O.DH_OBS_ERR) * 1.0e5,
               (O.DH_OBS + O.DH_OBS_ERR) * 1.0e5,
               color="gray", alpha=0.25, label="Cooke+ 2018 obs (1$\\sigma$)")

    pri = E.predictions("primary")
    clo = E.predictions("closure-pool")
    ax.plot(pri["eta10"], pri["DH"] * 1.0e5, "D", color="#2c6fad",
            markersize=10, label=f"PRIMARY: eta = {pri['eta10']:.3f}")
    ax.plot(clo["eta10"], clo["DH"] * 1.0e5, "s", color="#d62728",
            markersize=10, label=f"CLOSURE-POOL: eta = {clo['eta10']:.3f}")

    ax.set_xlabel(r"$\eta_{10}$")
    ax.set_ylabel(r"$D/H \times 10^5$")
    ax.set_title("Study E09: BBN D/H under both Identity B readings")
    ax.legend(fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig_bbn_DH.png")
    fig.savefig(out, dpi=150)
    fig.savefig(out.replace(".png", ".pdf"))
    plt.close(fig)
    print(f"[E09] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
