# FNMADD — fused negated multiply-add

`FNMADD` computes the fused $\mathrm{exact}=-(x\cdot y)-z$ with $x=\mathrm{val}_F(a)$, $y=\mathrm{val}_F(b)$, $z=\mathrm{val}_F(c)$ and rounds once to format $F$. Formats H, S, D, Q; the extension condition is `impl(Ext(F))`. The effective product sign is $p=1\oplus s_a\oplus s_b$ and the effective addend sign is $q=1\oplus s_c$; the descriptions below name the signs of the effective product and effective addend.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FNMADD.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Ext}(F))\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FNMADD.1) No H, M/S/U: a source is not correctly NaN-boxed and another is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \bigl(\bigl(\mathrm{boxed}_{F}(f[rs1])\land e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs2])\lor\neg\mathrm{boxed}_{F}(f[rs3]))\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs2])\land e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs1])\lor\neg\mathrm{boxed}_{F}(f[rs3]))\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs3])\land e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs1])\lor\neg\mathrm{boxed}_{F}(f[rs2]))\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.2) H, M/HS/U: a source is not correctly NaN-boxed and another is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \bigl(\bigl(\mathrm{boxed}_{F}(f[rs1])\land e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs2])\lor\neg\mathrm{boxed}_{F}(f[rs3]))\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs2])\land e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs1])\lor\neg\mathrm{boxed}_{F}(f[rs3]))\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs3])\land e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs1])\lor\neg\mathrm{boxed}_{F}(f[rs2]))\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.3) H, VS/VU: a source is not correctly NaN-boxed and another is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \bigl(\bigl(\mathrm{boxed}_{F}(f[rs1])\land e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs2])\lor\neg\mathrm{boxed}_{F}(f[rs3]))\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs2])\land e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs1])\lor\neg\mathrm{boxed}_{F}(f[rs3]))\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs3])\land e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0\land(\neg\mathrm{boxed}_{F}(f[rs1])\lor\neg\mathrm{boxed}_{F}(f[rs2]))\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.4) No H, M/S/U: a source is not correctly NaN-boxed → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs2])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs3])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.5) H, M/HS/U: a source is not correctly NaN-boxed → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs2])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs3])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.6) H, VS/VU: a source is not correctly NaN-boxed → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs2])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs3])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.7) No H, M/S/U: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\lor(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.8) H, M/HS/U: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\lor(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.9) H, VS/VU: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\lor(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.10) No H, M/S/U: $0\times\infty$ → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=0\land f_a=0)\land(e_b=e_{\max}\land f_b=0))\lor((e_a=e_{\max}\land f_a=0)\land(e_b=0\land f_b=0))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.11) H, M/HS/U: $0\times\infty$ → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=0\land f_a=0)\land(e_b=e_{\max}\land f_b=0))\lor((e_a=e_{\max}\land f_a=0)\land(e_b=0\land f_b=0))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.12) H, VS/VU: $0\times\infty$ → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=0\land f_a=0)\land(e_b=e_{\max}\land f_b=0))\lor((e_a=e_{\max}\land f_a=0)\land(e_b=0\land f_b=0))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.13) No H, M/S/U: product $\infty$, addend opposite-signed $\infty$ → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.14) H, M/HS/U: product $\infty$, addend opposite-signed $\infty$ → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.15) H, VS/VU: product $\infty$, addend opposite-signed $\infty$ → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.16) No H, M/S/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ \neg(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\\
&\land\ \neg(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0)\\
&\land\ \neg\big(((e_a=0\land f_a=0)\land(e_b=e_{\max}\land f_b=0))\lor((e_a=e_{\max}\land f_a=0)\land(e_b=0\land f_b=0))\big)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=1)\lor(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.17) H, M/HS/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ \neg(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\\
&\land\ \neg(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0)\\
&\land\ \neg\big(((e_a=0\land f_a=0)\land(e_b=e_{\max}\land f_b=0))\lor((e_a=e_{\max}\land f_a=0)\land(e_b=0\land f_b=0))\big)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=1)\lor(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.18) H, VS/VU: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ \neg(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\\
&\land\ \neg(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=0)\\
&\land\ \neg\big(((e_a=0\land f_a=0)\land(e_b=e_{\max}\land f_b=0))\lor((e_a=e_{\max}\land f_a=0)\land(e_b=0\land f_b=0))\big)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=1)\lor(e_c=e_{\max}\land1\le f_c\le f_{\max}\land f_c[w_f-1]=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.19) No H, M/S/U: product $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (1\oplus s_a\oplus s_b=0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ \big((e_c\ne e_{\max})\lor((e_c=e_{\max}\land f_c=0)\land(1\oplus s_c=0))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.20) H, M/HS/U: product $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (1\oplus s_a\oplus s_b=0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ \big((e_c\ne e_{\max})\lor((e_c=e_{\max}\land f_c=0)\land(1\oplus s_c=0))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.21) H, VS/VU: product $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (1\oplus s_a\oplus s_b=0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ \big((e_c\ne e_{\max})\lor((e_c=e_{\max}\land f_c=0)\land(1\oplus s_c=0))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.22) No H, M/S/U: product $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (1\oplus s_a\oplus s_b=1)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ \big((e_c\ne e_{\max})\lor((e_c=e_{\max}\land f_c=0)\land(1\oplus s_c=1))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.23) H, M/HS/U: product $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (1\oplus s_a\oplus s_b=1)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ \big((e_c\ne e_{\max})\lor((e_c=e_{\max}\land f_c=0)\land(1\oplus s_c=1))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.24) H, VS/VU: product $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big(((e_a=e_{\max}\land f_a=0)\land\neg(e_b=0\land f_b=0)\land\neg(e_b=e_{\max}\land f_b\ne0))\lor((e_b=e_{\max}\land f_b=0)\land\neg(e_a=0\land f_a=0)\land\neg(e_a=e_{\max}\land f_a\ne0))\big)\\
&\land\ (1\oplus s_a\oplus s_b=1)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ \big((e_c\ne e_{\max})\lor((e_c=e_{\max}\land f_c=0)\land(1\oplus s_c=1))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.25) No H, M/S/U: product finite, addend $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_c=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.26) H, M/HS/U: product finite, addend $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_c=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.27) H, VS/VU: product finite, addend $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_c=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.28) No H, M/S/U: product finite, addend $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_c=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.29) H, M/HS/U: product finite, addend $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_c=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.30) H, VS/VU: product finite, addend $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c=e_{\max}\land f_c=0)\\
&\land\ (1\oplus s_c=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.31) No H, M/S/U: product zero + addend zero, same signs → zero of that sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b=1\oplus s_c)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(0_F(1\oplus s_a\oplus s_b)),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.32) H, M/HS/U: product zero + addend zero, same signs → zero of that sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b=1\oplus s_c)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(0_F(1\oplus s_a\oplus s_b)),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.33) H, VS/VU: product zero + addend zero, same signs → zero of that sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b=1\oplus s_c)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(0_F(1\oplus s_a\oplus s_b)),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.34) No H, M/S/U: product zero + addend zero, opposite signs and not RDN → $+0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ \big(\mathrm{instr}.rm\notin\{\mathrm{RDN}(2),\mathrm{DYN}(7)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\ne\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.35) H, M/HS/U: product zero + addend zero, opposite signs and not RDN → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ \big(\mathrm{instr}.rm\notin\{\mathrm{RDN}(2),\mathrm{DYN}(7)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\ne\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.36) H, VS/VU: product zero + addend zero, opposite signs and not RDN → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ \big(\mathrm{instr}.rm\notin\{\mathrm{RDN}(2),\mathrm{DYN}(7)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\ne\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.37) No H, M/S/U: product zero + addend zero, opposite signs and RDN → $-0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ \big(\mathrm{instr}.rm=\mathrm{RDN}(2)\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm=\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.38) H, M/HS/U: product zero + addend zero, opposite signs and RDN → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ \big(\mathrm{instr}.rm=\mathrm{RDN}(2)\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm=\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.39) H, VS/VU: product zero + addend zero, opposite signs and RDN → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \big((e_a=0\land f_a=0)\lor(e_b=0\land f_b=0)\big)\\
&\land\ \neg(e_a=e_{\max}\land f_a=0)\\
&\land\ \neg(e_b=e_{\max}\land f_b=0)\\
&\land\ (e_c=0\land f_c=0)\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ \neg(e_c=e_{\max}\land f_c\ne0)\\
&\land\ (1\oplus s_a\oplus s_b\ne 1\oplus s_c)\\
&\land\ \big(\mathrm{instr}.rm=\mathrm{RDN}(2)\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm=\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.40) No H, M/S/U: nonzero product exactly cancels addend, not RDN → $+0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \neg(e_b=0\land f_b=0)\\
&\land\ \neg(e_c=0\land f_c=0)\\
&\land\ (\mathrm{exact}=0)\\
&\land\ \big(\mathrm{instr}.rm\notin\{\mathrm{RDN}(2),\mathrm{DYN}(7)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\ne\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.41) H, M/HS/U: nonzero product exactly cancels addend, not RDN → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \neg(e_b=0\land f_b=0)\\
&\land\ \neg(e_c=0\land f_c=0)\\
&\land\ (\mathrm{exact}=0)\\
&\land\ \big(\mathrm{instr}.rm\notin\{\mathrm{RDN}(2),\mathrm{DYN}(7)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\ne\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.42) H, VS/VU: nonzero product exactly cancels addend, not RDN → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \neg(e_b=0\land f_b=0)\\
&\land\ \neg(e_c=0\land f_c=0)\\
&\land\ (\mathrm{exact}=0)\\
&\land\ \big(\mathrm{instr}.rm\notin\{\mathrm{RDN}(2),\mathrm{DYN}(7)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\ne\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.43) No H, M/S/U: nonzero product exactly cancels addend, RDN → $-0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \neg(e_b=0\land f_b=0)\\
&\land\ \neg(e_c=0\land f_c=0)\\
&\land\ (\mathrm{exact}=0)\\
&\land\ \big(\mathrm{instr}.rm=\mathrm{RDN}(2)\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm=\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.44) H, M/HS/U: nonzero product exactly cancels addend, RDN → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \neg(e_b=0\land f_b=0)\\
&\land\ \neg(e_c=0\land f_c=0)\\
&\land\ (\mathrm{exact}=0)\\
&\land\ \big(\mathrm{instr}.rm=\mathrm{RDN}(2)\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm=\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.45) H, VS/VU: nonzero product exactly cancels addend, RDN → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \neg(e_b=0\land f_b=0)\\
&\land\ \neg(e_c=0\land f_c=0)\\
&\land\ (\mathrm{exact}=0)\\
&\land\ \big(\mathrm{instr}.rm=\mathrm{RDN}(2)\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm=\mathrm{RDN}(2))\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.46) No H, M/S/U: result normal and exact**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert \mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.47) H, M/HS/U: result normal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert \mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.48) H, VS/VU: result normal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert \mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.49) No H, M/S/U: result normal and inexact, set NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert \mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}\ne \mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ \neg\mathrm{tiny}\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.50) H, M/HS/U: result normal and inexact, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert \mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}\ne \mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ \neg\mathrm{tiny}\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.51) H, VS/VU: result normal and inexact, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(2^{E_{\min}}\le\lvert \mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}\ne \mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ \neg\mathrm{tiny}\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.52) No H, M/S/U: result subnormal and exact**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(0<\lvert \mathrm{rounded}\rvert<2^{E_{\min}}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.53) H, M/HS/U: result subnormal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(0<\lvert \mathrm{rounded}\rvert<2^{E_{\min}}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.54) H, VS/VU: result subnormal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(0<\lvert \mathrm{rounded}\rvert<2^{E_{\min}}\big)\\
&\land\ (\mathrm{rounded}=\mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.55) No H, M/S/U: result tiny and inexact, set UF(1), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \mathrm{tiny}\\
&\land\ (\mathrm{rounded}\ne0)\\
&\land\ (\mathrm{rounded}\ne \mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.56) H, M/HS/U: result tiny and inexact, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \mathrm{tiny}\\
&\land\ (\mathrm{rounded}\ne0)\\
&\land\ (\mathrm{rounded}\ne \mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.57) H, VS/VU: result tiny and inexact, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \mathrm{tiny}\\
&\land\ (\mathrm{rounded}\ne0)\\
&\land\ (\mathrm{rounded}\ne \mathrm{exact})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.58) No H, M/S/U: positive underflow to zero → $+0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.59) H, M/HS/U: positive underflow to zero → $+0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.60) H, VS/VU: positive underflow to zero → $+0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.61) No H, M/S/U: negative underflow to zero → $-0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.62) H, M/HS/U: negative underflow to zero → $-0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.63) H, VS/VU: negative underflow to zero → $-0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.64) No H, M/S/U: positive overflow, effective rounding RNE/RMM/RUP → $+\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.65) H, M/HS/U: positive overflow, effective rounding RNE/RMM/RUP → $+\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.66) H, VS/VU: positive overflow, effective rounding RNE/RMM/RUP → $+\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.67) No H, M/S/U: positive overflow, effective rounding RTZ/RDN → $+\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.68) H, M/HS/U: positive overflow, effective rounding RTZ/RDN → $+\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.69) H, VS/VU: positive overflow, effective rounding RTZ/RDN → $+\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}>0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\mathrm{MAX}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.70) No H, M/S/U: negative overflow, effective rounding RNE/RMM/RDN → $-\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.71) H, M/HS/U: negative overflow, effective rounding RNE/RMM/RDN → $-\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.72) H, VS/VU: negative overflow, effective rounding RNE/RMM/RDN → $-\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.73) No H, M/S/U: negative overflow, effective rounding RTZ/RUP → $-\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.74) H, M/HS/U: negative overflow, effective rounding RTZ/RUP → $-\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FNMADD.75) H, VS/VU: negative overflow, effective rounding RTZ/RUP → $-\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ (e_b\ne e_{\max})\\
&\land\ (e_c\ne e_{\max})\\
&\land\ (\mathrm{exact}\ne0)\\
&\land\ \big(\lvert \mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{exact}<0)\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\})\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FNMADD}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\mathrm{MAX}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$
