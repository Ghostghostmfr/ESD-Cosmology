"""E_G gravitational-slip statistic anchors (Study 34).

E_G(z) = Omega_m,0 / f(z)   in linear LCDM (Reyes 2010, Zhang 2007).

In ESD, Study 19's applicability theorem (A1 fails for linear modes,
since linear delta is a fluctuation of the SAME field that constitutes
the cosmological background -> no system/spectator split) implies that
R(u) does NOT modify linear cosmological perturbations. The closure
kernel only applies to bound, virialized subsystems.

Consequently, at the linear scales E_G is constructed for
(k ~ 0.01 - 0.1 h/Mpc, RSD-velocity vs CMB-lensing convergence),
ESD's predictions reduce IDENTICALLY to LCDM:

    mu(z, k) = 1   (Poisson unmodified)
    Sigma(z, k) = 1   (lensing potential unmodified)
    eta(z) = Phi/Psi = 1   (no anisotropic stress)

Therefore E_G_ESD(z) = E_G_LCDM(z) = Omega_m,0 / f(z).

Published measurements (in chronological order):
"""
from __future__ import annotations

# Locked cosmological parameters (ESD = LCDM-Planck for linear sector)
OMEGA_M0_LOCKED = 0.31574                 # ESD Identity B C2 lock
OMEGA_L0_LOCKED = 1.0 - OMEGA_M0_LOCKED
GAMMA_GROWTH    = 0.55                    # Wang & Steinhardt 1998

# ---------------- E_G measurements ----------------
# Each entry: (z_eff, E_G_obs, sigma, label, citation)
EG_MEASUREMENTS = [
    (0.32, 0.392, 0.065, "Reyes+ 2010",     "Nature 464, 256 (SDSS LRG x CFHT-WL)"),
    (0.32, 0.48,  0.10,  "Blake+ 2016a",    "MNRAS 462, 4240 (BOSS-LOWZ x RCSLenS)"),
    (0.57, 0.30,  0.07,  "Blake+ 2016b",    "MNRAS 462, 4240 (BOSS-CMASS x RCSLenS)"),
    (0.57, 0.243, 0.060, "Pullen+ 2016",    "MNRAS 460, 4098 (BOSS-CMASS x Planck-kappa)"),
    (0.32, 0.40,  0.09,  "Singh+ 2020",     "MNRAS 491, 51 (BOSS x Planck PR3 kappa)"),
    (0.32, 0.46,  0.06,  "Alam+ 2017",      "MNRAS 470, 2617 (BOSS DR12 RSD-only)"),
    (0.60, 0.48,  0.10,  "de la Torre+ 2017", "A&A 608, A44 (VIPERS PDR-2)"),
    (0.42, 0.43,  0.11,  "Amon+ 2018",      "MNRAS 479, 3422 (KiDS-450 x 2dFLenS+GAMA)"),
    (0.305,0.404, 0.080, "Jullo+ 2019",     "A&A 627, A137 (CFHTLenS x BOSS)"),
]


def E2_of_z(z: float) -> float:
    """Dimensionless Hubble parameter squared E^2(z) = H^2(z)/H0^2 for flat LCDM."""
    return OMEGA_M0_LOCKED * (1.0 + z) ** 3 + OMEGA_L0_LOCKED


def Omega_m_of_z(z: float) -> float:
    """Matter density parameter at redshift z."""
    return OMEGA_M0_LOCKED * (1.0 + z) ** 3 / E2_of_z(z)


def growth_rate_f(z: float) -> float:
    """Linear growth rate f(z) = Omega_m(z)^gamma (Wang-Steinhardt)."""
    return Omega_m_of_z(z) ** GAMMA_GROWTH


def E_G_predicted(z: float) -> float:
    """E_G(z) = Omega_m,0 / f(z) in LCDM and in ESD (Study 19 theorem)."""
    return OMEGA_M0_LOCKED / growth_rate_f(z)


def slip_eta() -> float:
    """Phi/Psi slip parameter; ESD = LCDM = 1 in linear regime."""
    return 1.0


def Sigma_lensing() -> float:
    """Lensing modification Sigma; ESD = LCDM = 1 in linear regime."""
    return 1.0


def mu_growth() -> float:
    """Effective Poisson modification mu; ESD = LCDM = 1 in linear regime."""
    return 1.0


if __name__ == "__main__":
    print(f"{'z':>6}  {'E_G_ESD':>10}  {'Omega_m(z)':>10}  {'f(z)':>8}")
    for z in (0.0, 0.32, 0.42, 0.57, 0.60, 1.0):
        print(f"{z:>6.3f}  {E_G_predicted(z):>10.4f}  {Omega_m_of_z(z):>10.4f}  {growth_rate_f(z):>8.4f}")
