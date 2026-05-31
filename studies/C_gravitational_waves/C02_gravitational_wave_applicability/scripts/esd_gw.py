"""Study 21: applicability of R(u) to gravitational waves.

Second companion derivation to Study 19 (after Study 20 on photons).
Same axiomatic framework (Paper 1 spectator-relational axioms A1-A3)
applied to *gravitational radiation*.

A gravitational wave is a tensor perturbation h_{mu nu} of the
background metric, propagating at c in vacuum via the linearized
Einstein equations.  For axiom (A1) — "the kernel R(u) dresses the
gravitational interaction between a localized massive subsystem and
a separated spectator background" — the GW is not a localized
massive subsystem; it is a *vacuum perturbation of the background
itself*.  For axiom (A2) — "u = 4 g / a_0 must be a well-defined
scalar at the point of evaluation" — the GW has no proper
acceleration of an associated mass: a test particle in vacuum follows
a geodesic of the perturbed metric, but the GW carries no system g
of its own.

Therefore both (A1) and (A2) fail: R(u) does NOT modify GW
propagation.

Observational consequences:

  C1. c_GW = c exactly.  Falsifiable: any speed difference would
      falsify ESD.  GW170817 already constrains |c_GW - c|/c < 3e-15
      via the 1.74 +- 0.05 s GW-GRB timing across 40 Mpc.

  C2. GW polarization content unchanged: only the two tensor modes
      h_+, h_x (no scalar/vector modes from R(u)).

  C3. GW amplitude scales standardly with luminosity distance:
      h ~ 1/D_L, which inherits the LambdaCDM form from Study 20.

  C4. Standard-siren H_0 from GW170817 inherits LambdaCDM analysis;
      ESD prediction matches the published 70 +12/-8 km/s/Mpc
      (Abbott+2017) within its 1-sigma error.
"""
from __future__ import annotations
import math
from esd_core import OMEGA_M_LOCK, a_zero
import esd_redshift as RZ  # type: ignore  # for D_L

H0_PLANCK_KMS = 67.36
C_M_S         = 299792458.0
MPC_M         = 3.0856775814913673e22
A0_SI         = a_zero(H0_PLANCK_KMS)

def applicability_test_gravitational_wave():
    """Verify R(u) cannot apply to GW propagation in vacuum."""
    return {
        "A1_bound_system_locality":    False,    # GW is a vacuum perturbation, not a localized massive subsystem
        "A2_acceleration_definedness": False,    # no proper acceleration of an associated mass
        "A3_closure_universality":     True,
        "Ru_applies":                  False,
        "rationale": (
            "A gravitational wave is a tensor perturbation h_{mu nu} of "
            "the background metric, propagating at c in vacuum via the "
            "linearized Einstein equations.  There is no localized "
            "massive subsystem and no associated g.  Both (A1) and (A2) "
            "fail; R(u) cannot dress the propagation."
        ),
    }

def cGW_over_c():
    """ESD prediction for the gravitational-wave speed (as fraction of c)."""
    return 1.0

def gw170817_propagation_delay(distance_mpc=40.0):
    """Predicted GW-EM arrival-time difference at Earth in seconds.

    With c_GW = c exactly, any observed delay must be sourced from the
    astrophysical emission process (e.g. GRB delay after BNS merger),
    NOT from differential propagation.  Returns the propagation
    contribution (= 0)."""
    return 0.0

def standard_siren_DL(z, **kw):
    """Luminosity distance to a GW source at redshift z, inherited
    unmodified from the photon-side derivation (Study 20)."""
    return RZ.D_L(z, **kw)

def gw170817_inferred_H0(D_L_mpc_obs=40.0, D_L_err_mpc=(8.0,-14.0),
                         z_em=0.0098, peculiar_v_kms=310.0):
    """LIGO-style standard-siren H_0 estimate from GW170817.

    Uses the EM-determined redshift of NGC 4993 with a peculiar-velocity
    correction.  Returns (H0_central, H0_lo, H0_hi).
    """
    # cosmological redshift after peculiar-velocity subtraction
    z_cosmo = z_em - peculiar_v_kms / 299792.458
    # for z << 1, H_0 = c z / D_L
    H0_central = 299792.458 * z_cosmo / D_L_mpc_obs
    H0_lo      = 299792.458 * z_cosmo / (D_L_mpc_obs + D_L_err_mpc[0])
    H0_hi      = 299792.458 * z_cosmo / (D_L_mpc_obs + D_L_err_mpc[1])
    return H0_central, H0_lo, H0_hi

def h_blindness_GW_observables():
    """GW speed and polarization content are dimensionless / H_0-blind."""
    return 0.0
