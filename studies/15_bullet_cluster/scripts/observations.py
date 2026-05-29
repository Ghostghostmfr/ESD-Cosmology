"""Dissociative cluster merger weak-lensing + X-ray measurements.

Each entry gives the X-ray (gas) mass and weak-lensing total mass
inside a common aperture, plus the spatial offset between the gas
peak and the convergence peak.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Merger:
    label:        str
    aperture_kpc: float
    M_gas:        float        # in 1e13 Msun
    M_gas_err:    float
    M_total:      float        # weak lensing, in 1e13 Msun
    M_total_err:  float
    offset_kpc:   float
    offset_err:   float
    z_cluster:    float
    reference:    str

    @property
    def ratio_obs(self) -> float:
        return self.M_total / self.M_gas

    @property
    def ratio_err(self) -> float:
        # Standard error propagation on a ratio
        return self.ratio_obs * (
            (self.M_total_err / self.M_total)**2 +
            (self.M_gas_err   / self.M_gas)**2
        )**0.5


# Clowe et al. 2006 ApJ 648, L109; Markevitch et al. 2004 ApJ 606, 819
# MACS J0025: Bradac et al. 2008 ApJ 687, 959
# Abell 520:  Jee et al. 2014 ApJ 783, 78  (note: controversial; M/L large)
SAMPLES = [
    Merger("1E 0657-56 (Bullet) East", 250,
           M_gas=5.5,  M_gas_err=0.6,  M_total=35.0, M_total_err=5.0,
           offset_kpc=200, offset_err=30, z_cluster=0.296,
           reference="Clowe+2006 ApJ 648, L109"),
    Merger("1E 0657-56 (Bullet) Main", 250,
           M_gas=11.0, M_gas_err=1.5,  M_total=60.0, M_total_err=10.0,
           offset_kpc=210, offset_err=30, z_cluster=0.296,
           reference="Clowe+2006 ApJ 648, L109"),
    Merger("MACS J0025.4-1222",        300,
           M_gas=2.5,  M_gas_err=0.3,  M_total=15.0, M_total_err=3.0,
           offset_kpc=150, offset_err=40, z_cluster=0.586,
           reference="Bradac+2008 ApJ 687, 959"),
    Merger("Abell 520 (Train Wreck)",  300,
           M_gas=4.5,  M_gas_err=0.5,  M_total=32.0, M_total_err=6.0,
           offset_kpc=480, offset_err=80, z_cluster=0.20,
           reference="Jee+2014 ApJ 783, 78"),
]
