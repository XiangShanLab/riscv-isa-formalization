# RISC-V Hypervisor Extension Formalization

This directory formalizes the instruction behaviour added by the RISC-V hypervisor extension
(Chapter 15 of the privileged manual): the virtual-machine loads and stores `HLV`, `HSV`, and
`HLVX`, and the hypervisor memory-management fences `HFENCE.VVMA` and `HFENCE.GVMA`. It also
covers `HINVAL.VVMA` and `HINVAL.GVMA`, the two hypervisor instructions provided by the Svinval
extension.

Every instruction file contains only formulas: one formula per distinguishable result category.
All shared material — symbols, privilege rules, address-translation predicates, exception
codes — is defined once in this file. A formula in an instruction file may be read on its own
with only this file as context.

The hypervisor CSRs (`hstatus`, `hgatp`, `vsatp`, `hedeleg`, `hideleg`, `henvcfg`, and the
others) are configuration in these formulas. The generic `Zicsr` instructions that read and write
them are not specific to the hypervisor extension and are not modelled here. Instructions whose
behaviour the hypervisor extension modifies without adding a new encoding — `SRET`, `WFI`,
`SFENCE.VMA`, trap entry and delegation — are also outside this directory.

Each file models the 32-bit SYSTEM encoding of its instruction. Compressed encodings are separate
ISA chapters and are not modelled here.

## 1. Formula shape

Every formula has the form

$$
\text{privileged configuration}\ \land\ \text{extension configuration}\ \land\ \text{memory predicate}\ \land\ \text{variant domain}\ \land\ \mathrm{instr}=I
\ \longrightarrow\
\{\, \text{updates} \,\}.
$$

The left-hand groups always appear in this order; a group that does not exist for an instruction
is empty, and the remaining groups keep their positions. The instruction conjunct is always last.

The first left-hand line of every formula fixes the privileged execution configuration: the
current privilege mode, `hstatus.HU`, or `mstatus.TVM`, whichever the case needs. The extension
configuration is the second group and is always written out: `impl(H)` in every formula, plus
`impl(Svinval)` for `HINVAL`, and their negation in the guard formula 0. The mode names `HS`,
`VS`, and `VU` presuppose the hypervisor extension (Priv. Table 44,
`sources/riscv-privileged.txt:8719-8727`), so when the first line names one of them the
`impl(H)` conjunct repeats what the mode name already implies; it is stated anyway, because no
predicate of a formula may be left implicit (rule 10).
The right-hand side lists, in order: the destination (`rd` or memory), then `exception` last.
No formula assigns `mstatus.FS` and none touches `fcsr.fflags`: no hypervisor instruction writes
floating-point state or a floating-point flag.

Formula 0 of every file is the exception-only configuration: when the extension is unavailable,
the instruction writes nothing and raises `IllegalInstruction(2)`. Formulas 1 and 2 are the
privilege guards of the virtual-machine memory instructions: `V=1` raises
`VirtualInstruction(22)`, and U-mode with `hstatus.HU=0` raises `IllegalInstruction(2)`. In the
fence files, formulas 1–3 cover `V=1`, U-mode, and the `mstatus.TVM` case. A formula's `exception`
field lists only the exceptions the instruction itself can raise, and reads
`\mathrm{exception}=\varnothing` when it can raise none; the instruction-fetch outcomes are common
to every instruction, depend only on `PC`, and are stated once in §6.4 instead of being repeated in
each formula. When a listed code applies, the block's register and memory updates do not occur.

A fence writes no register and no memory. Its right-hand side therefore contains only
`exception`, and its ordering guarantee is stated in the prose of its instruction file.

## 2. Symbols

These are the symbols used in the instruction files and in the shared definitions of this file.
A new symbol must be added here first.

| Symbol | Meaning | Values / form | Source |
|---|---|---|---|
| `Priv` | Current privilege mode | `U`, `S`, `HS`, `M`, `VS`, `VU` (`S` and `HS` name the same mode without and with `H`) | Priv. Table 44 |
| `hstatus.HU` | Enables `HLV`, `HSV`, `HLVX` in U-mode | 0, 1 | Priv. §15.2.1 |
| `hstatus.SPVP` | Selects the effective privilege of a virtual-machine access | 0, 1 | Priv. §15.2.1 |
| `hstatus.GVA` | Trap value is a guest virtual address | 0, 1 | Priv. §15.2.1 |
| `mstatus.TVM` | Trap virtual memory | 0, 1 | Priv. §3.1.6.2 |
| `\mathrm{EPM}` | Effective privilege of a virtual-machine memory access | `VU` if `hstatus.SPVP=0`, `VS` if `hstatus.SPVP=1` | Priv. §15.3.1 |
| `impl(X)` | Extension X is implemented | boolean; X is a manual extension name | Priv. §3.1 |
| `instr` | Instruction being executed | mnemonic with variant suffix | — |
| `T` | Width-variant parameter | `HLV`: `B`, `BU`, `H`, `HU`, `W`, `WU`, `D`; `HSV`: `B`, `H`, `W`, `D`; `HLVX`: `HU`, `WU` | §4.2 |
| `\mathrm{w}(T)` | Access width in bits | 8, 16, 32, 64 | §4.2 |
| `\mathrm{ext}_T(u)` | Register image of a loaded word | piecewise, §4.2 | §4.2 |
| `\mathrm{low}_n(v)` | Low $n$ bits of $v$ | — | — |
| `\mathrm{XLEN}` | Integer register width | 32 or 64 | Unpriv. §1.2 |
| `\mathrm{x}[i]` | Integer register | width `XLEN` | — |
| `rd`, `rs1`, `rs2` | Integer register identifiers | — | — |
| `\mathrm{EA}` | Effective address of the access | `x[rs1]` | Priv. §15.3.1 |
| `\mathrm{PC}` | Address of the instruction being fetched | instruction address | Unpriv. §2.2 |
| `I` | Instruction under consideration in a family-wide file | mnemonic with variant suffix | — |
| `\mathrm{sext}_n`, `\mathrm{zext}_n` | Sign and zero extension to $n$ bits | — | — |
| `\mathrm{mem}[a,w]` | Memory word of $w$ bits at address $a$ | little-endian bit vector | Unpriv. §1.4 |
| `kind` | Access kind of a memory predicate | `load`, `store`, `loadx` | §5.2 |
| `\mathrm{Breakpoint}(\mathrm{EA})` | the environment reports a data breakpoint | boolean | §5.3 |
| `\mathrm{MisalignedPre}(\mathrm{EA},w)` | width-$w$ access misaligned, before translation | boolean | §5.3 |
| `\mathrm{PageFault}(\mathrm{EA},\mathrm{kind})` | VS-stage translation fails with a page fault | boolean | §5.3 |
| `\mathrm{GuestPageFault}(\mathrm{EA},\mathrm{kind})` | G-stage translation fails with a guest-page fault | boolean | §5.3 |
| `\mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{kind})` | translation fails with an access fault | boolean | §5.3 |
| `\mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{kind})` | translated access fails with an access fault | boolean | §5.3 |
| `\mathrm{MisalignedPost}(\mathrm{EA},w)` | width-$w$ access misaligned, after translation | boolean | §5.3 |
| `\mathrm{MemOK}_{\mathrm{kind}}(\mathrm{EA},w)` | the access completes normally | boolean | §5.3 |
| `exception` | Synchronous exception outcome of the instruction itself | `\varnothing` when the block raises none; otherwise `\{X\}` with the block's own code (`IllegalInstruction(2)`, `VirtualInstruction(22)`, a breakpoint, misaligned, page-fault, guest-page-fault, or access-fault code); `\mathrm{walk}`, `\mathrm{phys}`, `\mathrm{data}`, `\mathrm{lowest}` qualify the manual's duplicate rows; instruction-fetch outcomes are not repeated in the formulas | §6.1, §6.4 |
| `\mathrm{walk}`, `\mathrm{phys}`, `\mathrm{data}`, `\mathrm{lowest}` | Origin label on an exception code; a shorthand of this document, not a manual term — the manual identifies these rows only by the descriptions in Table 51 | `data`: data-address breakpoint row (`:10550`), or the final-access row for codes 5 and 7 (`:10556`); `walk`: the address-translation row for codes 1, 5, and 7 (`:10542`, `:10554`); `phys`: the physical-address row for codes 1, 5, and 7 (`:10544`, `:10556`); `lowest`: the second misaligned row (`:10558`); `fetch`, `fetch walk`, and `fetch physical` mark the instruction-fetch rows in §6.4 | Priv. Table 51 |

The extension names used with `impl` are `H` for the hypervisor extension and `Svinval` for the
Svinval extension of Chapter 12.9.

## 3. Writing rules

1. One result formula is one display block with a single `aligned` environment; each left-hand
   line starts with `&`.
2. At most one top-level `\land` per line; `\land` inside parentheses does not count.
3. `\longrightarrow` separates the left and right sides; the right side is `\{\, … \,\}` with
   comma-separated fields.
4. Right-hand order: destination, `exception`; the exception is always last.
5. Multi-letter names go in `\mathrm{}`; single-letter indices and the variant symbol `T` are
   italic.
6. Enumerations are `Name(code)` with no space; sets are `\{…\}`; the empty set is
   `\varnothing`; a singleton is `\{X\}`.
7. Only `\land`, `\lor`, `\neg`, `\longrightarrow`, `\in`, `\notin`, `=`, `\ne`, `\le`, `<`,
   `\ge`, `>` are used as logical notation; no textual connectives.
8. A derived symbol is defined once as `\mathrm{name}=…` and then used as a term; it is not
   expanded inline inside a formula.
9. No table cell contains inline math with a vertical bar.
10. No hidden predicate is allowed. The variant domain, the register-width condition, and every
    privilege condition are written out in each formula.
11. A left-hand disjunction may combine only terms that leave the right-hand side unchanged: if
    any nonempty subset of its disjuncts holds, the block yields the same result. Where the
    outcome depends on which term holds — two mnemonics with different effects, for example —
    the terms are split into separate formulas. The mode disjunctions
    (`\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\lor(\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)`,
    `\mathrm{Priv}=\mathrm{M}\lor(\mathrm{Priv}=\mathrm{HS}\land mstatus.TVM=0)`,
    `\mathrm{Priv}=\mathrm{M}\lor\mathrm{Priv}=\mathrm{HS}`), the variant-domain disjunction
    (`T\in\{\ldots\}\lor\mathrm{XLEN}=64`), and the guard disjunctions over extensions or
    mnemonics all satisfy this: every term leads to the same exception code or to the same
    access.

## 4. Instructions and privilege

### 4.1 Validity

`HLV`, `HSV`, and `HLVX` are valid only in M-mode or HS-mode, or in U-mode when
`hstatus.HU=1` (Priv. §15.3.1, `sources/riscv-privileged.txt:9795-9801`). Executing one when
`V=1` raises `VirtualInstruction(22)`; executing one from U-mode when `hstatus.HU=0` raises
`IllegalInstruction(2)` (`sources/riscv-privileged.txt:9840-9842`).

`HFENCE.VVMA` is valid only in M-mode or HS-mode, and is not affected by `mstatus.TVM` or
`hstatus.VTVM` (`sources/riscv-privileged.txt:9861,9886`). `HFENCE.GVMA` is valid in M-mode
irrespective of `mstatus.TVM`, or in HS-mode when `mstatus.TVM=0`; in HS-mode with
`mstatus.TVM=1` it raises `IllegalInstruction(2)`
(`sources/riscv-privileged.txt:9894-9895,9935-9937`). Both raise
`VirtualInstruction(22)` when `V=1` and `IllegalInstruction(2)` in U-mode.

`HINVAL.VVMA` and `HINVAL.GVMA` require the same permissions and raise the same exceptions as
their `HFENCE` counterparts (Priv. §12.9, `sources/riscv-privileged.txt:8326-8336`). They
require both the hypervisor extension and Svinval: Svinval provides them only when the hypervisor
extension is implemented.

| Instruction | Valid modes | `V=1` | `Priv=U` | HS-mode with `mstatus.TVM=1` |
|---|---|---|---|---|
| `HLV`, `HSV`, `HLVX` | M, HS, U with `hstatus.HU=1` | 22 | 2 when `HU=0`; valid when `HU=1` | valid |
| `HFENCE.VVMA` | M, HS | 22 | 2 | valid |
| `HFENCE.GVMA` | M, HS with `TVM=0` | 22 | 2 | 2 |
| `HINVAL.VVMA` | M, HS | 22 | 2 | valid |
| `HINVAL.GVMA` | M, HS with `TVM=0` | 22 | 2 | 2 |

The codes 2 and 22 in the table are `IllegalInstruction(2)` and `VirtualInstruction(22)`.

### 4.2 Width variants

The variant symbol `T` selects the access width and the way a loaded word is placed in `rd`. The
`HLV` family covers every integer load width; the `HSV` family covers every integer store width;
`HLVX` is designed for emulating instruction fetch and provides only the two unsigned variants.

| Variant | `T` | `w(T)` | Extension | Defined on RV32 |
|---|---|---:|---|---|
| `HLV.B` | `B` | 8 | sign-extend | yes |
| `HLV.BU` | `BU` | 8 | zero-extend | yes |
| `HLV.H` | `H` | 16 | sign-extend | yes |
| `HLV.HU` | `HU` | 16 | zero-extend | yes |
| `HLV.W` | `W` | 32 | sign-extend | yes |
| `HLV.WU` | `WU` | 32 | zero-extend | no |
| `HLV.D` | `D` | 64 | sign-extend | no |
| `HSV.B` | `B` | 8 | — | yes |
| `HSV.H` | `H` | 16 | — | yes |
| `HSV.W` | `W` | 32 | — | yes |
| `HSV.D` | `D` | 64 | — | no |
| `HLVX.HU` | `HU` | 16 | zero-extend | yes |
| `HLVX.WU` | `WU` | 32 | zero-extend | yes |

`HLV.WU`, `HLV.D`, and `HSV.D` are not valid for RV32 (`sources/riscv-privileged.txt:9806-9807`).
`HLVX.WU` is valid for RV32 even though `HLV.WU` is not
(`sources/riscv-privileged.txt:9824-9825`). The extension function is

$$
\mathrm{ext}_T(u)=
\begin{cases}
\mathrm{sext}_{\mathrm{XLEN}}(u), & T\in\{\mathrm{B},\mathrm{H},\mathrm{W},\mathrm{D}\},\\[2pt]
\mathrm{zext}_{\mathrm{XLEN}}(u), & T\in\{\mathrm{BU},\mathrm{HU},\mathrm{WU}\}.
\end{cases}
$$

On RV32 these three variants are not valid instructions, so no formula covers them: the model
covers only configurations in which the mnemonic is defined, just as it covers no reserved
rounding mode in the floating-point document.

### 4.3 Effective privilege and address translation

The explicit memory access of `HLV`, `HSV`, and `HLVX` always acts as though `V=1` and the
nominal privilege mode were `hstatus.SPVP`, regardless of `mstatus.MPRV`
(`sources/riscv-privileged.txt:10042-10044`). The effective privilege mode is therefore

$$
\mathrm{EPM}=
\begin{cases}
\mathrm{VU}, & hstatus.SPVP=0,\\
\mathrm{VS}, & hstatus.SPVP=1.
\end{cases}
$$

Two-stage address translation applies: the VS-stage uses `vsatp`, and the G-stage uses `hgatp`
(`sources/riscv-privileged.txt:9798-9799`). The HS-level `sstatus.SUM` is ignored; when
`\mathrm{EPM}=\mathrm{VS}`, `vsstatus.SUM` applies instead. The HS-level `sstatus.MXR` makes
execute-only pages readable at both stages; `vsstatus.MXR` affects only the VS-stage
(`sources/riscv-privileged.txt:9799-9801,10030-10038`). These permission rules are part of the
predicate assignment of §5.3, not separate conjuncts.

### 4.4 Registers

`HLV` and `HLVX` write `rd`; `HSV` reads `rs2` and writes memory. A write to `x0` is discarded
in full. None of these instructions reads or writes an `f` register and none touches `fcsr`.

## 5. Memory accesses

### 5.1 Effective address

The address is the value of `rs1`; these instructions have no immediate:

$$
\mathrm{EA}=\mathrm{x}[rs1].
$$

A store reads `x[rs2]` and writes its low `w(T)` bits. The model assumes little-endian memory and
that `EA` is not subject to pointer masking. The `HLVX.*` accesses are explicitly exempt from
pointer masking (`sources/riscv-privileged.txt:9832-9837`).

### 5.2 Access kinds

`kind` distinguishes the permissions checked during translation:

| `kind` | Used by | Translation permission |
|---|---|---|
| `load` | `HLV` | read permission |
| `store` | `HSV` | write permission |
| `loadx` | `HLVX` | execute permission in place of read permission at both stages |

For `loadx`, the supervisor physical memory attributes must grant both execute and read
permission. `HLVX` cannot override machine-level physical memory protection, and it raises load
exceptions, not fetch exceptions (`sources/riscv-privileged.txt:9809-9822`).

### 5.3 Predicates

| Predicate | Meaning |
|---|---|
| $\mathrm{Breakpoint}(\mathrm{EA})$ | the environment reports a data breakpoint at `EA` |
| $\mathrm{MisalignedPre}(\mathrm{EA},w)$ | the width-$w$ access is misaligned, as determined before address translation |
| $\mathrm{PageFault}(\mathrm{EA},\mathrm{kind})$ | VS-stage translation fails with a page fault |
| $\mathrm{GuestPageFault}(\mathrm{EA},\mathrm{kind})$ | G-stage translation fails with a guest-page fault |
| $\mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{kind})$ | translation fails with an access fault |
| $\mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{kind})$ | the translated access fails with an access fault |
| $\mathrm{MisalignedPost}(\mathrm{EA},w)$ | the width-$w$ access is misaligned, as determined after translation |
| $\mathrm{MemOK}_{\mathrm{kind}}(\mathrm{EA},w)$ | the access completes normally |

These predicates are environment-dependent: which ones hold, and in which cases misalignment is
checked before or after translation, is a property of the memory system, not of the instruction.
In each instruction file the formulas are ordered and mutually exclusive by convention: a formula
applies when its predicate holds and no earlier predicate does, and the last formula is the
complement of the other seven. Translation of the VS-stage reports a page fault (`PageFault`),
translation of the G-stage reports a guest-page fault (`GuestPageFault`), and PMP/PMA checks
report an access fault (`AccessFaultPre` or `AccessFaultPost`); the instruction files map the
failing stage and the access kind to the exception code of §6.1.

Some predicates are triggered indirectly. The page-table walk reads PTEs with implicit accesses; a
PMA or PMP violation on such a read raises an access fault corresponding to the original access
type, and an invalid PTE raises a page fault, also corresponding to the original access type
(`sources/riscv-privileged.txt:7770-7774`); a guest-page fault can arise from an implicit VS-stage
PTE access (`sources/riscv-privileged.txt:9349-9352`). Misaligned accesses may be decomposed into
multiple memory operations that are checked independently, and one may fault after another has
succeeded (`sources/riscv-privileged.txt:4421-4428`, `4451-4457`). All are reported against the
original instruction through the predicates above.

Store formulas describe the intended full-width write. When an exception is raised, a misaligned
store may already have committed some bytes, so the exception branches leave any partial memory
effect unconstrained (Priv. §3.7.1.3,
`sources/riscv-privileged.txt:4421-4428`). Load formulas likewise describe the full-width read;
the first-fault rule for misaligned or page-crossing accesses is part of the memory system's
predicate assignment.

## 6. Exceptions

### 6.1 Exception codes

| Code | Name |
|---:|---|
| 1 | `InstructionAccessFault` |
| 2 | `IllegalInstruction` |
| 3 | `Breakpoint` |
| 4 | `LoadAddressMisaligned` |
| 5 | `LoadAccessFault` |
| 6 | `StoreAMOAddressMisaligned` |
| 7 | `StoreAMOAccessFault` |
| 12 | `InstructionPageFault` |
| 13 | `LoadPageFault` |
| 15 | `StoreAMOPageFault` |
| 20 | `InstructionGuestPageFault` |
| 21 | `LoadGuestPageFault` |
| 22 | `VirtualInstruction` |
| 23 | `StoreAMOGuestPageFault` |

(Priv. Table 50, `sources/riscv-privileged.txt:10436-10450`.) Codes 1, 3, 12, and, with `V=1`, 20 can be raised
on the instruction fetch of any instruction in this directory; that phase depends only on `PC`, not
on the instruction, so it is stated once in §6.4 and not repeated in the formulas, which list only
the exceptions the instruction itself can raise — or `\varnothing` when it raises none. When a
listed code applies, the block's register and memory fields do not occur.

The exception priority of Table 51 applies (`sources/riscv-privileged.txt:10538-10560`); the
first-encountered rule and the implementation-defined position of misalignment are stated at
`sources/riscv-privileged.txt:3051-3060`. Every code these instructions can raise — directly, on
the instruction fetch, or through an implicit access — is listed with its origin:

| Code | Raised directly | Raised indirectly |
|---|---|---|
| `Breakpoint(3)` | an instruction-address breakpoint at `PC`, highest (`:10540`); or the environment reports a data breakpoint at `EA` | — |
| `InstructionPageFault(12)` | the first-stage translation of `PC` fails (`:10542`) | — |
| `InstructionGuestPageFault(20)` | the G-stage translation of `PC` fails with `V=1` (`:10542`) | — |
| `InstructionAccessFault(1)` | the physical fetch of `PC` fails a PMA or PMP check (`:10544`); or the page-table walk for `PC` fails (`:7770-7771`) | — |
| `IllegalInstruction(2)` | privilege or `hstatus.HU` gate; `mstatus.TVM=1` for `HFENCE.GVMA` and `HINVAL.GVMA` in HS-mode (`:8337-8339`, `:9935-9937`) | — (the encoding is legal; the environment vetoes execution) |
| `VirtualInstruction(22)` | — | `V=1`: an HS-qualified instruction is executed from VS/VU (`:10487`, `:8339-8341`) |
| `LoadAddressMisaligned(4)`, `StoreAMOAddressMisaligned(6)` | `EA` is misaligned, at whichever point the implementation checks it | — (the manual also permits an access fault instead, `:4033-4034`) |
| `LoadPageFault(13)`, `StoreAMOPageFault(15)` | the VS-stage walk fails: invalid or non-permitted PTE, misaligned superpage, or A/D update required under `Svade` (`:7771-7787`) | one part of a decomposed access (`:10286-10292`) |
| `LoadGuestPageFault(21)`, `StoreAMOGuestPageFault(23)` | the G-stage walk fails | an implicit VS-stage PTE access fails (`:9349-9352`); one part of a decomposed access (`:10286-10292`) |
| `LoadAccessFault(5)`, `StoreAMOAccessFault(7)` | the final access fails a PMA or PMP check | a PTE read violates PMA/PMP (`:7770-7771`); a PTE A/D write does (`:7788-7789`); one of several memory operations fails while others succeed (`:4451-4457`) |

`InstructionAddressMisaligned(0)` is not reachable: it is raised by a control-flow instruction whose
target is misaligned, not by the fetch (`:3069-3071`), and none of these instructions is a control
transfer. Environment calls and environment breaks belong to `ECALL` and `EBREAK`, which are not in
scope.

Execution-phase priority chains, highest first:

| Instruction | Priority |
|---|---|
| `HLV`, `HLVX` | `IllegalInstruction(2) > VirtualInstruction(22) > Breakpoint(3, data) > LoadAddressMisaligned(4) > LoadPageFault(13) = LoadGuestPageFault(21) = LoadAccessFault(5, walk) > LoadAccessFault(5, data) > LoadAddressMisaligned(4, lowest)` |
| `HSV` | `IllegalInstruction(2) > VirtualInstruction(22) > Breakpoint(3, data) > StoreAMOAddressMisaligned(6) > StoreAMOPageFault(15) = StoreAMOGuestPageFault(23) = StoreAMOAccessFault(7, walk) > StoreAMOAccessFault(7, data) > StoreAMOAddressMisaligned(6, lowest)` |
| `HFENCE.VVMA`, `HFENCE.GVMA`, `HINVAL.VVMA`, `HINVAL.GVMA` | `IllegalInstruction(2) > VirtualInstruction(22)` |

`=` marks the manual's "first encountered during address translation" group: the walk stops at its
first failure, so those codes never occur together and are tied for priority. Two pairs of codes
appear twice because the manual has two rows for them: 4/6 is "optionally" above the translation
group and "if not higher priority" lowest, and the `MisalignedPre` and `MisalignedPost` formulas
encode the two placements; 5/7 is in the first-encountered group when a walk (PTE read or A/D write)
faults and after translation when the explicit access faults, and the two cannot both occur because
a failed walk performs no access. The instruction-fetch outcomes precede every chain in the table —
`Breakpoint(3, fetch)` highest, then `InstructionPageFault(12) = InstructionGuestPageFault(20) =
InstructionAccessFault(1, fetch walk)`, then `InstructionAccessFault(1, fetch physical)` — and are
described in §6.4 instead of being repeated in it; they come before `IllegalInstruction(2)` because
a fetch fault is raised before the instruction is decoded. `fetch` and `data` label the two origins of code 3, which the manual places at two different
priorities: an instruction-address breakpoint at the top (`:10540`), and a load/store/AMO address
breakpoint below the illegal-instruction and virtual-instruction rows and above the optional
misaligned row (`:10550`), so the data breakpoint outranks both the misaligned check and the
address-translation group. `fetch walk` and `fetch physical` label the two rows of code 1 that the
manual gives for instruction fetch; `walk` and `data` label the data origin; `lowest` labels the
second misaligned row. `HLVX` checks execute permission instead of read permission but raises load
exceptions, not fetch exceptions, for the data access it performs (`:9809-9822`); code 20 arises
only on the fetch of the instruction itself. An instruction file's `exception` field lists, in this
order, the codes its configuration can raise, or `\varnothing` when it raises none; the
instruction-fetch chain holds for every block and is not written out in them.

### 6.2 Virtual instruction

When `V=1`, a hypervisor instruction is HS-qualified but prevented from executing, so the trap is
`VirtualInstruction(22)` rather than `IllegalInstruction(2)`
(`sources/riscv-privileged.txt:10453-10456,10487`). The same code is raised by `HINVAL.VVMA` and
`HINVAL.GVMA` in VS-mode or VU-mode (`sources/riscv-privileged.txt:8331-8333`).

### 6.3 Guest-page faults

On a guest-page fault the trap writes the faulting guest virtual address to `stval`/`mtval` and
zero or the faulting guest physical address shifted right by 2 bits to `htval`/`mtval2`
(Priv. §15.5.2, `sources/riscv-privileged.txt:9344-9360,10100-10110,10279-10296`). For a
breakpoint or memory-access trap of an explicit `HLV`, `HSV`, or `HLVX` access that writes the
guest virtual address to `stval`, `hstatus.GVA=1` while `hstatus.SPV=0`
(`sources/riscv-privileged.txt:8880-8888`). The formulas state the exception only; these
trap-entry CSR writes are not repeated in the right-hand side.

### 6.4 Instruction fetch

Every instruction is fetched before it is decoded, so a fetch fault preempts the instruction
entirely: if the fetch does not complete, the instruction writes no register or memory. The fetch
depends only on `PC`, not on the instruction, so this chain is identical for every instruction and
every block, and it is stated once here rather than repeated in the formulas. It is

$$
\mathrm{Breakpoint}(3,\mathrm{fetch}) > \mathrm{InstructionPageFault}(12)
= \mathrm{InstructionGuestPageFault}(20)
= \mathrm{InstructionAccessFault}(1,\mathrm{walk})
> \mathrm{InstructionAccessFault}(1,\mathrm{phys})
> \text{any execution-phase code of §6.1}.
$$

For a block whose configuration excludes `V=1` the `InstructionGuestPageFault(20)` term is absent.
Every code here precedes `IllegalInstruction(2)` and `VirtualInstruction(22)`, because the fetch
completes before the instruction is decoded, and precedes every data-access code because the access
happens after the instruction executes. The qualifiers
`\mathrm{fetch}`, `\mathrm{walk}`, `\mathrm{phys}`, and `\mathrm{data}` name the manual's two
rows for code 3 and two rows for code 1. Table 51 gives the order
(`sources/riscv-privileged.txt:10540-10544`). If a 16-bit-aligned fetch straddles a page boundary,
both translations belong to this fetch, and a fault in either uses the instruction address `PC`
(`:10286-10292`).

## 7. Instruction files

All instruction files are in `instructions/`; this README stays at the directory root.

| File | Mnemonics | Variants | Status |
|---|---|---|---|
| [hlv.md](instructions/hlv.md) | `HLV.B`, `HLV.BU`, `HLV.H`, `HLV.HU`, `HLV.W`, `HLV.WU`, `HLV.D` | `T` | complete |
| [hsv.md](instructions/hsv.md) | `HSV.B`, `HSV.H`, `HSV.W`, `HSV.D` | `T` | complete |
| [hlvx.md](instructions/hlvx.md) | `HLVX.HU`, `HLVX.WU` | `T` | complete |
| [hfence.md](instructions/hfence.md) | `HFENCE.VVMA`, `HFENCE.GVMA` | — | complete |
| [hinval.md](instructions/hinval.md) | `HINVAL.VVMA`, `HINVAL.GVMA` | — | complete |

## 8. Validation

```bash
python3 -I tools/check_md.py    out/h-svinval/README.md
python3 -I tools/check_style.py out/h-svinval/README.md
python3 -I tools/check_md.py    out/h-svinval/instructions/hlv.md
python3 -I tools/check_style.py out/h-svinval/instructions/hlv.md
```

Run both commands on every file in `instructions/` as well.

Both must pass for this file and for every instruction file before it is marked complete.
