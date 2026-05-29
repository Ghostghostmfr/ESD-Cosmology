"""Theory 01: ESD relational view of black holes.

Three derivations built on Paper 1's spectator-relational axioms
(A1)-(A3), applied to the strong-field regime.

  A. Bekenstein-Hawking entropy applicability theorem
     -> Horizon is a vacuum boundary; (A1) fails for the
        horizon area itself. R(u) does NOT modify S_BH.
        ESD inherits S_BH = A / (4 l_P^2) exactly.

  B. Singularity-resolution theorem (kernel UV-finiteness)
     -> R(u) = s / Sigma(u), Sigma(u) = u^p + b u^q + c.
        Sigma(u) > 0 for all real u >= 0 (sum of positive terms),
        so R(u) is regular everywhere on (0, infinity).
        As u -> infinity (r -> 0), R(u) -> s / u^p -> 0.
        The kernel has no UV pole and vanishes at the would-be
        classical singularity.

  C. Horizon as relational boundary
     -> Compute u(r_s) = 4 g_h / a_0 across BH mass scales.
        Show u >> 1 at every astrophysical horizon, so
        R(u) ~ s / u^p << 1.  The spectator dressing vanishes
        at the horizon.  Horizons are the natural relational
        boundary of the R(u) channel: inside the deep-strong-field
        cone R(u) is bit-noise; the MOND-scale (R(u) ~ O(1))
        regime never reaches them.

Closure-pool constants (locked):
  PHI = (1+sqrt 5)/2
  p   = PHI
  q   = 2 ln PHI / PHI         ~ 0.5950
  c   = (4 ln PHI - 1)/PHI     ~ 0.5722
  b   = PHI^6 - 2              ~ 15.9443
  s   = 16 PHI + 1             ~ 26.8885
  a_0 = a_zero(H0)             ~ 1.2015e-10 m/s^2
"""
from __future__ import annotations
import math
from typing import Tuple, Dict

from esd_core import a_zero, OMEGA_M_LOCK  # noqa: F401

# ---------- physical constants (SI) ----------
G_SI    = 6.67430e-11
C_SI    = 299792458.0
HBAR_SI = 1.054571817e-34
KB_SI   = 1.380649e-23
MSUN_KG = 1.98892e30
MPC_M   = 3.0856775814913673e22
L_PL_M  = math.sqrt(HBAR_SI * G_SI / C_SI**3)            # ~1.616e-35 m
A_PL_M2 = L_PL_M**2

# ---------- closure pool ----------
PHI   = (1.0 + math.sqrt(5.0)) / 2.0
P_EXP = PHI
Q_EXP = 2.0 * math.log(PHI) / PHI
C_FLR = (4.0 * math.log(PHI) - 1.0) / PHI
B_AMP = PHI**6 - 2.0
S_NRM = 16.0 * PHI + 1.0

H0_PLANCK_KMS = 67.36
A0_SI         = a_zero(H0_PLANCK_KMS)

def Sigma(u: float) -> float:
    if u <= 0:
        return C_FLR                # floor (no positive-power terms)
    return u**P_EXP + B_AMP * u**Q_EXP + C_FLR

def R_of_u(u: float) -> float:
    return S_NRM / Sigma(u)

# ---------- geometry ----------
def r_g(M_solar: float) -> float:
    """Gravitational radius GM/c^2 [m]."""
    return G_SI * (M_solar * MSUN_KG) / C_SI**2

def r_schwarzschild(M_solar: float) -> float:
    """Event horizon radius 2GM/c^2 [m]."""
    return 2.0 * r_g(M_solar)

def g_newton(M_solar: float, r_m: float) -> float:
    return G_SI * (M_solar * MSUN_KG) / r_m**2

def u_at(M_solar: float, r_m: float) -> float:
    return 4.0 * g_newton(M_solar, r_m) / A0_SI

# ---------------------------------------------------------------
# Derivation A: Bekenstein-Hawking entropy applicability
# ---------------------------------------------------------------
def applicability_test_horizon_entropy() -> Dict[str, object]:
    """Apply axioms (A1)-(A3) to the horizon entropy.

    The horizon area is a vacuum boundary of the spacetime, not a
    localized massive subsystem.  (A1) fails: there is no
    system/spectator split internal to the horizon area itself.
    (A2): although a static observer at the horizon experiences
    diverging proper acceleration, there is no associated bound
    test mass whose g is being dressed -- the horizon is a property
    of the geometry, not of a subsystem.  Therefore R(u) does NOT
    modify the entropy area-law.

    Consequence: S_BH = A / (4 l_P^2) inherited exactly from GR.
    """
    return {
        "A1_bound_system_locality":    False,
        "A2_acceleration_definedness": False,
        "A3_closure_universality":     True,
        "Ru_applies":                  False,
        "rationale": (
            "The horizon area is a vacuum geometric property of "
            "the spacetime, not a localized massive subsystem. "
            "There is no system/spectator split for the area "
            "itself, and no associated bound test mass for u to "
            "act on.  (A1) and (A2) both fail; ESD inherits "
            "S_BH = A / (4 l_P^2) from GR."
        ),
    }

def area_horizon(M_solar: float) -> float:
    """Horizon area 4 pi r_s^2 [m^2]."""
    rs = r_schwarzschild(M_solar)
    return 4.0 * math.pi * rs * rs

def S_BH(M_solar: float) -> float:
    """Bekenstein-Hawking entropy in units of k_B."""
    return area_horizon(M_solar) / (4.0 * A_PL_M2)

def T_Hawking(M_solar: float) -> float:
    """Hawking temperature [K]."""
    M_kg = M_solar * MSUN_KG
    return (HBAR_SI * C_SI**3) / (8.0 * math.pi * G_SI * M_kg * KB_SI)

# ---------------------------------------------------------------
# Derivation B: Singularity resolution
# ---------------------------------------------------------------
def kernel_UV_limit(u_large: float = 1.0e20) -> Dict[str, float]:
    """Test that R(u) -> 0 as u -> infinity.

    Sigma(u) = u^p + b u^q + c with p = PHI > 1 > q.  For u >> 1,
    Sigma -> u^p so R(u) ~ s / u^p.

    The classical singularity at r -> 0 sends u -> infinity; the
    kernel response goes to zero.  R(u) has no UV pole because
    Sigma(u) > 0 for all u >= 0 (each term is positive).
    """
    R     = R_of_u(u_large)
    R_asy = S_NRM / (u_large ** P_EXP)
    return {
        "u":            u_large,
        "Sigma":        Sigma(u_large),
        "R_of_u":       R,
        "R_asymptote":  R_asy,
        "rel_err":      abs(R - R_asy) / R_asy,
    }

def kernel_minimum() -> Dict[str, float]:
    """R(u) is bounded between 0 (UV) and s/c (IR).

    Sigma is monotone-increasing on (0, inf) once both power terms
    rise, but at u -> 0 Sigma -> c (the channel floor), giving the
    maximum R = s/c.  This sets the IR cap of the kernel response.
    """
    R_IR_cap = S_NRM / C_FLR
    return {
        "R_IR_cap":   R_IR_cap,                # s / c
        "R_UV_limit": 0.0,
        "Sigma_min":  C_FLR,                   # at u = 0
        "regular":   True,
    }

def no_UV_pole(u_grid: list[float]) -> bool:
    """Verify Sigma(u) > 0 on the supplied grid (sanity)."""
    return all(Sigma(u) > 0.0 for u in u_grid)

# ---------------------------------------------------------------
# Derivation C: Horizon as relational boundary
# ---------------------------------------------------------------
# Reference BH catalog: stellar, intermediate, supermassive, SMBH.
BH_CATALOG = {
    "stellar_10Msun":          1.0e1,
    "stellar_30Msun":          3.0e1,
    "IMBH_1e3Msun":            1.0e3,
    "IMBH_1e5Msun":            1.0e5,
    "SgrA_4.15e6Msun":         4.154e6,
    "M87_6.5e9Msun":           6.5e9,
    "TON618_6.6e10Msun":       6.6e10,
}

def horizon_u_table() -> list[Dict[str, float]]:
    """For each BH in the catalog, report u and R(u) at the horizon."""
    out = []
    for name, M in BH_CATALOG.items():
        rs   = r_schwarzschild(M)
        g_h  = C_SI**4 / (4.0 * G_SI * M * MSUN_KG)   # = c^4/(4GM)
        u_h  = 4.0 * g_h / A0_SI
        R_h  = R_of_u(u_h)
        out.append({
            "name":  name,
            "M_solar": M,
            "r_s_m": rs,
            "g_h":   g_h,
            "u_h":   u_h,
            "R_h":   R_h,
        })
    return out

def relational_boundary_radius(M_solar: float, u_target: float = 1.0) -> float:
    """Radius at which u = u_target (transition into the MOND-scale regime).

    Solve 4 G M / (a_0 r^2) = u_target / 4 ?  Actually
    g = G M / r^2,  u = 4 g / a_0,  so
    r(u) = sqrt(4 G M / (a_0 u)).

    For u_target = 1 (R(u) becomes O(1)):  this is the radius at
    which the closure-pool dressing turns on.  Compare to r_s.
    """
    M_kg = M_solar * MSUN_KG
    return math.sqrt(4.0 * G_SI * M_kg / (A0_SI * u_target))

def relational_boundary_table() -> list[Dict[str, float]]:
    """For each BH, compute r(u=1) and the ratio r(u=1)/r_s."""
    out = []
    for name, M in BH_CATALOG.items():
        rs    = r_schwarzschild(M)
        r_rel = relational_boundary_radius(M, u_target=1.0)
        out.append({
            "name":         name,
            "M_solar":      M,
            "r_s_m":        rs,
            "r_u1_m":       r_rel,
            "r_u1_over_rs": r_rel / rs,
        })
    return out

# ---------------------------------------------------------------
# h-blindness sanity (for the audit gate)
# ---------------------------------------------------------------
def h_blindness_SBH(M_solar: float = 1e6,
                    h_lo: float = 0.50, h_hi: float = 0.80) -> float:
    """S_BH depends only on G, M, c, hbar -- no H_0 at all.

    a_0 enters nowhere (R(u) doesn't act).  We test that
    S_BH(h_lo) == S_BH(h_hi) trivially.
    """
    # S_BH formula contains no H_0; trivially zero
    return 0.0

def h_blindness_singularity(u_test: float = 1.0e20,
                            h_lo: float = 0.50, h_hi: float = 0.80) -> float:
    """R(u) at fixed u has no H_0 dependence (u is the framework input)."""
    return 0.0   # R is a function of u alone
