"""Rebuild the BTFR figure from `outputs/btfr_results.npz`."""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
NPZ_PATH = os.path.join(_HERE, "outputs", "btfr_results.npz")
FIG_DIR = os.path.abspath(os.path.join(_HERE, "..", "figures_generated"))
FIG_PNG = os.path.join(FIG_DIR, "btfr_low_acc_slope.png")
FIG_PDF = os.path.join(FIG_DIR, "btfr_low_acc_slope.pdf")


def main() -> int:
    if not os.path.exists(NPZ_PATH):
        print(
            f"[fig] cache not found: {NPZ_PATH}\n"
            f"      run `python run_btfr_test.py` first.",
            file=sys.stderr,
        )
        return 1
    os.makedirs(FIG_DIR, exist_ok=True)

    d = np.load(NPZ_PATH, allow_pickle=True)
    logM = d["logM"]
    logV = d["logV"]
    slope = float(d["slope"])
    intercept = float(d["intercept"])
    se = float(d["stderr"])
    R2 = float(d["R2"])
    pred = float(d["predicted_slope"])
    N = int(d["N_kept"])
    verdict = str(d["verdict"])
    n_sigma = float(d["n_sigma"])

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.scatter(logM, logV, s=22, c="#0d3b66", alpha=0.78,
               edgecolor="white", linewidth=0.6, label=f"SPARC deep regime (N={N})")

    xs = np.linspace(logM.min() - 0.1, logM.max() + 0.1, 100)
    # ESD locked prediction: slope = 0.25, intercept matched at the
    # sample mean so the comparison is purely about slope.
    intercept_pred = float(logV.mean()) - pred * float(logM.mean())
    ax.plot(xs, intercept + slope * xs, "-", color="#ee964b", lw=2.0,
            label=f"OLS fit: slope = {slope:.3f} +/- {se:.3f}")
    ax.plot(xs, intercept_pred + pred * xs, "--", color="#114b5f", lw=1.6,
            label=f"ESD locked: slope = {pred:.3f}")

    ax.set_xlabel(r"$\log_{10}\, M_b \;[\mathrm{M_\odot}]$")
    ax.set_ylabel(r"$\log_{10}\, V_f \;[\mathrm{km/s}]$")
    ax.set_title(
        f"BTFR deep low-acceleration regime ($g<0.5\\,a_0$)\n"
        f"$R^2={R2:.3f}$    tension = {n_sigma:.2f}$\\sigma$    {verdict}"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.92)

    fig.tight_layout()
    fig.savefig(FIG_PNG, dpi=200)
    fig.savefig(FIG_PDF)
    plt.close(fig)
    print(f"[fig] wrote {FIG_PNG}")
    print(f"[fig] wrote {FIG_PDF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
