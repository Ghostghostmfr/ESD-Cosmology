"""ESD predictions for EHT photon-ring diameters.

Strong-field regime: at the photon sphere r = 3GM/c², the Newtonian
acceleration g_N = c^4/(9 G M) is enormous, so u = 4 g_N / a_0 is huge
(~10^13 for M87*, ~10^16 for Sgr A*), making the closure-pool
correction R(u) = s/Σ(u) astronomically small.  The ESD prediction
for the photon-ring angular diameter is therefore the GR (Schwarzschild)
value to one part in ~10^20 — well below EHT precision (~few %).

The angular diameter of the photon ring (critical impact parameter
b_c = √27 GM/c²) is:

    θ_d = 2 b_c / D = 2 √27 (GM/c²) / D
"""
from __future__ import annotations
import math
from esd_core import a_zero, OMEGA_B_LOCK  # noqa: F401  (for sanity)

# physical constants
G_SI    = 6.67430e-11
C_SI    = 299792458.0
MSUN_KG = 1.98892e30
MPC_M   = 3.0856775814913673e22
KPC_M   = 3.0856775814913673e19
MUAS    = math.pi/(180.0*3600.0*1e6)   # micro-arcsecond -> radians

# closure-pool constants
PHI   = (1 + math.sqrt(5)) / 2
P_EXP = PHI
Q_EXP = 2*math.log(PHI)/PHI
C_FLR = (4*math.log(PHI) - 1)/PHI
B_AMP = PHI**6 - 2
S_NRM = 16*PHI + 1

H0_PLANCK_KMS = 67.36
A0_SI = a_zero(H0_PLANCK_KMS)   # ~1.2015e-10 m/s^2

def Sigma(u: float) -> float:
    return u**P_EXP + B_AMP*u**Q_EXP + C_FLR

def R_of_u(u: float) -> float:
    return S_NRM / Sigma(u)

def r_g(M_solar: float) -> float:
    """Gravitational radius GM/c^2 in metres."""
    return G_SI * (M_solar * MSUN_KG) / C_SI**2

def g_at_photon_sphere(M_solar: float) -> float:
    """Newtonian acceleration at r = 3 GM/c^2 (in m/s^2)."""
    r_ps = 3.0 * r_g(M_solar)
    return G_SI * (M_solar * MSUN_KG) / r_ps**2

def theta_ring_GR(M_solar: float, D_m: float) -> float:
    """Schwarzschild photon-ring angular diameter (radians)."""
    return 2.0 * math.sqrt(27.0) * r_g(M_solar) / D_m

def theta_ring_ESD(M_solar: float, D_m: float) -> tuple[float, float]:
    """ESD prediction and relative correction to GR.

    At the photon sphere, multiply effective g by (1 + R(u)).  The
    ring radius scales as ~ √(1 + R(u)) for a circular orbit-like
    estimate; here we report both the scaled angular diameter and the
    fractional correction R(u) (which is <<1 in the strong-field regime).
    """
    gN = g_at_photon_sphere(M_solar)
    u  = 4.0 * gN / A0_SI
    R  = R_of_u(u)
    th_gr = theta_ring_GR(M_solar, D_m)
    th_es = th_gr * math.sqrt(1.0 + R)
    return th_es, R

def h_blindness_theta(M_solar: float, D_m: float, h_lo=0.50, h_hi=0.80) -> float:
    """Theorem 1 (C1): θ_ring depends only on G, M, c, D — no H0.

    a_0 enters only through R(u), and R(u) ~ 1e-20 is bit-noise.  We
    return |θ(H0_lo) - θ(H0_hi)| / θ as a sanity check.
    """
    from esd_core import a_zero as _a
    A_lo = _a(100.0*h_lo); A_hi = _a(100.0*h_hi)
    gN = g_at_photon_sphere(M_solar)
    R_lo = S_NRM/Sigma(4.0*gN/A_lo)
    R_hi = S_NRM/Sigma(4.0*gN/A_hi)
    th_gr = theta_ring_GR(M_solar, D_m)
    th_lo = th_gr * math.sqrt(1.0 + R_lo)
    th_hi = th_gr * math.sqrt(1.0 + R_hi)
    return abs(th_lo - th_hi)/th_gr
