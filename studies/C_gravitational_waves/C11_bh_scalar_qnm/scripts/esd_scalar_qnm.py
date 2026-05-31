"""ESD prediction for black-hole scalar quasi-normal modes.

The ESD D-field is the framework's scalar degree of freedom. The
question this study answers is whether the D-field excites an extra
spin-0 ringdown branch in addition to GR's tensor (spin-2) QNM
spectrum (the standard 220 mode of Study C05).

By the GW-sector applicability theorem (Study C02) the ESD tensor
sector reduces identically to GR, and in the near-horizon /
photon-sphere region u = 4 g / a0 is deep in the high-u regime where
the locked closure kernel R(u) -> 0. The D-field therefore *decouples*
from the radiative dynamics there: the remnant carries no scalar charge
and the scalar QNM amplitude vanishes,

    A_scalar^ESD = 0,   Q_scalar^ESD = 0,

with |A_scalar^ESD - 0| <= O(R(u_horizon)). No free parameter enters.
ESD inherits GR's purely tensorial, no-hair ringdown.

For completeness the module also computes the scalar (ell=0) QNM
frequency that a radiating D-field *would* produce, so the prediction
"no scalar mode at this frequency" is explicit and falsifiable.
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


def M_sec(M_Msun: float) -> float:
    """Geometrized mass GM/c^3 [s]."""
    return O.G_M3_KG_S2 * M_Msun * O.M_SUN_KG / O.C_M_S ** 3


def g_horizon(M_Msun: float) -> float:
    """Schwarzschild surface gravity kappa = c^4 / (4 G M) [m/s^2]."""
    M_kg = M_Msun * O.M_SUN_KG
    return O.C_M_S ** 4 / (4.0 * O.G_M3_KG_S2 * M_kg)


def R_at_horizon(M_Msun: float, H0: float = 67.36) -> float:
    return kernel(4.0 * g_horizon(M_Msun) / a_zero(H0))


def scalar_mode_amplitude_ESD(M_Msun: float, H0: float = 67.36) -> float:
    """ESD scalar/tensor ringdown amplitude ratio: 0 (no-hair, D-field
    decouples at the horizon)."""
    return O.SCALAR_MODE_AMPLITUDE_GR * (1.0 + R_at_horizon(M_Msun, H0))


def scalar_charge_ESD(M_Msun: float, H0: float = 67.36) -> float:
    """ESD remnant scalar charge: 0."""
    return O.SCALAR_CHARGE_GR * (1.0 + R_at_horizon(M_Msun, H0))


def scalar_amplitude_dev_bound(M_Msun: float, H0: float = 67.36) -> float:
    """Upper bound on |A_scalar^ESD - 0|, set by the fractional metric
    deviation R(u_horizon)."""
    return R_at_horizon(M_Msun, H0)


def scalar_qnm_frequency_if_radiating(M_Msun: float) -> tuple[float, float]:
    """Scalar (ell=0, n=0) QNM frequency [Hz] a radiating D-field WOULD
    produce: (f_real, 1/tau). ESD predicts NO such mode (A_scalar=0);
    this is the frequency at which a future detection would falsify the
    prediction."""
    inv_M = 1.0 / M_sec(M_Msun)          # c^3 / (G M) [1/s]
    f_re = O.M_OMEGA_SCALAR_RE * inv_M / (2.0 * math.pi)
    inv_tau = O.M_OMEGA_SCALAR_IM * inv_M
    return f_re, inv_tau
