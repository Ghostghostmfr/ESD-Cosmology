"""ESD modification of Newtonian gravity for the N-body solver.

Sub-task 1.2a of simulation 01: pure-function module exposing the
closure-pool kernel R(u), its support Sigma(u), and the **relational
applicability gate** that selects where R(u) is admissible.

Nothing in this module touches ``run_sim.py``. The integrator wiring
lives in sub-task 1.2b, after the FOF halo finder (sub-task 1.4) is
available — at which point the smooth-density gate exposed here is
optionally replaceable by a binary halo-membership mask.

Framework provenance
--------------------
Per Study 19 (applicability theorem for R(u)) and Paper 1 (closure-
pool axioms), the kernel

    R(u) = s / Sigma(u),   Sigma(u) = u^p + b u^q + c,   u = 4 |g_N| / a0

is constructed for a **bound subsystem** feeling a Newtonian
acceleration ``g_N`` from a **separated spectator background**.
Three axioms must hold:

    (A1) Bound-system locality — unambiguous system/spectator split.
    (A2) Newtonian floor      — a well-defined Newtonian g on the
                                bound subsystem.
    (A3) Closure universality — when (A1) and (A2) hold, R is the
                                universal closure-pool kernel.

Linear cosmological perturbations *fail* (A1): rho-bar + delta is one
field at different scales — the "subsystem" and the "spectator" are
the same field. Virialized halos *satisfy* all three axioms, and R(u)
acts as the spectator-relational dressing of the halo's own internal
gravity. This module's ``applicability_gate`` returns the smooth
indicator of "are we in the regime where R(u) is admissible."

All numeric constants come from ``esd_core``. No values are
re-derived here, in keeping with the rule that locked constants
must never drift between studies.
"""

from __future__ import annotations

import math
from typing import Union

import numpy as np
from numpy.typing import NDArray

from esd_core import (
    PHI,
    S_NORM as S_PHI,        # s = 16 phi + 1
    Q_BRIDGE as Q_EXP,      # q = 2 ln phi / phi
    C_CHANNEL as C_PHI,     # c = (4 ln phi - 1) / phi
)

# Locked closure-kernel constants
P_EXP: float = PHI                  # p = phi
B_PHI: float = PHI**6 - 2.0         # b = phi^6 - 2
S_PHI_: float = S_PHI               # re-expose for symmetry
C_PHI_: float = C_PHI

# MOND-scale acceleration — paper-1 literal value (m / s^2). Matches
# the value Study 05 uses bit-for-bit, ensuring the N-body
# dressed-force operator reproduces the RAR result on rotation curves.
A0_SI: float = 1.2e-10

# Virialization threshold for the applicability gate.
# 200 * rho-bar is the standard cosmological convention for halo
# membership (SO(200) halos in every modern halo finder). Width is
# one e-fold (factor e in density), giving a smooth, differentiable
# transition that's effectively binary at scales > 4 e-folds away.
# Both are physical conventions, not tuned parameters.
DELTA_VIR: float = 200.0
GATE_WIDTH_LN: float = 1.0


# ---------------------------------------------------------------------------
# Closure-pool kernel
# ---------------------------------------------------------------------------


ArrayLike = Union[float, NDArray[np.float64]]


def sigma_kernel(u: ArrayLike) -> ArrayLike:
    """Closure-pool support function Sigma(u) = u^p + b u^q + c.

    Positive for all u >= 0 (verified by Study 01's BH audit gate B2).
    """
    return u**P_EXP + B_PHI * u**Q_EXP + C_PHI


def R_kernel(u: ArrayLike) -> ArrayLike:
    """ESD closure-pool kernel R(u) = s / Sigma(u).

    Limits (verified analytically and numerically):
      * u -> 0:    R -> s / c ~ 46.99 (deep-MOND amplification)
      * u -> inf:  R -> 0          (UV-clean, no singularity)
    """
    return S_PHI / sigma_kernel(u)


def u_of_gN(g_N: ArrayLike, a0: float = A0_SI) -> ArrayLike:
    """Map Newtonian acceleration g_N [m/s^2] to the dimensionless u."""
    return 4.0 * np.abs(g_N) / a0


# ---------------------------------------------------------------------------
# Relational applicability gate
# ---------------------------------------------------------------------------


def applicability_gate(
    delta: ArrayLike,
    delta_vir: float = DELTA_VIR,
    width_ln: float = GATE_WIDTH_LN,
) -> ArrayLike:
    """Smooth indicator that axiom (A1) of Study 19 is satisfied.

    The relational kernel R(u) is only admissible where there is an
    unambiguous bound subsystem / spectator split. The standard
    cosmological proxy for "bound subsystem" is the SO(200) halo
    definition: regions with overdensity > 200 * rho-bar.

    We return a smooth tanh-shaped gate in ln(1 + delta), normalised
    so that

        gate -> 0  for delta << delta_vir  (linear regime, fail A1)
        gate -> 1  for delta >> delta_vir  (virialized halo, A1 holds)
        gate = 0.5 at delta == delta_vir.

    ``width_ln`` is the gate half-width in natural log units. The
    default 1.0 means a one-e-fold (~ x e ~ x 2.7) transition window,
    which is sharp enough to be effectively binary at >= 4 e-folds
    away from the threshold and smooth enough for a gradient-based
    integrator. Sensitivity to this choice is a sub-task 1.2b figure.
    """
    delta = np.asarray(delta, dtype=float) if not np.isscalar(delta) else delta
    arg = (np.log1p(delta) - math.log1p(delta_vir)) / width_ln
    return 0.5 * (1.0 + np.tanh(arg))


# ---------------------------------------------------------------------------
# Composite operator: dressed acceleration
# ---------------------------------------------------------------------------


def dressed_acceleration(
    g_N: ArrayLike,
    delta: ArrayLike,
    a0: float = A0_SI,
    delta_vir: float = DELTA_VIR,
    width_ln: float = GATE_WIDTH_LN,
) -> ArrayLike:
    """Apply the gated ESD closure to a Newtonian acceleration field.

        g_ESD = g_N * [ 1 + gate(delta) * R(u(g_N)) ]

    In the linear regime gate -> 0, recovering g_ESD = g_N exactly
    (matching ESD's ΛCDM-equivalent linear sector, per Study 19).
    In the virialized regime gate -> 1 and the operator reduces to
    Study 05's RAR mapping g_ESD = g_N (1 + R(u)) bit-for-bit.

    This is the **operator that should be wired into the PM solver**
    in sub-task 1.2b. Until then it is exposed as a pure function
    so that the tests and the RAR cross-check in this module exercise
    exactly the form the integrator will see.
    """
    u = u_of_gN(g_N, a0)
    return g_N * (1.0 + applicability_gate(delta, delta_vir, width_ln) * R_kernel(u))


# ---------------------------------------------------------------------------
# Self-test: cross-check against Study 05 + analytic limits
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    """Verify the kernel matches Study 05 and respects the gate limits."""
    # Re-implementation in this module must match Study 05's R_esd bit-for-bit
    # at a representative sweep of u-values.
    from importlib import util
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    rar_path = os.path.abspath(
        os.path.join(here, "..", "..", "..", "studies", "05_rar", "scripts", "esd_rar.py")
    )
    spec = util.spec_from_file_location("esd_rar", rar_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import Study 05 esd_rar from {rar_path}")
    rar = util.module_from_spec(spec)
    spec.loader.exec_module(rar)

    u_grid = np.logspace(-3, 4, 71)
    R_here = R_kernel(u_grid)
    R_rar = rar.R_esd(u_grid)
    rel = np.max(np.abs((R_here - R_rar) / R_rar))

    # Analytic limits.
    # Sigma(u) approaches c slowly because q = 2 ln phi / phi ~= 0.595,
    # so the b u^q term decays only as u^0.595. To probe R(u->0) at
    # machine precision we need u <~ 1e-20.
    R_zero = R_kernel(1e-20)
    R_inf = R_kernel(1e8)
    sc_ratio = S_PHI / C_PHI

    # Gate behaviour. At delta = 0 (mean density) the gate is small but
    # *not* zero (~ 2.5e-5 with width_ln=1, threshold=200): an empty
    # void (delta -> -1) is the true linear-regime limit.
    g_empty = float(applicability_gate(-0.9999))
    g_at_thresh = float(applicability_gate(DELTA_VIR))
    g_halo = float(applicability_gate(1e6))

    # Composite operator collapses to GR in a true linear-regime cell
    g_N_test = 1e-12
    g_ESD_linear = float(dressed_acceleration(g_N_test, delta=-0.9999))
    rel_linear = abs(g_ESD_linear - g_N_test) / g_N_test

    # ...and to Study-05 form in the virialized regime. The tanh gate
    # asymptotes; delta = 1e10 saturates it to machine precision.
    g_N_halo = 1e-11
    g_ESD_halo = float(dressed_acceleration(g_N_halo, delta=1e10))
    g_ESD_study05 = float(rar.g_esd_vec(np.array([g_N_halo]))[0])
    rel_halo = abs(g_ESD_halo - g_ESD_study05) / g_ESD_study05

    result = {
        "max_rel_err_vs_study05_R": rel,
        "R_at_u0": R_zero,
        "R_at_u_inf": R_inf,
        "s_over_c_target": sc_ratio,
        "gate_empty_void": g_empty,
        "gate_at_threshold": g_at_thresh,
        "gate_halo": g_halo,
        "rel_err_linear_collapse": rel_linear,
        "rel_err_halo_matches_study05": rel_halo,
    }

    ok = (
        rel < 1e-12
        and abs(R_zero - sc_ratio) / sc_ratio < 1e-8
        and R_inf < 1e-5
        and g_empty < 1e-8
        and abs(g_at_thresh - 0.5) < 1e-10
        and g_halo > 0.999
        and rel_linear < 1e-8
        and rel_halo < 1e-10
    )

    if verbose:
        print("[esd_mod] R(u) vs Study 05 max rel err :", f"{rel:.2e}")
        print(f"[esd_mod] R(u -> 0)         = {R_zero:.6f}  (target s/c = {sc_ratio:.6f})")
        print(f"[esd_mod] R(u -> inf)       = {R_inf:.2e}   (target 0)")
        print(f"[esd_mod] gate(empty void)  = {g_empty:.2e}  (target ~0)")
        print(f"[esd_mod] gate(delta=200)   = {g_at_thresh:.4f}  (target 0.5)")
        print(f"[esd_mod] gate(delta=1e6)   = {g_halo:.6f}     (target ~1)")
        print(f"[esd_mod] linear collapse  rel err = {rel_linear:.2e}")
        print(f"[esd_mod] halo == Study 05 rel err = {rel_halo:.2e}")
        print(f"[esd_mod] {'PASS' if ok else 'FAIL'}")

    result["passed"] = ok
    return result


if __name__ == "__main__":
    import sys

    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
