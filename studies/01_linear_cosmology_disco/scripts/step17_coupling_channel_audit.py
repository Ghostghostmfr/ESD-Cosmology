"""
Audit: which channel actually drives inflaton-Higgs preheating in ESD?

The earlier estimate q_0 ~ 10^9 used the BARE conformal coupling g^2 = 2/3
as if the Higgs were Planck-mass. That's wrong. The actual Mathieu/
Whittaker-Hill resonance parameters are set by the *effective mass shift*
in the produced field, which carries m_H^2/M_Pl^2 suppression.

Expand parent action conformal factor around end-of-inflation vev:
  A = exp(beta chi/M_Pl)   with beta = sqrt(2/3)
  A^2 = 1 + 2 beta (chi/M_Pl) + 2 beta^2 (chi/M_Pl)^2 + ...
  A^4 = 1 + 4 beta (chi/M_Pl) + 8 beta^2 (chi/M_Pl)^2 + ...

So the chi-Higgs interaction has:
  Lin-kinetic:  2 beta (chi/M_Pl) |dH|^2       (Whittaker-Hill type, ~cos(omega t))
  Lin-mass:     4 beta (chi/M_Pl) m_H^2 |H|^2  (Whittaker-Hill, ~cos(omega t))
  Quad-kinetic: 2 beta^2 (chi/M_Pl)^2 |dH|^2   (Mathieu, ~cos(2 omega t))
  Quad-mass:    8 beta^2 (chi/M_Pl)^2 m_H^2 |H|^2 (Mathieu, ~cos(2 omega t))

Driving inflaton chi(t) = Phi(t) cos(omega t) with omega = m_chi.
The Higgs eq of motion in the inflaton background:
  ddot(sigma_k) + [omega_H^2(k) + delta_m^2(t)] sigma_k = 0

where delta_m^2(t) collects the time-varying piece from the couplings above.

Linear-in-chi pieces give Whittaker-Hill with drive ~ Phi cos(omega t)
Quad-in-chi pieces give Mathieu with drive ~ Phi^2 cos^2(omega t)
                                            = Phi^2/2 * [1 + cos(2 omega t)]

Mathieu q parameter convention:
  ddot(sigma) + [A - 2q cos(2 omega t)] sigma = 0
  with A = (k^2 + m_H^2)/m_chi^2 and q = drive amplitude / (4 m_chi^2)

For broad resonance we need q >> 1.
"""
import math

phi   = (1 + math.sqrt(5))/2
beta  = math.sqrt(2/3)
beta2 = 2/3

M_Pl  = 2.435e18       # GeV (reduced)
m_chi = 3.336e13       # GeV
m_H   = 125.0          # GeV (Higgs, at low energy; could be O(few) heavier at inflation scale)
Phi_end = 1.063 * M_Pl # Starobinsky end-of-inflation amplitude

print("="*78)
print("ESD chi-Higgs coupling audit: Mathieu/Whittaker-Hill resonance parameters")
print("="*78)
print(f"  beta = sqrt(2/3) = {beta:.6f}")
print(f"  M_Pl  = {M_Pl:.3e} GeV")
print(f"  m_chi = {m_chi:.3e} GeV")
print(f"  m_H   = {m_H:.3e} GeV   (low-energy SM)")
print(f"  Phi_end ~ {Phi_end:.3e} GeV  ({Phi_end/M_Pl:.3f} M_Pl)")
print()

# === QUADRATIC channel (Mathieu, broad-resonance candidate) ===
# Drive: 8 beta^2 (Phi/M_Pl)^2 m_H^2 cos^2(omega t)
# Amplitude of cos(2 omega t) piece: 4 beta^2 (Phi/M_Pl)^2 m_H^2
# Mathieu q = amplitude / (4 m_chi^2) = beta^2 (Phi/M_Pl)^2 m_H^2 / m_chi^2

q_Q = beta2 * (Phi_end/M_Pl)**2 * (m_H/m_chi)**2
print("--- QUADRATIC channel (chi^2 |H|^2 mass coupling) ---")
print(f"  q_Q (Mathieu) = beta^2 (Phi/M_Pl)^2 (m_H/m_chi)^2")
print(f"               = {beta2:.4f} * {(Phi_end/M_Pl)**2:.4f} * {(m_H/m_chi)**2:.3e}")
print(f"               = {q_Q:.3e}")
print(f"  -> q_Q << 1  : NARROW resonance regime")
print(f"  -> Floquet mu_Q ~ q_Q/2 ~ {q_Q/2:.3e}  (negligible)")
print()

# Compare to the kinetic-coupling estimate
# After canonical normalisation the kinetic chi^2 |dH|^2 contributes at order
# (omega_H/m_chi)^2 to the effective mass shift; for resonant modes omega_H ~ m_chi/2
q_Q_kinetic = beta2 * (Phi_end/M_Pl)**2 * (1/4)
print(f"  q_Q (kinetic, resonant mode k~m_chi/2)")
print(f"  upper bound: beta^2 (Phi/M_Pl)^2 / 4 = {q_Q_kinetic:.3e}")
print(f"  -> q_Q (kin) = {q_Q_kinetic:.4f}    <-- BROAD resonance only if this channel is real")
print()

# === LINEAR channel (Whittaker-Hill) ===
# Drive: 4 beta (Phi/M_Pl) m_H^2 cos(omega t)
# Whittaker-Hill 'b' parameter: drive amplitude / (4 m_chi^2)
b_WH = beta * (Phi_end/M_Pl) * (m_H/m_chi)**2
print("--- LINEAR channel (chi |H|^2 mass coupling, Whittaker-Hill) ---")
print(f"  b_L = beta (Phi/M_Pl) (m_H/m_chi)^2")
print(f"      = {beta:.4f} * {Phi_end/M_Pl:.4f} * {(m_H/m_chi)**2:.3e}")
print(f"      = {b_WH:.3e}")
print(f"  -> b_L << 1 : NEGLIGIBLE Whittaker-Hill amplification")
print()

# Kinetic Whittaker-Hill (resonant mode)
b_WH_kinetic = beta * (Phi_end/M_Pl) * (1/2)
print(f"  b_L (kinetic, resonant): beta (Phi/M_Pl) / 2 = {b_WH_kinetic:.4f}")
print(f"  -> O(1) for resonant modes, BUT this is a derivative coupling --")
print(f"     after canonical normalisation it does not contribute a Mathieu-type")
print(f"     mass shift, only a friction-like term that vanishes on time-average.")
print()

# === VERDICT ===
print("="*78)
print("VERDICT")
print("="*78)
print(f"""
Higgs portal preheating in ESD is STRUCTURALLY SUPPRESSED by (m_H/m_chi)^2:

  (m_H/m_chi)^2 = ({m_H}/{m_chi:.1e})^2 = {(m_H/m_chi)**2:.3e}

  Quadratic-mass channel (true Mathieu):  q_Q = {q_Q:.3e}  -> NARROW, mu ~ q/2 ~ 10^-23
  Linear-mass channel (Whittaker-Hill):   b_L = {b_WH:.3e}  -> negligible

The previous q_0 ~ 10^9 estimate was using the BARE conformal coupling g^2 = 2/3
as if the produced field had Planck-scale mass. In reality the produced Higgs is
~10^11 times lighter than the inflaton, so all Mathieu/Whittaker-Hill drive
parameters carry (m_H/m_chi)^2 ~ 10^-23 suppression.

CONCLUSION:
  There is NO significant preheating amplification of inflaton decay in ESD
  through the Higgs portal. The perturbative decay rate is the dominant channel.

Therefore the framework's reheating delay IS set by the perturbative formula
(modulo the textbook coefficient choice), and the previous "preheating
closes reheating in-frame" finding was based on a coupling overestimate.

The PREVIOUSLY-LOCAL point prediction Delta_reh ~ 17.82, n_s ~ 0.9611 is the
honest framework value, NOT the preheating-enhanced n_s ~ 0.9665.

UNLESS the framework contains an additional heavy scalar with mass m_S ~ m_chi
that couples conformally. Check known ESD scalars:
  - Higgs: m_H = 125 GeV   (too light by 10^11)
  - D-field: m_D ~ 1.7e-22 eV (ultralight, too light by 10^33)
  - No other scalars in the closure pool to my knowledge.

So unless ESD reveals another heavy scalar, preheating is NOT active and the
perturbative-only n_s ~ 0.961 IS the framework prediction.
""")

# === Sanity check: what if some heavy partner exists? ===
print("="*78)
print("SENSITIVITY: what if a heavy scalar partner exists?")
print("="*78)
print(f"For broad resonance (q > 1) we need m_S >= m_chi sqrt(1/[beta^2 (Phi/Mpl)^2])")
m_S_threshold = m_chi / math.sqrt(beta2 * (Phi_end/M_Pl)**2)
print(f"  m_S threshold = {m_S_threshold:.3e} GeV  (~ {m_S_threshold/m_chi:.3f} * m_chi)")
print(f"  i.e. any scalar with mass within ~factor 1.5 of m_chi would trigger broad resonance.")
print(f"  ESD has no such scalar in the established closure pool.")
