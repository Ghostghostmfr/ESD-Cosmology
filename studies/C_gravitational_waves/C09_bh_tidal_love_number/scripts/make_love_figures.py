"""C09 figure: BH tidal Love number / deformability null vs data + exotics."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_love as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)


def main() -> int:
    fig, ax = plt.subplots(figsize=(7.5, 4.3))

    # exotic-compact-object band (objects with k2 != 0 -> nonzero Lambda)
    ax.axvspan(50, 1000, color="#f0c0c0", alpha=0.5,
               label="exotic compact objects ($k_2\\neq0$)")

    # observational 90% CL upper bounds
    ys = list(range(len(O.TIDAL_BOUNDS)))
    for y, b in zip(ys, O.TIDAL_BOUNDS):
        ax.annotate("", xy=(2, y), xytext=(b["Lambda_upper_90CL"], y),
                    arrowprops=dict(arrowstyle="->", color="#2c6fad", lw=2))
        ax.text(b["Lambda_upper_90CL"], y + 0.06,
                f"{b['event']} 90% CL $\\leq${b['Lambda_upper_90CL']:.0f}",
                ha="right", va="bottom", fontsize=8, color="#2c6fad")

    # ESD / GR BH prediction: Lambda = 0 exactly
    ax.axvline(0.5, color="#d62728", lw=2.4,
               label="ESD = GR/Kerr: $k_2=0,\\ \\Lambda=0$")

    ax.set_xscale("log")
    ax.set_xlim(0.3, 1500)
    ax.set_ylim(-0.6, len(O.TIDAL_BOUNDS) - 0.2)
    ax.set_yticks(ys)
    ax.set_yticklabels([b["event"] for b in O.TIDAL_BOUNDS])
    ax.set_xlabel(r"tidal deformability $\Lambda$")
    ax.set_title("C09: black-hole tidal Love number (zero-parameter null)")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_love.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C09] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
