"""B05 figure: solar Delta_nu + Sirius B vgr bar."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_stellar as E, observations as O

FIG = os.path.join(_HERE, "..", "figures_generated"); os.makedirs(FIG, exist_ok=True)

def main() -> int:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2))
    ax1.errorbar(["meas", "ESD"],
                 [O.DELTA_NU_SUN_MEAS_UHZ, E.delta_nu_pred()],
                 yerr=[O.DELTA_NU_SUN_ERR_UHZ, 0.0], fmt="o", ms=8,
                 color="#2c6fad", capsize=5)
    ax1.set_ylabel(r"Solar $\Delta\nu$ ($\mu$Hz)")
    ax1.set_title("Solar large frequency separation")

    ax2.errorbar(["meas", "ESD"],
                 [O.SIRIUS_B_VGR_KMS, E.sirius_b_vgr_pred()],
                 yerr=[O.SIRIUS_B_VGR_ERR, 0.0], fmt="o", ms=8,
                 color="#d62728", capsize=5)
    ax2.set_ylabel(r"Sirius B $v_{\rm gr}$ (km/s)")
    ax2.set_title("White-dwarf gravitational redshift")

    fig.suptitle("B05: stellar-interior NULL test")
    fig.tight_layout()
    out = os.path.join(FIG, "fig_stellar_null.png")
    fig.savefig(out, dpi=150); fig.savefig(out.replace(".png", ".pdf")); plt.close(fig)
    print(f"[B05] wrote {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
