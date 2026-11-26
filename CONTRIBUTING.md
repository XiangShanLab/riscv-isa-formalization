English | [中文](CONTRIBUTING.zh.md)

# Contributing

This repository is a framework: `specs/` holds instances produced with it. Adding an extension
family means adding an instance; changing the method means changing `workflow.md`, `templates/`,
or `tools/`.

## What goes where

| Path | Contents |
|---|---|
| `specs/<instance>/README.md` | All shared definitions for that instance: symbols, formats, value classes, state writes, exception priorities |
| `specs/<instance>/instructions/<mnemonic>.md` | Result formulas only, one file per mnemonic group |
| `templates/` | Skeletons and placeholder conventions |
| `sources/` | The ISA manuals (PDF and plain-text extraction) |
| `tools/` | Structural checkers shared by every instance |

## Before writing

1. Read [`workflow.md`](workflow.md) — the method, the formula shape, and §11 for families other
   than floating point.
2. Locate the normative text in `sources/*.txt` first. **Do not add a rule from memory.** Every
   condition, value class, flag and exception must be traceable to a manual line or to IEEE 754.
3. Decide the scope: one mnemonic group per instruction file; operand forms with different state
   behavior get different blocks, and different result categories get different formulas.

## Create an instance

1. Pick a directory name under `specs/` that lists the covered extensions (for example
   `h-svinval` or `v-zvfh-zvfhmin-zvfbfmin-zvfbfwma`).
2. Copy the skeletons from [`templates/`](templates/README.md) and replace every `{{…}}`
   placeholder. `grep -R '{{' specs/*/` must return nothing.
3. Write the delivery README before the instruction files. Register every symbol there; the
   instruction files must not introduce hidden predicates or unregistered names.
4. Add a row to [`specs/README.md`](specs/README.md).

## Writing rules

These are the non-negotiables; the full treatment is in `workflow.md` §2–§5 and the instance
README.

- Left-hand groups in a fixed order, with `\mathrm{instr}=…` last.
- One display `aligned` block per formula; at most one top-level `\land` per line.
- Right side is a set `\{\, … \,\}`: destination → state writes → sticky flags →
  `exception` last.
- Formula `.0` is the guard: extension unavailable or execution configuration not permitted;
  only the corresponding exception is produced.
- Result categories are mutually exclusive and numbered in evaluation order; later formulas do
  not repeat conditions already excluded.
- A disjunction on the left is allowed only when the result does not depend on which disjunct
  holds. Otherwise split the block.
- Results are domain-canonical values or classes, never hardware bit patterns.
- Sticky state is updated with `\mathrel{|}=`, never assigned with `=`.
- Each instruction file lists only the exceptions that instruction itself can raise; the fetch
  chain is stated once in the instance README.

## Language

- Specifications (`specs/**/instructions/*.md`, delivery `README.md`) are English only.
- Framework documents are English canonical with a full `*.zh.md` companion.
- `workflow.md` is the detailed Chinese method, with an English overview at the top.
- A Chinese translation of a delivery README, such as the scalar `README.zh.md`, is a reading aid
  and is not normative.

## Validation

From the repository root, after every edit:

```bash
python3 -I tools/check_md.py    <file.md>
python3 -I tools/check_style.py <file.md>
```

Or over a whole instance:

```bash
find specs/<instance> -name '*.md' \
  -exec python3 -I tools/check_md.py {} \; \
  -exec python3 -I tools/check_style.py {} \;
```

Both must exit 0. The checkers are structural, not semantic; passing them does not prove the
formula matches the manual, and they must not be weakened to accommodate a formula.

## Review checklist

- Every result category is covered, and the blocks are mutually exclusive and ordered.
- Each exception code is reachable in exactly the block that can raise it, and no block lists an
  exception it cannot raise.
- Every symbol is registered in the instance README; every new rule cites the manual.
- No bit-pattern results, hidden predicates, or weakened rounding-mode conditions.
- Index tables, counts and cross-references in the instance README and `specs/README.md` are
  updated.
- `grep -R '{{' specs/*/` is empty and both checkers pass.

## Commits

Keep commits small and logical: one for a new instruction group, one for a README change, one
for a tool change. Do not push without the maintainer's request.
