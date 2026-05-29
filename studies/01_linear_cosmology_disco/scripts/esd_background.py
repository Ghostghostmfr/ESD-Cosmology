"""ESD-grammar background sector for DISCO-EB.

Phase 1 strategy: at zero ESD knobs the framework recovers LCDM exactly, so
this module just exports a parameter-dict factory that anchors a DISCO-EB run
to the framework's locked cosmological constants. Once the LCDM-limit recovery
gate is passed (<0.1 percent vs CLASS), Phase 2 will add D-field and
Lambda_eff modifications to H(z).

The dict shape is the DISCO-EB minimal example: Omegam, Omegab, w_DE_0,
w_DE_a, cs2_DE, Omegak, A_s, n_s, H0, Tcmb, YHe, Neff, Nmnu, mnu, k_p.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent

import esd_core as ESD


def esd_param_dict(
    Omegam: float = 0.3099,
    Omegab: float = 0.0488911,
    H0: float = 67.742,
    mnu: float = 0.06,
) -> dict:
    """Build a DISCO-EB param dict anchored on framework-locked values.

    The scalar spectral index n_s and tensor-to-scalar ratio r come from
    esd_core (LOCK after 2026-05-27 Delta_reh derivation). All other
    values are Planck 2018 defaults matching DISCO-EB's minimal example so
    the LCDM-limit recovery check is apples-to-apples vs CLASS.
    """
    return {
        # matter / baryon / curvature
        "Omegam": float(Omegam),
        "Omegab": float(Omegab),
        "Omegak": 0.0,
        # dark energy as quintessence fluid (w0, wa) -- LCDM limit is w0=-1, wa=0
        "w_DE_0": -0.99,  # DISCO-EB minimal example default
        "w_DE_a": 0.0,
        "cs2_DE": 1.0,
        # primordial power spectrum -- framework LOCK
        "A_s": 2.1064e-9,
        "n_s": float(ESD.NS_STAR),  # 0.9611 (LOCK, was 0.96822 in DISCO-EB default)
        "k_p": 0.05,
        # background expansion / CMB
        "H0": float(H0),
        "Tcmb": 2.7255,
        # neutrinos
        "YHe": 0.248,
        "Neff": 2.046,
        "Nmnu": 1,
        "mnu": float(mnu),
    }


def planck2018_param_dict() -> dict:
    """Vanilla Planck 2018 dict matching DISCO-EB's minimal example exactly.

    Used as the LCDM oracle baseline: when ESD's primordial cascade is off,
    esd_param_dict() with n_s set to Planck central (0.96822) must reproduce
    this within solver tolerance. The check is wired in run_lcdm_baseline.
    """
    d = esd_param_dict()
    d["n_s"] = 0.96822
    return d


def esd_locked_param_dict(
    H0: float = 67.36,
    mnu: float = 0.06,
    reading: str = "primary",
) -> dict:
    """Framework zero-parameter LOCK dict.

    Replaces Planck-borrowed (Omega_m, Omega_b, Omega_Lambda) with values
    derived from the ESD Framework (Higginson 2026) Ch.4 topological-reflection identities
    (A) Omega_Lambda = 2 pi c^2 / 3
    (B) 3 Omega_DM + Omega_b = 8 pi c^4 Omega_m
    starting from the single closure constant c = (4 ln phi - 1)/phi.
    n_s is the framework's reheating-derived lock NS_STAR = 0.9611.

    H_0 is NOT framework-locked (Ch.4 explicit statement); use Planck
    baseline. mnu and other thermo defaults follow Planck baseline.

    H(z) is identically LCDM (Paper 1 Sec.4.3): the oscillating D-field
    averages to pressureless dust and is absorbed into Omega_m. This
    factory does NOT modify the expansion history; the framework's
    voice at background level lives entirely in the LOCKED Omega values.

    Reading toggle
    --------------
    ``reading="primary"`` (default): Omega_b is the Planck 2018 anchor
        (OMEGA_B_INPUT = 0.0493). Identity B then fixes Omega_DM.
        This is the headline paper reading.
    ``reading="closure-pool"``: Omega_b is derived from c alone via
        Identity B closed against matter closure (OMEGA_B_LOCK = 0.05009,
        +1.6% above Planck, +2.4 sigma omega_b h^2 pull). This is the
        secondary published prediction.

    Any reading-independent observable (a_0, m_D, lambda_D, n_s, S_8)
    is identical under both options.
    """
    r = ESD.Reading.parse(reading)
    Omegab = ESD.OMEGA_B_INPUT if r is ESD.Reading.PRIMARY else ESD.OMEGA_B_LOCK
    return {
        # matter / baryon / curvature
        # Omega_m: Identity A prediction (LOCK, reading-independent).
        # Omega_b: see reading toggle docstring above.
        "Omegam": float(ESD.OMEGA_M_LOCK),
        "Omegab": float(Omegab),
        "Omegak": 0.0,
        # dark energy: LCDM limit (w0=-1 forbidden by some DE parameterizations;
        # use w_DE_0=-0.99 to match DISCO-EB minimal example and stay clear of
        # divergent quintessence sound-speed at w=-1). At our recovery-gate
        # precision (<1%) this 1% offset in w is below the noise floor.
        "w_DE_0": -0.99,
        "w_DE_a": 0.0,
        "cs2_DE": 1.0,
        # primordial -- framework LOCK
        "A_s": ESD.A_S_PIVOT,
        "n_s": float(ESD.NS_STAR),
        "k_p": ESD.K_PIVOT_MPC,
        # H_0 and thermo: Planck baseline (NOT locked by framework)
        "H0": float(H0),
        "Tcmb": 2.7255,
        "YHe": 0.248,
        "Neff": 2.046,
        "Nmnu": 1,
        "mnu": float(mnu),
    }


if __name__ == "__main__":
    p = esd_param_dict()
    print("ESD-anchored DISCO-EB param dict:")
    for k, v in p.items():
        print(f"  {k:10s} = {v}")
    print(f"\nFramework lock used: n_s = {ESD.NS_STAR:.4f} (Delta_reh = {ESD.DELTA_REH})")
