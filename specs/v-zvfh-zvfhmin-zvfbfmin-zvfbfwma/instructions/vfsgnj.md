# VFSGNJ, VFSGNJN, VFSGNJX — vector floating-point sign injection

The three instructions copy each `vs2` element and replace its sign bit by the sign of the second
operand, by its complement, or by its exclusive-or with the source sign (Unpriv. §31.13.12,
`sources/riscv-unprivileged.txt:19026-19034`). Write `op∈{J,N,X}` with
`instr=VFSGN_op.form`; `sgn_J`, `sgn_N`, and `sgn_X` are `sgnj`, `sgnjn`, and `sgnjx` of §7.7.
With `a_i` element `i` of `vs2` and `b_i` element `i` of `vs1` or
$\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])$, the per-element result is
$f(i)=\mathrm{sgn}_{\mathrm{op}}(a_i,b_i)$. The operation is bitwise: payloads and zero signs are
preserved apart from the sign bit, and no flag is raised.

**(VFSGNJ.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32,64\})\\
&\land\ (\mathrm{op}\in\{\mathrm{J},\mathrm{N},\mathrm{X}\})\\
&\land\ (\mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\})\\
&\land\ (\mathrm{instr}=\mathrm{VFSGN}_{\mathrm{op}}.\mathrm{form})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFSGNJ.1) No H, M/S/U: sign injection**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{op}\in\{\mathrm{J},\mathrm{N},\mathrm{X}\}\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFSGN}_{\mathrm{op}}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),f,vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFSGNJ.2) H, M/HS/U: sign injection**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{op}\in\{\mathrm{J},\mathrm{N},\mathrm{X}\}\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFSGN}_{\mathrm{op}}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),f,vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFSGNJ.3) H, VS/VU: sign injection**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{op}\in\{\mathrm{J},\mathrm{N},\mathrm{X}\}\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFSGN}_{\mathrm{op}}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),f,vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
