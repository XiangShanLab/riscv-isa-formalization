# FMV.X.W, FMV.W.X — whole-word moves

`FMV.X.W` copies the low 32 bits of $a$ to `rd`, sign-extending to `XLEN`. `FMV.W.X` writes the low 32 bits of `rs1` to `fd` and boxes them. Neither instruction rounds or raises a flag; writing `rd` alone leaves the floating-point state unchanged, while writing `fd` sets `mstatus.FS` to `Dirty(3)`. Requires `F`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FMV.X.W.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.W})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMV.X.W.1) No H, M/S/U: raw bits of $a$ → `rd`, sign-extended to `XLEN`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.W})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(f[rs1][31:0]),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.X.W.2) H, M/HS/U: raw bits of $a$ → `rd`, sign-extended to `XLEN`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.W})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(f[rs1][31:0]),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.X.W.3) H, VS/VU: raw bits of $a$ → `rd`, sign-extended to `XLEN`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.W})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(f[rs1][31:0]),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.W.X.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.W.X})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMV.W.X.1) No H, M/S/U: low 32 bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.W.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_S(x[rs1][31:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.W.X.2) H, M/HS/U: low 32 bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.W.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_S(x[rs1][31:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.W.X.3) H, VS/VU: low 32 bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.W.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_S(x[rs1][31:0]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
