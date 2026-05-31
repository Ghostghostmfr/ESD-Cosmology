"""CMB isotropic cosmic-birefringence measurements (degrees)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BirefMeasurement:
    name: str
    beta_deg: float
    sigma_deg: float
    reference: str
    notes: str = ""


PLANCK_PR3 = BirefMeasurement(
    name="Planck PR3 (Minami & Komatsu 2020)",
    beta_deg=0.35,
    sigma_deg=0.14,
    reference="Minami & Komatsu 2020, PRL 125 221301 (2011.11254)",
    notes="First detection via miscalibration-marginalising estimator",
)

PLANCK_PR4 = BirefMeasurement(
    name="Planck PR4 NPIPE (Eskilt 2022)",
    beta_deg=0.30,
    sigma_deg=0.11,
    reference="Eskilt 2022, A&A 662 A10 (2201.13347)",
    notes="NPIPE reprocessing, frequency-independence checked",
)

JOINT_PR4_WMAP = BirefMeasurement(
    name="Planck PR4 + WMAP joint (Eskilt & Komatsu 2023)",
    beta_deg=0.342,
    sigma_deg=0.094,
    reference="Eskilt & Komatsu 2023, PRL 130 121301 (2205.13962)",
    notes="Joint analysis, most precise currently published",
)


def all_measurements() -> tuple[BirefMeasurement, ...]:
    return (PLANCK_PR3, PLANCK_PR4, JOINT_PR4_WMAP)


# Forecast precisions for upcoming experiments (deg).
FORECASTS = {
    "Simons Observatory LAT": 0.10,
    "LiteBIRD":               0.05,
    "CMB-S4":                 0.02,
}
