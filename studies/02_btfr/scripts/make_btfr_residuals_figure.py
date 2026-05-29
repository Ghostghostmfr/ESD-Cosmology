"""Reproduce the BTFR comparison figure (fig:btfr) from outputs/btfr_residuals.npz.

Two-panel layout:
  Left  - BTFR scatter (log V_f vs log M_b) with observed best-fit
          (alpha) and MOND (alpha=4) reference lines.
  Right - Per-galaxy V_f^4 residuals for ESD vs MOND.
"""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from esd_btfr import G_SI, MSUN_KG  # noqa: E402

NPZ_PATH = os.path.join(_HERE, "outputs", "btfr_residuals.npz")
FIG_DIR = os.path.abspath(os.path.join(_HERE, "..", "figures_generated"))
FIG_PNG = os.path.join(FIG_DIR, "btfr_comparison.png")
FIG_PDF = os.path.join(FIG_DIR, "btfr_comparison.pdf")
GU_PNG = os.path.join(FIG_DIR, "G_u_variation.png")
GU_PDF = os.path.join(FIG_DIR, "G_u_variation.pdf")


def main() -> int:
    if not os.path.exists(NPZ_PATH):
        print(f"[fig] cache not found: {NPZ_PATH}\n"
              f"      run `python run_btfr_residuals.py` first.",
              file=sys.stderr)
        return 1
    os.makedirs(FIG_DIR, exist_ok=True)

    d = np.load(NPZ_PATH, allow_pickle=True)
    log_Mb = d["log_Mb"]
    log_Vf = d["log_Vf"]
    res_esd = d["residuals_esd"]
    res_mond = d["residuals_mond"]
    G_vals = d["G_values"]
    u_vals = d["u_values"]
    alpha_obs = float(d["alpha_obs"])
    obs_slope = float(d["obs_slope"])
    obs_intercept = float(np.polyfit(log_Mb, 4.0 * log_Vf, 1)[1])
    a0 = float(d["a_zero_SI"])
    esd_rms = float(d["esd_rms"])
    mond_rms = float(d["mond_rms"])
    esd_mean = float(d["esd_mean"])
    mond_mean = float(d["mond_mean"])

    # --- two-panel: BTFR scatter + residuals -----------------------
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.2))

    ax = axes[0]
    ax.scatter(log_Vf, log_Mb, s=14, alpha=0.65, color="#0d3b66",
               edgecolor="white", linewidth=0.5,
               label=f"SPARC Q$\\leq$2 (N={len(log_Mb)})")
    Vf_grid = np.linspace(log_Vf.min() - 0.05, log_Vf.max() + 0.05, 100)
    ax.plot(Vf_grid, (4.0 * Vf_grid - obs_intercept) / obs_slope,
            "k--", lw=1.4,
            label=rf"observed best fit: $\alpha={alpha_obs:.2f}$")
    # MOND line: log10 M_b = log10(V_f^4 / (G a_0)) - in Msun, V_f in km/s
    Mb_mond = (10**(4.0 * Vf_grid) * 1.0e12) / (G_SI * MSUN_KG * a0)
    ax.plot(Vf_grid, np.log10(Mb_mond), "r:", lw=1.4,
            label=r"MOND ($\alpha=4$)")
    ax.set_xlabel(r"$\log_{10}\, V_{\rm flat}$ [km/s]")
    ax.set_ylabel(r"$\log_{10}\, M_b$ [$M_\odot$]")
    ax.set_title("Baryonic Tully-Fisher relation")
    ax.legend(loc="upper left", fontsize=9, framealpha=0.92)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.scatter(log_Mb, res_esd, s=14, alpha=0.7, color="#0d3b66",
               edgecolor="white", linewidth=0.4,
               label=f"ESD: RMS={esd_rms:.3f} dex, "
                     f"mean={esd_mean:+.3f}")
    ax.scatter(log_Mb, res_mond, s=14, alpha=0.45, color="#d7263d",
               edgecolor="white", linewidth=0.4,
               label=f"MOND: RMS={mond_rms:.3f} dex, "
                     f"mean={mond_mean:+.3f}")
    ax.axhline(0.0, color="k", lw=1.0)
    ax.set_xlabel(r"$\log_{10}\, M_b$ [$M_\odot$]")
    ax.set_ylabel(r"$\log_{10}(V_f^4)_{\rm obs} - \log_{10}(V_f^4)_{\rm pred}$ [dex]")
    ax.set_title("BTFR residuals: ESD vs MOND")
    ax.legend(loc="lower right", fontsize=9, framealpha=0.92)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIG_PNG, dpi=180)
    fig.savefig(FIG_PDF)
    plt.close(fig)
    print(f"[fig] wrote {FIG_PNG}")
    print(f"[fig] wrote {FIG_PDF}")

    # --- G(u) consistency check -----------------------------------
    from esd_btfr import G_btfr  # noqa: E402

    fig2, ax2 = plt.subplots(figsize=(7.5, 4.6))
    u_grid = np.logspace(-3, 2, 500)
    Gu_grid = np.array([G_btfr(float(u)) for u in u_grid])
    ax2.semilogx(u_grid, Gu_grid, "-", color="#114b5f", lw=1.8,
                 label=r"$\mathcal{G}(u)$ theory")
    ax2.axhline(1.0, ls="--", color="gray", lw=1.0,
                label=r"$\mathcal{G}=1$ (MOND limit, exact $\alpha=4$)")
    ax2.scatter(u_vals, G_vals, s=18, alpha=0.7, color="#d7263d",
                edgecolor="white", linewidth=0.4,
                label=f"SPARC Q$\\leq$2 (N={len(u_vals)})")
    ax2.set_xlabel(r"$u = 4\,g_N / a_0$")
    ax2.set_ylabel(r"$\mathcal{G}(u)$")
    ax2.set_title(r"BTFR prefactor $\mathcal{G}(u) = u(1+R(u))^2/4$")
    ax2.set_ylim(0.0, max(5.0, float(G_vals.max()) * 1.25))
    ax2.legend(fontsize=10, loc="upper left")
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(GU_PNG, dpi=180)
    fig2.savefig(GU_PDF)
    plt.close(fig2)
    print(f"[fig] wrote {GU_PNG}")
    print(f"[fig] wrote {GU_PDF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
