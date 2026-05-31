"""Black-hole scalar quasi-normal-mode (QNM) anchors.

General Relativity is a purely *tensor* (spin-2) theory: a perturbed
Kerr black hole rings down through the tensor QNM spectrum (the
fundamental ell=2, m=2, n=0 "220" mode plus overtones/higher harmonics).
GR predicts NO scalar (spin-0, "breathing") quasi-normal mode in the
emitted radiation -- the no-hair theorem forbids an independently
radiating scalar hair (Berti, Cardoso & Will 2006 PRD 73 064030;
Isi+ 2019 PRL 123 111102).

Scalar-tensor and other extra-field theories generically excite an
additional spin-0 ringdown branch whose amplitude is set by the
scalar charge of the remnant. A massless scalar field on a
Schwarzschild background has a fundamental ell=0 QNM with the
well-known dimensionless eigenfrequency

    M omega_{scalar} ~ 0.1105 - 0.1049 i   (ell=0, n=0),

(Berti, Cardoso & Starinets 2009 CQG 26 163001). Searches for
non-tensorial polarization content and extra ringdown modes in LVK
data find NO statistically significant scalar component
(GWTC-3 tests of GR, Abbott+ 2021 PRD 103 122002; Isi+ 2019).
"""
from __future__ import annotations

G_M3_KG_S2 = 6.67430e-11
C_M_S      = 2.99792458e8
M_SUN_KG   = 1.98892e30

# GR / no-hair result (theorem, no free parameter):
# only tensor (spin-2) modes radiate; the scalar branch is absent.
SCALAR_MODE_AMPLITUDE_GR = 0.0   # scalar/tensor amplitude ratio
SCALAR_CHARGE_GR         = 0.0   # remnant scalar charge

# Dimensionless fundamental scalar (ell=0, n=0) QNM eigenfrequency of a
# Schwarzschild BH for a massless scalar field: M*omega (Berti+ 2009).
M_OMEGA_SCALAR_RE = 0.110455
M_OMEGA_SCALAR_IM = 0.104896

# Representative remnant masses (Msun)
REMNANTS = [
    {"object": "GW150914 remnant", "M_Msun": 62.0, "chi": 0.67},
    {"object": "GW190521 remnant", "M_Msun": 142.0,"chi": 0.72},
    {"object": "GW170814 remnant", "M_Msun": 53.0, "chi": 0.70},
]

# Scalar-mode / non-tensorial-polarization searches:
# "A_scalar_upper" = upper bound on the scalar/tensor amplitude ratio
# (consistent with 0 for GR); "sigma_claim" = reported detection
# significance for a non-tensorial / scalar component after trials.
SCALAR_SEARCHES = [
    {"search": "GW170814 polarization (tensor vs scalar)",
     "A_scalar_upper": 1.0, "sigma_claim": 0.0,
     "ref": "Abbott+ 2017 PRL 119 141101"},
    {"search": "Isi+ 2019 ringdown spectroscopy (GW150914)",
     "A_scalar_upper": 1.0, "sigma_claim": 0.0,
     "ref": "Isi+ 2019 PRL 123 111102"},
    {"search": "GWTC-3 tests of GR (polarizations)",
     "A_scalar_upper": 1.0, "sigma_claim": 0.0,
     "ref": "Abbott+ 2021 PRD 103 122002"},
]

# Theories that DO predict a scalar ringdown branch (the targets this
# null discriminates against).
SCALAR_ALTERNATIVES = [
    {"theory": "scalar-tensor / Brans-Dicke", "A_scalar": "prop. scalar charge",
     "ref": "Berti+ 2006 PRD 73 064030"},
    {"theory": "Einstein-dilaton-Gauss-Bonnet", "A_scalar": "O(alpha_GB/M^2)",
     "ref": "Blazquez-Salcedo+ 2017 PRD 96 064008"},
    {"theory": "massive scalar field (hairy BH)", "A_scalar": "prop. hair",
     "ref": "Herdeiro & Radu 2014 PRL 112 221101"},
]
