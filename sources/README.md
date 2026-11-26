# sources

The two manuals the deliverables cite, each as a PDF and as a plain-text extraction:

| File | Document |
|---|---|
| `riscv-unprivileged.pdf` / `.txt` | The RISC-V Instruction Set Manual, Volume I: Unprivileged Architecture (Version 20260120). Chapters 21–27 (scalar floating point), 25 (BF16), 31 (vector floating point). |
| `riscv-privileged.pdf` / `.txt` | The RISC-V Instruction Set Manual, Volume II: Privileged Architecture (Version 20260120). Floating-point/vector context status, `stateen`, exception priority, H-extension chapters. |

Both documents state that they are released under a Creative Commons Attribution 4.0 International
License (`sources/riscv-unprivileged.txt:810`, `sources/riscv-privileged.txt:262`).

The `.txt` files are the plain-text extractions used for citations. A reference of the form
`sources/riscv-unprivileged.txt:18374` means line 18374 of that file. When a PDF is replaced, its
extraction must be regenerated at the same time, otherwise line-number citations drift.
