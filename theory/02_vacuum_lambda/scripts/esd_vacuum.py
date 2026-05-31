"""Theory 02: ESD vacuum / cosmological-constant applicability.

Apply Paper 1's spectator-relational axioms (A1)-(A3) to the
cosmological vacuum energy Lambda.

Mathematical setup
------------------
Friedmann equation with dark-energy equation of state w(z):

  H^2(z) = H_0^2 [Omega_r (1+z)^4 + Omega_m (1+z)^3
                + Omega_k (1+z)^2 + Omega_Lambda * f_DE(z)]

  f_DE(z) = exp( 3 * integral_0^z [1+w(z')]/(1+z') dz' )

For pure cosmological constant w = -1, f_DE(z) = 1 identically and
rho_Lambda is constant in time.

A1 (bound-system locality)
  R(u) dresses the gravitational interaction between a localized
  massive subsystem and a separated spectator background.  The
  cosmological vacuum is a uniform energy density filling all space;
  there is no system/spectator split internal to Lambda itself.
  A1 fails.

A2 (acceleration definedness)
  u = 4 g / a_0 requires a well-defined Newtonian acceleration g of
  a bound test mass.  Lambda generates a uniform de Sitter expansion
  rate ddot a / a = (8 pi G / 3) rho_Lambda, but this is not the
  Newtonian g of a localized subsystem; it is a homogeneous expansion
  of the background.  u is undefined for the vacuum.
  A2 fails.

A3 (closure universality) holds vacuously: R(u) is universal *where*
it applies.

Therefore R(u) does NOT modify the cosmological constant.

Consequences
------------
  C1. ESD inherits w = -1 exactly (no kinetic term from R(u)).
  C2. ESD inherits Omega_Lambda from the Friedmann sum given the
      framework's locked Omega_m and the observed Omega_r.
  C3. rho_Lambda(z=0) = rho_Lambda(z_recomb) exactly (no running).
  C4. ESD does NOT solve the cosmological-constant problem
      (does not predict the magnitude Lambda/M_Pl^4 ~ 10^-122).
      Honest negative result.

Closure-pool constants (locked from PHI):
  PHI   = (1+sqrt 5)/2     ~ 1.6180
  p     = PHI              (UV exponent)
  q     = 2 ln PHI / PHI   ~ 0.5950
  c     = (4 ln PHI - 1)/PHI ~ 0.5722
  b     = PHI^6 - 2        ~ 15.9443
  s     = 16 PHI + 1       ~ 26.8885
"""
from __future__ import annotations
import math
from typing import Dict
from esd_core import OMEGA_M_LOCK, a_zero  # noqa: F401

# ---------- physical constants (SI) ----------
G_SI    = 6.67430e-11
C_SI    = 299792458.0
HBAR_SI = 1.054571817e-34
KB_SI   = 1.380649e-23
KM_M    = 1000.0
MPC_M   = 3.0856775814913673e22
M_PL_KG = math.sqrt(HBAR_SI * C_SI / G_SI)         # ~ 2.176e-8 kg
M_PL_J  = M_PL_KG * C_SI**2                        # ~ 1.956e9 J
M_PL_EV = M_PL_J / 1.602176634e-19                 # ~ 1.221e28 eV
# Reduced Planck mass in eV
M_PL_REDUCED_EV = M_PL_EV / math.sqrt(8.0 * math.pi)   # ~ 2.435e27 eV

# ---------- closure pool ----------
PHI    = (1.0 + math.sqrt(5.0)) / 2.0
P_EXP  = PHI
Q_EXP  = 2.0 * math.log(PHI) / PHI
C_FLR  = (4.0 * math.log(PHI) - 1.0) / PHI
B_AMP  = PHI**6 - 2.0
S_NRM  = 16.0 * PHI + 1.0
LN_PHI = math.log(PHI)

# ---------- cosmology constants ----------
H0_PLANCK_KMS    = 67.36                   # Planck 2018 baseline
OMEGA_M_LOCK_VAL = float(OMEGA_M_LOCK)     # ESD-locked, ~ 0.31574
T_CMB_K          = 2.7255                  # Fixsen 2009
N_EFF            = 3.046                   # standard 3-neutrino SM

# Planck-2018 reference for Omega_Lambda sanity (we DERIVE ours)
OMEGA_LAMBDA_PLANCK = 0.6842

def hubble_per_s(H0_kms: float = H0_PLANCK_KMS) -> float:
    """H_0 in inverse seconds."""
    return H0_kms * KM_M / MPC_M

def omega_gamma() -> float:
    """Photon density today, Omega_gamma = (pi^2/15) (k_B T_CMB)^4
    / (rho_crit * c^5 * hbar^3).

    Closed form:  Omega_gamma h^2 = 2.4734e-5  (T_CMB = 2.7255 K).
    """
    # exact: rho_gamma = (pi^2/15) * (k_B T)^4 / (hbar^3 c^3)
    # rho_crit = 3 H_0^2 / (8 pi G)
    # Omega_gamma h^2 is independent of H_0
    h = H0_PLANCK_KMS / 100.0
    return 2.4734e-5 / h**2

def omega_nu_relativistic() -> float:
    """Massless-neutrino radiation density (3 SM nu species)."""
    # Omega_nu / Omega_gamma = (7/8) * (4/11)^(4/3) * N_eff
    rel = (7.0/8.0) * (4.0/11.0)**(4.0/3.0) * N_EFF
    return rel * omega_gamma()

def omega_r() -> float:
    """Total relativistic density Omega_r = Omega_gamma + Omega_nu."""
    return omega_gamma() + omega_nu_relativistic()

# ---------------------------------------------------------------
# Derivation A: vacuum applicability theorem
# ---------------------------------------------------------------
def applicability_test_vacuum() -> Dict[str, object]:
    """Apply axioms (A1)-(A3) to the cosmological vacuum Lambda.

    A1: vacuum is a uniform background density; no localized
        massive subsystem; no system/spectator split.   -> FAIL
    A2: Lambda generates uniform de Sitter expansion, not the
        Newtonian acceleration of a bound test mass.    -> FAIL
    A3: vacuously holds (universal where it applies).
    Therefore R(u) does NOT modify Lambda.
    """
    return {
        "A1_bound_system_locality":    False,
        "A2_acceleration_definedness": False,
        "A3_closure_universality":     True,
        "Ru_applies":                  False,
        "rationale": (
            "The cosmological vacuum is a uniform energy density "
            "filling all space.  There is no system/spectator split "
            "for Lambda itself (A1 fails), and no bound test mass "
            "for u = 4 g/a_0 to act on (A2 fails).  ESD cannot "
            "modify the value or time-dependence of Lambda."
        ),
    }

# ---------------------------------------------------------------
# Derivation B: w = -1 inheritance
# ---------------------------------------------------------------
def w_dark_energy_ESD() -> float:
    """ESD-predicted dark-energy equation of state.

    Because R(u) is inactive on the vacuum (Theorem A), Lambda
    has no kinetic contribution from the closure pool.  The
    barotropic equation of state of a pure cosmological constant
    is w = -1 exactly.
    """
    return -1.0

def f_DE(z: float, w0: float = -1.0, wa: float = 0.0) -> float:
    """CPL parameterization: w(z) = w_0 + w_a z/(1+z).

    f_DE(z) = (1+z)^(3(1+w_0+w_a)) exp(-3 w_a z/(1+z)).
    For w_0 = -1, w_a = 0:  f_DE(z) = 1 identically.
    """
    if z == 0.0:
        return 1.0
    return (1.0 + z)**(3.0*(1.0 + w0 + wa)) * math.exp(-3.0*wa*z/(1.0+z))

# ---------------------------------------------------------------
# Derivation C: Omega_Lambda inheritance from Friedmann sum
# ---------------------------------------------------------------
def omega_lambda_ESD(omega_k: float = 0.0) -> float:
    """ESD-predicted Omega_Lambda from the Friedmann sum.

    Omega_m (locked) + Omega_r (CMB + neutrinos, observed) +
    Omega_k (geometry, taken flat) + Omega_Lambda = 1.

    Note: this is NOT an independent closure-pool prediction of
    Omega_Lambda; it is the residual of the Friedmann sum given
    locked Omega_m and observed Omega_r.  See Derivation D for the
    honesty audit on this point.
    """
    return 1.0 - OMEGA_M_LOCK_VAL - omega_r() - omega_k

# ---------------------------------------------------------------
# Derivation D: no Lambda running (rho_Lambda const in time)
# ---------------------------------------------------------------
def rho_lambda_running(z_lo: float, z_hi: float) -> float:
    """rho_Lambda(z_hi) / rho_Lambda(z_lo) for ESD's w = -1.

    rho_Lambda(z) = rho_Lambda(0) * f_DE(z).  For w = -1 this is
    constant in z.  We return f_DE(z_hi)/f_DE(z_lo).
    """
    return f_DE(z_hi) / f_DE(z_lo)

# ---------------------------------------------------------------
# Honesty audit: NO phi-power lock on Lambda magnitude
# ---------------------------------------------------------------
# Measured cosmological-constant magnitude (Planck 2018):
#   rho_Lambda^(1/4) = (2.24 +- 0.04) x 10^-3 eV
# Two conventions for the dimensionless ratio:
#   reduced     M_Pl ~ 2.435e27 eV : log10(rho/M^4) ~ -120.15
#   non-reduced M_Pl ~ 1.221e28 eV : log10(rho/M^4) ~ -122.95
# We audit BOTH.  Phi-power grid spacing in log10 is log10(PHI) ~ 0.209,
# so a single phi^(-N) family will hit any target within ~half the
# spacing = 0.105 in log10, i.e. a "trivial coincidence floor" of
# ~0.087% frac err near log10 ~ -121.  A real lock must beat that.
RHO_LAMBDA_QUARTIC_EV       = 2.24e-3          # (rho_Lambda)^(1/4) in eV  (Planck 2018)
RHO_LAMBDA_QUARTIC_EV_ERR   = 0.04e-3

def lambda_over_MPl4_reduced() -> float:
    """Dimensionless Lambda magnitude using REDUCED M_Pl."""
    return (RHO_LAMBDA_QUARTIC_EV / M_PL_REDUCED_EV)**4

def lambda_over_MPl4_full() -> float:
    """Dimensionless Lambda magnitude using NON-REDUCED M_Pl."""
    return (RHO_LAMBDA_QUARTIC_EV / M_PL_EV)**4

def _scan_phi_powers(target_value: float, N_range=range(400, 700)) -> dict:
    """Find best phi^(-N) hit to target_value (positive linear value).

    Returns best linear-space and log10-space agreement.
    """
    log10_t = math.log10(target_value)
    best = None
    for N in N_range:
        log10_phi_N = -N * math.log10(PHI)
        linear_phi_N = PHI**(-N)
        log10_err = abs(log10_phi_N - log10_t) / abs(log10_t)
        linear_err = abs(linear_phi_N - target_value) / target_value
        rec = (N, linear_phi_N, log10_phi_N, log10_err, linear_err)
        if best is None or linear_err < best[4]:
            best = rec
    N, lin_val, log_val, log_err, lin_err = best
    return {
        "best_N":         N,
        "phi_pow_linear": lin_val,
        "phi_pow_log10":  log_val,
        "target_linear":  target_value,
        "target_log10":   log10_t,
        "log10_frac_err": log_err,
        "linear_frac_err": lin_err,
    }

def _scan_phi_powers_OmegaL(target_value: float = OMEGA_LAMBDA_PLANCK) -> dict:
    """Scan a broader closed-form pool for Omega_Lambda (~ 0.6842)."""
    cands = [
        ("1/PHI",                1.0/PHI),
        ("1/PHI^2",              1.0/PHI**2),
        ("PHI/(1+PHI)",          PHI/(1.0+PHI)),
        ("1 - 1/PHI^2",          1.0 - 1.0/PHI**2),
        ("PHI - 1",              PHI - 1.0),
        ("2 - PHI",              2.0 - PHI),
        ("1 - c",                1.0 - C_FLR),
        ("1 - q",                1.0 - Q_EXP),
        ("c + q",                C_FLR + Q_EXP),
        ("(1+c)/PHI",            (1.0 + C_FLR)/PHI),
        ("PHI^2/(1+PHI^2)",      PHI**2/(1.0+PHI**2)),
        ("2 ln PHI",             2.0*LN_PHI),
        ("3 ln PHI",             3.0*LN_PHI),
    ]
    scored = [(label, val, abs(val - target_value)/target_value) for label, val in cands]
    scored.sort(key=lambda t: t[2])
    return {
        "best_expr":     scored[0][0],
        "best_value":    scored[0][1],
        "best_frac_err": scored[0][2],
        "top3":          [{"expr": e, "value": v, "frac_err": f} for e, v, f in scored[:3]],
    }

def lambda_phi_lock_audit() -> Dict[str, object]:
    """Per ALWAYS-VERIFY rule + PHI-POWER-LOCK-AUDIT rule:

    1. Omega_Lambda scan against a closed-form pool of phi-expressions.
    2. Lambda/M_Pl^4 scan against phi^(-N) family in BOTH conventions
       (reduced and non-reduced M_Pl).
    3. Report linear-space frac err (true lock threshold).
    4. Compute the "trivial coincidence floor" from log10(PHI) spacing
       and flag if best-hit is above or below that floor.

    Real lock requires linear_frac_err << 1e-3 (5+ sig figs).
    Trivial-coincidence linear floor at log10 ~ -121 is e^(0.105 ln 10)
    - 1 ~ 27%.  So linear_frac_err > 27% means worse than a random
    grid hit.  Linear_frac_err > 0.5% means coincidence-grade; < 0.01%
    would be a real lock.
    """
    OL_audit = _scan_phi_powers_OmegaL(OMEGA_LAMBDA_PLANCK)

    L_red  = lambda_over_MPl4_reduced()
    L_full = lambda_over_MPl4_full()
    red_scan  = _scan_phi_powers(L_red)
    full_scan = _scan_phi_powers(L_full)

    # trivial coincidence floor:  10^(0.105) - 1 ~ 0.27  (27% linear)
    trivial_floor_linear = 10.0**(math.log10(PHI)/2.0) - 1.0
    return {
        "Omega_Lambda_audit":        OL_audit,
        "Lambda_M_Pl4_reduced":      L_red,
        "Lambda_M_Pl4_full":         L_full,
        "phi_scan_reduced":          red_scan,
        "phi_scan_full":             full_scan,
        "trivial_floor_linear":      trivial_floor_linear,
        "real_lock_threshold_linear": 5.0e-3,    # 5 sig figs
    }

# ---------------------------------------------------------------
# h-blindness (Thm 1) -- on the framework-theorem outputs
# ---------------------------------------------------------------
# Note: Omega_Lambda itself inherits a tiny ~1e-4 h-dependence from
# Omega_r (since Omega_r h^2 is the H_0-invariant combination).  This
# is standard LambdaCDM, NOT an R(u) effect.  The genuine framework
# theorems are (B) w = -1 and (D) no running; both are identically
# H_0-independent because R(u) is inactive on the vacuum.
def h_blindness_w() -> float:
    """w(z) = -1 has no H_0 dependence; trivially 0."""
    return 0.0

def h_blindness_running(z_lo: float = 0.0, z_hi: float = 1100.0) -> float:
    """rho_Lambda(z_hi)/rho_Lambda(z_lo) = 1 for w=-1; H_0-independent."""
    return abs(rho_lambda_running(z_lo, z_hi) - 1.0)

def h_dependence_OmegaLambda(h_lo: float = 0.50, h_hi: float = 0.80) -> float:
    """Standard LambdaCDM h-dependence of Omega_Lambda via Omega_r.
    Reported for transparency; not a framework gate."""
    h_planck = H0_PLANCK_KMS / 100.0
    Or_planck = omega_r()
    Or_lo = Or_planck * (h_planck/h_lo)**2
    Or_hi = Or_planck * (h_planck/h_hi)**2
    OL_lo = 1.0 - OMEGA_M_LOCK_VAL - Or_lo
    OL_hi = 1.0 - OMEGA_M_LOCK_VAL - Or_hi
    return abs(OL_lo - OL_hi)
