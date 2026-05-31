#!/usr/bin/env python3
"""
EVALUATE-ONLY: Probe the disformal-chameleon gate(delta) from B(D).

Theoretical setup:
In the ESD framework, matter couples to the metric:
    g~_{mu nu} = A^2(D) g_{mu nu} + B(D) d_mu D d_nu D

This produces two types of screening:
  1. Conformal Chameleon (from A^2): D-dependence of the conformal factor 
     drives the field to the minimum of V_eff(D) = V(D) + A(D) * rho.
  2. Disformal Vainshtein/Chameleon (from B): Gradient interactions suppress
     the coupling in regions of high density/field-gradients.

For a static, spherically symmetric local source (like the Sun), the Klein-Gordon
equation for the perturbation delta D = D - D_bg is governed by the effective
coupling. When B(D) is included, the gradient term (B(D) * (nabla D)^2) alters
the kinetic term of the scalar field.

Simplified Model (K-mouflage / Disformal Screening):
Let the field have a kinetic modification: 
    L_kin = -1/2 Z(D, X) P(X) 
    where X = -1/2 (nabla D)^2
In the ESD, the disformal matter coupling induces an effective kinetic term 
modification proportional to exactly B(D) * rho.
    Z_eff ~ 1 + B(D) * rho / M_Pl^2

The effective coupling coupling strength beta_eff scales as:
    beta_eff = beta_bare / sqrt(Z_eff)

We know from the lensing closure constraint (Hubble paper):
    B'(D_0) <dot{D}_0^2> = -4 beta_m
If B(D) is linear, B(D) = B_1 D, and the baseline B_1 is locked to the 
galactic closure.

Let's test what scaling gate(rho_solar)/gate(rho_cosmo) is natively produced 
if the gate is directly inverse to sqrt(Z_eff), i.e.,
    gate(rho) = 1 / sqrt(1 + b_eff * rho)
"""

import math
import numpy as np

def evaluate_disformal_gate(b_eff_range):
    """
    Evaluate the gate ratio gate_cosmo / gate_solar for a range of effective
    b_eff coupling constants.
    
    gate(rho) = 1 / sqrt(1 + b_eff * rho)
    
    rho_cosmo = 1e-29 g/cm^3
    rho_solar = 1e-24 g/cm^3
    """
    rho_cosmo = 1e-29
    rho_solar = 1e-24
    
    print(f"{'b_eff (scaled)':>15} | {'gate_cosmo':>12} | {'gate_solar':>12} | {'Ratio c/s':>10}")
    print("-" * 57)
    
    target_ratio = 10.48
    best_b_eff = None
    best_diff = float('inf')
    
    # We span b_eff from values that make b_eff * rho_solar ~ O(1) to much larger.
    # So b_eff ~ 1e24 to 1e28
    b_effs = np.logspace(22, 28, 1000)
    
    for b_eff in b_effs:
        # Prevent division by zero or negative in sqrt (not possible here since b_eff, rho > 0)
        gate_c = 1.0 / math.sqrt(1.0 + b_eff * rho_cosmo)
        gate_s = 1.0 / math.sqrt(1.0 + b_eff * rho_solar)
        
        ratio = gate_c / gate_s
        
        diff = abs(ratio - target_ratio)
        if diff < best_diff:
            best_diff = diff
            best_b_eff = b_eff
            
        if b_eff in [1e22, 1e23, 1e24, 1e25, 1e26, 1e27, 1e28]:
            print(f"{b_eff:>15.1e} | {gate_c:>12.5e} | {gate_s:>12.5e} | {ratio:>10.3f}")

    print("-" * 57)
    gate_c_best = 1.0 / math.sqrt(1.0 + best_b_eff * rho_cosmo)
    gate_s_best = 1.0 / math.sqrt(1.0 + best_b_eff * rho_solar)
    best_ratio = gate_c_best / gate_s_best
    
    print(f"To hit the TARGET RATIO of 10.48x:")
    print(f"  Requires effective B-coupling b_eff ~ {best_b_eff:.2e}")
    print(f"  At this b_eff:")
    print(f"    Cosmo gate  = {gate_c_best:.4f}  (very close to 1.0, i.e., unscreened vacuum)")
    print(f"    Solar gate  = {gate_s_best:.4e}  (suppressed by the local density)")
    print(f"    Ratio       = {best_ratio:.3f}x")
    print()
    print("Does this b_eff ~ 1e26 (in these units) match the framework's B(D)?")
    print("In natural units, rho_solar ~ 10^-24 g/cm^3 is ~ 10^-42 eV^4.")
    print("The B(D) parameter must provide this suppression.")

if __name__ == "__main__":
    print("============================================================")
    print("SCOPING THE DISFORMAL GATE FUNCTION: gate(rho) from B(D)")
    print("============================================================")
    print("Assume the disformal coupling B(D) induces a kinetic screening:")
    print("  gate(rho) = 1 / sqrt(1 + b_eff * rho)\n")
    evaluate_disformal_gate(None)
