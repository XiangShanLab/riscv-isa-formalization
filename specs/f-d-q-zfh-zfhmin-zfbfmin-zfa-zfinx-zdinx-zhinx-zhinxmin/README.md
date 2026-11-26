# RISC-V Scalar Floating-Point Formalization

This directory formalizes the complete scalar floating-point part of the RISC-V instruction set
manual: Chapter 21 (`F`), Chapter 22 (`D`), Chapter 23 (`Q`), Chapter 24 (`Zfh`/`Zfhmin`),
Chapter 25 (`Zfbfmin`, scalar BF16), Chapter 26 (`Zfa`), and Chapter 27
(`Zfinx`/`Zdinx`/`Zhinx`/`Zhinxmin`). It covers loads, stores, arithmetic, sign injection,
minimum/maximum, comparison, classification, conversion, moves, the floating-point CSR
instructions, and the integer-register forms.

Every instruction file contains only formulas: one formula per distinguishable result category.
All shared material — symbols, formats, operand classes, rounding rules, status rules, exception
codes — is defined once in this file. A formula in an instruction file may be read on its own with
only this file as context.

Each file models the 32-bit encoding of its instruction. Compressed encodings (`C.FLW`,
`C.FSW`, and the other `C.*` forms) are separate ISA chapters and are not modelled here.

## 1. Formula shape

Every formula has the form

$$
\text{privileged configuration}\ \land\ \text{extension configuration}\ \land\ \text{floating-point CSR}\ \land\ \text{operands}\ \land\ \mathrm{instr}=I
\ \longrightarrow\
\{\, \text{updates} \,\}.
$$

The left-hand groups always appear in this order; a group that does not exist for an instruction
is empty, and the remaining groups keep their positions. The instruction conjunct is always last.

The first left-hand line of every formula fixes the privileged execution configuration, and the
right-hand side lists, in order: the destination (`fd`, `rd`, memory, or CSR), the `FS` writes
of §6.2 when floating-point state changes, the sticky
flag increment `fcsr.fflags \mathrel{|}= S`, and `exception` last.

Formula 0 of every instruction is the exception-only configuration: when the extension is
unavailable or the effective `FS` is Off, the instruction writes nothing and raises
`IllegalInstruction(2)`. In `zfinx.md` the `FS` term is replaced by the `stateen` gate, and a second
guard covers the VS/VU case that raises `VirtualInstruction(22)`. Loads and stores have the same
formula 0 before their address-exception formulas. A formula's `exception` field lists only the
exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it can
raise none — the ordinary arithmetic, CSR, and register-move paths. Outcomes that belong to the
instruction fetch are common to every instruction, depend only on `PC`, and are stated once in
§7.1.1 and §7.1.2 instead of being repeated in each formula. When a listed code applies, the block's
register, `FS`, memory, and flag updates do not occur.

In the `f`-register files every result category appears three times, once per privileged
configuration, and the first left-hand line of each copy fixes that configuration. Whether the
hypervisor extension `H` is implemented decides which mode names exist (Priv. Table 1,
`sources/riscv-privileged.txt:748-752`, and Table 44, `sources/riscv-privileged.txt:8719-8727`):

| Privilege line | Configuration |
|---|---|
| `¬impl(H) ∧ Priv∈{M,S,U}` | no hypervisor extension: the supervisor mode is `S` |
| `impl(H) ∧ Priv∈{M,HS,U}` | hypervisor extension, `V=0`: the supervisor mode is `HS` |
| `impl(H) ∧ (Priv∈{VS,VU} ∧ vsstatus.FS∈{1,2,3} ∧ sstatus.FS∈{1,2,3})` | hypervisor extension, `V=1`: a guest runs in `VS` or `VU` |

In the first two configurations the only floating-point gate is the later `mstatus.FS` conjunct. In
the third, both the guest field and the HS-level field must be enabled, and because `sstatus.FS` is
`mstatus.FS`, the later `mstatus.FS` conjunct is that same field. Because each block fixes one
configuration, its right-hand side carries only that configuration's `FS` writes. Together with the
`mstatus.FS` conjunct the three lines exhaust the negation of formula 0's privilege and `FS`
disjuncts, so every privileged configuration either enters a result block or raises
`IllegalInstruction(2)`.

## 2. Symbols

These are the only symbols used in the instruction files. A new symbol must be added here first.

| Symbol | Meaning | Values / form | Source |
|---|---|---|---|
| `Priv` | Current privilege mode | `U`, `S`, `HS`, `M`, `VS`, `VU` | Priv. Tables 1 and 44 |
| `mstatus.FS` | Floating-point state, M/HS/U view | `Off(0)`, `Initial(1)`, `Clean(2)`, `Dirty(3)` | Priv. Table 13 |
| `sstatus.FS` | HS-level view; the same field as `mstatus.FS` | same | Priv. §15.2.11 |
| `vsstatus.FS` | Floating-point state in VS/VU | same | Priv. Table 13 |
| `misa.F` | F bit of `misa` | 0, 1 | Priv. §3.1.1 |
| `\mathrm{stateen}` | The stateen CSRs are implemented | boolean | Priv. §4.2 |
| `mstateen0.FCSR` | `fcsr` access bit, machine view; controls every mode below M | 0, 1 | Priv. §4.2 |
| `hstateen0.FCSR` | `fcsr` access bit, hypervisor view; controls VS and VU | 0, 1 | Priv. §4.2 |
| `sstateen0.FCSR` | `fcsr` access bit, supervisor view; controls U and VU | 0, 1 | Priv. §4.2 |
| `impl(X)` | Extension X is implemented | boolean; X is a manual extension name | Priv. §3.1 and the extension chapters |
| `Ext(F)` | Extension that provides format F | see §4 | — |
| `instr` | Instruction being executed | mnemonic with format suffix | — |
| `instr.rm` | Rounding field of the encoding | `RNE(0)`…`RMM(4)`, 5, 6, `DYN(7)` | Unpriv. Table 24 |
| `fcsr.frm` | Dynamic rounding mode | `RNE(0)`…`RMM(4)`, 5, 6, 7 | Unpriv. Table 24 |
| `fcsr.fflags` | Sticky floating-point flags | `NV(4)`, `DZ(3)`, `OF(2)`, `UF(1)`, `NX(0)` | Unpriv. §21.2 |
| `exception` | Synchronous exception outcome of the instruction itself | `\varnothing` when the block raises none; otherwise `\{X\}` with the block's own code (`IllegalInstruction(2)`, `VirtualInstruction(22)`, a breakpoint, misaligned, page-fault, guest-page-fault, or access-fault code); `\mathrm{walk}`, `\mathrm{phys}`, `\mathrm{data}`, `\mathrm{lowest}` qualify the manual's duplicate rows; instruction-fetch outcomes are not repeated in the formulas | §7.1.1, §7.1.2 |
| `\mathrm{walk}`, `\mathrm{phys}`, `\mathrm{data}`, `\mathrm{lowest}` | Origin label on an exception code; a shorthand of this document, not a manual term — the manual identifies these rows only by the descriptions in Tables 17 and 51 | `data`: data-address breakpoint row (`:10550`), or the final-access row for codes 5 and 7 (`:10556`); `walk`: the address-translation row for codes 1, 5, and 7 (`:10542`, `:10554`); `phys`: the physical-address row for codes 1, 5, and 7 (`:10544`, `:10556`); `lowest`: the second misaligned row (`:10558`); the same labels with `fetch` mark the instruction-fetch rows in §7.1.2 | Priv. Tables 17 and 51 |
| `F` | Format parameter | `H`, `S`, `D`, `Q` | — |
| `a`, `b` | Source operands | the triple $(s,e,f)$ of the low $w_F$ bits of `f[rs1]`, `f[rs2]` once that register is correctly boxed; a conversion source of format `G` uses $w_G$ | §5.1, §5.4 |
| `c` | Third multiplicand of an FMA | same reading from `f[rs3]` | §5.1, §5.4 |
| `w_F`, `w_e`, `w_f` | Total, exponent, significand widths of format `F`; a second format `G` uses `w_G`, `w_{e,G}`, `w_{f,G}` | per format | §5.1 |
| `e_{\max}`, `f_{\max}` | Maximum biased exponent and significand of format `F`; the source format `G` of a conversion uses `e_{\max,G}`, `f_{\max,G}` | `2^{w_e}-1`, `2^{w_f}-1` | — |
| `E_{\min}`, `E_{\max}` | Minimum and maximum unbiased exponent | per format | §5.1 |
| `\mathrm{val}_F(a)` | Value of a bit-field triple | piecewise | §5.2 |
| `x`, `y`, `z` | Numeric values of the sources | `\mathrm{val}_F(a)` etc. | — |
| `\mathrm{exact}` | Exact result before rounding | instruction-specific | — |
| `\mathrm{rounded}` | `\mathrm{exact}` correctly rounded by the effective mode | piecewise | §6.1 |
| `\mathrm{round}_{F,m}(v)` | Round `v` to format F with mode `m` on the format grid, subnormal step included; no exponent cap above `MAX` | — | §6.1 |
| `\mathrm{round}^{\infty}_{F,m}(v)` | Round `v` to format F's precision with mode `m` and no exponent cap at either end; used only by tininess detection | — | §6.1 |
| `\mathrm{tiny}` | Tininess after rounding, for the instruction's destination format: `0<\lvert\mathrm{round}^{\infty}_{F,m}(\mathrm{exact})\rvert<2^{E_{\min}}` | boolean | Unpriv. §21.4, §25.3.2.6.1 |
| `\mathrm{FLEN}` | Floating-point register width | implementation-defined | Unpriv. §22.2 |
| `\mathrm{XLEN}` | Integer register width | 32 or 64 | Unpriv. §1.2 |
| `\mathrm{qNaN}_F` | Canonical quiet NaN | `s=0`, `e=e_{\max}`, `f=2^{w_f-1}` | Unpriv. §21.3 |
| `\mathrm{sNaN}`, `\mathrm{qNaN}` | Input NaN classes | see §5.2 | — |
| `+\infty_F`, `-\infty_F` | Infinity result classes | per format | — |
| `+0_F`, `-0_F` | Zero result classes | per format | — |
| `0_F(p)` | Zero of format `F` with sign bit `p`: `+0_F` if `p=0`, `-0_F` if `p=1` | `p` is 0 or 1 | — |
| `+\mathrm{MAX}_F`, `-\mathrm{MAX}_F` | Maximum finite result classes | per format | — |
| `fd`, `fs1`, `fs2`, `fs3` | Floating-point registers | register identifiers | — |
| `rd`, `rs1`, `rs2`, `rs3` | Integer registers | register identifiers | — |
| `f[i]`, `x[i]` | Register file entries | width `FLEN` / `XLEN` | — |
| `mem[a,w]` | Memory word of `w` bits at address `a` | little-endian bit vector | Unpriv. §1.4 |
| `imm` | Immediate field of the encoding | per instruction | — |
| `u` | Integer operand value of type `T` | two's complement for `W`/`L`, unsigned for `WU`/`LU`; `FCVT.F.T` binds `u=\mathrm{sext}_n(x[\mathrm{rs1}][n-1:0])` for `W`/`L` and `u=\mathrm{zext}_n(x[\mathrm{rs1}][n-1:0])` for `WU`/`LU`; `FCVT.T.F` writes it as `\mathrm{enc}_T(u)` | §5.1, Unpriv. §21.7 |
| `n` | Width of type `T` in bits | 32 for `W`/`WU`; 64 for `L`/`LU`, whose blocks require `\mathrm{XLEN}=64` | Unpriv. §21.7 |
| `T` | Integer type of a float–integer conversion | `W`, `WU`, `L`, `LU` | Unpriv. §21.7 |
| `\min T`, `\max T` | Smallest and largest values of type `T` | `W`: $-2^{31}$, $2^{31}-1$; `WU`: $0$, $2^{32}-1$; `L`: $-2^{63}$, $2^{63}-1$; `LU`: $0$, $2^{64}-1$ | Unpriv. Table 27 |
| `I` | Instruction under consideration in a family-wide file | mnemonic with format suffix | — |
| `G` | Source format of a floating-point conversion | `H`, `S`, `D`, `Q` | — |
| `\mathrm{fcsr}` | Floating-point control and status register | 32-bit register | Unpriv. §21.1 |
| `\mathrm{Extm}(F)` | Extension providing the H conversion subset | `Zfhmin`, `F`, `D`, `Q` | §4 |
| `\mathrm{Extx}(F)` | x-register extension providing format F | `Zhinx`, `Zfinx`, `Zdinx` | §4 |
| `\mathrm{EA}` | Effective address of a load or store | $(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$, bound in every data-access block | §5.1 |
| `\mathrm{PC}` | Address of the instruction being fetched | instruction address | Unpriv. §2.2 |
| `\mathrm{sext}_n`, `\mathrm{zext}_n` | Sign and zero extension to $n$ bits | — | — |
| `\mathrm{low}_n(v)`, `\mathrm{high}_n(v)` | Low $n$ bits of $v$, and the bits above them | — | — |
| `\mathrm{raw}_F(v)` | $w_F$-bit IEEE encoding of a value or class | — | — |
| `\mathrm{box}_F`, `\mathrm{enc}_F(v)` | Boxing into `FLEN` bits and its result | — | §5.4 |
| `\mathrm{boxed}_F(v)` | Correct NaN-boxing of a register image | $\mathrm{FLEN}=w_F$ or $v[\mathrm{FLEN}-1:w_F]=1^{\mathrm{FLEN}-w_F}$; `G`, `D`, `S`, `B` subscript the same predicate for those format names | §5.4, Unpriv. §22.2 |
| `\mathrm{senc}_F(v)` | $w_F$-bit encoding sign-extended to `XLEN` | — | §5.4 |
| `\mathrm{xop}_F(i)` | Source operand read from `x[i]` under `Zfinx` | piecewise; `w_F=2\,\mathrm{XLEN}` (RV32Zdinx `D`) reads the aligned pair `x[i]`:`x[i+1]`, and `i=0` reads zero | §5.4, Unpriv. §27.3 |
| `\mathrm{xwr}_F(i,v)` | Result-set element for a `Zfinx` write of $v$ into `x[i]` | piecewise; expands into one or two register assignments, and a write through `x0` leaves `x[0]=0` | §5.4, Unpriv. §27.3 |
| `\mathrm{enc}_T(u)` | Integer register value after a $T$ write: on `XLEN=32` every type writes $u$; on `XLEN=64` both `W` and `WU` write $\mathrm{sext}_{64}(\mathrm{low32}(u))$, while `L` and `LU` write $u$ | `T` is `W`, `WU`, `L`, `LU` | Unpriv. §21.7 |
| `\mathrm{roundInt}(x)` | $x$ rounded to an integer by the effective mode | — | — |
| `\mathrm{ires}` | Rounded integer before range clamping | — | — |
| `\mathrm{trunc}(x)` | $x$ truncated toward zero | — | — |
| `\mathrm{low32}(v)` | Low 32 bits of an integer | — | — |
| `\min_\prec`, `\max_\prec` | Minimum and maximum in the total order | §5.3.1 | — |
| `\mathrm{FLI}_F(imm)` | Constant selected by the FLI immediate | §2.1 | Unpriv. §26.1 |

The ten IEEE value classes (quiet/signaling NaN, the two infinities, the two zeros, normal,
subnormal) are not separate symbols: formulas write them as ranges over
$s,e,f$ using $e_{\max}$ and $f_{\max}$.

### 2.1 FLI constants

$\mathrm{FLI}_F(imm)$ selects one of the 32 constants below (Unpriv. Table 35,
`sources/riscv-unprivileged.txt:8470-8576`). Entry 1 is the minimum positive normal of the
destination format, so it differs among H, S, D, and Q; every other entry has the same numeric value
in all four formats, except entry 29, which is $2^{16}$ in S, D, and Q but $+\infty_F$ in H because
$2^{16}$ is not representable there. Entries 2 and 3 are subnormal in H.

| `imm` | Value | `imm` | Value |
|---:|---|---:|---|
| 0 | $-1$ | 16 | $1$ |
| 1 | $2^{E_{\min}}$ | 17 | $1.25$ |
| 2 | $2^{-16}$ | 18 | $1.5$ |
| 3 | $2^{-15}$ | 19 | $1.75$ |
| 4 | $2^{-8}$ | 20 | $2$ |
| 5 | $2^{-7}$ | 21 | $2.5$ |
| 6 | $2^{-4}$ | 22 | $3$ |
| 7 | $2^{-3}$ | 23 | $4$ |
| 8 | $2^{-2}$ | 24 | $8$ |
| 9 | $0.3125$ | 25 | $16$ |
| 10 | $0.375$ | 26 | $128$ |
| 11 | $0.4375$ | 27 | $256$ |
| 12 | $0.5$ | 28 | $2^{15}$ |
| 13 | $0.625$ | 29 | $2^{16}$ (H: $+\infty$) |
| 14 | $0.75$ | 30 | $+\infty$ |
| 15 | $0.875$ | 31 | $\mathrm{qNaN}_F$ |

## 3. Writing rules

1. One result formula is one display block with a single `aligned` environment; each left-hand
   line starts with `&`.
2. At most one top-level `\land` per line; `\land` inside parentheses does not count.
3. `\longrightarrow` separates the left and right sides; the right side is `\{\, … \,\}` with
   comma-separated fields.
4. Right-hand order: destination, the `FS` writes, flags, `exception`; the exception is always last.
   A configuration that updates more than one status field lists them as comma-separated results,
   because every listed result occurs; `\land` is reserved for the left side.
5. Multi-letter names go in `\mathrm{}`; single-letter operand symbols and indices are italic
   ($s_a$, $e_a$, $f_a$); format subscripts are $H$, $S$, $D$, $Q$, and $F$ when parameterized.
6. Enumerations are `Name(code)` with no space; sets are `\{…\}`; the empty set is
   `\varnothing`; a singleton is `\{X\}`.
7. Only `\land`, `\lor`, `\neg`, `\longrightarrow`, `\in`, `\notin`, `=`, `\ne`, `\le`, `<`, `\ge`,
   `>` are used as logical notation; no textual connectives.
8. A derived symbol is defined once as `\mathrm{name}=…` and then used as a term; it is not
   expanded inline inside a formula.
9. Results are IEEE classes or normal/subnormal values $r$, never bit patterns. The only
   exceptions are instructions defined as verbatim bit copies — sign injection, moves, and
   `FCLASS` — whose results are written as bit-field triples `(s,e,f)` or as integer words.
10. No table cell contains inline math with a vertical bar.
11. The privileged configuration is the first left-hand line and is one of the three cases of §1:
    `¬impl(H) ∧ Priv∈{M,S,U}`, `impl(H) ∧ Priv∈{M,HS,U}`, or
    `impl(H) ∧ (Priv∈{VS,VU} ∧ vsstatus.FS∈{1,2,3} ∧ sstatus.FS∈{1,2,3})`. The right-hand side
    then carries only the `FS` writes of that configuration (§6.2).

No hidden disjunction predicate is allowed. In particular, the legality of the rounding mode is
written out over `instr.rm` and `fcsr.frm` every time it is needed. Helper predicates over
operand classes are likewise forbidden: write the range over $s,e,f$ directly.

## 4. Formats and extensions

| Format | Extension `Ext(F)` | `w_F` | `w_e` | `w_f` | `E_{\min}` | `E_{\max}` |
|---|---|---:|---:|---:|---:|---:|
| H | `Zfh` | 16 | 5 | 10 | $-14$ | $15$ |
| S | `F` | 32 | 8 | 23 | $-126$ | $127$ |
| D | `D` | 64 | 11 | 52 | $-1022$ | $1023$ |
| Q | `Q` | 128 | 15 | 112 | $-16382$ | $16383$ |

`D` implies `F`, `Q` implies `D`, and `Zfh`, `Zfhmin`, and `Zfbfmin` each imply `F`, so a single
`impl(Ext(F))` conjunct is enough for an instruction available in all four formats.

In these formulas $F$ is the format variable, not the `F` extension: each block is a schema over
$F$, and the mnemonic fixes the case. `FADD.D` is $F=D$, so its format conjunct is
`impl(Ext(D))`, i.e. `impl(D)`, and its instruction conjunct is `instr=FADD.D`. The extension `F`
itself is written upright, as in `impl(F)` in the `FLW`/`FSW` row below; the italic $F$ always
ranges over H, S, D, and Q.

`impl(X)` means that extension `X` is implemented. The model has no separate predicate for the
value `misa` reports: every configuration considered here is one in which `misa` truthfully reports
the implemented extensions, hence `impl(F)` implies `misa.F=1`. This matters for `stateen`: while
`misa.F=1`, `mstateen0.FCSR` is read-only zero and gates nothing, but an implementation may hardwire
`misa` to zero (Priv. §3.1.1, `sources/riscv-privileged.txt:1578-1583`); then the bit is writable
and, when it is zero, *all* floating-point instructions raise an illegal-instruction exception,
whether they use `f` or `x` registers (Priv. §4.2, `sources/riscv-privileged.txt:4692-4699`).
`zfinx.md` writes that gate out for the x-register forms; the `f`-register files would carry the
same conjunct in a configuration where `misa` reads zero.

`\mathrm{impl}(H)` is the hypervisor extension of Priv. Chapter 15. It is not the 16-bit format
`H`, whose extension is `Zfh` ($\mathrm{Ext}(H)=\mathrm{Zfh}$): the format never appears alone in
`impl(...)`. The mode names `HS`, `VS`, and `VU` exist only when `H` is implemented; without it
the supervisor mode is `S` (Priv. Table 1, `sources/riscv-privileged.txt:748-752`; Table 44,
`sources/riscv-privileged.txt:8719-8727`).

`Zfhmin`
provides only the data-transfer and conversion instructions of Chapter 24.6, not the arithmetic
instructions. BF16 (`Zfbfmin`) provides the two conversions of `bf16.md` together with the four
16-bit transfer instructions `FLH`, `FSH`, `FMV.X.H`, and `FMV.H.X` of Chapter 24; BF16 is not a
member of the four-format family and is written out explicitly.

BF16 is 16 bits wide with 8 exponent bits, $w_{f,B}=7$ significand bits, $E_{\min,B}=-126$, and
$E_{\max,B}=127$; its classes carry the subscript $B$: $\mathrm{qNaN}_B$, $+\infty_B$, $+0_B$,
$\pm\mathrm{MAX}_B$. The x-register extensions map formats as $\mathrm{Extx}(H)=\mathrm{Zhinx}$,
$\mathrm{Extx}(S)=\mathrm{Zfinx}$, and $\mathrm{Extx}(D)=\mathrm{Zdinx}$; no `Zqinx` exists, so
`zfinx.md` covers H, S, and D only.

$\mathrm{Extm}(F)$ is the minimal extension providing the H conversion subset:
$\mathrm{Extm}(H)=\mathrm{Zfhmin}$, and $\mathrm{Extm}(F)=\mathrm{Ext}(F)$ for S, D, and Q. It is
the implementation condition for every `FCVT` conversion involving H, because `Zfhmin` already
contains those H conversions while the arithmetic H instructions need `Zfh` (Unpriv. §24.6,
`sources/riscv-unprivileged.txt:7786-7799`). The four 16-bit transfer instructions `FLH`, `FSH`,
`FMV.X.H`, and `FMV.H.X` are provided independently by `Zfhmin` (Chapter 24) and by `Zfbfmin`
(Chapter 25.4.1), so their condition is the disjunction `impl(Zfhmin) ∨ impl(Zfbfmin)`
(`sources/riscv-unprivileged.txt:8109-8110`).

Format availability per instruction:

| Instruction group | Formats | Extension condition |
|---|---|---|
| Arithmetic, sign injection, min/max, compare, classify | H, S, D, Q | `impl(Ext(F))` |
| `FMINM`, `FMAXM`, `FROUND`, `FROUNDNX`, `FLEQ`, `FLTQ`, `FLI` | H, S, D, Q | `impl(Ext(F)) ∧ impl(Zfa)` |
| `FCVTMOD.W.D` | D | `impl(D) ∧ impl(Zfa)` |
| `FLW`/`FSW` | S | `impl(F)` |
| `FLD`/`FSD` | D | `impl(D)` |
| `FLQ`/`FSQ` | Q | `impl(Q)` |
| `FLH`/`FSH` | H | `impl(Zfhmin) ∨ impl(Zfbfmin)` |
| `FMV.X.W`/`FMV.W.X` | S | `impl(F)` |
| `FMV.X.D`/`FMV.D.X` | D | `impl(D)` |
| `FMV.X.H`/`FMV.H.X` | H | `impl(Zfhmin) ∨ impl(Zfbfmin)` |
| `FMVH.X.D`/`FMVP.D.X` | D | `impl(D) ∧ impl(Zfa)` |
| `FMVH.X.Q`/`FMVP.Q.X` | Q | `impl(Q) ∧ impl(Zfa)` |
| `FCVT.dst.src` | H, S, D, Q | `impl(Extm(F)) ∧ impl(Extm(G))` |
| `FCVT.BF16.S`, `FCVT.S.BF16` | BF16 | `impl(F) ∧ impl(Zfbfmin)` |
| `FRCSR`, `FSCSR`, `FRRM`, `FSRM`, `FRFLAGS`, `FSFLAGS` | — | `impl(F) ∧ impl(Zicsr)` |
| x-register forms of the above (no transfers) | H, S, D | `impl(Extx(F)) ∧ impl(Zicsr)` |

In the x-register family `Zhinxmin` alone provides `FCVT.S.H`/`FCVT.H.S`, and `FCVT.D.H`/`FCVT.H.D`
when `Zdinx` is present — the counterpart of the H-conversion subset of `Zfhmin`; every other H
instruction of that family needs `Zhinx` (Unpriv. §27.5).

`FADD.H` and every other H arithmetic instruction require `Zfh`, so `misa.F=1` in every usable
configuration. Whenever `misa.F=1`, `mstateen0.FCSR` is read-only zero, so no stateen bit gates and
no virtual-instruction exception can arise. No formula of an `f`-register file carries a stateen
conjunct; the Zfinx forms, where `misa.F=0` and stateen gating is live, are handled in `zfinx.md`.

A stateen CSR controls only less-privileged modes (Priv. §4.1), so M-mode is never gated by
`mstateen0`. For the Zfinx forms the controlling bits are `mstateen0.FCSR` in HS-mode,
`mstateen0.FCSR` and `sstateen0.FCSR` in U-mode, `mstateen0.FCSR` and `hstateen0.FCSR` in VS-mode,
and all three in VU-mode (Priv. §4.2, `sources/riscv-privileged.txt:4556-4562`, `4575-4577`). A
zero in `mstateen0` is an illegal-instruction condition in every mode below M, whereas a zero in
`hstateen0` or `sstateen0` reached from VS or VU raises `VirtualInstruction(22)`.

## 5. Operands

### 5.1 Bit fields

Each operand is a triple $a=(s_a,e_a,f_a)$: sign, biased exponent, trailing significand (without
the hidden bit). $e_{\max}=2^{w_e}-1$ and $f_{\max}=2^{w_f}-1$. An `f`-register source is read as
the triple of its low $w_F$ bits, and every formula requires that register to be correctly boxed
(§5.4); that requirement is carried by the instruction file's leading `¬boxed` blocks, so later
blocks state field conditions only. An `x`-register source under `Zfinx` is
$a=\mathrm{xop}_F(\mathrm{rs1})$, with no boxing check. A load or store binds
$\mathrm{EA}=(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$. The
integer source of `FCVT.F.T` is bound as $u=\mathrm{sext}_n(x[\mathrm{rs1}][n-1:0])$ for a signed
type and $u=\mathrm{zext}_n(x[\mathrm{rs1}][n-1:0])$ for an unsigned one, where $n$ is the width of
the type (Unpriv. §21.7, `:7107-7113`).

### 5.2 Value classes

| Class | Condition ($s$ is 0 or 1) |
|---|---|
| $-\infty_F$ | $s=1,\ e=e_{\max},\ f=0$ |
| negative normal | $s=1,\ 1\le e\le e_{\max}-1$ |
| negative subnormal | $s=1,\ e=0,\ 1\le f\le f_{\max}$ |
| $-0_F$ | $s=1,\ e=0,\ f=0$ |
| $+0_F$ | $s=0,\ e=0,\ f=0$ |
| positive subnormal | $s=0,\ e=0,\ 1\le f\le f_{\max}$ |
| positive normal | $s=0,\ 1\le e\le e_{\max}-1$ |
| $+\infty_F$ | $s=0,\ e=e_{\max},\ f=0$ |
| sNaN | $e=e_{\max},\ 1\le f\le f_{\max},\ f[w_f-1]=0$ |
| qNaN | $e=e_{\max},\ 1\le f\le f_{\max},\ f[w_f-1]=1$ |

For an operation that performs no rounding, formulas use the class as a whole (for example
$fd=\mathrm{enc}_F(+\infty_F)$). For an operation with a numerical result, formulas use the value:

$$
\mathrm{val}_F(a)=
\begin{cases}
(-1)^{s}\,\bigl(1+f/2^{w_f}\bigr)\,2^{\,e-(2^{w_e-1}-1)}, & 1\le e\le e_{\max}-1,\\[2pt]
(-1)^{s}\,f\,2^{\,E_{\min}-w_f}, & e=0,\\[2pt]
(-1)^{s}\,\infty, & e=e_{\max},\ f=0.
\end{cases}
$$

The last case is the infinity $(-1)^s\infty$; a NaN ($e=e_{\max}$, $f\ne0$) has no value, and every
formula classifies NaN inputs before it uses $\mathrm{val}_F$.

### 5.3 Canonical NaN

A NaN result is always the canonical quiet NaN, with positive sign and zero payload:

$$
\mathrm{qNaN}_F:\quad s=0,\quad e=e_{\max},\quad f=2^{w_f-1}.
$$

Input NaN payloads are never propagated (Unpriv. §21.3,
`sources/riscv-unprivileged.txt:6946,6952`).

### 5.3.1 Total order for minimum and maximum

`MIN`/`MAX` compare non-NaN operands by the IEEE total order $\prec$: numeric order, with
$-0_F\prec+0_F$ and every other pair ordered by value. $\min_\prec(a,b)$ and $\max_\prec(a,b)$
return the smaller and larger *bit-field triples*, so the result of a minimum of $+0_F$ and
$-0_F$ is $-0_F$, and of a maximum $+0_F$. The ordering is used only after the NaN categories
have been excluded.

### 5.3.2 Comparison results

A comparison writes an integer to `rd`: the notation `rd=(P)` means $rd=1$ when the predicate $P$
holds and $rd=0$ otherwise. The integer result is not an IEEE value and raises no flag by itself.

### 5.4 Boxing

A narrower `f`-register value is NaN-boxed: its $w_F$ bits occupy the low bits of the
`FLEN`-bit register and the upper $\mathrm{FLEN}-w_F$ bits are all ones (Unpriv. §22.2,
`sources/riscv-unprivileged.txt:7288-7295`). Write

$$
\mathrm{boxed}_F(v):\quad
\mathrm{FLEN}=w_F\ \ \lor\ \ v[\mathrm{FLEN}-1:w_F]=1^{\mathrm{FLEN}-w_F},
$$

and use $\mathrm{boxed}_G$, $\mathrm{boxed}_D$, $\mathrm{boxed}_S$, $\mathrm{boxed}_B$ for the
other format names. Every non-transfer floating-point operation checks each `f`-register source:
a correctly boxed register contributes the triple $(s,e,f)$ of its low $w_F$ bits, while a
register that is not correctly boxed acts as the $w_F$-bit canonical NaN (Unpriv. §22.2,
`:7306-7309`). Each instruction file therefore opens its result blocks, one per privileged
configuration, with the blocks that carry a `¬boxed` conjunct:

1. the first is a disjunction with one disjunct per candidate signaling-NaN source: that source
   is correctly boxed and is a signaling NaN, and some *other* source is not correctly boxed;
   the block produces the instruction's NaN result with `NV(4)` set — a not-boxed register whose
   low bits happen to look like a signaling NaN sets no flag by itself. Inside a disjunct the
   `¬boxed` clause holds for every nonempty subset of the remaining sources, independently of
   which source is the signaling one; only the pattern with no correctly boxed source at all
   falls outside the block, and that pattern is the quiet-NaN case of block 2;
2. the next carries the `¬boxed` conjunct alone and produces what the instruction defines for a
   quiet-NaN source — possibly no flag at all, `NV(4)` for a conversion to integer or an ordered
   comparison, `rd=2^{9}` for `FCLASS`, and the sign-injected canonical NaN for `FSGNJ*`. It is
   a disjunction only where the result does not depend on *which* source is not boxed: any one
   or several of its terms may hold, and the block's result is the same. Where the result does
   depend on it, the conjunct is a conjunction over all sources instead, and the per-source
   cases follow as separate blocks.

Blocks are mutually exclusive and ordered, so every later block speaks about correctly boxed
operands only. For `FMIN`, `FMAX`, and the sign injections block 2 is therefore the pattern with
every source not boxed, and blocks 3–6 (or 3–4) give the rest: one block per not-boxed operand
and per NaN/non-NaN shape of the other operand. `FMINM`/`FMAXM` are covered by blocks 1 and 2 as
written, because their result collapses to the canonical NaN for any NaN input.

The transfer instructions — `FLn`, `FSn`, `FMV.X.n`, `FMV.n.X`, `FMVH.X.D`, `FMVH.X.Q`, and
`FMVP` — move the low bits of a register directly and do not check boxing (`:7302-7304`), so
their formulas name `f[rs1][j:i]` and carry no `\mathrm{boxed}` conjunct.

Every right side names the register image, so the boxing of the result is part of the formula
rather than of write-back: `fd=\mathrm{enc}_F(v)` for a class or value $v$, and
`fd=\mathrm{box}_F(\text{bits})` for a sign, significand, or other bit field (Unpriv. §22.2). A
bit-copy instruction — a load, `FMV.W.X`, `FMV.H.X`, `FMV.D.X`, or `FMVP` — names the boxed
register image directly.

The three encodings are related by

$$
\mathrm{enc}_F(v)=\mathrm{box}_F(\mathrm{raw}_F(v)),\qquad
\mathrm{senc}_F(v)=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{raw}_F(v)),
$$

where $\mathrm{raw}_F(v)$ is the $w_F$-bit IEEE pattern of the value or class $v$. The
`f`-register files write $\mathrm{enc}_F(v)$ (written `fd=\mathrm{enc}_F(…)`); the x-register
family writes through $\mathrm{xwr}_F(\mathrm{rd},v)$ with no boxing. On RV32Zdinx a double lives in
the aligned pair `x[i]`:`x[i+1]`, so there $\mathrm{xop}_F$ and $\mathrm{xwr}_F$ read and write both
registers, an odd register number is reserved, and `x0` is read as zero and discarded on write
(Unpriv. §27.3, `:8765-8779`).

### 5.5 Memory access predicates

Loads and stores model the memory system with predicates over the effective address and the access
width $w$:

| Predicate | Meaning |
|---|---|
| $\mathrm{Breakpoint}(\mathrm{EA})$ | the environment reports a data breakpoint at `EA` |
| $\mathrm{MisalignedPre}(\mathrm{EA},w)$ | the width-$w$ access is misaligned, as determined before address translation |
| $\mathrm{PageFault}(\mathrm{EA},\mathrm{kind})$ | translation fails with a page fault |
| $\mathrm{GuestPageFault}(\mathrm{EA},\mathrm{kind})$ | translation fails with a guest-page fault |
| $\mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{kind})$ | translation fails with an access fault |
| $\mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{kind})$ | the translated access fails with an access fault |
| $\mathrm{MisalignedPost}(\mathrm{EA},w)$ | the width-$w$ access is misaligned, as determined after translation |
| $\mathrm{MemOK}_{\mathrm{kind}}(\mathrm{EA},w)$ | the access completes normally |

`kind` is `load` or `store`. These predicates are environment-dependent: which ones hold, and in
which cases misalignment is checked before or after translation, is a property of the memory system,
not of the instruction. In each load or store file the eight formulas are ordered and mutually
exclusive by convention: a formula applies when its predicate holds and no earlier predicate does,
and the last formula is the complement of the other seven.

Some of these predicates can be triggered by accesses the instruction does not itself perform. A
page-table walk reads PTEs with implicit accesses; a PMA or PMP violation on such a read raises an
access fault corresponding to the original access type, and an invalid PTE raises a page fault,
also corresponding to the original access type (`sources/riscv-privileged.txt:7770-7774`). In
two-stage translation, a guest-page fault can arise from an implicit VS-stage PTE access
(`sources/riscv-privileged.txt:9349-9352`). These events are the `AccessFaultPre`, `PageFault`, and
`GuestPageFault` rows. A misaligned access, and a store wider than `XLEN`, may likewise be
decomposed into multiple memory operations that are checked independently: the instruction raises an
access fault if at least one operation fails, while others may succeed and become visible
(`sources/riscv-privileged.txt:4421-4428`, `4451-4457`). Every such fault is attributed to the
original instruction, which is why the predicates are stated over `EA` and $w$ rather than over the
individual bytes or PTE addresses.

The model assumes little-endian memory, that `EA` is formed from the current `rs1` value and the
immediate, and that address translation, PMP/PMA checks, and two-stage translation are all
summarized by the predicates above; the effective privilege mode (including `MPRV`) only selects
which rows of the summary apply. Store formulas describe the intended full-width write. When an
exception is raised, a misaligned store or a store wider than `XLEN` may already have committed
some bytes — PMP checking and decomposition are per memory operation — so the exception branches
state the exception and leave any partial memory effect unconstrained
(Priv. §3.7.1.3, `sources/riscv-privileged.txt:4421-4428`). Load formulas likewise describe the
full-width read; the first-fault rule for misaligned or page-crossing accesses is part of the
memory system's predicate assignment.

### 5.6 Representative operands

The guards of the formulas test value classes, signs, flags, and rounding modes, never individual
bit patterns, so one representative per class reaches every block. Write an operand as the triple
$(s,e,f)$ of §5.1.

**Class representatives.** The ten classes of §5.2 are reached by

| Class | Triple |
|---|---|
| $+0_F$ / $-0_F$ | $(0,0,0)$ / $(1,0,0)$ |
| positive subnormal, smallest / largest | $(0,0,1)$ / $(0,0,f_{\max})$ |
| positive normal, smallest / largest | $(0,1,0)$ / $(0,e_{\max}-1,f_{\max})$ |
| $+\infty_F$ / $-\infty_F$ | $(0,e_{\max},0)$ / $(1,e_{\max},0)$ |
| sNaN, smallest / largest payload | $(0,e_{\max},1)$ / $(0,e_{\max},2^{w_f-1}-1)$ |
| qNaN, canonical / largest payload | $(0,e_{\max},2^{w_f-1})$ / $(0,e_{\max},f_{\max})$ |

Setting $s=1$ in the subnormal, normal, and NaN rows gives the negative class. The ten rows are
also the ten result bits of `FCLASS`, so this one set exercises that instruction completely.

**Bit-pattern families.** `FCLASS`, the three sign injections, `FMV` in both directions, and the
box of §5.4 inspect individual bits, so their operands are patterns over $f$ at a fixed $e$. The
patterns live in one scalar operand's significand; no vector register or lane replication is
involved. With $0\le i<w_f$, the families are

| Family | Pattern | What it exercises |
|---|---|---|
| walking one | $f=2^i$ | one bit set at a time; reaches the quiet bit $f[w_f-1]$ |
| walking one, lsb set | $f=2^i+1$ | as above with bit 0 held |
| walking zero | $f=f_{\max}\oplus2^i$ | one bit cleared at a time |
| walking zero, lsb cleared | the walking zero with bit 0 cleared | as above with bit 0 held clear |
| marching ones | $f=2^{i+1}-1$ | a run of ones growing from bit 0 |
| marching zeros | $f=f_{\max}-(2^{i+1}-1)$ | a run of zeros growing from bit 0 |
| ranks from the edges | $f=(2^k-1)\,(2^{w_f-k}+1)$, $1\le k\le\lfloor (w_f-1)/2\rfloor$ | ones entering from both ends and meeting |
| ranks from the middle | the centred run of $w_f-2k$ ones, $1\le k\le\lfloor (w_f-1)/2\rfloor$ | ones retreating from both ends toward the middle |
| $k$-bit periodic, $2\le k\le5$ | every nonzero $k$-bit block repeated with period $k$ from bit $w_f-1$ downward; $2^k-1$ patterns, the all-ones block being $f=f_{\max}$ | coupling between bits $k$ apart |

Two of these reach the NaN boundaries: the walking one at $i=w_f-1$ is the canonical $\mathrm{qNaN}_F$,
and the marching ones at $i=w_f-2$ is the largest sNaN payload $2^{w_f-1}-1$. Apart from such bit
positions, every pattern of a family belongs to the same class as its neighbours, so the families
add nothing to the guards of the remaining instructions; they separate a copy, width, or
sign-injection error from a class error in the instructions that inspect bits.

**Field isolation.** Giving the three fields pairwise distinct recognizable values makes a field,
width, or endianness error visible in a single result; $s=1$, $e=11$, $f=22$ is one such triple.

**Pairs.** Some results depend on a relation between two operands and have no single-operand
representative: $+0_F$ added to $-0_F$ (FADD.19), two infinities of opposite sign (FADD.4), and in
§6 the tie and the overflow boundary, which are properties of the exact sum or product rather than
of either operand. These must be constructed from §5.1 and §6.1, not sampled from a class list.

## 6. Rounding and status

### 6.1 Effective rounding mode

`instr.rm` and `fcsr.frm` are both 3-bit fields. `RNE(0)`, `RTZ(1)`, `RDN(2)`, `RUP(3)`,
`RMM(4)` are legal; 5 and 6 are reserved; `instr.rm` additionally has `DYN(7)`, which selects
`fcsr.frm`. The rounding field is legal if and only if

$$
\bigl(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\ \lor\ (\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\bigr).
$$

Every instruction with an `rm` field carries this conjunct. The effective mode is `instr.rm` when
it is not `DYN(7)`, and `fcsr.frm` otherwise:

$$
\mathrm{rounded}=
\begin{cases}
\mathrm{round}_{F,\mathrm{instr}.rm}(\mathrm{exact}), & \mathrm{instr}.rm\ne\mathrm{DYN}(7),\\
\mathrm{round}_{F,fcsr.frm}(\mathrm{exact}), & \mathrm{instr}.rm=\mathrm{DYN}(7).
\end{cases}
$$

$\mathrm{round}_{F,m}(v)$ rounds $v$ once, in mode $m$, onto the format grid: below $2^{E_{\min}}$
the grid has step $2^{E_{\min}-w_f}$ (the subnormal grid), and above $\mathrm{MAX}_F$ it continues
without an exponent cap, so overflow is detected by comparing $\mathrm{rounded}$ with
$\mathrm{MAX}_F$ rather than by saturating inside the rounding.

Tininess is detected after rounding, and that detection uses its own rounding, distinct from the
rounding that delivers the result. Let $\mathrm{round}^{\infty}_{F,m}(v)$ round $v$ in mode $m$ to
$F$'s precision with no exponent cap at either end; every nonzero result of this rounding is a
normal $F$ number of the same sign. Then

$$
\mathrm{tiny}\iff 0<\bigl|\mathrm{round}^{\infty}_{F,m}(\mathrm{exact})\bigr|<2^{E_{\min}}.
$$

These two roundings can disagree at the bottom of the exponent range.
$\mathrm{round}^{\infty}_{F,m}$ can produce a magnitude below $2^{E_{\min}}$ while
$\mathrm{round}_{F,m}$ delivers $\pm2^{E_{\min}}$, and `UF(1)` is still signalled. The detection
rounding is finer than the delivered subnormal grid, so the disagreement has one direction only: a
$\mathrm{tiny}$ result can be delivered as $\pm2^{E_{\min}}$ (or as a subnormal), while a non-zero
result that is not $\mathrm{tiny}$ is always delivered as a normal value. Underflow therefore follows
$\mathrm{tiny}$, not the class of the delivered value: `UF(1)` and `NX(0)` are set together exactly
when $\mathrm{tiny}$ holds and $\mathrm{rounded}\ne\mathrm{exact}$ (Unpriv. §21.4, §25.3.2.6.1,
`sources/riscv-unprivileged.txt:6972-6978,8058-8073`). Consequently the instruction files bound the
`NX(0)`-only category to normal delivered values and require $\neg\mathrm{tiny}$, while the
tiny-inexact category has no class bound: its delivered value may be normal, and it always signals
`UF(1)` and `NX(0)` together.

The behavior of a reserved rounding mode is reserved, so those configurations are outside every
instruction file: they appear in no formula, neither as a result nor as an exception. Raising
`IllegalInstruction(2)` is a permitted implementation choice but not a requirement (Unpriv. §21.2,
`sources/riscv-unprivileged.txt:6889-6894,6920-6924`).

### 6.2 Dirty status

Writing any floating-point state — an `f` register or the `fcsr` — sets the floating-point state
to Dirty (Priv. §15.2.11, `sources/riscv-privileged.txt:9538-9540`). Each result block fixes one
privileged configuration, so its right-hand side names only that configuration's status writes:
`mstatus.FS=Dirty(3)` in the `M/S/U` and `M/HS/U` blocks, and
`vsstatus.FS=Dirty(3),\ sstatus.FS=Dirty(3)` in the `VS/VU` blocks. The two `VS/VU` writes are
comma-separated results of the same formula, not a conjunction: both occur.

In `U`, `S`, `HS`, and `M` mode only `mstatus.FS` exists. In `VS` and `VU` both `vsstatus.FS` and
the HS-level `sstatus.FS` are in effect and both are set (Priv. §15.2.11,
`sources/riscv-privileged.txt:9538-9540`). `mstatus.FS` and `sstatus.FS` are the same field, so
the `VS/VU` assignment also updates the HS-level field.

Consequently:

- an instruction that writes `fd` always carries the assignment on the right;
- an instruction that writes only `rd` carries it exactly in the branches that also set a flag in
  `fcsr.fflags` (the `fcsr` is then modified);
- a compare or move that writes only `rd` with no flag set does not change floating-point state
  and carries no assignment;
- `FSCSR`, `FSRM`, and `FSFLAGS` write `fcsr` and therefore carry it, although their `rd` write
  alone would not; `FRCSR`, `FRRM`, and `FRFLAGS` do not.

This is the precise (conservative) strategy. The privileged specification also permits imprecise
tracking: an implementation may set Dirty when the state is not actually modified, and may not
track dirtiness at all, in which case the reachable `FS` values are Off and Dirty
(Priv. §15.2.3, `sources/riscv-privileged.txt:2333-2346`). The formulas state the minimal Dirty
set; a coarser implementation may add Dirty transitions but never omit a required one.

## 7. Exceptions and flags

### 7.1 Exception codes

| Code | Name |
|---:|---|
| 0 | `InstructionAddressMisaligned` |
| 1 | `InstructionAccessFault` |
| 2 | `IllegalInstruction` |
| 3 | `Breakpoint` |
| 4 | `LoadAddressMisaligned` |
| 5 | `LoadAccessFault` |
| 6 | `StoreAMOAddressMisaligned` |
| 7 | `StoreAMOAccessFault` |
| 8 | `EnvironmentCallFromU` |
| 9 | `EnvironmentCallFromS` |
| 11 | `EnvironmentCallFromM` |
| 12 | `InstructionPageFault` |
| 13 | `LoadPageFault` |
| 15 | `StoreAMOPageFault` |
| 20 | `InstructionGuestPageFault` |
| 21 | `LoadGuestPageFault` |
| 22 | `VirtualInstruction` |
| 23 | `StoreAMOGuestPageFault` |

(Priv. Table 50, `sources/riscv-privileged.txt:10424-10456`.) All `zfinx` formulas use the same
codes; the virtual-instruction cases are written out in `zfinx.md`.

In the `f`-register files, an instruction whose operands are all registers raises only
`IllegalInstruction(2)` from the execution phase; the Zfinx forms additionally raise
`VirtualInstruction(22)` when the `stateen` gate denies a virtual machine. Loads and stores also
model address misalignment and storage access/page faults, whose trigger conditions depend on the
memory system and are stated as separate formulas in the load and store files. Outcomes that belong
to the instruction fetch depend only on `PC`, not on the instruction; they are tabulated once in
§7.1.2 and are therefore not repeated in the formulas, which list only the exceptions the instruction
itself can raise — or `\varnothing` when it raises none. When a listed code applies, the block's
register, memory, `FS`, and flag fields do not occur.

#### 7.1.1 Priority

When one execution can raise more than one synchronous exception, the decreasing order of Table 17
(`sources/riscv-privileged.txt:3027-3045`) decides which one is reported; when `H` is implemented,
Table 51 replaces it (`sources/riscv-privileged.txt:10538-10560`). The rule that the first exception
encountered wins, and the implementation-defined position of misalignment, are stated at
`sources/riscv-privileged.txt:3051-3060`. Every code these instructions can raise — directly, on the
instruction fetch, or through an implicit access — is listed with its origin:

| Code | Raised directly | Raised indirectly |
|---|---|---|
| `Breakpoint(3)` | an instruction-address breakpoint at `PC`, highest (`:3029`, `:10540`); or the environment reports a data breakpoint at `EA`, after address translation | — |
| `InstructionPageFault(12)` | the first-stage translation of `PC` fails (`:3031`, `:10542`) | — |
| `InstructionGuestPageFault(20)` | the G-stage translation of `PC` fails, with `H` implemented and `V=1` (`:10542`) | an implicit VS-stage PTE access fails (`:9349-9352`) |
| `InstructionAccessFault(1)` | the physical fetch of `PC` fails a PMA or PMP check (`:3033`, `:10544`); or the page-table walk for `PC` fails (`:7770-7771`) | — |
| `IllegalInstruction(2)` | extension not implemented, effective `FS` Off, `stateen` illegal | — (the encoding is legal; the environment vetoes execution) |
| `VirtualInstruction(22)` | — | `zfinx` under VS/VU while `hstateen0`/`sstateen0` deny and `mstateen0.FCSR=1` |
| `LoadAddressMisaligned(4)`, `StoreAMOAddressMisaligned(6)` | `EA` is misaligned, at whichever point the implementation checks it | — (the manual also permits an access fault instead, `:4033-4034`) |
| `LoadPageFault(13)`, `StoreAMOPageFault(15)` | the VS-stage walk fails: invalid or non-permitted PTE, misaligned superpage, or A/D update required under `Svade` (`:7771-7787`) | one part of a decomposed access (`:10286-10292`) |
| `LoadGuestPageFault(21)`, `StoreAMOGuestPageFault(23)` | the G-stage walk fails | an implicit VS-stage PTE access fails (`:9349-9352`); one part of a decomposed access (`:10286-10292`) |
| `LoadAccessFault(5)`, `StoreAMOAccessFault(7)` | the final access fails a PMA or PMP check | a PTE read violates PMA/PMP (`:7770-7771`); a PTE A/D write does (`:7788-7789`); one of several memory operations fails while others succeed (`:4451-4457`) |

`InstructionAddressMisaligned(0)` is not reachable: it is raised by a control-flow instruction whose
target is misaligned, not by the fetch (`:3069-3071`), and no instruction in §8 is a control
transfer. Environment calls and environment breaks are likewise not in scope: they belong to
`ECALL` and `EBREAK`.

An `FS` or `VS` field that is zero in `sstatus` or `vsstatus` yields `IllegalInstruction(2)`, never
`VirtualInstruction(22)` (`:10525-10527`), which is why the `f`-register groups have no 22.

Execution-phase priority chains, highest first, with `H` implemented:

| Instruction group | Priority |
|---|---|
| Arithmetic, FMA, `FSQRT`, `FDIV`, min/max, sign injection, compare, `FCLASS`, `FCVT`, `FMV`, `FLI`, the six `fcsr` instructions | `IllegalInstruction(2)` |
| `zfinx` forms | `IllegalInstruction(2) > VirtualInstruction(22)` |
| `FLW`, `FLD`, `FLQ`, `FLH` | `IllegalInstruction(2) > Breakpoint(3, data) > LoadAddressMisaligned(4) > LoadPageFault(13) = LoadGuestPageFault(21) = LoadAccessFault(5, walk) > LoadAccessFault(5, data) > LoadAddressMisaligned(4, lowest)` |
| `FSW`, `FSD`, `FSQ`, `FSH` | `IllegalInstruction(2) > Breakpoint(3, data) > StoreAMOAddressMisaligned(6) > StoreAMOPageFault(15) = StoreAMOGuestPageFault(23) = StoreAMOAccessFault(7, walk) > StoreAMOAccessFault(7, data) > StoreAMOAddressMisaligned(6, lowest)` |

In a chain, `>` means the left code has higher priority than the right and `=` means the two codes
have the same priority; the order is that of Table 17 when `H` is not implemented and Table 51
when it is. Without `H` the same chains apply with 21 and 23 removed and 22 impossible. The
instruction-fetch outcomes precede every chain in the table and are described in §7.1.2 instead of
being repeated in it: `Breakpoint(3, fetch)` is highest, the codes of the manual's "during
instruction address translation" row are tied at first encounter, and an access fault on the
physical fetch follows; all of them precede `IllegalInstruction(2)` because they are raised before
the instruction is decoded. The labels `fetch`, `walk`, `phys`, `data`, and `lowest` are not
manual terms; the manual identifies these rows only by the descriptions in the table. `fetch` and
`data` label the two origins of code 3, which the manual places at two different priorities: an
instruction-address breakpoint at the top, a data breakpoint after address translation. `walk` and `phys` label the two rows of
code 1 that the manual gives for instruction fetch. `=` marks the manual's "first encountered during
address translation" group: the walk stops at its first failure, so those codes never occur together
and are tied for priority. Two pairs of codes appear twice because the manual has two rows for them:
4/6 is "optionally" above the translation group and "if not higher priority" lowest, and the
`MisalignedPre` and `MisalignedPost` formulas encode the two placements; 5/7 is in the
first-encountered group when a walk (PTE read or A/D write) faults and after translation when the
explicit access faults, and the two cannot both occur because a failed walk performs no access. `walk` and `data` label that origin; `lowest` labels the second
misaligned row. An instruction file's `exception` field lists, in this order, the codes its
configuration can raise, or `\varnothing` when it raises none; the instruction-fetch chain of
§7.1.2 holds for every block of every file and is not written out in them.

#### 7.1.2 Instruction fetch

Every instruction is fetched before it is decoded, so a fetch fault preempts the instruction
entirely: if the fetch does not complete, the instruction writes no register, memory, or CSR and
sets no flag. The fetch depends only on `PC`, not on the instruction, so this chain is identical for
every instruction and every block, and it is stated once here rather than repeated in the formulas.
It is

$$
\mathrm{Breakpoint}(3,\mathrm{fetch}) > \mathrm{InstructionPageFault}(12)
= \mathrm{InstructionGuestPageFault}(20)
= \mathrm{InstructionAccessFault}(1,\mathrm{walk})
> \mathrm{InstructionAccessFault}(1,\mathrm{phys})
> \text{any execution-phase code of §7.1.1}.
$$

When `H` is not implemented, or for a block whose configuration excludes `V=1`, the
`InstructionGuestPageFault(20)` term is absent. Every code here precedes `IllegalInstruction(2)`
because the fetch completes before the instruction is decoded, and precedes every load or store
code because the access happens after translation of `PC`. The
qualifiers `\mathrm{fetch}`, `\mathrm{walk}`, `\mathrm{phys}`, and `\mathrm{data}` name the
manual's two rows for code 3 and two rows for code 1 (§7.1.1). Table 17 gives the order
(`sources/riscv-privileged.txt:3029-3033`); Table 51 inserts 20 into the translation group
(`:10540-10544`). If a 16-bit-aligned fetch straddles a page boundary, both translations belong to
this fetch, and a fault in either uses the instruction address `PC` (`:10286-10292`).

### 7.2 Floating-point flags

`fcsr.fflags` is sticky: `fcsr.fflags \mathrel{|}= S` sets every flag in $S$ and leaves the other
flags unchanged. The flags are `NV(4)`, `DZ(3)`, `OF(2)`, `UF(1)`, `NX(0)`; never clear a flag.

| Condition | Flag set |
|---|---|
| signaling NaN operand, or an invalid operation | `NV(4)` |
| a finite non-zero value divided by zero | `DZ(3)` |
| result too large to represent | `OF(2)` |
| result too small and inexact | `UF(1)` |
| result differs from the exact value | `NX(0)` |

Instructions without a rounding step (sign injection, min/max, class, moves, loads, stores) raise
no flags except `NV(4)` where the manual specifies it.

### 7.3 Per-instruction summary

| Instruction group | Exception IDs | Flags possible |
|---|---|---|
| Arithmetic (`FADD`, `FSUB`, `FMUL`, `FMA`) | 2 | `NV(4)`, `OF(2)`, `UF(1)`, `NX(0)` (no `DZ(3)`) |
| `FDIV` | 2 | `NV(4)`, `DZ(3)`, `OF(2)`, `UF(1)`, `NX(0)` |
| `FSQRT` | 2 | `NV(4)`, `NX(0)` |
| `FMIN`/`FMAX`/`FMINM`/`FMAXM` | 2 | `NV(4)` (sNaN) |
| `FSGNJ`/`FSGNJN`/`FSGNJX`, `FLI`, moves, loads, stores | 2 | none |
| `FEQ`/`FLT`/`FLE`/`FLEQ`/`FLTQ` | 2 | `NV(4)` (sNaN; quiet compares differ) |
| `FCLASS` | 2 | none |
| `FCVT` to integer | 2 | `NV(4)`, `NX(0)` |
| `FCVT` from integer | 2 | `OF(2)`, `NX(0)` |
| `FCVT` FP-to-FP, `FCVT.BF16.S`, `FCVT.S.BF16` | 2 | `NV(4)`, `OF(2)`, `UF(1)`, `NX(0)` |
| `FROUND`/`FROUNDNX`/`FCVTMOD` | 2 | `NV(4)`, `NX(0)` |
| `FRCSR`/`FSCSR`/`FRRM`/`FSRM`/`FRFLAGS`/`FSFLAGS` | 2 | none |
| Loads | 2, 3, 4, 5, 13, 21 | none |
| Stores | 2, 3, 6, 7, 15, 23 | none |

The IDs are listed in increasing order; the order in which they are reported when several apply is
given in §7.1.1. The table lists the codes the formulas carry. Every group can also trap on its own
fetch (1, 3, 12, and, with `H` and `V=1`, 20); those outcomes depend only on `PC`, are the same for
every instruction, and are stated in §7.1.2 rather than written into the formulas. The
`zfinx` forms of these groups raise 2 and 22 and no memory code, because their operands are all
registers.

## 8. Instruction files

All instruction files are in `instructions/`; this README stays at the directory root. Each file
contains the formulas for one mnemonic group. `F` is the format parameter; a file that
applies to all four formats carries `(F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})` on the
left and `(instr=MNEMONIC.F)` as the last conjunct. A file that applies to one format writes the
concrete suffix.

### Arithmetic and FMA

| File | Mnemonics | Formats | Status |
|---|---|---|---|
| [fadd.md](instructions/fadd.md) | `FADD` | H, S, D, Q | complete |
| [fsub.md](instructions/fsub.md) | `FSUB` | H, S, D, Q | complete |
| [fmul.md](instructions/fmul.md) | `FMUL` | H, S, D, Q | complete |
| [fdiv.md](instructions/fdiv.md) | `FDIV` | H, S, D, Q | complete |
| [fsqrt.md](instructions/fsqrt.md) | `FSQRT` | H, S, D, Q | complete |
| [fmadd.md](instructions/fmadd.md) | `FMADD` | H, S, D, Q | complete |
| [fmsub.md](instructions/fmsub.md) | `FMSUB` | H, S, D, Q | complete |
| [fnmsub.md](instructions/fnmsub.md) | `FNMSUB` | H, S, D, Q | complete |
| [fnmadd.md](instructions/fnmadd.md) | `FNMADD` | H, S, D, Q | complete |

### Minimum, maximum, sign, compare, classify

| File | Mnemonics | Formats | Status |
|---|---|---|---|
| [fmin.md](instructions/fmin.md) | `FMIN` | H, S, D, Q | complete |
| [fmax.md](instructions/fmax.md) | `FMAX` | H, S, D, Q | complete |
| [fminm.md](instructions/fminm.md) | `FMINM` | H, S, D, Q | complete |
| [fmaxm.md](instructions/fmaxm.md) | `FMAXM` | H, S, D, Q | complete |
| [fsgnj.md](instructions/fsgnj.md) | `FSGNJ`, `FSGNJN`, `FSGNJX` | H, S, D, Q | complete |
| [feq.md](instructions/feq.md) | `FEQ` | H, S, D, Q | complete |
| [flt.md](instructions/flt.md) | `FLT` | H, S, D, Q | complete |
| [fle.md](instructions/fle.md) | `FLE` | H, S, D, Q | complete |
| [fleq.md](instructions/fleq.md) | `FLEQ` | H, S, D, Q | complete |
| [fltq.md](instructions/fltq.md) | `FLTQ` | H, S, D, Q | complete |
| [fclass.md](instructions/fclass.md) | `FCLASS` | H, S, D, Q | complete |

### Conversion

| File | Mnemonics | Formats | Status |
|---|---|---|---|
| [fcvt-to-int.md](instructions/fcvt-to-int.md) | `FCVT.W`, `FCVT.WU`, `FCVT.L`, `FCVT.LU` | H, S, D, Q | complete |
| [fcvt-from-int.md](instructions/fcvt-from-int.md) | `FCVT.F.W`, `FCVT.F.WU`, `FCVT.F.L`, `FCVT.F.LU` | H, S, D, Q | complete |
| [fcvt-fp-fp.md](instructions/fcvt-fp-fp.md) | `FCVT.dst.src` | H, S, D, Q | complete |
| [fround.md](instructions/fround.md) | `FROUND` | H, S, D, Q | complete |
| [froundnx.md](instructions/froundnx.md) | `FROUNDNX` | H, S, D, Q | complete |
| [fcvttmod.md](instructions/fcvttmod.md) | `FCVTMOD.W.D` | D | complete |
| [bf16.md](instructions/bf16.md) | `FCVT.BF16.S`, `FCVT.S.BF16` | BF16 | complete |

### Move, load, store, CSR

| File | Mnemonics | Formats | Status |
|---|---|---|---|
| [fmv-w.md](instructions/fmv-w.md) | `FMV.X.W`, `FMV.W.X` | S | complete |
| [fmv-d.md](instructions/fmv-d.md) | `FMV.X.D`, `FMV.D.X` | D | complete |
| [fmv-h.md](instructions/fmv-h.md) | `FMV.X.H`, `FMV.H.X` | H | complete |
| [fmvh.md](instructions/fmvh.md) | `FMVH.X.D`, `FMVH.X.Q` | D, Q | complete |
| [fmvp.md](instructions/fmvp.md) | `FMVP.D.X`, `FMVP.Q.X` | D, Q | complete |
| [fli.md](instructions/fli.md) | `FLI` | H, S, D, Q | complete |
| [flw.md](instructions/flw.md) | `FLW` | S | complete |
| [fld.md](instructions/fld.md) | `FLD` | D | complete |
| [flq.md](instructions/flq.md) | `FLQ` | Q | complete |
| [flh.md](instructions/flh.md) | `FLH` | H | complete |
| [fsw.md](instructions/fsw.md) | `FSW` | S | complete |
| [fsd.md](instructions/fsd.md) | `FSD` | D | complete |
| [fsq.md](instructions/fsq.md) | `FSQ` | Q | complete |
| [fsh.md](instructions/fsh.md) | `FSH` | H | complete |
| [fcsr.md](instructions/fcsr.md) | `FRCSR`, `FSCSR`, `FRRM`, `FSRM`, `FRFLAGS`, `FSFLAGS` | — | complete |

### Integer register forms

| File | Mnemonics | Formats | Status |
|---|---|---|---|
| [zfinx.md](instructions/zfinx.md) | the whole scalar FP set on x-registers | S, D, H | complete |

## 9. Validation

```bash
python3 -I tools/check_md.py    specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md
python3 -I tools/check_style.py specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md
python3 -I tools/check_md.py    specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/instructions/fadd.md
python3 -I tools/check_style.py specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/instructions/fadd.md
```

Run both commands on every file in `instructions/` as well.

Both must pass for this file and for every instruction file before it is marked complete.
