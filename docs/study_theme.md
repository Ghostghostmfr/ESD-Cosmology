# Study Theme Guide

This note keeps the post-Study-22 additions visually and structurally coherent for
public release. It is intentionally simple: every study should feel like part of the
same suite even when the physics scope differs.

## Folder contract

Each new study folder should include:

- `README.md`
- `paper/README.md`
- `requirements.txt`
- `Makefile`
- `scripts/` with one audit entrypoint and one figure entrypoint
- auto-generated `scripts/outputs/`
- auto-generated `figures_generated/`

## README section order

Use this section order unless a study genuinely needs an extra section:

1. title line with study number and short subtitle
2. one-line status block
3. short opening paragraph explaining the study claim
4. `What this study does`
5. `Gates`
6. `Datasets`
7. `Quickstart`
8. `Key outputs`
9. `Scope boundary`

## Tone

- State what is reproduced, what is only scaffolded, and what is deferred.
- Prefer explicit scope boundaries over optimistic placeholders.
- If a study is compressed-summary only, say so directly.
- If a study is a falsifier candidate, say so directly.

## Figures

For compressed-summary and bridge studies:

- use one clean summary figure first
- write both PNG and PDF
- avoid decorative styling that differs strongly between studies
- keep titles in the form `Study NN: ...`
- use the same restrained palette family already used in Studies 22 and 23

## Paper note structure

Each `paper/README.md` should contain:

1. `Scope`
2. `Core observational references`
3. `Framework references`
4. `Planned extension`

## Naming

Use `NN_<probe>` matching the grammar of Studies 01-21: short noun phrase for the
physics being tested, no `_summary` or `_bootstrap` suffix. A numbered study slot
is reserved for new physics or a new likelihood; pure re-projections of existing
anchors or duplicates of an earlier study should be folded back into the
originating study rather than given a new number.
