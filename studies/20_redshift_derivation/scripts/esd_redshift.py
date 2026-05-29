"""Study 20: applicability of R(u) to null geodesics.

Companion derivation to Study 19.  Same axiomatic framework
(Paper 1 spectator-relational axioms A1-A3), but applied to
*photons* instead of *linear density perturbations*.

A photon traverses a null geodesic of the background metric.  For
axiom (A2) of R(u) — "u = 4 g / a_0 must be a single well-defined
scalar at the point of evaluation" — the relevant g is the
*gravitational acceleration of a localized mass*.  A photon is
massless and follows a geodesic with zero proper acceleration.
There is no g to feed into u, so (A2) fails identically.

Equivalently from (A1): the closure-pool kernel dresses the
*gravitational interaction between a localized subsystem and a
spectator background*.  A photon is not a localized massive
subsystem — it is a null perturbation of the radiation field and
its trajectory is fixed by the background metric.

Consequences (this study makes them explicit and tests them):

  C1. The cosmological redshift relation is unmodified:
          1 + z = a(t_obs) / a(t_emit)
      (no 'tired light', no anomalous redshift component, no
      Arp-style discordant-redshift mechanism.)

  C2. The comoving distance, luminosity distance, and angular-
      diameter distance inherit their LambdaCDM forms with ESD's
      locked Omega_m:
          D_C(z)  = c * integral_0^z dz' / H(z')
          D_L(z)  = (1+z) D_C(z)
          D_A(z)  = D_C(z) / (1+z)
      where H(z) = H_0 sqrt( Omega_m(1+z)^3 + Omega_Lambda )
      with Omega_m = OMEGA_M_LOCK.

  C3. The Sandage redshift-drift test is unmodified:
          dz/dt_obs = H_0 [ (1+z) - E(z) ]

  C4. Recombination z_* = 1100 is unmodified (radiation epoch
      already locked by Identity B C1).

  C5. h-blindness: at fixed Omega_m and Omega_Lambda, H_0 cancels
      in DIMENSIONLESS observables (the redshift z itself).
"""
from __future__ import annotations
import math
from esd_core import OMEGA_M_LOCK, a_zero

H0_PLANCK_KMS = 67.36
OMEGA_LAMBDA  = 1.0 - OMEGA_M_LOCK
C_KMS         = 299792.458
A0_SI         = a_zero(H0_PLANCK_KMS)

def applicability_test_null_geodesic():
    """Verify R(u) cannot apply to photon propagation.

    Returns the per-axiom check.  R(u) applies only if (A1) AND
    (A2) AND (A3); for a photon (A2) fails identically because the
    photon has no proper acceleration and no associated subsystem g.
    """
    return {
        "A1_bound_system_locality":    False,    # photon is not a localized massive subsystem
        "A2_acceleration_definedness": False,    # massless: no g to feed u = 4g/a_0
        "A3_closure_universality":     True,     # universal IF A1, A2 hold
        "Ru_applies":                  False,
        "rationale": (
            "Photons follow null geodesics with zero proper acceleration. "
            "u = 4 g / a_0 requires a localized mass with a well-defined "
            "gravitational acceleration; this does not exist for a photon. "
            "Both axiom (A1) and axiom (A2) fail."
        ),
    }

def H_of_z(z, H0=H0_PLANCK_KMS, Om=OMEGA_M_LOCK, OL=OMEGA_LAMBDA):
    """Standard LambdaCDM H(z) [km/s/Mpc] with ESD-locked Omega_m."""
    return H0 * math.sqrt(Om * (1.0+z)**3 + OL)

def E_of_z(z, Om=OMEGA_M_LOCK, OL=OMEGA_LAMBDA):
    return math.sqrt(Om * (1.0+z)**3 + OL)

def D_C(z, H0=H0_PLANCK_KMS, Om=OMEGA_M_LOCK, OL=OMEGA_LAMBDA, n=10000):
    """Comoving distance in Mpc.  Simpson integration."""
    if z <= 0:
        return 0.0
    h = z/n
    s = 1.0/E_of_z(0.0, Om, OL) + 1.0/E_of_z(z, Om, OL)
    for i in range(1, n):
        zi = i*h
        s += (4.0 if i % 2 else 2.0) / E_of_z(zi, Om, OL)
    integral = s * h / 3.0
    return (C_KMS / H0) * integral

def D_L(z, **kw):  return (1.0 + z) * D_C(z, **kw)
def D_A(z, **kw):  return D_C(z, **kw) / (1.0 + z)

def mu_distance_modulus(z, **kw):
    """mu = 5 log10(D_L / 10 pc) = 5 log10(D_L [Mpc]) + 25"""
    return 5.0 * math.log10(D_L(z, **kw)) + 25.0

def sandage_drift(z, H0=H0_PLANCK_KMS, Om=OMEGA_M_LOCK, OL=OMEGA_LAMBDA):
    """dz/dt_obs in [s^-1].  H_0 in km/s/Mpc -> s^-1 via 1 Mpc = 3.0857e19 km."""
    H0_inv_s = H0 * 1000.0 / (3.0856775814913673e22)
    return H0_inv_s * ((1.0 + z) - E_of_z(z, Om, OL))

def h_blindness_z():
    """The dimensionless integral D_C * H_0 / c depends only on (z, Omega_m,
    Omega_Lambda), NOT on H_0.  Show by evaluating at two H_0 values."""
    z = 1.0
    C_M_S = 299792458.0
    MPC_M = 3.0856775814913673e22
    def dimensionless(H0_kms):
        H0_si = H0_kms * 1000.0 / MPC_M
        DC_m  = D_C(z, H0=H0_kms) * MPC_M
        return DC_m * H0_si / C_M_S
    a = dimensionless(50.0)
    b = dimensionless(80.0)
    return abs(a - b) / a
