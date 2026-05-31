#!/usr/bin/env python3
"""
Test whether the Ch.3 bridge equation defines a Chameleon-like screening envelope.
Given the framework's density-dependent parameter u:
  u = (A/theta_sat)^2 = (rho/rho_max)^2  (or similar density map)
  R(u) = s / (u^phi + b*u^q + c)

We know:
  s = 16*phi + 1   ~ 26.889
  phi = 1.618
  q = 2*ln(phi)/phi ~ 0.595
  b = phi^6 - 2    ~ 15.944
  c = (4*ln(phi)-1)/phi ~ 0.572

Hypothesis: The effective conformally-coupled background gradient sigma_eta
acts as the source for the D-field response. If the measured beta_m is just
the local tangent of R(u) or effectively suppressed by a related bridge term,
how does it scale from solar system density to cosmological vacuum?
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# Framework Constants
PHI = (1 + math.sqrt(5))/2
Q_EXP = 2 * math.log(PHI) / PHI
B_AMP = PHI**6 - 2.0
C_BATH = (4 * math.log(PHI) - 1) / PHI
S_NORM = 16 * PHI + 1

def R(u):
    """Bridge equation from Master Ch.3"""
    return S_NORM / (u**PHI + B_AMP * u**Q_EXP + C_BATH)

def R_prime(u):
    """Derivative of the bridge equation (local tangent scaling).
    In scalar-tensor theories, the effective coupling beta_eff is often 
    proportional to the derivative of the screening function.
    """
    denom = u**PHI + B_AMP * u**Q_EXP + C_BATH
    d_denom = PHI * u**(PHI - 1) + B_AMP * Q_EXP * u**(Q_EXP - 1)
    return - S_NORM * d_denom / (denom**2)

def main():
    # 5 orders of magnitude difference in density means ~10 orders in u:
    #   if u ~ (rho/rho_max)^2
    # Let's map u logarithmically from 1e-12 (vacuum) up to 1 (max saturation)
    u_vals = np.logspace(-15, 0, 1000)
    R_vals = [R(u) for u in u_vals]
    abs_Rp_vals = [abs(R_prime(u)) for u in u_vals]

    # Look for the scaling exponent n, where beta ~ u^(-n) => d(log Rp)/d(log u)
    log_u = np.log10(u_vals)
    log_Rp = np.log10(abs_Rp_vals)
    n_exponent = -np.gradient(log_Rp, log_u)
    
    # We want to find what the framework's native scaling exponent is
    # at intermediate densities (between c-dominance and saturation).
    # The required chameleon scaling vs mass density was beta ~ rho^-0.25 (route A scoping).
    # If u ~ rho, we need beta ~ u^-0.25.
    # If u ~ rho^2, we need beta ~ (u^0.5)^-0.25 = u^-0.125.
    
    print("BRIDGE EQUATION TANGENT (CHAMELEON COUPLING) SCALING")
    print("=" * 60)
    print("If beta_eff is proportional to |R'(u)|, what exponent does the framework give?")
    
    # Print asymptotic behavior
    print("\n1. Deep Vacuum Asymptote (u -> 0):")
    # Limiting behavior of R'(u) when u is tiny:
    # Denominator ~ c^2. Numerator is dominated by the q-term (u^(q-1)) since q < phi.
    # q - 1 = 0.595 - 1 = -0.405.
    # So |R'(u)| ~ u^(-0.405)
    print(f"   Analytic limit: |R'(u)| ~ u^(q-1) = u^{Q_EXP - 1:.3f}")
    
    print("\n2. Intermediate regime:")
    # Find the maximum of n_exponent
    max_idx = np.argmax(abs_Rp_vals) # max coupling
    print(f"   Max coupling occurs at u = {u_vals[max_idx]:.2e}")
    
    # Let's see the boost factor between a "solar system" u and a "vacuum" u.
    # Suppose u_solar = 1e-4, u_cosmo = 1e-14
    u_solar = 1e-4
    u_cosmo = 1e-14
    
    beta_ratio_p = abs(R_prime(u_cosmo)) / abs(R_prime(u_solar))
    
    print(f"\n3. Test boost between u_solar=1e-4 and u_cosmo=1e-14")
    print(f"   Theoretical requirement from Route A scoping: 17.92x")
    print(f"   Bridge equation tangent boost: {beta_ratio_p:.2f}x")
    
    # What if the density map is different? 
    # What u_solar vs u_cosmo gives a ratio of exactly 17.92?
    target_ratio = 17.92
    print(f"\nLooking for regions where the boost is exactly {target_ratio:.2f}...")
    found = False
    for i in range(len(u_vals)-1):
        for j in range(i+1, len(u_vals)):
            # Force the 5-order of magnitude density gap.
            # If u~rho, u_solar / u_cosmo = 1e5
            if abs((u_vals[j] / u_vals[i]) - 1e5) < 0.1 * 1e5:
                ratio = abs(R_prime(u_vals[i])) / abs(R_prime(u_vals[j]))
                if abs(ratio - target_ratio) < 0.5:
                    print(f"   Found match! u_cosmo={u_vals[i]:.2e}, u_solar={u_vals[j]:.2e}")
                    found = True
                    break
        if found: break

    print("\n(Note: If testing R(u) directly instead of R'(u), the ratio R(u_cosmo)/R(u_solar) -> c/c = 1)")

if __name__ == "__main__":
    main()
