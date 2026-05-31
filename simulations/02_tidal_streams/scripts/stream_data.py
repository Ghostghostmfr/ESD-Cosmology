"""Published present-day progenitor phase-space and stream parameters.

Three canonical targets are bundled here:

* **GD-1**          — long thin cold stream, dissolved progenitor,
                       Price-Whelan & Bonaca 2018, Bonaca+ 2020.
* **Pal 5**          — disrupting globular cluster, Ibata+ 2017,
                       Bonaca+ 2020.
* **Sagittarius**    — massive (~1e8 Msun) dwarf with multi-wrap stream,
                       Vasiliev+ 2021.

Galactocentric Cartesian frame (x toward Sun, y in disc plane, z toward
NGP). All values converted from heliocentric in the original references
using R0 = 8.122 kpc and the Schoenrich+ 2010 solar peculiar velocity.

For the dissolved GD-1 progenitor we use the centre-of-mass orbit
published in Webb & Bovy 2019 / Bonaca+ 2020. For Pal 5 and Sgr the
present-day cluster position is the literal observation.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class StreamTarget:
    name: str
    galactocentric_xyz_kpc: tuple[float, float, float]
    galactocentric_v_kms: tuple[float, float, float]
    M_prog_msun: float
    age_gyr: float                # how long ago disruption began
    M_prog_describe: str          # "dissolved" / "current cluster" / "intact dwarf"

    @property
    def x0(self) -> NDArray[np.float64]:
        return np.array(self.galactocentric_xyz_kpc, dtype=float)

    @property
    def v0(self) -> NDArray[np.float64]:
        return np.array(self.galactocentric_v_kms, dtype=float)


# Galactocentric frame conversion uses R0 = 8.122 kpc, Sun's peculiar
# velocity (U, V, W) = (11.1, 12.24, 7.25) km/s, V_circ(R0) = 229 km/s,
# Sun's height above mid-plane z_sun = 20.8 pc.
GD1 = StreamTarget(
    name="GD-1",
    galactocentric_xyz_kpc=(-3.41, 13.28, 9.58),
    galactocentric_v_kms=(-200.4, -162.6, 13.9),
    M_prog_msun=2.0e4,
    age_gyr=3.0,
    M_prog_describe="dissolved progenitor (Webb & Bovy 2019 orbit)",
)

PAL5 = StreamTarget(
    name="Pal 5",
    galactocentric_xyz_kpc=(8.16, 0.24, 16.13),
    galactocentric_v_kms=(-44.0, -122.3, -8.7),
    M_prog_msun=1.6e4,
    age_gyr=3.0,
    M_prog_describe="current globular cluster (Ibata+ 2017)",
)

SGR = StreamTarget(
    name="Sagittarius",
    galactocentric_xyz_kpc=(17.5, 2.5, -6.5),
    galactocentric_v_kms=(237.9, -24.3, 209.0),
    M_prog_msun=1.0e8,
    age_gyr=4.0,
    M_prog_describe="intact massive dwarf (Vasiliev+ 2021)",
)

ALL_TARGETS = (GD1, PAL5, SGR)


# ---------------------------------------------------------------------------
# Stream-aligned coordinate frame derived from the orbit itself.
# ---------------------------------------------------------------------------


def stream_frame_from_orbit(
    x_p: NDArray[np.float64], v_p: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Return three orthonormal unit vectors (e1, e2, e3) where

      e3 = L / |L|             (angular-momentum direction; orbit normal)
      e1 = r_hat               (along the present-day progenitor position
                                 from the host centre, projected into the
                                 orbit plane)
      e2 = e3 x e1             (in-plane perpendicular)

    Stream particles can then be projected onto (e1, e2, e3); the
    along-stream coordinate is phi1 = atan2(y_e2, x_e1) in the orbit
    plane, the perpendicular angle is phi2 = arcsin(z_e3 / r).
    """
    L = np.cross(x_p, v_p)
    e3 = L / (np.linalg.norm(L) + 1.0e-30)
    r_hat = x_p / (np.linalg.norm(x_p) + 1.0e-30)
    # Project r_hat into the orbit plane (subtract any component along e3)
    e1 = r_hat - np.dot(r_hat, e3) * e3
    e1 = e1 / (np.linalg.norm(e1) + 1.0e-30)
    e2 = np.cross(e3, e1)
    return e1, e2, e3


def to_stream_coords(
    points_xyz: NDArray[np.float64],
    e1: NDArray[np.float64],
    e2: NDArray[np.float64],
    e3: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Project ``points_xyz`` (..., 3) into the stream frame and return
    (phi1_deg, phi2_deg) — longitude along the orbit, latitude across.
    """
    x1 = points_xyz @ e1
    x2 = points_xyz @ e2
    x3 = points_xyz @ e3
    r = np.sqrt(x1 * x1 + x2 * x2 + x3 * x3)
    phi1 = np.degrees(np.arctan2(x2, x1))
    phi2 = np.degrees(np.arcsin(x3 / np.where(r > 0, r, 1.0)))
    return phi1, phi2
