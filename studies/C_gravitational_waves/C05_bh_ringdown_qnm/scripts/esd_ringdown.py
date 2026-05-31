"""ESD ringdown predictor: Berti-Cardoso-Will Kerr 220 fits plus
closure-pool suppression check at the photon sphere.

Reference fits (Berti, Cardoso, Will 2006 PRD 73, 064030):
    f_220 (Hz) = (1/(2 pi M_f)) * [1.5251 - 1.1568 (1-chi)^0.1292]
    Q_220     = 0.7000 + 1.4187 (1-chi)^-0.4990
    tau_220   = Q_220 / (pi f_220)
where M_f in geometrized units M -> GM/c^3 (seconds).
"""
from __future__ import annotations
import math
from esd_core import a_zero
import observations as O

PHI    = (1.0 + math.sqrt(5.0)) / 2.0
LN_PHI = math.log(PHI)
P_EXP  = PHI
Q_EXP  = 2.0 * LN_PHI / PHI
S_NRM  = 16.0 * PHI + 1.0
B_AMP  = PHI ** 6 - 2.0
C_FLR  = (4.0 * LN_PHI - 1.0) / PHI


def kernel(u: float) -> float:
    if u <= 0.0:
        return S_NRM / C_FLR
    return S_NRM / (u ** P_EXP + B_AMP * u ** Q_EXP + C_FLR)


def M_sec(Mf_Msun: float) -> float:
    return O.G_M3_KG_S2 * Mf_Msun * O.M_SUN_KG / O.C_M_S ** 3


def f220_GR(Mf_Msun: float, chi: float) -> float:
    factor = 1.5251 - 1.1568 * (1.0 - chi) ** 0.1292
    return factor / (2.0 * math.pi * M_sec(Mf_Msun))


def tau220_GR(Mf_Msun: float, chi: float) -> float:
    Q = 0.7000 + 1.4187 * (1.0 - chi) ** -0.4990
    f = f220_GR(Mf_Msun, chi)
    return Q / (math.pi * f) * 1000.0  # ms


def g_photon_sphere(Mf_Msun: float) -> float:
    r_ph = 3.0 * O.G_M3_KG_S2 * Mf_Msun * O.M_SUN_KG / O.C_M_S ** 2
    return O.G_M3_KG_S2 * Mf_Msun * O.M_SUN_KG / r_ph ** 2


def R_photon(Mf_Msun: float, H0: float = 67.36) -> float:
    return kernel(g_photon_sphere(Mf_Msun) / a_zero(H0))


def f220_ESD(Mf_Msun: float, chi: float, H0: float = 67.36,
             z: float = 0.0) -> float:
    """Detector-frame 220 frequency. z = source redshift."""
    return f220_GR(Mf_Msun, chi) * (1.0 + R_photon(Mf_Msun, H0)) / (1.0 + z)


def tau220_ESD(Mf_Msun: float, chi: float, H0: float = 67.36,
               z: float = 0.0) -> float:
    """Detector-frame 220 damping time. z = source redshift."""
    return tau220_GR(Mf_Msun, chi) * (1.0 + R_photon(Mf_Msun, H0)) * (1.0 + z)
