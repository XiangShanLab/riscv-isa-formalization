# VFWMUL — vector widening floating-point multiply

`VFWMUL.VV` and `VFWMUL.VF` multiply two `SEW`-wide elements exactly and write the `2·SEW`-wide
product, rounded once (Unpriv. §31.13.5, `sources/riscv-unprivileged.txt:18390-18399`). The
destination has `EEW=2·SEW` and `EMUL=2·LMUL`, so `LMUL=8` is reserved.

For every element index `i`, let `a_i` be element `i` of `vs2` and let `b_i` be element `i` of
`vs1` for `.vv` or $\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1])$ for `.vf`. The per-element result is
$f(i)=\mathrm{mul}_{2\mathrm{SEW}}(\mathrm{widen}(a_i),\mathrm{widen}(b_i))$, with
$\mathrm{widen}$ as in §8.3. The product of two `SEW`-wide significands is exact in `2·SEW`, so the
single rounding is the only source of flags.

**(VFWMUL.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32,64\})\\
&\land\ (\mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\})\\
&\land\ (\mathrm{instr}=\mathrm{VFWMUL}.\mathrm{form})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFWMUL.1) No H, M/S/U: widening multiply**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFWMUL}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(f(i)),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWMUL.2) H, M/HS/U: widening multiply**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFWMUL}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(f(i)),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWMUL.3) H, VS/VU: widening multiply**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{form}\in\{\mathrm{VV},\mathrm{VF}\}\\
&\land\ \mathrm{instr}=\mathrm{VFWMUL}.\mathrm{form}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(f(i)),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(f(i)),\ \mathrm{exception}=\varnothing \,\}
$$
