# FMV.X.D, FMV.D.X — double-precision moves

`FMV.X.D` copies all 64 bits of $a$ to `rd`; `FMV.D.X` writes all 64 bits of `rs1` to `fd` and boxes them. Neither instruction rounds or raises a flag; `FMV.X.D` leaves the floating-point state unchanged and `FMV.D.X` sets `mstatus.FS` to `Dirty(3)`. Both require `XLEN=64` and `D`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FMV.X.D.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.D})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMV.X.D.1) No H, M/S/U: all bits of $a$ → `rd`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.D})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][63:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.X.D.2) H, M/HS/U: all bits of $a$ → `rd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.D})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][63:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.X.D.3) H, VS/VU: all bits of $a$ → `rd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.D})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][63:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.D.X.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.D.X})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMV.D.X.1) No H, M/S/U: all bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.D.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(x[rs1][63:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.D.X.2) H, M/HS/U: all bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.D.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(x[rs1][63:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.D.X.3) H, VS/VU: all bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.D.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(x[rs1][63:0]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
