"""ESD-modified MW potential -- sub-task D.2.

GR branch  :  full ``MWPotential`` (bulge + disk + NFW halo).
ESD branch :  baryons only (bulge + disk), with each acceleration
              vector dressed by the locked closure-pool kernel

                  a_ESD = a_bary * [ 1 + R(u) ],
                  u     = 4 |a_bary| / a0,
                  R(u)  = s / [ u^p + b u^q + c ],  (Study 05).

The applicability gate from sub-task 1.2 is structurally satisfied
here: a stellar stream + the Milky Way is a bound subsystem in a
spectator background (the cosmological dark sector + outer halo of
neighbouring systems), so axiom (A1) of Study 19 holds and R(u) is
admissible everywhere along the stream. We therefore do not apply
the cosmological delta-gate; gate == 1.

Closure constants come from ``esd_core`` (locked across all studies).
The kernel itself is re-imported from sim 01's
``esd_modification`` to guarantee bit-identical behaviour with the
N-body branch.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

# Import the locked R(u) kernel from sim 01 by absolute path so this
# module is independent of the Python path layout.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "01_dfield_nbody", "scripts"))
if _SIM01 not in sys.path:
    sys.path.insert(0, _SIM01)
from esd_modification import R_kernel, u_of_gN, A0_SI       # noqa: E402

from mw_potential import (
    MWPotential, HernquistBulge, MiyamotoNagaiDisk, DEFAULT_MW,
    R0_KPC, V_CIRC_R0_KMS, G_GAL,
)


# Unit conversion: 1 (km/s)^2 / kpc -> m/s^2
KMS2_PER_KPC_TO_MS2: float = (1.0e3) ** 2 / 3.0857e19   # 3.241e-14


# ---------------------------------------------------------------------------
# ESD MW potential (baryons only + R(u) dressing)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ESDMWPotential:
    """Baryons-only MW (bulge + disk) with dressed acceleration."""
    bulge: HernquistBulge = HernquistBulge()
    disk: MiyamotoNagaiDisk = MiyamotoNagaiDisk()
    a0_si: float = A0_SI

    def _bary_accel_cart(self, xyz: NDArray[np.float64]) -> NDArray[np.float64]:
        x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
        R = np.sqrt(x * x + y * y)
        r = np.sqrt(R * R + z * z)
        sph = self.bulge.accel_spherical(r)
        rsafe = np.where(r > 0, r, 1.0)
        ax = -sph * x / rsafe
        ay = -sph * y / rsafe
        az = -sph * z / rsafe
        a_R, a_z = self.disk.accel(R, z)
        Rsafe = np.where(R > 0, R, 1.0)
        ax = ax + a_R * x / Rsafe
        ay = ay + a_R * y / Rsafe
        az = az + a_z
        return np.stack([ax, ay, az], axis=1)

    def accel_cart(self, xyz: NDArray[np.float64]) -> NDArray[np.float64]:
        a_bary = self._bary_accel_cart(xyz)
        a_mag_gal = np.linalg.norm(a_bary, axis=1)               # (km/s)^2/kpc
        a_mag_si = a_mag_gal * KMS2_PER_KPC_TO_MS2               # m/s^2
        u = u_of_gN(a_mag_si, a0=self.a0_si)
        boost = 1.0 + R_kernel(u)                                # scalar per particle
        return a_bary * boost[:, None]

    def v_circ(self, R: NDArray[np.float64]) -> NDArray[np.float64]:
        """Mid-plane circular speed under the dressed potential."""
        xyz = np.zeros((R.size, 3))
        xyz[:, 0] = R
        a = self.accel_cart(xyz)
        a_R_in = -a[:, 0]                # inward radial in mid-plane
        a_R_in = np.where(a_R_in > 0, a_R_in, np.nan)
        return np.sqrt(a_R_in * R)


DEFAULT_ESD_MW = ESDMWPotential()


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test(verbose: bool = True) -> dict:
    mw_gr = DEFAULT_MW
    mw_esd = DEFAULT_ESD_MW

    # (1) ESD branch v_circ(R0) within ~30 km/s of observed.
    R0 = np.array([R0_KPC])
    vc_esd = float(mw_esd.v_circ(R0)[0])
    vc_ok = (V_CIRC_R0_KMS - 30.0) < vc_esd < (V_CIRC_R0_KMS + 30.0)

    # (2) RAR-style convergence at outer halo (R > 30 kpc): GR and ESD
    # rotation curves agree to within 15% (Study 05 reproduces RAR
    # closer than that on disk-galaxy fits; the MW is more bulge-heavy
    # so we allow a wider tolerance).
    R_out = np.linspace(30.0, 80.0, 6)
    vc_gr_out = mw_gr.v_circ(R_out)
    vc_esd_out = mw_esd.v_circ(R_out)
    rel_out = np.max(np.abs(vc_esd_out - vc_gr_out) / vc_gr_out)
    out_ok = rel_out < 0.15

    # (3) ESD reduces to baryonic Newtonian in the high-acceleration
    # limit: at the centre of the bulge u -> large, R(u) -> 0.
    R_inner = np.array([0.05])
    xyz = np.zeros((1, 3)); xyz[0, 0] = R_inner[0]
    a_esd = mw_esd.accel_cart(xyz)[0]
    a_bary = mw_esd._bary_accel_cart(xyz)[0]
    inner_boost = np.linalg.norm(a_esd) / np.linalg.norm(a_bary)
    inner_ok = (inner_boost - 1.0) < 0.05            # < 5% extra

    # (4) Cross-check: u at R0 should match the analytic calculation.
    a_bary_R0_gal = math.sqrt(
        mw_esd.bulge.v_circ2(R0)[0] + mw_esd.disk.v_circ2(R0)[0]
    ) ** 2 / R0_KPC                                  # (km/s)^2/kpc
    a_bary_R0_si = a_bary_R0_gal * KMS2_PER_KPC_TO_MS2
    u_R0 = 4.0 * a_bary_R0_si / A0_SI
    boost_R0 = 1.0 + float(R_kernel(np.array([u_R0]))[0])
    vc_R0_check = math.sqrt(boost_R0 * a_bary_R0_gal * R0_KPC)
    check_ok = abs(vc_R0_check - vc_esd) < 0.5       # km/s

    all_ok = vc_ok and out_ok and inner_ok and check_ok

    if verbose:
        print(f"[esd-mw] v_circ_GR (R0)             = "
              f"{float(mw_gr.v_circ(R0)[0]):7.2f} km/s")
        print(f"[esd-mw] v_circ_ESD(R0)             = {vc_esd:7.2f} km/s   "
              f"(target {V_CIRC_R0_KMS} +/- 30)")
        print(f"[esd-mw] u(R0)                      = {u_R0:7.4f}")
        print(f"[esd-mw] boost(R0)                  = 1 + R = {boost_R0:7.4f}")
        print(f"[esd-mw] outer-halo max |ESD-GR|/GR = {rel_out:7.4f}  (< 0.15)")
        print(f"[esd-mw] inner-bulge boost - 1      = "
              f"{inner_boost-1.0:.3e}  (< 0.05)")
        print(f"[esd-mw] v_circ analytic vs measured= "
              f"{vc_R0_check:7.2f} vs {vc_esd:7.2f}")
        print(f"[esd-mw] R(u=1000)                  = "
              f"{float(R_kernel(np.array([1000.0]))[0]):.3e}")
        print(f"[esd-mw] {'PASS' if all_ok else 'FAIL'}")

    return dict(
        passed=bool(all_ok), v_circ_esd=vc_esd, u_R0=u_R0,
        boost_R0=boost_R0, rel_out=rel_out,
        inner_boost=inner_boost,
    )


if __name__ == "__main__":
    res = self_test(verbose=True)
    sys.exit(0 if res["passed"] else 1)
