"""ESD prediction for f(z)*sigma_8(z) - Study 19 theorem: ESD = LCDM linear."""
from __future__ import annotations
import math


OMEGA_M0 = 0.31574
SIGMA_8_0 = 0.8111


def Omega_m_z(z: float) -> float:
    E2 = OMEGA_M0 * (1 + z) ** 3 + (1 - OMEGA_M0)
    return OMEGA_M0 * (1 + z) ** 3 / E2


def f_growth(z: float) -> float:
    """Linder gamma parameterization, gamma = 0.55 (LCDM)."""
    return Omega_m_z(z) ** 0.55


def D_plus(z: float, n: int = 200) -> float:
    """Linear growth factor D_+(z), normalized to D_+(0) = 1.

    D_+(z) = (5/2) Omega_m H^2 integral_z^inf (1+z')/H^3 dz'.
    Compute as ratio relative to z=0 numerically."""
    def integrand(zp):
        Hp = math.sqrt(OMEGA_M0 * (1 + zp) ** 3 + (1 - OMEGA_M0))
        return (1 + zp) / Hp ** 3
    # trapezoid to large z
    z_max = 1000.0

    def H_E(zz): return math.sqrt(OMEGA_M0 * (1 + zz) ** 3 + (1 - OMEGA_M0))

    def integral(z0):
        zs = [z0 + (z_max - z0) * i / n for i in range(n + 1)]
        vals = [integrand(zz) for zz in zs]
        s = 0.0
        for i in range(n):
            s += 0.5 * (vals[i] + vals[i + 1]) * (zs[i + 1] - zs[i])
        return s

    D_z  = 2.5 * OMEGA_M0 * H_E(z) * integral(z)
    D_0  = 2.5 * OMEGA_M0 * H_E(0.0) * integral(0.0)
    return D_z / D_0


def sigma_8_z(z: float) -> float:
    return SIGMA_8_0 * D_plus(z)


def fsigma8_predicted(z: float) -> float:
    return f_growth(z) * sigma_8_z(z)
