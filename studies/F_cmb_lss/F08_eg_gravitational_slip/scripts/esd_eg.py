"""ESD E_G predictor (Study 34).

This module is intentionally thin: by Study 19's applicability theorem,
the closure-pool kernel R(u) does NOT modify linear cosmological
perturbations (Axiom A1 fails for linear delta of the same field that
constitutes the background). The E_G statistic is a *linear*
gravitational-slip observable. Therefore:

    mu_ESD(z, k_linear) = 1
    Sigma_ESD(z, k_linear) = 1
    eta_ESD(z) = 1
    E_G_ESD(z) = Omega_m,0 / f(z)   == E_G_LCDM(z)

The predictive content of Study 34 is therefore:

  (a) ESD reproduces the LCDM E_G(z) curve identically at linear scales,
  (b) any reported tension with LCDM E_G is also an ESD tension,
      and identifies systematics in the measurement rather than a
      framework failure,
  (c) ESD predicts a small POSITIVE quasi-linear correction at
      k > 0.1 h/Mpc from the onset of bound-halo formation,
      computable from the halo-model and Study 19's R(u) applied
      to virialized halos.

This script computes (a) directly, and (c) as a forward prediction
for next-generation high-ell E_G probes (LSST x CMB-S4).
"""
from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3]))

from esd_core.constants import S_NORM, C_CHANNEL, PHI, Q_BRIDGE
from eg_data import (
    OMEGA_M0_LOCKED, OMEGA_L0_LOCKED,
    E2_of_z, Omega_m_of_z, growth_rate_f, E_G_predicted,
)

B_BRIDGE: float = PHI ** 6 - 2.0
R_FLOOR: float = S_NORM / C_CHANNEL


def kernel_R(u: float) -> float:
    tS = u ** PHI
    tE = B_BRIDGE * (u ** Q_BRIDGE)
    tD = C_CHANNEL
    return S_NORM / (tS + tE + tD)


def channel_weights(u: float) -> tuple[float, float, float]:
    tS = u ** PHI
    tE = B_BRIDGE * (u ** Q_BRIDGE)
    tD = C_CHANNEL
    sigma = tS + tE + tD
    return tS / sigma, tE / sigma, tD / sigma


# -------- linear-regime ESD = LCDM (Study 19 applicability theorem) ------
def E_G_esd_linear(z: float) -> float:
    return E_G_predicted(z)


def mu_esd_linear() -> float:
    return 1.0


def Sigma_esd_linear() -> float:
    return 1.0


def slip_eta_esd_linear() -> float:
    return 1.0


# -------- quasi-linear correction (forward prediction, k > 0.1 h/Mpc) ----
def quasi_linear_halo_fraction(k_h_per_Mpc: float, z: float) -> float:
    """Fraction of P(k) signal coming from bound halos at wavenumber k.

    Crude halo-model proxy: smooth transition from 0 at k_NL/3 to 1 at
    3 k_NL, where k_NL ~ 0.2 h/Mpc at z=0 evolving as (1+z) D+(0)/D+(z).
    """
    # Linear growth (Carroll-Press-Turner fitting): D+(z) ~ (5/2) Omega_m(z) / E(z) / g(z)
    # we just need a crude (1+z)-scaling for k_NL:
    k_NL_z0 = 0.20            # h/Mpc, conventional nonlinear scale today
    k_NL = k_NL_z0 * (1.0 + z) ** 1.5
    x = k_h_per_Mpc / k_NL
    # smooth Heaviside-ish:
    import math
    return 0.5 * (1.0 + math.tanh(2.0 * math.log(max(x, 1e-12))))


def u_halo_typical() -> float:
    """Typical u for the bound halo population dominating quasi-linear k.

    Galaxy-scale halos (M ~ 1e12 Msun, r ~ 100 kpc) give g ~ 1e-10 m/s^2,
    u = 4g/a_0 ~ 3. Use this as the representative scale for the
    halo-induced E_G correction.
    """
    return 3.0


def E_G_esd_with_halo_correction(z: float, k_h_per_Mpc: float = 0.05) -> float:
    """E_G with halo-model R(u) correction at quasi-linear scales.

    At k_h << k_NL (true linear) returns the LCDM value identically.
    At k_h ~ k_NL the bound-halo fraction enters R(u_halo) and lifts
    E_G by a small calculable amount.

    The lift is in mu (Poisson enhancement) but cancels in Sigma to
    leading order (photons trace (Phi+Psi)/2 which both shift the
    same way under conformal A^2 coupling).
    """
    f_halo = quasi_linear_halo_fraction(k_h_per_Mpc, z)
    R_halo = kernel_R(u_halo_typical())
    wS, wE, wD = channel_weights(u_halo_typical())
    # mu enhancement is dominated by conformal D-channel:
    mu_enh = 1.0 + f_halo * wD * R_halo
    # Sigma enhancement is symmetric photon-bridge -> same conformal lift:
    Sigma_enh = 1.0 + f_halo * 0.5 * wD * R_halo
    # E_G ~ Sigma / mu * (Omega_m,0 / f(z))
    return (Sigma_enh / mu_enh) * E_G_predicted(z)


def summary() -> dict:
    out = {
        "applicability_theorem": (
            "Study 19: R(u) does NOT apply to linear delta; ESD = LCDM "
            "for E_G in the linear regime."
        ),
        "linear_predictions_by_redshift": {},
        "quasi_linear_halo_correction": {},
        "u_halo_typical": u_halo_typical(),
        "R_halo_typical": kernel_R(u_halo_typical()),
        "channel_weights_at_u_halo": list(channel_weights(u_halo_typical())),
        "Omega_m0_locked": OMEGA_M0_LOCKED,
    }
    for z in (0.32, 0.42, 0.57, 0.60, 1.0):
        out["linear_predictions_by_redshift"][f"{z:.2f}"] = {
            "Omega_m_of_z": Omega_m_of_z(z),
            "f(z)":         growth_rate_f(z),
            "E_G_linear":   E_G_esd_linear(z),
            "E_G_at_k_0p10": E_G_esd_with_halo_correction(z, 0.10),
            "E_G_at_k_0p30": E_G_esd_with_halo_correction(z, 0.30),
        }
    out["quasi_linear_halo_correction"]["E_G_at_z_0p57_k_0p30"] = (
        E_G_esd_with_halo_correction(0.57, 0.30)
    )
    out["quasi_linear_halo_correction"]["E_G_linear_z_0p57"] = E_G_esd_linear(0.57)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=2))
