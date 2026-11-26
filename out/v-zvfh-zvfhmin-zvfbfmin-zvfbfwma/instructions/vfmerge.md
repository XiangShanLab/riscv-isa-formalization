# VFMERGE — vector floating-point merge

`VFMERGE.VFM` selects, for every body element, between the `vs2` element and the scalar `f[rs1]`
under the control of the mask register `v0` (Unpriv. §31.13.15,
`sources/riscv-unprivileged.txt:19140-19160`). The mnemonic is written `VFMERGE.VFM` and the
instruction is encoded with `vm=0`, but no element is inactive: the mask value chooses the operand.
The manual states that a merge "operates on all body elements from `vstart` up to the current vector
length in `vl` regardless of mask value", so the formula passes the literal `1` in the place of
`vm` to `\mathrm{Out}` and the mask value enters only through `f(i)`.

With `a_i` element `i` of `vs2`, the per-element result is
$f(i)=\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])$ when `\mathrm{bit}(\mathrm{V}_0,i)=1` and $f(i)=a_i$
otherwise. The instruction raises no flag and writes no `f` register; the tail follows `vta`.

**(VFMERGE.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32,64\})\\
&\land\ (\mathrm{instr}=\mathrm{VFMERGE}.\mathrm{VFM})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFMERGE.1) No H, M/S/U: merge of a vector element and a scalar**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{vm}=0\\
&\land\ \mathrm{instr}=\mathrm{VFMERGE}.\mathrm{VFM}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\bigl(\mathrm{bit}(\mathrm{V}_0,i)=1\ ?\ \mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])\ :\ \mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i)\bigr),vl,vstart,1,\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFMERGE.2) H, M/HS/U: merge of a vector element and a scalar**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{vm}=0\\
&\land\ \mathrm{instr}=\mathrm{VFMERGE}.\mathrm{VFM}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\bigl(\mathrm{bit}(\mathrm{V}_0,i)=1\ ?\ \mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])\ :\ \mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i)\bigr),vl,vstart,1,\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFMERGE.3) H, VS/VU: merge of a vector element and a scalar**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{vm}=0\\
&\land\ \mathrm{instr}=\mathrm{VFMERGE}.\mathrm{VFM}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\bigl(\mathrm{bit}(\mathrm{V}_0,i)=1\ ?\ \mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])\ :\ \mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i)\bigr),vl,vstart,1,\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
