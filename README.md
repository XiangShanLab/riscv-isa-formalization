English | [中文](README.zh.md)

# RISC-V ISA Formalization

A framework for writing **configuration-indexed formal specifications** of RISC-V instructions,
together with the specifications produced with it. The repository is organized around the method,
not around any one instruction family: `specs/` contains instances, and a new extension family is
added as another instance.

Every instruction is written as a set of formulas of the shape

$$
\begin{aligned}
&\text{privilege configuration}\ \land\ \text{extension conditions}\\
&\land\ \text{status fields}\\
&\land\ \text{operands}\\
&\land\ (\mathrm{instr}=I)
\end{aligned}
\longrightarrow
\{\, \text{state changes},\ \mathrm{exception}=\{\ldots\} \,\}
$$

The left-hand side is the execution configuration that makes a particular behavior applicable;
the right-hand side is the resulting register, memory, CSR and flag update, plus the exceptions the
instruction can raise. Different outcomes get different formulas, numbered in evaluation order;
formula `.0` is always the guard for an unavailable extension or a forbidden execution
configuration.

## Framework components

| Component | Role |
|---|---|
| [`workflow.md`](workflow.md) | The method: formula anatomy, the four left-hand groups, the right-hand side, the authoring process, and how to substitute a non-floating-point family (§11) |
| [`templates/`](templates/README.md) | Delivery-README and instruction-file skeletons with placeholder conventions |
| [`specs/`](specs/README.md) | Published instances (see below) |
| [`tools/`](tools/README.md) | Structural and style checkers shared by every instance |
| [`sources/`](sources/README.md) | The ISA manuals the instances cite, as PDF and plain-text extraction |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Scope, authoring steps, writing rules, validation and review checklist |

## Published instances

| Instance | Scope |
|---|---|
| [`specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/`](specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md) | Scalar floating point: `F`, `D`, `Q`, `Zfh`, `Zfhmin`, `Zfbfmin`, `Zfa`, `Zfinx`, `Zdinx`, `Zhinx`, `Zhinxmin` |
| [`specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/`](specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md) | Vector floating point with `Zvfh`, `Zvfhmin`, `Zvfbfmin`, `Zvfbfwma` |
| [`specs/h-svinval/`](specs/h-svinval/README.md) | H-extension `HLV`/`HSV`/`HLVX`, `HFENCE.VVMA`/`HFENCE.GVMA`, Svinval `HINVAL.VVMA`/`HINVAL.GVMA` |

[`specs/README.md`](specs/README.md) is the instance index: scopes, source chapters, file and
formula counts, and the conventions every instance shares.

## Start a new instance

1. Read [`workflow.md`](workflow.md) for the method and [`CONTRIBUTING.md`](CONTRIBUTING.md) for
   the working agreement. For a non-floating-point family, start from §11 of the workflow.
2. Locate the normative text in `sources/*.txt`; do not add rules from memory.
3. Copy the skeletons from [`templates/`](templates/README.md) and replace every `{{…}}`
   placeholder.
4. Write the delivery README first — symbols, formats, value classes, state writes, exception
   priorities — then one instruction file per mnemonic group.
5. Run both checkers on every touched file and add the instance to
   [`specs/README.md`](specs/README.md).

## Shared conventions

- One display `aligned` block per formula, at most one top-level `\land` per line.
- Left-hand groups in a fixed order, `\mathrm{instr}=…` last.
- Right-hand order: destination → state writes → sticky flags → `exception` last.
- Formula `.0` is the guard and writes nothing.
- All shared definitions (symbols, formats, value classes, exception priorities) live in the
  instance README; instruction files contain result formulas only.
- Results are domain-canonical values or classes, never hardware bit patterns.
- Sticky state is updated with `\mathrel{|}=`.

## Validation

Every Markdown file under `specs/` must pass both checkers (exit code 0):

```bash
find specs -name '*.md' -exec python3 -I tools/check_md.py {} \;
find specs -name '*.md' -exec python3 -I tools/check_style.py {} \;
```

`check_md.py` checks formula delimiters, environment balance, table column counts, and inline-math
delimiters. `check_style.py` checks the formula style: one top-level `\land` per line,
`\mathrm{instr}` last on the left, right-hand side ending in `\mathrm{exception}`, sticky-flag
updates, and no `\wedge`/`\vee` or bit-literal results.

## Sources and citation

The instances cite the two RISC-V manuals by line number, e.g.
`sources/riscv-unprivileged.txt:18374`. Both PDFs are publications of RISC-V International,
released under CC BY 4.0; the `.txt` files are the plain-text extractions those line numbers refer
to. [`sources/README.md`](sources/README.md) explains which volume to consult and the citation
convention.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) (or [`CONTRIBUTING.zh.md`](CONTRIBUTING.zh.md)):
scope, authoring steps, writing rules, validation and the review checklist. Specifications are
English-only; framework documents are English canonical with a Chinese companion.
