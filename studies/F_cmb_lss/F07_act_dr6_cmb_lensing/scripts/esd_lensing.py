"""
ESD prediction for the CMB-lensing structure-growth amplitude.

Per Study 19, axiom (A1) fails for *linear* cosmological perturbations
and R(u) does NOT modify the linear growth equation. Consequently,
sigma_8(z=0) on linear scales is the same as in LambdaCDM and is
inherited from Planck:

    sigma_8^{ESD} = sigma_8^{Planck} = 0.8111 +/- 0.0060

Paper 1 Identity B locks the matter density to

    Omega_m^{ESD} = 0.31574

so the CMB-lensing combination

    S_8^{CMBL} = sigma_8 * (Omega_m / 0.3)^0.25

is fully determined with no free parameters.

The ACT DR6 lensing kernel W(z) peaks near z ~ 1-2 and k ~ 0.1 h/Mpc.
Both are firmly in the linear regime where Study 19's derivation
applies; no nonlinear-template correction (which would require
Studies 18-style modeling) is invoked here.
"""
from __future__ import annotations

# Linear amplitude from Planck 2018 TT,TE,EE+lowE+lensing
# (also the input used in Study 19 esd_growth.py)
SIGMA8_PLANCK = 0.8111
SIGMA8_PLANCK_ERR = 0.0060

# Identity B (Paper 1, C2) locked value also used in Study 19.
OMEGA_M_LOCK = 0.31574


def s8_cmbl_esd() -> float:
    """ESD's locked prediction for S_8^{CMBL} = sigma_8 * (Omega_m/0.3)^0.25."""
    return SIGMA8_PLANCK * (OMEGA_M_LOCK / 0.3) ** 0.25


def s8_cmbl_esd_sigma() -> float:
    """
    Propagated 1-sigma uncertainty from Planck sigma_8 alone
    (Omega_m is locked, so it contributes no variance).
    """
    factor = (OMEGA_M_LOCK / 0.3) ** 0.25
    return SIGMA8_PLANCK_ERR * factor
