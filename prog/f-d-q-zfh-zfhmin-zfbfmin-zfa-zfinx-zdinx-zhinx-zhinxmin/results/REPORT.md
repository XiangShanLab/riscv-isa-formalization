# Spike / Sail comparison results

The same generated ELF is executed by both models. Numerical result, full `fcsr`, exception code and scratch-memory bytes are compared exactly. FS is reported separately because the architecture permits implementation policies.

| Profile | Cases | Paired cases | Value/flags/trap/memory differences | FS differences | Status |
|---|---:|---:|---:|---:|---|
| rv64-f | 141197 | 141197 | 0 | 0 | compared |
| rv32-f | 141197 | 141197 | 0 | 0 | compared |
| rv64-q | 14971 | 0 | — | — | single_model_only |
| rv32-q | 14909 | 0 | — | — | single_model_only |
| rv64-x | 125655 | 125655 | 0 | 0 | compared |
| rv32-x | 125655 | 125655 | 0 | 0 | compared |
| rv64-hmin | 49529 | 49529 | 0 | 0 | compared |
| rv64-bfmin | 49529 | 49529 | 0 | 0 | compared |
| rv64-xmin | 43621 | 43621 | 0 | 0 | compared |
| rv32-x-edges | 10 | 10 | 0 | 0 | compared |
| rv64-x-edges | 10 | 10 | 0 | 0 | compared |
| rv64-f-privilege | 45 | 45 | 0 | — | directed privilege gates |
| rv64-x-privilege | 120 | 120 | 15 | — | directed privilege gates |
| rv64-f-exceptions | 311 | 311 | 68 | — | directed exceptions |
| rv64-q-exceptions | 34 | 0 | 0 | — | directed exceptions |

Total: 706,793 test cases, 676,879 paired cases, 83 model disagreements; 29,880 Q cases on Spike only.

## Confirmed observations

- Main numerical/transfer/CSR suites and x0/register-pair suites agree between Spike and Sail.
- The 45 FS gate cases agree. The 120 stateen cases have 15 exception-code differences: with mstateen0.FCSR=1, VS denied by hstateen0.FCSR=0 (6 cases), or VU denied by hstateen0.FCSR=0 or sstateen0.FCSR=0 (9 cases). Spike reports 22, the installed Sail reports 2. Cases cover FADD.S, FCLASS.S and FRCSR; normal-mode entry is independently checked using the expected ECALL code.
- The directed exception suite (311 F/D/Zfh cases, 34 Q cases on Spike only) has no expectation differences on either model. mstatus.FS=00 raises illegal instruction for all 37 instruction forms and for read/write/set/clear of fcsr, frm and fflags; FS=01/10/11 with frm 0-4 executes all sampled instructions; access faults on unmapped address 0 raise 5 (load) and 7 (store) for FLH/FLW/FLD/FLQ and the matching stores.
- Misaligned FP accesses are the only exception-suite disagreement: for every non-naturally-aligned address at all 16 low-4-bit offsets, Spike raises cause 4/6 while the installed Sail completes the access (34 load and 34 store cases, 68 of 345). Offset 0 and all naturally aligned offsets agree. Misaligned-access support is implementation-defined, so both behaviours are permitted; the models simply choose differently.
- Reserved rounding modes are observational in this suite. Both models raise illegal instruction for static rm=5/6 and for DYN with frm=5/6/7, and execute with frm 0-4. The delivery leaves reserved modes outside every formula, so these results neither confirm nor contradict a formula.
- The tininess boundary vectors from the testplan now agree with the reference: FCVT.S.D with D bits 0x380fffffe8000000 signals UF+NX in both models, and the reference does the same because the exact value rounds below 2^Emin under unbounded-exponent rounding even though the delivered S value is MIN_NORM.
- The current source inventory has 487 formula labels. All 43 instruction files are represented by generated cases; that is mnemonic/group coverage, not proof that every formula branch was reached.

## Independent numerical interpretation

A separate Python exact-rational model checks arithmetic, FMA, square root, min/max, signs, comparisons, classify, integer and format conversions and round-to-integral operations. Tininess detection uses its own rounding with an unbounded exponent, as the delivery and Unpriv. 25.3.2.6.1 require. This is an independently written interpretation, not a mechanically translated or proved implementation of every Markdown formula. Its disagreements identify cases to inspect; neither simulator is assumed correct merely because of its name.

| Profile | Model | Checked | Differences | Outside numerical model |
|---|---|---:|---:|---:|
| rv64-f | spike | 141197 | 0 | 0 |
| rv64-f | sail | 141197 | 0 | 0 |
| rv32-f | spike | 141197 | 0 | 0 |
| rv32-f | sail | 141197 | 0 | 0 |
| rv64-q | spike | 14971 | 0 | 0 |
| rv32-q | spike | 14909 | 0 | 0 |
| rv64-x | spike | 125655 | 0 | 0 |
| rv64-x | sail | 125655 | 0 | 0 |
| rv32-x | spike | 125655 | 0 | 0 |
| rv32-x | sail | 125655 | 0 | 0 |
| rv64-hmin | spike | 49529 | 0 | 0 |
| rv64-hmin | sail | 49529 | 0 | 0 |
| rv64-bfmin | spike | 49529 | 0 | 0 |
| rv64-bfmin | sail | 49529 | 0 | 0 |
| rv64-xmin | spike | 43621 | 0 | 0 |
| rv64-xmin | sail | 43621 | 0 | 0 |
| rv32-x-edges | spike | 10 | 0 | 0 |
| rv32-x-edges | sail | 10 | 0 | 0 |
| rv64-x-edges | spike | 10 | 0 | 0 |
| rv64-x-edges | sail | 10 | 0 | 0 |

## Evidence and limits

- `environment.json`: simulator/compiler paths, version output and binary SHA-256. The installed Sail binary is a locally patched 0.15 build; the patches alongside it are recorded in README.
- Each profile directory contains build/run commands and exit codes, ELF symbols, raw signatures, decoded JSONL, differences and instruction-group execution counts.
- Q has no configuration in the available Sail schema. Q profiles run on Spike only and are explicitly excluded from paired totals.
- Full IEEE-class cross products are used for binary operations and FMA; ten legal static/dynamic rounding configurations, sticky flags, boundary vectors and deterministic random inputs are included. This is finite sampling, not exhaustive bit-pattern testing.
- Formula labels are inventoried from the current documents, but formula branch reachability is not inferred from mnemonic coverage. No claim of covering all 487 formulas is made.
- Main numerical execution is little-endian M-mode with Bare translation; separate directed suites cover M/HS/U/VS/VU FS and stateen gates, and M-mode FS/CSR illegal-instruction gates, legal frm values, reserved rounding modes, misaligned accesses and unmapped-address access faults. Paging/guest-page faults, trigger breakpoints, PMP-denied regions (an unmapped address is used instead), partial stores and interrupt-time exceptions are not covered.
- Q capability limits, expected extension-denial traps and real successful FP execution are distinguished in coverage files. An illegal instruction is not counted as a successful execution of its arithmetic semantics.
- For Zdinx, Sail 0.15 requires D.supported=true to allocate its 64-bit helper type even while F.supported=false. This is an explicit configuration workaround, not a model source patch. Every x-register record verifies misa.F/D/Q=0. Original failed probes are preserved in capability-probes/.
- A successful Sail run must report HTIF SUCCESS and contain all expected record IDs. Instruction-limit termination is not accepted as completion.
- Original Markdown and simulator sources are not modified.
