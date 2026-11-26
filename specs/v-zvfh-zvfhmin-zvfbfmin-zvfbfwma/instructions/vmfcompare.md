# VMFEQ, VMFNE, VMFLT, VMFLE, VMFGT, VMFGE — vector floating-point compare

The six instructions compare the `vs2` element with the second operand and write the result into
the mask register `vd`, one bit per element (Unpriv. §31.13.13,
`sources/riscv-unprivileged.txt:19035-19110`). Write `op∈{EQ,NE,LT,LE,GT,GE}` and
`instr=VMF_op.form`. The predicates and the NaN rules are those of §7.5: `EQ` and `NE` raise
`NV(4)` only for a signaling NaN, the four ordering predicates raise it for every NaN, and `NE`
returns one for a NaN. `GT` and `GE` have only the `.vf` form; the `.vv` encodings with those
funct6 values are `LT` and `LE` with exchanged operands and are not separate instructions.

With `a_i` element `i` of `vs2` and `b_i` element `i` of `vs1` (only `.vv` of `EQ`, `NE`, `LT`,
`LE`) or $\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])$, the mask bit is
$p(i)=\pi_1(\mathrm{cmp}_{\mathrm{op},\mathrm{SEW}}(a_i,b_i))$. The destination is a mask image of
`VLEN` bits, so its tail is always agnostic and may use the predicate value below `VLMAX`.

**(VMFEQ.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32,64\})\\
&\land\ (\mathrm{op}\in\{\mathrm{EQ},\mathrm{NE},\mathrm{LT},\mathrm{LE},\mathrm{GT},\mathrm{GE}\})\\
&\land\ (\mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\})\\
&\land\ ((\mathrm{op},\mathrm{form})\in\{(\mathrm{EQ},\mathrm{VV}),(\mathrm{EQ},\mathrm{VF}),(\mathrm{NE},\mathrm{VV}),(\mathrm{NE},\mathrm{VF}),(\mathrm{LT},\mathrm{VV}),(\mathrm{LT},\mathrm{VF}),(\mathrm{LE},\mathrm{VV}),(\mathrm{LE},\mathrm{VF}),(\mathrm{GT},\mathrm{VF}),(\mathrm{GE},\mathrm{VF})\})\\
&\land\ (\mathrm{instr}=\mathrm{VMF}_{\mathrm{op}}.\mathrm{form})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VMFEQ.1) No H, M/S/U: comparison into a mask**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{op}\in\{\mathrm{EQ},\mathrm{NE},\mathrm{LT},\mathrm{LE},\mathrm{GT},\mathrm{GE}\}\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ (\mathrm{op},\mathrm{form})\in\{(\mathrm{EQ},\mathrm{VV}),(\mathrm{EQ},\mathrm{VF}),(\mathrm{NE},\mathrm{VV}),(\mathrm{NE},\mathrm{VF}),(\mathrm{LT},\mathrm{VV}),(\mathrm{LT},\mathrm{VF}),(\mathrm{LE},\mathrm{VV}),(\mathrm{LE},\mathrm{VF}),(\mathrm{GT},\mathrm{VF}),(\mathrm{GE},\mathrm{VF})\}\\
&\land\ \mathrm{instr}=\mathrm{VMF}_{\mathrm{op}}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{V}_{vd}=\mathrm{MOut}(\mathrm{V}_{vd},p,vl,vstart,\mathrm{vm},\mathrm{V}_0,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$

**(VMFEQ.2) H, M/HS/U: comparison into a mask**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{op}\in\{\mathrm{EQ},\mathrm{NE},\mathrm{LT},\mathrm{LE},\mathrm{GT},\mathrm{GE}\}\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ (\mathrm{op},\mathrm{form})\in\{(\mathrm{EQ},\mathrm{VV}),(\mathrm{EQ},\mathrm{VF}),(\mathrm{NE},\mathrm{VV}),(\mathrm{NE},\mathrm{VF}),(\mathrm{LT},\mathrm{VV}),(\mathrm{LT},\mathrm{VF}),(\mathrm{LE},\mathrm{VV}),(\mathrm{LE},\mathrm{VF}),(\mathrm{GT},\mathrm{VF}),(\mathrm{GE},\mathrm{VF})\}\\
&\land\ \mathrm{instr}=\mathrm{VMF}_{\mathrm{op}}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{V}_{vd}=\mathrm{MOut}(\mathrm{V}_{vd},p,vl,vstart,\mathrm{vm},\mathrm{V}_0,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$

**(VMFEQ.3) H, VS/VU: comparison into a mask**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{op}\in\{\mathrm{EQ},\mathrm{NE},\mathrm{LT},\mathrm{LE},\mathrm{GT},\mathrm{GE}\}\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ (\mathrm{op},\mathrm{form})\in\{(\mathrm{EQ},\mathrm{VV}),(\mathrm{EQ},\mathrm{VF}),(\mathrm{NE},\mathrm{VV}),(\mathrm{NE},\mathrm{VF}),(\mathrm{LT},\mathrm{VV}),(\mathrm{LT},\mathrm{VF}),(\mathrm{LE},\mathrm{VV}),(\mathrm{LE},\mathrm{VF}),(\mathrm{GT},\mathrm{VF}),(\mathrm{GE},\mathrm{VF})\}\\
&\land\ \mathrm{instr}=\mathrm{VMF}_{\mathrm{op}}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{V}_{vd}=\mathrm{MOut}(\mathrm{V}_{vd},p,vl,vstart,\mathrm{vm},\mathrm{V}_0,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$
