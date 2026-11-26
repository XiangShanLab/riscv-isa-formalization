English | [中文](README.zh.md)

# Published instances

Each directory under `specs/` is one **instance**: a self-contained formalization of a family of
RISC-V instructions, produced with the method in [`workflow.md`](../workflow.md) and the skeletons
in [`templates/`](../templates). The framework is not tied to any of them; a new extension family
adds a directory and a row to the table below.

Every instance has the same shape:

```
specs/<instance>/
├── README.md          # all shared definitions: formula shape, symbols, conventions, exceptions
└── instructions/      # one file per mnemonic group, result formulas only
```

| Instance | Scope | Source chapters | Files | Formula blocks | Docs |
|---|---|---|---:|---:|---|
| [`f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/`](f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md) | Scalar floating point: `F`, `D`, `Q`, `Zfh`, `Zfhmin`, `Zfbfmin`, `Zfa`, `Zfinx`, `Zdinx`, `Zhinx`, `Zhinxmin` | Unpriv. 21–27; Priv. FS/SD and `stateen` | 43 | 1504 | [EN](f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md) · [中文](f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.zh.md) (reading aid) |
| [`v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/`](v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md) | Vector floating point: `V` with `Zvfh`, `Zvfhmin`, `Zvfbfmin`, `Zvfbfwma` | Unpriv. 25 and 31; Priv. VS/SD | 34 | 193 | [EN](v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md) |
| [`h-svinval/`](h-svinval/README.md) | `HLV`, `HSV`, `HLVX`, `HFENCE.VVMA`, `HFENCE.GVMA`, `HINVAL.VVMA`, `HINVAL.GVMA` | Priv. 15; Svinval | 5 | 45 | [EN](h-svinval/README.md) |

The Chinese file in the scalar instance is a translation of its English `README.md` for reading;
the English document is canonical.

## Shared conventions

All instances follow the same outer form; the delivery README owns every shared definition.

- One display `aligned` block per formula, left side a conjunction, right side `\{\, … \,\}`.
- Left-hand groups in a fixed order, `\mathrm{instr}=…` last.
- Right-hand order: destination → state writes → sticky flags → `exception` last.
- Formula `.0` is the guard: extension unavailable or execution configuration not permitted;
  it raises the corresponding exception and writes nothing.
- Instruction files contain result formulas only; symbols, formats, value classes and exception
  priorities are defined once in the delivery README.
- Sticky state is updated with `\mathrel{|}=`; results are domain-canonical values or classes,
  never hardware bit patterns.

## Adding an instance

1. Read [`CONTRIBUTING.md`](../CONTRIBUTING.md) and the method in [`workflow.md`](../workflow.md);
   for a non-floating-point family see §11.
2. Copy the skeletons from [`templates/`](../templates) and replace every `{{…}}` placeholder.
3. Write the delivery README first, then the instruction files.
4. Run both checkers on every file and add a row to the table above.

## Validation

From the repository root:

```bash
find specs -name '*.md' -exec python3 -I tools/check_md.py {} \;
find specs -name '*.md' -exec python3 -I tools/check_style.py {} \;
```

`check_style.py` accepts `--sticky-flag <name>` for an instance whose sticky state is not
`fcsr.fflags` or `vxsat`.

## Counting

“Files” counts `*.md` files under `instructions/`; “formula blocks” counts bold `**(…)**`
headers, one per formula. Counts are maintained by hand in this table when an instance is added
or extended.
