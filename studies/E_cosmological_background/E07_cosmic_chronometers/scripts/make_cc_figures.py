"""Figures for Study 42 - cosmic-chronometer H(z) compilation."""
from __future__ import annotations
from pathlib import Path
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cc_data import CHRONOMETER_DATA, H_z_LCDM

FIG_DIR = HERE.parent / "figures_generated"; FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    z   = np.array([r[0] for r in CHRONOMETER_DATA])
    H   = np.array([r[1] for r in CHRONOMETER_DATA])
    sig = np.array([r[2] for r in CHRONOMETER_DATA])
    zg  = np.linspace(0, 2.1, 400)
    Hg  = np.array([H_z_LCDM(zz) for zz in zg])
    ax.plot(zg, Hg, color="black", lw=2,
            label=r"ESD = $\Lambda$CDM (Identity B)")
    ax.errorbar(z, H, yerr=sig, fmt="o", capsize=3, ms=5,
                color="C0", label="Cosmic-chronometer compilation")
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"$H(z)$  (km/s/Mpc)")
    ax.set_title("Study 42 — Cosmic chronometers vs ESD background")
    ax.set_xlim(0, 2.1); ax.set_ylim(40, 280)
    ax.legend(loc="upper left"); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    out = FIG_DIR / "cc_Hz.png"; plt.savefig(out, dpi=150); plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
