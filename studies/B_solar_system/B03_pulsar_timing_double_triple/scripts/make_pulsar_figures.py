"""Study B03 figure: R(u) suppression curve with pulsar markers."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_pulsar as E, observations as O
from esd_pulsar import kernel
from esd_core import a_zero

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    a0 = a_zero(67.36)
    us = np.logspace(-3, 14, 400)
    Rs = [kernel(u) for u in us]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.loglog(us, Rs, "k-", lw=1.5, label="closure-pool R(u)")
    for label, g in [("J0737 orbital", O.G_ORBITAL_PSR),
                     ("NS surface",    O.G_NS_SURFACE)]:
        u = g / a0
        ax.axvline(u, ls="--", lw=0.8, color="C3", alpha=0.6)
        ax.text(u, 1e-12, f" {label}", rotation=90, color="C3", fontsize=8, va="bottom")
    ax.axhline(1e-6, ls=":", color="gray", lw=0.7)
    ax.set_xlabel("u = g / a0"); ax.set_ylabel("R(u)")
    ax.set_title("B03: closure-pool kernel suppression at pulsar scales")
    ax.legend(loc="lower left")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_pulsar_Ru.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[B03] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
