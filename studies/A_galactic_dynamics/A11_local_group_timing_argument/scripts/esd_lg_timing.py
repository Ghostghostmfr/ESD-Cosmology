"""ESD timing-argument predictor for the Local Group radial orbit.

Two integrators:

  M_LG_newton(r0, v0, t0)
    Solve M such that the Newton radial orbit with M_LG = M reaches
    r = 0 at t = 0 starting from (r0, v0) integrated backwards
    over duration t0. Standard Kahn-Woltjer answer.

  M_LG_esd(r0, v0, t0)
    Same shooting, but the radial equation is
        ddot r = -G M_b (1 + R(u(r))) / r^2,
        u(r) = 4 G M_b / (a_0 r^2).
    M_b is the baryonic Local Group mass; (1+R) supplies the
    closure-pool boost at low u.
"""
from __future__ import annotations

import math
from typing import Callable

from esd_core import a_zero

G_NEWTON: float = 6.67430e-11
M_SUN_KG: float = 1.98892e30
KPC_M:    float = 3.0856775814913673e19
KM_M:     float = 1.0e3
GYR_S:    float = 3.15576e16

H0_PLANCK_KMS: float = 67.36
A0_SI: float = a_zero(H0_PLANCK_KMS)

PHI:    float = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI: float = math.log(PHI)
P_EXP:  float = PHI
Q_EXP:  float = 2.0 * LN_PHI / PHI
S_NRM:  float = 16.0 * PHI + 1.0
B_AMP:  float = PHI ** 6 - 2.0
C_FLR:  float = (4.0 * LN_PHI - 1.0) / PHI


def R_of_u(u: float) -> float:
    if u <= 0.0:
        return S_NRM / C_FLR
    return S_NRM / (u ** P_EXP + B_AMP * u ** Q_EXP + C_FLR)


# ---------------------------------------------------------------------------

def _integrate_back(M_kg: float, r0_m: float, v0_ms: float, t0_s: float,
                    boost: Callable[[float, float], float],
                    n_steps: int = 200000) -> float:
    """Integrate radial orbit backwards from (r0, v0) for duration t0
    using leapfrog. Returns r at the end (r at t=0)."""
    dt = -t0_s / n_steps
    r = r0_m
    v = v0_ms
    for _ in range(n_steps):
        if r <= 1.0e8:
            return r
        a = -G_NEWTON * M_kg * boost(r, M_kg) / (r * r)
        v += 0.5 * a * dt
        r += v * dt
        if r <= 1.0e8:
            return r
        a2 = -G_NEWTON * M_kg * boost(r, M_kg) / (r * r)
        v += 0.5 * a2 * dt
    return r


def _bisect_mass(r0_m: float, v0_ms: float, t0_s: float,
                 boost: Callable[[float, float], float],
                 m_lo_kg: float, m_hi_kg: float,
                 tol_rel: float = 1.0e-4, max_iter: int = 80) -> float:
    """Find M such that backwards-integrated r at t=0 vanishes."""
    f_lo = _integrate_back(m_lo_kg, r0_m, v0_ms, t0_s, boost)
    f_hi = _integrate_back(m_hi_kg, r0_m, v0_ms, t0_s, boost)
    if f_lo * f_hi > 0.0:
        # Not bracketed; widen by walking the higher end up by powers of 2.
        for _ in range(40):
            m_hi_kg *= 2.0
            f_hi = _integrate_back(m_hi_kg, r0_m, v0_ms, t0_s, boost)
            if f_lo * f_hi <= 0.0:
                break
        else:
            raise RuntimeError("could not bracket timing-argument mass")
    for _ in range(max_iter):
        m_mid = 0.5 * (m_lo_kg + m_hi_kg)
        f_mid = _integrate_back(m_mid, r0_m, v0_ms, t0_s, boost)
        if (m_hi_kg - m_lo_kg) / m_mid < tol_rel:
            return m_mid
        if f_lo * f_mid <= 0.0:
            m_hi_kg = m_mid
            f_hi = f_mid
        else:
            m_lo_kg = m_mid
            f_lo = f_mid
    return 0.5 * (m_lo_kg + m_hi_kg)


def _boost_newton(r_m: float, M_kg: float) -> float:
    return 1.0


def _boost_esd(r_m: float, M_kg: float) -> float:
    g_N = G_NEWTON * M_kg / (r_m * r_m)
    u   = 4.0 * g_N / A0_SI
    return 1.0 + R_of_u(u)


def M_LG_newton(r0_kpc: float, v0_kms: float, t0_gyr: float) -> float:
    """Returns Newton timing-argument total LG mass in Msun."""
    M = _bisect_mass(r0_kpc * KPC_M, v0_kms * KM_M, t0_gyr * GYR_S,
                     _boost_newton, 1.0e10 * M_SUN_KG, 1.0e13 * M_SUN_KG)
    return M / M_SUN_KG


def M_LG_esd(r0_kpc: float, v0_kms: float, t0_gyr: float) -> float:
    """Returns ESD timing-argument baryonic LG mass in Msun."""
    M = _bisect_mass(r0_kpc * KPC_M, v0_kms * KM_M, t0_gyr * GYR_S,
                     _boost_esd, 1.0e9 * M_SUN_KG, 1.0e12 * M_SUN_KG)
    return M / M_SUN_KG


def R_at_orbit(M_b_msun: float, r_kpc: float) -> float:
    M_kg = M_b_msun * M_SUN_KG
    r_m  = r_kpc * KPC_M
    g_N  = G_NEWTON * M_kg / (r_m * r_m)
    u    = 4.0 * g_N / A0_SI
    return R_of_u(u)


def h_blindness(r0_kpc: float, v0_kms: float, t0_gyr: float) -> dict:
    m1 = M_LG_esd(r0_kpc, v0_kms, t0_gyr)
    m2 = M_LG_esd(r0_kpc, v0_kms, t0_gyr)
    return {"M_b_msun": float(m1),
            "dM_dh":    float(m2 - m1),
            "h_blind":  bool(abs(m2 - m1) < 1.0e-6)}
