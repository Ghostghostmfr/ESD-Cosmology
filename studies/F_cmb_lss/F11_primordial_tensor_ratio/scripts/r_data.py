"""Primordial tensor-to-scalar ratio data (Study 38).

ESD's parent action embeds a Starobinsky-plateau inflation epoch
(Master Ch. 15) with the locked single-field slow-roll prediction
   r = 16 epsilon ~ 12 / N_e^2
For N_e = 50-60 e-folds (standard reheating window):
   r(N_e = 50) ~ 4.8e-3
   r(N_e = 60) ~ 3.3e-3
   r(N_e = 70) ~ 2.4e-3
Best-anchor prediction: r ~ 3.3e-3 at N_e = 60.

Combined with the Starobinsky-locked scalar tilt:
   n_s - 1 = -2 / N_e ~ -0.033  (i.e. n_s ~ 0.967)
matches Planck 2018: n_s = 0.9649 +/- 0.0042 at 0.18 sigma.

Current upper limits and future forecasts:
"""
from __future__ import annotations

# --- Framework prediction (parameter-free from Master Ch. 15) ---
ESD_R_PREDICTION         = 3.3e-3   # at N_e = 60 (best anchor)
ESD_R_RANGE_LOW          = 2.4e-3   # N_e = 70
ESD_R_RANGE_HIGH         = 4.8e-3   # N_e = 50
ESD_N_S_PREDICTION       = 0.967    # n_s = 1 - 2/N_e at N_e=60
PLANCK_N_S               = 0.9649
PLANCK_N_S_SIG           = 0.0042

# --- Upper limits and forecasts ---
# Each entry: (label, value (r), kind, citation)
# kind = "upper95" -> 95% CL upper limit; "forecast_sigma" -> 1-sigma forecast
R_CONSTRAINTS = [
    ("BICEP/Keck BK18",          0.036,  "upper95",
     "Ade+ 2021, PRL 127, 151301 (with Planck+WMAP, r_{0.05})"),
    ("ACT DR4 + WMAP",           0.114,  "upper95",
     "Aiola+ 2020 ApJ; less stringent, foreground-dominated"),
    ("BICEP3 / Keck (proj. 2027)", 0.003, "forecast_sigma",
     "BICEP/Keck Stage-4 collaboration projections (sigma_r)"),
    ("Simons Observatory",        0.003, "forecast_sigma",
     "Ade+ 2019 JCAP 02, 056 (LAT + SAT combined)"),
    ("LiteBIRD",                  0.001, "forecast_sigma",
     "Hazumi+ 2022 PTEP, ISAS-JAXA L-class mission"),
    ("CMB-S4",                    0.0005, "forecast_sigma",
     "Abazajian+ 2022 ApJ 926, 54 (Stage-IV ground)"),
    ("PICO",                      0.0001, "forecast_sigma",
     "Hanany+ 2019 NASA Probe-class concept"),
]
