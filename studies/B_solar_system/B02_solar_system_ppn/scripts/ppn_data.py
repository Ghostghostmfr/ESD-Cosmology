"""Solar-system PPN anchors (Study 33)."""

# ---------------- physical constants (SI) ----------------
G_NEWTON_SI = 6.67430e-11
C_LIGHT_SI = 2.99792458e8
A0_MOND_SI = 1.20e-10
M_SUN_KG = 1.98892e30
M_EARTH_KG = 5.9722e24
AU_M = 1.495978707e11

# ---------------- orbital scales ----------------
R_EARTH_ORBIT_M = 1.0 * AU_M
R_MERCURY_ORBIT_M = 0.387 * AU_M
R_CASSINI_CLOSEST_M = 1.6 * 6.9634e8     # 1.6 R_sun (Cassini superior conjunction)
R_MOON_M = 3.844e8

# ---------------- PPN anchors ----------------
# Cassini Shapiro time delay (Bertotti+ 2003, Nature 425, 374):
GAMMA_MINUS_1_CASSINI = 2.1e-5            # |gamma - 1| < 2.3e-5 95% C.L.; central
GAMMA_MINUS_1_CASSINI_SIGMA = 2.3e-5

# Lunar Laser Ranging perihelion precession (Williams+ 2009, IJMPD 18, 1129):
BETA_MINUS_1_LLR = 1.1e-4
BETA_MINUS_1_LLR_SIGMA = 1.1e-4

# Lunar Laser Ranging Nordtvedt parameter eta_N = 4(beta-1) - (gamma-1):
ETA_N_LLR = -2.0e-4
ETA_N_LLR_SIGMA = 7.0e-4                  # Williams+ 2012 update

# Lunar Laser Ranging Gdot/G (Williams+ 2009):
GDOT_OVER_G_LLR_PER_YR = 0.2e-13
GDOT_OVER_G_LLR_SIGMA_PER_YR = 0.7e-13     # central 0.2e-13, |Gdot/G| < 1e-13/yr

# Mercury perihelion (MESSENGER, Park+ 2017):
PERIHELION_SHIFT_MERCURY_ARCSEC_CY = 42.9799
PERIHELION_SHIFT_MERCURY_SIGMA = 0.0009

# ---------------- typical Solar-system gravitational accelerations ----------------
# acceleration at Earth's orbit toward the Sun:
G_EARTH_ORBIT_SI = G_NEWTON_SI * M_SUN_KG / R_EARTH_ORBIT_M ** 2
# acceleration at Cassini closest approach (Shapiro test geometry):
G_CASSINI_SI = G_NEWTON_SI * M_SUN_KG / R_CASSINI_CLOSEST_M ** 2
# Earth's surface gravity:
G_EARTH_SURFACE_SI = 9.81
