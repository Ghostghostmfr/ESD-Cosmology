# Paper note — Study A09 (dwarf spheroidal kinematics)

## Scope

Closed-form audit of the locked closure-pool kernel R(u) against
Milky-Way classical dwarf spheroidals (Fornax, Sculptor, Draco,
Sextans, Carina, Leo I, Leo II, Ursa Minor) plus two diffuse
outliers (Crater II, Antlia II). External-field-effect (EFE) is
applied via `u = 4(g_int + g_ext)/a_0`, identical to study A07.

## Core observational references

- McConnachie 2012, AJ 144, 4 (compilation).
- Walker+ 2009, ApJ 704, 1274 (kinematics).
- Caldwell+ 2017, ApJ 839, 20 (Crater II).
- Torrealba+ 2019, MNRAS 488, 2743 (Antlia II).
- Wolf+ 2010, MNRAS 406, 1220 (mass estimator).

## Framework references

- [HigginsonESDFramework2026], closure pool §3, Theorem 1 row C1
  (a_0 lock), EFE convention as in Study A07.

## Planned extension

- Per-star Jeans modelling with R(u) source.
- Anisotropy-profile marginalisation.
- Inclusion of M31 dSph subsystem when proper motions land.
