"""Regression tests for the locked constants, identities, inflation
chain, and primordial spectrum. These values appear in published
papers; if any test fails, the code and the published numbers have
drifted apart.
"""

import math

import pytest

from esd_core import (
    A_S_PIVOT,
    ALPHA_S_STAR,
    ALPHA_STAR,
    DELTA_REH,
    F12,
    GAMMA_CHI_GEV,
    K_PIVOT_MPC,
    M_CHI_GEV,
    M_PL_GEV,
    NS_PLANCK_BAND,
    NS_PLANCK_MEAS,
    NS_PLANCK_SIGMA,
    NS_STAR,
    N_E_STAR,
    N_E_TOTAL,
    N_PATH,
    N_PATH_D,
    N_T_STAR,
    OMEGA_B_PRIMARY,
    PHI,
    R_TENSOR,
    Reading,
    S_NORM,
    T_REH_GEV,
    a_zero,
    beta,
    c,
    c2,
    c4,
    gamma_chi_gev,
    identity_B_rhs,
    lambda_D_over_RH,
    ln_phi,
    m_D,
    omega_b,
    omega_b_closure_pool,
    omega_dm,
    omega_dm_from_identity_B,
    omega_lambda,
    omega_matter,
    q,
    t_reh_gev,
)


def approx(expected: float, rel: float = 1e-5):
    return pytest.approx(expected, rel=rel)


# ---------------------------- constants -----------------------------------
def test_phi():
    assert PHI == approx(1.6180339887)


def test_ln_phi():
    assert ln_phi == approx(math.log(PHI))


def test_F12_and_paths():
    assert F12 == 144
    assert N_PATH == 12
    assert N_PATH_D == 4


def test_c():
    assert c == approx(0.5715870660)


def test_c_powers():
    assert c2 == approx(0.326712)
    assert c4 == approx(0.10674, rel=1e-4)


def test_q_bridge():
    # q = 2 ln(phi) / phi = 0.594811
    assert q == approx(0.594811, rel=1e-5)


def test_S_NORM():
    assert S_NORM == approx(16.0 * PHI + 1.0)


def test_beta_and_alpha_star():
    assert beta == approx(math.sqrt(2.0 / 3.0))
    assert ALPHA_STAR == approx(beta)


def test_M_PL_GEV():
    assert M_PL_GEV == 2.435e18


# ---------------------------- Identity A ----------------------------------
def test_identity_A():
    assert omega_lambda() == approx(0.684264)
    assert omega_matter() == approx(0.315736)


# ---------------------------- Identity B ----------------------------------
def test_identity_B_rhs():
    assert identity_B_rhs() == approx(0.847021)


def test_omega_b_closure_pool():
    assert omega_b_closure_pool() == approx(0.050094)


def test_omega_dm_primary():
    assert omega_dm_from_identity_B(OMEGA_B_PRIMARY) == approx(0.265907)


def test_omega_dm_closure_pool():
    assert omega_dm_from_identity_B(omega_b_closure_pool()) == approx(0.265642)


# ---------------------------- Reading dispatcher --------------------------
def test_reading_enum_parse():
    assert Reading.parse("primary") is Reading.PRIMARY
    assert Reading.parse("PRIMARY") is Reading.PRIMARY
    assert Reading.parse("planck") is Reading.PRIMARY
    assert Reading.parse("closure-pool") is Reading.CLOSURE_POOL
    assert Reading.parse("closure_pool") is Reading.CLOSURE_POOL
    assert Reading.parse("cp") is Reading.CLOSURE_POOL


def test_reading_enum_parse_rejects_unknown():
    with pytest.raises(ValueError):
        Reading.parse("planck-2018")


def test_omega_b_dispatch():
    assert omega_b("primary") == OMEGA_B_PRIMARY
    assert omega_b("closure-pool") == approx(0.050094)


def test_omega_dm_dispatch():
    assert omega_dm("primary") == approx(0.265907)
    assert omega_dm("closure-pool") == approx(0.265642)


# ---------------------------- omega_b h^2 ---------------------------------
def test_omega_b_h2_primary_matches_planck():
    h = 0.6736
    omega_b_h2 = 0.04931 * h * h
    assert omega_b_h2 == approx(0.022373, rel=1e-4)


def test_omega_b_h2_closure_pool():
    h = 0.6736
    val = omega_b_closure_pool() * h * h
    assert val == approx(0.022730, rel=1e-4)


# ---------------------------- a_0, m_D, lambda_D --------------------------
def test_a_zero():
    assert a_zero(67.36) == approx(1.2014e-10, rel=1e-3)


def test_m_D_in_per_mpc():
    MPC_M = 3.0857e22
    assert m_D(67.36) * MPC_M == approx(1.3313e-5, rel=1e-3)


def test_lambda_D_over_RH():
    assert lambda_D_over_RH(67.36) == approx(16.88, rel=1e-3)


# ---------------------------- inflation chain -----------------------------
def test_N_E_TOTAL():
    assert N_E_TOTAL == approx(F12 * ln_phi)
    assert N_E_TOTAL == approx(69.295, rel=1e-4)


def test_DELTA_REH():
    assert DELTA_REH == 17.82


def test_N_E_STAR():
    assert N_E_STAR == approx(51.475, rel=1e-4)


def test_M_CHI_GEV():
    assert M_CHI_GEV == 3.336e13


def test_gamma_chi():
    expected = M_CHI_GEV**3 / (24.0 * math.pi * M_PL_GEV**2)
    assert gamma_chi_gev() == approx(expected)
    assert GAMMA_CHI_GEV == approx(83.3, rel=5e-3)


def test_T_reh():
    assert t_reh_gev() == approx(7.69e9, rel=5e-3)
    assert T_REH_GEV == approx(7.69e9, rel=5e-3)


# ---------------------------- primordial spectrum -------------------------
def test_NS_STAR():
    assert NS_STAR == approx(0.9611, rel=1e-3)


def test_R_TENSOR():
    assert R_TENSOR == approx(0.00453, rel=1e-2)


def test_N_T_STAR():
    assert N_T_STAR == approx(-R_TENSOR / 8.0)


def test_ALPHA_S_STAR():
    assert ALPHA_S_STAR == approx(-2.0 / (N_E_STAR ** 2))


def test_planck_anchors():
    assert NS_PLANCK_MEAS == 0.9649
    assert NS_PLANCK_SIGMA == 0.0042
    lo, hi = NS_PLANCK_BAND
    assert lo == approx(NS_PLANCK_MEAS - NS_PLANCK_SIGMA)
    assert hi == approx(NS_PLANCK_MEAS + NS_PLANCK_SIGMA)


def test_NS_STAR_within_planck_1sigma():
    lo, hi = NS_PLANCK_BAND
    assert lo < NS_STAR < hi


def test_A_S_and_k_pivot():
    assert A_S_PIVOT == 2.10e-9
    assert K_PIVOT_MPC == 0.05


# ---------------------------- uppercase alias snapshot --------------------
# Backwards-compatible names used by the ported study scripts.
def test_uppercase_constant_aliases():
    from esd_core import (
        C_CHANNEL,
        LN_PHI,
        OMEGA_B_INPUT,
        OMEGA_B_LOCK,
        OMEGA_DM_FROM_IDB,
        OMEGA_DM_LOCK,
        OMEGA_DM_OVER_B_LOCK,
        OMEGA_LAMBDA_LOCK,
        OMEGA_M_LOCK,
        Q_BRIDGE,
    )

    assert LN_PHI == ln_phi
    assert C_CHANNEL == c
    assert Q_BRIDGE == q
    assert OMEGA_LAMBDA_LOCK == approx(0.684264)
    assert OMEGA_M_LOCK == approx(0.315736)
    assert OMEGA_B_INPUT == OMEGA_B_PRIMARY
    assert OMEGA_DM_FROM_IDB == approx(0.265907)
    assert OMEGA_B_LOCK == approx(0.050094)
    assert OMEGA_DM_LOCK == approx(0.265642)
    assert OMEGA_DM_OVER_B_LOCK == approx(
        (8.0 * math.pi * c4 - 1.0) / (3.0 - 8.0 * math.pi * c4)
    )
