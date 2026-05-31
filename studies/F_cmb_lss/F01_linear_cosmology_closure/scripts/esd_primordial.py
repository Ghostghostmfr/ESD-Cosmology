"""ESD F_12 cascade modulation of the primordial power spectrum.

  delta_cascade(k) = -(1/N_e_star) * sin^2( pi * ln(k/k_end) / ln(phi) )

Applied post-hoc as a multiplicative factor on P_m(k):

  P_m^ESD(k) = (1 + delta_cascade(k)) * P_m^LCDM(k)

This is exact under the linear transfer assumption: the cascade enters
P_R(k) and propagates through the unchanged transfer function T(k).

k_end is the comoving wavenumber that exited the horizon at the END of
inflation (not the pivot). Mapping: k_end = a_end * H_end. At zero ESD
knobs (knob_amplitude=0) the modulation vanishes and LCDM is recovered
exactly.
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

_HERE = Path(__file__).resolve().parent

import esd_core as ESD

PHI = ESD.PHI
LN_PHI = ESD.LN_PHI
N_E_STAR = ESD.N_E_STAR  # 51.4745 (LOCK)


def k_end_mpc_inverse() -> float:
    """Comoving k that exited horizon at end of inflation, in 1/Mpc.

    Using k_pivot = 0.05 1/Mpc as the anchor at N_e^* e-folds before end:
        k_end / k_pivot = exp(N_e_star)
    """
    return 0.05 * np.exp(N_E_STAR)


def cascade_modulation(
    k: np.ndarray,
    knob_amplitude: float = 1.0,
    k_end: float | None = None,
) -> np.ndarray:
    """Return delta_cascade(k) as a 1-D array.

    knob_amplitude=0 -> identically zero (LCDM recovery gate).
    knob_amplitude=1 -> full ESD prediction.
    """
    if knob_amplitude == 0.0:
        return np.zeros_like(np.asarray(k, dtype=float))
    if k_end is None:
        k_end = k_end_mpc_inverse()
    k = np.asarray(k, dtype=float)
    # Guard against log of zero / negative
    safe_k = np.where(k > 0, k, 1e-30)
    phase = np.pi * np.log(safe_k / k_end) / LN_PHI
    return -knob_amplitude * (1.0 / N_E_STAR) * np.sin(phase) ** 2


def apply_cascade(
    pk: np.ndarray,
    k: np.ndarray,
    knob_amplitude: float = 1.0,
) -> np.ndarray:
    """Return P_m^ESD(k) = (1 + delta_cascade) * P_m^LCDM(k)."""
    delta = cascade_modulation(k, knob_amplitude=knob_amplitude)
    return (1.0 + delta) * np.asarray(pk, dtype=float)


if __name__ == "__main__":
    # Quick sanity print across CMB / LSS k-range
    k_test = np.logspace(-4, 1, 7)
    print(f"k_end = {k_end_mpc_inverse():.3e} 1/Mpc")
    print(f"N_e_star = {N_E_STAR:.4f}, max amplitude = 1/N_e_star = {1/N_E_STAR:.4e}")
    print()
    print(f"{'k [1/Mpc]':>12s}  {'delta_cascade':>15s}")
    for kv in k_test:
        d = cascade_modulation(np.array([kv]))[0]
        print(f"{kv:12.4e}  {d:15.4e}")
    print()
    print("LCDM recovery check (knob=0):")
    d0 = cascade_modulation(k_test, knob_amplitude=0.0)
    print(f"  max |delta_cascade| = {np.max(np.abs(d0)):.2e}  (must be 0)")
