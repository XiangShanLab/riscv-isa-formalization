# RISC-V ISA Formalization

Formal, configuration-indexed specifications of RISC-V instructions. Every instruction is written
as a set of formulas of the shape

$$
\text{privilege configuration} \ \land\ \text{extension} \ \land\ \text{status fields} \ \land\ \text{operands} \ \land\ \mathrm{instr}=I
\ \longrightarrow\ \text{results},
$$

where the right-hand side is the set of state changes (registers, memory, CSRs) and exceptions the
instruction produces for that configuration. Different outcomes get different formulas.

## Deliverables

| Directory | Scope | Files | Formulas |
|---|---|---|---|
| `out/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/` | Scalar floating point: `F`, `D`, `Q`, `Zfh`, `Zfhmin`, `Zfbfmin`, `Zfa`, `Zfinx`, `Zdinx`, `Zhinx`, `Zhinxmin` | 43 | 1504 |
| `out/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/` | Vector floating point (`V` with `Zvfh`, `Zvfhmin`, `Zvfbfmin`, `Zvfbfwma`) | 34 | 193 |
| `out/h-svinval/` | H-extension `HLV`/`HSV`/`HLVX`, `HFENCE.VVMA`/`HFENCE.GVMA`, and Svinval `HINVAL.VVMA`/`HINVAL.GVMA` | 5 | 45 |

Each delivery directory contains a `README.md` with the shared definitions (formula shape, symbol
table, conventions, exceptions, instruction index) and an `instructions/` directory with one file
per mnemonic group. Read the delivery README first; it makes the instruction files self-contained.

## Layout

```
.
├── out/               # deliverables (table above)
├── sources/           # ISA manuals: PDFs and plain-text extractions
├── tools/             # Markdown/structure checkers; legacy scripts documented in tools/README.md
├── prog/              # Spike/Sail differential-testing pipeline (generated artifacts untracked)
├── reports/           # ACT4 comparison reports (raw 35 MB diff untracked)
├── workflow.md        # how a family is derived from the manuals, with a worked FADD example
├── README-fp-zh.md    # Chinese translation of the scalar delivery README (reading aid only)
└── README.md          # this file
```

## Validation

Every Markdown file under `out/` must pass both checkers (exit code 0):

```bash
find out -name '*.md' -exec python3 -I tools/check_md.py {} \;
find out -name '*.md' -exec python3 -I tools/check_style.py {} \;
```

`check_md.py` checks formula delimiters, environment balance, table column counts, and inline-math
delimiters. `check_style.py` checks the formula style: one top-level `\land` per line, `\mathrm{instr}`
last on the left, right-hand side ending in `\mathrm{exception}`, sticky flag updates, and no
`\wedge`/`\vee` or bit-literal results.

## Sources

The deliverables cite the two manuals by line number, e.g.
`sources/riscv-unprivileged.txt:18374`. Both PDFs are RISC-V International publications released
under CC BY 4.0; the `.txt` files are the plain-text extractions those line numbers refer to. See
`sources/README.md` for details.

## 中文简介

本仓库把 RISC-V 指令整理为“配置 + 操作数 → 结果”的公式：左端是一次执行所需的特权/扩展/状态/操作数
配置，右端是该指令产生的状态变化与异常；结果不同就拆成不同公式。目前包含标量浮点、向量浮点、
H 扩展与 Svinval 三份交付（见上表），共享定义与写作约定在各交付的 `README.md`，工作流见
`workflow.md`。
