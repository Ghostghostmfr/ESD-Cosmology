# Study 23 paper notes: NANOGrav 15-yr SGWB

## Scope

This study is a reproduction of the headline results from the NANOGrav 15-year data release concerning the stochastic gravitational-wave background (SGWB). It tests whether the data is consistent with the predictions of General Relativity, which the ESD framework inherits for the gravitational-wave sector (per Study 21).

## Core observational references

1.  **Agazie et al. 2023 (ApJL 951 L8):** "The NANOGrav 15-year Data Set: Evidence for a Gravitational-Wave Background". This is the primary discovery paper.
2.  **Agazie et al. 2023 (ApJ):** "The NANOGrav 15-year Data Set: Characterization of the Gravitational-Wave Background". This paper provides the detailed analysis of the spectral properties and spatial correlations.

## Framework references

1.  **ESD Cosmology Paper 1, Section [TBD]:** The formal derivation showing the GW sector is identical to GR.
2.  **Study 21 (`C02_gravitational_wave_applicability`):** The local audit script that certifies the GW sector derivation, showing that the closure-pool kernel `R(u)` does not apply to propagating tensor modes, resulting in `c_g = c` and no massive-graviton terms.

## Planned extension

- Incorporate data from other pulsar timing arrays (PPTA, EPTA) to form an International Pulsar Timing Array (IPTA) joint analysis.
- Extend the analysis to include constraints on alternative polarizations (scalar, vector) to explicitly show the data's preference for the tensor modes predicted by GR and ESD.
- Investigate potential (but expected to be null) effects from the D-field on pulsar timing noise itself, separate from the GW propagation.
