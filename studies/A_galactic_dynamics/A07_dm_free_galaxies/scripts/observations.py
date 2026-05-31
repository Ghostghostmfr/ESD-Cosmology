"""Published velocity-dispersion measurements and canonical Newtonian /
MOND-EFE predictions for the DM-free UDGs NGC 1052-DF2 and DF4.

Sigma values are line-of-sight stellar velocity dispersions in km/s.

Sources:
  DF2:  van Dokkum+2018 (Nature 555, 629);
        Danieli+2019 (ApJ 874, L12);
        Kroupa+2018 (Nature 561, E4)        [MOND no-EFE prediction];
        Famaey+2018 (A&A 619, A86)          [MOND with-EFE prediction].
  DF4:  van Dokkum+2019 (ApJL 874, L5);
        Danieli+2020 (ApJL 895, L4).
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class UDG:
    label:               str
    M_star_msun:         float
    R_half_kpc:          float
    sigma_obs_kms:       float
    sigma_obs_err_kms:   float
    sigma_newton_kms:    float        # published baryon-only prediction
    sigma_mond_noEFE_kms: float       # MOND no-EFE published prediction
    sigma_mond_EFE_kms:  float        # MOND with-EFE published prediction
    host_M_msun:         float
    host_distance_kpc:   float
    reference:           str


SAMPLES = [
    UDG("NGC 1052-DF2", 2.0e8, 2.2, 7.8, 1.7, 7.0, 20.0, 9.0,
        1.0e12, 80.0,  "van Dokkum+2018 / Famaey+2018"),
    UDG("NGC 1052-DF4", 1.5e8, 1.6, 4.2, 1.4, 6.0, 18.0, 8.0,
        1.0e12, 90.0,  "van Dokkum+2019 / Danieli+2020"),
]
