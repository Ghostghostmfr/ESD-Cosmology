"""Study 20 figures."""
from __future__ import annotations
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, _HERE)
import esd_redshift as R

FIG = os.path.normpath(os.path.join(_HERE, "..", "figures_generated"))
os.makedirs(FIG, exist_ok=True)


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name+".png"), dpi=150, bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name+".pdf"),            bbox_inches="tight")
    plt.close(fig)


def fig_mu_z():
    zs = np.linspace(0.01, 2.5, 60)
    mu_esd  = [R.mu_distance_modulus(z) for z in zs]
    mu_lcdm = [R.mu_distance_modulus(z, H0=67.36, Om=0.3158, OL=0.6842) for z in zs]
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(7.5, 6.0), sharex=True,
                                  gridspec_kw={"height_ratios":[2.5,1]})
    ax.plot(zs, mu_esd,  "C2-",  lw=2.2, label=r"ESD (locked $\Omega_m=0.3157$)")
    ax.plot(zs, mu_lcdm, "k--",  lw=1.2, alpha=0.7, label=r"$\Lambda$CDM Planck ($\Omega_m=0.3158$)")
    ax.set_ylabel(r"distance modulus $\mu(z)$ [mag]")
    ax.set_title("ESD reproduces LambdaCDM $\\mu(z)$ to <0.0001 mag everywhere")
    ax.legend(); ax.grid(alpha=0.3)
    delta = [a-b for a,b in zip(mu_esd, mu_lcdm)]
    ax2.plot(zs, [d*1000 for d in delta], "C2-", lw=1.4)
    ax2.axhline(0, color="k", lw=0.5)
    ax2.set_xlabel("redshift z")
    ax2.set_ylabel(r"$\Delta\mu$ [mmag]")
    ax2.grid(alpha=0.3)
    _save(fig, "fig_mu_z_identity")


def fig_sandage_drift():
    zs = np.linspace(0.01, 5.0, 80)
    drift = [R.sandage_drift(z)*365.25*86400*1e10 for z in zs]
    fig, ax = plt.subplots(figsize=(7, 4.0))
    ax.plot(zs, drift, "C2-", lw=2.0)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("redshift z")
    ax.set_ylabel(r"$dz/dt_{\rm obs}$ [$10^{-10}$ / yr]")
    ax.set_title("Sandage redshift drift — ESD predicts standard LambdaCDM curve")
    ax.grid(alpha=0.3)
    _save(fig, "fig_sandage_drift")


if __name__ == "__main__":
    fig_mu_z()
    fig_sandage_drift()
    print(f"[redshift] figures written to {FIG}")
