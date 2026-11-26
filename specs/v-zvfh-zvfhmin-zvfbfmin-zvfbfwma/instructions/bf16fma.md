# VFWMACCBF16.VV, VFWMACCBF16.VF — vector BF16 widening multiply-accumulate

`VFWMACCBF16` multiplies two BF16 elements, adds the exact product to the binary32 accumulator held
in the destination, and rounds once with `fcsr.frm` (Unpriv. §25.5.5,
`sources/riscv-unprivileged.txt:8380-8450`). The destination has `EEW=2\cdot\mathrm{SEW}` and
`EMUL=2\cdot\mathrm{LMUL}`, so `LMUL=8` is reserved; `SEW=16`. The `.vf` form reads a BF16 scalar
from the low 16 bits of `f[rs1]` when they are correctly NaN-boxed and the canonical BF16 quiet NaN
`\mathrm{qNaN}_{\mathrm{B}}` otherwise, without raising a flag (§8.4).

With `a_i` element `i` of `vs1`, `b_i` element `i` of `vs2` for `.vv` or
$\mathrm{fsrc}_{\mathrm{B}}(f[rs1])$ for `.vf`, and `c_i` the old element `i` of `vd` at
`2\cdot\mathrm{SEW}` bits, the per-element result is
$f(i)=\mathrm{fma}_{2\mathrm{SEW}}\bigl(\mathrm{bf16to32}(a_i),\mathrm{bf16to32}(b_i),c_i\bigr)$.
The product of two 8-bit significands is exact in binary32, so the single rounding of `fma` is the
only rounding; its flags are those of §7.3.

**(VFWMACCBF16.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ \neg\mathrm{impl}(Zvfbfwma)\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16\})\\
&\land\ (\mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\})\\
&\land\ (\mathrm{instr}=\mathrm{VFWMACCBF16}.\mathrm{form})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFWMACCBF16.1) No H, M/S/U: widening BF16 multiply-accumulate**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ \mathrm{impl}(Zvfbfwma)\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFWMACCBF16}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(f(i)),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWMACCBF16.2) H, M/HS/U: widening BF16 multiply-accumulate**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ \mathrm{impl}(Zvfbfwma)\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFWMACCBF16}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(f(i)),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWMACCBF16.3) H, VS/VU: widening BF16 multiply-accumulate**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ \mathrm{impl}(Zvfbfwma)\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFWMACCBF16}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(f(i)),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$
