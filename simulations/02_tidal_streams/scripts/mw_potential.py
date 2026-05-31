"""Milky Way axisymmetric potential -- sub-task D.1.

Three-component baseline used throughout the rest of Study D:

    Phi_total(R, z) = Phi_bulge + Phi_disk + Phi_halo

* Bulge   : Hernquist (1990)
* Disk    : Miyamoto-Nagai (1975)
* Halo    : NFW (Navarro-Frenk-White 1996)

Parameters tuned so the circular velocity at the Sun
(R = 8.122 kpc, GRAVITY 2019) matches v_c = 229 +/- 0.2 km/s
(Eilers+ 2019). This places us inside the Bovy MWPotential2014
family but with a Hernquist bulge for analytic simplicity.

Units throughout: kpc, km/s, M_sun. G = 4.302e-6 kpc (km/s)^2 / M_sun.

CLI:
    python scripts/mw_potential.py            # run self-test
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

G_GAL: float = 4.302e-6                  # kpc * (km/s)^2 / M_sun
R0_KPC: float = 8.122                    # Sun's galactocentric radius
V_CIRC_R0_KMS: float = 229.0             # Eilers+ 2019
KPC_TO_KM: float = 3.0857e16             # for time conversion
GYR_TO_S: float = 3.1557e16


# ---------------------------------------------------------------------------
# Potential dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HernquistBulge:
    M_msun: float = 1.0e10
    a_kpc: float = 0.7

    def potential(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        return -G_GAL * self.M_msun / (r + self.a_kpc)

    def v_circ2(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        # v^2 = G M r / (r + a)^2
        return G_GAL * self.M_msun * r / (r + self.a_kpc) ** 2

    def accel_spherical(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        """Magnitude of radial acceleration (pointing toward centre)."""
        return G_GAL * self.M_msun / (r + self.a_kpc) ** 2


@dataclass(frozen=True)
class MiyamotoNagaiDisk:
    M_msun: float = 6.5e10
    a_kpc: float = 3.0
    b_kpc: float = 0.28

    def potential(
        self, R: NDArray[np.float64], z: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        zb = np.sqrt(z * z + self.b_kpc ** 2)
        denom = np.sqrt(R * R + (self.a_kpc + zb) ** 2)
        return -G_GAL * self.M_msun / denom

    def v_circ2(self, R: NDArray[np.float64]) -> NDArray[np.float64]:
        # v_c^2(R, z=0) = G M R^2 / [R^2 + (a+b)^2]^(3/2)
        ab = self.a_kpc + self.b_kpc
        return G_GAL * self.M_msun * R * R / (R * R + ab * ab) ** 1.5

    def accel(
        self, R: NDArray[np.float64], z: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Cylindrical (a_R, a_z) accelerations (negative inward / downward)."""
        zb = np.sqrt(z * z + self.b_kpc ** 2)
        s = self.a_kpc + zb
        denom = (R * R + s * s) ** 1.5
        a_R = -G_GAL * self.M_msun * R / denom
        a_z = -G_GAL * self.M_msun * z * s / (zb * denom)
        return a_R, a_z


@dataclass(frozen=True)
class NFWHalo:
    """Spherical NFW profile, parameterised by virial mass and concentration.

    rho(r) = rho_s / [ (r/r_s) (1 + r/r_s)^2 ],
    M(<r) = 4 pi rho_s r_s^3 [ ln(1+x) - x/(1+x) ],  x = r / r_s.
    """
    M_vir_msun: float = 1.0e12
    c: float = 15.0
    r_vir_kpc: float = 245.0             # ~ R200 for 1e12 M_sun host

    @property
    def r_s_kpc(self) -> float:
        return self.r_vir_kpc / self.c

    @property
    def _gc(self) -> float:
        c = self.c
        return math.log(1.0 + c) - c / (1.0 + c)

    @property
    def rho_s(self) -> float:
        return self.M_vir_msun / (
            4.0 * math.pi * self.r_s_kpc ** 3 * self._gc
        )

    def m_enclosed(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        x = r / self.r_s_kpc
        return (4.0 * math.pi * self.rho_s * self.r_s_kpc ** 3) * (
            np.log(1.0 + x) - x / (1.0 + x)
        )

    def potential(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        # Phi(r) = -4 pi G rho_s r_s^3 ln(1 + r/r_s) / r
        prefac = 4.0 * math.pi * G_GAL * self.rho_s * self.r_s_kpc ** 3
        x = r / self.r_s_kpc
        return -prefac * np.log(1.0 + x) / np.where(r > 0, r, 1.0)

    def v_circ2(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        return G_GAL * self.m_enclosed(r) / r

    def accel_spherical(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        """Magnitude of radial acceleration (pointing toward centre)."""
        return G_GAL * self.m_enclosed(r) / (r * r)


# ---------------------------------------------------------------------------
# Composite model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MWPotential:
    bulge: HernquistBulge = HernquistBulge()
    disk: MiyamotoNagaiDisk = MiyamotoNagaiDisk()
    halo: NFWHalo = NFWHalo()

    def potential(
        self, R: NDArray[np.float64], z: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        r = np.sqrt(R * R + z * z)
        return (
            self.bulge.potential(r)
            + self.disk.potential(R, z)
            + self.halo.potential(r)
        )

    def v_circ(self, R: NDArray[np.float64]) -> NDArray[np.float64]:
        """Mid-plane circular speed."""
        z = np.zeros_like(R)
        r = np.sqrt(R * R + z * z)
        v2 = (
            self.bulge.v_circ2(r)
            + self.disk.v_circ2(R)
            + self.halo.v_circ2(r)
        )
        return np.sqrt(v2)

    def accel_cart(
        self, xyz: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Cartesian acceleration for an (N, 3) position array.

        Returns ``(N, 3)`` acceleration vector ``a`` such that
        ``dv/dt = a``.
        """
        x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
        R = np.sqrt(x * x + y * y)
        r = np.sqrt(R * R + z * z)
        # spherical contributions (bulge + halo) -> radial unit vector r_hat
        sph_mag = (
            self.bulge.accel_spherical(r) + self.halo.accel_spherical(r)
        )
        # unit r_hat (guard r > 0)
        rsafe = np.where(r > 0, r, 1.0)
        ax = -sph_mag * x / rsafe
        ay = -sph_mag * y / rsafe
        az = -sph_mag * z / rsafe
        # disk contribution (cylindrical, a_R + a_z)
        a_R, a_z = self.disk.accel(R, z)
        Rsafe = np.where(R > 0, R, 1.0)
        ax = ax + a_R * x / Rsafe
        ay = ay + a_R * y / Rsafe
        az = az + a_z
        return np.stack([ax, ay, az], axis=1)


DEFAULT_MW = MWPotential()


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    mw = DEFAULT_MW

    # (1) Circular velocity at the Sun.
    R_arr = np.array([R0_KPC])
    vc = float(mw.v_circ(R_arr)[0])
    vc_ok = (V_CIRC_R0_KMS - 5.0) < vc < (V_CIRC_R0_KMS + 5.0)

    # (2) Decomposition at the Sun.
    r_sun = np.array([R0_KPC])
    vb = math.sqrt(float(mw.bulge.v_circ2(r_sun)[0]))
    vd = math.sqrt(float(mw.disk.v_circ2(r_sun)[0]))
    vh = math.sqrt(float(mw.halo.v_circ2(r_sun)[0]))

    # (3) Rotation curve sanity: flat-ish out to ~30 kpc, then declining.
    R_grid = np.linspace(2.0, 60.0, 12)
    vcurve = mw.v_circ(R_grid)
    peak = float(vcurve.max())
    peak_at_R = float(R_grid[int(np.argmax(vcurve))])
    flat_ok = 150.0 < peak < 260.0 and 4.0 < peak_at_R < 25.0

    # (4) Acceleration consistency at the Sun.
    xyz = np.array([[R0_KPC, 0.0, 0.0]])
    a = mw.accel_cart(xyz)[0]
    a_R = -a[0]                              # inward radial in mid-plane
    # v_c^2 / R should equal radial acceleration magnitude
    a_expected = vc * vc / R0_KPC
    rel = abs(a_R - a_expected) / a_expected
    acc_ok = rel < 1.0e-6

    # (5) Potential is monotonically rising (toward zero) for r > 50 kpc.
    # NFW only falls as log(r)/r so we cannot use a literal r -> infinity
    # test; instead we check Phi(100 kpc) > Phi(50 kpc) > Phi(R0).
    r_check = np.array([R0_KPC, 50.0, 100.0])
    pot_check = mw.potential(r_check, np.zeros_like(r_check))
    far_ok = bool(pot_check[2] > pot_check[1] > pot_check[0])

    all_ok = vc_ok and flat_ok and acc_ok and far_ok

    if verbose:
        print(f"[mw] v_circ(R0={R0_KPC} kpc)      = {vc:7.2f} km/s   "
              f"(target {V_CIRC_R0_KMS} +/- 5)")
        print(f"[mw]    bulge contribution     = {vb:7.2f} km/s")
        print(f"[mw]    disk  contribution     = {vd:7.2f} km/s")
        print(f"[mw]    halo  contribution     = {vh:7.2f} km/s")
        print(f"[mw] rotation curve peak       = {peak:7.2f} km/s at "
              f"R = {peak_at_R:.1f} kpc")
        print(f"[mw] |a_R - v_c^2/R| / a_R     = {rel:.3e}  (< 1e-6)")
        print(f"[mw] Phi(R0,50,100) kpc        = "
              f"{pot_check[0]:.3e}, {pot_check[1]:.3e}, {pot_check[2]:.3e}")
        print(f"[mw] {'PASS' if all_ok else 'FAIL'}")

    return dict(
        passed=bool(all_ok), v_circ_kms=vc,
        v_bulge=vb, v_disk=vd, v_halo=vh,
        rot_peak=peak, rot_peak_R=peak_at_R,
        accel_rel_err=rel,
        pot_R0=float(pot_check[0]),
        pot_50=float(pot_check[1]),
        pot_100=float(pot_check[2]),
    )


if __name__ == "__main__":
    import sys
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
