# FMVH.X.D, FMVH.X.Q — high-word moves

`FMVH.X.D` moves bits 63:32 of $a$ to `rd` and is RV32-only; it is used with `FMV.X.W` to move a double through a pair of integer registers. `FMVH.X.Q` moves bits 127:64 of $a$ to `rd` and is RV64-only; it is used with `FMV.X.D` to move a quad through a pair of integer registers. Neither writes floating-point state, so neither changes `mstatus.FS`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FMVH.X.D.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.D})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMVH.X.D.1) No H, M/S/U: high 32 bits of $a$ → `rd`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.D})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][63:32],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVH.X.D.2) H, M/HS/U: high 32 bits of $a$ → `rd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.D})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][63:32],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVH.X.D.3) H, VS/VU: high 32 bits of $a$ → `rd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=32)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.D})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][63:32],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVH.X.Q.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ \neg\mathrm{impl}(\mathrm{Q})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.Q})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMVH.X.Q.1) No H, M/S/U: high 64 bits of $a$ → `rd`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{Q})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.Q})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][127:64],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVH.X.Q.2) H, M/HS/U: high 64 bits of $a$ → `rd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{Q})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.Q})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][127:64],\ \mathrm{exception}=\varnothing \,\}
$$

**(FMVH.X.Q.3) H, VS/VU: high 64 bits of $a$ → `rd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ \mathrm{impl}(\mathrm{Q})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{XLEN}=64)\\
&\land\ (\mathrm{instr}=\mathrm{FMVH.X.Q})\\
\end{aligned}
\longrightarrow
\{\, rd=f[rs1][127:64],\ \mathrm{exception}=\varnothing \,\}
$$
