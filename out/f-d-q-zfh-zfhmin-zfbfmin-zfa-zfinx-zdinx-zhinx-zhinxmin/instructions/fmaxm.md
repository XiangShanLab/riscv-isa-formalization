# FMAXM — IEEE 754-2019 maximum

`FMAXM` returns the larger of $x=\mathrm{val}_F(a)$ and $y=\mathrm{val}_F(b)$ under the IEEE 754-2019 maximum semantics, with $+0_F$ larger than $-0_F$; any signaling NaN raises `NV(4)`. Requires `Zfa`. Formats H, S, D, Q; the extension condition is `impl(Ext(F)) ∧ impl(Zfa)`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FMAXM.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Ext}(F))\ \lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMAXM.1) No H, M/S/U: a source is not correctly NaN-boxed and another is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\bigl(\mathrm{boxed}_{F}(f[rs1])\land e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs2])\land e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0\land\neg\mathrm{boxed}_{F}(f[rs1])\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.2) No H, M/S/U: a source is not correctly NaN-boxed → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.3) H, M/HS/U: a source is not correctly NaN-boxed and another is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\bigl(\mathrm{boxed}_{F}(f[rs1])\land e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs2])\land e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0\land\neg\mathrm{boxed}_{F}(f[rs1])\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.4) H, M/HS/U: a source is not correctly NaN-boxed → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.5) H, VS/VU: a source is not correctly NaN-boxed and another is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\bigl(\mathrm{boxed}_{F}(f[rs1])\land e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\qquad\lor\ \bigl(\mathrm{boxed}_{F}(f[rs2])\land e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0\land\neg\mathrm{boxed}_{F}(f[rs1])\bigr)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.6) H, VS/VU: a source is not correctly NaN-boxed → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\ \lor\ \neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.7) No H, M/S/U: any NaN and at least one sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.8) H, M/HS/U: any NaN and at least one sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.9) H, VS/VU: any NaN and at least one sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.10) No H, M/S/U: any qNaN and no sNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ \neg(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.11) H, M/HS/U: any qNaN and no sNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ \neg(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.12) H, VS/VU: any qNaN and no sNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ \neg(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=0)\\
&\land\ \big((e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\lor(e_b=e_{\max}\land1\le f_b\le f_{\max}\land f_b[w_f-1]=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.13) No H, M/S/U: both non-NaN → $\max_\prec(a,b)$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(\max_\prec(a,b)),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.14) H, M/HS/U: both non-NaN → $\max_\prec(a,b)$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(\max_\prec(a,b)),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMAXM.15) H, VS/VU: both non-NaN → $\max_\prec(a,b)$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg(e_a=e_{\max}\land f_a\ne0)\\
&\land\ \neg(e_b=e_{\max}\land f_b\ne0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FMAXM}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(\max_\prec(a,b)),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
