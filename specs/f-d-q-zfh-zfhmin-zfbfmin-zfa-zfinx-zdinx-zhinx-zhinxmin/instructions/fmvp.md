# FMVP.D.X, FMVP.Q.X — pair packs

`FMVP.D.X` writes `rs2` in bits 63:32 and `rs1` in bits 31:0 of `fd`, and is RV32-only. `FMVP.Q.X` writes `rs2` in bits 127:64 and `rs1` in bits 63:0 of `fd`, and is RV64-only. Both write floating-point state and set `mstatus.FS` to `Dirty(3)`; neither rounds or raises a flag.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FMVP.D.X.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.D.X})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMVP.D.X.1) No H, M/S/U: pack `rs2`:`rs1` into `fd`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.D.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(x[rs2][31:0]\Vert x[rs1][31:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVP.D.X.2) H, M/HS/U: pack `rs2`:`rs1` into `fd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.D.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(x[rs2][31:0]\Vert x[rs1][31:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVP.D.X.3) H, VS/VU: pack `rs2`:`rs1` into `fd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.D.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(x[rs2][31:0]\Vert x[rs1][31:0]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVP.Q.X.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ \neg\mathrm{impl}(\mathrm{Q})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.Q.X})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMVP.Q.X.1) No H, M/S/U: pack `rs2`:`rs1` into `fd`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{Q})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.Q.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_Q(x[rs2][63:0]\Vert x[rs1][63:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVP.Q.X.2) H, M/HS/U: pack `rs2`:`rs1` into `fd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{Q})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.Q.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_Q(x[rs2][63:0]\Vert x[rs1][63:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVP.Q.X.3) H, VS/VU: pack `rs2`:`rs1` into `fd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{Q})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVP.Q.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_Q(x[rs2][63:0]\Vert x[rs1][63:0]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
