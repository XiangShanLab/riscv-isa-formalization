# {{INSTANCE_TITLE}}

<!-- TEMPLATE: copy to specs/{{INSTANCE_SLUG}}/README.md.
     English only. All shared definitions belong here, not in instruction files.
     Replace every {{...}} placeholder and delete this comment. -->

{{One paragraph of scope: the instruction family, the extensions it depends on, the manual
chapters it comes from, and what is explicitly out of scope.}}

## 1. Formula shape

Every formula has the form

$$
\begin{aligned}
&\text{privileged configuration}\ \land\ \text{extension conditions}\\
&\land\ \text{state}\\
&\land\ \text{operands}\\
&\land\ (\mathrm{instr}=I)
\end{aligned}
\longrightarrow
\{\, \text{destination},\ \text{state},\ \text{flags},\ \mathrm{exception}=\varnothing \,\}
$$

The left-hand groups always appear in this order; a group that does not exist for an
instruction is omitted and the remaining groups keep their relative order. The instruction
conjunct is always last. Formula `.0` is the guard: the extension is unavailable or the
execution configuration is not permitted, nothing is written, and only the corresponding
exception is raised. The right-hand side lists the destination, state writes, sticky-flag
increments, and `exception` last.

## 2. Symbols

Register every symbol before it is used; instruction files must not introduce new ones.

| Symbol | Meaning | Values / form | Source |
|---|---|---|---|
| `{{SYMBOL}}` | {{MEANING}} | {{VALUES}} | {{SOURCE}} |

## 3. Writing rules

1. One formula is one display block with a single `aligned` environment; every left-hand line
   starts with `&` and continuation lines use `&\qquad`.
2. At most one top-level `\land` per line.
3. `\longrightarrow` separates the two sides; the right side is `\{\, … \,\}`.
4. Right-hand order: destination, state, sticky flags, `exception`; `exception` is last.
5. Multi-letter names go in `\mathrm{…}`; single-letter operands are italic.
6. Enumerations are `Name(code)`; sets are `\{…\}`; the empty set is `\varnothing`.
7. Derived symbols are defined once and used by name.
8. Results are domain-canonical values or classes, never hardware bit patterns.
9. Sticky state is updated with `\mathrel{|}=`, never assigned with `=`.
10. Each instruction file lists only the exceptions that instruction itself can raise; fetch
    outcomes are stated once in §7.

## 4. Extensions and conditions

{{Map each mnemonic group to its extension condition, e.g. `impl(Ext)` vs a disjunction.}}

## 5. Operands and values

{{Bit fields, value classes, encodings, write-back model, and any representative operands.}}

## 6. State and flags

{{Which state fields each instruction writes, and how sticky flags are accumulated.}}

## 7. Exceptions and flags

{{Exception codes, their priority order, the fetch chain stated once, and the per-instruction
flag summary.}}

## 8. Instruction files

| File | Mnemonics | Variants | Status |
|---|---|---|---|
| `{{mnemonic}}.md` | `{{MNEMONIC}}` | {{VARIANTS}} | complete |

## 9. Validation

From the repository root:

```bash
python3 -I tools/check_md.py    specs/{{INSTANCE_SLUG}}/README.md
python3 -I tools/check_style.py specs/{{INSTANCE_SLUG}}/README.md
find specs/{{INSTANCE_SLUG}}/instructions -name '*.md' \
  -exec python3 -I tools/check_md.py {} \; \
  -exec python3 -I tools/check_style.py {} \;
```

If the domain has a sticky state other than `fcsr.fflags` or `vxsat`, add
`--sticky-flag <name>` to `check_style.py`.
