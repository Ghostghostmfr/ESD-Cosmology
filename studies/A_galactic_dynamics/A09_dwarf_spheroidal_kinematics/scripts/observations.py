"""Milky-Way dwarf-spheroidal compilation for Study A09.

Values are publication-grade compilations; M_*, R_half, sigma_obs are
the standard reference numbers (McConnachie 2012 ARA&A 50, 211 and
references therein), updated for Crater II (Caldwell+ 2017, ApJ 839,
20) and Antlia II (Torrealba+ 2019, MNRAS 488, 2743).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DSph:
    label:           str
    M_star_msun:     float
    R_half_kpc:      float
    sigma_obs_kms:   float
    sigma_err_kms:   float
    D_gc_kpc:        float
    reference:       str


SAMPLES = [
    DSph("Fornax",      4.3e7, 0.71, 11.7, 0.9, 140.0, "Walker+ 2009"),
    DSph("Sculptor",    2.3e6, 0.28,  9.2, 1.4,  86.0, "Walker+ 2009"),
    DSph("Draco",       2.9e5, 0.22,  9.1, 1.2,  82.0, "Walker+ 2009"),
    DSph("Sextans",     4.4e5, 0.69,  7.9, 1.3,  86.0, "Walker+ 2009"),
    DSph("Carina",      3.8e5, 0.25,  6.6, 1.2, 101.0, "Walker+ 2009"),
    DSph("Leo I",       5.5e6, 0.25,  9.2, 1.4, 254.0, "Mateo+ 2008"),
    DSph("Leo II",      7.4e5, 0.18,  6.6, 0.7, 233.0, "Koch+ 2007"),
    DSph("Ursa Minor",  2.9e5, 0.18,  9.5, 1.2,  78.0, "Walker+ 2009"),
    DSph("Crater II",   1.6e5, 1.07,  2.7, 0.3, 117.0, "Caldwell+ 2017"),
    DSph("Antlia II",   8.8e5, 2.80,  5.7, 1.1, 132.0, "Torrealba+ 2019"),
]
