"""Theory 02 figures."""
from __future__ import annotations
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import esd_vacuum as V

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)

def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)

def fig_w_of_z():
    z = np.linspace(0, 3, 200)
    w_ESD = np.full_like(z, -1.0)
    # illustrative alternatives (NOT framework predictions)
    w_w0wa_a = -0.95 + -0.4 * z/(1+z)
    w_w0wa_b = -0.73 + -1.05 * z/(1+z)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(z, w_ESD, lw=3, color="C2", label=r"ESD prediction: $w = -1$ (exact)")
    ax.plot(z, w_w0wa_a, lw=1.5, ls="--", color="C0",
            label=r"illustrative CPL ($w_0=-0.95$, $w_a=-0.4$)")
    ax.plot(z, w_w0wa_b, lw=1.5, ls=":", color="C3",
            label=r"illustrative CPL ($w_0=-0.73$, $w_a=-1.05$)")
    ax.axhline(-1, color="k", lw=0.4)
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"dark-energy equation of state $w(z)$")
    ax.set_title(r"ESD locks $w(z) = -1$ at all $z$ (no R(u) on vacuum)")
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    _save(fig, "fig_w_of_z")

def fig_omega_components():
    labels = [r"$\Omega_m$", r"$\Omega_r$", r"$\Omega_\Lambda$"]
    Om = V.OMEGA_M_LOCK_VAL
    Or = V.omega_r()
    Ol = V.omega_lambda_ESD(0.0)
    vals = [Om, Or, Ol]
    colors = ["C0", "C3", "C2"]
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.bar(labels, vals, color=colors)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.01, f"{v:.4f}", ha="center", fontsize=10)
    ax.set_ylim(0, 0.8)
    ax.set_ylabel("density fraction at $z=0$")
    ax.set_title(r"ESD: $\Omega_m$ locked, $\Omega_\Lambda$ inherited from Friedmann sum")
    ax.grid(alpha=0.3, axis="y")
    _save(fig, "fig_omega_components")

def fig_phi_lock_scan():
    Ns = np.arange(550, 620)
    phi = V.PHI
    L_red = V.lambda_over_MPl4_reduced()
    L_full = V.lambda_over_MPl4_full()
    phi_vals = phi**(-Ns.astype(float))
    log_target_red  = np.log10(L_red)
    log_target_full = np.log10(L_full)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    # left: log10 vs N
    ax1.plot(Ns, np.log10(phi_vals), "o-", lw=1, color="C0", label=r"$\log_{10}\phi^{-N}$")
    ax1.axhline(log_target_red,  color="C2", ls="--",
                label=fr"reduced $M_{{\rm Pl}}$: $\log_{{10}} \Lambda/M^4 = {log_target_red:.2f}$")
    ax1.axhline(log_target_full, color="C3", ls=":",
                label=fr"non-reduced $M_{{\rm Pl}}$: $\log_{{10}} \Lambda/M^4 = {log_target_full:.2f}$")
    ax1.set_xlabel(r"$N$")
    ax1.set_ylabel(r"$\log_{10}\phi^{-N}$")
    ax1.set_title(r"$\phi$-power grid density near $\log_{10}\sim-121$")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)
    # right: relative gap in linear space
    rel_red  = np.abs(phi_vals - L_red)/L_red
    rel_full = np.abs(phi_vals - L_full)/L_full
    ax2.semilogy(Ns, rel_red,  "o-", color="C2", label="reduced $M_{Pl}$")
    ax2.semilogy(Ns, rel_full, "s-", color="C3", label="non-reduced $M_{Pl}$")
    triv = 10.0**(np.log10(phi)/2.0) - 1.0
    ax2.axhline(triv, color="k", ls="-.", label=fr"trivial floor $\sim$ {triv:.0%}")
    ax2.axhline(5e-3, color="b", ls=":", label="real-lock threshold $5\\times10^{-3}$")
    ax2.set_xlabel(r"$N$")
    ax2.set_ylabel(r"linear frac err to target")
    ax2.set_title(r"No real $\phi$-power lock for $\Lambda/M_{Pl}^4$")
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3, which="both")
    _save(fig, "fig_phi_lock_scan")

if __name__ == "__main__":
    fig_w_of_z()
    fig_omega_components()
    fig_phi_lock_scan()
    print(f"[vacuum] figures written to {FIG}")
