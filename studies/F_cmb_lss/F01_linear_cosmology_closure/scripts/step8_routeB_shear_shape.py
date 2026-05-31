"""
Step 8 Route B: Cosmic shear SHAPE test.

Question: After absorbing the +6% P(k) amplitude offset into a single
multiplicative constant (i.e. a re-calibration of sigma_8), does the
locked vs Planck SHAPE of P(k) -- and the corresponding cosmic-shear
two-point projection xi_+(theta) -- still distinguish at sub-sigma in
KiDS-1000-class precision?

Approach (linear-only; valid for k < 0.1 h/Mpc, theta > ~30 arcmin):
    1. Take locked & Planck linear P(k) at z=0 (CLASS, already stored).
    2. Marginalize over a free amplitude A: fit P_lock(k) <-> A*P_planck(k)
       with diagonal sigma = 1% of P_planck (rough KiDS-1000 mode floor).
    3. Examine the AMPLITUDE-FREE shape residual r(k) = P_lock/P_planck - A.
    4. Project both P(k) to a representative KiDS-1000-bin xi_+(theta) via
       Limber + flat-sky J_0 kernel using a Gaussian-window source kernel
       peaking at z=0.5 (KiDS-1000 bin 3 effective z).
    5. Quote (a) sigma_8 mis-calibration implied by best-fit A, (b) shape
       residual chi^2, (c) xi_+(theta) shape residual after amplitude
       rescaling vs KiDS-1000 quoted xi_+ precision (~3-5% per theta bin).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.interpolate import interp1d
from scipy.special import j0

# ------------------------------------------------------------------
# Load locked vs Planck linear P(k, z=0)
# ------------------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
data = np.load(os.path.join(ROOT, "outputs", "phase2a_locked_z0.npz"))
k = data["k"]                           # [h/Mpc] CLASS native grid
P_lock = data["p_class_lock"]           # [Mpc/h]^3
P_planck = data["p_class_planck"]
H0 = float(data["H0"])
h = H0 / 100.0
Omega_m_lock = float(data["Omega_m_lock"])
n_s = float(data["n_s_lock"])

print("=" * 78)
print("Step 8 Route B: Cosmic-shear SHAPE residual test")
print("=" * 78)
print(f"H_0 = {H0:.3f}  Omega_m_lock = {Omega_m_lock:.4f}  n_s = {n_s:.4f}")
print(f"k-grid:  {k.min():.4e} -- {k.max():.4e} h/Mpc   (npts = {len(k)})")
print()

# ------------------------------------------------------------------
# Step 1: best-fit amplitude rescaling
# ------------------------------------------------------------------
# Restrict to the linear regime relevant for cosmic shear xi_+ at
# theta > 30 arcmin, which corresponds to ell ~ 100-3000.
# Using Limber  k ~ ell / chi(z_eff) with chi(0.5) ~ 1900 Mpc ->
# ell = 100..3000 maps k ~ 5e-3 .. 0.16 h/Mpc (in 1/Mpc:  ~ 0.0033 .. 0.105)
kmin, kmax = 5e-3, 0.15      # h/Mpc, well inside linear regime
mask = (k >= kmin) & (k <= kmax)
kf = k[mask]
Plf = P_lock[mask]
Ppf = P_planck[mask]

# Assume diagonal 1% sigma per logk mode (representative KiDS shear mode-
# noise floor).  Cosmic shear at 1% per ell-bin is already aspirational.
sigma_frac = 0.01
sigma_P = sigma_frac * Ppf

# Amplitude best fit:  A = sum(P_lock * P_planck / sig^2) / sum(P_planck^2 / sig^2)
A = np.sum(Plf * Ppf / sigma_P**2) / np.sum(Ppf**2 / sigma_P**2)
sigma8_miscal = np.sqrt(A) - 1.0     # P ~ sigma_8^2 -> A = (sigma_8_lock/sigma_8_planck)^2
ratio = Plf / Ppf
mean_ratio = np.mean(ratio)
print(f"Best-fit amplitude rescaling   A   = {A:.6f}")
print(f"  Implied sigma_8 mis-calibration  = {sigma8_miscal*100:+.3f}%")
print(f"  Mean unweighted P_lock/P_planck  = {mean_ratio:.6f}  ({(mean_ratio-1)*100:+.3f}%)")
print()

# Shape residual after amplitude marginalisation
resid = (Plf - A * Ppf) / sigma_P
chi2_shape = float(np.sum(resid**2))
ndof = len(kf) - 1
print(f"Shape-only residual: chi^2 = {chi2_shape:.2f}  / dof = {ndof}  -> {chi2_shape/ndof:.3f}")
print(f"  RMS shape mismatch (after amplitude fit) = "
      f"{np.sqrt(np.mean((Plf/(A*Ppf)-1.0)**2))*100:.4f}% per mode")
print(f"  max |P_lock/(A*P_planck) - 1|            = "
      f"{np.max(np.abs(Plf/(A*Ppf)-1.0))*100:.4f}%")
print()

# ------------------------------------------------------------------
# Step 2: Limber projection to xi_+(theta) for a KiDS-1000-like
# tomographic bin centred on z_eff ~ 0.5.
# ------------------------------------------------------------------
c_kms = 299792.458
Omega_L_lock = 1.0 - Omega_m_lock

def H_of_z(z, Om=Omega_m_lock):
    OL = 1.0 - Om
    return H0 * np.sqrt(Om * (1 + z)**3 + OL)

def chi_of_z(z, Om=Omega_m_lock):
    """Comoving distance in Mpc."""
    return c_kms * quad(lambda zp: 1.0 / H_of_z(zp, Om), 0, z)[0]

# Source redshift distribution: Gaussian centred at z=0.5, sigma=0.1
# (representative KiDS-1000 bin 3 effective shape).
z_src = np.linspace(0.05, 1.5, 60)
n_z = np.exp(-0.5 * ((z_src - 0.5) / 0.1)**2)
n_z /= np.trapezoid(n_z, z_src)

chi_src = np.array([chi_of_z(z) for z in z_src])

# Lensing kernel q(chi) = (3/2) Omega_m (H0/c)^2 chi (1+z) *
#                         integral_{z}^{infty} dz' n(z') (1 - chi/chi(z'))
def q_of_z(z):
    chi_z = chi_of_z(z)
    integrand = n_z * np.where(chi_src > chi_z,
                               (1.0 - chi_z / np.where(chi_src > 0, chi_src, 1)),
                               0.0)
    return (1.5 * Omega_m_lock * (H0 / c_kms)**2
            * chi_z * (1 + z) * np.trapezoid(integrand, z_src))

# We use the same kernel for both cosmologies (Omega_m, H0 differ by <0.2%
# -> negligible effect on shape).  This isolates the P(k) shape sensitivity.

# Build C_ell^kk via Limber:
#   C_ell = integral dz [q(z)^2 / (H(z)/c * chi(z)^2)] P( k=ell/chi(z), z=0 )
ell_arr = np.logspace(np.log10(50), np.log10(3000), 25)

# Interpolators on log-log for stability
logk_in_h = np.log(k)
log_Plock = np.log(P_lock)
log_Pplanck = np.log(P_planck)
interp_lock = interp1d(logk_in_h, log_Plock, kind="cubic",
                       bounds_error=False, fill_value=-np.inf)
interp_planck = interp1d(logk_in_h, log_Pplanck, kind="cubic",
                         bounds_error=False, fill_value=-np.inf)

def P_at(k_h, which):
    f = interp_lock if which == "lock" else interp_planck
    return np.exp(f(np.log(k_h)))

# Use z-grid for Limber integration
z_int = np.linspace(0.02, 1.4, 80)
chi_int = np.array([chi_of_z(z) for z in z_int])
H_int = np.array([H_of_z(z) for z in z_int])
q_int = np.array([q_of_z(z) for z in z_int])
# growth-factor-squared scaling assumed identical for both cosmologies
# (Omega_m differs by 0.14%; D(z) shape effect on C_ell is ~ 1e-4)
prefactor = q_int**2 / (H_int / c_kms * chi_int**2)

def C_ell(ell, which):
    out = 0.0
    for i, z in enumerate(z_int):
        kh = (ell / chi_int[i]) / h   # convert 1/Mpc to h/Mpc
        if kh < k.min() or kh > k.max():
            continue
        # P(k) in (Mpc/h)^3 -> divide by h^3 to get Mpc^3
        Pk = P_at(kh, which) / h**3
        out += prefactor[i] * Pk
    dz = z_int[1] - z_int[0]
    return out * dz

C_lock = np.array([C_ell(e, "lock")   for e in ell_arr])
C_planck = np.array([C_ell(e, "planck") for e in ell_arr])

# xi_+(theta) via flat-sky J_0 transform
theta_arcmin = np.logspace(np.log10(2), np.log10(300), 18)
theta_rad = theta_arcmin * (np.pi / 180.0 / 60.0)

ell_fine = np.logspace(np.log10(2), np.log10(1e4), 600)
C_lock_fine   = np.interp(ell_fine, ell_arr, C_lock,   left=C_lock[0],   right=0.0)
C_planck_fine = np.interp(ell_fine, ell_arr, C_planck, left=C_planck[0], right=0.0)

def xi_plus(theta_r, Cf):
    integrand = ell_fine * Cf * j0(ell_fine * theta_r) / (2 * np.pi)
    return np.trapezoid(integrand, ell_fine)

xi_lock   = np.array([xi_plus(t, C_lock_fine)   for t in theta_rad])
xi_planck = np.array([xi_plus(t, C_planck_fine) for t in theta_rad])

print("-" * 78)
print("Cosmic-shear xi_+(theta) projection (Limber + flat-sky J_0)")
print("-" * 78)
print(f"{'theta [arcmin]':<16}{'xi_+ lock':<13}{'xi_+ Planck':<13}"
      f"{'shift%':<10}")
for t, xl, xp in zip(theta_arcmin, xi_lock, xi_planck):
    print(f"{t:<16.2f}{xl:<13.4e}{xp:<13.4e}{(xl/xp-1)*100:+<10.3f}")
print()

# Amplitude-marginalised xi_+ shape comparison
A_xi = np.sum(xi_lock * xi_planck) / np.sum(xi_planck**2)
shape_resid_xi = xi_lock / (A_xi * xi_planck) - 1.0
print(f"Best-fit amplitude ratio (xi space)  A_xi = {A_xi:.6f}")
print(f"  implied sigma_8 mis-calibration         = {(np.sqrt(A_xi)-1)*100:+.3f}%")
rms_shape = np.sqrt(np.mean(shape_resid_xi**2)) * 100
max_shape = np.max(np.abs(shape_resid_xi)) * 100
print(f"  RMS xi_+ shape residual after rescale  = {rms_shape:.4f}%")
print(f"  Max |xi_+ shape residual|              = {max_shape:.4f}%")
print()

# KiDS-1000 quoted xi_+ per-theta-bin precision: ~3-5% in the best bins,
# >=10% in the lowest-amplitude bins.  Use 4% as a uniform shape-mode floor.
sigma_xi_pct = 4.0
print(f"KiDS-1000-class shape-mode precision floor:  ~ {sigma_xi_pct:.1f}% per theta bin")
if max_shape < sigma_xi_pct:
    print(f"-> xi_+ SHAPE is INDISTINGUISHABLE from Planck at KiDS-1000 precision.")
else:
    print(f"-> xi_+ SHAPE could be detectable in best KiDS bins.")
print()

# ------------------------------------------------------------------
# Verdict
# ------------------------------------------------------------------
print("=" * 78)
print("VERDICT")
print("=" * 78)
print()
print(f"P(k) amplitude offset absorbs into  sigma_8_lock / sigma_8_planck")
print(f"  = sqrt(A) = {np.sqrt(A):.5f}    ({sigma8_miscal*100:+.3f}%)")
print(f"P(k) shape residual after amplitude marginalisation:")
print(f"  RMS = {np.sqrt(np.mean((Plf/(A*Ppf)-1.0)**2))*100:.4f}%  per mode")
print(f"  max = {np.max(np.abs(Plf/(A*Ppf)-1.0))*100:.4f}%")
print()
print(f"xi_+(theta) projected shape residual (after A_xi rescale):")
print(f"  RMS = {rms_shape:.4f}%   max = {max_shape:.4f}%")
print(f"  vs ~{sigma_xi_pct}% KiDS-1000 per-bin precision")
print()
if max_shape < sigma_xi_pct and chi2_shape / ndof < 2:
    print("ROUTE B PASS: After absorbing the 6% offset into a +3% sigma_8")
    print("re-calibration, the residual SHAPE is below KiDS-1000 per-bin precision.")
    print("Locked-vs-Planck is observationally indistinguishable at current shear")
    print("precision when sigma_8 is treated as a fit parameter.")
else:
    print("ROUTE B FAIL: shape residual survives amplitude marginalisation.")
print()

# ------------------------------------------------------------------
# Figure
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(11, 8))

ax = axes[0, 0]
ax.loglog(kf, Plf, label="locked", lw=1.7, color="goldenrod")
ax.loglog(kf, Ppf, label="Planck",  lw=1.0, color="black", linestyle="--")
ax.set_xlabel(r"$k\ [h/\mathrm{Mpc}]$"); ax.set_ylabel(r"$P(k)\ [(\mathrm{Mpc}/h)^3]$")
ax.set_title(r"Linear $P(k,z=0)$, locked vs Planck"); ax.grid(True, alpha=0.3); ax.legend()

ax = axes[0, 1]
ax.semilogx(kf, (Plf / Ppf - 1) * 100,
            label=r"raw $P_\mathrm{lock}/P_\mathrm{Planck} - 1$", color="C0")
ax.semilogx(kf, (Plf / (A * Ppf) - 1) * 100,
            label="after best-fit amplitude $A$", color="firebrick")
ax.axhline(0, color="black", lw=0.7)
ax.set_xlabel(r"$k\ [h/\mathrm{Mpc}]$"); ax.set_ylabel(r"residual [%]")
ax.set_title("Shape vs amplitude split"); ax.grid(True, alpha=0.3); ax.legend()

ax = axes[1, 0]
ax.loglog(theta_arcmin, xi_lock,   color="goldenrod", lw=1.7, label="locked")
ax.loglog(theta_arcmin, xi_planck, color="black",     lw=1.0, linestyle="--", label="Planck")
ax.set_xlabel(r"$\theta$ [arcmin]"); ax.set_ylabel(r"$\xi_+(\theta)$")
ax.set_title(r"Cosmic-shear $\xi_+$ (KiDS-bin-3 mock)"); ax.grid(True, alpha=0.3); ax.legend()

ax = axes[1, 1]
ax.semilogx(theta_arcmin, (xi_lock / xi_planck - 1) * 100,
            label=r"raw $\xi_\mathrm{lock}/\xi_\mathrm{Planck} - 1$", color="C0")
ax.semilogx(theta_arcmin, shape_resid_xi * 100,
            label="after best-fit amplitude $A_\\xi$", color="firebrick")
ax.axhline(0, color="black", lw=0.7)
ax.axhspan(-sigma_xi_pct, sigma_xi_pct, color="grey", alpha=0.15,
           label=f"KiDS ~{sigma_xi_pct:.0f}% floor")
ax.set_xlabel(r"$\theta$ [arcmin]"); ax.set_ylabel(r"$\xi_+$ residual [%]")
ax.set_title(r"$\xi_+$ shape vs amplitude split"); ax.grid(True, alpha=0.3); ax.legend()

plt.tight_layout()
out_dir = os.path.join(ROOT, "outputs")
fig_path = os.path.join(out_dir, "step8_routeB_shear_shape.png")
plt.savefig(fig_path, dpi=140)
print(f"Wrote figure: {fig_path}")
