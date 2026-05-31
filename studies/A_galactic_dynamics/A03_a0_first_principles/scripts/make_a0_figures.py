"""Figures for Study 04: a_0(H_0) sensitivity + f_b scan.

Generates (under figures_generated/):
  fig_a0_vs_H0           a_0 vs H_0 with Planck/SH0ES bands and McGaugh line
  fig_fb_scan            paper's Sec. 'sensitivity to f_b' (reproduces Fig. 1)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import esd_a0 as ea  # noqa: E402

FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def fig_a0_vs_H0() -> None:
    H0 = np.linspace(60.0, 78.0, 401)
    a0_paper = np.array([ea.a0_paper_mode(float(h)) for h in H0])
    a0_frw = np.array([ea.a0_framework_mode(float(h)) for h in H0])
    a0_milg = np.array([ea.a0_milgrom_coincidence(float(h)) for h in H0])

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(H0, a0_paper * 1e10, color="C0", lw=2.0,
            label=r"ESD paper mode: $a_0 = cH_0\sqrt{(3\Omega_{DM}+\Omega_b)/(8\pi)}$")
    ax.plot(H0, a0_frw * 1e10, color="C2", lw=2.0, ls="--",
            label=r"ESD framework (Identity B locked)")
    ax.plot(H0, a0_milg * 1e10, color="0.5", lw=1.4, ls=":",
            label=r"Milgrom coincidence $cH_0/(2\pi)$")

    # canonical RAR band
    rar_lo = (ea.A0_RAR_MCGAUGH - ea.A0_RAR_MCGAUGH_ERR) * 1e10
    rar_hi = (ea.A0_RAR_MCGAUGH + ea.A0_RAR_MCGAUGH_ERR) * 1e10
    ax.axhspan(rar_lo, rar_hi, color="C3", alpha=0.15,
               label=r"McGaugh+2016 RAR: $a_0 = (1.20\pm0.026)\times10^{-10}$")
    ax.axhline(ea.A0_RAR_MCGAUGH * 1e10, color="C3", lw=1.0, ls="-")

    # H0 anchors
    ax.axvline(ea.H0_PLANCK, color="C0", lw=0.8, alpha=0.7)
    ax.text(ea.H0_PLANCK, 1.35, "Planck 2018", rotation=90,
            va="top", ha="right", color="C0", fontsize=8)
    ax.axvline(ea.H0_SH0ES, color="C4", lw=0.8, alpha=0.7)
    ax.text(ea.H0_SH0ES, 1.35, "SH0ES (Riess+22)", rotation=90,
            va="top", ha="right", color="C4", fontsize=8)

    ax.set_xlabel(r"$H_0$  (km s$^{-1}$ Mpc$^{-1}$)")
    ax.set_ylabel(r"$a_0$  ($10^{-10}$ m s$^{-2}$)")
    ax.set_title(r"Study 04: ESD-derived $a_0(H_0)$ vs the empirical MOND constant")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = FIG_DIR / f"fig_a0_vs_H0.{ext}"
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


def fig_fb_scan() -> None:
    fb, a0 = ea.fb_sensitivity_scan(n=401)
    fb_best = ea.fb_best_fit_to_rar(ea.A0_RAR_MCGAUGH)
    a0_best = ea.a0_paper_mode(ea.H0_PAPER, f_b=fb_best)

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.plot(fb, a0 * 1e10, color="C0", lw=2.0,
            label=r"$a_0(f_b) = cH_0\sqrt{3(\Omega_{DM}+f_b\Omega_b)/(8\pi)}$")
    ax.axhline(ea.A0_RAR_MCGAUGH * 1e10, color="C3", ls="--", lw=1.2,
               label=r"McGaugh+2016 RAR canonical")
    ax.axvline(1.0 / 3.0, color="purple", ls="-.", lw=1.0,
               label=r"$f_b=1/3$ (3D isotropy prediction)")
    ax.axvline(fb_best, color="green", ls=":", lw=1.2,
               label=f"$f_b={fb_best:.3f}$ (best fit to RAR)")
    ax.axvline(0.5, color="orange", ls=":", lw=1.0, label=r"$f_b=1/2$")
    ax.plot([fb_best], [a0_best * 1e10], "o", color="green", ms=5)

    ax.set_xlabel(r"baryon weight $f_b$")
    ax.set_ylabel(r"$a_0$  ($10^{-10}$ m s$^{-2}$)")
    ax.set_title(r"Study 04: sensitivity of $a_0$ to baryon weight $f_b$"
                 r" (reproduces Fig. 1)")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = FIG_DIR / f"fig_fb_scan.{ext}"
        fig.savefig(p, dpi=150)
        print(f"[fig] wrote {p}")
    plt.close(fig)


if __name__ == "__main__":
    fig_a0_vs_H0()
    fig_fb_scan()
