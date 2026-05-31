"""ISL lab-test anchors (Kapner+ 2007; Lee+ 2020; Tan+ 2020)."""
from __future__ import annotations

GRAV_LAB = 9.81  # m/s^2  (Earth surface)

BOUNDS = [
    {"experiment": "Lee+2020 EW",  "lambda_um":  38.0,  "alpha_95":  1.0},
    {"experiment": "Lee+2020 EW",  "lambda_um":  52.0,  "alpha_95":  0.1},
    {"experiment": "Kapner+2007",  "lambda_um":  56.0,  "alpha_95":  0.1},
    {"experiment": "Tan+2020 HUST","lambda_um":  70.0,  "alpha_95":  0.014},
    {"experiment": "Tan+2020 HUST","lambda_um": 480.0,  "alpha_95":  9e-6},
]
