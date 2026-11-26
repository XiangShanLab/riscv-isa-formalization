# tools

Two checkers, run with `python3 -I` and the target Markdown as the argument:

```bash
python3 -I tools/check_md.py    <file.md>
python3 -I tools/check_style.py <file.md>
```

Both are idempotent; exit code 0 means the file passes. Every `README.md` and instruction file
under `out/` must pass both.

| Script | What it checks |
|---|---|
| `check_md.py` | formula delimiters, `aligned`/`cases`/`pmatrix` environment balance, table column counts, inline-math delimiters, pipes inside tables |
| `check_style.py` | formula blocks: left side starts with `&`, `\mathrm{instr}` comes last, at most one top-level `\land` per line, right-side shape, `\mathrm{exception}` last, sticky flag updates, no `\wedge`/`\vee` or bit-literal results |
