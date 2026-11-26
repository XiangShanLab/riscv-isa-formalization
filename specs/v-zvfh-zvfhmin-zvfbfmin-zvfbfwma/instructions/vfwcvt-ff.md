# VFWCVT.F.F.V — vector widening floating-point type-convert

`VFWCVT.F.F.V` converts a `SEW`-wide floating-point element to a `2\cdot\mathrm{SEW}`-wide
floating-point element with the rules of §8.3 (Unpriv. §31.13.18,
`sources/riscv-unprivileged.txt:19240-19275`). Every finite conversion is exact and raises no flag;
an infinity or zero keeps its sign, and a NaN becomes the canonical quiet NaN of the destination
format, raising `NV(4)` only when it is signaling. The destination has `EEW=2\cdot\mathrm{SEW}` and
`EMUL=2\cdot\mathrm{LMUL}`, so `LMUL=8` is reserved. `SEW=16` is enabled by `Zvfh` or `Zvfhmin`, and
`SEW=32` needs `D`.

**(VFWCVT.F.F.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh)\ \land\ \neg\mathrm{impl}(Zvfhmin))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32\})\\
&\land\ (\mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{F}.\mathrm{V})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFWCVT.F.F.1) No H, M/S/U: widening float conversion**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{F}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}_{\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}_{\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.F.2) H, M/HS/U: widening float conversion**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{F}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}_{\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}_{\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.F.3) H, VS/VU: widening float conversion**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{F}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}_{\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}_{\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$
