English | [中文](README.zh.md)

# templates

Skeletons for a new instance. They contain structure and conventions only — no instruction
semantics. Copy them, replace every `{{…}}` placeholder, and fill in the manual-derived content.

| File | Use |
|---|---|
| `delivery-README.md` | Copy to `specs/<instance>/README.md`; owns all shared definitions |
| `instruction.md` | Copy to `specs/<instance>/instructions/<mnemonic>.md`, once per mnemonic group |

## Placeholders

| Placeholder | Meaning |
|---|---|
| `{{INSTANCE_TITLE}}` | Human-readable title of the instance |
| `{{INSTANCE_SLUG}}` | Directory name under `specs/` |
| `{{MNEMONIC}}` | Instruction mnemonic group, written as in formulas (`\mathrm{FADD}`) |
| `{{EXT}}` | Extension condition, e.g. `\mathrm{Ext}(F)` or `Zfhmin` |
| `{{UNSUPPORTED_CONFIGURATION}}` | Execution configurations that make the instruction illegal |
| `{{ONE_LINE_DESCRIPTION}}`, `{{RESULT_CATEGORY}}`, `{{VARIANTS}}` | Heading and index-table text |
| `{{SYMBOL}}`, `{{MEANING}}`, `{{VALUES}}`, `{{SOURCE}}` | One row of the instance symbol table |
| `{{PRIVILEGE_CONFIGURATION}}` | Privilege-mode conjunction for one result category |
| `{{STATE_CONDITION}}`, `{{OPERAND_CONDITION}}` | Status and operand conditions |
| `{{DESTINATION}}`, `{{RESULT}}` | Destination register/CSR/memory and its new value form |

## Start an instance

```bash
mkdir -p specs/{{INSTANCE_SLUG}}/instructions
cp templates/delivery-README.md specs/{{INSTANCE_SLUG}}/README.md
cp templates/instruction.md     specs/{{INSTANCE_SLUG}}/instructions/{{mnemonic}}.md
grep -R '{{' specs/*/   # must produce no output after editing
```

Then follow [`CONTRIBUTING.md`](../CONTRIBUTING.md):

1. Write the delivery README first — symbols, formats, value classes, state writes, exception
   priorities. Every symbol used later must be registered there.
2. Write one instruction file per mnemonic group; start with the `.0` guard block, then the result
   categories in evaluation order.
3. Run both checkers on every touched file.
4. Add the instance to the table in [`specs/README.md`](../specs/README.md).

## Rules that the skeletons assume

- One display `aligned` block per formula; every left-hand line starts with `&`.
- At most one top-level `\land` per line; `\mathrm{instr}=…` is the last conjunct.
- Right side is `\{\, … \,\}`, with `\mathrm{exception}` last.
- Sticky state is updated with `\mathrel{|}=`.
- Instruction files contain result formulas only; shared definitions live in the delivery README.
- Specs are English only; the Chinese companion for this directory is [`README.zh.md`](README.zh.md).

The two skeletons are checker-clean as written: `python3 -I tools/check_md.py` and
`python3 -I tools/check_style.py` pass on them, so a copied file starts from a valid structure.
Once placeholders are replaced with instance content, they are validated as part of `specs/`.
