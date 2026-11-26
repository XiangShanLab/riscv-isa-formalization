# RISC-V Vector Floating-Point Formalization

This directory formalizes the vector floating-point part of the RISC-V instruction set manual:
Chapter 31 §31.13 (vector floating-point arithmetic), §31.14.3 and §31.14.4 (floating-point
reductions), §31.16.2 (floating-point scalar moves), §31.16.3.4 and §31.16.3.6 (floating-point
slide-1 instructions), and Chapter 25 §25.4.2, §25.4.3, §25.5.3–§25.5.5 (vector BF16). It covers
the `V` extension with its floating-point element widths and the extensions `Zvfh`, `Zvfhmin`,
`Zvfbfmin`, and `Zvfbfwma`. Integer vector instructions, vector loads and stores, mask instructions,
permutation instructions other than the two floating-point slides, `vsetvl`/`vsetvli`/`vsetivli`,
and whole-register moves are outside this directory.

Every instruction file contains only formulas: one formula per distinguishable result category.
All shared material — the vector configuration, the element and mask write model, symbols, value
classes, operations, rounding rules, status rules, and exception codes — is defined once in this
file. A formula in an instruction file may be read on its own with only this file as context.

## 1. Formula shape

Every formula has the form

$$
\text{privileged configuration}\ \land\ \text{extension configuration}\ \land\ \text{vector and floating-point state}\ \land\ \text{operands}\ \land\ \mathrm{instr}=I
\ \longrightarrow\
\{\, \text{updates} \,\}.
$$

The left-hand groups appear in this order:

1. the privileged configuration, on the first line;
2. the extension configuration: `impl(V)` and the width-conditional scalar extension;
3. the vector and floating-point context status: `mstatus.VS` and `mstatus.FS`, both required to be
   enabled for every instruction of this directory; the `FS` Dirty *assignment* is conditional on
   the instruction modifying floating-point state (§4.2);
4. the rounding-mode validity `fcsr.frm∈{0,…,4}`;
5. the vector configuration: `vill`, the element width, `vl`, `vstart`, and the mask bit;
6. the operand bindings: vector elements, the scalar `f` source, and the mask register;
7. the format or form condition;
8. the instruction conjunct, always last.

The right-hand side lists, in order: the destination (a vector register-group image, a mask
register image, the scalar `f[rd]`, or element 0 of a vector register), the `vstart` reset, the
`VS` and `FS` writes of §4.2, the sticky flag increment `fcsr.fflags \mathrel{|}= S`, and
`exception` last. A field that the instruction never changes is absent.

Formula 0 of every instruction file is the illegal-instruction configuration: when the extension is
unavailable, the vector or floating-point context is Off, `vill=1`, or an instruction-specific
condition holds, the instruction writes nothing and raises `IllegalInstruction(2)`. A formula's
`exception` field lists only the exceptions the instruction itself can raise, and reads
`\mathrm{exception}=\varnothing` when it can raise none. Outcomes that belong to the instruction
fetch are common to every instruction, depend only on `PC`, and are stated once in §4.7 instead of
being repeated in each formula. When a listed code applies, the block's register, `vstart`, `VS`,
`FS`, and flag updates do not occur.

In every result category the three privileged configurations are written separately, and the first
left-hand line of each copy fixes that configuration. Whether the hypervisor extension `H` is
implemented decides which mode names exist (Priv. Table 1, `sources/riscv-privileged.txt:748-752`,
and Table 44, `sources/riscv-privileged.txt:8719-8727`):

| Privilege line | Configuration |
|---|---|
| `¬impl(H) ∧ Priv∈{M,S,U}` | no hypervisor extension: the supervisor mode is `S` |
| `impl(H) ∧ Priv∈{M,HS,U}` | hypervisor extension, `V=0`: the supervisor mode is `HS` |
| `impl(H) ∧ (Priv∈{VS,VU} ∧ vsstatus.VS∈{1,2,3} ∧ sstatus.VS∈{1,2,3} ∧ vsstatus.FS∈{1,2,3} ∧ sstatus.FS∈{1,2,3})` | hypervisor extension, `V=1`: a guest runs in `VS` or `VU` |

In the first two configurations the only context gates are the later `mstatus.VS` and
`mstatus.FS` conjuncts. In the third, both the guest fields and the HS-level fields must be enabled;
because `sstatus.VS` and `sstatus.FS` are `mstatus.VS` and `mstatus.FS`, the later conjuncts name
the same fields. Because each block fixes one configuration, its right-hand side carries only that
configuration's status writes. Together with the `VS` and `FS` conjuncts the three lines exhaust the
negation of formula 0's privilege and context disjuncts, so every privileged configuration either
enters a result block or raises `IllegalInstruction(2)`.

### 1.1 Parameters, not disjunctions over results

As in the scalar deliverable, a formula may be schematic in a parameter whose value is fixed by the
left side: there the format `F` and the mnemonic suffix, here the instruction form `\mathrm{form}`
(`\mathrm{VV}` or `\mathrm{VF}`) and the element index `i`. Symbols such as `\mathrm{enc}_w`,
`\mathrm{fsrc}_w`, and the operation functions of §7 are defined for every value of the parameter,
so the right side determines one result for every execution that satisfies the left side.

A left-side disjunction is used only in two ways. The first is a guard block, where every disjunct
produces the same `IllegalInstruction(2)` result. The second is a binding disjunction such as

$$
b_i=\mathrm{el}^{w}_{m}(vs1,i)\ \lor\ b_i=\mathrm{fsrc}_{w}(f[rs1]),
$$

which introduces a symbol `b_i` and constrains it; the result expression is a single expression in
`b_i`, so it does not depend on which disjunct holds. A result that would change with the disjunct
is always split into separate blocks.

An instruction file may introduce a per-file operation indexed by its mnemonic parameter, written
with the parameter as a subscript, such as `\mathrm{mm}_{\mathrm{op}}` in `vfminmax.md` or
`\mathrm{sgn}_{\mathrm{op}}` in `vfsgnj.md`; it is defined once in that file's prose. Such a
function is a shorthand for one of the operations of §7–§9, not a new rule.

## 2. Symbols

These are the only symbols used in the instruction files. A new symbol must be added here first.

| Symbol | Meaning | Values or form | Source |
|---|---|---|---|
| `Priv` | Current privilege mode | `U`, `S`, `HS`, `M`, `VS`, `VU` | Priv. Tables 1 and 44 |
| `mstatus.VS` | Vector state, M/HS/U view | `Off(0)`, `Initial(1)`, `Clean(2)`, `Dirty(3)` | Priv. Table 13 |
| `mstatus.FS` | Floating-point state, M/HS/U view | same | Priv. Table 13 |
| `sstatus.VS`, `sstatus.FS` | HS-level view; the same fields as `mstatus.VS`, `mstatus.FS` | same | Priv. §15.2.11 |
| `vsstatus.VS`, `vsstatus.FS` | Vector and floating-point state in VS/VU | same | Priv. Table 13 |
| `impl(X)` | Extension X is implemented | boolean; X is a manual extension name | Priv. §3.1 and the extension chapters |
| `V` | Vector extension | boolean | Unpriv. §31.18.3 |
| `H` | Hypervisor extension | boolean | Priv. §15 |
| `F`, `D` | Scalar single- and double-precision extensions | boolean | Unpriv. Chapters 21–22 |
| `Zvfh`, `Zvfhmin` | Vector half-precision extensions | boolean | Unpriv. §31.18.4–§31.18.5 |
| `Zvfbfmin`, `Zvfbfwma` | Vector BF16 extensions | boolean | Unpriv. §25.4.2–§25.4.3 |
| `\mathrm{VLEN}` | Vector register length in bits | power of two, at least 128 | Unpriv. §31.2 |
| `\mathrm{vlenb}` | `VLEN/8` | implementation-defined | Unpriv. §31.3.6 |
| `vill` | `vtype` illegal-value bit, `vtype[XLEN-1]` | 0, 1 | Unpriv. §31.3.4.4 |
| `vta` | Tail-agnostic bit, `vtype[6]` | 0, 1 | Unpriv. §31.3.4.3 |
| `vma` | Mask-agnostic bit, `vtype[7]` | 0, 1 | Unpriv. §31.3.4.3 |
| `\mathrm{vsew}` | `vtype[5:3]` | 0–3; 4–7 reserved | Unpriv. Table 44 |
| `\mathrm{vlmul}` | `vtype[2:0]` | 0–3 and 5–7; 4 reserved | Unpriv. §31.3.4.2 |
| `\mathrm{SEW}` | Selected element width | `2^{\mathrm{vsew}+3}` | Unpriv. §31.3.4.1 |
| `\mathrm{LMUL}` | Register-group multiplier | `1/8`, `1/4`, `1/2`, 1, 2, 4, 8 | Unpriv. §31.3.4.2 |
| `vl` | Vector length register | `0 ≤ vl ≤ VLMAX` | Unpriv. §31.3.5 |
| `vstart` | Start-index register | `0 ≤ vstart < VLMAX`; larger values reserved | Unpriv. §31.3.7 |
| `\mathrm{VLMAX}` | Maximum element count for the current SEW and LMUL | `LMUL·VLEN/SEW` | Unpriv. §31.3.4.2 |
| `\mathrm{vm}` | Mask bit of the encoding | 0 (masked), 1 (unmasked) | Unpriv. §31.5.3.1 |
| `\mathrm{form}` | Instruction form | `\mathrm{VV}`, `\mathrm{VF}`, `\mathrm{WV}`, `\mathrm{WF}` | Unpriv. §31.10 |
| `\mathrm{instr}` | Instruction being executed | mnemonic with form suffix | — |
| `\mathrm{EEW}`, `\mathrm{EMUL}` | Effective element width and group multiplier of an operand | per instruction | Unpriv. §31.5.2 |
| `w` | Element width of the destination image | 8, 16, 32, or 64 | — |
| `N(w,m)` | Number of `w`-bit element slots in the register image of EMUL `m`: `max(1,m)·VLEN/w` | integer | Unpriv. §31.4 |
| `\mathrm{el}^{w}_{m}(r,i)` | Element `i` of width `w` in the register group of EMUL `m` starting at register `r` | `w`-bit vector | §3.2 |
| `\mathrm{Im}^{w}_{m}(r)` | Register image holding that group: `max(1,m)` registers concatenated low-to-high | bit string | §3.2 |
| `\mathrm{bit}(W,i)` | Bit `i` of an image or register | 0, 1 | — |
| `\mathrm{Upd}_{w}(W,I,f)` | Image `W` with element `i` replaced by `f(i)` for every `i∈I` | image | §3.4 |
| `\mathrm{Agn}_{w}(W,I)` | Set of images equal to `W` outside `I` and, on `I`, each element either `W` or all ones | set of images | §3.4 |
| `\mathrm{Act}`, `\mathrm{Inact}`, `\mathrm{Tail}` | Active, inactive, and tail index sets | sets of indices | §3.3 |
| `\mathrm{Out}`, `\mathrm{MOut}` | Permitted destination image of a vector or mask write | set of images | §3.4 |
| `\mathrm{qNaN}_w` | Canonical quiet NaN of a `w`-bit format | `s=0`, `e=e_{\max}`, `f=2^{w_f-1}` | §5.2; Unpriv. §21.3 |
| `\mathrm{qNaN}_{\mathrm{B}}` | Canonical quiet NaN of BF16 | 16-bit value `\mathrm{enc}` of that triple | §8.4; Unpriv. §25.2 |
| `\mathrm{val}_w(a)` | Numeric value of a `w`-bit field triple | real, infinity, or undefined for NaN | §5.2 |
| `\mathrm{enc}_w(v)` | `w`-bit encoding of a value class | `w`-bit vector | §5.2 |
| `\mathrm{boxed}_w(f[r])` | The upper `FLEN-w` bits of `f[r]` are all ones | boolean | §5.3; Unpriv. §22.2 |
| `\mathrm{fsrc}_w(f[r])` | Scalar `f` source of width `w` | low `w` bits if boxed, else `\mathrm{qNaN}_w` | §5.3 |
| `\mathrm{uint}_w(b)`, `\mathrm{sint}_w(b)` | Unsigned and two's-complement signed value of `w` bits | integer | §8.1 |
| `fcsr.frm` | Dynamic rounding mode | `RNE(0)`, `RTZ(1)`, `RDN(2)`, `RUP(3)`, `RMM(4)`; 5–7 reserved | §4.3; Unpriv. Table 24 |
| `\mathrm{ROD}` | Round-to-odd, used only by `vfncvt.rod.f.f.w` | mode | §8.3; Unpriv. §31.13.19 |
| `\mathrm{fcsr.fflags}` | Sticky floating-point flags | `NV(4)`, `DZ(3)`, `OF(2)`, `UF(1)`, `NX(0)` | Unpriv. §21.2 |
| `S` | Flag set of one element operation | subset of `{NV(4),DZ(3),OF(2),UF(1),NX(0)}` | §6.2 |
| `\pi_1`, `\pi_2` | First and second projection of a pair `(value, flags)` | — | §6.2 |
| `\bigcup` | Union over an index set, used only for flags | — | §7.2 |
| `exception` | Synchronous exception outcome of the instruction itself | `\varnothing` when the block raises none; otherwise `\{X\}` with the block's own code | §4.6–§4.7 |
| `\mathrm{add}_w`, `\mathrm{mul}_w`, `\mathrm{div}_w`, `\mathrm{fma}_w`, `\mathrm{sqrt}_w` | Flagged IEEE arithmetic operations | pair `(value, flags)` | §7.3 |
| `\mathrm{minNum}_w`, `\mathrm{maxNum}_w` | RISC-V `FMIN`/`FMAX` minimumNumber and maximumNumber | pair | §7.4 |
| `\mathrm{cmp}_{P,w}` | Floating-point comparison predicate `P` | pair `(0 or 1, flags)` | §7.5 |
| `\mathrm{class}_w` | Ten-bit `FCLASS` code | integer | §7.6 |
| `\mathrm{sgnj}_w`, `\mathrm{sgnjn}_w`, `\mathrm{sgnjx}_w` | Bit-level sign injection | `w`-bit vector | §7.7 |
| `\mathrm{op}` | Mnemonic-selecting parameter of an instruction file | fixed by the left side | §1.1 |
| `\mathrm{mm}_{\mathrm{op}}` | `\mathrm{minNum}` or `\mathrm{maxNum}`, selected by `op` | pair | §7.4; `vfminmax` |
| `\mathrm{sgn}_{\mathrm{op}}` | `\mathrm{sgnj}`, `\mathrm{sgnjn}`, or `\mathrm{sgnjx}`, selected by `op` | `w`-bit vector | §7.7; `vfsgnj` |
| `\mathrm{f2i}^{\sigma}_{v\to w,\mu}`, `\mathrm{i2f}^{\sigma}_{w\to v,\mu}` | Float–integer conversions, `σ∈{\mathrm{s},\mathrm{u}}`, rounding mode written as `\mu` | pair | §8.1–§8.2 |
| `\mathrm{f2f}_{v\to u,\mu}`, `\mathrm{f2f}^{\mathrm{rod}}_{v\to u}` | Float–float conversions | pair | §8.3 |
| `\mathrm{widen}_{v\to u}` | Exact widening of a `v`-bit value to `u=2v` bits | value class | §8.3 |
| `\mathrm{bf16to32}`, `\mathrm{f2bf16}_{\mu}`, `\mathrm{fsrc}_{\mathrm{B}}` | BF16 widening, narrowing, and scalar `f` source | pair or 16-bit field | §8.4 |
| `\mathrm{box}_w(b)` | Place a `w`-bit field into the low bits of an `f` register | `\mathrm{FLEN}`-bit value | §5.3 |
| `\mathrm{SOut}_w`, `\mathrm{Rout}_{w_d}` | Permitted image of a single-register write of element 0 and of a reduction destination | set of images | §3.4, §9.1 |
| `\mathrm{fold}_{\oplus}` | Ordered fold of a pair-valued function over an index set | pair | §9.1 |
| `\mathrm{ordsum}_w`, `\mathrm{ordmax}_w`, `\mathrm{ordmin}_w` | Deterministic reduction folds | pair | §9.1 |
| `\mathrm{usum}_w` | Set of permitted unordered-sum outcomes | set of pairs | §9.2 |
| `\mathrm{rsqrt7}_w`, `\mathrm{rec7}_w` | Reciprocal square-root and reciprocal estimates | pair | §9.3–§9.4 |

## 3. Vector configuration

### 3.1 `vtype`

`vtype` has the fields `vill` at bit `XLEN-1`, zero bits at `XLEN-2:8`, `vma` at bit 7, `vta` at
bit 6, `vsew` at bits 5:3, and `vlmul` at bits 2:0 (Unpriv. Table 43,
`sources/riscv-unprivileged.txt:14880-14930`). `vtype` is written only by the configuration-setting
instructions; every formula in this directory assumes a `vtype` value that such an instruction can
leave behind: either `vill=1` with all other bits zero, or `vill=0` with a non-reserved `vsew` and
`vlmul` and zero reserved bits. A `vtype` with `vill=1` makes every instruction here raise
`IllegalInstruction(2)` (§4.4).

| `vsew` | `SEW` | | `vlmul` | `LMUL` |
|---|---|---|---|---|
| 000 | 8 | | 000 | 1 |
| 001 | 16 | | 001 | 2 |
| 010 | 32 | | 010 | 4 |
| 011 | 64 | | 011 | 8 |
| 1xx | reserved | | 100 | reserved |
| — | — | | 101 | 1/8 |
| — | — | | 110 | 1/4 |
| — | — | | 111 | 1/2 |

The number of elements in a vector register group is

$$
\mathrm{VLMAX}=\mathrm{LMUL}\cdot\mathrm{VLEN}/\mathrm{SEW}.
$$

Every configuration formalized here has `LMUL·VLEN ≥ SEW`, so `VLMAX` is a positive integer. A
configuration with a smaller product gives no complete element slot; it is outside these formulas
and implementations may make such a `vtype` unsupported (Unpriv. §31.6.1.1,
`sources/riscv-unprivileged.txt:16023-16044`). `vl` is set only by the configuration-setting
instructions and satisfies `vl ≤ VLMAX` (Unpriv. §31.6.3, `sources/riscv-unprivileged.txt:16093-16128`).
`vstart` has writable bits for indices below the largest `VLMAX`; a value greater than the largest
element index of the current configuration is reserved (Unpriv. §31.3.7,
`sources/riscv-unprivileged.txt:15210-15268`), so every formula assumes `vstart < VLMAX`.

### 3.2 Element and mask layout

For an operand with effective element width `w=EEW` and effective group multiplier `m=EMUL`, the
register image is the concatenation of `max(1,m)` whole vector registers beginning at the register
named by the operand, lowest-numbered register first and least-significant bit first:

$$
\mathrm{Im}^{w}_{m}(r)=\mathrm{V}_{r}\ \Vert\ \mathrm{V}_{r+1}\ \Vert\ \cdots\ \Vert\ \mathrm{V}_{r+\max(1,m)-1},
\qquad
\mathrm{el}^{w}_{m}(r,i)=\mathrm{Im}^{w}_{m}(r)\,[\,iw+w-1:iw\,].
$$

When `m<1`, only the low `m·VLEN` bits of `V_r` carry the group's elements; the remaining bits of
the same register are part of the tail (Unpriv. §31.4.2, `sources/riscv-unprivileged.txt:15445-15463`).
The number of element slots in the image is `N(w,m)=max(1,m)·VLEN/w`.

Mask elements are single bits: element `i` of the mask held in vector register `r` is
`\mathrm{bit}(\mathrm{V}_{r},i)`. The mask register is always one register, whatever the `LMUL`
setting (Unpriv. §31.4.5, `sources/riscv-unprivileged.txt:15612-15619`). The source mask register is
always register 0, and its element `i` is written `\mathrm{M}[i]` for
`\mathrm{M}=\mathrm{V}_{0}`.

### 3.3 Element classes

With the initial values of `vl` and `vstart`, the destination element indices are partitioned as
(Unpriv. §31.5.4, `sources/riscv-unprivileged.txt:15866-15920`):

$$
\mathrm{Act}(vl,vstart,\mathrm{vm},M)=\{\,i\mid vstart\le i<vl\ \land\ (\mathrm{vm}=1\ \lor\ \mathrm{bit}(M,i)=1)\,\},
$$

$$
\mathrm{Inact}(vl,vstart,\mathrm{vm},M)=\{\,i\mid vstart\le i<vl\ \land\ \mathrm{vm}=0\ \land\ \mathrm{bit}(M,i)=0\,\},
$$

$$
\mathrm{Tail}(N,vl,vstart)=\{\,i\mid vl\le i<N\ \land\ vstart<vl\,\}.
$$

The elements below `vstart` are prestart elements: they do not raise exceptions and are not
updated. The active elements can raise exceptions and are written with the instruction result. The
inactive elements never raise exceptions; they are left undisturbed or made agnostic by `vma`. The
tail elements never raise exceptions; they are left undisturbed or made agnostic by `vta`. When
`vstart ≥ vl` there are no body elements, and no destination element, including a tail element, is
updated; this is why `\mathrm{Tail}` carries the conjunct `vstart<vl` (Unpriv. §31.5.4,
`sources/riscv-unprivileged.txt:15905-15917`). Instructions that write an `f` register do so even
when `vstart ≥ vl`.

### 3.4 Destination write model

For an undisturbed destination, every active element receives the instruction's result and every
other element keeps its previous value:

$$
\mathrm{Upd}_{w}(W,I,f)=W\ \text{with element } i \text{ replaced by } f(i) \text{ for every } i\in I.
$$

The agnostic policy permits each element of a set to keep its old value or to be overwritten with
all ones, independently and nondeterministically (Unpriv. §31.3.4.3,
`sources/riscv-unprivileged.txt:15074-15164`):

$$
\mathrm{Agn}_{w}(W,I)=\{\,W'\mid \forall i\notin I:\ W'[iw+w-1:iw]=W[iw+w-1:iw],\quad
\forall i\in I:\ W'[iw+w-1:iw]\in\{W[iw+w-1:iw],\ 2^{w}-1\}\,\}.
$$

For a vector destination of element width `w` and group multiplier `m`, the permitted images after
an instruction whose per-element result is `f(i)` are

$$
\mathrm{Out}_{w,m}(W,f,vl,vstart,\mathrm{vm},M,vta,vma)=
\mathrm{Agn}_{w}\Bigl(\mathrm{Upd}_{w}\bigl(W,\mathrm{Act}(vl,vstart,\mathrm{vm},M),f\bigr),\
\bigl(\mathrm{vma}=1\ ?\ \mathrm{Inact}(vl,vstart,\mathrm{vm},M)\ :\ \varnothing\bigr)
\ \cup\
\bigl(\mathrm{vta}=1\ ?\ \mathrm{Tail}(N(w,m),vl,vstart)\ :\ \varnothing\bigr)\Bigr).
$$

`W` is the image before the instruction and `N(w,m)=max(1,m)·VLEN/w`. The set is a singleton
exactly when no element of the inactive or tail set is agnostic. This single definition covers all
four `vta`/`vma` combinations and the `vstart ≥ vl` case, because its tail set is empty then.

For a mask destination, the destination register image has `VLEN` bits, one per element. A
mask-producing instruction writes each active bit with the predicate value `p(i)`, and its tail is
always agnostic regardless of `vta`; a tail bit may additionally be written with the value the
operation would have computed with `vl=VLMAX` when that index is below `VLMAX` (Unpriv. §31.3.4.3,
`sources/riscv-unprivileged.txt:15118-15132`). With `W` the mask image before the instruction,

$$
\mathrm{MOut}(W,p,vl,vstart,\mathrm{vm},M,vma)=\{\,W'\mid
\begin{array}{l}
i<vstart\ \Rightarrow\ W'[i]=W[i],\\
i\in\mathrm{Act}(vl,vstart,\mathrm{vm},M)\ \Rightarrow\ W'[i]=p(i),\\
i\in\mathrm{Inact}(vl,vstart,\mathrm{vm},M)\ \Rightarrow\
  W'[i]=W[i]\ \text{if } vma=0,\ \text{else } W'[i]\in\{W[i],1\},\\
vl\le i<\mathrm{VLEN}\ \land\ vstart<vl\ \Rightarrow\
  W'[i]\in\{W[i],1\}\ \cup\ \{\,p(i)\mid i<\mathrm{VLMAX}\,\}
\end{array}\,\}.
$$

When `vstart ≥ vl` every set is the singleton `{W}`. The conjunct `i < VLMAX` in the last line is
the manual's permission to write the tail with the value computed for `vl=VLMAX`; above `VLMAX`
only the two ordinary agnostic choices remain.

A single-register destination whose element 0 is written and whose other slots are tail elements —
a reduction result, `vfmv.s.f` — uses

$$
\mathrm{SOut}_{w}(W,v,c,vta)=
\begin{cases}
\{W\}, & \neg c,\\
\mathrm{Agn}_{w}\bigl(\mathrm{Upd}_{w}(W,\{0\},\lambda i.v),\
\mathrm{vta}=1\ ?\ \{1,\ldots,N(w,1)-1\}\ :\ \varnothing\bigr), & c,
\end{cases}
$$

with `N(w,1)=VLEN/w` the number of slots of one register. The condition `c` carries the
instruction's own guard: `vstart<vl` for an instruction that is skipped when `vstart ≥ vl`, and
`vl>0` for a reduction, which is illegal for `vstart≠0` (§4.4).

## 4. Extensions, context status, and exceptions

### 4.1 Extension conditions

The `V` extension depends on the scalar `F` and `D` extensions and implements the vector
floating-point instructions for `EEW=32` and `EEW=64`, including widening and narrowing conversions
between FP32 and FP64 (Unpriv. §31.18.3, `sources/riscv-unprivileged.txt:20631-20676`). The
half-precision element width is enabled by `Zvfh`; `Zvfhmin` enables only `vfwcvt.f.f.v` and
`vfncvt.f.f.w` at `SEW=16` (Unpriv. §31.18.4–§31.18.5, `sources/riscv-unprivileged.txt:20677-20711`).
The BF16 instructions are enabled by `Zvfbfmin`, and `vfwmaccbf16` by `Zvfbfwma` (Unpriv.
§25.4.2–§25.4.3, `sources/riscv-unprivileged.txt:8155-8209`).

For an instruction whose floating-point elements are `SEW` wide, define

$$
\mathrm{Ext}_{\mathrm{fp}}(w)=\mathrm{impl}(V)\land(w=16\Rightarrow\mathrm{impl}(Zvfh))
\land(w=32\Rightarrow\mathrm{impl}(F))\land(w=64\Rightarrow\mathrm{impl}(D)).
$$

For `vfwcvt.f.f.v` and `vfncvt.f.f.w`, whose `SEW=16` case is also provided by `Zvfhmin`, use

$$
\mathrm{Ext}_{\mathrm{fmin}}(w)=\mathrm{impl}(V)\land(w=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))
\land(w=32\Rightarrow\mathrm{impl}(D)).
$$

The remaining conversions gate on the width whose floating-point format they use, not always on the
source width: §8.5 lists the exact condition of every conversion form. The BF16 files use
`impl(V)∧impl(Zvfbfmin)` or `impl(V)∧impl(Zvfbfwma)`. An instruction whose element width is not a
supported floating-point width for that form has a reserved encoding (§4.5); the formulas state the
supported widths in their format conjunct.

### 4.2 Context status

A vector instruction raises `IllegalInstruction(2)` when `mstatus.VS` is Off. When `V=1`, both
`vsstatus.VS` and `mstatus.VS` are in effect and either being Off is illegal. Executing an
instruction that changes vector state sets `mstatus.VS` to Dirty, and in `V=1` sets both
`mstatus.VS` and `vsstatus.VS` to Dirty (Unpriv. §31.3.2–§31.3.3,
`sources/riscv-unprivileged.txt:14829-14879`).

A vector floating-point instruction additionally requires `mstatus.FS` to be enabled and, when
`V=1`, `vsstatus.FS` as well; either being Off raises `IllegalInstruction(2)`. An instruction that
modifies floating-point extension state — an `f` register or the floating-point CSRs — must set
`mstatus.FS` to Dirty, and in `V=1` both `mstatus.FS` and `vsstatus.FS` (Unpriv. §31.13,
`sources/riscv-unprivileged.txt:18308-18325`).

The formulas use the conservative strategy for both fields: a block carries the `VS` assignment
because every vector instruction updates vector state or resets `vstart`, and it carries the `FS`
assignment exactly when the instruction can modify `f` registers or `fcsr` for some execution with
that configuration, including a flag raised only by particular operand values. The privileged
specification permits setting Dirty when the state is not actually modified (Priv. §15.2.3,
`sources/riscv-privileged.txt:2333-2346`), so the assignments are sufficient but may be coarser than
the minimal set. In the `VS/VU` blocks the `VS` and `FS` assignments name both the guest field and
the HS-level field, and all four assignments occur together.

### 4.3 Rounding mode

Every vector floating-point instruction requires a valid dynamic rounding mode in `fcsr.frm`, even
when it does not round, when `vl=0`, or when `vstart ≥ vl`; use of a reserved value is reserved
(Unpriv. §31.10.1, `sources/riscv-unprivileged.txt:17129-17132`). Every result block therefore
carries `fcsr.frm∈{RNE(0),RTZ(1),RDN(2),RUP(3),RMM(4)}`. The reserved values 5–7 are outside every
formula: they appear neither as a result nor as an exception. The effective mode is `fcsr.frm`
except for the `.rtz` conversion forms, which use `RTZ(1)`, and `vfncvt.rod.f.f.w`, which uses
`\mathrm{ROD}`.

### 4.4 `vill` and mandated illegal instructions

If `vill=1`, any attempt to execute a vector instruction that depends on `vtype` raises
`IllegalInstruction(2)` (Unpriv. §31.3.4.4, `sources/riscv-unprivileged.txt:15165-15185`). Every
instruction in this directory depends on `vtype`, so `vill=1` appears in every guard block.

A vector reduction raises `IllegalInstruction(2)` when `vstart` is non-zero (Unpriv. §31.14,
`sources/riscv-unprivileged.txt:19315-19327`); the reduction files add `vstart≠0` to their guard.
No other exception is raised by the instructions formalized here: they access no memory and no CSR
other than `fcsr`.

### 4.5 Reserved configurations

The manual marks the following configurations as reserved encodings, not as mandated exceptions.
They are outside every formula: no formula asserts a result and none asserts an exception, and an
implementation may raise `IllegalInstruction(2)` or take another reserved-encoding action.

| Reserved configuration | Source |
|---|---|
| `EEW` is not a supported floating-point width of the form (for example `SEW=8` for arithmetic, `SEW=64` for widening, `SEW=8` for a float source) | Unpriv. §31.13, `:18296-18299`; §25.5.3–§25.5.5, `:8330-8340`, `:8360-8370`, `:8390-8400` |
| `EMUL > 8`, including `LMUL=8` for a widening or narrowing form whose destination or source is `2·LMUL` | Unpriv. §31.5.2, `:15796-15802` |
| A vector register read with two different `EEW` in one instruction, or a register-group number that is not the lowest of its group | Unpriv. §31.5.2, `:15760-15772` |
| Destination and source group overlap that violates §31.5.2, and a destination overlapping the source mask register unless the destination is a mask or a reduction scalar | Unpriv. §31.5.2–§31.5.3, `:15774-15795`, `:15822-15830` |
| `vfmv.v.f` with `vs2≠v0` or `vm=1`; `vfmerge.vfm` with `vm=1`; `vfmv.f.s` and `vfmv.s.f` with `vm=0` | Unpriv. §31.13.15–§31.13.16, `:19140-19177`; §31.16.2, `:20013-20039` |
| A slide-1 form whose destination group overlaps its source group | Unpriv. §31.16.3.3–§31.16.3.4, `:20136-20186` |
| `FLEN < SEW` for an `f`-register scalar source | Unpriv. §31.10.1, `:17155-17158` |

The files state the supported `SEW` and `LMUL` domains in their format conjunct, and the
`vfmv`/`vfmerge`/slide files state their fixed `vm` and register constraints. Configurations not
covered by a file's conjuncts are outside the model.

### 4.6 Exception field

The `exception` field of a block is `\{\mathrm{IllegalInstruction}(2)\}` in a guard block and
`\varnothing` in every result block. No instruction in this directory raises any other
execution-phase exception.

### 4.7 Instruction fetch

Instruction-fetch outcomes are common to all instructions, depend only on the fetch address, and
are not repeated in the formulas. In priority order they are

$$
\mathrm{Breakpoint}(3,\mathrm{fetch})>
\mathrm{InstructionPageFault}(12)=
\mathrm{InstructionGuestPageFault}(20)=
\mathrm{InstructionAccessFault}(1,\mathrm{walk})>
\mathrm{InstructionAccessFault}(1,\mathrm{phys}),
$$

with the guest-page-fault code absent when the configuration cannot execute with `V=1`. These
outcomes precede the execution-phase `IllegalInstruction(2)` of every formula. The labels
`fetch`, `walk`, and `phys` are shorthands of this document for the manual's duplicate rows in
Priv. Table 17 and Table 51 (`sources/riscv-privileged.txt:10536-10560`).

## 5. Operands and values

### 5.1 Formats

Vector floating-point elements use the IEEE 754-2019 binary16, binary32, and binary64 formats,
selected by `SEW`, and the BF16 format of Chapter 25 for the three BF16 instructions. A format is
fixed by the widths $(w_e,w_f)$ of its exponent and fraction fields, with total width
$w=1+w_e+w_f$ and exponent bias $B=2^{w_e-1}-1$ (Unpriv. §21.3,
`sources/riscv-unprivileged.txt:10908-10950`; §25.2, `sources/riscv-unprivileged.txt:7930-7960`).

| Format | `SEW` | `w_e` | `w_f` | `w` | `B` | `e_min` | `e_max` | Largest finite | `qNaN` encoding |
|---|---|---|---|---|---|---|---|---|---|
| binary16 (H) | 16 | 5 | 10 | 16 | 15 | −14 | 15 | 65504 | 0x7E00 |
| binary32 (S) | 32 | 8 | 23 | 32 | 127 | −126 | 127 | $(2-2^{-23})\cdot2^{127}$ | 0x7FC00000 |
| binary64 (D) | 64 | 11 | 52 | 64 | 1023 | −1022 | 1023 | $(2-2^{-52})\cdot2^{1023}$ | 0x7FF8000000000000 |
| BF16 | 16 | 8 | 7 | 16 | 127 | −126 | 127 | $(2-2^{-7})\cdot2^{127}$ | 0x7FC0 |

`e_min = 1-B` and `e_max = B` are the unbiased exponents of the smallest normal and the largest
finite value. BF16 is not selected by `vtype`: the three BF16 instructions of §8.4 have a fixed
16-bit element and are enabled by their own extensions.

### 5.2 Bit fields and value classes

A `w`-bit element `b` is read as the triple

$$
s=b[w-1],\qquad e=b[w-2:w-1-w_e],\qquad f=b[w_f-1:0].
$$

The value and the class are determined as follows (Unpriv. §21.3,
`sources/riscv-unprivileged.txt:10929-10992`):

| Exponent | Fraction | Value | Class |
|---|---|---|---|
| `e=0` | `f=0` | zero with sign `s` | zero |
| `e=0` | `f≠0` | $(-1)^s\,2^{1-B}\,f/2^{w_f}$ | subnormal |
| `1 ≤ e ≤ 2B` | any | $(-1)^s\,2^{e-B}\,(1+f/2^{w_f})$ | normal |
| `e=2B+1` | `f=0` | infinity with sign `s` | infinity |
| `e=2B+1` | `f≠0` | not a number; quiet iff `f[w_f-1]=1` | NaN |

A NaN with `f[w_f-1]=0` is signaling. The ten classes are negative infinity, negative normal,
negative subnormal, negative zero, positive zero, positive subnormal, positive normal, positive
infinity, quiet NaN, and signaling NaN. The sign of a zero is part of its class and is observable
through `vfmin`, `vfmax`, `vfsgnj`, `vfclass`, and through the sign rules of §7.

`\mathrm{val}_w(b)` is the numeric real value of a normal, subnormal, or zero element and $+\infty$
or $-\infty$ of an infinity; it is undefined on a NaN. `\mathrm{enc}_w(v)` is the `w`-bit encoding
of a value class: a sign and a finite value, an infinity, or a NaN class. The canonical quiet NaN
`\mathrm{qNaN}_w` has `s=0`, `e=2B+1`, and `f=2^{w_f-1}`, so its significand is the quiet bit and
nothing else; every operation of §7 and every conversion of §8 that produces a NaN produces exactly
this encoding. Operand NaN payloads are ignored except for the quiet/signaling distinction, and
preserved only by the bit-level instructions of §7.6–§7.7 and by the moves.

### 5.3 Scalar `f` operands

A `.vf` or `.wf` form reads one scalar floating-point register. With `FLEN` the width of an `f`
register (Unpriv. §22.2, `sources/riscv-unprivileged.txt:11315-11340`),

$$
\mathrm{boxed}_w(f[r])=\bigl(\ f[r][\mathrm{FLEN}-1:w]=1^{\mathrm{FLEN}-w}\ \bigr),
\qquad
\mathrm{fsrc}_w(f[r])=
\begin{cases}
f[r][w-1:0], & \mathrm{FLEN}=w\ \text{or}\ \mathrm{boxed}_w(f[r]),\\
\mathrm{enc}_w(\mathrm{qNaN}_w), & \text{otherwise}.
\end{cases}
$$

A value that is not correctly NaN-boxed therefore contributes the canonical quiet NaN and raises no
flag (Unpriv. §31.10.1, `sources/riscv-unprivileged.txt:17144-17165`); a signaling NaN contributes
itself. `FLEN<w` is reserved (§4.5). The register is read once, and every element of the
instruction sees the same value. In `.wf` forms, `w` is the width of the narrow multiplicand or
addend, which is the source element width, not the destination width.

For the opposite direction, `\mathrm{box}_w(b)` places a `w`-bit field into an `f` register:
$\mathrm{box}_w(b)=1^{\mathrm{FLEN}-w}\Vert b$, which is the identity when `FLEN=w`. It is used by
`vfmv.f.s`.

## 6. Rounding and flags

### 6.1 The rounding function

Every floating-point result that is not exact is produced by one rounding of an exact real value
$\rho$ to a destination format. With `m` the effective rounding mode and `s_0` the sign the
operation assigns to an exact zero:

$$
\mathrm{RN}_{w,m}(\rho,s_0)=(\text{value},\ \text{flag set}).
$$

The computation is:

1. If $\rho=0$, the value is the zero of sign $s_0$, with no flags.
2. Let $\rho^{\infty}$ be $\rho$ rounded to $p=w_f+1$ significant bits with mode `m` and unbounded
   exponent range. This is the value used to detect overflow and tininess, and it never depends on
   the destination exponent range.
3. If $|\rho^{\infty}|>\mathrm{MAX}_w$, the result overflows:

   | Mode | Value for $\rho>0$ | Value for $\rho<0$ |
   |---|---|---|
   | `RNE(0)`, `RMM(4)` | $+\infty$ | $-\infty$ |
   | `RTZ(1)` | $+\mathrm{MAX}_w$ | $-\mathrm{MAX}_w$ |
   | `RDN(2)` | $+\mathrm{MAX}_w$ | $-\infty$ |
   | `RUP(3)` | $+\infty$ | $-\mathrm{MAX}_w$ |

   The flags are `OF(2)` and `NX(0)`.
4. Otherwise let $\rho^{\mathrm{g}}$ be the destination-format finite value that mode `m` selects
   for $\rho$, with magnitude capped at $\mathrm{MAX}_w$; this is the delivered value, on the
   normal or subnormal grid as appropriate. If $0<|\rho^{\infty}|<2^{e_{\min}}$ and
   $\rho^{\mathrm{g}}\ne\rho$, the flags contain `UF(1)` and `NX(0)`; if only
   $\rho^{\mathrm{g}}\ne\rho$, they contain `NX(0)`; if the value is exact, they are empty.
   `UF(1)` is never signaled without `NX(0)`.

Tininess is detected after rounding to $p$ bits with unbounded exponent, as in the scalar delivery.
The selection of $\rho^{\mathrm{g}}$ uses the destination grid directly, so a subnormal result is
not produced by double rounding. Overflow is decided on $\rho^{\infty}$, so it precedes any
saturation of $\rho^{\mathrm{g}}$.

### 6.2 Flags and their union

The floating-point flags are the five bits of `fcsr.fflags`: `NV(4)` invalid, `DZ(3)` divide by
zero, `OF(2)` overflow, `UF(1)` underflow, `NX(0)` inexact (Unpriv. §21.2,
`sources/riscv-unprivileged.txt:10812-10850`). Each element operation returns a pair
$(\text{value},S)$ with $S$ a subset of these five bits; $\pi_1$ and $\pi_2$ select the value and
the flag set. A flag is set with

$$
\mathrm{fcsr.fflags}\mathrel{|}=S,
$$

which never clears a flag.

Only active body elements contribute:

$$
\mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},M)}\pi_2(f(i)),
$$

where $f(i)$ is the pair the instruction computes for element `i` (Unpriv. §31.13.1,
`sources/riscv-unprivileged.txt:18326-18347`). Prestart, inactive, and tail elements contribute
nothing, even when `vma=1` or `vta=1` overwrites them. An instruction whose per-element function
can never produce a flag omits the `fcsr.fflags` field and the `FS` Dirty assignment; the
`mstatus.FS` *enablement* conjunct of §4.2 is present in every formula regardless. This is the case
for the sign-injection, classification, merge, move, and slide instructions. A reduction unions the
flags of the elements it actually combines, as defined in §9.

## 7. Operations

### 7.1 Sign utilities

For a value class $v$, `\mathrm{neg}_w(v)` flips the sign bit and `\mathrm{abs}_w(v)` clears it.
Both are bit operations on the encoding and apply to every class, including NaNs; neither raises a
flag. They are used only to express the sign variants of the FMA instructions.

### 7.2 Operation conventions

Every arithmetic operation of §7.3 first tests for NaN operands, then for infinities and zeros, and
only then computes a finite exact value and rounds it once with §6.1. When the exact finite result
is zero, its sign is given by the operation's rule rather than by the sign of $\rho=+0$; these
rules are the IEEE 754-2019 §6.3 rules and are stated in each table. Unless a row says otherwise,
the flags are those of the single rounding of §6.1.

### 7.3 Addition, multiplication, division, fused multiply-add, and square root

`\mathrm{add}_w(a,b)`:

| Condition | Value | Flags |
|---|---|---|
| `a` or `b` is a signaling NaN | `qNaN` | `NV(4)` |
| otherwise, `a` or `b` is a quiet NaN | `qNaN` | none |
| both are infinities of the same sign | that infinity | none |
| one is $+\infty$, the other $-\infty$ | `qNaN` | `NV(4)` |
| exactly one is infinite | that infinity | none |
| both are finite | $\mathrm{RN}_{w,m}(a+b,\ s_0)$ with $s_0=1$ iff both are negative zeros, or the mode is `RDN(2)` and not both are positive zeros | per §6.1 |

`\mathrm{sub}_w(a,b)=\mathrm{add}_w(a,\mathrm{neg}_w(b))`.

`\mathrm{mul}_w(a,b)`:

| Condition | Value | Flags |
|---|---|---|
| `a` or `b` is a signaling NaN | `qNaN` | `NV(4)` |
| otherwise, `a` or `b` is a quiet NaN | `qNaN` | none |
| one is zero, the other infinite | `qNaN` | `NV(4)` |
| one is infinite, the other finite nonzero | infinity with sign equal to the exclusive-or of the operand signs | none |
| one is zero, the other finite | zero with sign equal to the exclusive-or of the operand signs | none |
| both finite | $\mathrm{RN}_{w,m}(a\cdot b,\ s_0)$ with $s_0$ the exclusive-or of the operand signs | per §6.1 |

`\mathrm{div}_w(a,b)`:

| Condition | Value | Flags |
|---|---|---|
| `a` or `b` is a signaling NaN | `qNaN` | `NV(4)` |
| otherwise, `a` or `b` is a quiet NaN | `qNaN` | none |
| both are zero, or both are infinite | `qNaN` | `NV(4)` |
| `a` is finite nonzero, `b` is zero | infinity with the exclusive-or sign | `DZ(3)` |
| `a` is zero, `b` is finite nonzero | zero with the exclusive-or sign | none |
| `a` is infinite, `b` is finite | infinity with the exclusive-or sign | none |
| `a` is finite, `b` is infinite | zero with the exclusive-or sign | none |
| both finite | $\mathrm{RN}_{w,m}(a/b,\ s_0)$ with $s_0$ the exclusive-or of the operand signs | per §6.1 |

`\mathrm{fma}_w(a,b,c)` computes $a\cdot b+c$ with a single rounding of the exact product added to
`c`:

| Condition | Value | Flags |
|---|---|---|
| any operand is a signaling NaN | `qNaN` | `NV(4)` |
| otherwise, any operand is a quiet NaN | `qNaN` | none |
| one multiplicand is zero and the other infinite | `qNaN` | `NV(4)` |
| $a\cdot b$ is infinite and `c` is an infinity of the opposite sign | `qNaN` | `NV(4)` |
| $a\cdot b$ is infinite | that infinity | none |
| `c` is infinite | `c` | none |
| all finite | $\mathrm{RN}_{w,m}(a\cdot b+c,\ s_0)$ with $s_0=1$ iff the product is $-0$ and `c` is $-0$, or the mode is `RDN(2)` and not both are $+0$ | per §6.1 |

`\mathrm{sqrt}_w(a)`:

| Condition | Value | Flags |
|---|---|---|
| `a` is a signaling NaN | `qNaN` | `NV(4)` |
| otherwise, `a` is a quiet NaN | `qNaN` | none |
| `a` is negative and not a zero, including $-\infty$ | `qNaN` | `NV(4)` |
| `a` is a zero | that zero | none |
| `a` is $+\infty$ | $+\infty$ | none |
| `a` is positive and finite | $\mathrm{RN}_{w,m}(\sqrt{a},\ 0)$ | per §6.1 (only `NX(0)` is possible) |

### 7.4 Minimum and maximum

`\mathrm{minNum}_w(a,b)` and `\mathrm{maxNum}_w(a,b)` are the RISC-V `FMIN` and `FMAX`
operations (Unpriv. §21.8, `sources/riscv-unprivileged.txt:11076-11145`):

| Condition | `minNum` | `maxNum` | Flags |
|---|---|---|---|
| both are NaN | `qNaN` | `qNaN` | `NV(4)` if either is signaling |
| exactly one is NaN | the other operand | the other operand | `NV(4)` if the NaN is signaling |
| both are numbers, not both zero | the numerically smaller | the numerically larger | none |
| one is $+0$, the other $-0$ | $-0$ | $+0$ | none |
| both are zeros of the same sign | that zero | that zero | none |

When both operands are the same number (the same encoding, or two NaNs handled above), the returned
number is that encoding. A NaN operand never contributes its payload: the non-NaN operand is
returned unchanged, or the canonical quiet NaN when both are NaN.

### 7.5 Comparisons

`\mathrm{cmp}_{P,w}(a,b)` returns a pair whose first component is 0 or 1 and is the value written
into the mask bit:

| `P` | Operand is NaN | Otherwise | Flags |
|---|---|---|---|
| `eq` | 0 | 1 iff the values are numerically equal, with $+0=-0$ | `NV(4)` iff an operand is a signaling NaN |
| `ne` | 1 | 1 iff the values are not numerically equal | `NV(4)` iff an operand is a signaling NaN |
| `lt` | 0 | 1 iff $a<b$ | `NV(4)` if any operand is a NaN |
| `le` | 0 | 1 iff $a\le b$ | `NV(4)` if any operand is a NaN |
| `gt` | 0 | 1 iff $a>b$ | `NV(4)` if any operand is a NaN |
| `ge` | 0 | 1 iff $a\ge b$ | `NV(4)` if any operand is a NaN |

These are the manual's rules: `vmfeq` and `vmfne` raise `NV(4)` only for signaling NaNs, while the
four ordering comparisons raise it for every NaN (Unpriv. §31.13.13,
`sources/riscv-unprivileged.txt:19035-19110`). `ne` is the only comparison that returns 1 for a
NaN.

### 7.6 Classification

`\mathrm{class}_w(a)` is the ten-bit code of the scalar `FCLASS` instruction (Unpriv. §21.9,
`sources/riscv-unprivileged.txt:11147-11190`), zero-extended into the destination element:

| Bit | Class | Bit | Class |
|---|---|---|---|
| 0 | $-\infty$ | 5 | positive subnormal |
| 1 | negative normal | 6 | positive normal |
| 2 | negative subnormal | 7 | $+\infty$ |
| 3 | $-0$ | 8 | signaling NaN |
| 4 | $+0$ | 9 | quiet NaN |

Exactly one bit is set. `\mathrm{class}_w` raises no flag.

### 7.7 Sign injection

`\mathrm{sgnj}_w(a,b)`, `\mathrm{sgnjn}_w(a,b)`, and `\mathrm{sgnjx}_w(a,b)` copy the bits of `a`
and replace their sign bit by the sign bit of `b`, its complement, or its exclusive-or with the sign
of `a`, respectively (Unpriv. §21.7, `sources/riscv-unprivileged.txt:11010-11074`):

$$
\mathrm{sgnj}_w(a,b)=a\ \text{with}\ a[w-1]\leftarrow b[w-1],\qquad
\mathrm{sgnjn}_w(a,b)=a\ \text{with}\ a[w-1]\leftarrow 1-b[w-1],
$$
$$
\mathrm{sgnjx}_w(a,b)=a\ \text{with}\ a[w-1]\leftarrow a[w-1]\oplus b[w-1].
$$

All three operate on raw bits: they move NaN payloads, infinities, and zeros unchanged apart from
the sign bit, and they raise no flag.

## 8. Conversions

### 8.1 Integer values and float-to-integer conversion

`\mathrm{uint}_w(b)` is the unsigned value of the `w`-bit field `b`, and `\mathrm{sint}_w(b)` is
its two's-complement signed value. Integer elements have no sign or exponent fields: every bit is a
digit.

`\mathrm{f2i}^{\sigma}_{v\to w,m}(a)` converts a `v`-bit floating-point element to a `w`-bit integer
with signedness $\sigma\in\{\mathrm{s},\mathrm{u}\}$ (Unpriv. §31.13.17,
`sources/riscv-unprivileged.txt:19490-19610`; the scalar rule is §21.4,
`sources/riscv-unprivileged.txt:10994-11008`). The result is the `w`-bit encoding of the integer.

| Condition | Value | Flags |
|---|---|---|
| `a` is a NaN or $+\infty$ | $\sigma=\mathrm{u}$: $2^{w}-1$; $\sigma=\mathrm{s}$: $2^{w-1}-1$ | `NV(4)` |
| `a` is $-\infty$ | $\sigma=\mathrm{u}$: 0; $\sigma=\mathrm{s}$: $-2^{w-1}$ | `NV(4)` |
| `a` finite, $y=\mathrm{round}_m(\mathrm{val}_v(a))$ is outside the integer range | the nearest endpoint of the range | `NV(4)` |
| `a` finite, `y` in range, $y\ne\mathrm{val}_v(a)$ | `y` | `NX(0)` |
| `a` finite, `y` in range, $y=\mathrm{val}_v(a)$ | `y` | none |

$\mathrm{round}_m$ rounds to an integral value with mode `m`; `RNE` and `RMM` differ only at an
exact half, and the directed modes round in their direction. The saturation endpoints are
$[0,2^{w}-1]$ for unsigned and $[-2^{w-1},2^{w-1}-1]$ for signed. The range test is applied to the
rounded value `y`, not to the unrounded input.

### 8.2 Integer-to-float conversion

`\mathrm{i2f}^{\sigma}_{w\to v,m}(u)` converts an integer element to a `v`-bit floating-point
element:

$$
\mathrm{i2f}^{\sigma}_{w\to v,m}(u)=\mathrm{RN}_{v,m}(\mathrm{val}(u),\ 0),
$$

where $\mathrm{val}(u)=\mathrm{uint}_w(u)$ for $\sigma=\mathrm{u}$ and $\mathrm{val}(u)=\mathrm{sint}_w(u)$
for $\sigma=\mathrm{s}$. The flags are those of §6.1. Because every integer has magnitude at least
one, `UF(1)` is unreachable; `OF(2)` and `NX(0)` are possible when the integer exceeds the
destination precision or range. The result of a zero input is $+0$.

### 8.3 Float-to-float conversion

`\mathrm{f2f}_{v\to u,m}(a)` converts a `v`-bit floating-point element to a `u`-bit floating-point
element:

| Condition | Value | Flags |
|---|---|---|
| `a` is a signaling NaN | `qNaN` of the destination format | `NV(4)` |
| `a` is a quiet NaN | `qNaN` of the destination format | none |
| `a` is an infinity | the infinity of the same sign | none |
| `a` is a zero | the zero of the same sign | none |
| `a` is finite and nonzero | $\mathrm{RN}_{u,m}(\mathrm{val}_v(a),\ 0)$ | per §6.1 |

Every widening conversion of this directory is exact and raises no flag for a finite input. A
narrowing conversion can overflow, underflow, and round; a NaN input always yields the canonical
quiet NaN of the destination format, so payloads are not propagated across formats.

The widening instructions `vfwadd`, `vfwsub`, `vfwmul`, `vfwcvt.f.f.v`, and `vfwred` use the exact
widening of a value at one width into the next IEEE format of the table of §5.1, written

$$
\mathrm{widen}_{v\to u}(b),\qquad u=2v,
$$

which re-encodes a normal, subnormal, zero, or infinity with the same sign and value and no flag,
and maps a NaN to a NaN of the destination format with the same sign and the same quiet/signaling
class. The payload of a NaN is not modelled, because every operation of §7 that consumes it returns
the canonical quiet NaN (§5.2). This is why a signaling NaN in a widening operand raises `NV(4)`
at the later arithmetic step and not at the widening itself.

`\mathrm{f2f}^{\mathrm{rod}}_{v\to u}(a)` is the round-to-odd conversion used only by
`vfncvt.rod.f.f.w` (Unpriv. §31.13.19, `sources/riscv-unprivileged.txt:19940-19990`). Its NaN,
infinity, and zero rows are those of `\mathrm{f2f}`. For a finite nonzero input `x`:

1. if `x` is representable in the destination format, the result is `x` with no flags;
2. otherwise let `z` be the destination-format finite value obtained by truncating `x` toward zero,
   with the same sign; if `z` is zero, the result is the smallest subnormal of that sign;
3. otherwise the result is `z` with the least-significant bit of its stored significand set to one;
4. the flags are `NX(0)` and nothing else.

Truncation in step 2 already produces $\mathrm{MAX}_u$ for every input above the destination's
largest finite value, and the least-significant bit of $\mathrm{MAX}_u$ is already one, so step 3
delivers $\mathrm{MAX}_u$ with the sign of `x`. The manual specifies this saturating value; this
document additionally takes the flag set to be `NX(0)` exactly when the delivered value differs
from `x`, with no `OF(2)` and no `UF(1)`, because the conversion saturates instead of overflowing
and preserves a nonzero result for every nonzero input.

### 8.4 BF16

BF16 is a 16-bit interchange format with an 8-bit exponent and a 7-bit fraction (`B=127`,
`w_f=7`); it is not an IEEE 754 format and is not selected by `vtype`. Its widening to binary32 is
exact and consists of appending sixteen zero bits (Unpriv. §25.2,
`sources/riscv-unprivileged.txt:7930-7990`):

$$
\mathrm{bf16to32}(b)=b\ \Vert\ 0^{16}.
$$

The quiet bit of BF16 is bit 6 and the quiet bit of binary32 is bit 22, so the extension preserves
the signaling/quiet distinction and the payload. Define

$$
\mathrm{widenB}(b)=\bigl(\mathrm{bf16to32}(b),\ \{\mathrm{NV}(4)\}\ \text{if } b \text{ is a signaling NaN, else } \varnothing\bigr).
$$

The narrowing conversion `\mathrm{f2bf16}_m(a)` uses the rules of §8.3 with destination format
BF16: a NaN becomes `qNaN` with BF16 encoding 0x7FC0 and raises `NV(4)` only when it is signaling;
an infinity or zero is preserved with its sign; a finite value is rounded by
$\mathrm{RN}_{\mathrm{B},m}$, which can overflow the BF16 range and raise `OF(2)` and `NX(0)`, or
underflow and raise `UF(1)` and `NX(0)`.

A BF16 scalar `f` operand is read with the same NaN-boxing rule as §5.3, but the canonical quiet
NaN is the BF16 one: with `\mathrm{qNaN}_{\mathrm{B}}` the 16-bit value 0x7FC0,

$$
\mathrm{fsrc}_{\mathrm{B}}(f[r])=
\begin{cases}
f[r][15:0], & \mathrm{FLEN}=16\ \text{or}\ \mathrm{boxed}_{16}(f[r]),\\
\mathrm{qNaN}_{\mathrm{B}}, & \text{otherwise},
\end{cases}
$$

and no flag is raised by the substitution. `\mathrm{boxed}_{16}` is the test of §5.3 at `w=16`.
The difference from `\mathrm{fsrc}_{16}` matters: 0x7FC0 is a signaling NaN when read as binary16.

`vfwmaccbf16` multiplies two BF16 elements and adds a binary32 addend with a single rounding; since
the product of two 8-bit significands has at most 16 significant bits and is exact in binary32, the
result is

$$
\mathrm{fma}_{32}\bigl(\mathrm{bf16to32}(a_i),\ \mathrm{bf16to32}(b_i),\ c_i\bigr),
$$

whose flags are those of §7.3; a signaling NaN operand is preserved as a signaling NaN by
`\mathrm{bf16to32}`, so it raises `NV(4)` there.

### 8.5 Widths and extension conditions of the conversion forms

`SEW` selects the width of the element that gives the form its name; the other side of the
conversion is `SEW` or `2·SEW` as listed. `EMUL` is `LMUL` for the `SEW` side and `2·LMUL` for the
`2·SEW` side; a configuration with `2·LMUL>8` is reserved (§4.5).

| Forms | `SEW` | Source EEW | Destination EEW | Extension condition |
|---|---|---|---|---|
| `vfcvt.xu.f.v`, `vfcvt.x.f.v`, `vfcvt.rtz.xu.f.v`, `vfcvt.rtz.x.f.v` | 16, 32, 64 | `SEW` | `SEW` | $\mathrm{Ext}_{\mathrm{fp}}(\mathrm{SEW})$ |
| `vfcvt.f.xu.v`, `vfcvt.f.x.v` | 16, 32, 64 | `SEW` | `SEW` | $\mathrm{Ext}_{\mathrm{fp}}(\mathrm{SEW})$ |
| `vfwcvt.xu.f.v`, `vfwcvt.x.f.v`, `vfwcvt.rtz.xu.f.v`, `vfwcvt.rtz.x.f.v` | 16, 32 | `SEW` | `2·SEW` | `SEW=16` needs `Zvfh`; `SEW=32` needs `D` |
| `vfwcvt.f.xu.v`, `vfwcvt.f.x.v` | 8, 16, 32 | `SEW` | `2·SEW` | `SEW=8` needs `Zvfh`; `SEW=16` needs `F`; `SEW=32` needs `D` |
| `vfncvt.xu.f.w`, `vfncvt.x.f.w`, `vfncvt.rtz.xu.f.w`, `vfncvt.rtz.x.f.w` | 8, 16, 32 | `2·SEW` | `SEW` | `SEW=8` needs `Zvfh`; `SEW=16` needs `F`; `SEW=32` needs `D` |
| `vfncvt.f.xu.w`, `vfncvt.f.x.w` | 16, 32 | `2·SEW` | `SEW` | `SEW=16` needs `Zvfh`; `SEW=32` needs `F` |
| `vfwcvt.f.f.v` | 16, 32 | `SEW` | `2·SEW` | `SEW=16` needs `Zvfh` or `Zvfhmin`; `SEW=32` needs `D` |
| `vfncvt.f.f.w`, `vfncvt.rod.f.f.w` | 16, 32 | `2·SEW` | `SEW` | `SEW=16` needs `Zvfh` or `Zvfhmin`; `SEW=32` needs `D` |
| `vfncvtbf16.f.f.w` | 16 | 32 | 16 | `Zvfbfmin` |
| `vfwcvtbf16.f.f.v` | 16 | 16 | 32 | `Zvfbfmin` |
| `vfwmaccbf16.vv`, `vfwmaccbf16.vf` | 16 | 16 | 32 | `Zvfbfwma` |

Each row is read together with `impl(V)`; the `F` and `D` entries record which scalar format the
conversion needs and are implied by `V`. A `SEW` outside the listed set has a reserved encoding
(§4.5).

## 9. Reductions and estimates

### 9.1 Reduction destination and ordered folds

A reduction reads a source vector register group and writes one destination register. The
destination result width is $w_d=\mathrm{SEW}$ for the single-width reductions and
$w_d=2\cdot\mathrm{SEW}$ for the widening reductions; its register is a single register with
$N_d=\mathrm{VLEN}/w_d$ element slots, regardless of `LMUL` (Unpriv. §31.14,
`sources/riscv-unprivileged.txt:19291-19335`). Element 0 receives the result; every element with
index in $1\le i<N_d$ is a tail element governed by `vta`, even when its index is below `vl`. If
`vl=0`, no element is updated. Define

$$
\mathrm{Rout}_{w_d}(W,v,vl,vta)=\mathrm{SOut}_{w_d}(W,v,vl>0,vta).
$$

The source elements that take part are the active elements
$\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0)$; the seed is element 0 of `vs1`. Inactive elements
and elements past `vl` are excluded. A non-zero `vstart` is illegal (§4.4), so every result block
has `vstart=0` and the formulas substitute zero for it.

An ordered fold combines the seed with the active elements in increasing index order, one
operation at a time. For a pair-valued element function `x` and a pair-valued binary operation
$\oplus$, the fold $\mathrm{fold}_{\oplus}(z,S,x)$ is defined by the following recursion:

1. if $S=\varnothing$, the result is $(z,\varnothing)$;
2. otherwise let $i_0=\min S$, let $(u,F_u)=x(i_0)$, let $(v_1,F_1)=\oplus(z,u)$, and let
   $(v,F_2)=\mathrm{fold}_{\oplus}(v_1,S\setminus\{i_0\},x)$; the result is
   $(v,\ F_u\cup F_1\cup F_2)$.

The three folds are
$\mathrm{ordsum}_w=\mathrm{fold}_{\mathrm{add}_w}$, $\mathrm{ordmax}_w=\mathrm{fold}_{\mathrm{maxNum}_w}$,
and $\mathrm{ordmin}_w=\mathrm{fold}_{\mathrm{minNum}_w}$. Their flags are the union of the
element-producing flags and the flags of every combining step; in particular, an sNaN anywhere in
the active set raises `NV(4)` at the step that first meets it. With an empty active set the seed is
returned unchanged with no flags.

### 9.2 Unordered sum

`\mathrm{usum}_w(z,S,x)` is the set of pairs a `vfredusum` or `vfwredusum` may produce. The manual
permits any tree-shaped summation, wider intermediate formats, and the insertion of an additive
identity (Unpriv. §31.14.3, `sources/riscv-unprivileged.txt:19360-19420`). Formally, $(v,F)$ is in
the set when there is a finite binary tree whose leaves are the multiset
$\{z\}\cup\{x(i)\mid i\in S\}$, optionally extended by leaves equal to $+0$ or $-0$, such that:

1. every internal node computes the exact sum of its two children and rounds it once to a format
   whose precision is at least `w` and whose exponent range contains that of the `w`-bit format,
   with mode `m`, accumulating the flags of that rounding;
2. the root value, if its format is wider than `w`, is rounded once more to the `w`-bit format
   with mode `m`, accumulating the flags of that rounding;
3. $v$ is the root value and $F$ is the union of all accumulated flags.

The element pairs $x(i)$ contribute their own flags. When $S=\varnothing$, the permitted outcomes
are $(z,\varnothing)$ and, when `z` is a NaN, its canonicalization to `qNaN` with `NV(4)` exactly
when `z` is signaling; the manual permits either the original NaN with no exception or the
canonical NaN with the invalid flag. Unlike the ordered fold, the set may contain several values
for one execution; the instruction formula therefore writes a set membership for the destination
value, and every permitted outcome carries the same flag union rule.

### 9.3 Reciprocal square-root estimate

`vfrsqrt7.v` returns a 7-bit estimate of $1/\sqrt{x}$ and depends on no rounding mode (Unpriv.
§31.13.9, `sources/riscv-unprivileged.txt:18505-18625`). For a NaN, an infinity, or a zero the
behavior is fixed by the class table:

| Input | Value | Flags |
|---|---|---|
| $-\infty\le x<-0$ | `qNaN` | `NV(4)` |
| $-0$ | $-\infty$ | `DZ(3)` |
| $+0$ | $+\infty$ | `DZ(3)` |
| $+\infty$ | $+0$ | none |
| quiet NaN | `qNaN` | none |
| signaling NaN | `qNaN` | `NV(4)` |

For a positive finite input, let `e` and `f` be its exponent and fraction fields. The normalized
input exponent is

$$
n_e=\begin{cases}e, & e\ne 0,\\ -\,(\text{number of leading zeros of the } w_f\text{-bit field } f), & e=0,\end{cases}
$$

and the normalized significand field (the `w_f` bits after the leading one) is `f` when `e≠0` and
`(f\ll(1-n_e))\bmod 2^{w_f}` when `e=0`. Let `s` be the six most significant bits of that field.
The table index is

$$
\mathrm{idx}=64\cdot(n_e\bmod 2)+s,
$$

where $n_e\bmod 2$ is taken in $\{0,1\}$ for negative $n_e$ as well. With
$\sigma_{57}(\mathrm{idx})$ the entry of Table 57, the output is the normal number

$$
e_{\mathrm{out}}=\left\lfloor\frac{3B-1-n_e}{2}\right\rfloor,\qquad
f_{\mathrm{out}}=\sigma_{57}(\mathrm{idx})\cdot 2^{w_f-7},
$$

with the sign of the input and no flags. Every positive normal or subnormal input produces a normal
output, so $1\le e_{\mathrm{out}}\le 2B$. The output is independent of `fcsr.frm`.

**Table 57. `vfrsqrt7` common-case lookup table.** Indexed by the low bit of the normalized
input exponent and the six high bits of the normalized significand; the result is the seven
high bits of the output significand. The right half lists the entries for `exp[0]=1`.

| `exp[0]` | `sig[MSB-:6]` | `sig_out[MSB-:7]` | `exp[0]` | `sig[MSB-:6]` | `sig_out[MSB-:7]` |
|---|---|---|---|---|---|
| 0 | 0 | 52 | 1 | 0 | 127 |
| 0 | 1 | 51 | 1 | 1 | 125 |
| 0 | 2 | 50 | 1 | 2 | 123 |
| 0 | 3 | 48 | 1 | 3 | 121 |
| 0 | 4 | 47 | 1 | 4 | 119 |
| 0 | 5 | 46 | 1 | 5 | 118 |
| 0 | 6 | 44 | 1 | 6 | 116 |
| 0 | 7 | 43 | 1 | 7 | 114 |
| 0 | 8 | 42 | 1 | 8 | 113 |
| 0 | 9 | 41 | 1 | 9 | 111 |
| 0 | 10 | 40 | 1 | 10 | 109 |
| 0 | 11 | 39 | 1 | 11 | 108 |
| 0 | 12 | 38 | 1 | 12 | 106 |
| 0 | 13 | 36 | 1 | 13 | 105 |
| 0 | 14 | 35 | 1 | 14 | 103 |
| 0 | 15 | 34 | 1 | 15 | 102 |
| 0 | 16 | 33 | 1 | 16 | 100 |
| 0 | 17 | 32 | 1 | 17 | 99 |
| 0 | 18 | 31 | 1 | 18 | 97 |
| 0 | 19 | 30 | 1 | 19 | 96 |
| 0 | 20 | 30 | 1 | 20 | 95 |
| 0 | 21 | 29 | 1 | 21 | 93 |
| 0 | 22 | 28 | 1 | 22 | 92 |
| 0 | 23 | 27 | 1 | 23 | 91 |
| 0 | 24 | 26 | 1 | 24 | 90 |
| 0 | 25 | 25 | 1 | 25 | 88 |
| 0 | 26 | 24 | 1 | 26 | 87 |
| 0 | 27 | 23 | 1 | 27 | 86 |
| 0 | 28 | 23 | 1 | 28 | 85 |
| 0 | 29 | 22 | 1 | 29 | 84 |
| 0 | 30 | 21 | 1 | 30 | 83 |
| 0 | 31 | 20 | 1 | 31 | 82 |
| 0 | 32 | 19 | 1 | 32 | 80 |
| 0 | 33 | 19 | 1 | 33 | 79 |
| 0 | 34 | 18 | 1 | 34 | 78 |
| 0 | 35 | 17 | 1 | 35 | 77 |
| 0 | 36 | 16 | 1 | 36 | 76 |
| 0 | 37 | 16 | 1 | 37 | 75 |
| 0 | 38 | 15 | 1 | 38 | 74 |
| 0 | 39 | 14 | 1 | 39 | 73 |
| 0 | 40 | 14 | 1 | 40 | 72 |
| 0 | 41 | 13 | 1 | 41 | 71 |
| 0 | 42 | 12 | 1 | 42 | 70 |
| 0 | 43 | 12 | 1 | 43 | 70 |
| 0 | 44 | 11 | 1 | 44 | 69 |
| 0 | 45 | 10 | 1 | 45 | 68 |
| 0 | 46 | 10 | 1 | 46 | 67 |
| 0 | 47 | 9 | 1 | 47 | 66 |
| 0 | 48 | 9 | 1 | 48 | 65 |
| 0 | 49 | 8 | 1 | 49 | 64 |
| 0 | 50 | 7 | 1 | 50 | 63 |
| 0 | 51 | 7 | 1 | 51 | 63 |
| 0 | 52 | 6 | 1 | 52 | 62 |
| 0 | 53 | 6 | 1 | 53 | 61 |
| 0 | 54 | 5 | 1 | 54 | 60 |
| 0 | 55 | 4 | 1 | 55 | 59 |
| 0 | 56 | 4 | 1 | 56 | 59 |
| 0 | 57 | 3 | 1 | 57 | 58 |
| 0 | 58 | 3 | 1 | 58 | 57 |
| 0 | 59 | 2 | 1 | 59 | 56 |
| 0 | 60 | 2 | 1 | 60 | 56 |
| 0 | 61 | 1 | 1 | 61 | 55 |
| 0 | 62 | 1 | 1 | 62 | 54 |
| 0 | 63 | 0 | 1 | 63 | 53 |

### 9.4 Reciprocal estimate

`vfrec7.v` returns a 7-bit estimate of $1/x$; it too depends on no rounding mode except in the
overflow case (Unpriv. §31.13.10, `sources/riscv-unprivileged.txt:18700-18990`). For a NaN, an
infinity, or a zero:

| Input | Value | Flags |
|---|---|---|
| $-\infty$ | $-0$ | none |
| $+\infty$ | $+0$ | none |
| $-0$ | $-\infty$ | `DZ(3)` |
| $+0$ | $+\infty$ | `DZ(3)` |
| quiet NaN | `qNaN` | none |
| signaling NaN | `qNaN` | `NV(4)` |

For a finite nonzero input, compute $n_e$ and the normalized significand field exactly as in §9.3,
and let `s` now be its seven most significant bits. The normalized output exponent is
$n_o=2B-1-n_e$; the exceptional cases are $n_o>2B$, where the result overflows, and $n_o\in\{0,-1\}$,
where it is subnormal. For negative inputs every result is the negation of the result for the
positive input of the same magnitude, with the same flags.

| Case | Value | Flags |
|---|---|---|
| $n_o>2B$, positive input, `RUP(3)`, `RNE(0)`, `RMM(4)` | $+\infty$ | `NX(0)`, `OF(2)` |
| $n_o>2B$, positive input, `RDN(2)`, `RTZ(1)` | $+\mathrm{MAX}$ | `NX(0)`, `OF(2)` |
| $n_o>2B$, negative input, `RUP(3)`, `RTZ(1)` | $-\mathrm{MAX}$ | `NX(0)`, `OF(2)` |
| $n_o>2B$, negative input, `RDN(2)`, `RNE(0)`, `RMM(4)` | $-\infty$ | `NX(0)`, `OF(2)` |
| $1\le n_o\le 2B$ | normal with $e=n_o$, $f=\sigma_{58}(s)\cdot2^{w_f-7}$ | none |
| $n_o\in\{0,-1\}$ | subnormal with $e=0$, $f=\bigl((2^7\ \vert\ \sigma_{58}(s))\ll(w_f-7)\bigr)\gg(1-n_o)$ | none |

Here $\sigma_{58}(s)$ is the entry of Table 58 and `\vert` is bitwise or. Every subnormal input of
magnitude at least $2^{-(B+1)}$ produces a normal output, and every normal input of magnitude at
least $2^{B-1}$ produces a subnormal output, as the table's class analysis requires.

**Table 58. `vfrec7` common-case lookup table.** Indexed by the seven high bits of the
normalized input significand; the result is the seven high bits of the normalized output
significand.

| `sig` | `out` | `sig` | `out` | `sig` | `out` | `sig` | `out` |
|---|---|---|---|---|---|---|---|
| 0 | 127 | 32 | 76 | 64 | 42 | 96 | 18 |
| 1 | 125 | 33 | 75 | 65 | 41 | 97 | 17 |
| 2 | 123 | 34 | 74 | 66 | 40 | 98 | 17 |
| 3 | 121 | 35 | 72 | 67 | 40 | 99 | 16 |
| 4 | 119 | 36 | 71 | 68 | 39 | 100 | 15 |
| 5 | 117 | 37 | 70 | 69 | 38 | 101 | 15 |
| 6 | 116 | 38 | 69 | 70 | 37 | 102 | 14 |
| 7 | 114 | 39 | 68 | 71 | 36 | 103 | 14 |
| 8 | 112 | 40 | 66 | 72 | 35 | 104 | 13 |
| 9 | 110 | 41 | 65 | 73 | 35 | 105 | 12 |
| 10 | 109 | 42 | 64 | 74 | 34 | 106 | 12 |
| 11 | 107 | 43 | 63 | 75 | 33 | 107 | 11 |
| 12 | 105 | 44 | 62 | 76 | 32 | 108 | 11 |
| 13 | 104 | 45 | 61 | 77 | 31 | 109 | 10 |
| 14 | 102 | 46 | 60 | 78 | 31 | 110 | 9 |
| 15 | 100 | 47 | 59 | 79 | 30 | 111 | 9 |
| 16 | 99 | 48 | 58 | 80 | 29 | 112 | 8 |
| 17 | 97 | 49 | 57 | 81 | 28 | 113 | 8 |
| 18 | 96 | 50 | 56 | 82 | 28 | 114 | 7 |
| 19 | 94 | 51 | 55 | 83 | 27 | 115 | 7 |
| 20 | 93 | 52 | 54 | 84 | 26 | 116 | 6 |
| 21 | 91 | 53 | 53 | 85 | 25 | 117 | 5 |
| 22 | 90 | 54 | 52 | 86 | 25 | 118 | 5 |
| 23 | 88 | 55 | 51 | 87 | 24 | 119 | 4 |
| 24 | 87 | 56 | 50 | 88 | 23 | 120 | 4 |
| 25 | 85 | 57 | 49 | 89 | 23 | 121 | 3 |
| 26 | 84 | 58 | 48 | 90 | 22 | 122 | 3 |
| 27 | 83 | 59 | 47 | 91 | 21 | 123 | 2 |
| 28 | 81 | 60 | 46 | 92 | 21 | 124 | 2 |
| 29 | 80 | 61 | 45 | 93 | 20 | 125 | 1 |
| 30 | 79 | 62 | 44 | 94 | 19 | 126 | 1 |
| 31 | 77 | 63 | 43 | 95 | 19 | 127 | 0 |

## 10. Instruction index

Each row is one file under `instructions/`. The `SEW` column lists the element widths the file's
formulas cover; a width outside it is a reserved encoding (§4.5). `Ext` is the extension condition
of §4.1. `Flags` is `yes` when the result blocks carry `fcsr.fflags` and the `FS` Dirty assignment,
which is exactly when the instruction can modify floating-point state. `Blocks` counts the formulas
of the file: one guard block plus three result blocks for each result category, one per privileged
configuration of §1.

### 10.1 Arithmetic

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfadd.md` | `VFADD.VV`, `VFADD.VF` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfsub.md` | `VFSUB.VV`, `VFSUB.VF`, `VFRSUB.VF` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfmul.md` | `VFMUL.VV`, `VFMUL.VF` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfdiv.md` | `VFDIV.VV`, `VFDIV.VF`, `VFRDIV.VF` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfwadd.md` | `VFWADD` `.vv`, `.vf`, `.wv`, `.wf`; `LMUL≤4` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfwsub.md` | `VFWSUB` `.vv`, `.vf`, `.wv`, `.wf`; `LMUL≤4` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfwmul.md` | `VFWMUL.VV`, `VFWMUL.VF`; `LMUL≤4` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfsqrt.md` | `VFSQRT.V` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |

### 10.2 Fused multiply-add

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfmacc.md` | `VFMACC`, `VFNMACC`, `VFMSAC`, `VFNMSAC`, each `.vv`/`.vf` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfmadd.md` | `VFMADD`, `VFNMADD`, `VFMSUB`, `VFNMSUB`, each `.vv`/`.vf` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfwmacc.md` | `VFWMACC`, `VFWNMACC`, `VFWMSAC`, `VFWNMSAC`, each `.vv`/`.vf`; `LMUL≤4` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |

### 10.3 Estimates

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfrsqrt7.md` | `VFRSQRT7.V` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfrec7.md` | `VFREC7.V` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |

### 10.4 Minimum, sign, comparison, classification

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfminmax.md` | `VFMIN`, `VFMAX`, each `.vv`/`.vf` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfsgnj.md` | `VFSGNJ`, `VFSGNJN`, `VFSGNJX`, each `.vv`/`.vf` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |
| `vmfcompare.md` | `VMFEQ`, `VMFNE`, `VMFLT`, `VMFLE` (`.vv`, `.vf`); `VMFGT`, `VMFGE` (`.vf`) | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfclass.md` | `VFCLASS.V` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |

### 10.5 Merge and scalar moves

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfmerge.md` | `VFMERGE.VFM` (`vm=0`) | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |
| `vfmv-vf.md` | `VFMV.V.F` (`vm=1`, `vs2=v0`) | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |
| `vfmv-fs.md` | `VFMV.F.S` (`vm=1`) | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 4 |
| `vfmv-sf.md` | `VFMV.S.F` (`vm=1`) | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |

### 10.6 Conversions

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfcvt.md` | `VFCVT.XU.F.V`, `VFCVT.X.F.V`, `VFCVT.RTZ.XU.F.V`, `VFCVT.RTZ.X.F.V`, `VFCVT.F.XU.V`, `VFCVT.F.X.V` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 19 |
| `vfwcvt-x.md` | `VFWCVT.XU.F.V`, `VFWCVT.X.F.V`, and the two `.RTZ` forms; `LMUL≤4` | 16, 32 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 13 |
| `vfwcvt-fx.md` | `VFWCVT.F.XU.V`, `VFWCVT.F.X.V`; `LMUL≤4` | 8, 16, 32 | §8.5 row 4 | yes | 7 |
| `vfwcvt-ff.md` | `VFWCVT.F.F.V`; `LMUL≤4` | 16, 32 | $\mathrm{Ext}_{\mathrm{fmin}}$ | yes | 4 |
| `vfncvt-x.md` | `VFNCVT.XU.F.W`, `VFNCVT.X.F.W`, and the two `.RTZ` forms; `LMUL≤4` | 8, 16, 32 | §8.5 row 5 | yes | 13 |
| `vfncvt-fx.md` | `VFNCVT.F.XU.W`, `VFNCVT.F.X.W`; `LMUL≤4` | 16, 32 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 7 |
| `vfncvt-ff.md` | `VFNCVT.F.F.W`, `VFNCVT.ROD.F.F.W`; `LMUL≤4` | 16, 32 | $\mathrm{Ext}_{\mathrm{fmin}}$ | yes | 7 |

### 10.7 Reductions

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfred.md` | `VFREDOSUM.VS`, `VFREDUSUM.VS`, `VFREDMAX.VS`, `VFREDMIN.VS` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 13 |
| `vfwred.md` | `VFWREDOSUM.VS`, `VFWREDUSUM.VS`; `LMUL≤4` | 16, 32 | $\mathrm{Ext}_{\mathrm{fp}}$ | yes | 7 |

### 10.8 Slides

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `vfslide1up.md` | `VFSLIDE1UP.VF` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |
| `vfslide1down.md` | `VFSLIDE1DOWN.VF` | 16, 32, 64 | $\mathrm{Ext}_{\mathrm{fp}}$ | no | 4 |

### 10.9 BF16

| File | Instructions | SEW | Ext | Flags | Blocks |
|---|---|---|---|---|---|
| `bf16cvt.md` | `VFNCVTBF16.F.F.W`, `VFWCVTBF16.F.F.V`; `LMUL≤4` | 16 | `impl(V)` ∧ `impl(Zvfbfmin)` | yes | 7 |
| `bf16fma.md` | `VFWMACCBF16.VV`, `VFWMACCBF16.VF`; `LMUL≤4` | 16 | `impl(V)` ∧ `impl(Zvfbfwma)` | yes | 4 |

The 34 files contain 193 formulas: 34 guard blocks and 159 result blocks. A result block is a
distinct result category under one privileged configuration; the number of categories per file is
one for each row of the operation tables of §7–§9 that the file formalizes.

## 11. Validation

Both checkers are run on this file and on every instruction file:

```bash
python3 -I tools/check_md.py    specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md
python3 -I tools/check_style.py specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md
find specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/instructions -name '*.md' \
  -exec python3 -I tools/check_md.py {} \; \
  -exec python3 -I tools/check_style.py {} \;
```

`check_md.py` checks the Markdown structure: paired display-math delimiters, balanced `aligned` and
`cases` environments, even inline math delimiters, and uniform table column counts. `check_style.py`
checks the formula style for every `aligned` block that contains `\mathrm{instr}`: each body line starts
with `&`, `\mathrm{instr}` is the last body line, at most one top-level `\land` per line,
`\longrightarrow` follows the block, the right side is a `\{\, … \,\}` set ending in
`\mathrm{exception}`, and no `\wedge`, `\vee`, or bit-literal constant appears. Both exit with
status 1 on a violation.


