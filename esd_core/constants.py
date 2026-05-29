"""Locked dimensionless constants of the ESD framework.

These values are derived from phi alone and are not free parameters.
See Ch. 2 (closure pool) and Ch. 3 (channel grammar) of the
Energy-Space-Displacement framework reference
[HigginsonESDFramework2026] for the parent-action derivation.
"""

import math

# ----------------------------- structural ---------------------------------
# Golden ratio.
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Natural log of phi (appears throughout the cascade closures).
ln_phi: float = math.log(PHI)
LN_PHI: float = ln_phi          # uppercase alias for script compatibility

# Fibonacci F_12 - locks the total inflationary e-fold count.
F12: int = 144

# Channel-grammar path counts (Ch. 3).
N_PATH: int = 12     # total channel grammar
N_PATH_D: int = 4    # D-channel paths

# ----------------------------- closure pool -------------------------------
# Channel-floor constant
#   c = (4 ln phi - 1) / phi
# Single dimensionless number that floors every spectator-relational
# channel in the framework.
c: float = (4.0 * ln_phi - 1.0) / PHI
C_CHANNEL: float = c            # uppercase alias for script compatibility

# Bridge exponent
#   q = 2 ln phi / phi
q: float = 2.0 * ln_phi / PHI
Q_BRIDGE: float = q             # uppercase alias for script compatibility

# Normalisation constant (Ch. 3)
#   S_norm = 16 phi + 1
S_NORM: float = 16.0 * PHI + 1.0

# Convenience powers of c.
c2: float = c * c
c4: float = c2 * c2

# Conformal weight of the parent action.
beta: float = math.sqrt(2.0 / 3.0)

# Reduced Planck mass (external SM input - not framework-locked).
M_PL_GEV: float = 2.435e18
