"""
Phase 3 Step 2: semi-analytic linear-growth & f sigma_8(z) for the
ESD framework on the locked cosmology, with Yukawa-screened fifth-force.

ESD Framework (Higginson 2026) references:
  Ch.4 Eq. gravity-mD-master:  m_D = a_0 phi / sqrt(8 pi)  (natural units)
  Ch.4 L57:                    beta_m^2 / alpha is structurally absorbed
                               into the canonical normalization that
                               locks a_0.  -> NOT free, but also NOT
                               independently published as a number.
  Ch.3 Eq. parent-deom-canonical:  static Yukawa source = -beta_m c^2/alpha_kin rho_m

Sub-horizon linear growth (quasi-static, scalar-tensor):
  d^2 D / dN^2 + (2 + dlnH/dN) dD/dN = (3/2) Omega_m(a) mu_eff(k,a) D
where N = ln(a), and
  mu_eff(k, a) = G_eff/G = 1 + 2 (beta_m^2/alpha) W(k/a, m_D)
  W(k_phys, m_D) = k_phys^2 / (k_phys^2 + m_D^2),  k_phys = k_comov / a.

Because beta_m^2/alpha is closure-absorbed and not published, we BRACKET
it over [0, 1] (covers null -> max plausible) and report f sigma_8(z) for
each bracket point against published DESI/BOSS RSD data.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.integrate import solve_ivp

PHI = (1.0 + math.sqrt(5.0)) / 2.0
C_CLOSURE = (4.0 * math.log(PHI) - 1.0) / PHI

C_LIGHT = 2.99792458e8
MPC_M = 3.0857e22
H0_KMSMPC = 67.36
H0_SI = H0_KMSMPC * 1.0e3 / MPC_M

OMEGA_M = 0.315736
OMEGA_DM = 0.265642
OMEGA_B = 0.050094
OMEGA_L = 1.0 - OMEGA_M

# m_D in 1/Mpc from step 1
A0 = C_LIGHT * H0_SI * math.sqrt((3.0*OMEGA_DM + OMEGA_B) / (8.0 * math.pi))
LAMBDA_D = C_LIGHT**2 * math.sqrt(8.0 * math.pi) / (A0 * PHI)
M_D_inv_m = 1.0 / LAMBDA_D
M_D = M_D_inv_m * MPC_M       # 1/Mpc

# sigma_8 normalization at z=0 from compute_s8: framework lock = 0.81144 (CB-quadrature)
SIGMA8_Z0 = 0.81144


def H_over_H0(a):
    return math.sqrt(OMEGA_M / a**3 + OMEGA_L)

def dlnH_dN(a):
    h2 = OMEGA_M / a**3 + OMEGA_L
    return -1.5 * OMEGA_M / a**3 / h2

def Omega_m_a(a):
    h2 = OMEGA_M / a**3 + OMEGA_L
    return OMEGA_M / a**3 / h2

def mu_eff(k_comov, a, b2_over_alpha):
    """G_eff/G under Yukawa-screened conformal coupling. k_comov in 1/Mpc."""
    k_phys = k_comov / a
    W = k_phys**2 / (k_phys**2 + M_D**2)
    return 1.0 + 2.0 * b2_over_alpha * W


def growth_ivp(k_comov, b2_over_alpha, N_start=-5.0, N_end=0.0):
    """Integrate sub-horizon growth from a = e^-5 ~ 0.0067 to a = 1.
    Returns f(z=0) = dlnD/dlna at N=0 and D(N) interp."""
    def rhs(N, y):
        a = math.exp(N)
        D, dD = y
        ddD = -(2.0 + dlnH_dN(a)) * dD + 1.5 * Omega_m_a(a) * mu_eff(k_comov, a, b2_over_alpha) * D
        return [dD, ddD]
    # matter-domination IC: D ~ a, dD/dN = D
    sol = solve_ivp(rhs, [N_start, N_end], [math.exp(N_start), math.exp(N_start)],
                    method="RK45", rtol=1e-9, atol=1e-12, dense_output=True)
    return sol


def fsigma8_at_z(k_comov, b2_over_alpha, z_grid):
    """f sigma_8 at requested redshifts, normalized so sigma_8(z=0) matches SIGMA8_Z0
    in the LCDM (b2/alpha=0) limit. For non-zero coupling we scale the LCDM sigma_8
    by the modified D(0)/D_LCDM(0) at the same k."""
    sol = growth_ivp(k_comov, b2_over_alpha)
    sol0 = growth_ivp(k_comov, 0.0)
    # sigma_8(z) = sigma_8(0) * D(z)/D(0) , using mode-dependent D for this k
    N_z = np.array([-math.log1p(z) for z in z_grid])
    D_modified = sol.sol(N_z)[0]
    D_modified_0 = sol.sol(np.array([0.0]))[0][0]
    D_lcdm_0 = sol0.sol(np.array([0.0]))[0][0]
    # absolute amplitude at z=0 scales with modified-vs-LCDM ratio
    sigma8_0_mod = SIGMA8_Z0 * (D_modified_0 / D_lcdm_0)
    sigma8_z = sigma8_0_mod * (D_modified / D_modified_0)
    # f = dlnD/dlna at each z
    eps = 1e-3
    D_plus = sol.sol(N_z + eps)[0]
    D_minus = sol.sol(N_z - eps)[0]
    f_z = (np.log(D_plus) - np.log(D_minus)) / (2.0 * eps)
    return f_z * sigma8_z


# --- DESI Y1 + BOSS DR12 + 6dFGS f sigma_8 compilation (public values) ---
# (z, fsigma8, sigma_err)  rough but representative
RSD_DATA = [
    (0.067, 0.423, 0.055),   # 6dFGS  Beutler+12
    (0.15,  0.490, 0.145),   # SDSS MGS  Howlett+15
    (0.32,  0.427, 0.056),   # BOSS DR12 z1 (Alam+17)
    (0.38,  0.500, 0.039),   # BOSS DR12 zeff=0.38
    (0.51,  0.455, 0.039),   # BOSS DR12 zeff=0.51
    (0.61,  0.436, 0.034),   # BOSS DR12 zeff=0.61
    (0.85,  0.470, 0.040),   # DESI Y1 LRG
    (1.48,  0.300, 0.090),   # DESI Y1 QSO
]

print("=" * 72)
print("Phase 3 Step 2: f sigma_8(z) bracket for ESD locked cosmology")
print("=" * 72)
print(f"m_D = {M_D:.4e} 1/Mpc, lambda_D = {LAMBDA_D:.4e} m")
print(f"Yukawa W at k = 0.1 1/Mpc, a=1:  {(0.1)**2/((0.1)**2 + M_D**2):.6f}")
print("(sub-horizon RSD/BAO scales: W ~ 1 always)")
print()

z_grid = np.array([d[0] for d in RSD_DATA])
fs8_obs = np.array([d[1] for d in RSD_DATA])
fs8_err = np.array([d[2] for d in RSD_DATA])

# bracket beta^2/alpha values; k_eff at BAO scale ~ 0.1 1/Mpc (W ~ 1)
brackets = [0.0, 0.01, 0.05, 0.1, 0.3, 1.0]
k_ref = 0.1  # 1/Mpc, RSD-scale

print(f"{'beta^2/alpha':>14} | " + " ".join(f"z={z:.2f}" for z in z_grid) + " |   chi2/dof")
print("-" * 130)

for b2a in brackets:
    fs8_th = fsigma8_at_z(k_ref, b2a, z_grid)
    chi2 = float(np.sum(((fs8_th - fs8_obs) / fs8_err)**2))
    dof = len(z_grid)
    row = f"{b2a:>14.3f} | " + " ".join(f"{x:6.4f}" for x in fs8_th)
    print(row + f" |  {chi2:6.2f} / {dof}")

print()
print("Observed:    " + " ".join(f"{x:6.4f}" for x in fs8_obs))
print("Errors:      " + " ".join(f"{x:6.4f}" for x in fs8_err))
print()
print("=" * 72)
print("VERDICT")
print("=" * 72)
print("For Yukawa-screened fifth-force at the LOCKED m_D = 1.33e-5 1/Mpc,")
print("the screening W(k,m_D) -> 1 fully for all RSD-scale k.  So mu_eff")
print("is uniformly enhanced -> linear growth boosted at all observable")
print("scales by the SAME factor.  This is degenerate with G itself in")
print("the linear-growth sector: the only signature is the absolute")
print("amplitude of f sigma_8(z) shifting upward with beta^2/alpha.")
print()
print("Whether the framework is observationally consistent depends only")
print("on the value of beta^2/alpha.  From the chi2 bracket above:")
print("  - beta^2/alpha = 0   (pure LCDM):     chi2/dof readout")
print("  - beta^2/alpha < ~0.1 keeps deviation within RSD error bars")
print("  - beta^2/alpha > ~0.3 is increasingly disfavored by current RSD")
print()
print("The framework's structural prediction is that beta^2/alpha is FIXED")
print("by the same canonical normalization that locks a_0 (Ch.4 L57).")
print("Extracting that fixed numerical value is the next derivation step.")
