# Zfinx, Zdinx, Zhinx, Zhinxmin — scalar floating point on integer registers

The Zfinx family provides the same arithmetic as `F`, `D`, and `Zfh`, but reads and writes the integer register file. Every operand that would be an `f` register becomes the `x` register with the same number; `rd` remains an integer destination. Q is not provided: no Zqinx is defined, so the formats are H, S, and D, with $\mathrm{Extx}(H)=\mathrm{Zhinx}$, $\mathrm{Extx}(S)=\mathrm{Zfinx}$, and $\mathrm{Extx}(D)=\mathrm{Zdinx}$.

The floating-point state `FS` plays no part: it is hardwired to Off and `misa.F` to zero, so no formula tests `mstatus.FS`, no formula assigns `mstatus.FS`, and no write-back sets `FS=Dirty`. The `fcsr` still exists and is still gated by `Zicsr`; its sticky flags are written exactly as before. Because `misa.F=0`, the `stateen0.FCSR` bits are live: when the stateen CSRs are implemented, every floating-point instruction is gated as though it read `fcsr`, whether or not it does. A stateen CSR controls only less-privileged modes, so M-mode is never gated; HS-mode is gated by `mstateen0`, U-mode by `mstateen0` and `sstateen0`, VS-mode by `mstateen0` and `hstateen0`, and VU-mode by all three (Priv. §4.1). A zero `mstateen0.FCSR` makes the instruction illegal in every mode below M; a zero `hstateen0.FCSR` or `sstateen0.FCSR` reached from VS or VU raises a virtual-instruction exception instead, because the instruction would still be valid in HS-mode (Priv. §15.6).

A value of width $w_F\le\mathrm{XLEN}$ occupies bits $w_F-1{:}0$ of one `x` register; the operand
bits $\mathrm{XLEN}-1{:}w_F$ are ignored, and a result is sign-extended into them. There is no
NaN-boxing. On RV32Zdinx a double instead occupies an aligned register pair, low-order bits in the
lower-numbered register, so $w_F=2\,\mathrm{XLEN}$ there (Unpriv. §27.3, `:8765-8779`). Every
formula binds its sources and writes its destination through

$$
\mathrm{xop}_F(i)=
\begin{cases}
0, & i=0,\\
\mathrm{low}_{w_F}(x[i]), & w_F\le\mathrm{XLEN},\ i\ne0,\\
x[i]\Vert x[i+1], & w_F=2\,\mathrm{XLEN},\ i\ne0,
\end{cases}
\qquad
\mathrm{xwr}_F(i,v)=
\begin{cases}
x[0]=0, & i=0,\\
x[i]=\mathrm{senc}_F(v), & w_F\le\mathrm{XLEN},\ i\ne0,\\
x[i]=\mathrm{low}_{\mathrm{XLEN}}(\mathrm{raw}_F(v)),\ x[i+1]=\mathrm{high}_{\mathrm{XLEN}}(\mathrm{raw}_F(v)),
  & w_F=2\,\mathrm{XLEN},\ i\ne0,
\end{cases}
$$

with $\mathrm{senc}_F(v)=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{raw}_F(v))$, where
$\mathrm{raw}_F(v)$ is the $w_F$-bit IEEE encoding of the value or class $v$. A source is read as
$a=\mathrm{xop}_F(\mathrm{rs1})$, $b=\mathrm{xop}_F(\mathrm{rs2})$, $c=\mathrm{xop}_F(\mathrm{rs3})$;
a destination is written as the single result-set element $\mathrm{xwr}_F(\mathrm{rd},v)$, which
expands into the one or two assignments of its case. A pair requires an even register number (an odd
one is reserved), and an operand read or a destination write through `x0` touches no other register.

The instruction formulas are the formulas of the corresponding `f`-register files with `fd=…` replaced by `\mathrm{xwr}_F(\mathrm{rd},…)`, `a`, `b`, `c` bound by `\mathrm{xop}_F`, and all `FS` terms deleted. Each category, its condition, its flags, and its exception are unchanged. $I$ is the instruction under consideration and $F$ its format. The blocks below fix the configuration and write-back for each arity; every other instruction keeps the same pattern. Formulas are tried in order: the guard blocks precede every result block, so an unavailable extension or a denied `stateen` bit takes precedence.

For the six `fcsr` access instructions — `FRCSR`, `FSCSR`, `FRRM`, `FSRM`, `FRFLAGS`, and `FSFLAGS` — the format-dependent conjuncts of blocks 0 and 1 (`¬impl(Extx(F))`, `impl(Extx(F))`, and `F∈{H,S,D}`) are dropped because the instruction has no format; `Zicsr` and the `stateen` gate keep their roles, and Z.9 and Z.10 show the resulting result form.

The mode names follow the same rule as the `f`-register files: `HS`, `VS`, and `VU` exist only when `H` is implemented. Without `H` the supervisor mode is `S`, gated by `mstateen0` exactly like `HS`, so the gate conditions below write `Priv∈{S,HS}` for that shared case; `VS` and `VU`, and the `hstateen0` gate, presuppose `H` (Priv. Tables 1 and 44, `sources/riscv-privileged.txt:748-752`, `8719-8727`).

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(Z.0) Extension or `Zicsr` unavailable, or `stateen` makes the instruction illegal → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\neg\mathrm{impl}(\mathrm{Extx}(F))\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\\
&\qquad\lor\ \bigl(\mathrm{impl}(\mathrm{stateen})\ \land\ ((\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=0)\\
&\qquad\qquad\lor\ (\mathrm{Priv}=\mathrm{U}\land(mstateen0.FCSR=0\lor sstateen0.FCSR=0))\ \lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=0)\\
&\qquad\qquad\lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=0))\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(Z.1) `stateen` denies access to a virtual machine while `mstateen0.FCSR=1` → VirtualInstruction(22)**

$$
\begin{aligned}
&\bigl(\mathrm{impl}(\mathrm{stateen})\land mstateen0.FCSR=1\\
&\qquad\land\ \big((\mathrm{Priv}=\mathrm{VS}\land hstateen0.FCSR=0)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land(hstateen0.FCSR=0\lor sstateen0.FCSR=0))\big)\bigr)\\
&\land\ \mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{VirtualInstruction}(22)\} \,\}
$$

**(Z.2) `FADD` normal and exact → `\mathrm{xwr}_F(\mathrm{rd},…)` of the rounded value**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (a=\mathrm{xop}_F(rs1)\land b=\mathrm{xop}_F(rs2))\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{xwr}_F(\mathrm{rd},\mathrm{rounded}),\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.3) `FSQRT` of $+\infty_F$ → `\mathrm{xwr}_F(\mathrm{rd},…)` of $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (a=\mathrm{xop}_F(rs1))\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{xwr}_F(\mathrm{rd},+\infty_F),\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.4) `FSGNJ` → magnitude of `x[rs1]` with the sign of `x[rs2]`**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ (a=\mathrm{xop}_F(rs1)\land b=\mathrm{xop}_F(rs2))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{xwr}_F(\mathrm{rd},(s_b,e_a,f_a)),\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.5) `FEQ` with a signaling NaN → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ (a=\mathrm{xop}_F(rs1)\land b=\mathrm{xop}_F(rs2))\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.6) `FCVT.W.F` in range and inexact → integer in `rd`, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (a=\mathrm{xop}_F(rs1))\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{ires}\le2^{31}-1\big)\\
&\land\ (\mathrm{ires}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{enc}_{W}(\mathrm{ires}),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.7) `FCVT.F.W` exact → `\mathrm{xwr}_F(\mathrm{rd},…)` of the value**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (u=\mathrm{sext}_{32}(x[rs1][31:0]))\\
&\land\ (\mathrm{rounded}=u)\\
&\land\ \neg\big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{xwr}_F(\mathrm{rd},u),\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.8) `FMADD` normal and exact → `\mathrm{xwr}_F(\mathrm{rd},…)` of the rounded value**

$$
\begin{aligned}
&\mathrm{impl}(\mathrm{Extx}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ \big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (a=\mathrm{xop}_F(rs1)\land b=\mathrm{xop}_F(rs2)\land c=\mathrm{xop}_F(rs3))\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D}\})\\
&\land\ (\mathrm{instr}=I)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{xwr}_F(\mathrm{rd},\mathrm{rounded}),\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.9) `FRCSR` reads `fcsr`; no `FS` term applies**

$$
\begin{aligned}
&\big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (\mathrm{instr}=\mathrm{FRCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ \mathrm{exception}=\varnothing \,\}
$$

**(Z.10) `FSCSR` reads old `fcsr` and writes new `fcsr`; no `mstatus.FS` write**

$$
\begin{aligned}
&\big(\neg\mathrm{impl}(\mathrm{stateen})\ \lor\ \mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}\in\{\mathrm{S},\mathrm{HS}\}\land mstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{U}\land mstateen0.FCSR=1\land sstateen0.FCSR=1)\\
&\qquad\lor\ (\mathrm{Priv}=\mathrm{VS}\land mstateen0.FCSR=1\land hstateen0.FCSR=1)\ \lor\ (\mathrm{Priv}=\mathrm{VU}\land mstateen0.FCSR=1\land hstateen0.FCSR=1\land sstateen0.FCSR=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (\mathrm{instr}=\mathrm{FSCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ fcsr=\mathrm{zext}_{32}(x[rs1][7:0]),\ \mathrm{exception}=\varnothing \,\}
$$

## Coverage

`Zfinx` adds every `F` instruction except the transfers `FLW`, `FSW`, `FMV.W.X`, `FMV.X.W`, `C.FLW`, and `C.FSW`: the arithmetic, sign-injection, minimum/maximum, comparison, and classification instructions, `FCVT.W`/`WU`/`L`/`LU`, and `FCVT.S.D`/`FCVT.D.S`. `Zdinx` adds the `D` set except `FLD`, `FSD`, `FMV.D.X`, `FMV.X.D`, and their compressed forms, including the conversions `FCVT.S.D` and `FCVT.D.S`. `Zhinx` adds the `Zfh` set except `FLH`, `FSH`, `FMV.H.X`, `FMV.X.H`. `Zhinxmin` adds only `FCVT.S.H` and `FCVT.H.S`, plus `FCVT.D.H` and `FCVT.H.D` when `Zdinx` is present. Floating-point values are transferred with integer loads and stores, and register-to-register moves with `FSGNJ`.

`FLI`, `FMINM`, `FMAXM`, `FROUND`, `FROUNDNX`, `FCVTMOD`, `FLEQ`, `FLTQ`, `FMVH`, and `FMVP` are `Zfa` forms of the `f`-register architecture and are not defined for the x-register family.

Two refinements of the extension condition apply. `FCVT.S.H` and `FCVT.H.S` are also available in a
configuration that implements only `Zhinxmin`, and `FCVT.D.H` and `FCVT.H.D` when `Zdinx` is also
present, so for those four conversions the H condition is `impl(Zhinx) ∨ impl(Zhinxmin)`
(`sources/riscv-unprivileged.txt:8796-8805`). On RV32Zdinx a double lives in the aligned pair
`x[i]`:`x[i+1]`, handled uniformly by `\mathrm{xop}_F` and `\mathrm{xwr}_F` (Unpriv. §27.3,
`sources/riscv-unprivileged.txt:8765-8779`).
