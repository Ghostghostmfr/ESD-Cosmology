"""Published S_8 measurements: Planck CMB, KiDS-1000, DES-Y3, HSC-Y3."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class S8Measurement:
    label:     str
    S8:        float
    S8_err:    float
    Omega_m:   float          # marginalized
    Omega_m_err: float
    probe:     str
    reference: str

MEASUREMENTS = [
    S8Measurement("Planck 2018 (CMB)",      0.832, 0.013, 0.3158, 0.0073,
                  "CMB",        "Planck Collaboration 2020 (A&A 641 A6)"),
    S8Measurement("KiDS-1000 (3x2pt)",      0.766, 0.017, 0.305,  0.080,
                  "cosmic shear","Heymans+2021 (A&A 646 A140)"),
    S8Measurement("DES-Y3 (3x2pt)",         0.776, 0.017, 0.339,  0.032,
                  "cosmic shear","Abbott+2022 (PRD 105 023520)"),
    S8Measurement("HSC-Y3 (real-space)",    0.776, 0.026, 0.256,  0.044,
                  "cosmic shear","Dalal+2023 (PRD 108 123519)"),
]

def planck():
    return MEASUREMENTS[0]

def weak_lensing():
    return [m for m in MEASUREMENTS if m.probe == "cosmic shear"]
