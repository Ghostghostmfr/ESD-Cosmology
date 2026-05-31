"""Plane-of-satellites literature catalogue."""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class SatellitePlane:
    host: str
    name: str
    rms_thickness_kpc: float
    host_extent_kpc: float
    n_corotating: int
    n_total: int
    lcdm_pvalue: float        # one-sided probability of as-or-more-extreme config
    sigma: float
    reference: str

    @property
    def aspect_ratio(self) -> float:
        return self.rms_thickness_kpc / self.host_extent_kpc

    @property
    def corotation_fraction(self) -> float:
        return self.n_corotating / self.n_total


MW_VPOS = SatellitePlane(
    host="Milky Way",
    name="VPOS",
    rms_thickness_kpc=29.3,
    host_extent_kpc=254.0,
    n_corotating=8,
    n_total=11,
    lcdm_pvalue=9.0e-5,
    sigma=3.92,
    reference="Pawlowski, Pflamm-Altenburg, Kroupa 2012 MNRAS 423 1109",
)

M31_GPOA = SatellitePlane(
    host="M31",
    name="Great Plane of Andromeda",
    rms_thickness_kpc=12.6,
    host_extent_kpc=600.0,
    n_corotating=13,
    n_total=15,
    lcdm_pvalue=2.0e-5,
    sigma=4.10,
    reference="Ibata et al. 2013 Nature 493 62",
)

CEN_A = SatellitePlane(
    host="Centaurus A",
    name="Plane of Cen A satellites",
    rms_thickness_kpc=70.0,
    host_extent_kpc=800.0,
    n_corotating=14,
    n_total=16,
    lcdm_pvalue=1.0e-3,
    sigma=3.30,
    reference="Müller, Pawlowski, Jerjen, Lelli 2018 Science 359 534",
)


def all_planes() -> tuple[SatellitePlane, ...]:
    return (MW_VPOS, M31_GPOA, CEN_A)


def joint_sigma(planes=None) -> float:
    """Stouffer combination of independent per-host sigmas."""
    if planes is None:
        planes = all_planes()
    sigmas = [p.sigma for p in planes]
    return sum(sigmas) / sqrt(len(sigmas))
