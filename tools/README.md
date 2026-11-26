# tools

Two checkers, run with `python3 -I` and the target Markdown as the argument:

```bash
python3 -I tools/check_md.py    <file.md>
python3 -I tools/check_style.py <file.md> [--sticky-flag NAME ...]
```

Both are idempotent; exit code 0 means the file passes. Every `README.md` and instruction file
under `specs/` must pass both. The checkers are structural, not semantic: they enforce the formula
shape and notation, not whether the formula matches the manual.

| Script | What it checks |
|---|---|
| `check_md.py` | formula delimiters, `aligned`/`cases`/`pmatrix` environment balance, table column counts, inline-math delimiters, pipes inside tables |
| `check_style.py` | formula blocks: left side starts with `&`, `\mathrm{instr}` comes last, at most one top-level `\land` per line, right-side shape, `\mathrm{exception}` last, sticky flag updates, no `\wedge`/`\vee` or bit-literal results |

`check_style.py` treats `fcsr.fflags` and `vxsat` as sticky state and requires such a field to be
updated with `\mathrel{|}=`. An instance whose domain has another sticky state passes it with
`--sticky-flag <name>`, where `<name>` is the part inside `\mathrm{...}`; the option is repeatable.
