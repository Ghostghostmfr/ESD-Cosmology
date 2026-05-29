"""Multi-anchor H_0 catalogue for the Study 08 audit.

Each entry: (mean, sigma, family, reference). Sigmas are 1-sigma
total errors as reported in the primary paper. 'family' partitions:

  cmb           CMB-anchored (Planck-side, naturally ~67-68)
  bao_bbn       BAO + BBN (early-time, no CMB)
  distance      Distance-ladder (SH0ES-side, naturally ~72-74)
  trgb          TRGB (intermediate, depends on calibration)
  lensing       Time-delay strong lensing (independent)
  masers        Megamaser direct
  gw            Gravitational-wave standard sirens
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class H0Anchor:
    name:    str
    H0:      float          # km/s/Mpc
    sigma:   float
    family:  str
    ref:     str


ANCHORS = [
    # ---- CMB-anchored ----
    H0Anchor("Planck 2018 (TT,TE,EE+lowE+lensing)",
             67.36, 0.54, "cmb",
             "Aghanim+ 2020, A&A 641, A6"),
    H0Anchor("ACT-DR4 + WMAP",
             67.6,  1.1,  "cmb",
             "Aiola+ 2020, JCAP 12 047"),
    H0Anchor("ACT-DR6 (lensing combined)",
             68.1,  0.9,  "cmb",
             "Madhavacheril+ 2024, ApJ 962, 113"),
    H0Anchor("SPT-3G TT/TE/EE",
             68.3,  1.5,  "cmb",
             "Balkenhol+ 2023, PRD 108, 023510"),

    # ---- BAO + BBN (early-time, no CMB) ----
    H0Anchor("DESI Y1 BAO + BBN",
             68.5,  0.8,  "bao_bbn",
             "DESI 2024 VI, arXiv:2404.03002"),
    H0Anchor("BOSS+eBOSS BAO + BBN",
             67.4,  1.1,  "bao_bbn",
             "Alam+ 2021, PRD 103, 083533"),

    # ---- Distance ladder (Cepheids) ----
    H0Anchor("SH0ES 2022 (Cepheid-SN1a)",
             73.04, 1.04, "distance",
             "Riess+ 2022, ApJL 934, L7"),
    H0Anchor("SH0ES JWST + HST 2024",
             72.6,  2.0,  "distance",
             "Riess+ 2024, ApJL 962, L17"),

    # ---- TRGB ----
    H0Anchor("CCHP TRGB-JWST",
             69.85, 1.95, "trgb",
             "Freedman+ 2024, arXiv:2408.06153"),
    H0Anchor("EDD TRGB",
             71.5,  1.8,  "trgb",
             "Anand+ 2022, ApJ 932, 15"),

    # ---- Time-delay lensing ----
    H0Anchor("H0LiCOW (TDCOSMO IV)",
             73.3,  1.8,  "lensing",
             "Wong+ 2020, MNRAS 498, 1420"),
    H0Anchor("TDCOSMO + ext (hierarchical)",
             67.4,  3.5,  "lensing",
             "Birrer+ 2020, A&A 643, A165"),

    # ---- Megamasers ----
    H0Anchor("Megamaser Cosmology Project",
             73.9,  3.0,  "masers",
             "Pesce+ 2020, ApJL 891, L1"),

    # ---- Gravitational-wave standard sirens ----
    H0Anchor("GW170817 + EM counterpart",
             70.0,  12.0, "gw",
             "Abbott+ 2017, Nature 551, 85"),
]
