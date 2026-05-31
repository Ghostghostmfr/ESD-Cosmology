"""C11 figure: scalar-QNM null -- tensor 220 mode present, scalar ell=0 absent."""
from __future__ import annotations
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_scalar_qnm as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)


def _lorentzian(f, f0, gamma, amp):
    return amp * (gamma ** 2) / ((f - f0) ** 2 + gamma ** 2)


def main() -> int:
    M = 62.0
    # tensor 220 mode (GR/ESD): M*omega_220 ~ 0.3737 - 0.0890 i
    inv_M = 1.0 / E.M_sec(M)
    f_220 = 0.37367 * inv_M / (2 * np.pi)
    g_220 = 0.08896 * inv_M / (2 * np.pi)
    # scalar ell=0 mode that a radiating D-field WOULD produce
    f_sc, inv_tau = E.scalar_qnm_frequency_if_radiating(M)
    g_sc = inv_tau / (2 * np.pi)

    f = np.linspace(0.0, 1.2 * f_220, 4000)
    tensor = _lorentzian(f, f_220, g_220, 1.0)
    scalar_eco = _lorentzian(f, f_sc, g_sc, 0.5)  # alt theory amplitude

    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.plot(f, scalar_eco + tensor, color="#c0c0c0", lw=1.0,
            label="scalar-tensor (extra spin-0 branch)")
    ax.plot(f, tensor, color="#d62728", lw=1.8,
            label="ESD = GR: tensor 220 only, $A_{\\rm scalar}=0$")
    ax.axvline(f_sc, color="#1f77b4", ls="--", lw=1.0,
               label=f"would-be scalar $\\ell{{=}}0$ ({f_sc:.0f} Hz)")
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("ringdown power (schematic)")
    ax.set_title("C11: scalar quasi-normal modes (zero-parameter null)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_scalar_qnm.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[C11] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
