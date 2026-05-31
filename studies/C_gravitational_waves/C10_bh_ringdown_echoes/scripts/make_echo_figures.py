"""C10 figure: ringdown-echo null -- absorbing horizon vs ECO echo train."""
from __future__ import annotations
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_echoes as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)


def main() -> int:
    M = 62.0
    tau = 4.0e-3   # ~ ringdown damping time (s), schematic
    t = np.linspace(0.0, 0.05, 4000)

    # main ringdown (damped sinusoid)
    f0 = 250.0
    main = np.exp(-t / tau) * np.cos(2 * np.pi * f0 * t)

    # ECO echo train a reflective wall WOULD produce (schematic)
    eps = 1e-30
    dt_echo = E.echo_delay_if_reflective(M, eps)
    Rwall = 0.5
    eco = main.copy()
    for n in range(1, 5):
        shift = int(n * dt_echo / (t[1] - t[0]))
        if shift < len(t):
            eco[shift:] += (Rwall ** n) * np.exp(-(t[:len(t) - shift]) / tau) \
                * np.cos(2 * np.pi * f0 * (t[:len(t) - shift]))

    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.plot(t * 1e3, eco, color="#c0c0c0", lw=1.0,
            label=f"ECO (reflective wall, $|R|={Rwall}$): echo train")
    ax.plot(t * 1e3, main, color="#d62728", lw=1.8,
            label="ESD = GR absorbing horizon: $A_{\\rm echo}=0$")
    ax.set_xlabel("time after merger [ms]")
    ax.set_ylabel("strain (schematic)")
    ax.set_title("C10: ringdown echoes (zero-parameter null)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_echoes.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C10] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
