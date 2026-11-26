# FCVT.F.G — floating-point to floating-point conversion

`FCVT.F.G` converts $x=\mathrm{val}_G(a)$ from format $G$ to format $F$ under the effective rounding mode. Narrowing ($G\succ F$) rounds once and may overflow, produce a subnormal, or underflow to zero; widening ($F\succ G$) is always exact. The order $H\prec S\prec D\prec Q$ is the increasing precision order. Both extensions are implemented; since the wider format implies the narrower, the two `impl` conjuncts are redundant but stated explicitly.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FCVT.F.G.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Extm}(F))\ \lor\ \neg\mathrm{impl}(\mathrm{Extm}(G))\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FCVT.F.G.1) No H, M/S/U: the source is not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg\mathrm{boxed}_{G}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.2) H, M/HS/U: the source is not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg\mathrm{boxed}_{G}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.3) H, VS/VU: the source is not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg\mathrm{boxed}_{G}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.4) No H, M/S/U: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.5) H, M/HS/U: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.6) H, VS/VU: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.7) No H, M/S/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.8) H, M/HS/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.9) H, VS/VU: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.10) No H, M/S/U: $+\infty_G$ → $+\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.11) H, M/HS/U: $+\infty_G$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.12) H, VS/VU: $+\infty_G$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.13) No H, M/S/U: $-\infty_G$ → $-\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.14) H, M/HS/U: $-\infty_G$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.15) H, VS/VU: $-\infty_G$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.16) No H, M/S/U: $+0_G$ → $+0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.17) H, M/HS/U: $+0_G$ → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.18) H, VS/VU: $+0_G$ → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.19) No H, M/S/U: $-0_G$ → $-0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.20) H, M/HS/U: $-0_G$ → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.21) H, VS/VU: $-0_G$ → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.22) No H, M/S/U: narrowing, normal and exact**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(x),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.23) H, M/HS/U: narrowing, normal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(x),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.24) H, VS/VU: narrowing, normal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(x),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.25) No H, M/S/U: narrowing, normal and inexact, set NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ \neg\mathrm{tiny}\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.26) H, M/HS/U: narrowing, normal and inexact, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ \neg\mathrm{tiny}\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.27) H, VS/VU: narrowing, normal and inexact, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(2^{E_{\min}}\le\lvert\mathrm{rounded}\rvert<2^{E_{\max}+1}\big)\\
&\land\ (\mathrm{rounded}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ \neg\mathrm{tiny}\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.28) No H, M/S/U: narrowing, positive overflow, effective rounding RNE/RMM/RUP → $+\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.29) H, M/HS/U: narrowing, positive overflow, effective rounding RNE/RMM/RUP → $+\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.30) H, VS/VU: narrowing, positive overflow, effective rounding RNE/RMM/RUP → $+\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.31) No H, M/S/U: narrowing, positive overflow, effective rounding RTZ/RDN → $+\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.32) H, M/HS/U: narrowing, positive overflow, effective rounding RTZ/RDN → $+\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.33) H, VS/VU: narrowing, positive overflow, effective rounding RTZ/RDN → $+\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RDN}(2)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\mathrm{MAX}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.34) No H, M/S/U: narrowing, negative overflow, effective rounding RNE/RMM/RDN → $-\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.35) H, M/HS/U: narrowing, negative overflow, effective rounding RNE/RMM/RDN → $-\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.36) H, VS/VU: narrowing, negative overflow, effective rounding RNE/RMM/RDN → $-\infty_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RDN}(2),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.37) No H, M/S/U: narrowing, negative overflow, effective rounding RTZ/RUP → $-\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.38) H, M/HS/U: narrowing, negative overflow, effective rounding RTZ/RUP → $-\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\mathrm{MAX}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.39) H, VS/VU: narrowing, negative overflow, effective rounding RTZ/RUP → $-\mathrm{MAX}_F$, set OF(2), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RTZ}(1),\mathrm{RUP}(3)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}+1}\big)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\mathrm{MAX}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{OF}(2),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.40) No H, M/S/U: narrowing, subnormal and exact**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(0<\lvert\mathrm{rounded}\rvert<2^{E_{\min}}\big)\\
&\land\ (\mathrm{rounded}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.41) H, M/HS/U: narrowing, subnormal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(0<\lvert\mathrm{rounded}\rvert<2^{E_{\min}}\big)\\
&\land\ (\mathrm{rounded}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.42) H, VS/VU: narrowing, subnormal and exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \big(0<\lvert\mathrm{rounded}\rvert<2^{E_{\min}}\big)\\
&\land\ (\mathrm{rounded}=x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.43) No H, M/S/U: narrowing, tiny and inexact, set UF(1), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \mathrm{tiny}\\
&\land\ (\mathrm{rounded}\ne0)\\
&\land\ (\mathrm{rounded}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.44) H, M/HS/U: narrowing, tiny and inexact, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \mathrm{tiny}\\
&\land\ (\mathrm{rounded}\ne0)\\
&\land\ (\mathrm{rounded}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.45) H, VS/VU: narrowing, tiny and inexact, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ \mathrm{tiny}\\
&\land\ (\mathrm{rounded}\ne0)\\
&\land\ (\mathrm{rounded}\ne x)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{rounded}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.46) No H, M/S/U: narrowing, positive underflow to zero → $+0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.47) H, M/HS/U: narrowing, positive underflow to zero → $+0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.48) H, VS/VU: narrowing, positive underflow to zero → $+0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (x>0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.49) No H, M/S/U: narrowing, negative underflow to zero → $-0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.50) H, M/HS/U: narrowing, negative underflow to zero → $-0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.51) H, VS/VU: narrowing, negative underflow to zero → $-0_F$, set UF(1), NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (\mathrm{rounded}=0)\\
&\land\ (x<0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (F\prec G)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{UF}(1),\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W1) No H, M/S/U: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W2) H, M/HS/U: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W3) H, VS/VU: any source is sNaN → canonical qNaN, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W4) No H, M/S/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W5) H, M/HS/U: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W6) H, VS/VU: only qNaN → canonical qNaN, no flags**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ \neg(e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=0)\\
&\land\ (e_a=e_{\max,G}\land1\le f_a\le f_{\max,G}\land f_a[w_G-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{qNaN}_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W7) No H, M/S/U: $+\infty_G$ → $+\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W8) H, M/HS/U: $+\infty_G$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W9) H, VS/VU: $+\infty_G$ → $+\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W10) No H, M/S/U: $-\infty_G$ → $-\infty_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W11) H, M/HS/U: $-\infty_G$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W12) H, VS/VU: $-\infty_G$ → $-\infty_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=e_{\max,G}\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-\infty_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W13) No H, M/S/U: $+0_G$ → $+0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W14) H, M/HS/U: $+0_G$ → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W15) H, VS/VU: $+0_G$ → $+0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=0\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(+0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W16) No H, M/S/U: $-0_G$ → $-0_F$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W17) H, M/HS/U: $-0_G$ → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W18) H, VS/VU: $-0_G$ → $-0_F$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (s_a=1\land e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(-0_F),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W19) No H, M/S/U: widening → exact**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(x),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W20) H, M/HS/U: widening → exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(x),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVT.F.G.W21) H, VS/VU: widening → exact**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Extm}(F))\\
&\land\ \mathrm{impl}(\mathrm{Extm}(G))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\lor(\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\big)\\
&\land\ (e_a\ne e_{\max,G})\\
&\land\ \neg(e_a=0\land f_a=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (G\prec F)\\
&\land\ (\mathrm{instr}=\mathrm{FCVT}.F.G)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_F(x),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
