"""Observational constraints used by the Study 06 lock audit.

Every entry is (central, sigma, citation_tag). When the constraint
is asymmetric we report the larger of the two 1-sigma errors so the
pull metric is conservative.

All numbers are direct quotes from the cited primary papers (or, for
H_0, the canonical "team" measurements). Tags are short keys for the
output tables; full citations live in paper/README.md.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Obs:
    central: float
    sigma:   float
    tag:     str


# --- Planck 2018 (Aghanim+ 2020, A&A 641, A6, TT,TE,EE+lowE+lensing) ----
PLANCK = {
    "Omega_m":   Obs(0.3158, 0.0073, "Planck18"),
    "Omega_b":   Obs(0.04930, 0.00060, "Planck18"),
    "Omega_DM":  Obs(0.2650, 0.0070, "Planck18"),
    "Omega_Lambda": Obs(0.6842, 0.0073, "Planck18"),
    "n_s":       Obs(0.9649, 0.0042, "Planck18"),
    "alpha_s":   Obs(-0.0045, 0.0067, "Planck18"),
    "A_s":       Obs(2.105e-9, 0.030e-9, "Planck18"),
    "H_0":       Obs(67.36, 0.54, "Planck18"),
    "S_8":       Obs(0.834, 0.016, "Planck18"),
    "sigma_8":   Obs(0.8120, 0.0073, "Planck18"),
    "omega_b_h2":Obs(0.02237, 0.00015, "Planck18"),
}

# --- KiDS-1000 cosmic shear (Asgari+ 2021, A&A 645, A104) ---------------
KIDS1000 = {
    "S_8":       Obs(0.759, 0.024, "KiDS-1000"),
}

# --- DES Y3 cosmic shear (Amon+/Secco+ 2022, PRD 105, 023514/023515) ---
DESY3 = {
    "S_8":       Obs(0.772, 0.017, "DES-Y3"),
}

# --- SH0ES (Riess+ 2022, ApJL 934, L7) ---------------------------------
SHOES = {
    "H_0":       Obs(73.04, 1.04, "SH0ES"),
}

# --- BBN / post-LUNA primordial D/H (current best inference) -----------
# Pisanti+2021 (JCAP 04 020) and Yeh+2021 (JCAP 03 046) re-derive the
# baryon density from Cooke+2018's D/H abundance using the LUNA-2020
# d(p,gamma)3He cross section (Mossa et al., Nature 587, 210, 2020).
# The pre-LUNA Cooke+2018 value (0.02166) is now ~4.7 sigma low against
# Planck and is superseded by the post-LUNA inference (0.02222) which
# sits within 1 sigma of Planck. We use the post-LUNA value as the
# headline BBN reference and retain Cooke+2018 only as a transparency
# entry for the historical (pre-LUNA) tension breakdown.
BBN_LUNA = {
    "omega_b_h2":Obs(0.02222, 0.00015, "BBN-D/H post-LUNA (Pisanti+/Yeh+ 2021)"),
}
BBN_COOKE = {
    "omega_b_h2":Obs(0.02166, 0.00015, "BBN-D/H Cooke+2018 (pre-LUNA, historical)"),
}

# --- BICEP/Keck 2021 (95% upper limit on tensor-to-scalar) -------------
BICEPKECK = {
    # 95% upper limit r_0.05 < 0.036 -> treat as 1-sigma ~ 0.018
    "r":         Obs(0.0, 0.018, "BICEP/Keck-2021 (95% UL r<0.036)"),
}

# --- McGaugh+2016 canonical RAR a_0 (m s^-2) ---------------------------
MCGAUGH2016 = {
    "a_0":       Obs(1.20e-10, 0.026e-10, "McGaugh+2016"),
}

# Bundled survey catalogues for the audit runner. BBN post-LUNA is the
# headline reference; BBN-Cooke (pre-LUNA) is retained for the historical
# tension decomposition only and is not in the headline survey list.
SURVEYS = {
    "Planck 2018":      PLANCK,
    "KiDS-1000":        KIDS1000,
    "DES Y3":           DESY3,
    "SH0ES":            SHOES,
    "BBN (post-LUNA)":  BBN_LUNA,
    "BICEP/Keck-21":    BICEPKECK,
    "McGaugh+2016":     MCGAUGH2016,
}

# Historical-context survey, reported only in the decomposition footer.
HISTORICAL = {
    "BBN (Cooke+2018, pre-LUNA)": BBN_COOKE,
}
