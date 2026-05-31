"""ESD BBN predictor using Pitrou+ 2018 fitting formulas.

eta_10 = 273.46 * Omega_b * h^2  (with h = H_0 / 100)

D/H pred  = D/H_anchor * (eta_10 / eta_anchor)^(d ln(D/H) / d ln eta)
Yp pred   = Yp_anchor   + Yp_slope * log10(eta_10 / eta_anchor)
"""
from __future__ import annotations

import math

from esd_core import omega_b
from esd_core.identities import Reading

import observations as O   # noqa: E402

H0_PLANCK_KMS: float = 67.36
H_DIM:         float = H0_PLANCK_KMS / 100.0

ETA10_PER_OMEGA_BH2: float = 273.46


def eta10_for_reading(reading: Reading | str = Reading.PRIMARY,
                       h: float = H_DIM) -> float:
    Ob = omega_b(reading)
    omega_bh2 = Ob * h * h
    return ETA10_PER_OMEGA_BH2 * omega_bh2


def DH_pred(eta10: float) -> float:
    return O.DH_FIT_AT_ANCHOR * (eta10 / O.ETA10_FIT_ANCHOR) ** O.DH_ETA_EXPONENT


def Yp_pred(eta10: float) -> float:
    return O.YP_FIT_AT_ANCHOR + O.YP_ETA_SLOPE * math.log10(eta10 / O.ETA10_FIT_ANCHOR)


def predictions(reading: Reading | str = Reading.PRIMARY) -> dict:
    eta = eta10_for_reading(reading)
    return {
        "reading": Reading.parse(reading).value,
        "eta10":   eta,
        "DH":      DH_pred(eta),
        "Yp":      Yp_pred(eta),
    }
