# FROUNDNX — round floating-point to integral value

`FROUNDNX` rounds $x=\mathrm{val}_F(a)$ to an integral value using the effective rounding mode and writes it back in format $F$. $\mathrm{ires}=\mathrm{roundInt}(x)$; when the rounded value is zero the sign of $a$ is preserved. An input that is not already integral sets `NX(0)`. Requires `Zfa`. Formats H, S, D, Q; the extension condition is `impl(Ext(F)) ∧ impl(Zfa)`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FROUNDNX.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Ext}(F))\ \lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FROUNDNX.1) No H, M/S/U: the source is not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.2) H, M/HS/U: the source is not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.3) H, VS/VU: the source is not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.4) No H, M/S/U: sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.5) H, M/HS/U: sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.6) H, VS/VU: sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.7) No H, M/S/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.8) H, M/HS/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.9) H, VS/VU: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.10) No H, M/S/U: $+0_F$ → $+0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.11) H, M/HS/U: $+0_F$ → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.12) H, VS/VU: $+0_F$ → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.13) No H, M/S/U: $-0_F$ → $-0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.14) H, M/HS/U: $-0_F$ → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.15) H, VS/VU: $-0_F$ → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.16) No H, M/S/U: $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.17) H, M/HS/U: $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.18) H, VS/VU: $+\infty_F$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.19) No H, M/S/U: $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.20) H, M/HS/U: $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.21) H, VS/VU: $-\infty_F$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.22) No H, M/S/U: finite, nonzero, integral value nonzero and exact**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}\ne0)\\
&\land\ (\mathrm{ires}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(\mathrm{ires}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.23) H, M/HS/U: finite, nonzero, integral value nonzero and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}\ne0)\\
&\land\ (\mathrm{ires}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(\mathrm{ires}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.24) H, VS/VU: finite, nonzero, integral value nonzero and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}\ne0)\\
&\land\ (\mathrm{ires}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(\mathrm{ires}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.25) No H, M/S/U: finite, nonzero, integral value nonzero and inexact, set NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}\ne0)\\
&\land\ (\mathrm{ires}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(\mathrm{ires}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.26) H, M/HS/U: finite, nonzero, integral value nonzero and inexact, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}\ne0)\\
&\land\ (\mathrm{ires}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(\mathrm{ires}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.27) H, VS/VU: finite, nonzero, integral value nonzero and inexact, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}\ne0)\\
&\land\ (\mathrm{ires}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(\mathrm{ires}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.28) No H, M/S/U: finite, nonzero, rounded to zero with $s_a=0$ → $+0_F$, set NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}=0)\\
&\land\ (s_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.29) H, M/HS/U: finite, nonzero, rounded to zero with $s_a=0$ → $+0_F$, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}=0)\\
&\land\ (s_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.30) H, VS/VU: finite, nonzero, rounded to zero with $s_a=0$ → $+0_F$, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}=0)\\
&\land\ (s_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.31) No H, M/S/U: finite, nonzero, rounded to zero with $s_a=1$ → $-0_F$, set NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}=0)\\
&\land\ (s_a=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.32) H, M/HS/U: finite, nonzero, rounded to zero with $s_a=1$ → $-0_F$, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}=0)\\
&\land\ (s_a=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FROUNDNX.33) H, VS/VU: finite, nonzero, rounded to zero with $s_a=1$ → $-0_F$, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{ires}=0)\\
&\land\ (s_a=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FROUNDNX}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$
