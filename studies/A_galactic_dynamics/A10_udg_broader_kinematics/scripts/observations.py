"""UDG kinematic compilation for Study A10 (beyond DM-free pair)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UDG:
    label:              str
    M_star_msun:        float
    R_half_kpc:         float
    sigma_obs_kms:      float
    sigma_err_kms:      float
    M_host_msun:        float
    r_host_kpc:         float
    dm_class:           str
    reference:          str


# Excluded systems and reasons:
#   - AGC 114905: HI rotating disk; single-component Wolf estimator
#     does not apply (Newton itself over-predicts here with this
#     estimator). The fair test is an HI rotation-curve study under
#     R(u) and belongs in a separate study.
#   - DGSAT I: isolated UDG with no identified host. The EFE-aggregation
#     test (the novelty of this study) has nothing to act on, so
#     including it would not test the framework's broader claim.

SAMPLES = [
    # NGC 1052-DF2 / DF4 cross-check.
    UDG("NGC 1052-DF2",     2.0e8, 2.20,  7.8, 1.7,
        1.0e12, 80.0,   "DM-free", "van Dokkum+ 2018"),
    UDG("NGC 1052-DF4",     1.5e8, 1.60,  4.2, 1.4,
        1.0e12, 90.0,   "DM-free", "van Dokkum+ 2019"),
    # NGC 5846-UDG1 - DM-poor group UDG.
    UDG("NGC 5846-UDG1",    1.1e8, 2.00, 17.0, 2.0,
        2.0e13, 90.0,   "DM-poor", "Forbes+ 2021"),
    # Dragonfly 44 - DM-rich Coma UDG, headline falsifier candidate.
    UDG("Dragonfly 44",     3.0e8, 4.70, 33.0, 3.0,
        1.0e15, 400.0,  "DM-rich", "van Dokkum+ 2019"),
]
