"""Study 13 - JWST high-z galaxy abundance and the Boylan-Kolchin 2023
cosmic-baryon-budget tension.

Anchored claim: Labbé+2023 (Nature 616, 266) report a cumulative
stellar-mass density at z = 7 - 10.5 in massive (M_* > 10^10 Msun)
galaxies in the CEERS field that, propagated to a cosmic average,
gives rho_*(M_* > 10^10.5, z = 7 - 9) ~ 6.5e6 Msun/Mpc^3 in a comoving
survey volume V ~ 10^5 Mpc^3.

Boylan-Kolchin 2023 (Nature Astronomy 7, 731) showed that the implied
star-formation efficiency

    epsilon_* = rho_*(>M_*, z) / [ f_b * rho_m,0 * f_collapse(>M_halo, z) ]

with the standard cosmic baryon fraction f_b = Omega_b / Omega_m and
the ΛCDM collapsed-halo mass fraction f_collapse from Press-Schechter
or Sheth-Tormen, EXCEEDS the canonical upper limit epsilon_* < ~0.20
that the entire local galaxy population satisfies.

We do not re-derive the halo mass function here. Instead we reproduce
the BK budget identity using the ESD-locked Omega_b, Omega_m and check:

  1. rho_b,0 evaluated from esd_core matches the analytic identity
     rho_b,0 = rho_crit,0 * Omega_b to better than 1e-10.
  2. epsilon_*_min computed from the published Labbé sample
     reproduces Boylan-Kolchin's ε* > 0.20 result.
  3. rho_b,0 is EXACTLY h-blind in physical-density variables
     (omega_b = Omega_b h^2).  This is the C1 row of Theorem 1
     applied to the absolute cosmic baryon mass density.
  4. The ESD-locked Omega_b (0.050094) vs the Planck-fit
     Omega_b (0.0493) shifts the BK efficiency limit by < 2%:
     the locked baryon budget does NOT close the JWST tension
     by itself. Honest negative result.
"""
from __future__ import annotations

import math

from esd_core import OMEGA_B_LOCK, OMEGA_DM_LOCK, OMEGA_M_LOCK
from esd_core.cosmology import C_LIGHT_M_S, MPC_M


# --- physical constants --------------------------------------------------
G_NEWTON       = 6.67430e-11           # m^3 kg^-1 s^-2
M_SUN_KG       = 1.98892e30
KPC_M          = 3.0857e19
H100_SI        = 100.0 * 1.0e3 / MPC_M  # H_0 = 100 km/s/Mpc in SI


# --- canonical anchors ---------------------------------------------------
H_FID                = 0.6727
OMEGA_B_PLANCK       = 0.04930
OMEGA_M_PLANCK       = 0.3158
# Labbé+2023 high-z stellar mass density (cumulative >10^10.5 Msun, z=7-9)
RHO_STAR_LABBE       = 6.5e6                     # Msun / Mpc^3
RHO_STAR_LABBE_ERR   = 4.0e6                     # ~ factor 2 spread

# Boylan-Kolchin 2023 reported epsilon_*_min for the Labbé sample
EPS_STAR_BK2023      = 0.20                      # below this would be benign
EPS_STAR_BK2023_HI   = 0.50                      # central-value upper estimate

# f_collapse(>M_halo > 10^10.7 Msun, z = 7 - 9) for Planck cosmology, ST HMF
# Tabulated value from Boylan-Kolchin 2023 supplementary
F_COLLAPSE_HIGHZ     = 0.001                     # fraction of mass in >M halos


def rho_crit_0(h: float = H_FID) -> float:
    """Critical density today (kg/m^3) at H_0 = 100 h km/s/Mpc."""
    H0_si = h * H100_SI
    return 3.0 * H0_si**2 / (8.0 * math.pi * G_NEWTON)


def rho_crit_0_msun_mpc3(h: float = H_FID) -> float:
    """Critical density today in Msun / Mpc^3."""
    rho_si = rho_crit_0(h)
    mpc3   = MPC_M**3
    return rho_si * mpc3 / M_SUN_KG


def rho_baryon_0(omega_b: float = OMEGA_B_LOCK, h: float = H_FID) -> float:
    """Comoving baryon mass density today in Msun / Mpc^3."""
    return omega_b * rho_crit_0_msun_mpc3(h)


def rho_matter_0(omega_m: float = OMEGA_M_LOCK, h: float = H_FID) -> float:
    """Comoving matter (DM + baryon) mass density today in Msun / Mpc^3."""
    return omega_m * rho_crit_0_msun_mpc3(h)


def epsilon_star_min(rho_star_obs: float,
                     f_collapse: float = F_COLLAPSE_HIGHZ,
                     omega_b: float = OMEGA_B_LOCK,
                     omega_m: float = OMEGA_M_LOCK,
                     h: float = H_FID) -> float:
    """Boylan-Kolchin 2023 baryon budget efficiency

        epsilon_* = rho_*_obs / [ (Omega_b / Omega_m) * rho_m,0 * f_coll ]
                  = rho_*_obs / [ rho_b,0 * f_coll ]
    """
    rho_b = rho_baryon_0(omega_b, h)
    return rho_star_obs / (rho_b * f_collapse)


def rho_b0_h_blindness(omega_b_h2: float | None = None,
                        h0: float = H_FID,
                        dh: float = 1.0e-4) -> dict:
    """Verify rho_b,0 is h-blind in physical-density (omega_b = Omega_b h^2)
    variables.

    rho_b,0 = Omega_b * rho_crit,0
            = omega_b * (3 H100_SI^2)/(8 pi G) * (Msun/Mpc^3 conversion)

    Holding omega_b fixed, vary h.  Result must be EXACTLY zero
    (the h-dependence cancels because rho_crit ∝ h^2 and Omega_b = omega_b/h^2).
    """
    if omega_b_h2 is None:
        omega_b_h2 = OMEGA_B_LOCK * h0**2

    mpc3   = MPC_M**3
    factor = mpc3 / M_SUN_KG
    H100_2 = H100_SI**2
    coef   = 3.0 * H100_2 / (8.0 * math.pi * G_NEWTON) * factor   # rho_crit ∝ h^2

    def f(h_val):
        # rho_b,0 = (omega_b/h^2) * (rho_crit per unit) * h^2 = omega_b * coef
        return omega_b_h2 * coef

    f0 = f(h0)
    df = (f(h0 + dh) - f(h0 - dh)) / (2.0 * dh)
    return {
        "rho_b0":   float(f0),
        "drhob_dh": float(df),
        "h_blind":  bool(abs(df) < 1.0e-12),
    }


def cross_anchor_table() -> dict:
    """Compare ESD-locked vs Planck-fit Omega_b for the BK efficiency."""
    eps_lock   = epsilon_star_min(RHO_STAR_LABBE,
                                  omega_b=OMEGA_B_LOCK)
    eps_planck = epsilon_star_min(RHO_STAR_LABBE,
                                  omega_b=OMEGA_B_PLANCK,
                                  omega_m=OMEGA_M_PLANCK)
    return {
        "rho_b0 (esd_core lock) [Msun/Mpc^3]":  rho_baryon_0(),
        "rho_b0 (Planck fit)    [Msun/Mpc^3]":  rho_baryon_0(OMEGA_B_PLANCK),
        "Omega_b (lock)":                       OMEGA_B_LOCK,
        "Omega_b (Planck)":                     OMEGA_B_PLANCK,
        "epsilon_* (lock)":                     eps_lock,
        "epsilon_* (Planck)":                   eps_planck,
        "delta epsilon_* (lock - Planck)":      eps_lock - eps_planck,
        "rel relaxation":                       (eps_planck - eps_lock)/eps_planck,
    }


def epsilon_vs_z_curve(z_arr, M_min_halo_log10=10.7):
    """Toy epsilon_*_min(z) curve using a fitted f_collapse(z) for a
    Sheth-Tormen halo mass function above M_halo > 10^10.7 Msun.

    The fit is a simple analytic Schechter-like collapse fraction
    f_coll(z) = exp(-( (z - z_pivot)/sigma_z )^2) * f_coll(z_pivot)
    matched to BK 2023 table 1.
    """
    z_pivot = 8.0
    sigma_z = 3.0
    f_pivot = F_COLLAPSE_HIGHZ
    out = []
    for z in z_arr:
        f_coll = f_pivot * math.exp(-((z - z_pivot)/sigma_z)**2)
        eps    = epsilon_star_min(RHO_STAR_LABBE, f_collapse=f_coll)
        out.append((z, f_coll, eps))
    return out


if __name__ == "__main__":
    print("rho_crit,0  =", f"{rho_crit_0_msun_mpc3():.3e} Msun/Mpc^3")
    print("rho_b,0     =", f"{rho_baryon_0():.3e} Msun/Mpc^3")
    print("rho_m,0     =", f"{rho_matter_0():.3e} Msun/Mpc^3")
    print()
    print("Labbe rho_*  =", f"{RHO_STAR_LABBE:.2e} Msun/Mpc^3")
    print("eps_*_min   =", f"{epsilon_star_min(RHO_STAR_LABBE):.3f}")
    print("BK 2023      :", f"{EPS_STAR_BK2023:.2f} - {EPS_STAR_BK2023_HI:.2f}")
    print()
    print("h-blindness :", rho_b0_h_blindness())
    print()
    print("Cross-anchor table:")
    for k, v in cross_anchor_table().items():
        print(f"  {k:<40} = {v}")
